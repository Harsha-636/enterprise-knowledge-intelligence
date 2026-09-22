import re


def validate_grounding(
    answer: str,
    context: str,
    threshold: float = 0.25,
) -> dict:
    if not answer.strip():
        return {
            "grounded": False,
            "score": 0.0,
            "reason": "Empty answer",
        }

    if not context.strip():
        return {
            "grounded": False,
            "score": 0.0,
            "reason": "No supporting context",
        }

    answer_words = set(
        re.findall(r"\b[a-zA-Z0-9+#.]+\b", answer.lower())
    )

    context_words = set(
        re.findall(r"\b[a-zA-Z0-9+#.]+\b", context.lower())
    )

    stop_words = {
        "the", "a", "an", "is", "are", "was", "were",
        "this", "that", "these", "those", "and", "or",
        "of", "in", "on", "to", "for", "with", "from",
        "it", "as", "at", "by",
    }

    answer_words -= stop_words

    if not answer_words:
        return {
            "grounded": False,
            "score": 0.0,
            "reason": "No meaningful answer terms",
        }

    matched_words = answer_words.intersection(context_words)

    score = len(matched_words) / len(answer_words)

    grounded = score >= threshold

    return {
        "grounded": grounded,
        "score": round(score, 4),
        "reason": (
            "Answer is supported by retrieved context"
            if grounded
            else "Answer has insufficient overlap with retrieved context"
        ),
    }