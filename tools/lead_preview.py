#!/usr/bin/env python3
"""Build a free preview site for a real business from a lead row: lead_preview.py leads.csv [slug ...]
Writes specs/leads/<slug>.json and p/<slug>/index.html. Text is generic and photos are licensed stand-ins."""
import csv, json, re, sys, shutil, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_site

ROOT = pathlib.Path(__file__).resolve().parent.parent
DAYS = dict(Mo="Mon", Tu="Tue", We="Wed", Th="Thu", Fr="Fri", Sa="Sat", Su="Sun", PH="Public holidays")
LABEL = {"cafe": "Café", "restaurant": "Restaurant", "hairdresser": "Hair salon", "beauty": "Beauty salon", "bakery": "Bakery",
         "pastry": "Cookies & treats", "bar": "Bar", "deli": "Delicatessen", "optician": "Optometrist", "dentist": "Dentist",
         "doctors": "Clinic", "panel_beater": "Panel beater", "bicycle": "Bike shop",
         "stonemason": "Concreting", "gift": "Homewares & gifts", "candles": "Candles & gifts", "newsagent": "Newsagency",
         "convenience": "Grocery", "computer": "Audio visual & computers", "homeopathy": "Natural health supplies", "butcher": "Butcher", "greengrocer": "Greengrocer", "tattoo": "Tattoo studio", "fast_food": "Takeaway", "tailor": "Tailor", "pub": "Pub", "veterinary": "Vet clinic", "florist": "Florist", "sports_centre": "Sports centre", "car_repair": "Mechanic", "jewelry": "Jeweller", "lawyer": "Law firm", "chemist": "Pharmacy", "copyshop": "Print shop", "massage": "Massage", "internet_cafe": "Internet café", "locksmith": "Locksmith", "books": "Bookshop", "roof": "Roofing", "plant_hire": "Equipment hire", "accountant": "Accountant", "insurance": "Insurance broker", "general": "General store", "training_centre": "Training centre", "motorcycle_repair": "Motorcycle mechanic", "tea": "Tea shop", "car_parts": "Car parts", "tyres": "Tyre shop", "optometrist": "Optometrist", "coffee": "Coffee roaster", "pet": "Pet shop", "psychotherapist": "Psychologist", "seafood": "Seafood shop", "electrical": "Electrical supplies", "alternative": "Natural therapies", "builder": "Builder", "carpet": "Carpet store", "electronics": "Electronics store", "ice_cream": "Ice creamery", "photo": "Photography studio", "hearing_aids": "Hearing clinic", "advertising_agency": "Ad agency", "engineer": "Engineering firm", "property_management": "Property manager", "wholesale": "Wholesaler", "funeral_directors": "Funeral directors", "party": "Party hire", "karaoke_box": "Karaoke bar", "pet_grooming": "Dog groomer", "clinic": "Clinic", "alcohol": "Bottle shop", "graphic_design": "Design studio", "travel_agency": "Travel agency", "tax_advisor": "Tax agent", "fitness_centre": "Gym"}
KITS = {
    "cafe": dict(layout="venue", font="Fraunces", color="#9a4a1f", accent="#2d1d14", paper="#f6efe6", photos="cafe", services_title="What we serve",
                 headline="Café in {where}", services=["Coffee", "Breakfast", "Lunch", "Takeaway"],
                 cta_secondary="Send an enquiry"),
    "restaurant": dict(layout="venue", font="Fraunces", color="#8c2f1b", accent="#24140f", paper="#f7f1ea", services_title="Eat with us",
                 headline="{cuisine_label} in {where}", services=["Dine in", "Takeaway", "Bookings", "Groups & functions"],
                 cta_primary="Call to book", cta_secondary="Request a booking"),
    "hairdresser": dict(font="Cormorant Garamond", font_weights="500;600;700", color="#9b4d5b", accent="#3b2230", paper="#f8f1ee",
                 photos="beauty", radius="4px", services_title="Cuts, colour and styling", headline="Hair salon in {where}",
                 services=["Cuts", "Colour", "Blow-dry & styling", "Treatments"], cta_primary="Call to book", cta_secondary="Request a booking", bar_cta="Book"),
    "bakery": dict(layout="venue", font="Fraunces", color="#a0522d", accent="#3a2416", paper="#f8f0e3", services_title="From our oven",
                 headline="Bakery in {where}", services=["Bread", "Pastries", "Cakes to order", "Coffee"]),
}
KITS["pastry"] = {**KITS["bakery"], "services": ["Cookies", "Boxes & gifts", "Orders for events"]}
KITS["beauty"] = KITS["hairdresser"]
GENERIC = dict(font="Archivo", font_weights="700;800", heading_weight=800, color="#1f4fd1", accent="#0f1f3d", paper="#f4f5f7", radius="6px",
               headline="{label} in {where}", services=[])
