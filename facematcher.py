
"""facematcher.py

Simple utility for detecting faces in images and comparing whether the first
face in *image A* appears to match the first face in *image B* using the
Google Cloud Vision API.

Examples
--------
Detect and visualise faces:

    python facematcher.py detect --image photo.jpg --show

Compare two faces:

    python facematcher.py compare --image-a alice.jpg --image-b bob.jpg

Notes
-----
* You need a Google Cloud project with the Vision API enabled and a service
  account JSON key file. Either set the path in the *GOOGLE_APPLICATION_CREDENTIALS*
  environment variable or pass ``--credentials`` on the command line.
* This script relies on *Pillow* and *matplotlib* for optional visualisation.
* The comparison heuristic here is extremely naive – it simply measures the
  sum of absolute differences between corresponding facial landmark positions.
  For production‑grade matching you would use an embedding model such as
  FaceNet. Adjust the ``--threshold`` option to tune sensitivity.
"""

from __future__ import annotations

import argparse
import io
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence

from google.cloud import vision
from google.cloud.vision_v1 import types as vision_types
from PIL import Image, ImageDraw

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
DEFAULT_THRESHOLD: float = 100.0
LOG = logging.getLogger(__name__)


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
        raise RuntimeError(f"Vision API error: {response.error.message}")
    return response.face_annotations  # type: ignore[return-value]


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


def compare_faces(
    image_a: str | Path,
    image_b: str | Path,
    client: vision.ImageAnnotatorClient,
    threshold: float = DEFAULT_THRESHOLD,
) -> tuple[bool, float]:
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


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------
def _build_client(credentials: str | None) -> vision.ImageAnnotatorClient:
    if credentials:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
    return vision.ImageAnnotatorClient()


def _cmd_detect(args: argparse.Namespace) -> None:
    client = _build_client(args.credentials)
    faces = detect_faces(args.image, client)
    LOG.info("%d face(s) detected", len(faces))
    if args.show:
        draw_faces(args.image, faces)


def _cmd_compare(args: argparse.Namespace) -> None:
    client = _build_client(args.credentials)
    match, score = compare_faces(args.image_a, args.image_b, client, args.threshold)
    status = "MATCH ✅" if match else "NO MATCH ❌"
    print(f"Face comparison score: {score:.2f} — {status}")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Face detection and naive matching utility.")
    parser.add_argument("--credentials", help="Path to Google Cloud service‑account JSON key.")

    sub = parser.add_subparsers(required=True)

    p_detect = sub.add_parser("detect", help="Detect faces in an image")
    p_detect.add_argument("--image", required=True, help="Path to the image file")
    p_detect.add_argument("--show", action="store_true", help="Display the image with bounding boxes")
    p_detect.set_defaults(func=_cmd_detect)

    p_compare = sub.add_parser("compare", help="Compare the first faces in two images")
    p_compare.add_argument("--image-a", required=True, help="Path to the first image file")
    p_compare.add_argument("--image-b", required=True, help="Path to the second image file")
    p_compare.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD, help="Match threshold (lower is stricter)")
    p_compare.set_defaults(func=_cmd_compare)

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = _parse_args(argv)
    try:
        args.func(args)
    except Exception as exc:  # noqa: BLE001
        LOG.error("%s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
