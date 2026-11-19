#!/usr/bin/env python3
"""Check every link on the site for breakage.

Usage (from the repo root):
    python3 _scripts/check_links.py              # internal + external links
    python3 _scripts/check_links.py --internal   # internal links only (fast, offline)

Internal links (/path/, relative paths) are resolved against this repo: page
permalinks from front matter, pages without a permalink, and files on disk.
Paths served by other GitHub Pages repos under the same domain (e.g. /gamedev/)
are checked live. External links are fetched with a browser-like User-Agent.

Exits 1 if any link is broken. Uses only the Python standard library.
"""
import concurrent.futures as cf
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

SITE = "https://omprabhu31.github.io"
# Path prefixes served by separate repos (project sites) on the same domain.
OTHER_REPOS = ("/gamedev/",)
# Hosts that block automated requests; a non-200 from these is not a real failure.
BOT_BLOCKING = {
    "www.linkedin.com": "LinkedIn blocks bots (HTTP 999)",
    "www.facebook.com": "Facebook redirects bots to a login page (HTTP 400)",
}
# Google Forms return HTTP 200 even for deleted forms; a live form's page
# always contains this marker.
GOOGLE_FORM_HOSTS = ("forms.gle", "docs.google.com/forms")
GOOGLE_FORM_MARKER = "FB_PUBLIC_LOAD_DATA_"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

LINK_RE = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"|\]\(([^)\s]+(?: [^)"]+)*)\)')
PERMALINK_RE = re.compile(r"^permalink:\s*[\"']?([^\"'\s]+)", re.M)


def tracked_files():
    out = subprocess.check_output(["git", "ls-files"], text=True)
    # Skip tracked files deleted in the working tree (deletion not yet committed).
    return [f for f in out.splitlines() if f and os.path.isfile(f)]


def source_files(files):
    for f in files:
        if f in ("README.md", "AGENTS.md", "CLAUDE.md") or f.startswith("_scripts/"):
            continue
        if f.endswith((".md", ".html")) or f == "_config.yml":
            yield f


def site_paths(files):
    """Every URL path the built site will serve from this repo."""
    paths = set()
    for f in files:
        paths.add("/" + f)
        if f.endswith((".md", ".html")) and not f.startswith("_"):
            text = open(f, encoding="utf-8", errors="ignore").read()
            m = PERMALINK_RE.search(text[:2000]) if text.startswith("---") else None
            if m:
                paths.add(m.group(1))
            else:
                base = f.rsplit(".", 1)[0]
                paths.add("/" + base + ".html")
                if base == "index" or base.endswith("/index"):
                    paths.add("/" + base[: -len("index")])
    return paths


def extract_links(files):
    links = []
    for f in files:
        text = open(f, encoding="utf-8", errors="ignore").read()
        for m in LINK_RE.finditer(text):
            url = (m.group(1) or m.group(2)).strip().strip("<>")
            if "{{" in url or "{%" in url:
                continue
            if url.startswith(("mailto:", "tel:", "javascript:", "#", "data:")):
                continue
            links.append((f, url))
    return links


def fetch(url):
    """Return the HTTP status for url (or an error name); 'dead form' for deleted Google Forms.

    Uses curl when available: Python's ssl module can't talk to some older
    servers (e.g. portal.iitb.ac.in) that curl handles fine.
    """
    url = urllib.parse.quote(url, safe=":/?=&%#+~@!$,;")
    is_form = any(h in url for h in GOOGLE_FORM_HOSTS)
    if shutil.which("curl"):
        cmd = ["curl", "-s", "-L", "--max-time", "25", "-A", UA,
               "-o", "-" if is_form else os.devnull, "-w", "\n%{http_code}", url]
        res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
        body, _, code = res.stdout.rpartition("\n")
        status = int(code) if code.isdigit() and code != "000" else f"curl exit {res.returncode}"
    else:
        body, status = "", None
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                status = r.status
                body = r.read().decode("utf-8", "ignore") if is_form else ""
        except urllib.error.HTTPError as e:
            status = e.code
        except Exception as e:  # DNS, SSL, timeout
            status = type(e).__name__
    if status == 200 and is_form and GOOGLE_FORM_MARKER not in body:
        return "dead form"
    return status


def main():
    internal_only = "--internal" in sys.argv
    files = tracked_files()
    paths = site_paths(files)
    broken, external = [], {}

    for f, url in extract_links(source_files(files)):
        if url.startswith("//"):  # protocol-relative URL, e.g. //fonts.googleapis.com/...
            url = "https:" + url
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme in ("http", "https"):
            if url.startswith(SITE + "/") and not url[len(SITE):].startswith(OTHER_REPOS):
                parsed = urllib.parse.urlparse(url[len(SITE):])
            else:
                external.setdefault(url.split("#")[0], []).append(f)
                continue
        path = urllib.parse.unquote(parsed.path)
        if not path:
            continue
        if not path.startswith("/"):
            base = "/" + os.path.dirname(f)
            path = os.path.normpath(os.path.join(base, path))
        if path.startswith(OTHER_REPOS):
            external.setdefault(SITE + path, []).append(f)
            continue
        candidates = {path, path.rstrip("/") + "/", path.rstrip("/"),
                      path.rstrip("/") + "/index.html"}
        if not candidates & paths:
            broken.append((f, url, "no matching page or file in repo"))

    if not internal_only:
        urls = sorted(external)
        with cf.ThreadPoolExecutor(8) as ex:
            for url, status in zip(urls, ex.map(fetch, urls)):
                if status == 200:
                    continue
                host = urllib.parse.urlparse(url).netloc
                if host in BOT_BLOCKING:
                    continue
                if status == 429:
                    print(f"SKIPPED {url}  (HTTP 429 rate-limited; re-run later)")
                    continue
                why = "Google Form deleted or closed" if status == "dead form" else f"HTTP {status}"
                for f in sorted(set(external[url])):
                    broken.append((f, url, why))

    for f, url, why in sorted(broken):
        print(f"BROKEN  {f}: {url}  ({why})")
    checked = "internal" if internal_only else f"internal + {len(external)} external"
    print(f"\n{len(broken)} broken link(s) found ({checked} checked).")
    print("Note: a non-200 from an external site can be bot-blocking or a "
          "temporary outage; open it in a browser before removing it.")
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
