#!/usr/bin/env python3
"""Dependency-free Berth discovery, token validation, and publishing client."""

from __future__ import annotations

import argparse
import io
import json
import os
import pathlib
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request

PLATFORMS = {
    "local": {"name": "本地服", "url": "http://127.0.0.1:8600"},
    "competition": {"name": "比赛服", "url": "http://61.29.254.146"},
}


def request(platform: str, path: str, *, method: str = "GET",
            data: bytes | None = None, auth: bool = False,
            content_type: str = "application/json"):
    headers = {"Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = content_type
    if auth:
        token = os.environ.get("BERTH_TOKEN", "").strip()
        if not token.startswith("bt_"):
            raise SystemExit("BERTH_TOKEN must be a bt_ developer token")
        headers["Authorization"] = f"Bearer {token}"
    url = PLATFORMS[platform]["url"] + path
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            body = response.read()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise SystemExit(f"Berth API {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Cannot reach {PLATFORMS[platform]['url']}: {exc.reason}") from exc


def package_payload(package_dir: pathlib.Path) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        archive.add(package_dir, arcname=package_dir.name)
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", choices=PLATFORMS, default="competition")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("platforms")
    sub.add_parser("verify-token")
    sub.add_parser("models")
    for name in ("publish", "publish-async"):
        publish = sub.add_parser(name)
        publish.add_argument("package")
        publish.add_argument("--visibility", choices=("private", "public"), required=True)
        if name == "publish-async":
            publish.add_argument("--no-wait", action="store_true")
    args = parser.parse_args()

    if args.command == "platforms":
        print(json.dumps(PLATFORMS, ensure_ascii=False, indent=2))
        return
    if args.command == "verify-token":
        result = request(args.platform, "/v1/dev/me", auth=True)
        print(json.dumps({"valid": True, "platform": PLATFORMS[args.platform]["name"],
                          "developer_id": result.get("developer_id")},
                         ensure_ascii=False, indent=2))
        return
    if args.command == "models":
        print(json.dumps(request(args.platform, "/v1/models"), ensure_ascii=False, indent=2))
        return

    package = pathlib.Path(args.package).resolve()
    if not (package / "berth.json").is_file():
        raise SystemExit(f"Missing berth.json in {package}")
    asynchronous = args.command == "publish-async"
    endpoint = "/v1/dev/publish-async" if asynchronous else "/v1/dev/publish"
    endpoint += "?" + urllib.parse.urlencode({"visibility": args.visibility})
    result = request(args.platform, endpoint, method="POST",
                     data=package_payload(package), auth=True,
                     content_type="application/gzip")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    job_id = result.get("job_id") if isinstance(result, dict) else None
    if asynchronous and job_id and not args.no_wait:
        while True:
            job = request(args.platform, f"/v1/dev/publish-jobs/{job_id}", auth=True)
            print(json.dumps(job, ensure_ascii=False))
            if job.get("status") in {"succeeded", "failed", "cancelled"}:
                if job.get("status") != "succeeded":
                    raise SystemExit(1)
                break
            time.sleep(2)


if __name__ == "__main__":
    main()
