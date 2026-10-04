# Things to go learn

Python concepts that came up while building this project. Oldest first.
Tick them off once you've properly looked them up.

| ✓ | Concept | What it is | Node / TS equivalent |
|---|---|---|---|
| [ ] | `uv add` / `uv run` / `uv sync` | install deps, run code, install everything from the lockfile | `npm i` / `npm run` / `npm ci` |
| [ ] | `pyproject.toml` | project config **and** tool config, all in one file | `package.json` + eslintrc + tsconfig combined |
| [ ] | `[dependency-groups] dev` | dev-only dependencies | `devDependencies` |
| [ ] | module vs package | a `.py` file vs a folder of them | a file vs a folder with `index.ts` |
| [ ] | `__init__.py` | the file that makes a folder an importable package | `index.ts` in a folder |
| [ ] | `src/` layout vs flat layout | code under `src/` forces a real install before import; flat is simpler | committing `dist/` or not |
| [ ] | `if __name__ == "__main__":` | "only run this if I'm the file being executed, not imported" | `if (require.main === module)` |
| [ ] | type hints (`-> None`, `list[Paper]`) | optional annotations, checked by mypy, ignored at runtime | TS types, except not compiled away |
| [ ] | `mypy --strict` | makes missing annotations an error | `tsc` strict mode |
| [ ] | duck typing | Python checks what a thing *can do*, not what it *is* | TS structural typing, minus the compiler |
| [ ] | `len(x)` | universal "how many" — strings, lists, dicts | `.length`, but a function not a property |
| [ ] | slicing `x[:500]` | `x[start:stop]`, built into the language | `.slice(0, 500)` |
| [ ] | f-strings | string interpolation: `f"page {n}"` | template literals |

## Not yet covered, coming soon
- `with` statement / context managers (`with httpx.Client() as client:`)
- list comprehensions (`[p.title for p in papers]`)
- `dict` vs `list` vs `tuple` vs `set`
- pydantic models (`class Paper(BaseModel)`)
- exceptions: `try` / `except` / `raise`
- `pathlib.Path` for file paths
- generators and `yield`
