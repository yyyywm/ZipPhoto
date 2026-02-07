# ZipPhoto - Image Batch Compression Tool

> **中文版**: [README.zh-CN.md](README.md)

A simple and easy-to-use image batch compression tool that reduces images to a specified size.

## Features

- Batch compression: Process multiple images at once
- Size control: Automatically compress images below 2MB
- Format support: Supports JPG, PNG, BMP, WebP and other common formats
- Preserve originals: Compressed images saved to `output/` directory
- Detailed statistics: Shows before/after size comparison for each image

## Quick Start

### 1. Prerequisites

Make sure you have Python 3.7 or later installed. Open your terminal:

```bash
# Check Python version
python --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

### 2. Install Dependencies

Run this command in the project root:

```bash
pip install -r requirements.txt
```

This installs the project's only dependency: `Pillow` (a powerful image processing library).

### 3. Add Images

Place your images in the `photos/` directory. Supported formats:
- `.jpg` / `.jpeg`
- `.png`
- `.bmp`
- `.webp`

### 4. Run the Program

```bash
python main.py
```

### 5. Check Results

Compressed images are saved in the `output/` directory, and compression statistics are displayed in the terminal.

---

## How It Works (Beginner Friendly)

### What is Image Compression?

When you take a photo, the camera saves lots of detail information (like the color of every leaf, the position of every ray of sunshine). This makes photos very large, sometimes several MB.

**Image compression** finds ways to remove "unnecessary" information while keeping quality acceptable, making files smaller.

### Compression Method Used in This Project

This project uses **JPEG lossy compression**. Here's the core principle:

#### Step 1: Open the Image

```python
img = Image.open(image_path)
```

Use Pillow library to read the image file, just like opening a photo in an image viewer.

#### Step 2: Color Mode Conversion

```python
if img.mode in ('RGBA', 'P'):
    img = img.convert('RGB')
```

This ensures consistent image format:
- `RGBA`: Images with transparency channel (common in PNG)
- `P`: Palette mode images
- `RGB`: Standard color mode (JPEG only supports this)

#### Step 3: Progressive Quality Reduction

```python
for quality in range(95, 10, -5):
    img.save(output_path, 'JPEG', quality=quality, optimize=True)
    if output_path.stat().st_size <= max_size_mb * 1024 * 1024:
        break
```

This is the core compression logic:

1. **Quality parameter (95 → 10)**: Start from high quality
2. **Step size (-5)**: Reduce quality by 5% each time
3. **Optimization (optimize=True)**: Use more efficient JPEG encoding
4. **Auto-stop**: Stop once file is under 2MB to minimize quality loss

**Why use a loop?**

Because the "optimal compression rate" varies for each image. Some simple images达标 easily with light compression; others with rich details need more aggressive compression. The loop finds the "sweet spot" for each image.

---

## Project Structure

```text
zipphoto/
├── main.py           # Main program containing all logic
├── requirements.txt  # Project dependencies (Pillow)
├── photos/          # Directory for images to compress
└── output/          # Output directory for compressed images (auto-generated)
```

### Code Explanation

#### `get_file_size_str()` Function

```python
def get_file_size_str(size_bytes: int) -> str:
    """Get human-readable file size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"
```

Converts bytes to human-readable format:
- `1024` bytes = 1 KB
- `1024 KB` = 1 MB
- `1024 MB` = 1 GB

Example: `4346044` bytes → `4.14 MB`

#### `compress_image()` Function

```python
def compress_image(image_path: Path, output_dir: Path, max_size_mb: float = 2.0) -> tuple:
```

Takes an image path and output directory, returns compression info after processing.

#### `main()` Function

Program entry point, responsible for:
1. Checking if `photos/` directory exists
2. Finding all supported image files
3. Calling compression function for each image
4. Displaying summary statistics

---

## Customization

### Change Target Size

Find this line in `main.py` and modify the value:

```python
max_size_mb = 2.0  # Change to your desired MB value
```

### Change Image Directories

```python
photos_dir = Path("your_directory")  # Change to your image folder
output_dir = Path("output_directory")  # Change to your output folder
```

### Add More Image Formats

Find this line in `main.py` and add new formats:

```python
image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.new_format'}
```

---

## FAQ

### Q: The compressed image looks blurry?

A: This is normal. Lower quality means smaller file size but some quality loss. The project defaults to a 2MB limit and tries to maintain the highest quality within that constraint.

### Q: Are GIF animations supported?

A: Not currently. GIF requires special handling. Only static image formats are supported.

### Q: Will PNG images be converted to JPEG?

A: Yes, for better compression, PNG is converted to JPEG format (may lose transparency).

### Q: Why did the file size increase after compression?

A: This rarely happens. It could be the original image was already highly compressed. Try lowering `max_size_mb`.

---

## Tech Stack

- **Python 3.7+**
- **Pillow 10.0+** - Python image processing library

---

## License

MIT License - Feel free to use and modify
