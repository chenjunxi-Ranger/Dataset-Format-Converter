# VOC 转 YOLO 格式转换工具 (Python)

这是一个用于目标检测数据集格式转换的轻量级 Python 脚本，将 PASCAL VOC 格式的 .xml 标注文件批量转换为 YOLO 格式的 .txt 标注文件（归一化坐标）。

## 使用前必读

运行前请先修改 `voc2yolo.py` 中的 3 个配置项：

### 1. 配置类别 (CLASSES)
```python
CLASSES = []  # 修改为你的数据集中的类别名称
```
- 严格匹配大小写！
- 顺序很重要，第一个类是索引 0，第二个是 1，依此类推
- 示例：`CLASSES = ["ship"]` 或 `CLASSES = ["airplane", "ship", "storage tank"]`

### 2. 配置输入路径 (XML_dir)
```python
XML_dir = ''  # 存放 VOC 格式 .xml 文件的目录
```
- 示例：`XML_dir = 'Annotations'` 或绝对路径
- 目录树结构：
  ```
  XML_dir/
  ├── 000001.xml
  ├── 000002.xml
  ├── 000003.xml
  └── ...
  ```
  所有 .xml 文件直接放在 XML_dir 目录下，不包含子目录

### 3. 配置输出路径 (TXT_dir)
```python
TXT_dir = ''  # 存放转换后 YOLO 格式 .txt 文件的目录
```
- 示例：`TXT_dir = 'Yolo_Labels'`，脚本会自动创建该文件夹

## 运行方法

确保已安装 Python 3.6+，在脚本所在目录下运行：

```bash
python voc2yolo.py
```

运行结束后，去 `TXT_dir` 目录查看生成的 .txt 文件。
