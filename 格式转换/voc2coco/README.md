# VOC 转 COCO 格式转换工具 (Python)

这是一个用于目标检测数据集格式转换的轻量级 Python 脚本，将 PASCAL VOC 格式的 .xml 标注文件批量转换为 COCO 格式的 .json 标注文件。

## 使用前必读

运行前请先修改 `voc2coco.py` 中的 3 个配置项：

### 1. 配置类别 (CLASSES)
```python
CLASSES = []  # 修改为你的数据集中的类别名称
```
- 严格匹配大小写！
- 顺序很重要，第一个类是索引 1，第二个是 2，依此类推（COCO 格式类别 ID 从 1 开始）
- 示例：`CLASSES = ["ship"]` 或 `CLASSES = ["airplane", "ship", "storage tank"]`

### 2. 配置输入路径 (VOC_DIR)
```python
VOC_DIR = 'Annotations'  # 存放 VOC 格式 .xml 文件的目录
```
- 示例：`VOC_DIR = 'Annotations'` 或绝对路径
- 目录树结构：
  ```
  VOC_DIR/
  ├── 000001.xml
  ├── 000002.xml
  ├── 000003.xml
  └── ...
  ```
  所有 .xml 文件直接放在 VOC_DIR 目录下，不包含子目录

### 3. 配置输出路径 (COCO_DIR)
```python
COCO_DIR = 'COCO'  # 存放转换后 COCO 格式文件的目录
```
- 脚本会自动创建该文件夹
- 输出文件固定为 `COCO_DIR/instances_train.json`

## 运行方法

确保已安装 Python 3.6+，在脚本所在目录下运行：

```bash
python voc2coco.py
```

运行结束后，去 `COCO_DIR` 目录查看生成的 `instances_train.json` 文件。

## COCO 格式输出说明

转换后的 JSON 文件包含以下结构：

| 字段 | 说明 |
|------|------|
| `info` | 数据集基本信息描述 |
| `licenses` | 许可证列表（空） |
| `images` | 所有图像的信息列表 |
| `annotations` | 所有标注框的信息列表 |
| `categories` | 所有类别的定义列表 |

### images 字段结构
每个图像包含：
- `id`: 图像唯一 ID（从 1 开始递增）
- `file_name`: 文件名
- `width`: 图像宽度
- `height`: 图像高度

### annotations 字段结构
每个标注框包含：
- `id`: 标注框唯一 ID（从 1 开始递增）
- `image_id`: 对应的图像 ID
- `category_id`: 类别 ID（与 categories 中的 id 对应）
- `bbox`: 边界框坐标 `[x_min, y_min, width, height]`
- `area`: 边界框面积
- `iscrowd`: 是否为密集遮挡对象（从 VOC 的 difficult 字段转换）

### categories 字段结构
每个类别包含：
- `id`: 类别 ID（从 1 开始）
- `name`: 类别名称
- `supercategory`: 父类别（固定为 "none"）

## VOC 标注格式说明

脚本支持标准 VOC XML 格式，示例：

```xml
<annotation>
    <filename>000001.jpg</filename>
    <size>
        <width>1920</width>
        <height>1080</height>
    </size>
    <object>
        <name>airplane</name>
        <bndbox>
            <xmin>100</xmin>
            <ymin>200</ymin>
            <xmax>300</xmax>
            <ymax>400</ymax>
        </bndbox>
        <difficult>0</difficult>
    </object>
</annotation>
```

## 注意事项

1. **文件命名**：脚本会自动从 XML 中提取 `filename` 节点作为图片文件名；若 XML 中无 `filename` 节点，则自动使用与 XML 同名的 `.jpg` 文件

2. **宽高检查**：脚本会自动跳过 `width` 或 `height` 为 0 的图像

3. **bbox 检查**：脚本会自动跳过没有 `bndbox` 节点的标注

4. **类别过滤**：只处理 `CLASSES` 中定义的类别，其他类别会被自动忽略

5. **difficult 字段**：`iscrowd` 值从 VOC 的 `difficult` 字段转换而来（0 或 1）

6. **编码格式**：XML 文件使用 UTF-8 编码读取




