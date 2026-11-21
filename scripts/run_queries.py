"""Runs every query in data/queries.json against data/olist.db.gz with SQLite, the same engine the page uses.
Prints the results (saved to docs/query-output.txt) and writes data/results.json for the narrative."""
import json, gzip, shutil, sqlite3, tempfile
Q = json.load(open("data/queries.json"))
tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
shutil.copyfileobj(gzip.open("data/olist.db.gz"), open(tmp, "wb"))
con = sqlite3.connect(tmp); out = {}
print("SQLite", sqlite3.sqlite_version)
for q in Q:
    cur = con.execute(q["sql"]); cols = [d[0] for d in cur.description]; rows = cur.fetchall()
    out[q["id"]] = {"cols": cols, "rows": rows}
    print(f"\n## {q['id']} {q['title']}\n" + " | ".join(cols)); [print(" | ".join(str(v) for v in r)) for r in rows]
json.dump(out, open("data/results.json", "w"))
