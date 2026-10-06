from app.services.pdf_loader import extract_text_from_pdf
from app.services.text_splitter import split_text
from app.services.vector_store import add_chunks, search_chunks



pdf_path = "uploads/resume.pdf"

text = extract_text_from_pdf(pdf_path)

print("Extracted text:", len(text), "characters")


chunks = split_text(text)

print("Total chunks:", len(chunks))


count = add_chunks(
    chunks,
    document_name="resume.pdf")

print("Stored chunks:", count)

query = "What are the technical skills?"

results = search_chunks(query, top_k=2)


print("\nSearch results:")
print(results)