# app/scripts/test_docx_loader.py

from app.ingestion.docx_loader import (
    DOCXLoader,
)


file_path = (
    "app/uploads/onboarding.docx"
)


loader = DOCXLoader()


elements = loader.load(
    file_path
)


print(
    f"Total extracted elements: "
    f"{len(elements)}"
)


for element in elements[:30]:

    print(
        element
    )