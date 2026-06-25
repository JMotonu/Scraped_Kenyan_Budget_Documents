import requests

from bs4 import BeautifulSoup

from config import TREASURY_URL

from database.mongodb import save_document


def scrape_treasury():

    response = requests.get(TREASURY_URL)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    links = soup.find_all("a")

    for link in links:

        href = link.get("href")

        title = link.get_text(strip=True)

        if href and ".pdf" in href.lower():

            if (
                "2026" in title
                or "2025" in title
            ):

                if href.startswith("/"):

                    href = (
                        "https://www.treasury.go.ke"
                        + href
                    )

                document = {
                    "title": title,
                    "url": href,
                    "source": "Treasury",
                    "viewed": False
                }

                save_document(document)