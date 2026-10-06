import re


def split_text(
    pages,
    chunk_size: int = 1000,
    overlap: int = 200
):
    """
    Split PDF pages into meaningful chunks
    while preserving the page number.
    """

    chunks = []

    for page in pages:

        page_number = page["page"]
        text = page["text"]

        # Normalize spaces
        text = re.sub(r"[ \t]+", " ", text)

        # Normalize multiple blank lines
        text = re.sub(r"\n\s*\n+", "\n\n", text)

        text = text.strip()

        if not text:
            continue

        # Split page into paragraphs
        paragraphs = text.split("\n\n")

        current_chunk = ""

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            # If paragraph fits in current chunk
            if len(current_chunk) + len(paragraph) + 2 <= chunk_size:

                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph

            else:

                # Save current chunk
                if current_chunk:
                    chunks.append({
                        "text": current_chunk,
                        "page": page_number
                    })

                # Start new chunk
                current_chunk = paragraph

        # Save remaining chunk from this page
        if current_chunk:
            chunks.append({
                "text": current_chunk,
                "page": page_number
            })

    return chunks