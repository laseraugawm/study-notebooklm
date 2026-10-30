import datetime as dt, json, os, shutil, subprocess, urllib.request

W = "/var/lib/docker/volumes/advisor-data/_data/study"
REPO = "/root/study-notebooklm"
DATA = os.path.join(REPO, "data")
KST = dt.timezone(dt.timedelta(hours=9))
OWNER = "laseraugawm"
SHARD_BYTES = 900 * 1024 * 1024
MEDIA_STATE = "/root/study-media.json"
TOKEN = open("/root/.gh-laseraugawm").read().strip()
GROUP = {"report": "report", "quiz": "quiz", "flashcards": "flashcards", "audio": "audio", "video": "video"}
KIND_KO = {"report": "개념정리", "quiz": "퀴즈", "flashcards": "플래시카드", "audio": "오디오", "video": "비디오"}


def jload(p, d):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return d


def kname(k):
    if "_s" in k:
        b, n = k.split("_s")
        return f"{KIND_KO[b]} 보충 {n}"
    return KIND_KO[k]


def ics_escape(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line):
    b = line.encode("utf-8")
    out, cur = [], b""
    for ch in line:
        c = ch.encode("utf-8")
        if len(cur) + len(c) > (75 if not out else 74):
            out.append(cur)
            cur = b""
        cur += c
    out.append(cur)
    return "\r\n ".join(x.decode("utf-8") for x in out)


cat = jload(os.path.join(W, "catalog.json"), {"subjects": []})
cfg = {"budget": {"report": 8, "quiz": 5, "flashcards": 4, "audio": 3, "video": 1}, "order": [], **jload(os.path.join(W, "config.json"), {})}
st = jload(os.path.join(W, "state.json"), {})
done, fails, daily = st.get("done", {}), st.get("fails", {}), st.get("daily", {})
now = dt.datetime.now(KST)
today = now.strftime("%Y-%m-%d")

os.makedirs(DATA, exist_ok=True)
shutil.copytree(os.path.join(W, "site"), REPO, dirs_exist_ok=True)
ms = jload(MEDIA_STATE, {"shards": [], "files": {}})
dirty = set()


def save_ms():
    json.dump(ms, open(MEDIA_STATE, "w"), ensure_ascii=False, indent=1)


def gh(method, path, body=None):
    req = urllib.request.Request("https://api.github.com" + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json", "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read()[:300].decode("utf-8", "replace")}


def new_shard():
    name = f"study-media-{len(ms['shards']) + 1}"
    gh("POST", "/user/repos", {"name": name, "description": "소단원 학습자료 실험실 미디어 저장소", "private": False, "auto_init": True})
    path = f"/root/{name}"
    if not os.path.exists(path):
        subprocess.run(["git", "clone", "-q", f"https://x-access-token:{TOKEN}@github.com/{OWNER}/{name}.git", path], check=True)
    open(os.path.join(path, ".nojekyll"), "w").close()
    open(os.path.join(path, "index.html"), "w", encoding="utf-8").write(f'<!doctype html><meta charset="utf-8"><title>{name}</title><p>소단원 학습자료 실험실의 미디어 저장소입니다. <a href="https://{OWNER}.github.io/study-notebooklm/">본 사이트로</a></p>')
    for a in (["config", "user.name", OWNER], ["config", "user.email", f"{OWNER}@users.noreply.github.com"]):
        subprocess.run(["git", "-C", path, *a])
    ms["shards"].append({"name": name, "used": 0})
    dirty.add(name)
    save_ms()
    return ms["shards"][-1]


def place_media(n):
    if n not in ms["files"]:
        src = os.path.join(W, "out", n)
        size = os.path.getsize(src)
        sh = ms["shards"][-1] if ms["shards"] and ms["shards"][-1]["used"] + size <= SHARD_BYTES else new_shard()
        dst = os.path.join("/root", sh["name"], n)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)
        sh["used"] += size
        ms["files"][n] = sh["name"]
        dirty.add(sh["name"])
        save_ms()
    return f"https://{OWNER}.github.io/{ms['files'][n]}/{n}"


for dp, _, fs in os.walk(DATA):
    for f in fs:
        if f.endswith((".mp4", ".m4a")):
            os.remove(os.path.join(dp, f))

