#!/usr/bin/env python3
"""Push content to a BlackCodeLabs site through its content API.

    export BCL_API_URL=https://yourdomain.com
    export BCL_API_TOKEN=...            # same value as API_TOKEN on the server

    python scripts/push_content.py                              # scripts/content/offerings.json
    python scripts/push_content.py --file scripts/content/examples/new_post.json
    python scripts/push_content.py --file x.json --only posts   # just one kind
    python scripts/push_content.py --file x.json --dry-run      # validate the file, send nothing

The JSON file may contain any of: "services", "solutions", "posts", "portfolio".
Items are upserted, so running a file twice updates instead of duplicating
(services by name; solutions, posts and portfolio by slug).

Convenience keys, handled here (never sent as-is):
    posts[].body_file         path to an .html file used as the post body
    posts[].image_file        path to a JPEG/PNG/WebP used as the post image
    portfolio[].cover_image_file   path to a JPEG/PNG/WebP used as the cover
    (paths are relative to the JSON file). Large images are resized when Pillow is installed.
"""
import argparse
import base64
import io
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_FILE = Path(__file__).parent / "content" / "offerings.json"
KINDS = {  # key in the JSON file -> (endpoint, identifying field)
    "services": ("/api/v1/services/", "name"),
    "solutions": ("/api/v1/solutions/", "slug"),
    "posts": ("/api/v1/posts/", "slug"),
    "portfolio": ("/api/v1/portfolio/", "slug"),
}
MAX_RAW = 6 * 1024 * 1024


def encode_image(path):
    raw = Path(path).read_bytes()
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(raw))
        img.load()
        img.thumbnail((1600, 1600))
        out = io.BytesIO()
        if img.mode in ("RGBA", "LA", "P") and "transparency" in img.info or img.mode in ("RGBA", "LA"):
            img.save(out, "PNG", optimize=True)
        else:
            img.convert("RGB").save(out, "JPEG", quality=85, optimize=True, progressive=True)
        raw = out.getvalue()
    except ImportError:
        pass  # no Pillow: send the file as it is
    if len(raw) > MAX_RAW:
        sys.exit(f"{path}: image is {len(raw) // 1024 // 1024} MB after processing; the limit is {MAX_RAW // 1024 // 1024} MB. Install Pillow to auto-resize.")
    return base64.b64encode(raw).decode()


def resolve(item, kind, base_dir):
    """Turn the *_file convenience keys into the fields the API expects."""
    item = dict(item)
    if kind == "posts" and "body_file" in item:
        item["body"] = (base_dir / item.pop("body_file")).read_text(encoding="utf-8")
    if kind == "posts" and "image_file" in item:
        item["image_base64"] = encode_image(base_dir / item.pop("image_file"))
    if kind == "portfolio" and "cover_image_file" in item:
        item["cover_image_base64"] = encode_image(base_dir / item.pop("cover_image_file"))
    return item


def call(base, token, path, payload):
    req = urllib.request.Request(
        f"{base.rstrip('/')}{path}", data=json.dumps(payload).encode(), method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "bcl-content-push/2.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.load(resp)
    except urllib.error.HTTPError as exc:
        try:
            body = json.load(exc)
        except ValueError:
            body = {"error": exc.reason}
        return exc.code, body


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default=str(DEFAULT_FILE))
    ap.add_argument("--only", action="append", choices=sorted(KINDS), help="push only this kind (repeatable)")
    ap.add_argument("--dry-run", action="store_true", help="validate the file and list what would be sent")
    args = ap.parse_args()

    path = Path(args.file)
    data = json.loads(path.read_text(encoding="utf-8"))
    unknown = set(data) - set(KINDS)
    if unknown:
        sys.exit("Unknown top-level key(s) in the file: " + ", ".join(sorted(unknown)))

    jobs = []
    for kind, (endpoint, key) in KINDS.items():
        if args.only and kind not in args.only:
            continue
        for item in data.get(kind, []):
            jobs.append((kind, endpoint, key, resolve(item, kind, path.parent)))

    if args.dry_run:
        for kind, endpoint, key, item in jobs:
            extras = [k for k in ("image_base64", "cover_image_base64") if k in item]
            print(f"would POST {endpoint}  {item.get(key) or item.get('title')}" + (f"  (+ image {len(item[extras[0]]) * 3 // 4 // 1024} KB)" if extras else ""))
        return 0

    base, token = os.environ.get("BCL_API_URL"), os.environ.get("BCL_API_TOKEN")
    if not base or not token:
        sys.exit("Set BCL_API_URL and BCL_API_TOKEN first (see --help).")
    if not base.startswith("https://") and "localhost" not in base and "127.0.0.1" not in base:
        sys.exit("Refusing to send the token over plain HTTP. Use an https:// URL.")

    failed = 0
    for kind, endpoint, key, item in jobs:
        status, body = call(base, token, endpoint, item)
        label = {200: "updated", 201: "created"}.get(status, f"FAILED ({status})")
        print(f"{label:<14} {endpoint}  {item.get(key) or item.get('title')}")
        if status in (200, 201) and body.get("url"):
            print(f"{'':<14} -> {base.rstrip('/')}{body['url']}")
        if status not in (200, 201):
            failed += 1
            print("    ", json.dumps(body, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
