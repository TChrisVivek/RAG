from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

from app.services.pdf_loader import extract_text_from_pdf
from app.services.text_splitter import split_text
from app.services.vector_store import add_chunks


router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    print("Filename:", file.filename)
    print("Content type:", file.content_type)

    # 1. Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # 2. Save PDF
    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)

    if file_size == 0:
        os.remove(file_path)

        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty."
        )

    print("PDF saved:", file_path)

    # 3. Extract text page by page
    pages = extract_text_from_pdf(file_path)

    if not pages:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from PDF."
        )
    total_characters = sum(
        len(page["text"])
        for page in pages
    )

    print("Pages extracted:",len(pages))
    print("Extracted characters:", total_characters)

    # 4. Split text into chunks
    chunks = split_text(pages)

    print("Created chunks:", len(chunks))

    # 5. Create embeddings and store in ChromaDB
    stored_chunks = add_chunks(
        chunks=chunks,
        document_name=file.filename
    )

    print("Stored chunks:", stored_chunks)

    return {
        "message": "PDF uploaded and processed successfully",
        "filename": file.filename,
        "size": file_size,
        "characters": total_characters,
        "chunks": stored_chunks
    }