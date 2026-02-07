# ZipPhoto - 图片批量压缩工具

> **English version**: [README.en.md](README.en.md)

一个简单易用的图片批量压缩工具，可以将图片压缩到指定大小以下。

## 功能特性

- 批量压缩：一次处理多张图片
- 大小控制：自动将图片压缩到 2MB 以下
- 格式支持：支持 JPG、PNG、BMP、WebP 等常见格式
- 保留原图：压缩后的图片保存到 `output/` 目录，不影响原始文件
- 详细统计：显示每张图片的压缩前后大小对比

## 快速开始

### 1. 环境准备

确保你安装了 Python 3.7 或更高版本。打开终端（命令行）：

```bash
# 检查 Python 版本
python --version
```

如果提示"找不到命令"，请先 [安装 Python](https://www.python.org/downloads/)。

### 2. 安装依赖

在项目根目录下运行：

```bash
pip install -r requirements.txt
```

这会安装本项目唯一的依赖：`Pillow`（一个强大的图片处理库）。

### 3. 添加要压缩的图片

将你的图片放入 `photos/` 目录。支持的文件格式：
- `.jpg` / `.jpeg`
- `.png`
- `.bmp`
- `.webp`

### 4. 运行程序

```bash
python main.py
```

### 5. 查看结果

压缩后的图片会保存在 `output/` 目录中，同时终端会显示压缩统计信息。

---

## 原理详解（新手友好）

### 什么是图片压缩？

想象一下，你在拍一张照片，相机保存了非常多的细节信息（比如每一片树叶的颜色、每一缕阳光的位置）。这使得照片非常大，有时候好几 MB。

**图片压缩**就是想办法在不明显降低画质的前提下，去掉一些"不必要"的信息，让文件变小。

### 本项目使用的压缩方法

本项目采用 **JPEG 有损压缩** 技术，核心原理如下：

#### 第 1 步：打开图片

```python
img = Image.open(image_path)
```

使用 Pillow 库读取图片文件，就像用图片查看器打开一张照片一样。

#### 第 2 步：颜色模式转换

```python
if img.mode in ('RGBA', 'P'):
    img = img.convert('RGB')
```

这一步是为了确保图片格式统一：
- `RGBA`：带透明通道的图片（常见于 PNG）
- `P`：调色板模式的图片
- `RGB`：标准颜色模式，JPEG 只支持这种格式

#### 第 3 步：逐级降低质量压缩

```python
for quality in range(95, 10, -5):
    img.save(output_path, 'JPEG', quality=quality, optimize=True)
    if output_path.stat().st_size <= max_size_mb * 1024 * 1024:
        break
```

这是压缩的核心逻辑：

1. **质量参数（95 → 10）**：从高质量开始尝试
2. **步长（-5）**：每次降低 5% 的质量
3. **优化选项（optimize=True）**：让 JPEG 编码器使用更高效的压缩算法
4. **自动停止**：一旦文件小于 2MB 就停止，降低不必要的画质损失

**为什么要循环尝试？**

因为不同图片的"最佳压缩率"不一样。有些图片内容简单，轻微压缩就能达标；有些图片细节丰富，需要压得更狠才能变小。循环尝试能找到每个图片的"临界点"。

---

## 代码结构

```
zipphoto/
├── main.py           # 主程序，所有逻辑都在这里
├── requirements.txt  # 项目依赖（Pillow）
├── photos/          # 存放要压缩的图片（你需要放这里）
└── output/          # 压缩后的图片输出目录（自动生成）
```

### 代码逐行解释

#### `get_file_size_str()` 函数

```python
def get_file_size_str(size_bytes: int) -> str:
    """获取人类可读的文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"
```

把字节数转换成人类容易理解的格式：
- `1024` 字节 = 1 KB
- `1024 KB` = 1 MB
- `1024 MB` = 1 GB

例如：`4346044` 字节 → `4.14 MB`

#### `compress_image()` 函数

```python
def compress_image(image_path: Path, output_dir: Path, max_size_mb: float = 2.0) -> tuple:
```

接收一张图片路径和输出目录，压缩后返回压缩信息。

#### `main()` 函数

程序入口，负责：
1. 检查 `photos/` 目录是否存在
2. 找出所有支持的图片文件
3. 逐个调用压缩函数
4. 汇总并显示统计结果

---

## 自定义配置

### 修改目标大小

在 `main.py` 中找到这行，修改数值：

```python
max_size_mb = 2.0  # 改成你想要的 MB 数
```

### 修改图片目录

```python
photos_dir = Path("你的目录名")  # 改成你的图片文件夹
output_dir = Path("输出目录名")   # 改成你想要的输出文件夹
```

### 添加更多图片格式

在 `main.py` 中找到这行，添加新格式：

```python
image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.新格式'}
```

---

## 常见问题

### Q: 压缩后图片变模糊了？
A: 这是正常现象，质量越低文件越小，但画质也会有所损失。项目已经默认了 2MB 的上限，在这个范围内会尽量保持较高质量。

### Q: 支持 GIF 动图吗？
A: 目前不支持。GIF 需要特殊的处理方式，暂时只支持静态图片格式。

### Q: PNG 图片会被转成 JPEG 吗？
A: 是的，为了更好的压缩效果，PNG 会被转成 JPEG 格式（可能会失去透明通道）。

### Q: 为什么压缩后文件反而变大了？
A: 这种情况极少发生，可能是原图片已经是高度压缩过的（JPEG 质量很低）。可以尝试调低 `max_size_mb` 的值。

---

## 技术栈

- **Python 3.7+**
- **Pillow 10.0+** - Python 图片处理库

---

## 许可证

MIT License - 随意使用和修改
