from backend.app.retrieval.query_rewriter import rewrite_query


questions = [
    "What programming skills does Harsha have?",
    "what about his backend experience?",
    "tell me about his AI work",
]


for question in questions:

    rewritten = rewrite_query(question)

    print("\nOriginal:")
    print(question)

    print("Rewritten:")
    print(rewritten)