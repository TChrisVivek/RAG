from app.services.llm import generate_answer

question = "What technologies does Chris Know?"

context = """
Technical Skills:
Language: C++, Python, JavaScript
Frontend: React,js, Next.js, Tailwind CSS
Backend: Node.js, Express.js, Spring Boot
Databases: PostgresSQL, MngoDB
"""


answer = generate_answer(
    question=question,
    context=context
)

print("Question:")
print(question)

print("\nAnswer")
print(answer)

