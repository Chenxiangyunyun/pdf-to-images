# PDF to Images PDF转高清图片工具

将 PDF 页面批量导出为高分辨率 PNG/JPG 图片。适合把 LaTeX、PPT、Canva 或其他排版工具导出的 PDF 转成图片素材。

> 说明：PDF 转成图片后，文字会变成像素图，不能像矢量 PDF 一样无限放大。因此建议先保证 PDF 本身排版清晰，再使用较高 DPI 导出。

## 项目结构

```text
pdf-to-images/
├── data/
│   └── PDF_example.pdf        # 示例 PDF，脚本默认读取它
├── results/
│   ├── page_001.png           # 示例导出结果
│   ├── page_002.png
│   └── ...
├── pdf_to_images.py           # 主脚本
├── pyproject.toml             # 项目元数据与依赖配置
├── requirements.txt           # pip 依赖列表
├── LICENSE
└── README.md
```

## 功能

- 将 PDF 页面批量导出为 `png`、`jpg` 或 `jpeg`
- 支持自定义 DPI，默认 `600`
- 支持指定起止页码
- 支持设置 JPG/JPEG 图片质量
- 支持自定义输出目录和文件名前缀
- 输出目录不存在时会自动创建

## 环境要求

- Python 3.9+
- PyMuPDF
- Pillow

安装依赖：

```bash
pip install -r requirements.txt
```

也可以根据 `pyproject.toml` 安装项目依赖：

```bash
pip install .
```

## 快速开始

直接运行脚本会使用默认配置：

```bash
python pdf_to_images.py
```

默认行为：

- 输入 PDF：`./data/PDF_example.pdf`
- 输出目录：`./results`
- 输出格式：`png`
- 导出 DPI：`600`
- 文件名前缀：`page`

生成文件示例：

```text
results/page_001.png
results/page_002.png
results/page_003.png
```

## 常用命令

将指定 PDF 导出为 600 DPI 的 PNG：

```bash
python pdf_to_images.py data/PDF_example.pdf -o results --dpi 600
```

导出为 JPG，并设置图片质量：

```bash
python pdf_to_images.py data/PDF_example.pdf -o results --format jpg --quality 95
```

只导出第 1 页到第 3 页：

```bash
python pdf_to_images.py data/PDF_example.pdf -o results --start 1 --end 3
```

使用 900 DPI 导出更高清的图片：

```bash
python pdf_to_images.py data/PDF_example.pdf -o results --dpi 900
```

自定义输出文件名前缀：

```bash
python pdf_to_images.py data/PDF_example.pdf -o results --prefix slide
```

输出文件将类似：

```text
results/slide_001.png
results/slide_002.png
```

## 参数说明


| 参数           | 默认值                   | 说明                                      |
| -------------- | ------------------------ | ----------------------------------------- |
| `pdf`          | `./data/PDF_example.pdf` | 输入 PDF 文件路径，可省略                 |
| `-o, --output` | `results`                | 图片输出目录                              |
| `--dpi`        | `600`                    | 导出分辨率，数值越大越清晰，文件也越大    |
| `--format`     | `png`                    | 输出格式，支持`png`、`jpg`、`jpeg`        |
| `--quality`    | `95`                     | JPG/JPEG 质量，范围`1-100`，对 PNG 无影响 |
| `--start`      | `1`                      | 起始页码，从 1 开始                       |
| `--end`        | 最后一页                 | 结束页码，从 1 开始                       |
| `--prefix`     | `page`                   | 输出图片文件名前缀                        |

## DPI 建议


| 用途               | 推荐 DPI |
| ------------------ | -------: |
| 快速预览           |      300 |
| 常规高清导出       |      600 |
| 放大查看或精细排版 |      900 |
| 控制文件体积       |      450 |

## 注意事项

- DPI 越高，导出图片越清晰，但文件体积和处理时间也会增加。
- 如果原始 PDF 里的图片本身分辨率较低，提高 DPI 只能改善渲染尺寸，不能真正恢复丢失的细节。
- 脚本导出图片时使用白色背景，避免透明背景在部分平台显示异常。
- `.gitignore` 当前会忽略 `*.pdf`，如果要提交新的示例 PDF，需要调整忽略规则或使用强制添加。

## 许可证

MIT License
