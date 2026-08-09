#!/usr/bin/env python3
"""Produce a paste-ready HTML fragment of the latest issue for Substack.

Runs `hugo` to build the site, extracts the article body of the newest post,
and writes it to raw/substack-<date>.html. Open that file in a browser,
select all, copy, and paste into the Substack editor.

Usage:
    pixi run python export_substack.py
"""

import re
import subprocess
import webbrowser
from pathlib import Path

subprocess.run(["hugo", "--quiet"], check=True)

posts = sorted(Path("public/posts").glob("*/index.html"))
if not posts:
    raise SystemExit("no built posts found under public/posts/")
page = posts[-1].read_text()

m = re.search(r"<article>(.*)</article>", page, re.S)
if not m:
    raise SystemExit(f"no <article> found in {posts[-1]}")
body = m.group(1)
# Substack has its own heading hierarchy; the post title becomes the
# Substack title field, so drop it and the date line from the body.
body = re.sub(r"<h1>.*?</h1>\s*", "", body, count=1, flags=re.S)
body = re.sub(r'<div class="post-meta">.*?</div>\s*', "", body, count=1, flags=re.S)
title = re.search(r"<h1>(.*?)</h1>", page, re.S)

out = Path("raw") / f"substack-{posts[-1].parent.name[:10]}.html"
out.parent.mkdir(exist_ok=True)
out.write_text(f"<!-- title: {title.group(1) if title else ''} -->\n{body}")
print(f"wrote {out}\nopen it, select all, copy, paste into the Substack editor")
webbrowser.open(out.resolve().as_uri())
