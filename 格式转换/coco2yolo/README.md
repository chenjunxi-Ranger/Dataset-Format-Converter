# COCO 转 YOLO 格式转换工具 (Python)

这是一个用于目标检测数据集格式转换的轻量级 Python 脚本，将 COCO 格式的 .json 标注文件转换为 YOLO 格式的 .txt 标注文件（归一化坐标）。

## 使用前必读

运行前请先修改 `coco2yolo.py` 中的 2 个配置项：

### 1. 配置输入路径 (JSON_FILE_PATH)
```python
JSON_FILE_PATH = 'coco/train2017.json'  # COCO 格式 JSON 文件路径
```
- 支持相对路径和绝对路径
- JSON 文件需符合标准 COCO 格式

### 2. 配置输出路径 (YOLO_TXT_DIR)
```python
YOLO_TXT_DIR = 'yolo'  # 存放转换后 YOLO 格式 .txt 文件的目录
```
- 脚本会自动创建该文件夹
- 输出的 .txt 文件与对应图片同名（仅扩展名不同）

## 运行方法

确保已安装 Python 3.6+，在脚本所在目录下运行：

```bash
python coco2yolo.py
```

运行结束后，去 `YOLO_TXT_DIR` 目录查看生成的 .txt 文件。

## COCO 格式输入说明

脚本支持标准 COCO JSON 格式，需包含以下字段：

| 字段 | 说明 |
|------|------|
| `images` | 图像信息列表 |
| `annotations` | 标注框信息列表 |
| `categories` | 类别定义列表 |

### images 字段结构
```json
{
    "id": 1,
    "file_name": "image.jpg",
    "width": 1920,
    "height": 1080
}
```

### annotations 字段结构
```json
{
    "id": 1,
    "image_id": 1,
    "category_id": 1,
    "bbox": [x_min, y_min, width, height],
    "iscrowd": 0
}
```

### categories 字段结构
```json
{
    "id": 1,
    "name": "category_name",
    "supercategory": "none"
}
```

## YOLO 格式输出说明

转换后的每个 .txt 文件包含多行标注，每行格式如下：

```
<类别ID> <x_center> <y_center> <width> <height>
```

- **类别 ID**: 从 0 开始的连续整数（自动从 COCO ID 映射）
- **坐标**: 归一化到 0-1 范围的浮点数
- **坐标表示**: `[x_center, y_center, width, height]`

示例输出：
```
0 0.500000 0.500000 0.200000 0.300000
1 0.700000 0.300000 0.150000 0.250000
```

## 依赖项

```bash
pip install json  # Python 标准库，无需额外安装
pip install collections  # Python 标准库，无需额外安装
```
