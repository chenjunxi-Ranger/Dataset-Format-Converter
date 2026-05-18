import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from PIL import Image

# ================= 必须修改的配置 =================
CLASSES = ['ship', 'airplane']  # 必须与 YOLO 训练时的 classes 顺序严格一致
IMG_DIR = 'images'  # 存放原始图片的文件夹（必须有，为了读尺寸）
TXT_DIR = 'labels'  # 存放 YOLO 格式 txt 的文件夹
XML_DIR = 'Annotations_Output'  # 转换后 XML 的输出文件夹


# ==================================================

def create_xml(img_name, img_w, img_h, bboxes):
    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = 'VOC'
    ET.SubElement(annotation, 'filename').text = img_name

    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(img_w)
    ET.SubElement(size, 'height').text = str(img_h)
    ET.SubElement(size, 'depth').text = '3'

    for bbox in bboxes:
        cls_id, x_norm, y_norm, w_norm, h_norm = bbox

        # --- 核心：YOLO 逆向还原为 VOC 坐标 ---
        x_center = x_norm * img_w
        y_center = y_norm * img_h
        w = w_norm * img_w
        h = h_norm * img_h

        xmin = int(round(x_center - w / 2))
        ymin = int(round(y_center - h / 2))
        xmax = int(round(x_center + w / 2))
        ymax = int(round(y_center + h / 2))

        # 安全越界裁剪
        xmin = max(0, xmin)
        ymin = max(0, ymin)
        xmax = min(img_w, xmax)
        ymax = min(img_h, ymax)

        obj = ET.SubElement(annotation, 'object')
        ET.SubElement(obj, 'name').text = CLASSES[int(cls_id)]
        ET.SubElement(obj, 'pose').text = 'Unspecified'  # 无中生有
        ET.SubElement(obj, 'truncated').text = '0'  # 无中生有
        ET.SubElement(obj, 'difficult').text = '0'  # 无中生有

        bndbox = ET.SubElement(obj, 'bndbox')
        ET.SubElement(bndbox, 'xmin').text = str(xmin)
        ET.SubElement(bndbox, 'ymin').text = str(ymin)
        ET.SubElement(bndbox, 'xmax').text = str(xmax)
        ET.SubElement(bndbox, 'ymax').text = str(ymax)

    return annotation


def main():
    os.makedirs(XML_DIR, exist_ok=True)
    img_files = [f for f in os.listdir(IMG_DIR) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    print(f"找到 {len(img_files)} 张图片，开始转换 VOC...")
    count = 0
    for img_name in img_files:
        img_path = os.path.join(IMG_DIR, img_name)
        txt_name = os.path.splitext(img_name)[0] + '.txt'
        txt_path = os.path.join(TXT_DIR, txt_name)

        # 1. 强制读取图片尺寸
        try:
            with Image.open(img_path) as img:
                img_w, img_h = img.size
        except Exception as e:
            print(f"读取图片 {img_name} 失败，跳过。")
            continue

        bboxes = []
        # 2. 如果存在 txt 文件，则读取 YOLO 坐标
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        bboxes.append([float(x) for x in parts[:5]])

        # 3. 生成并保存 XML
        xml_tree = create_xml(img_name, img_w, img_h, bboxes)
        save_path = os.path.join(XML_DIR, os.path.splitext(img_name)[0] + '.xml')

        xml_string = ET.tostring(xml_tree, encoding='utf-8')
        pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ", encoding='utf-8')
        with open(save_path, 'wb') as f:
            f.write(pretty_xml)

        count += 1

    print(f"成功生成 {count} 个 XML 文件！")


if __name__ == '__main__':
    main()