from app.services.embeddings import create_embedding

text = "Employees receive 20 days of annual leave."

embedding = create_embedding(text)

print("embedding type:", type(embedding))
print("embedding dimensions:", len(embedding))
print("First 10 values:")
print(embedding[:10])