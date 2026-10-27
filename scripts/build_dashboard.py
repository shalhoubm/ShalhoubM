#!/usr/bin/env python3
"""Builds the META Intel Desk site from the daily dashboard.json files.

  META_Intel/<YYYY-MM-DD>/dashboard.json  ->  META_Intel/dashboard/site/data/*.json + site/img/*.jpg

Port of build-dashboard.ps1 for the Linux cloud runner. Prints a summary line, then (last line)
a JSON array of site-relative paths written or changed in this run, for the Artifact publish "files" map.
Needs Pillow for thumbnails (pip install pillow); without it, stories simply get no image.
"""
import argparse
import datetime as dt
import html
import io
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # thumbnails are optional
    Image = None

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
IMG_PATTERNS = [
    re.compile(r"""<meta[^>]+(?:property|name)\s*=\s*["'](?:og:image(?::secure_url)?|twitter:image(?::src)?)["'][^>]*content\s*=\s*["']([^"']+)["']""", re.I),
    re.compile(r"""<meta[^>]+content\s*=\s*["']([^"']+)["'][^>]*(?:property|name)\s*=\s*["'](?:og:image(?::secure_url)?|twitter:image(?::src)?)["']""", re.I),
]


def fetch(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def find_image_url(page_url):
    try:
        page = fetch(page_url, 15).decode("utf-8", errors="replace")
    except Exception:
        return None
    for p in IMG_PATTERNS:
        m = p.search(page)
        if m:
            try:
                return urllib.parse.urljoin(page_url, html.unescape(m.group(1).strip()))
            except Exception:
                return None
    return None


def save_thumb(img_url, out_path):
    if Image is None:
        return False
    try:
        data = fetch(img_url, 20)
        if len(data) < 2000:
            return False
        src = Image.open(io.BytesIO(data)).convert("RGB")
        W, H = 640, 360
        scale = max(W / src.width, H / src.height)
        cw, ch = int(W / scale), int(H / scale)
        cx, cy = (src.width - cw) // 2, (src.height - ch) // 2
        src.crop((cx, cy, cx + cw, cy + ch)).resize((W, H), Image.LANCZOS).save(out_path, "JPEG", quality=72)
        return True
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent / "META_Intel"))
    ap.add_argument("--keep-image-days", type=int, default=60)
    args = ap.parse_args()

    root = Path(args.root)
    site = root / "dashboard" / "site"
    data_dir, img_dir = site / "data", site / "img"
    data_dir.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)
    changed = []

    def write_json(path, obj):
        text = json.dumps(obj, indent=4, ensure_ascii=False)
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        if old != text:
            path.write_text(text, encoding="utf-8")
            changed.append(path.relative_to(site).as_posix())

    # ---- Days ----
    days = sorted(
        (d for d in root.iterdir() if d.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", d.name) and (d / "dashboard.json").exists()),
        key=lambda d: d.name, reverse=True,
    )
    index, all_opps = [], []
    cutoff = (dt.date.today() - dt.timedelta(days=args.keep_image_days)).isoformat()

    for d in days:
        day = json.loads((d / "dashboard.json").read_text(encoding="utf-8-sig"))
        stories = day.get("stories") or []
        img_hits = 0
        for s in stories:
            file = f"{s['id']}.jpg"
            out = img_dir / file
            has = out.exists()
            if not has and day["date"] >= cutoff and s.get("url"):
                iu = find_image_url(s["url"])
                if iu and save_thumb(iu, out):
                    has = True
                    changed.append(f"img/{file}")
            s["image"] = f"img/{file}" if has else None
            if has:
                img_hits += 1
        opps = day.get("opportunities") or []
        for o in opps:
            src = next((s for s in stories if s.get("id") == o.get("source_story_id")), None)
            o["date"] = day["date"]
            o["source_title"] = src["title"] if src else None
            o["source_url"] = src["url"] if src else None
        all_opps += opps
        write_json(data_dir / f"{day['date']}.json", {
            "date": day["date"], "window": day.get("window"), "headline": day.get("headline"),
            "lenovo_read": day.get("lenovo_read"), "pillars": day.get("pillars"), "stories": stories,
        })
        bands = {}
        for s in stories:
            bands[s.get("band")] = bands.get(s.get("band"), 0) + 1
        index.append({
            "date": day["date"], "window": day.get("window"), "stories": len(stories),
            "flash": bands.get("FLASH", 0), "high": bands.get("HIGH", 0), "images": img_hits, "opportunities": len(opps),
        })
    write_json(data_dir / "index.json", index)

    # ---- Opportunities: merge across days, stable IDs ----
    opp_path = data_dir / "opportunities.json"
    existing = json.loads(opp_path.read_text(encoding="utf-8-sig")) if opp_path.exists() else []
    if isinstance(existing, dict):
        existing = [existing]

    def key(o):
        return re.sub(r"[^a-z0-9|]+", "", ((o.get("account") or "") + "|" + (o.get("title") or "")).lower())

    by_key, next_id = {}, 1
    for e in existing:
        by_key[key(e)] = e
        n = int(re.sub(r"\D", "", e.get("id") or "0") or 0)
        if n >= next_id:
            next_id = n + 1
    for o in sorted(all_opps, key=lambda x: x["date"]):
        k = key(o)
        sighting = {"date": o["date"], "story_id": o.get("source_story_id"), "title": o.get("source_title"), "url": o.get("source_url")}
        if k in by_key:
            e = by_key[k]
            sightings = e.get("sightings") or []
            if isinstance(sightings, dict):
                sightings = [sightings]
            if not any(x.get("date") == o["date"] for x in sightings):
                sightings.append(sighting)
            e["sightings"] = sightings
            if o["date"] > (e.get("last_seen") or ""):
                e["last_seen"], e["why_now"], e["urgency"], e["entry_point"] = o["date"], o.get("why_now"), o.get("urgency"), o.get("entry_point")
        else:
            bu = o.get("bu")
            by_key[k] = {
                "id": f"OPP-{next_id:03d}", "title": o.get("title"), "account": o.get("account"), "country": o.get("country"),
                "bu": bu if isinstance(bu, list) else ([bu] if bu else []),
                "why_now": o.get("why_now"), "entry_point": o.get("entry_point"), "owner": o.get("owner"),
                "urgency": o.get("urgency"), "status": o.get("status"),  # status is never overwritten for existing leads
                "first_seen": o["date"], "last_seen": o["date"], "sightings": [sighting],
            }
            next_id += 1
    merged = sorted(by_key.values(), key=lambda e: e.get("id") or "")
    merged = sorted(merged, key=lambda e: e.get("last_seen") or "", reverse=True)
    write_json(opp_path, merged)

    print(f"days={len(days)} opportunities={len(merged)} changed={len(changed)}")
    print(json.dumps(list(dict.fromkeys(changed)), separators=(",", ":")))


if __name__ == "__main__":
    main()
