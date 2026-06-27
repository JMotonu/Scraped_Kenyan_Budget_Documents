import pandas as pd

from database.mongodb import get_documents


def export_csv():

    documents = get_documents()

    rows = []

    for doc in documents:

        rows.append(
            {
                "Title": doc["title"],
                "URL": doc["url"],
                "Source": doc["source"],
                "Viewed": doc["viewed"]
            }
        )

    df = pd.DataFrame(rows)

    df.to_csv(
        "exports/documents.csv",
        index=False
    )