order = {s: i for i, s in enumerate(cfg["order"])}
subjects, queue = [], {k: [] for k in GROUP}
sup_queue = {k: [] for k in GROUP}
sup_list = jload(os.path.join(W, "sups.json"), [])
days = {}
for s in sorted(cat["subjects"], key=lambda s: order.get(s["id"], 99)):
    units = []
    for u in s["units"]:
        files = {}
        for kind in GROUP:
            key = f"{s['id']}/{u['id']}/{kind}"
            r = done.get(key)
            if r:
                names = [f["file"] for f in r["files"] if f["ok"]]
                url = None
                for n in names:
                    if n.endswith((".mp4", ".m4a")):
                        url = place_media(n)
                        continue
                    src, dst = os.path.join(W, "out", n), os.path.join(DATA, n)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src):
                        shutil.copy(src, dst)
                main = next((n for n in names if not n.endswith(".json")), names[0] if names else None)
                files[kind] = {"file": main, "json": next((n for n in names if n.endswith(".json")), None),
                               "secs": r["secs"], "at": r["at"][:16].replace("T", " "), "url": url}
                if main and kind in ("audio", "video"):
                    dn = main.rsplit(".", 1)[0] + ".desc.json"
                    if os.path.exists(os.path.join(W, "out", dn)):
                        shutil.copy(os.path.join(W, "out", dn), os.path.join(DATA, dn))
                        files[kind]["desc"] = dn
                days.setdefault(r["at"][:10], []).append({"s": s["name"], "u": u["code"], "t": u["title"], "k": kind, "st": "done"})
            else:
                n = fails.get(key, 0)
                if n:
                    files[kind] = {"failed": n}
                if (u.get("source") or u.get("source_id")) and n < cfg.get("max_fails", 3):
                    queue[GROUP[kind]].append({"s": s["name"], "u": u["code"], "t": u["title"], "k": kind, "st": "planned"})
        sups = []
        for sp in [x for x in sup_list if x["subject"] == s["id"] and x["unit"] == u["id"]]:
            key = f"{s['id']}/{u['id']}/{sp['id']}"
            item = {"id": sp["id"], "kind": sp["kind"], "focus": sp["focus"]}
            r = done.get(key)
            if r:
                main = next((f["file"] for f in r["files"] if f["ok"]), None)
                if main:
                    item["file"] = main
                    item["url"] = place_media(main)
                    dn = main.rsplit(".", 1)[0] + ".desc.json"
                    if os.path.exists(os.path.join(W, "out", dn)):
                        shutil.copy(os.path.join(W, "out", dn), os.path.join(DATA, dn))
                        item["desc"] = dn
                item["at"] = r["at"][:16].replace("T", " ")
                days.setdefault(r["at"][:10], []).append({"s": s["name"], "u": u["code"], "t": u["title"], "k": sp["id"], "st": "done"})
            else:
                n = fails.get(key, 0)
                item["planned"] = True
                if n:
                    item["failed"] = n
                if n < cfg.get("max_fails", 3):
                    sup_queue[sp["kind"]].append({"s": s["name"], "u": u["code"], "t": u["title"], "k": sp["id"], "st": "planned"})
            sups.append(item)
        units.append({k: u.get(k) for k in ("id", "code", "chapter", "section", "title", "pages")} | {"files": files, "sups": sups})
    subjects.append({"id": s["id"], "name": s["name"], "book": s.get("book", ""), "units": units})

every = max(1, cfg.get("sup_every", 3))
for g in queue:
    merged, base, extra = [], queue[g], sup_queue[g]
    while base or extra:
        merged.extend(base[:every]); base = base[every:]
        if extra:
            merged.append(extra.pop(0))
    queue[g] = merged
ACCOUNTS = cfg.get("accounts") or ["default"]
today_sum = {}
for k, v in daily.get(today, {}).items():
    today_sum[k.split(":")[-1]] = today_sum.get(k.split(":")[-1], 0) + v
horizon = {}
for g, items in queue.items():
    per = max(1, cfg["budget"][g]) * len(ACCOUNTS)
    left_today = max(0, per - today_sum.get(g, 0))
    bl = [st.get("blocked", {}).get(g if a == "default" else f"{a}:{g}", "") for a in ACCOUNTS]
    blocked = min(bl) if bl else ""
    d = now.date()
    if blocked > now.isoformat() or left_today == 0:
        d += dt.timedelta(days=1)
        cap = per
    else:
        cap = left_today
    i = 0
    while i < len(items):
        take = items[i:i + cap]
        horizon.setdefault(d.isoformat(), []).extend(take)
        i += cap
        d += dt.timedelta(days=1)
        cap = per
