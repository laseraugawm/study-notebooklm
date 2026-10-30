import json, os, re, subprocess, sys, time, urllib.request

W = "/var/lib/docker/volumes/advisor-data/_data/study"
ADVISOR = "http://192.168.75.225:8765/ask"
SECRET = open("/root/.advisor-secret").read().strip()
PROVIDERS = os.environ.get("DESC_PROVIDERS", "deepseek,qwen,grok,gemini_junghhco1").split(",")
MAX_PER_RUN = int(os.environ.get("DESC_MAX", "3"))
IMAGE = os.environ.get("DESC_IMAGE", "advisor-mcp:fw29")
KIND_KO = {"audio": "오디오 요약", "video": "영상 해설"}

PROMPT = """아래 [대본]은 고1 {subject} 「{code} {title}」(교과서 {pages}쪽) 학습용 {kind}({dur})를 받아쓴 것이고, [개념정리]는 같은 단원의 개념정리다.
대본에 실제로 나온 내용만 근거로, 아래 형식의 JSON 하나만 ```json 코드블록으로 출력하라. 다른 말은 쓰지 마라.
{{"chapters": ["대본 흐름 순서대로 구간 제목 3~8개"],
 "concepts": ["대본에서 실제로 설명한 핵심 개념"],
 "missing": ["개념정리에는 있으나 대본에서 다루지 않은, 시험 대비에 필요한 개념 (중요한 것부터)"],
 "errors": ["대본 내용 중 개념정리와 어긋나거나 부정확한 진술 (받아쓰기 오타는 제외, 없으면 빈 배열)"]{still_field}}}

{focus_block}[대본]
{transcript}

[개념정리]
{report}"""


def nlm(*args, timeout=600):
    cmd = ["docker", "run", "--rm", "--entrypoint", "notebooklm", "-v", "advisor-data:/data", "-e", "NOTEBOOKLM_HOME=/data/notebooklm", IMAGE, *args]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def jparse(s):
    for i in (0, s.find("{")):
        if i < 0:
            continue
        try:
            return json.loads(s[i:])
        except Exception:
            pass
    return {}


