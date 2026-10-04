# CLAUDE.md — dummy-scraper

## About me (Nico)
- Learning Python for fun. Beginner: only basics done (data types, print, input).
- Experienced full-stack dev: Next.js 16 (App Router), React 19, TypeScript (strict), Prisma, PostgreSQL, Tailwind, Vercel.
- **Always compare Python concepts to their Node/Next.js/TypeScript equivalent.** This is how I learn best.

## How to work with me
- **One step at a time.** Give ONE step, then wait for me to report back. No long lists of instructions.
- Be direct and concise. Don't over-explain.
- Role is **mixed**: sometimes you write code and explain it, sometimes I want to write it myself.
  - If I say I want to try, give hints and point me in the right direction. Don't write the solution unless I ask.
  - When you write code, briefly explain the new Python concepts in it.
- Aim for best-practice, production-quality Python (typed, linted, tested), but keep it simple.
- Never make assumptions. If information is missing, ask.
- Only change code related to the current task.
- **Never rename functions, files, classes or variables after you've supplied them.**
- Rewrites: give the **full file**, **one file at a time**, so I can check it.
- **Keep `LEARNING.md` up to date.** Whenever a new Python concept comes up in conversation or in
  code you write, append a row to the table there (concept, one-line explanation, Node/TS
  equivalent). Don't announce it, just do it.

## Environment
- Windows, PowerShell. Give PowerShell commands, not bash.
- IDE: PyCharm 2026.2. The interpreter is set to the project `.venv` (Python 3.14.8).
- Project path: `C:\Dev\Projects\dummy-scraper`
- Git initialised (branch `master`).

## Target site
- https://dummy-scrape-site.vercel.app/ (my own Next.js app, built as a scraping practice target)
- Same dataset on every level: 137 fictional journal papers, each with a detail page and a PDF.
- 12 levels, each harder than the last. Only level 01 is live; the rest are planned.

| Level | Name | Challenge |
|---|---|---|
| 01 | Plain HTML | Server-rendered table, `?page=` pagination (10/page, 14 pages), direct links |
| 02 | Form POST Download | POST-only downloads with hidden form fields |
| 03 | JS-rendered List | Empty HTML; table filled from a JSON API |
| 04 | Login Required | Username/password, session cookies |
| 05 | CAPTCHA Gate | Challenge on the first page |
| 06 | Login + MFA | TOTP codes (secret provided) |
| 07 | Rate Limited | 429s; throttling + Retry-After |
| 08 | Header Inspection | Needs a believable User-Agent, Referer, Accept |
| 09 | Rotating Tokens + Honeypots | Short-lived nonces per link; trap links |
| 10 | Infinite Scroll | Cursor-based pagination |
| 11 | Obfuscated Markup | Random class names; drawn text |
| 12 | Bot Fingerprinting | Client-side automation detection |

Level 01 URLs:
- List: `/level/01-plain?page=N`
- Detail: `/level/01-plain/paper/<id>` (e.g. `mjas-14-3-01`)
- PDF: `/level/01-plain/download/<id>.pdf`
- Table columns: Title, Authors, Section, Published, Issue, Pages, Size, PDF

## Tooling (and the Node equivalents)
| Tool | Purpose | Node equivalent |
|---|---|---|
| uv | Package/env/Python manager | pnpm + nvm |
| `pyproject.toml` | Project config + dependencies | package.json |
| `uv.lock` | Locked versions | pnpm-lock.yaml |
| `.venv` | Project packages | node_modules |
| `.python-version` | Pinned Python | .nvmrc |
| httpx | HTTP client | fetch / axios |
| beautifulsoup4 + lxml | HTML parsing | cheerio |
| pydantic | Data models + validation | zod |
| Ruff (planned, dev) | Lint + format | ESLint + Prettier |
| mypy --strict (planned, dev) | Type checking | tsc strict |
| pytest (planned, dev) | Tests | Vitest/Jest |
| Playwright (later) | Browser automation (levels 03, 11, 12) | Playwright |

Rules:
- Use `uv add <pkg>` / `uv add --dev <pkg>`. Never use `pip`, and never edit dependencies by hand.
- Run code with `uv run ...`. Never "activate" the venv manually.

