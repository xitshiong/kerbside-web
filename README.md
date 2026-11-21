# Kerbside Web

Offer page and site generator for $299 websites for Melbourne small businesses.

- `index.html` — sales page (`{{EMAIL}}` replaced at deploy time)
- `tools/build_site.py spec.json out_dir` — renders `tools/template.html.j2` from a JSON spec
- `specs/demo/*.json` → `demo/*/` — fictional demo businesses
- `p/<slug>/` — per-lead free previews (noindex)

Requires Python 3 + Jinja2.
