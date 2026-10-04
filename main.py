import httpx

URL = "https://dummy-scrape-site.vercel.app/level/01-plain?page=1"


def main() -> None:
    response = httpx.get(URL)
    print(response.status_code)
    print(response.text[:500])


if __name__ == "__main__":
    main()
