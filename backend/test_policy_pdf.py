import pymupdf

pdf_path = "uploads/HR Policies - Pytheos Health Systems 2_1228.pdf"

document = pymupdf.open(pdf_path)

print("Number of pages:", len(document))

total_characters = 0

for page_number, page in enumerate(document, start=1):

    text = page.get_text()

    print(
        f"Page {page_number}: {len(text)} characters"
    )

    total_characters += len(text)

print("\nTotal characters:", total_characters)

document.close()