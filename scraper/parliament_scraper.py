import requests

from bs4 import BeautifulSoup

from config import PARLIAMENT_URL

from database.mongodb import save_document


def scrape_parliament():

    response = requests.get(PARLIAMENT_URL)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    links = soup.find_all("a")

    count = 0

    for link in links:

        href = link.get("href")

        title = link.get_text(strip=True)

        if href and ".pdf" in href.lower():

            if href.startswith("/"):

                href = (
                    "https://www.parliament.go.ke"
                    + href
                )

            document = {
                "title": title,
                "url": href,
                "source": "Parliament",
                "viewed": False
            }

            save_document(document)

            count += 1

            if count >= 17:
                break