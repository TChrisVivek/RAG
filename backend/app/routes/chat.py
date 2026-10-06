from fastapi import APIRouter
from pydantic import BaseModel

from app.services.vector_store import search_chunks
from app.services.llm import generate_answer


router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    # Get the question from the request body
    question = request.question

    # Retrieve relevant chunks from ChromaDB
    results = search_chunks(
        query=question,
        top_k=3
    )

    print("\n==== Retrieved Chunks ===")

    for result in results:
        print("\n---------------------------")
        print("Source:", result["source"])
        print("Chunk:", result["chunk_index"])
        print("Distance:", result["distance"])
        print(result["text"])

    # Combine retrieved chunks into context
    context = "\n\n".join(
        result["text"]
        for result in results
    )

    # Generate answer using GPT-4.1
    answer = generate_answer(
        question=question,
        context=context
    )

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "document": result["source"],
                "page": result["page"],
                "chunk": result["chunk_index"]
            }
            for result in results
        ]
    }