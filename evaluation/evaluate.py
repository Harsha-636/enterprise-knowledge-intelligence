import json
import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))


from backend.app.database.connection import SessionLocal
from backend.app.models.document import Document
from backend.app.models.chunk import Chunk
from backend.app.retrieval.hybrid_search import hybrid_search
from backend.app.retrieval.reranker import rerank


DATASET_PATH = PROJECT_ROOT / "evaluation" / "dataset.json"


def normalize_text(text: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        text.lower(),
    ).strip()


def evaluate_question(
    db,
    question: str,
    expected_keywords: list[str],
    user_id: int,
) -> dict:

    candidates = hybrid_search(
        db=db,
        query=question,
        user_id=user_id,
        top_k=10,
    )

    if not candidates:
        return {
            "question": question,
            "retrieved": 0,
            "matched_keywords": [],
            "missing_keywords": expected_keywords,
            "keyword_coverage": 0.0,
        }

    results = rerank(
        query=question,
        results=candidates,
        top_k=5,
    )

    retrieved_text = " ".join(
        result["content"]
        for result in results
    )

    normalized_text = normalize_text(retrieved_text)

    matched_keywords = []
    missing_keywords = []

    for keyword in expected_keywords:
        if normalize_text(keyword) in normalized_text:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    coverage = (
        len(matched_keywords) / len(expected_keywords)
        if expected_keywords
        else 0.0
    )

    return {
        "question": question,
        "retrieved": len(results),
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "keyword_coverage": round(coverage, 4),
    }


def main():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    db = SessionLocal()

    try:
        documents = db.query(Document).order_by(Document.id).all()

        if not documents:
            print("No documents found.")
            return

        user_id = documents[0].uploaded_by

        results = []

        for item in dataset:
            result = evaluate_question(
                db=db,
                question=item["question"],
                expected_keywords=item["expected_keywords"],
                user_id=user_id,
            )

            results.append(result)

        total_coverage = sum(
            result["keyword_coverage"]
            for result in results
        ) / len(results)

        print("\n===== RAG EVALUATION =====\n")

        for index, result in enumerate(results, start=1):
            print(f"Question {index}:")
            print(result["question"])
            print(f"Retrieved chunks: {result['retrieved']}")
            print(
                f"Keyword coverage: "
                f"{result['keyword_coverage']:.2%}"
            )
            print(
                f"Matched: "
                f"{', '.join(result['matched_keywords'])}"
            )

            if result["missing_keywords"]:
                print(
                    f"Missing: "
                    f"{', '.join(result['missing_keywords'])}"
                )

            print()

        print(
            f"Overall keyword coverage: "
            f"{total_coverage:.2%}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()