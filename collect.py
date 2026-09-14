#!/usr/bin/env python3
"""Collect a week of torch.compile changes from a local pytorch checkout.

Emits a JSON dump and a markdown draft for the digest.

Usage:
    python collect.py --repo ~/git/pytorch313 --days 7
    python collect.py --since 2026-08-01 --until 2026-08-08
"""

import argparse
import json
import re
import subprocess
import urllib.request
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

FORUM = "https://dev-discuss.pytorch.org/c/compiler/5"
FORUM_CATEGORIES = [
    ("https://dev-discuss.pytorch.org", "/c/compiler/5.json", "forum"),
]
ANNOUNCE = ("https://dev-discuss.pytorch.org", "/c/release-announcements/27.json", "dev-discuss")
# Digest reflects what landed upstream, never the local checkout: we fetch
# origin/main before walking it (local HEAD may hold unlanded ghstack work).
REF = "origin/main"

SUBSYSTEMS = [
    ("Dynamo", ["torch/_dynamo/", "torch/csrc/dynamo/", "test/dynamo/"]),
    ("Inductor", ["torch/_inductor/", "torch/csrc/inductor/", "test/inductor/"]),
]
MAX_PER_SECTION = 10
TAG_PREFIX = re.compile(r"^(\s*\[[^\]]+\])+\s*")
# Fallback ranking when the LLM is unavailable: features/fixes > misc > churn.
FEATURE = re.compile(r"\b(add|support|enable|introduce|implement|fix|speed|faster|new)\b", re.I)
CHURN = re.compile(r"typo|lint|\btyping\b|type annotation|migrate|rename|bump|\[BE\]|\btest", re.I)
ALL_PATHS = [p.rstrip("/") for _, paths in SUBSYSTEMS for p in paths]
CONFIG_FILES = ["torch/_dynamo/config.py", "torch/_inductor/config.py"]

PR_IN_SUBJECT = re.compile(r"\(#(\d+)\)\s*$")
PR_RESOLVED = re.compile(r"Pull Request resolved: .*/pull/(\d+)")
REVERT_SUBJECT = re.compile(r'^Revert "(.*)"$')


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout


def classify(files):
    """Assign a commit to the subsystem owning most of its touched files."""
    counts = defaultdict(int)
    for f in files:
        for name, prefixes in SUBSYSTEMS:
            if any(f.startswith(p) for p in prefixes):
                counts[name] += 1
                break
    if not counts:
        return SUBSYSTEMS[0][0]
    best = max(counts.values())
    for name, _ in SUBSYSTEMS:  # ties resolve in SUBSYSTEMS order
        if counts[name] == best:
            return name


def collect_commits(repo, since, until):
    sep = "\x1e"
    fmt = sep.join(["%H", "%h", "%an", "%as", "%s", "%b"])
    out = git(
        repo, "log", REF, f"--since={since} 00:00", f"--until={until} 23:59:59",
        f"--format=%x1d{fmt}", "--", *ALL_PATHS,
    )
    commits = []
    for rec in out.split("\x1d"):
        rec = rec.strip("\n")
        if not rec:
            continue
        sha, short, author, when, subject, body = (rec.split(sep) + [""] * 6)[:6]
        pr = None
        m = PR_IN_SUBJECT.search(subject) or PR_RESOLVED.search(body)
        if m:
            pr = int(m.group(1))
        files = git(repo, "show", "--name-only", "--format=", sha).split()
        commits.append({
            "sha": sha, "short": short, "author": author, "date": when,
            "subject": subject, "body": body[:800], "pr": pr, "files": files,
            "subsystem": classify(files),
        })
    return commits


def collapse_reverts(commits):
    """Collapse revert/reland churn. Commits are newest-first.

    For each subject, walk history oldest-first keeping net state:
    land -> revert -> reland nets out to the newest land.
    Reverted-without-reland is kept, flagged 'reverted'.
    """
    by_subject = defaultdict(list)  # canonical subject -> events oldest-first
    for c in reversed(commits):
        m = REVERT_SUBJECT.match(c["subject"])
        key = m.group(1) if m else c["subject"]
        by_subject[key].append((bool(m), c))

    kept = []
    for key, events in by_subject.items():
        is_revert, last = events[-1]
        if is_revert:
            # Net effect is a revert. Find what it reverted, flag it.
            lands = [c for rev, c in events if not rev]
            if lands:
                lands[-1]["reverted"] = True
                kept.append(lands[-1])
            # Revert of a commit landed before the window: show the revert itself.
            else:
                last["is_revert"] = True
                kept.append(last)
        else:
            last["relanded"] = len(events) > 1
            kept.append(last)
    kept.sort(key=lambda c: c["date"], reverse=True)
    return kept


