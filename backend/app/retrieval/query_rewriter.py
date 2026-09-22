import re


def rewrite_query(question: str) -> str:
    """
    Lightweight local query rewriting.
    Removes conversational filler while preserving
    important keywords.
    """

    query = question.strip()

    query = re.sub(
        r"\b(can you|could you|please|tell me|show me|i want to know)\b",
        "",
        query,
        flags=re.IGNORECASE,
    )

    query = re.sub(r"\s+", " ", query).strip()

    return query