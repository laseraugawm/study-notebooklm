import datetime as dt, json, os, subprocess, sys, time

W = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(W, "catalog.json")
CONFIG = os.path.join(W, "config.json")
STATE = os.path.join(W, "state.json")
LOG = os.path.join(W, "log.jsonl")
SUPS = os.path.join(W, "sups.json")
FOCUS = {}
KST = dt.timezone(dt.timedelta(hours=9))

CTX = "고1 {subject} 시험대비. 이 소스(교과서 해당 쪽) 내용만 사용하고, 모든 출력은 한국어로."
KINDS = {
    "report": ("report", lambda c: ["report", "--format", "study-guide", "--language", "ko", "--append", c + " 핵심 용어는 굵게, 정의·분류·비교표를 포함하고, 시험에서 헷갈리기 쉬운 함정 포인트를 따로 정리."], 900),
    "quiz": ("quiz", lambda c: ["quiz", c + " 핵심 개념과 헷갈리기 쉬운 세부 사항을 묻는 객관식.", "--difficulty", "medium", "--quantity", "standard"], 900),
    "flashcards": ("flashcards", lambda c: ["flashcards", c + " 핵심 용어와 정의, 비교 포인트.", "--quantity", "standard"], 900),
    "audio": ("audio", lambda c: ["audio", c + " 시험 직전 복습용 핵심 요약.", "--format", "brief", "--length", "short", "--language", "ko"], 3600),
    "video": ("video", lambda c: ["video", c + " 개념을 그림으로 설명하는 해설 영상.", "--format", "explainer", "--style", "whiteboard", "--language", "ko"], 3600),
}
EXT = {"report": [("md", [])], "quiz": [("json", ["--format", "json"]), ("md", ["--format", "markdown"])],
       "flashcards": [("json", ["--format", "json"]), ("md", ["--format", "markdown"])],
       "audio": [("m4a", [])], "video": [("mp4", [])]}
LIMIT_WORDS = ("ratelimit", "rate limit", "quota", "한도", "too many", "exceeded", "resource_exhausted")
DEFAULT_CONFIG = {"budget": {"report": 8, "quiz": 5, "flashcards": 4, "audio": 3, "video": 1}, "slots_per_day": 3, "gap_s": 180,
                  "max_fails": 3, "order": ["social", "science", "info", "korean", "english", "math"]}


def now():
    return dt.datetime.now(KST)


def today():
    return now().strftime("%Y-%m-%d")


def jload(p, d):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return d


def jsave(p, v):
    tmp = p + ".tmp"
    json.dump(v, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, p)


def log(**kw):
    kw = {"at": now().isoformat(timespec="seconds"), **kw}
    print(json.dumps(kw, ensure_ascii=False), flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(kw, ensure_ascii=False) + "\n")


