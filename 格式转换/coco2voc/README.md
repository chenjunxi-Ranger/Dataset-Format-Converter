# COCO 转 VOC 格式转换工具 (Python)

这是一个用于目标检测数据集格式转换的轻量级 Python 脚本，将 COCO 格式的 .json 标注文件批量转换为 PASCAL VOC 格式的 .xml 标注文件。

## 使用前必读

运行前请先修改 `coco2voc.py` 中的 2 个配置项：

### 1. 配置输入路径 (JSON_FILE_PATH)
```python
JSON_FILE_PATH = 'coco/train2017.json'  # COCO 格式 JSON 文件路径
```
- 支持相对路径和绝对路径
- JSON 文件需符合标准 COCO 格式

### 2. 配置输出路径 (XML_DIR)
```python
XML_DIR = 'voc'  # 存放转换后 VOC 格式 .xml 文件的目录
```
- 脚本会自动创建该文件夹
- 输出的 .xml 文件与对应图片同名（仅扩展名不同）

## 运行方法

确保已安装 Python 3.6+，在脚本所在目录下运行：

```bash
python coco2voc.py
```

运行结束后，去 `XML_DIR` 目录查看生成的 .xml 文件。

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

## VOC 格式输出说明

转换后的每个 .xml 文件结构如下：

```xml
<annotation>
    <folder></folder>
    <filename>image.jpg</filename>
    <size>
        <width>1920</width>
        <height>1080</height>
        <depth>3</depth>
    </size>
    <object>
        <name>category_name</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>100</xmin>
            <ymin>200</ymin>
            <xmax>300</xmax>
            <ymax>400</ymax>
        </bndbox>
    </object>
</annotation>
```


## 注意事项

1. **宽高检查**: 脚本假设图像宽高信息正确，建议确保 JSON 中的 `width` 和 `height` 字段有效

2. **iscrowd 转换**: COCO 的 `iscrowd` 字段会映射到 VOC 的 `difficult` 字段

3. **文件命名**: 输出 .xml 文件名与 JSON 中 `file_name` 字段对应（去除扩展名后加 `.xml`）

4. **编码格式**: JSON 文件使用 UTF-8 编码读取和写入

5. **坐标四舍五入**: 坐标值会四舍五入为整数

```bash
pip install xml.etree.ElementTree  # Python 标准库，无需额外安装
pip install xml.dom.minidom  # Python 标准库，无需额外安装
```
