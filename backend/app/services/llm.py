import os


from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set.")

client = OpenAI(api_key=api_key)

def generate_answer(question: str, context: str) -> str:

    prompt = f"""
Answer the user's question using only the information
provided in the context below.

If the answer cannot be found in the context, say:
"I could not find this information in the provided context."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return response.output_text
