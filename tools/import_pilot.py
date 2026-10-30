import json, os, shutil, datetime as dt
P = "/var/lib/docker/volumes/advisor-data/_data/nlm-pilot"
W = "/var/lib/docker/volumes/advisor-data/_data/study"
MAP = {"U1": "1-01a", "U2": "1-01b", "U3": "1-02a", "U4": "1-02b"}
ps = json.load(open(f"{P}/state.json"))
cat = json.load(open(f"{W}/catalog.json", encoding="utf-8"))
info = next(s for s in cat["subjects"] if s["id"] == "info")
for u in info["units"]:
    pu = u.pop("imported", None)
    if pu:
        u["notebook"] = ps["nb"]; u["source_id"] = ps["src"][pu]
json.dump(cat, open(f"{W}/catalog.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
st = json.load(open(f"{W}/state.json")) if os.path.exists(f"{W}/state.json") else {}
for k in ("notebooks", "sources", "done", "fails", "blocked", "daily"): st.setdefault(k, {})
os.makedirs(f"{W}/out/info", exist_ok=True)
for line in open(f"{P}/manifest.jsonl", encoding="utf-8"):
    r = json.loads(line)
    if not r.get("ok"): continue
    uid = MAP[r["unit"]]; files = []
    for f in r["files"]:
        ext = f["file"].rsplit(".", 1)[1]; new = f"info/{uid}_{r['kind']}.{ext}"
        shutil.copy(f"{P}/out/{f['file']}", f"{W}/out/{new}")
        files.append({"file": new, "ok": True, "bytes": f["bytes"]})
    at = (dt.datetime.fromisoformat(r["at"]).replace(tzinfo=dt.timezone.utc).astimezone(dt.timezone(dt.timedelta(hours=9)))).isoformat(timespec="seconds")
    st["done"][f"info/{uid}/{r['kind']}"] = {"artifact": r["artifact"], "files": files, "secs": r["secs"], "at": at}
json.dump(st, open(f"{W}/state.json", "w"), ensure_ascii=False, indent=1)
print("imported", len(st["done"]))