for k, v in horizon.items():
    days.setdefault(k, []).extend(v)

remaining = sum(len(v) for v in queue.values())
finish = max(horizon) if horizon else today
total = sum(len(s["units"]) * len(GROUP) for s in subjects) + len(sup_list)
status = {"updated": now.strftime("%Y-%m-%d %H:%M KST"), "last_run": (st.get("last_run") or "")[:16].replace("T", " "),
          "done": len(done), "remaining": remaining, "total": total, "finish": finish,
          "blocked": {(KIND_KO.get(g.split(":")[-1], g) + (f" ({g.split(':')[0]})" if ":" in g else " (default)")): v[:16].replace("T", " ") for g, v in st.get("blocked", {}).items() if v > now.isoformat()},
          "today": today_sum, "budget": {k: v * len(ACCOUNTS) for k, v in cfg["budget"].items()}, "accounts": ACCOUNTS,
          "stale": bool(st.get("last_run")) and (now - dt.datetime.fromisoformat(st["last_run"])).total_seconds() > 26 * 3600}

json.dump({"status": status, "subjects": subjects}, open(os.path.join(DATA, "catalog.json"), "w", encoding="utf-8"), ensure_ascii=False)
json.dump(dict(sorted(days.items())), open(os.path.join(DATA, "schedule.json"), "w", encoding="utf-8"), ensure_ascii=False)

lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//study-notebooklm//KO", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
         "X-WR-CALNAME:학습자료 생성 일정", "X-WR-TIMEZONE:Asia/Seoul"]
stamp = now.astimezone(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
for day, items in sorted(days.items()):
    nd = sum(1 for x in items if x["st"] == "done")
    np_ = len(items) - nd
    d0 = dt.date.fromisoformat(day)
    summ = f"학습자료 {'완료 ' + str(nd) if nd else ''}{' · ' if nd and np_ else ''}{'예정 ' + str(np_) if np_ else ''}건"
    desc = "\n".join(f"{'✔' if x['st'] == 'done' else '·'} {x['s']} {x['u']} {x['t']} — {kname(x['k'])}" for x in items[:60])
    lines += ["BEGIN:VEVENT", f"UID:{day}@study-notebooklm", f"DTSTAMP:{stamp}",
              f"DTSTART;VALUE=DATE:{d0.strftime('%Y%m%d')}", f"DTEND;VALUE=DATE:{(d0 + dt.timedelta(days=1)).strftime('%Y%m%d')}",
              fold("SUMMARY:" + ics_escape(summ)), fold("DESCRIPTION:" + ics_escape(desc)), "TRANSP:TRANSPARENT", "END:VEVENT"]
lines.append("END:VCALENDAR")
open(os.path.join(REPO, "calendar.ics"), "w", encoding="utf-8", newline="").write("\r\n".join(lines) + "\r\n")

for name in sorted(dirty):
    path = f"/root/{name}"
    gm = lambda *a: subprocess.run(["git", "-C", path, *a], capture_output=True, text=True)
    gm("add", "-A")
    if gm("diff", "--cached", "--quiet").returncode:
        gm("commit", "-q", "-m", "media sync")
        p = gm("push", "-q", "origin", "HEAD:main")
        print("media push", name, p.returncode, p.stderr.strip()[-200:])
    pages = gh("GET", f"/repos/{OWNER}/{name}/pages")
    if pages.get("error") == 404:
        print("pages enable", name, gh("POST", f"/repos/{OWNER}/{name}/pages", {"source": {"branch": "main", "path": "/"}}).get("html_url"))
g = lambda *a: subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True)
g("add", "-A")
if g("diff", "--cached", "--quiet").returncode:
    g("commit", "-q", "-m", f"sync: {len(done)} done, {remaining} queued")
    p = g("push", "-q", "origin", "HEAD:main")
    print(now.strftime("%F %T"), "pushed", len(done), remaining, p.stderr.strip()[-200:])
else:
    print(now.strftime("%F %T"), "no change")
