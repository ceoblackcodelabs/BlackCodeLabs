#!/usr/bin/env python3
"""Push Services and Solutions to a BlackCodeLabs site through its content API.

    export BCL_API_URL=https://yourdomain.com
    export BCL_API_TOKEN=...            # same value as API_TOKEN on the server
    python scripts/push_content.py                      # uses scripts/content/offerings.json
    python scripts/push_content.py --dry-run
    python scripts/push_content.py --file other.json

Safe to re-run: items are upserted (services by name, solutions by slug).
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_FILE = Path(__file__).parent / "content" / "offerings.json"


def call(base, token, path, payload):
    req = urllib.request.Request(
        f"{base.rstrip('/')}{path}", data=json.dumps(payload).encode(), method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "bcl-content-push/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
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
    ap.add_argument("--dry-run", action="store_true", help="validate the file and list what would be sent")
    args = ap.parse_args()

    data = json.loads(Path(args.file).read_text())
    jobs = [("/api/v1/services/", "name", s) for s in data.get("services", [])]
    jobs += [("/api/v1/solutions/", "slug", s) for s in data.get("solutions", [])]

    if args.dry_run:
        for path, key, item in jobs:
            print(f"would POST {path}  {item[key]}")
        return 0

    base, token = os.environ.get("BCL_API_URL"), os.environ.get("BCL_API_TOKEN")
    if not base or not token:
        sys.exit("Set BCL_API_URL and BCL_API_TOKEN first (see --help).")
    if not base.startswith("https://") and "localhost" not in base and "127.0.0.1" not in base:
        sys.exit("Refusing to send the token over plain HTTP. Use an https:// URL.")

    failed = 0
    for path, key, item in jobs:
        status, body = call(base, token, path, item)
        label = {200: "updated", 201: "created"}.get(status, f"FAILED ({status})")
        print(f"{label:<14} {path}  {item[key]}")
        if status not in (200, 201):
            failed += 1
            print("    ", json.dumps(body, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
