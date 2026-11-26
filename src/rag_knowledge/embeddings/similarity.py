import numpy as np


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:

    a = np.asarray(vector_a, dtype=float)
    b = np.asarray(vector_b, dtype=float)

    if a.ndim != 1 or b.ndim != 1:
        raise ValueError("Vectors must be one-dimensional")

    if a.shape != b.shape:
        raise ValueError("Vector dimensions must match")

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        raise ValueError("Zero vectors are not supported")

    return float(np.dot(a, b) / (norm_a * norm_b))
