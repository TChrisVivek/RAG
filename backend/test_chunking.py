from app.services.pdf_loader import extract_text_from_pdf
from app.services.text_splitter import split_text

pdf_path = "uploads/resume.pdf"

text = extract_text_from_pdf(pdf_path)

chunks = split_text(text)

print("Total characters:", len(text))
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print("\n" + "=" * 50)
    print(f"CHUNK {i + 1}")
    print("=" * 50)
    print(chunk)