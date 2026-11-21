#!/usr/bin/env python3
"""Write p/index.html: a noindex list of every lead preview (for Charles, not linked from the site)."""
import json, pathlib, html
root = pathlib.Path(__file__).resolve().parent.parent
specs = sorted(((json.loads(f.read_text()), f.stem) for f in (root / "specs/leads").glob("*.json") if (root / "p" / f.stem).is_dir()), key=lambda x: x[0]["name"].lower())
items = "\n".join(f'<li><a href="{s}/">{html.escape(d["name"])}</a><span>{html.escape(d.get("tagline", ""))}</span></li>' for d, s in specs)
(root / "p/index.html").write_text(f"""<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Previews · Kerbside Web</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;max-width:760px;margin:40px auto;padding:0 20px;color:#14213d}}h1{{font-size:28px}}
ul{{list-style:none;padding:0}}li{{display:flex;justify-content:space-between;gap:16px;padding:12px 0;border-bottom:1px solid #e3e0d8}}
a{{color:#14213d;font-weight:600}}span{{color:#4f5a70;text-align:right}}</style></head><body>
<h1>{len(specs)} free previews</h1><p><a href="../">Sales page</a> · Demos: <a href="../demo/cafe/">café</a>, <a href="../demo/plumber/">plumber</a>, <a href="../demo/beauty/">salon</a></p>
<ul>
{items}
</ul></body></html>
""")
print(len(specs), "previews listed")
