#!/usr/bin/env python3
"""批量压缩 source/img 下的图片。

用法：
    python tools/compress-images.py [目录] [--max-edge 1600] [--quality 82] [--threshold-kb 300]

规则：
- 长边超过 max_edge 的等比缩小；
- JPEG 超过阈值时按 quality 重新编码；
- PNG 超过阈值时重新优化（照片建议先转 JPG，PNG 对照片压缩率差）。
- 已小于阈值的文件不动。
"""

import argparse
import io
import os
from pathlib import Path

from PIL import Image

EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def compress(path: Path, max_edge: int, quality: int, threshold: int) -> tuple[int, int]:
    before = path.stat().st_size
    if before <= threshold:
        return before, before

    with Image.open(path) as im:
        im = im.convert("RGB") if im.mode in ("RGBA", "P") and path.suffix.lower() != ".png" else im
        im.thumbnail((max_edge, max_edge), Image.LANCZOS)
        suffix = path.suffix.lower()
        buf = io.BytesIO()
        if suffix == ".png":
            im.save(buf, "PNG", optimize=True)
        elif suffix == ".webp":
            im.save(buf, "WEBP", quality=quality, method=6)
        else:
            im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)

    # 压缩后反而更大就保留原图
    if buf.tell() >= before:
        return before, before

    path.write_bytes(buf.getvalue())
    return before, path.stat().st_size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", default="source/img")
    parser.add_argument("--max-edge", type=int, default=1600)
    parser.add_argument("--quality", type=int, default=82)
    parser.add_argument("--threshold-kb", type=int, default=300)
    args = parser.parse_args()

    threshold = args.threshold_kb * 1024
    total_before = total_after = 0

    for path in sorted(Path(args.target).rglob("*")):
        if path.suffix.lower() not in EXTS or not path.is_file():
            continue
        before, after = compress(path, args.max_edge, args.quality, threshold)
        if before != after:
            total_before += before
            total_after += after
            print(f"{path}: {before / 1024:.0f}KB -> {after / 1024:.0f}KB")

    if total_before:
        saved = (total_before - total_after) / 1024 / 1024
        print(f"\n共节省 {saved:.2f} MB")
    else:
        print("没有需要压缩的图片")


if __name__ == "__main__":
    main()
