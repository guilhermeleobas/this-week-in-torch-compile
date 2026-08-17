# This Week in torch.compile

Weekly digest of [torch.compile](https://docs.pytorch.org/docs/stable/torch.compiler.html)
development: the most relevant Dynamo and Inductor commits of the week, config
changes, release announcements, and active discussions on the
[PyTorch developer forum](https://dev-discuss.pytorch.org/c/compiler/5).

**Read it at <https://guilhermeleobas.github.io/this-week-in-torch-compile/>.**

Published every Sunday. Inspired by [LLVM Weekly](https://llvmweekly.org/).

## Layout

| Path | What |
| --- | --- |
| `collect.py` | Generates a digest draft from a local pytorch checkout |
| `content/posts/` | Published issues (Markdown) |
| `layouts/` | Hugo templates |
| `raw/` | Per-week JSON dumps and caches (gitignored) |

## Generating an issue

Requires [pixi](https://pixi.sh), a pytorch checkout, and `gh` authenticated
for PR author lookups.

```sh
pixi run collect                          # window ending the upcoming Sunday
pixi run collect -- --days 7
pixi run collect -- --since 2026-08-01 --until 2026-08-08
pixi run collect -- --repo ~/git/pytorch  # defaults to ~/git/pytorch313
```

`collect.py` walks `origin/main` (fetching first, so unlanded local ghstack work
never leaks in), collapses revert/reland churn, groups commits by subsystem, and
ranks them with `claude -p`. Every network step degrades to a warning and a
fallback, so a run without `gh`, `claude`, or forum access still produces a
draft.

The output lands in `content/posts/` as a draft: the News and Announcements
section is an editorial stub, so fill it in or delete it before publishing.

## Previewing

```sh
pixi run hugo server
```

Pushing to `main` deploys to GitHub Pages via `.github/workflows/hugo.yml`.
