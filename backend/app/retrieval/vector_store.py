import json
from pathlib import Path


VECTOR_STORE_PATH = Path("storage/vectors.json")


def save_embedding(
    chunk_id: int,
    embedding: list[float],
) -> None:
    VECTOR_STORE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if VECTOR_STORE_PATH.exists():
        data = json.loads(
            VECTOR_STORE_PATH.read_text()
        )
    else:
        data = {}

    data[str(chunk_id)] = embedding

    VECTOR_STORE_PATH.write_text(
        json.dumps(data)
    )


def load_embeddings() -> dict[str, list[float]]:
    if not VECTOR_STORE_PATH.exists():
        return {}

    return json.loads(
        VECTOR_STORE_PATH.read_text()
    )