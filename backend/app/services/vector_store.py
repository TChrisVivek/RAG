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
    top_k: int = 3
):
    """
    Search ChromaDB and return the most relevant
    document chunks with their metadata.
    """

    # Create embedding for the user's question
    query_embedding = create_embedding(query)

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k
    )

    retrieved_chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        retrieved_chunks.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "chunk_index": metadata["chunk_index"],
            "distance": distance
        })

    return retrieved_chunks