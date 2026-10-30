import datetime as dt, json, os, re, subprocess, sys, time, urllib.request

W = "/var/lib/docker/volumes/advisor-data/_data/study"
VOL = "/var/lib/docker/volumes/advisor-data/_data"
ADVISOR = "http://192.168.75.225:8765/ask"
SECRET = open("/root/.advisor-secret").read().strip()
PROVIDERS = os.environ.get("REV_PROVIDERS", "deepseek,qwen,grok,gemini_junghhco1").split(",")
MAX_PER_RUN = int(os.environ.get("REV_MAX", "2"))
MAX_ROUNDS = int(os.environ.get("REV_ROUNDS", "5"))
MIN_GAP_H = float(os.environ.get("REV_GAP_H", "6"))
IMAGE = os.environ.get("REV_IMAGE", "advisor-mcp:fw29")
KST = dt.timezone(dt.timedelta(hours=9))

REVIEW = """너는 고1 {subject} 교과서 검토 위원이다. 아래 [교과서 원문]은 「{code} {title}」(교과서 {pages}쪽)이고, [개념정리]는 학생용으로 작성한 정리본이다.
교과서 원문만 근거로 개념정리를 검토하고, 아래 형식의 JSON 하나만 ```json 코드블록으로 출력하라. 다른 말은 쓰지 마라.
{{"missing": [{{"point": "교과서에 있으나 개념정리에 빠진 시험 대상 내용", "page": "쪽", "add": "추가할 문장(교과서 근거)"}}],
 "errors": [{{"wrong": "개념정리의 틀리거나 교과서와 다른 서술", "right": "교과서에 따른 바른 내용", "page": "쪽"}}],
 "unclear": ["학생이 오해할 수 있는 모호한 설명"],
 "score": 1~10 정수 (교과서 대비 정확성·완결성)}}
교과서에 없는 내용을 요구하지 마라. 사소한 표현 취향은 지적하지 마라.

[교과서 원문]
{source}

[개념정리]
{report}"""

REVISE = """아래 [개념정리]를 [검토 의견]에 따라 보완하라. 근거는 [교과서 원문]뿐이다.
규칙: 기존 구성과 제목(# 제목, ## 학습 목표 / ## 핵심 개념 / ## 비교·정리표 / ## 시험 함정 포인트 / ## 핵심 용어 사전 / ## 자기점검 질문)을 그대로 유지한다. 검토 의견 중 교과서로 확인되는 것만 반영하고, 나머지 내용은 지우거나 줄이지 마라. 수식은 LaTeX 금지(유니코드). 주요 개념 끝의 (p.NN) 쪽 표기를 유지한다.
완성된 개념정리 전체를 ```markdown 코드블록 하나로만 출력하라.

[검토 의견]
{review}

[교과서 원문]
{source}

[개념정리]
{report}"""


def now():
    return dt.datetime.now(KST)


def ask(prompt, provider, timeout_s=420):
    body = json.dumps({"provider": provider, "prompt": prompt, "timeout_s": timeout_s}).encode()
    req = urllib.request.Request(ADVISOR, data=body, headers={"content-type": "application/json", "x-advisor-secret": SECRET})
    with urllib.request.urlopen(req, timeout=timeout_s + 120) as r:
        j = json.loads(r.read())
    if not j.get("answer"):
        raise RuntimeError(str(j)[:200])
    return j


def clean(a):
    a = a.replace(" ", " ")
    a = re.sub(r"^[ \t]*\d+[ \t]*$", "", a, flags=re.M)
    return re.sub(r"^[ \t]*(json|JSON|markdown|복사|Copy)[ \t]*$", "", a, flags=re.M)


def parse_json(answer):
    a = clean(answer)
    cands = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", a, re.S)
    if "{" in a:
        cands.append(a[a.find("{"):a.rfind("}") + 1])
    for c in cands:
        try:
            return json.loads(c)
        except Exception:
            continue
    raise ValueError("no JSON in answer")


def parse_md(answer):
    m = re.search(r"```(?:markdown|md)?\s*\n(.*)\n```", answer, re.S)
    return (m.group(1) if m else answer).strip() + "\n"


def nlm(*args, timeout=900):
    cmd = ["docker", "run", "--rm", "--entrypoint", "notebooklm", "-v", "advisor-data:/data", "-e", "NOTEBOOKLM_HOME=/data/notebooklm", IMAGE, *args]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def source_text(s, u):
    path = os.path.join(W, "sources_text", s["id"], f"{u['id']}.txt")
    text = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if len(text) >= 1500 or not u.get("source"):
        return text
    nb = open(os.path.join(W, "transcript_nb.txt")).read().strip()
    rel = "/data/study/" + u["source"]
    rc, out, err = nlm("source", "add", rel, "--type", "file", "--title", f"ocr {s['id']} {u['id']}", "-n", nb, "--json")
    try:
        j = json.loads(out[out.find("{"):]) if "{" in out else {}
    except Exception:
        j = {}
    sid = j.get("id") or (j.get("source") or {}).get("id") or j.get("source_id")
    if not sid:
        raise RuntimeError(f"ocr source add failed: {(err or out)[-200:]}")
    try:
        nlm("source", "wait", sid, "-n", nb)
        tmp = f"/data/study/sources_text/{s['id']}/{u['id']}.ocr.txt"
        nlm("source", "fulltext", sid, "-n", nb, "-o", tmp, "--force")
        host = os.path.join(VOL, tmp[len("/data/"):])
        if os.path.exists(host):
            text = open(host, encoding="utf-8").read()
            os.replace(host, path)
    finally:
        nlm("source", "delete", sid, "-n", nb, "--yes")
    return text