## Project structure
Created with `uv init --package --name scraper dummy-scraper`, but deliberately flattened to a
beginner-friendly layout: plain modules in the project root, no `src/` package. `[project.scripts]`
and `[build-system]` were removed and `[tool.uv] package = false` added, so uv treats this as a
non-packaged project. Imports are plain, e.g. `from core.http import fetch`.
We can migrate to the `src/` package layout later; it's a mechanical move.

Current:
```
dummy-scraper/
├── pyproject.toml
├── uv.lock
├── .python-version
├── README.md
└── main.py              # contains main()
```

Planned:
```
dummy-scraper/
├── main.py              # entry point
├── core/
│   ├── http.py          # shared HTTP client (headers, retries, throttling)
│   ├── models.py        # Paper model (pydantic)
│   └── storage.py       # save JSON/CSV + PDFs to ./output
├── levels/
│   ├── level01_plain.py
│   ├── level02_form_post.py
│   └── ...
├── tests/
└── output/              # scraped data (git-ignored)
```

## Architecture plan (all 12 levels)

**Scope:** the point of this project is demonstrating how to get *past* each level's
anti-scraping obstacle. Production hardening is explicitly out of scope - don't offer atomic
writes, retry policies, concurrency or similar robustness polish unless Nico asks. If a
download goes bad, delete the file and rerun.

All 12 levels produce **identical output**: the same 137 papers, same fields, same PDFs.
Only the *acquisition* differs. So each level is one swappable function behind a fixed contract:

```
levels/level01_plain.py   ->  scrape() -> list[Paper]
levels/level02_form.py    ->  scrape() -> list[Paper]
...
core/models.py            Paper (one definition, shared by all levels)
core/storage.py           save JSON/CSV + PDFs to ./output
core/http.py              client, headers, retries, throttling
main.py                   dispatcher: `uv run main.py 01`
```

No base class or registry needed - if every level module exposes `scrape()`, that *is* the
contract (duck typing). TS equivalent: `interface Scraper { scrape(): Paper[] }`.

### Build order (deliberate)
1. **Level 01 written flat and plain**, start to finish. No `core/` yet.
2. **Level 02.** Now there are two real examples.
3. **Then** extract what is genuinely duplicated into `core/`.
4. Levels 03-12 slot into the established shape.

Rationale: with only one level the shared seams are guesswork. Two examples reveal the real
boundary. Do not build `core/` early.

### Level 01 notes (learned the hard way)
- Stable hooks: `#archive-results` on the table, `data-paper-id` on each `<tr>`.
  Class names are Tailwind - useless, and obfuscated at level 11.
- **Out-of-range pages clamp to the last page**: `?page=99` returns page 14's 7 rows with
  status 200. "Loop until a page is empty" never terminates. Follow `a[rel=next]` instead;
  it is absent on page 14 even when clamping.
- All 137 rows are `N-N` pages and `N.N KB` size - verified, no edge cases.
- `size_kb` is a float, not bytes: `7.6 KB` is already rounded, so bytes would invent precision.
  True byte sizes come from the downloaded files.

## Commands
- Run: `uv run main.py`. (The earlier `uv run scraper` entry point was removed with the flat layout.)
- Lint: `uv run ruff check .` · Format: `uv run ruff format .`
- Type-check: `uv run mypy .`
- Test: `uv run pytest`
- Install everything: `uv sync`
- Run from PyCharm's terminal (Alt+F12). No Run/Debug configuration yet; we'll add one when breakpoints are needed.

## Progress
- [x] Step 1: Installed uv 0.12.23
- [x] Step 2: Python 3.14.8 already installed
- [x] Step 3: Created the project with uv init + uv sync
- [x] Step 4: Went through pyproject.toml
- [x] Step 5: PyCharm interpreter set to .venv
- [x] Step 6: `uv run main.py` works in the PyCharm terminal
- [x] Step 7: `uv add httpx beautifulsoup4 lxml pydantic` (check pyproject.toml to confirm)
- [x] Step 8: Dev tools: `uv add --dev ruff mypy pytest` + strict config in pyproject.toml
- [x] Step 9: Flattened structure to root-level `main.py` (no `src/` package)
- [x] Step 10: **Level 01 complete** - 137 papers scraped, validated, saved to
      `output/papers.json`, 137 PDFs in `output/pdfs/`. All in `main.py`, deliberately flat.
- [ ] Next: level 02 (form POST download), then extract the shared parts into `core/`
