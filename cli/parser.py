"""CLI argument parsing."""

import argparse
from typing import List

from facematcher.core.face_comparator import DEFAULT_THRESHOLD


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Face detection and naive matching utility.")
    parser.add_argument("--credentials", help="Path to Google Cloud service‑account JSON key.")

    sub = parser.add_subparsers(required=True)

    p_detect = sub.add_parser("detect", help="Detect faces in an image")
    p_detect.add_argument("--image", required=True, help="Path to the image file")
    p_detect.add_argument("--show", action="store_true", help="Display the image with bounding boxes")
    p_detect.set_defaults(func="detect")

    p_compare = sub.add_parser("compare", help="Compare the first faces in two images")
    p_compare.add_argument("--image-a", required=True, help="Path to the first image file")
    p_compare.add_argument("--image-b", required=True, help="Path to the second image file")
    p_compare.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help="Match threshold (lower is stricter)"
    )
    p_compare.set_defaults(func="compare")

    return parser.parse_args(argv) 