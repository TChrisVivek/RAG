from app.services.pdf_loader import extract_text_from_pdf

pdf_path = "uploads/resume.pdf"

text = extract_text_from_pdf(pdf_path)

print(text)