def config_changes(repo, since, until):
    """New/removed top-level assignments in dynamo/inductor config over the window."""
    changes = {}
    assign = re.compile(r"^[+-]([a-zA-Z_][a-zA-Z0-9_]*)\s*(?::[^=]+)?=")
    for cfg in CONFIG_FILES:
        out = git(repo, "log", REF, "-p", f"--since={since} 00:00", f"--until={until} 23:59:59", "--", cfg)
        added, removed = set(), set()
        for line in out.splitlines():
            m = assign.match(line)
            if not m:
                continue
            (added if line[0] == "+" else removed).add(m.group(1))
        churn = added & removed
        module = cfg.replace("torch/", "torch.").replace("/config.py", ".config")
        if added - churn or removed - churn:
            changes[module] = (sorted(added - churn), sorted(removed - churn))
    return changes


def fetch_topics(site, category, label, since, until, new_only=False):
    """Discourse topics active (or created, if new_only) in the window. None on failure."""
    try:
        req = urllib.request.Request(site + category, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as e:
        print(f"warning: fetch failed for {site}{category}: {e}")
        return None
    topics = []
    for t in data["topic_list"]["topics"]:
        if t.get("pinned"):
            continue
        created = t["created_at"][:10]
        last = (t.get("last_posted_at") or t["created_at"])[:10]
        anchor = created if new_only else last
        if not (since <= anchor <= until):
            continue
        topics.append({
            "title": t["title"],
            "url": f"{site}/t/{t['slug']}/{t['id']}",
            "new": since <= created <= until,
            "posts": t["posts_count"],
            "label": label,
        })
    return topics


def fetch_forum(since, until):
    """Merged compile-related topics across forums. None if every fetch failed."""
    results = [fetch_topics(s, c, lbl, since, until) for s, c, lbl in FORUM_CATEGORIES]
    if all(r is None for r in results):
        return None
    return [t for r in results if r for t in r]


def fetch_logins(prs):
    """PR number -> GitHub login via gh GraphQL, cached across runs."""
    cache_file = Path("raw/authors.json")
    cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    missing = [n for n in sorted(set(prs)) if str(n) not in cache]
    for i in range(0, len(missing), 50):
        chunk = missing[i:i + 50]
        fields = " ".join(f"p{n}: pullRequest(number:{n}) {{ author {{ login }} }}" for n in chunk)
        query = f'query {{ repository(owner:"pytorch", name:"pytorch") {{ {fields} }} }}'
        try:
            out = subprocess.run(
                ["gh", "api", "graphql", "-f", f"query={query}"],
                capture_output=True, text=True, check=True,
            ).stdout
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"warning: github login fetch failed, falling back to git author names: {e}")
            break
        data = json.loads(out)["data"]["repository"]
        for n in chunk:
            node = data.get(f"p{n}")
            cache[str(n)] = node["author"]["login"] if node and node.get("author") else None
    cache_file.parent.mkdir(exist_ok=True)
    cache_file.write_text(json.dumps(cache, indent=2))
    return {int(n): v for n, v in cache.items() if v}


RATE_PROMPT = """\
You are curating "This week in torch.compile", a weekly digest for PyTorch developers.
For each commit below, rate its relevance to digest readers and write a summary.

Score 1-5: 5 = major feature or user-visible behavior change, 4 = notable fix or
capability, 3 = useful but niche, 2 = internal plumbing, 1 = mechanical churn
(typing, lint, renames, test-only). Summary: one plain-English sentence, spell out
jargon (e.g. NGB = nested graph breaks), no leading "This commit".

Output ONLY a JSON array, no prose, one entry per commit:
[{"sha": "...", "score": 3, "summary": "..."}]

Commits:
"""


def llm_rate(commits):
    """sha -> {score, summary} via `claude -p`, cached across runs."""
    cache_file = Path("raw/ratings.json")
    cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    missing = [c for c in commits if c["sha"] not in cache]
    if missing:
        payload = json.dumps(
            [{"sha": c["sha"], "subject": c["subject"], "body": c["body"]} for c in missing],
            indent=1,
        )
        try:
            out = subprocess.run(
                ["claude", "-p", RATE_PROMPT + payload],
                capture_output=True, text=True, check=True, timeout=600,
            ).stdout
            text = out.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
            for entry in json.loads(text):
                cache[entry["sha"]] = {"score": entry["score"], "summary": entry["summary"]}
        except Exception as e:
            print(f"warning: llm rating failed, falling back to keyword ranking: {e}")
        cache_file.parent.mkdir(exist_ok=True)
        cache_file.write_text(json.dumps(cache, indent=2))
    return cache


