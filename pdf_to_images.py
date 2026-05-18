#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF to Images High-Resolution Export Tool

Purpose:
1. Convert PDF pages into PNG/JPG images in batch.
2. Render PDF pages with high DPI to keep images clear when zoomed in.

Installation:
    pip install pymupdf pillow

Examples:
    python pdf_to_images.py
    python pdf_to_images.py data/input.pdf -o results --dpi 600
    python pdf_to_images.py data/input.pdf -o results --dpi 900 --format png
    python pdf_to_images.py data/input.pdf -o results --start 1 --end 3
"""

from __future__ import annotations

import argparse
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image


# ============================================================
# Default settings
# ============================================================

# Put your PDF file path here.
# Example 1: relative path
# DEFAULT_PDF_PATH = r"data/2-奇异值知识点总结.pdf"
#
# Example 2: Windows absolute path
# DEFAULT_PDF_PATH = r"D:\software\EdgeDownload\pdf-to-images\data\2-奇异值知识点总结.pdf"

DEFAULT_PDF_PATH = r"./data/PDF_example.pdf"
DEFAULT_OUTPUT_DIR = r"results"
DEFAULT_DPI = 600
DEFAULT_FORMAT = "png"
DEFAULT_QUALITY = 95
DEFAULT_PREFIX = "page"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert PDF pages to high-resolution images."
    )

    parser.add_argument(
        "pdf",
        type=str,
        nargs="?",
        default=DEFAULT_PDF_PATH,
        help=f"Input PDF file path. Default: {DEFAULT_PDF_PATH}",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output folder. Default: {DEFAULT_OUTPUT_DIR}",
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=DEFAULT_DPI,
        help="Export resolution in DPI. Recommended: 300, 600, or 900. Default: 600",
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["png", "jpg", "jpeg"],
        default=DEFAULT_FORMAT,
        help="Output image format: png, jpg, or jpeg. Default: png",
    )

    parser.add_argument(
        "--quality",
        type=int,
        default=DEFAULT_QUALITY,
        help="JPG/JPEG quality, from 1 to 100. Default: 95. This option does not affect PNG.",
    )

    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Start page number, starting from 1. Default: 1",
    )

    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="End page number, starting from 1. Default: the last page",
    )

    parser.add_argument(
        "--prefix",
        type=str,
        default=DEFAULT_PREFIX,
        help=f"Output image filename prefix. Default: {DEFAULT_PREFIX}",
    )

    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> tuple[Path, Path, str]:
    pdf_path = Path(args.pdf).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"The input file must be a PDF file: {pdf_path}")

    if args.dpi <= 0:
        raise ValueError("DPI must be greater than 0.")

    if not (1 <= args.quality <= 100):
        raise ValueError("Quality must be between 1 and 100.")

    image_format = args.format.lower()
    if image_format == "jpeg":
        image_format = "jpg"

    output_dir.mkdir(parents=True, exist_ok=True)

    return pdf_path, output_dir, image_format


def convert_pdf_to_images(
    pdf_path: Path,
    output_dir: Path,
    dpi: int = 600,
    image_format: str = "png",
    quality: int = 95,
    start_page: int = 1,
    end_page: int | None = None,
    prefix: str = "page",
) -> None:
    """
    Render each PDF page as a high-resolution image.

    PyMuPDF uses points as the default unit:
        1 inch = 72 points

    Therefore:
        zoom = dpi / 72

    For example:
        dpi = 600 means zoom is about 8.33.
    """

    doc = fitz.open(pdf_path)

    total_pages = len(doc)
    if total_pages == 0:
        raise ValueError("The PDF file has no pages.")

    start_page = max(1, start_page)
    end_page = total_pages if end_page is None else min(end_page, total_pages)

    if start_page > end_page:
        raise ValueError(
            f"Invalid page range: start={start_page}, end={end_page}, total={total_pages}"
        )

    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    print(f"PDF file: {pdf_path}")
    print(f"Total pages: {total_pages}")
    print(f"Export range: {start_page} - {end_page}")
    print(f"DPI: {dpi}")
    print(f"Output folder: {output_dir}")
    print("-" * 60)

    for page_index in range(start_page - 1, end_page):
        page = doc[page_index]

        # alpha=False creates images with a white background instead of transparency.
        pix = page.get_pixmap(matrix=matrix, alpha=False)

        page_number = page_index + 1
        output_path = output_dir / f"{prefix}_{page_number:03d}.{image_format}"

        if image_format == "png":
            pix.save(output_path)
        else:
            # Save JPG/JPEG through Pillow to control quality.
            image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            image.save(output_path, quality=quality, optimize=True)

        print(f"Exported: {output_path.name}  {pix.width} x {pix.height}px")

    doc.close()
    print("-" * 60)
    print("Done.")


def main() -> None:
    args = parse_args()
    pdf_path, output_dir, image_format = validate_args(args)

    convert_pdf_to_images(
        pdf_path=pdf_path,
        output_dir=output_dir,
        dpi=args.dpi,
        image_format=image_format,
        quality=args.quality,
        start_page=args.start,
        end_page=args.end,
        prefix=args.prefix,
    )


if __name__ == "__main__":
    main()