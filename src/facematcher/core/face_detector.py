"""Core face detection functionality."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence

from google.cloud import vision
from google.cloud.vision_v1 import types as vision_types


@dataclass
class BoundingBox:
    vertices: List[tuple[int, int]]

    @classmethod
    def from_vision(cls, face: vision_types.FaceAnnotation) -> "BoundingBox":
        vertices = [(v.x, v.y) for v in face.bounding_poly.vertices]
        return cls(vertices)


def _load_image_bytes(path: str | Path) -> bytes:
    """Read an image from *path* and return raw bytes."""
    with open(path, "rb") as fh:
        return fh.read()


def detect_faces(image_path: str | Path, client: vision.ImageAnnotatorClient) -> Sequence[vision_types.FaceAnnotation]:
    """Return a sequence of faces detected in *image_path*."""
    content = _load_image_bytes(image_path)
    img = vision_types.Image(content=content)  # type: ignore[attr-defined]
    response = client.face_detection(image=img)
    if response.error.message:
        raise RuntimeError(f"Vision API error: {response.error.message}")
    return response.face_annotations  # type: ignore[return-value] 