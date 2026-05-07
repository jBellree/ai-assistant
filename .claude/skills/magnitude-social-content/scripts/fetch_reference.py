#!/usr/bin/env python3
"""
Fetch reference images for a vehicle make from Autotrader UK.

Usage:
    python3 fetch_reference.py <make>

Saves up to 5 reference images into library/vehicles/<make>/reference/
with sidecar .md files capturing the source URL and fetch date.

Designed to be run from the AI Assistant workspace root.
"""

import sys
import re
import urllib.request
from datetime import date
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]


def fetch_url(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def extract_image_urls(html: str) -> list[str]:
    pattern = r'https://m\.atcdn\.co\.uk/vms/media/[a-f0-9]{32}\.jpg'
    return list(dict.fromkeys(re.findall(pattern, html)))


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <make>", file=sys.stderr)
        sys.exit(1)

    make = sys.argv[1].lower().strip()
    out_dir = WORKSPACE_ROOT / "library" / "vehicles" / make / "reference"
    out_dir.mkdir(parents=True, exist_ok=True)

    page_url = f"https://www.autotrader.co.uk/cars/{make}"
    print(f"Fetching: {page_url}")
    html = fetch_url(page_url).decode("utf-8", errors="ignore")

    urls = extract_image_urls(html)
    if not urls:
        print(f"No images found for {make}. Check the make slug.", file=sys.stderr)
        sys.exit(2)

    print(f"Found {len(urls)} candidate images, saving up to 5")
    saved = 0
    for i, url in enumerate(urls[:5]):
        img_bytes = fetch_url(url)
        if len(img_bytes) < 20_000:
            continue
        slug = f"{make}-ref-{i+1:02d}"
        img_path = out_dir / f"{slug}.jpg"
        md_path = out_dir / f"{slug}.md"
        img_path.write_bytes(img_bytes)
        md_path.write_text(
            f"---\n"
            f"make: {make}\n"
            f"source: Autotrader UK brand page\n"
            f"source_url: {page_url}\n"
            f"image_url: {url}\n"
            f"fetched: {date.today().isoformat()}\n"
            f"notes: Auto-fetched. Review and rename meaningfully if kept long-term.\n"
            f"---\n"
        )
        print(f"  saved {img_path.relative_to(WORKSPACE_ROOT)}")
        saved += 1

    print(f"\nDone. {saved} images saved to {out_dir.relative_to(WORKSPACE_ROOT)}/")


if __name__ == "__main__":
    main()
