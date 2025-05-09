"""CLI command implementations."""

import logging
from pathlib import Path

from google.cloud import vision

from facematcher.core.face_detector import detect_faces
from facematcher.core.face_comparator import compare_faces
from facematcher.utils.visualization import draw_faces

LOG = logging.getLogger(__name__)


def _build_client(credentials: str | None) -> vision.ImageAnnotatorClient:
    """Build and return a Vision API client."""
    if credentials:
        import os
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
    return vision.ImageAnnotatorClient()


def cmd_detect(args) -> None:
    """Handle the detect command."""
    client = _build_client(args.credentials)
    faces = detect_faces(args.image, client)
    LOG.info("%d face(s) detected", len(faces))
    if args.show:
        draw_faces(args.image, faces)


def cmd_compare(args) -> None:
    """Handle the compare command."""
    client = _build_client(args.credentials)
    match, score = compare_faces(args.image_a, args.image_b, client, args.threshold)
    status = "MATCH ✅" if match else "NO MATCH ❌"
    print(f"Face comparison score: {score:.2f} — {status}") 