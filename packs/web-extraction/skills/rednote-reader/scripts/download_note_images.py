"""
Download Xiaohongshu note images and write manifest for text extraction.

Input: list of image URLs (from an authorized source's "imgs") or a manifest JSON.
Output: images saved as 01.webp, 02.webp, ... in --output-dir; manifest.json with
        title, source_url, author, image_paths for Agent to read in order.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
import socket
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen

REQUEST_TIMEOUT = 30
MAX_IMAGE_BYTES = 25 * 1024 * 1024
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.xiaohongshu.com/",
}


def slug(s: str, max_len: int = 40) -> str:
    s = re.sub(r"[^\w\s\u4e00-\u9fff\-]", "", s)
    s = re.sub(r"\s+", "_", s.strip())
    return s[:max_len] if s else "rednote"


def validate_image_url(url: str) -> None:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https":
        raise ValueError("only HTTPS image URLs are allowed")
    if host != "xhscdn.com" and not host.endswith(".xhscdn.com"):
        raise ValueError(f"image host is not an approved Rednote CDN: {host or '<missing>'}")
    for info in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
        address = ipaddress.ip_address(info[4][0])
        if not address.is_global:
            raise ValueError(f"image host resolved to a non-public address: {address}")


def download_image(url: str, path: str) -> bool:
    try:
        validate_image_url(url)
        request = Request(url, headers=HEADERS)
        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            validate_image_url(response.geturl())
            content_type = response.headers.get_content_type()
            if not content_type.startswith("image/"):
                raise ValueError(f"unexpected content type: {content_type}")
            content = response.read(MAX_IMAGE_BYTES + 1)
        if len(content) > MAX_IMAGE_BYTES:
            raise ValueError("image exceeds 25 MiB limit")
        with open(path, "wb") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"  skip {path}: {e}", file=sys.stderr)
        return False


def main() -> None:
    ap = argparse.ArgumentParser(description="Download Rednote note images and write manifest.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--urls", nargs="+", help="Image URLs in source order")
    g.add_argument("--manifest", type=str, help="Path to JSON with imgs, title, author, url")
    ap.add_argument("--output-dir", required=True, help="Directory to save images and manifest.json")
    args = ap.parse_args()

    urls = []
    title = ""
    author = ""
    source_url = ""

    if args.manifest:
        with open(args.manifest, "r", encoding="utf-8") as f:
            data = json.load(f)
        urls = list(data.get("imgs") or [])
        title = data.get("title") or ""
        author = data.get("author") or ""
        source_url = data.get("url") or ""
    else:
        urls = list(args.urls)

    if not urls:
        print("No image URLs to download.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    # Deduplicate while preserving order
    seen = set()
    unique_urls = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique_urls.append(u)

    image_paths = []
    for i, url in enumerate(unique_urls, start=1):
        # Keep .webp from xhscdn or use .webp by default for small size
        ext = ".webp"
        parsed = urlparse(url)
        if parsed.path and "." in parsed.path.split("/")[-1]:
            ext = "." + parsed.path.split(".")[-1].split("!")[0]
        fname = f"{i:02d}{ext}"
        path = os.path.join(args.output_dir, fname)
        if download_image(url, path):
            image_paths.append(fname)

    manifest = {
        "title": title,
        "source_url": source_url,
        "author": author,
        "image_paths": image_paths,
        "num_images": len(image_paths),
    }
    manifest_path = os.path.join(args.output_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(json.dumps({"manifest": manifest_path, "image_paths": image_paths}, ensure_ascii=False))


if __name__ == "__main__":
    main()
