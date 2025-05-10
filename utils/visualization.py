"""Visualization utilities for face detection results."""

from pathlib import Path
from typing import Sequence

from google.cloud.vision_v1 import types as vision_types
from PIL import Image, ImageDraw

from facematcher.core.face_detector import BoundingBox


def draw_faces(image_path: str | Path, faces: Sequence[vision_types.FaceAnnotation]) -> None:
    """Show *image_path* with red rectangles drawn around *faces*."""
    try:
        import matplotlib.pyplot as plt  # Lazy import so tests don't need it
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise RuntimeError("matplotlib is required for --show") from exc

    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = BoundingBox.from_vision(face).vertices
        # Draw polygon plus closing edge
        draw.line(box + [box[0]], width=3, fill="red")

    plt.figure(figsize=(8, 8))
    plt.imshow(im)
    plt.axis("off")
    plt.tight_layout()
    plt.show() 