def relevance(c):
    if CHURN.search(c["subject"]):
        return 0
    return 2 if FEATURE.search(c["subject"]) else 1


def item_line(c):
    link = f"[#{c['pr']}](https://github.com/pytorch/pytorch/pull/{c['pr']})" if c["pr"] else f"`{c['short']}`"
    desc = c.get("summary") or TAG_PREFIX.sub("", c["subject"].split(" (#")[0]).strip().rstrip(".")
    desc = desc[:1].upper() + desc[1:]
    who = f"@{c['login']}" if c.get("login") else c["author"]
    return f"- {desc} ({link}, {who})"


def render(commits, forum, announcements, cfg_changes, since, until, issue, pubdate):

    pub = pubdate.strftime("%b %d")
    lines = [
        "---",
        f'title: "This week in torch.compile #{issue} - {pub}"',
        f"date: {pubdate.isoformat()}",
        "---",
        "",
        f"_Covering {since} to {until}._",
        "",
        "## News and Announcements",
        "",
        "<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->",
        "",
    ]
    if announcements:
        lines += [f"- [{t['title']}]({t['url']})" for t in announcements] + [""]
    lines += ["## On the forums", ""]
    if forum is None:
        lines += ["<!-- forum fetch failed; fill in manually from " + FORUM + " -->", ""]
    elif not forum:
        lines += ["Quiet week on [the compiler forum](" + FORUM + ").", ""]
    else:
        for t in forum:
            mark = " (new)" if t["new"] else ""
            src = f", {t['label']}" if t["label"] != "forum" else ""
            lines.append(f"- [{t['title']}]({t['url']}) ({t['posts']} posts{src}){mark}")
        lines.append("")
    if cfg_changes:
        lines.append("## Config changes")
        for module, (added, removed) in cfg_changes.items():
            for name in added:
                lines.append(f"- new: `{module}.{name}`")
            for name in removed:
                lines.append(f"- removed: `{module}.{name}`")
        lines.append("")
    groups = defaultdict(list)
    for c in commits:
        groups[c["subsystem"]].append(c)
    for name, _ in SUBSYSTEMS:
        if not groups.get(name):
            continue
        # LLM score (1-5) when rated; keyword tiers (0-2) rank below rated items
        section = sorted(groups[name], key=lambda c: c.get("score") or relevance(c), reverse=True)
        shown, rest = section[:MAX_PER_SECTION], section[MAX_PER_SECTION:]
        lines.append(f"## {name} commits")
        lines.extend(item_line(c) for c in shown)
        if rest:
            anchor = name.lower().replace(" ", "-") + "-commits"
            ref = f'{{{{< relref "/full-log/{pubdate}#{anchor}" >}}}}'
            lines.append(f"- ...plus {len(rest)} more commits ([full log]({ref}))")
        lines.append("")
    counts = {name: sum(c["subsystem"] == name for c in commits) for name, _ in SUBSYSTEMS}
    totals = " and ".join(f"{n} {name}" for name, n in counts.items())
    lines += [f"_In total, {totals} commits landed upstream this week._", ""]
    lines += trend(pubdate)
    return "\n".join(lines)


TREND_WEEKS = 8
BAR_WIDTH = 22
EIGHTHS = " ▏▎▍▌▋▊▉█"


