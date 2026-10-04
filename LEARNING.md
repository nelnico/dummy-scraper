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
| [ ] | `from bs4 import BeautifulSoup` | import one name out of a package | `import { x } from "pkg"` |
| [ ] | `BeautifulSoup(html, "lxml")` | parse an HTML string into a searchable tree | `cheerio.load(html)` |
| [ ] | `.select("css selector")` | find all matching elements, returns a list | `querySelectorAll` |
| [ ] | `rows[0]` | index into a list; `rows[-1]` is the last one | `rows[0]`, but negative indexing is new |
| [ ] | `.select_one(...)` | first match, or `None` if nothing matched | `querySelector` |
| [ ] | `None` | the "nothing" value | `null` |
| [ ] | `if x is None:` | identity check, the correct way to test for None | `if (x === null)` |
| [ ] | `raise ValueError("...")` | throw an error | `throw new Error("...")` |
| [ ] | `.text` | all text inside an element | `.textContent` |
| [ ] | `for row in rows:` | loop over any iterable, no index needed | `for (const row of rows)` |
| [ ] | indentation as syntax | the colon + indent **is** the block; no `{ }` | `{ }` braces |
| [ ] | `row["data-paper-id"]` | read an HTML attribute, square-bracket style | `el.dataset.paperId` / `getAttribute` |
| [ ] | `print(a, b)` | print takes many args, space-separated | `console.log(a, b)` |
| [ ] | `dict` literal `{"k": v}` | key/value map; keys are real strings, quotes required | object literal `{ k: v }` |
| [ ] | trailing commas | allowed, and the formatter wants them on multi-line | same |
| [ ] | `class Paper(BaseModel):` | define a class, inheriting from another | `class Paper extends BaseModel` |
| [ ] | pydantic model | typed fields + runtime validation in one | `z.object()` + the inferred TS type |
| [ ] | `Paper(id=..., title=...)` | keyword arguments, passed by name | an options object `{ id, title }` |
| [ ] | `ValidationError` | raised when data doesn't match the model | `ZodError` / `safeParse` failure |
| [ ] | `.model_dump()` / `.model_dump_json()` | model -> dict / JSON string | `JSON.stringify` |
| [ ] | `Paper.model_validate(raw)` | validate a raw dict into a model | `schema.parse(raw)` in zod |
| [ ] | `@field_validator(...)` | convert/check one field before validation | `.transform()` in zod |
| [ ] | decorators (`@something`) | wrap a function to change its behaviour | TS decorators, roughly |
| [ ] | `@classmethod` | method on the class, not an instance; takes `cls` | `static` method |
| [ ] | `datetime.strptime(s, fmt)` | parse a string into a datetime with a format | `date-fns` `parse()` |
| [ ] | `%d %b %Y` | strftime codes: day, abbreviated month, 4-digit year | `dd MMM yyyy` |
| [ ] | `a, b = x.split("-")` | tuple unpacking: assign two names at once | array destructuring `[a, b] = ...` |
| [ ] | `.split("-")` | string to list of parts | `.split("-")`, identical |
| [ ] | pydantic coercion | `"16"` becomes `16` for an `int` field, for free | zod `z.coerce.number()` |
| [ ] | `.removesuffix(" KB")` | strip a trailing substring if present | `.replace(/ KB$/, "")` |
| [ ] | `def f(page: int) -> list[Paper]:` | typed parameter and return type | `(page: number): Paper[]` |
| [ ] | `papers: list[Paper] = []` | empty list needs an annotation under strict mypy | `const p: Paper[] = []` |
| [ ] | `.append(x)` | add to the end of a list | `.push(x)` |
| [ ] | `params={"page": page}` | httpx builds the query string for you | `axios` `{ params }` |
| [ ] | `tuple[list[Paper], bool]` | return two values at once | returning `[Paper[], boolean]` |
| [ ] | `batch, has_next = scrape_page(p)` | unpack a returned tuple | `const [batch, hasNext] = ...` |
| [ ] | `while True:` + `break` | loop until you decide to stop | `while (true) { ... break }` |
| [ ] | `page += 1` | increment; Python has **no** `++` | `page++` |
| [ ] | `if not x:` | truthiness; empty list/string/0 are falsy | `if (!x)` |
| [ ] | `.extend(other)` | append every item of another list | `a.push(...b)` |
| [ ] | f-string `f"page {page}"` | interpolation, expressions allowed inside `{}` | `` `page ${page}` `` |
| [ ] | `a[rel=next]` | CSS attribute selector | same CSS |
| [ ] | `Path("output")` | a path object, not a string | `path.join` but object-oriented |
| [ ] | `OUTPUT_DIR / "papers.json"` | `/` joins paths | `path.join(dir, file)` |
| [ ] | `.mkdir(exist_ok=True)` | create a folder, don't error if it exists | `mkdir -p` |
| [ ] | `.write_bytes(...)` / `.write_text(...)` | write a whole file in one call | `fs.writeFileSync` |
| [ ] | `TypeAdapter(list[Paper])` | validate/serialise a **list** of models | `z.array(PaperSchema)` |
| [ ] | `with httpx.Client() as client:` | context manager: guaranteed cleanup on exit | `try/finally`, or `using` |
| [ ] | `response.content` vs `.text` | raw bytes vs decoded string | `arrayBuffer()` vs `text()` |
| [ ] | `.raise_for_status()` | throw on a 4xx/5xx response | `if (!res.ok) throw ...` |
| [ ] | `.exists()` | does this path exist? | `fs.existsSync` |
| [ ] | `continue` | skip to the next loop iteration | `continue`, identical |
| [ ] | `parents=True` | also create missing parent folders | `mkdir -p` |

## Not yet covered, coming soon
- `with` statement / context managers (`with httpx.Client() as client:`)
- list comprehensions (`[p.title for p in papers]`)
- `dict` vs `list` vs `tuple` vs `set`
- pydantic models (`class Paper(BaseModel)`)
- exceptions: `try` / `except` / `raise`
- `pathlib.Path` for file paths
- generators and `yield`