def dur_of(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    try:
        return float(p.stdout.strip())
    except ValueError:
        return 0.0


def mmss(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def transcript_nb():
    path = os.path.join(W, "transcript_nb.txt")
    if os.path.exists(path):
        return open(path).read().strip()
    rc, out, err = nlm("create", "학습자료 미디어 대본", "--json")
    j = jparse(out)
    nb = j.get("id") or (j.get("notebook") or {}).get("id")
    if not nb:
        raise RuntimeError(f"create transcript notebook: {(err or out)[-200:]}")
    open(path, "w").write(nb)
    return nb


def transcribe(audio_host_path, title):
    nb = transcript_nb()
    rel = "/data/" + os.path.relpath(audio_host_path, "/var/lib/docker/volumes/advisor-data/_data")
    rc, out, err = nlm("source", "add", rel, "--type", "file", "--title", title, "-n", nb, "--json", timeout=900)
    j = jparse(out)
    sid = j.get("id") or (j.get("source") or {}).get("id") or j.get("source_id")
    if not sid:
        raise RuntimeError(f"source add: {(err or out)[-300:]}")
    try:
        nlm("source", "wait", sid, "-n", nb, timeout=900)
        tmp = rel.rsplit(".", 1)[0] + ".transcript.txt"
        rc, out, err = nlm("source", "fulltext", sid, "-n", nb, "-o", tmp, "--force")
        host_tmp = os.path.join("/var/lib/docker/volumes/advisor-data/_data", tmp[len("/data/"):])
        text = open(host_tmp, encoding="utf-8").read().strip() if os.path.exists(host_tmp) else ""
        if os.path.exists(host_tmp):
            os.remove(host_tmp)
        rc, out, err = nlm("source", "guide", sid, "-n", nb, "--json")
        guide = jparse(out)
        return text, guide
    finally:
        nlm("source", "delete", sid, "-n", nb, "--yes")


def ask(prompt, provider):
    body = json.dumps({"provider": provider, "prompt": prompt, "timeout_s": 300}).encode()
    req = urllib.request.Request(ADVISOR, data=body, headers={"content-type": "application/json", "x-advisor-secret": SECRET})
    with urllib.request.urlopen(req, timeout=420) as r:
        return json.loads(r.read())


def parse(answer):
    a = answer.replace(" ", " ")
    a = re.sub(r"^[ 	]*\d+[ 	]*$", "", a, flags=re.M)
    a = re.sub(r"^[ 	]*(json|JSON|복사|Copy)[ 	]*$", "", a, flags=re.M)
    cands = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", a, re.S)
    if "{" in a:
        cands.append(a[a.find("{"):a.rfind("}") + 1])
    for c in cands:
        try:
            return json.loads(c)
        except Exception:
            continue
    raise ValueError("no JSON object in answer")


def describe(s, u, kind, rec, focus=None):
    media = os.path.join(W, "out", next(f["file"] for f in rec["files"] if f["ok"]))
    out = media.rsplit(".", 1)[0] + ".desc.json"
    audio = media
    base = kind.split("_s")[0]
    if base == "video":
        audio = media.rsplit(".", 1)[0] + ".track.m4a"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", media, "-vn", "-ac", "1", "-b:a", "64k", audio], check=True)
        os.chown(audio, 1001, 1001)
    dur = dur_of(audio)
    t0 = time.time()
    try:
        text, guide = transcribe(audio, f"{s['id']} {u['id']} {kind}")
    finally:
        if audio != media and os.path.exists(audio):
            os.remove(audio)
    if len(text) < 50:
        raise RuntimeError(f"transcript empty ({len(text)} chars)")
    rep = os.path.join(W, "out", s["id"], f"{u['id']}_report.md")
    report = open(rep, encoding="utf-8").read() if os.path.exists(rep) else "(개념정리 없음)"
    d = {"summary": guide.get("summary", ""), "keywords": guide.get("keywords", []), "chapters": [], "concepts": [], "missing": [], "errors": []}
    try:
        fb = ("[보충 초점] 이 자료는 다음 개념을 채우라는 지시로 만든 보충 자료다:\n- " + "\n- ".join(focus) + "\n\n") if focus else ""
        sf = ',\n "still_missing": ["보충 초점 중 대본에서 실제로 다루지 않은 것"]' if focus else ""
        q = PROMPT.format(subject=s["name"], code=u["code"], title=u["title"], pages=u["pages"], kind=KIND_KO[base] + (" 보충" if focus else ""), dur=mmss(dur), transcript=text, report=report[:14000], focus_block=fb, still_field=sf)
        errs = []
        for prov in PROVIDERS:
            try:
                r = ask(q, prov)
                j = parse(r.get("answer", ""))
                if not isinstance(j, dict) or "missing" not in j:
                    raise ValueError("no missing field")
                d.update({k: v for k, v in j.items() if k in ("chapters", "concepts", "missing", "errors", "still_missing")})
                d["analyzer"] = r.get("provider", prov)
                break
            except Exception as e:
                errs.append(f"{prov}: {str(e)[:80]}")
        else:
            raise RuntimeError("; ".join(errs))
        if errs:
            d["analyzer_fallbacks"] = errs
    except Exception as e:
        d["analyzer_error"] = str(e)[:200]
    if focus:
        d["focus"] = focus
    d.update({"kind": kind, "duration": round(dur), "transcript": text, "made_secs": round(time.time() - t0), "made_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
    json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.chown(out, 1001, 1001)
    return d


SUPS = os.path.join(W, "sups.json")
MAX_SUPS = 3


def plan_sups(sid, uid, kind, d):
    sups = json.load(open(SUPS, encoding="utf-8")) if os.path.exists(SUPS) else []
    base, n = (kind.split("_s")[0], int(kind.split("_s")[1])) if "_s" in kind else (kind, 0)
    need = d.get("still_missing") if n else d.get("missing")
    need = [x for x in (need or []) if x]
    if len(need) < (2 if n else 3) or n >= MAX_SUPS:
        return None
    nid = f"{base}_s{n + 1}"
    if any(x["subject"] == sid and x["unit"] == uid and x["id"] == nid for x in sups):
        return None
    sups.append({"id": nid, "subject": sid, "unit": uid, "kind": base, "focus": need[:6], "from": f"{sid}/{uid}/{kind}", "created": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
    tmp = SUPS + ".tmp"
    json.dump(sups, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, SUPS)
    os.chown(SUPS, 1001, 1001)
    return nid


def main():
    cat = json.load(open(os.path.join(W, "catalog.json"), encoding="utf-8"))
    st = json.load(open(os.path.join(W, "state.json"), encoding="utf-8"))
    sups = json.load(open(SUPS, encoding="utf-8")) if os.path.exists(SUPS) else []
    focus_of = {f"{x['subject']}/{x['unit']}/{x['id']}": x["focus"] for x in sups}
    units = {(s["id"], u["id"]): (s, u) for s in cat["subjects"] for u in s["units"]}
    only = sys.argv[1] if len(sys.argv) > 1 else None
    n = 0
    for key, rec in sorted(st["done"].items(), key=lambda kv: kv[1].get("at", "")):
        sid, uid, kind = key.split("/")
        if kind.split("_s")[0] not in ("audio", "video") or (only and key != only) or (sid, uid) not in units:
            continue
        media = os.path.join(W, "out", next(f["file"] for f in rec["files"] if f["ok"]))
        dpath = media.rsplit(".", 1)[0] + ".desc.json"
        if os.path.exists(dpath):
            nid = plan_sups(sid, uid, kind, json.load(open(dpath, encoding="utf-8")))
            if nid:
                print(time.strftime("%F %T"), "planned", f"{sid}/{uid}/{nid}", "from existing", key, flush=True)
            continue
        if n >= MAX_PER_RUN:
            continue
        n += 1
        s, u = units[(sid, uid)]
        try:
            d = describe(s, u, kind, rec, focus_of.get(key))
            nid = plan_sups(sid, uid, kind, d)
            print(time.strftime("%F %T"), "described", key, len(d["transcript"]), "chars", "missing", len(d.get("missing", [])), "still", len(d.get("still_missing", [])), "-> sup", nid, d.get("analyzer_error", ""), flush=True)
        except Exception as e:
            print(time.strftime("%F %T"), "describe failed", key, str(e)[:300], flush=True)


if __name__ == "__main__":
    main()