def bar(value, scale, width=BAR_WIDTH):
    """Block bar with eighth-of-a-character precision."""
    if scale <= 0:
        return ""
    eighths = round(value / scale * width * 8)
    return "█" * (eighths // 8) + EIGHTHS[eighths % 8].strip()


def trend(pubdate, weeks=TREND_WEEKS):
    """Notable (score >=3) commits per subsystem over the trailing `weeks` dumps.

    Reads the per-week raw dumps, so it costs nothing beyond a few file reads.
    Weeks predating the LLM rating step have no scores at all; they are skipped
    rather than charted as zero.
    """
    rows = []
    for path in sorted(Path("raw").glob("2026-*.json")):
        try:
            week = date.fromisoformat(path.stem)
        except ValueError:
            continue
        if week > pubdate:
            continue
        try:
            commits = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if not any(c.get("score") is not None for c in commits):
            continue
        counts = {
            name: sum(
                c["subsystem"] == name and not c.get("reverted") and (c.get("score") or 0) >= 3
                for c in commits
            )
            for name, _ in SUBSYSTEMS
        }
        rows.append((week, counts))
    rows = rows[-weeks:]
    if len(rows) < 2:
        return []
    scale = max(n for _, counts in rows for n in counts.values()) or 1
    names = [name for name, _ in SUBSYSTEMS]
    head = "".join(f"{name:<{BAR_WIDTH + 6}}" for name in names)
    out = ["```text", f"{'':<8}{head.rstrip()}"]
    for week, counts in rows:
        cells = "".join(
            f"{bar(counts[name], scale):<{BAR_WIDTH}} {counts[name]:<5}" for name in names
        )
        out.append(f"{week:%b %d}  {cells.rstrip()}")
    out += ["```", ""]
    return [
        f"_Notable commits per week (score 3+ of 5), last {len(rows)} weeks:_",
        "",
        *out,
    ]


def render_fulllog(commits, since, until, issue, pubdate):
    """Companion page: every commit in the window, summarized, grouped as in the issue."""
    lines = [
        "---",
        f'title: "Full log - issue #{issue} ({pubdate:%b %-d})"',
        f"date: {pubdate}",
        "---",
        "",
        f"Every torch.compile commit that landed between {since} and {until}, "
        f"including the ones the [issue]({{{{< relref \"/posts/{pubdate}-this-week-in-torch-compile\" >}}}}) "
        "only counted.",
        "",
    ]
    groups = defaultdict(list)
    for c in commits:
        groups[c["subsystem"]].append(c)
    for name, _ in SUBSYSTEMS:
        if not groups.get(name):
            continue
        section = sorted(groups[name], key=lambda c: c.get("score") or relevance(c), reverse=True)
        lines.append(f"## {name} commits")
        lines.extend(item_line(c) for c in section)
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="~/git/pytorch313")
    ap.add_argument("--days", type=int, help="trailing window ending today (overrides default)")
    ap.add_argument("--since")
    ap.add_argument("--until")
    ap.add_argument("--out", default="content/posts")
    args = ap.parse_args()

    repo = Path(args.repo).expanduser()
    today = date.today()
    # Issues are published on Sundays and cover the 7 days up to publication.
    pubdate = today + timedelta(days=(6 - today.weekday()) % 7)
    if args.since or args.until:
        until = args.until or today.isoformat()
        days = args.days or 7
        since = args.since or (date.fromisoformat(until) - timedelta(days=days)).isoformat()
        # Backfilling an older week: the issue is dated by its window, not by today.
        pubdate = date.fromisoformat(until)
    elif args.days:
        until = today.isoformat()
        since = (today - timedelta(days=args.days)).isoformat()
    else:
        until = pubdate.isoformat()
        since = (pubdate - timedelta(days=7)).isoformat()

    try:
        git(repo, "fetch", "--quiet", "origin", "main")
    except subprocess.CalledProcessError as e:
        print(f"warning: git fetch failed, using possibly stale {REF}: {e.stderr.strip()[:200]}")

    commits = collapse_reverts(collect_commits(repo, since, until))
    # Net-reverted commits are not on main; they don't belong in the digest.
    live = [c for c in commits if not c.get("reverted")]
    logins = fetch_logins([c["pr"] for c in live if c["pr"]])
    ratings = llm_rate(live)
    for c in live:
        c["login"] = logins.get(c["pr"])
        c["score"] = ratings.get(c["sha"], {}).get("score")
        c["summary"] = ratings.get(c["sha"], {}).get("summary")
    cfg_changes = config_changes(repo, since, until)
    forum = fetch_forum(since, until)
    announcements = fetch_topics(*ANNOUNCE, since, until, new_only=True) or []

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    # 'raw', not 'data': data/ is a Hugo-reserved directory
    datadir = Path("raw")
    datadir.mkdir(exist_ok=True)
    (datadir / f"{until}.json").write_text(json.dumps(commits, indent=2))
    stem = "this-week-in-torch-compile"
    # Issue number is the week's chronological position, so regenerating an
    # older week renumbers it correctly instead of appending to the end.
    earlier = [p for p in outdir.glob(f"*-{stem}.md") if p.name[:10] < pubdate.isoformat()]
    issue = len(earlier) + 1
    md = render(live, forum, announcements, cfg_changes, since, until, issue, pubdate)
    post = outdir / f"{pubdate.isoformat()}-{stem}.md"
    post.write_text(md)
    logdir = Path("content/full-log")
    logdir.mkdir(parents=True, exist_ok=True)
    (logdir / f"{pubdate.isoformat()}.md").write_text(
        render_fulllog(live, since, until, issue, pubdate)
    )
    counts =", ".join(f"{s}: {sum(c['subsystem'] == s for c in commits)}" for s, _ in SUBSYSTEMS)
    print(f"{len(commits)} items ({counts}) -> {post}")


if __name__ == "__main__":
    main()
