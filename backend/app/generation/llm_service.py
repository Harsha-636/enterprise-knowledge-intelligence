import re


def local_fallback_answer(
    question: str,
    context: str,
) -> str:
    """
    Local extractive fallback.

    Returns only information that already exists
    in the retrieved document context.
    """

    if not context.strip():
        return (
            "I could not find this information "
            "in the available documents."
        )

    question_words = set(
        re.findall(r"\b[a-zA-Z0-9+#.]+\b", question.lower())
    )

    stop_words = {
        "what", "what's", "who", "where", "when",
        "why", "how", "is", "are", "was", "were",
        "the", "a", "an", "does", "do", "did",
        "can", "could", "tell", "me", "about",
        "his", "her", "their", "and", "or", "of",
        "in", "on", "to", "for"
    }

    question_words -= stop_words

    chunks = re.findall(
        r"\[Chunk (\d+)\]\s*(.*?)(?=\n\n\[Chunk \d+\]|\Z)",
        context,
        flags=re.DOTALL,
    )

    candidates = []

    for chunk_id, chunk_text in chunks:

        sentences = re.split(
            r"(?<=[.!?])\s+",
            chunk_text.strip(),
        )

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            sentence_words = set(
                re.findall(
                    r"\b[a-zA-Z0-9+#.]+\b",
                    sentence.lower(),
                )
            )

            matches = question_words.intersection(
                sentence_words
            )

            if matches:
                score = len(matches)

                candidates.append(
                    (
                        score,
                        int(chunk_id),
                        sentence,
                    )
                )

    candidates.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    if not candidates:
        return (
            "I could not find this information "
            "in the available documents."
        )

    selected = []
    used_sentences = set()

    for score, chunk_id, sentence in candidates:

        if sentence in used_sentences:
            continue

        selected.append(
            f"{sentence} [Chunk {chunk_id}]"
        )

        used_sentences.add(sentence)

        if len(selected) == 3:
            break

    return " ".join(selected)


def generate_answer(
    question: str,
    context: str,
) -> str:

    return local_fallback_answer(
        question=question,
        context=context,
    )