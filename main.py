# -*- coding: utf-8 -*-
import sys
import io

# 设置控制台输出编码
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    # Python 3.6 compatibility
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')

from PIL import Image
from pathlib import Path


def get_file_size_str(size_bytes: int) -> str:
    """获取人类可读的文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def compress_image(image_path: Path, output_dir: Path, max_size_mb: float = 2.0) -> tuple:
    """
    压缩单张图片到指定大小以下，保存到 output 目录

    Returns:
        tuple: (output_path, original_size, compressed_size)
    """
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / image_path.name

    img = Image.open(image_path)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # 逐级降低质量直到满足大小要求
    for quality in range(95, 10, -5):
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        if output_path.stat().st_size <= max_size_mb * 1024 * 1024:
            break

    original_size = image_path.stat().st_size
    compressed_size = output_path.stat().st_size
    return output_path, original_size, compressed_size


def main():
    photos_dir = Path("photos")
    output_dir = Path("output")
    max_size_mb = 2.0

    if not photos_dir.exists():
        print(f"错误: 目录 {photos_dir} 不存在")
        return

    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    images = [f for f in photos_dir.iterdir() if f.suffix.lower() in image_extensions]

    if not images:
        print("没有找到需要压缩的图片")
        return

    print(f"找到 {len(images)} 张图片，开始压缩...\n")

    total_original = 0
    total_compressed = 0

    for img_path in images:
        try:
            _, original_size, compressed_size = compress_image(img_path, output_dir, max_size_mb)
            total_original += original_size
            total_compressed += compressed_size

            ratio = (1 - compressed_size / original_size) * 100
            status = "[OK]" if compressed_size <= max_size_mb * 1024 * 1024 else "[WARN]"

            print(f"{status} {img_path.name}")
            print(f"   原始: {get_file_size_str(original_size)} -> 压缩: {get_file_size_str(compressed_size)}")
            print(f"   减少: {ratio:.1f}%\n")
        except Exception as e:
            print(f"[FAIL] {img_path.name}: 压缩失败 - {e}\n")

    # 汇总
    total_ratio = (1 - total_compressed / total_original) * 100 if total_original > 0 else 0
    print("=" * 40)
    print(f"总计: {get_file_size_str(total_original)} -> {get_file_size_str(total_compressed)}")
    print(f"总共减少: {total_ratio:.1f}%")
    print(f"输出目录: {output_dir.absolute()}")


if __name__ == "__main__":
    main()
