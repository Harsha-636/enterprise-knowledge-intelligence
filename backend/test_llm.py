from backend.app.generation.llm_service import generate_answer


answer = generate_answer(
    question="What is 2 + 2?",
    context="Basic mathematics: 2 + 2 = 4.",
)

print("Answer:")
print(answer)