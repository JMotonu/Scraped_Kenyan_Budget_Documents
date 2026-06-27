import customtkinter as ctk

import webbrowser

from tkinter import messagebox

from database.mongodb import (
    get_documents,
    delete_document,
    mark_viewed,
    get_documents_count
)

from scraper.parliament_scraper import scrape_parliament

from scraper.treasury_scraper import scrape_treasury

from exports import export_csv


class Dashboard(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title(
            "Budget Document Management System"
        )

        self.geometry("1200x750")

        ctk.set_appearance_mode("dark")

        ctk.set_default_color_theme("blue")

        self.build_ui()

        self.load_documents()


    def build_ui(self):

        self.header = ctk.CTkLabel(
            self,
            text="Budget Document Management System",
            font=("Arial", 28, "bold")
        )

        self.header.pack(
            pady=20
        )

        self.search_entry = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="Search documents..."
        )

        self.search_entry.pack(
            pady=10
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda e:
            self.load_documents()
        )

        self.button_frame = ctk.CTkFrame(self)

        self.button_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.refresh_btn = ctk.CTkButton(
            self.button_frame,
            text="Refresh",
            command=self.load_documents
        )

        self.refresh_btn.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.scrape_btn = ctk.CTkButton(
            self.button_frame,
            text="Scrape Documents",
            command=self.run_scrapers
        )

        self.scrape_btn.pack(
            side="left",
            padx=10
        )

        self.export_btn = ctk.CTkButton(
            self.button_frame,
            text="Export CSV",
            command=self.export_documents
        )

        self.export_btn.pack(
            side="left",
            padx=10
        )

        self.stats_label = ctk.CTkLabel(
            self,
            text="Total Documents: 0",
            font=("Arial", 18)
        )

        self.stats_label.pack(
            pady=10
        )

        self.documents_frame = (
            ctk.CTkScrollableFrame(self)
        )

        self.documents_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


    def load_documents(self):

        for widget in (
            self.documents_frame.winfo_children()
        ):
            widget.destroy()

        documents = get_documents()

        search_text = (
            self.search_entry.get()
            .lower()
            .strip()
        )

        self.stats_label.configure(
            text=f"Total Documents: {len(documents)}"
        )

        for doc in documents:

            if search_text:

                if (
                    search_text
                    not in doc["title"].lower()
                ):
                    continue

            self.create_document_card(doc)


    def create_document_card(
            self,
            doc
    ):

        card = ctk.CTkFrame(
            self.documents_frame
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        title = ctk.CTkLabel(
            card,
            text=doc["title"],
            font=("Arial", 16, "bold")
        )

        title.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        source = ctk.CTkLabel(
            card,
            text=f"Source: {doc['source']}"
        )

        source.pack(
            anchor="w",
            padx=10
        )

        viewed = doc.get(
            "viewed",
            False
        )

        status = (
            "Viewed"
            if viewed
            else
            "Not Viewed"
        )

        status_label = ctk.CTkLabel(
            card,
            text=f"Status: {status}"
        )

        status_label.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        actions = ctk.CTkFrame(card)

        actions.pack(
            fill="x",
            padx=10,
            pady=10
        )

        open_btn = ctk.CTkButton(
            actions,
            text="Open",
            command=lambda:
            webbrowser.open(
                doc["url"]
            )
        )

        open_btn.pack(
            side="left",
            padx=5
        )

        viewed_btn = ctk.CTkButton(
            actions,
            text="Viewed",
            command=lambda:
            self.mark_document(
                doc["_id"]
            )
        )

        viewed_btn.pack(
            side="left",
            padx=5
        )

        delete_btn = ctk.CTkButton(
            actions,
            text="Delete",
            command=lambda:
            self.delete_document_ui(
                doc["_id"]
            )
        )

        delete_btn.pack(
            side="left",
            padx=5
        )


    def mark_document(
            self,
            doc_id
    ):

        mark_viewed(
            str(doc_id)
        )

        self.load_documents()


    def delete_document_ui(
            self,
            doc_id
    ):

        delete_document(
            str(doc_id)
        )

        self.load_documents()


    def run_scrapers(self):

        scrape_parliament()

        scrape_treasury()

        messagebox.showinfo(
            "Success",
            "Documents scraped successfully"
        )

        self.load_documents()


    def export_documents(self):

        export_csv()

        messagebox.showinfo(
            "Success",
            "CSV exported successfully"
        )