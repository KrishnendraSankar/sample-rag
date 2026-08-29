from app.ingestion.pdf_loader import PDFLoader


file_path = "app/uploads/employee_policy.pdf"

loader = PDFLoader()

pages = loader.load(
    file_path
)


print(
    f"Total extracted pages: {len(pages)}"
)


for page in pages[:3]:

    print()
    print("=" * 80)

    print(
        f"PAGE: {page['page_number']}"
    )

    print("=" * 80)

    print(
        page["text"][:1000]
    )