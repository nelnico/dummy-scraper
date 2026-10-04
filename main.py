from datetime import date, datetime
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel, TypeAdapter, field_validator

URL = "https://dummy-scrape-site.vercel.app/level/01-plain"
DOWNLOAD_URL = "https://dummy-scrape-site.vercel.app/level/01-plain/download"
OUTPUT_DIR = Path("output")
PDF_DIR = OUTPUT_DIR / "pdfs"


class Paper(BaseModel):
    id: str
    title: str
    authors: str
    section: str
    published: date
    issue: str
    page_start: int
    page_end: int
    size_kb: float

    @field_validator("published", mode="before")
    @classmethod
    def parse_published(cls, value: str) -> date:
        return datetime.strptime(value, "%d %b %Y").date()


def scrape_page(page: int) -> tuple[list[Paper], bool]:
    response = httpx.get(URL, params={"page": page})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    rows = soup.select("#archive-results tbody tr")

    papers: list[Paper] = []
    for row in rows:
        title_link = row.select_one("a")
        if title_link is None:
            raise ValueError("No title link found in row")
        paper_id = row["data-paper-id"]
        cells = row.select("td")
        page_start, page_end = cells[5].text.split("-")
        size_kb = cells[6].text.removesuffix(" KB")

        paper = Paper.model_validate(
            {
                "id": paper_id,
                "title": title_link.text,
                "authors": cells[1].text,
                "section": cells[2].text,
                "published": cells[3].text,
                "issue": cells[4].text,
                "page_start": page_start,
                "page_end": page_end,
                "size_kb": size_kb,
            }
        )
        papers.append(paper)

    has_next = soup.select_one("a[rel=next]") is not None
    return papers, has_next


def save_papers(papers: list[Paper]) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / "papers.json"
    path.write_bytes(TypeAdapter(list[Paper]).dump_json(papers, indent=2))
    return path


def download_pdfs(papers: list[Paper]) -> int:
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    with httpx.Client() as client:
        for paper in papers:
            path = PDF_DIR / f"{paper.id}.pdf"
            if path.exists():
                continue

            response = client.get(f"{DOWNLOAD_URL}/{paper.id}.pdf")
            response.raise_for_status()
            path.write_bytes(response.content)
            downloaded += 1

    return downloaded


def main() -> None:
    papers: list[Paper] = []
    page = 1

    while True:
        batch, has_next = scrape_page(page)
        papers.extend(batch)
        print(f"page {page}: {len(batch)} papers")

        if not has_next:
            break
        page += 1

    path = save_papers(papers)
    print(f"total: {len(papers)} papers -> {path}")

    downloaded = download_pdfs(papers)
    print(f"downloaded {downloaded} new PDFs -> {PDF_DIR}")


if __name__ == "__main__":
    main()