PHOTOS = {"cafe": "cafe", "beauty": "beauty"}

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]
def phone_fmt(p):
    p = re.sub(r"[^\d+]", "", p.split(";")[0])
    if p.startswith("+61"): p = "0" + p[3:]
    if len(p) == 10 and p.startswith("04"): return f"{p[:4]} {p[4:7]} {p[7:]}"
    if len(p) == 10: return f"({p[:2]}) {p[2:6]} {p[6:]}"
    return p
def t12(t):
    if t.endswith("+"): return t12(t[:-1]) + " till late"
    h, m = map(int, t.split(":")); s = "am" if h < 12 or h == 24 else "pm"; h = h % 12 or 12
    return f"{h}{'' if m == 0 else ':%02d' % m}{s}"
def hours(oh):
    out = []
    for part in [x.strip() for x in oh.split(";") if x.strip()]:
        m = re.match(r"^([A-Za-z ,\-]+?)\s+(.+)$", part)
        if not m: return []
        days = re.sub(r"\b(Mo|Tu|We|Th|Fr|Sa|Su|PH)\b", lambda d: DAYS[d.group(1)], m.group(1)).replace("-", " to ")
        times = m.group(2)
        if times in ("off", "closed"): v = "Closed"
        else:
            try: v = ", ".join(" to ".join(t12(x.strip()) for x in r.split("-")) for r in times.split(","))
            except Exception: return []
        out.append([days, v])
    return out

def spec_for(r):
    kit = {**GENERIC, **KITS.get(r["kind"], {})}
    where = r["suburb"] or r.get("city") or "Melbourne"
    label = LABEL.get(r["kind"], r["kind"].replace("_", " ").capitalize())
    addr = ", ".join(x for x in (r["street"], r["suburb"]) if x)
    cuisine = f", {r['cuisine'].split(';')[0].replace('_', ' ')} food" if r.get("cuisine") else ""
    cuisine_label = f"{r['cuisine'].split(';')[0].replace('_', ' ').capitalize()} restaurant" if r.get("cuisine") else label
    hrs = hours(r["hours"]) if r["hours"] else []
    s = dict(name=r["name"], name_html=r["name"], tagline=f"{label} in {where}", noindex=True,
             headline=kit.pop("headline").format(name=r["name"], where=where, cuisine=cuisine, cuisine_label=cuisine_label, label=label),
             intro=f"Find {r['name']} in {where}" + (": opening hours, directions and a quick way to get in touch." if hrs else ": directions and a quick way to get in touch."),
             banner=f"Free website preview made for <b>{r['name']}</b> by <a href=\"../../\">Kerbside Web</a>. Sample text and stock photos, not live yet.",
             email=r["email"], phone=phone_fmt(r["phone"]) if r["phone"] else "", address=addr,
             map_query=f"{r['name']} {addr or where} VIC", hours=hrs,
             area_title="Visit us" if addr else "Find us", contact_title="Get in touch",
             links=[[n, u] for n, u in (("Facebook", r["facebook"]), ("Instagram", r["instagram"])) if u and u.startswith("http")],
             credit="https://kerbsidedesign.com/")
    if not s["phone"]: s["cta_secondary"] = kit.get("cta_secondary", "Send an enquiry")
    svc = kit.pop("services")
    s["services"] = [{"name": x} for x in svc]
    if not svc: s["services_title"] = ""
    photos = kit.pop("photos", None)
    s.update(kit)
    if photos:
        cred = json.loads((ROOT / "specs/demo" / f"{photos}.json").read_text())
        s["hero"], s["about_img"], s["photo_credits"] = cred.get("hero"), None, cred.get("photo_credits", [])
        hid = (s["hero"] or {}).get("id")
        s["photo_credits"] = [c for c in s["photo_credits"] if c.get("id") == hid][:1] or s["photo_credits"][:1]
        s["_photo_dir"] = photos
    return s

SKIP_KINDS = {"social_facility", "mall"}

def main(csv_path, *only):
    seen = set()
    for r in csv.DictReader(open(csv_path)):
        if r.get("existing_site") or r["kind"] in SKIP_KINDS: continue
        sl = slug(r["name"])
        if sl in seen: sl = slug(r["name"] + "-" + (r["suburb"] or r["street"]))
        seen.add(sl)
        if only and sl not in only: continue
        s = spec_for(r); pd = s.pop("_photo_dir", None)
        (ROOT / "specs/leads").mkdir(parents=True, exist_ok=True)
        sp = ROOT / "specs/leads" / f"{sl}.json"; sp.write_text(json.dumps(s, ensure_ascii=False, indent=1))
        out = ROOT / "p" / sl
        build_site.main(sp, out)
        if pd and s.get("hero"):
            (out / "img").mkdir(exist_ok=True)
            for f in (ROOT / "demo" / pd / "img").glob(s["hero"]["id"] + "-*.jpg"): shutil.copy(f, out / "img" / f.name)

if __name__ == "__main__":
    main(*sys.argv[1:])
    import gallery  # noqa: E402,F401  (rebuilds p/index.html)
