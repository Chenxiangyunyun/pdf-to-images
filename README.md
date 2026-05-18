# PDF to Images 高清切图工具

把 PDF 按指定 DPI 批量导出为 PNG/JPG 图片，适合把 LaTeX/PPT/Canva 导出的 PDF 转成小红书图文素材。

> 重点：PDF 转成图片后，文字不再是矢量，不能无限放大自动变清晰。  
> 正确做法是：先保证 PDF 是矢量排版，再用 600/900 DPI 高分辨率导出图片。

## 功能

- 支持 PDF 批量转 PNG / JPG
- 支持设置 DPI，例如 300、600、900
- 支持指定页码范围
- 支持 JPEG 质量设置
- 自动创建输出文件夹
- 适合小红书图文、学习资料切图、课程笔记发布

## 安装

建议使用 Python 3.9+。

```bash
pip install -r requirements.txt
```

## 基本用法

把 `input.pdf` 转成 600 DPI 的 PNG：

```bash
python pdf_to_images.py input.pdf -o output_images --dpi 600
```

导出 JPG：

```bash
python pdf_to_images.py input.pdf -o output_images --dpi 600 --format jpg --quality 95
```

只导出第 1 到第 3 页：

```bash
python pdf_to_images.py input.pdf -o output_images --dpi 600 --start 1 --end 3
```

使用 900 DPI，适合放大查看：

```bash
python pdf_to_images.py input.pdf -o output_images --dpi 900
```

## 推荐参数

| 用途 | 推荐 DPI |
|---|---:|
| 普通预览 | 300 |
| 小红书图文 | 600 |
| 放大查看更清晰 | 900 |
| 文件太大时折中 | 450 |

## 小红书建议

如果是专门发小红书，建议最终图片至少：

```text
2160 × 2880 px
```

更清晰可以：

```text
3000 × 4000 px
```

如果你从 A4 PDF 直接切图，600 DPI 通常已经够清晰，但图片文件会比较大。

## 原理说明

PDF 中的文字通常是矢量的，放大后依然清晰。

但一旦转成 PNG/JPG，文字就变成像素图。  
因此，切图时必须用高 DPI 渲染：

```text
高质量 PDF
    ↓
600/900 DPI 渲染
    ↓
高清 PNG/JPG
```

不要用截图代替导出。

## GitHub 上传命令

如果你已经在 GitHub 新建了仓库，例如：

```text
https://github.com/你的用户名/pdf-to-images.git
```

可以在本文件夹执行：

```bash
git init
git add .
git commit -m "Add PDF to images converter"
git branch -M main
git remote add origin https://github.com/你的用户名/pdf-to-images.git
git push -u origin main
```

## 许可证

MIT License
