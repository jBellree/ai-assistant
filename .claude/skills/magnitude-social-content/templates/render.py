#!/usr/bin/env python3
"""
Render a magnitude-social-content template via hcti.io.

Usage:
    python3 render.py <template_name> [--width 1080] [--height 1350] [--slug SLUG]

Reads .claude/skills/magnitude-social-content/templates/<template_name>.html,
substitutes {{LOGO_*}} placeholders with base64 logos, POSTs to hcti.io via curl,
downloads the PNG to library/posts/magnitude/YYYY-MM-DD-<slug>/card.png.

Pass --slug to set the folder name (e.g. "rate-watch-northridge"). Defaults to
the template name if omitted.

--local flag: writes a preview HTML to /tmp/hcti-previews/ and opens in browser.
No hcti.io call, no credits, no PNG. Use during design iteration.

Requires HCTI_API_USER_ID and HCTI_API_KEY in CLAUDE.local.md.

Enforces: never render em or en dashes.
"""
import sys
import re
import json
import time
import base64
import mimetypes
import argparse
import subprocess
import tempfile
from pathlib import Path


def inline_local_images(html, template_dir):
    """Replace <img src="relative/path.png"> with base64 data URIs.

    Template can reference images with relative paths so the file opens
    directly in a browser. When we ship to hcti.io (or write a standalone
    preview to /tmp/), those relative paths won't resolve. Inlining the
    images as data URIs makes the HTML fully self-contained.
    """
    def repl(match):
        full_tag, src = match.group(0), match.group(1)
        if src.startswith(("data:", "http://", "https://")):
            return full_tag
        img_path = (template_dir / src).resolve()
        if not img_path.exists():
            print(f"WARN: image not found: {img_path} (left as-is)")
            return full_tag
        mime = mimetypes.guess_type(str(img_path))[0] or "image/png"
        b64 = base64.b64encode(img_path.read_bytes()).decode()
        return full_tag.replace(src, f"data:{mime};base64,{b64}")

    return re.sub(r'<img[^>]*\ssrc="([^"]+)"[^>]*/?>', repl, html)


def load_env():
    env = {}
    local_md = Path(__file__).resolve().parents[4] / "CLAUDE.local.md"
    for line in local_md.read_text().splitlines():
        m = re.match(r"([A-Z_]+)=(.+)", line.strip())
        if m:
            env[m.group(1)] = m.group(2)
    return env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template", help="template name without .html (e.g. 'explainer')")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    ap.add_argument(
        "--local",
        action="store_true",
        help="Preview locally in browser, skip hcti.io (free). Use during design iteration.",
    )
    ap.add_argument(
        "--slug",
        default=None,
        help="Post slug for the output folder name (e.g. 'rate-watch-northridge'). Defaults to template name.",
    )
    ap.add_argument(
        "--template-dir",
        help="Directory containing the template .html. Defaults to this script's folder.",
    )
    ap.add_argument(
        "--var",
        action="append",
        default=[],
        help="Template variable, repeatable. Format: NAME=VALUE. Replaces {{NAME}} in the HTML.",
    )
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[4]
    templates_dir = Path(args.template_dir).resolve() if args.template_dir else Path(__file__).resolve().parent
    tpl_path = templates_dir / f"{args.template}.html"
    if not tpl_path.exists():
        print(f"Template not found: {tpl_path}")
        sys.exit(1)

    html = tpl_path.read_text()

    for pair in args.var:
        if "=" not in pair:
            print(f"Bad --var (expected NAME=VALUE): {pair}")
            sys.exit(1)
        name, value = pair.split("=", 1)
        if "\u2014" in value or "\u2013" in value:
            print(f"ERROR: --var {name} contains em or en dashes. Rewrite without them.")
            sys.exit(1)
        html = html.replace("{{" + name + "}}", value)

    if "\u2014" in html or "\u2013" in html:
        print("ERROR: template contains em or en dashes. Remove them before rendering.")
        sys.exit(1)

    logos_dir = root / "references" / "brand" / "logos"
    logo_map = {
        "{{LOGO_BRAND}}": logos_dir / "magnitude-full-brand.b64",
        "{{LOGO_WHITE}}": logos_dir / "magnitude-full-white.b64",
        "{{LOGO_ORANGE}}": logos_dir / "magnitude-full-orange.b64",
        "{{LOGO_CREST}}": logos_dir / "magnitude-crest.b64",
    }
    for token, path in logo_map.items():
        if token in html and path.exists():
            b64 = path.read_text().strip()
            html = html.replace(token, f"data:image/png;base64,{b64}")

    html = inline_local_images(html, templates_dir)

    if args.local:
        out_dir = Path("/tmp/hcti-previews")
        out_dir.mkdir(exist_ok=True)
        ts = time.strftime("%Y%m%d-%H%M%S")
        out_path = out_dir / f"{args.template}-{ts}.html"
        wrapped = (
            "<!doctype html><html><head><meta charset='utf-8'>"
            "<link href='https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Montserrat:wght@400;500;600&display=swap' rel='stylesheet'>"
            f"<title>{args.template} preview</title></head>"
            f"<body style='margin:0;background:#0d0f1a;display:flex;justify-content:center;padding:24px;'>"
            f"<div style='box-shadow:0 0 40px rgba(0,0,0,0.5);'>{html}</div>"
            "</body></html>"
        )
        out_path.write_text(wrapped)
        print(f"Local preview: {out_path}")
        subprocess.run(["open", str(out_path)], check=False)
        return

    env = load_env()
    user = env.get("HCTI_API_USER_ID")
    key = env.get("HCTI_API_KEY")
    if not user or not key:
        print("Missing HCTI_API_USER_ID or HCTI_API_KEY in CLAUDE.local.md")
        sys.exit(1)

    payload = {
        "html": html,
        "google_fonts": "Poppins:400,600,700,800|Montserrat:400,500,600",
        "viewport": {"width": args.width, "height": args.height},
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tf:
        json.dump(payload, tf)
        payload_file = tf.name

    try:
        result = subprocess.run(
            [
                "curl", "-s", "-u", f"{user}:{key}",
                "-H", "Content-Type: application/json",
                "-X", "POST", "https://hcti.io/v1/image",
                "-d", f"@{payload_file}",
            ],
            check=True, capture_output=True, text=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"curl failed: {e.stderr}")
        sys.exit(1)

    try:
        resp = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"bad response from hcti.io: {result.stdout}")
        sys.exit(1)

    if "url" not in resp:
        print(f"hcti.io error: {resp}")
        sys.exit(1)

    url = resp["url"]
    print(f"URL: {url}")

    date_str = time.strftime("%Y-%m-%d")
    slug = args.slug or args.template
    out_dir = root / "library" / "posts" / "magnitude" / f"{date_str}-{slug}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "card.png"
    subprocess.run(["curl", "-sL", url, "-o", str(out_path)], check=True)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
