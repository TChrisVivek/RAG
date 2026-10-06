from app.services.vector_store import search_chunks
from app.services.llm import generate_answer


#Employee'squestion
question = "What technologies does Chris know?"

# 1. Search ChromaDB
results = search_chunks(
    query=question,
    top_k=2
)

print("\nRetrieved Chunks:")

for result in results:
    print("\n-----------------")
    print("Source:", result["source"])
    print("Chunk:", result["distance"])
    print("---------------")


    print(result["text"])


context = "\n\n".join(
    result["text"]
    for result in results
)

# 4. Send the question + retrieved context to GPT-4.1
answer = generate_answer(
    question=question,
    context=context
)


# 5.Display the final answer
print("\nFinal Answer:")
print(answer)