def nlm(args, timeout=600):
    try:
        p = subprocess.run(["notebooklm", *args], capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def jparse(s):
    for i in (0, s.find("{"), s.find("[")):
        if i < 0:
            continue
        try:
            return json.loads(s[i:])
        except Exception:
            pass
    return None


def artifacts(nb):
    rc, out, err = nlm(["artifact", "list", "-n", nb, "--json"], 120)
    j = jparse(out) or {}
    items = j.get("artifacts", []) if isinstance(j, dict) else j
    return {str(a.get("id")): a for a in items if isinstance(a, dict)}


def pending(cat, st, cfg):
    order = {s: i for i, s in enumerate(cfg["order"])}
    subs = sorted(cat["subjects"], key=lambda s: order.get(s["id"], 99))
    out = {k: [] for k in KINDS}
    for s in subs:
        for u in s["units"]:
            for kind, (group, _, _) in KINDS.items():
                key = f"{s['id']}/{u['id']}/{kind}"
                if key in st["done"] or st["fails"].get(key, 0) >= cfg["max_fails"]:
                    continue
                if not u.get("source") and not u.get("source_id"):
                    continue
                out[group].append((s, u, kind, key))
    units = {(s["id"], u["id"]): (s, u) for s in cat["subjects"] for u in s["units"]}
    sup = {k: [] for k in KINDS}
    for sp in jload(SUPS, []):
        su = units.get((sp["subject"], sp["unit"]))
        key = f"{sp['subject']}/{sp['unit']}/{sp['id']}"
        if not su or key in st["done"] or st["fails"].get(key, 0) >= cfg["max_fails"]:
            continue
        FOCUS[key] = sp["focus"]
        sup[sp["kind"]].append((su[0], su[1], sp["id"], key))
    every = max(1, cfg.get("sup_every", 3))
    for g in out:
        merged, base, extra = [], out[g], sup[g]
        while base or extra:
            merged.extend(base[:every]); base = base[every:]
            if extra:
                merged.append(extra.pop(0))
        out[g] = merged
    return out


def ensure_source(s, u, st):
    nbk = u.get("notebook") or st["notebooks"].get(s["id"])
    if not nbk:
        rc, out, err = nlm(["create", f"고1 {s['name']} 소단원 학습자료", "--json"])
        j = jparse(out) or {}
        nbk = j.get("id") or (j.get("notebook") or {}).get("id")
        if not nbk:
            raise RuntimeError(f"create notebook failed: {(err or out)[-300:]}")
        st["notebooks"][s["id"]] = nbk
        log(event="notebook", subject=s["id"], notebook=nbk)
    skey = f"{s['id']}/{u['id']}"
    sid = u.get("source_id") or st["sources"].get(skey)
    if not sid:
        title = f"{u['code']} {u['title']} (p{u['pages']})"
        rc, out, err = nlm(["source", "add", os.path.join(W, u["source"]), "--type", "file", "--title", title, "-n", nbk, "--json"], 900)
        j = jparse(out) or {}
        sid = j.get("id") or (j.get("source") or {}).get("id") or j.get("source_id")
        if not sid:
            raise RuntimeError(f"source add failed: {(err or out)[-300:]}")
        st["sources"][skey] = sid
        log(event="source", key=skey, source=sid)
        time.sleep(30)
    return nbk, sid


def run_one(s, u, kind, key, st):
    nbk, sid = ensure_source(s, u, st)
    base = kind.split("_s")[0]
    group, gen, tmo = KINDS[base]
    ctx = CTX.format(subject=s["name"])
    if key in FOCUS:
        ctx += " 이번 자료는 보충용이다. 다음 개념만 집중해서, 앞선 자료에서 빠졌던 내용을 채우도록 설명하라: " + "; ".join(FOCUS[key]) + "."
    before = set(artifacts(nbk))
    t0 = time.time()
    rc, out, err = nlm(["generate", *gen(ctx), "-n", nbk, "-s", sid, "--wait", "--timeout", str(tmo), "--json"], tmo + 180)
    secs = round(time.time() - t0)
    after = artifacts(nbk)
    new = [a for i, a in after.items() if i not in before]
    j = jparse(out) or {}
    aid = str(new[0].get("id")) if new else (j.get("artifact_id") if isinstance(j, dict) else None)
    text = (out + err).lower()
    if rc != 0 or not aid:
        limited = any(w in text for w in LIMIT_WORDS)
        return {"ok": False, "limited": limited, "secs": secs, "err": (err or out)[-300:]}
    odir = os.path.join(W, "out", s["id"])
    os.makedirs(odir, exist_ok=True)
    files = []
    for ext, extra in EXT[base]:
        path = os.path.join(odir, f"{u['id']}_{kind}.{ext}")
        drc, dout, derr = nlm(["download", base, path, "-a", aid, "-n", nbk, *extra], 900)
        files.append({"file": f"{s['id']}/{os.path.basename(path)}", "ok": drc == 0 and os.path.exists(path),
                      "bytes": os.path.getsize(path) if os.path.exists(path) else 0})
    ok = all(f["ok"] for f in files)
    return {"ok": ok, "limited": False, "secs": secs, "artifact": aid, "files": files, "err": "" if ok else "download failed"}


def main():
    cfg = {**DEFAULT_CONFIG, **jload(CONFIG, {})}
    cat = jload(CATALOG, {"subjects": []})
    st = jload(STATE, {})
    for k in ("notebooks", "sources", "done", "fails", "blocked", "daily"):
        st.setdefault(k, {})
    redo_path = os.path.join(W, "redo.json")
    for r in jload(redo_path, []):
        import fnmatch
        for key in [k for k, v in st["done"].items() if fnmatch.fnmatch(k, r["pattern"]) and v.get("at", "") < r.get("before", "9999")]:
            for f in st["done"][key].get("files", []):
                try:
                    os.remove(os.path.join(W, "out", f["file"]))
                except OSError:
                    pass
            st["done"].pop(key)
            st["fails"].pop(key, None)
            log(event="redo", key=key, reason=r.get("reason", ""))
    if os.path.exists(redo_path):
        os.replace(redo_path, redo_path + ".applied")
    d = today()
    st["daily"].setdefault(d, {})
    st["last_run"] = now().isoformat(timespec="seconds")
    jsave(STATE, st)
    todo = pending(cat, st, cfg)
    per_slot = {g: max(1, -(-cfg["budget"][g] // cfg["slots_per_day"])) for g in todo}
    did_any = False
    for g in KINDS:
        if st["blocked"].get(g, "") > now().isoformat():
            log(event="skip_blocked", group=g, until=st["blocked"][g])
            continue
        n_slot = 0
        for s, u, kind, key in todo[g]:
            used = st["daily"][d].get(g, 0)
            if used >= cfg["budget"][g] or n_slot >= per_slot[g]:
                break
            if did_any:
                time.sleep(cfg["gap_s"])
            did_any = True
            try:
                r = run_one(s, u, kind, key, st)
            except Exception as e:
                r = {"ok": False, "limited": False, "secs": 0, "err": str(e)[-300:]}
            st["daily"][d][g] = used + 1
            n_slot += 1
            if r["ok"]:
                st["done"][key] = {"artifact": r["artifact"], "files": r["files"], "secs": r["secs"], "at": now().isoformat(timespec="seconds")}
                st["fails"].pop(key, None)
                log(event="done", key=key, secs=r["secs"], files=r["files"])
            else:
                st["fails"][key] = st["fails"].get(key, 0) + (0 if r["limited"] else 1)
                log(event="limited" if r["limited"] else "failed", key=key, secs=r["secs"], err=r["err"])
                if r["limited"]:
                    tomorrow = (now() + dt.timedelta(days=1)).replace(hour=0, minute=30, second=0, microsecond=0)
                    st["blocked"][g] = tomorrow.isoformat()
                    st["daily"][d][g] = used
                    jsave(STATE, st)
                    break
            jsave(STATE, st)
    log(event="run_end", daily=st["daily"][d])
    jsave(STATE, st)


if __name__ == "__main__":
    lock = os.path.join(W, ".lock")
    import fcntl
    with open(lock, "w") as lf:
        try:
            fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("already running"); sys.exit(0)
        main()
