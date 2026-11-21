#!/usr/bin/env python3
"""Render a site from a JSON spec: build_site.py spec.json out_dir"""
import json, sys, datetime, pathlib
from jinja2 import Environment, FileSystemLoader, select_autoescape

DEFAULTS = {
    "color": "#0b5394", "accent": "#073763", "icon": "★", "tagline": "", "pills": [],
    "services_title": "What we do", "area_title": "Where to find us", "contact_title": "Get in touch",
    "cta_primary": "Call now", "cta_secondary": "Get a quote", "form_placeholder": "How can we help?",
    "hours": [], "links": [], "services": [], "banner": "", "noindex": False,
    "bar_cta": "", "credit": "https://xitshiong.github.io/kerbside-web/",
}

def main(spec_path, out_dir):
    spec = {**DEFAULTS, **json.loads(pathlib.Path(spec_path).read_text())}
    spec.setdefault("name_html", spec["name"])
    spec.setdefault("map_query", spec.get("address", ""))
    spec["year"] = datetime.date.today().year
    env = Environment(loader=FileSystemLoader(pathlib.Path(__file__).parent), autoescape=select_autoescape())
    html = env.get_template("template.html.j2").render(**spec)
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(html)
    print(out / "index.html")

if __name__ == "__main__":
    main(*sys.argv[1:3])