def valid(new, old):
    heads = [l.strip() for l in old.splitlines() if l.startswith("## ")]
    probs = [h for h in heads if h not in new]
    if len(new) < 0.9 * len(old):
        probs.append(f"shorter {len(new)}<{len(old)}")
    if re.search(r"\\\(|\$\$|\\frac", new):
        probs.append("latex")
    return probs


def review_unit(s, u, rpath, rv):
    n = len(rv["rounds"]) + 1
    reviewer = PROVIDERS[(n - 1) % len(PROVIDERS)]
    report = open(rpath, encoding="utf-8").read()
    src = source_text(s, u)[:40000]
    if len(src) < 300:
        raise RuntimeError("no textbook text")
    t0 = time.time()
    order = [reviewer] + [p for p in PROVIDERS if p != reviewer]
    errs, rj, used = [], None, None
    for prov in order:
        try:
            rj = parse_json(ask(REVIEW.format(subject=s["name"], code=u["code"], title=u["title"], pages=u["pages"], source=src, report=report), prov)["answer"])
            used = prov
            break
        except Exception as e:
            errs.append(f"{prov}: {str(e)[:80]}")
    if rj is None:
        raise RuntimeError("; ".join(errs))
    missing, errors = rj.get("missing") or [], rj.get("errors") or []
    rnd = {"n": n, "reviewer": used, "at": now().isoformat(timespec="seconds"), "score": rj.get("score"), "missing": missing,
           "errors": errors, "unclear": rj.get("unclear") or [], "applied": "none", "review_secs": round(time.time() - t0)}
    if missing or errors:
        reviser_order = [p for p in PROVIDERS if p != used] + [used]
        new, probs = None, []
        for prov in reviser_order[:3]:
            try:
                cand = parse_md(ask(REVISE.format(review=json.dumps({"missing": missing, "errors": errors, "unclear": rnd["unclear"]}, ensure_ascii=False, indent=1), source=src, report=report), prov, 600)["answer"])
                p = valid(cand, report)
                if not p:
                    new, rnd["reviser"] = cand, prov
                    break
                probs.append(f"{prov}: " + ", ".join(p)[:160])
            except Exception as e:
                probs.append(f"{prov}: {str(e)[:80]}")
        os.replace(rpath, rpath.replace("_report.md", f"_report.v{n}.md"))
        if new:
            body, rnd["applied"] = new, "rewrite"
        else:
            note = [f"\n## 보완 노트 (외부 리뷰 {n}차 · {used})"]
            note += [f"- **빠진 내용** {m.get('point', '')} — {m.get('add', '')} (p.{m.get('page', '')})" for m in missing]
            note += [f"- **바로잡기** '{e.get('wrong', '')}' → {e.get('right', '')} (p.{e.get('page', '')})" for e in errors]
            body, rnd["applied"], rnd["rewrite_problems"] = report.rstrip() + "\n" + "\n".join(note) + "\n", "note", probs
        open(rpath, "w", encoding="utf-8").write(body)
        os.chown(rpath, 1001, 1001)
    rv["rounds"].append(rnd)
    sc = rj.get("score") or 0
    if (isinstance(sc, (int, float)) and sc >= 9 and len(missing) + len(errors) <= 1) or n >= MAX_ROUNDS:
        rv["done"] = True
    return rnd


def main():
    cat = json.load(open(os.path.join(W, "catalog.json"), encoding="utf-8"))
    only = sys.argv[1] if len(sys.argv) > 1 else None
    cands = []
    for s in cat["subjects"]:
        for u in s["units"]:
            rpath = os.path.join(W, "out", s["id"], f"{u['id']}_report.md")
            if not os.path.exists(rpath) or (only and f"{s['id']}/{u['id']}" != only):
                continue
            vpath = rpath.replace("_report.md", "_report.review.json")
            rv = json.load(open(vpath, encoding="utf-8")) if os.path.exists(vpath) else {"rounds": [], "done": False}
            if rv.get("done") and not only:
                continue
            last = rv["rounds"][-1]["at"] if rv["rounds"] else ""
            if last and (now() - dt.datetime.fromisoformat(last)).total_seconds() < MIN_GAP_H * 3600 and not only:
                continue
            cands.append((len(rv["rounds"]), last, s, u, rpath, vpath, rv))
    cands.sort(key=lambda c: (c[0], c[1]))
    for _, _, s, u, rpath, vpath, rv in cands[:MAX_PER_RUN]:
        try:
            rnd = review_unit(s, u, rpath, rv)
            json.dump(rv, open(vpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.chown(vpath, 1001, 1001)
            print(now().strftime("%F %T"), "reviewed", f"{s['id']}/{u['id']}", "round", rnd["n"], "by", rnd["reviewer"], "score", rnd["score"],
                  "missing", len(rnd["missing"]), "errors", len(rnd["errors"]), "applied", rnd["applied"], rnd.get("reviser", ""), rnd.get("rewrite_problems", ""), flush=True)
        except Exception as e:
            print(now().strftime("%F %T"), "review failed", f"{s['id']}/{u['id']}", str(e)[:300], flush=True)


if __name__ == "__main__":
    main()
