import os
import chromadb

from app.services.embeddings import create_embedding


# Create a local ChromaDB client
client = chromadb.PersistentClient(
    path="./chroma_db"
)


# Create or get the HR policy collection
collection = client.get_or_create_collection(
    name="hr_policies"
)


def add_chunks(
    chunks: list[str],
    document_name: str
):
    """
    Generate embeddings for chunks and store them
    in ChromaDB along with metadata.
    """

    embeddings = []
    documents = []
    ids = []
    metadatas = []

    # Remove .pdf from filename
    document_id = os.path.splitext(document_name)[0]

    for i, chunk in enumerate(chunks):

        # get chunk text
        chunk_text = chunk["text"]

        # get page number 
        page_number = chunk["page"]

        # Create embedding
        embedding = create_embedding(chunk["text"])

        embeddings.append(
            embedding.tolist()
        )

        # Store original text
        documents.append(chunk_text)

        # Create unique ID
        chunk_id = f"{document_id}_chunk_{i}"

        ids.append(chunk_id)

        # Store metadata
        metadatas.append({
            "source": document_name,
            "page": page_number,
            "chunk_index": i
        })

    # Store everything in ChromaDB
    collection.add(
        embeddings=embeddings,
        documents=documents,
        ids=ids,
        metadatas=metadatas
    )

    return len(chunks)


def search_chunks(
    query: str,
    top_k: int = 3,
    max_distance: float = 0.70
):

    """
    Search ChromaDB and return relevant document chunks.

    Smaller distance values generally indicate closer matches.
    Results above max_distance Are filtered out.
    """


    # Reject an empty question.
    if not query or not query.strip():
       return[]

    # Create an embedding for the user's question.
    query_embedding = create_embedding(query.strip())

    # Search ChromaDB for the closest document chunks.
    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k
    )

    retrieved_chunks = []

    # Safely get the first query's results.
    documents = results.get("documents") or [[]]
    metadatas = results.get("metadatas") or [[]]
    distances = results.get("distances") or [[]]


    documents = documents[0] if documents else []
    metadatas = metadatas[0] if metadatas else []
    distances = distances[0] if distances else []

    # Combine each documents with its metadata and distance.
    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        # Skip matches that are too distant.
        if distance > max_distance:
            continue

        # Handle missing metada safely.
        metadata = metadata or {}

        retrieved_chunks.append({
            "text": document,
            "source": metadata.get("source", "Unkown source"),
            "page": metadata.get("page"),
            "chunk_index": metadata.get("chunk_index"),
            "distance": distance
        })

    return retrieved_chunks