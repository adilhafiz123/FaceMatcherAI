"""Face comparison functionality."""

from pathlib import Path
from typing import Sequence, Tuple

from google.cloud import vision
from google.cloud.vision_v1 import types as vision_types

from facematcher.core.face_detector import detect_faces

DEFAULT_THRESHOLD: float = 100.0


def compare_faces(
    image_a: str | Path,
    image_b: str | Path,
    client: vision.ImageAnnotatorClient,
    threshold: float = DEFAULT_THRESHOLD,
) -> Tuple[bool, float]:
    """Compare the first face in *image_a* and *image_b*.

    Returns
    -------
    match : bool
        ``True`` if the match score is *below* the *threshold*.
    score : float
        Raw match score (lower means more similar under this heuristic).
    """
    faces_a = detect_faces(image_a, client)
    faces_b = detect_faces(image_b, client)

    if not faces_a or not faces_b:
        raise ValueError("No faces detected in one or both images.")

    face_a, face_b = faces_a[0], faces_b[0]

    score = sum(
        abs(l1.position.x - l2.position.x) + abs(l1.position.y - l2.position.y)  # type: ignore[attr-defined]
        for l1, l2 in zip(face_a.landmarks, face_b.landmarks)
    )

    return score < threshold, score 