#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
source_file = root / "01-sources.md"
if not source_file.exists():
    print(f"FAIL missing {source_file}")
    sys.exit(1)

TRAILING_URL_PUNCT = ".,;:!?)]}>'\""


def parse_markdown_table(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = [ln for ln in text.splitlines() if "|" in ln]
    header: list[str] | None = None
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        norm = [re.sub(r"\s+", "_", c.lower()) for c in cells]
        if header is None:
            header = norm
            continue
        rows.append({header[i]: cells[i] for i in range(min(len(header), len(cells)))})
    return rows


def extract_urls(text: str) -> list[str]:
    raw_urls = re.findall(r"https?://[^\s|<>]+", text)
    return sorted({url.rstrip(TRAILING_URL_PUNCT) for url in raw_urls})


def check_url(url: str) -> tuple[bool, str, str, str]:
    status = None
    final = url
    err = ""
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": "OpenClaw product-design source checker"})
            with urllib.request.urlopen(req, timeout=12) as response:
                status = response.status
                final = response.geturl()
                break
        except urllib.error.HTTPError as exc:
            status = exc.code
            final = exc.geturl()
            err = f"HTTPError:{exc.code}"
            if method == "GET":
                break
        except Exception as exc:
            err = type(exc).__name__
            if method == "GET":
                status = None
                break
    ok = status is not None and 200 <= status < 400
    return ok, str(status if status is not None else "ERR"), final, err


text = source_file.read_text(errors="ignore")
rows = parse_markdown_table(text)
urls = extract_urls(text)
print(f"source_file={source_file}")
print(f"urls_found={len(urls)}")

support_map: dict[str, bool] = {}
for row in rows:
    url = (row.get("url") or "").rstrip(TRAILING_URL_PUNCT)
    if url:
        support_map[url] = (row.get("supports_promotion", "").lower() in {"yes", "true", "y"})

failures: list[str] = []
warnings: list[str] = []
for url in urls:
    ok, status, final, err = check_url(url)
    supports_promotion = support_map.get(url, True)
    label = "OK" if ok else ("FAIL" if supports_promotion else "WARN")
    print(f"{label}\t{status}\t{url}\tfinal={final}\tsupports_promotion={str(supports_promotion).lower()}\t{err}")
    if not ok and supports_promotion:
        failures.append(url)
    elif not ok:
        warnings.append(url)

if failures:
    print("VERDICT=FAIL")
    for url in failures:
        print(f"failing_promotion_url={url}")
    for url in warnings:
        print(f"warning_context_url={url}")
    sys.exit(1)

print("VERDICT=PASS")
for url in warnings:
    print(f"warning_context_url={url}")
