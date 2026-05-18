#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF to Images 高清切图工具

用途：
1. 将 PDF 批量切分为 PNG/JPG 图片；
2. 通过高 DPI 渲染，尽量保证上传平台后放大查看仍然清晰；
3. 适合小红书图文、学习笔记、LaTeX/PPT/Canva 导出 PDF 后切图。

安装：
    pip install pymupdf pillow

示例：
    python pdf_to_images.py input.pdf -o output_images --dpi 600
    python pdf_to_images.py input.pdf -o output_images --dpi 900 --format png
    python pdf_to_images.py input.pdf -o output_images --start 1 --end 3
"""

from __future__ import annotations

import argparse
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert PDF pages to high-resolution images."
    )

    parser.add_argument(
        "pdf",
        type=str,
        help="输入 PDF 文件路径，例如 input.pdf",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output_images",
        help="输出文件夹，默认 output_images",
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=600,
        help="导出分辨率 DPI。推荐：300/600/900，默认 600",
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["png", "jpg", "jpeg"],
        default="png",
        help="输出格式：png/jpg/jpeg，默认 png",
    )

    parser.add_argument(
        "--quality",
        type=int,
        default=95,
        help="JPG/JPEG 质量，范围 1-100，默认 95。PNG 不使用该参数",
    )

    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="起始页码，从 1 开始，默认 1",
    )

    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="结束页码，从 1 开始，默认到最后一页",
    )

    parser.add_argument(
        "--prefix",
        type=str,
        default="page",
        help="输出图片名前缀，默认 page",
    )

    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> tuple[Path, Path, str]:
    pdf_path = Path(args.pdf).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"找不到 PDF 文件：{pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"输入文件必须是 PDF：{pdf_path}")

    if args.dpi <= 0:
        raise ValueError("DPI 必须大于 0")

    if not (1 <= args.quality <= 100):
        raise ValueError("quality 必须在 1 到 100 之间")

    fmt = args.format.lower()
    if fmt == "jpeg":
        fmt = "jpg"

    output_dir.mkdir(parents=True, exist_ok=True)

    return pdf_path, output_dir, fmt


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
    将 PDF 每一页渲染成高清图片。

    PyMuPDF 默认坐标单位为 point，1 inch = 72 points。
    因此：
        zoom = dpi / 72

    例如：
        dpi=600 时，zoom≈8.33。
    """
    doc = fitz.open(pdf_path)

    total_pages = len(doc)
    if total_pages == 0:
        raise ValueError("PDF 没有页面")

    start_page = max(1, start_page)
    end_page = total_pages if end_page is None else min(end_page, total_pages)

    if start_page > end_page:
        raise ValueError(
            f"页码范围不合法：start={start_page}, end={end_page}, total={total_pages}"
        )

    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    print(f"PDF: {pdf_path}")
    print(f"总页数: {total_pages}")
    print(f"导出范围: {start_page} - {end_page}")
    print(f"DPI: {dpi}")
    print(f"输出目录: {output_dir}")
    print("-" * 50)

    for page_index in range(start_page - 1, end_page):
        page = doc[page_index]

        # alpha=False 可避免透明背景，导出白底图片。
        pix = page.get_pixmap(matrix=matrix, alpha=False)

        page_number = page_index + 1
        output_path = output_dir / f"{prefix}_{page_number:03d}.{image_format}"

        if image_format == "png":
            pix.save(output_path)
        else:
            # JPG 需要通过 PIL 保存，避免 alpha/模式问题。
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            img.save(output_path, quality=quality, optimize=True)

        print(f"已导出：{output_path.name}  {pix.width}×{pix.height}px")

    doc.close()
    print("-" * 50)
    print("完成。")


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
