import os
import json
from PIL import Image

# ================= 必须修改的配置 =================
CLASSES = ['ship', 'airplane']
IMG_DIR = 'images'
TXT_DIR = 'labels'
JSON_SAVE_PATH = 'coco_from_yolo.json'


# ==================================================

def main():
    coco_format = {
        "images": [],
        "annotations": [],
        "categories": [{"id": idx + 1, "name": cls, "supercategory": "none"} for idx, cls in enumerate(CLASSES)]
    }

    image_id = 1
    annotation_id = 1

    img_files = [f for f in os.listdir(IMG_DIR) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    print(f"找到 {len(img_files)} 张图片，开始转换为 COCO...")

    for img_name in img_files:
        img_path = os.path.join(IMG_DIR, img_name)
        txt_name = os.path.splitext(img_name)[0] + '.txt'
        txt_path = os.path.join(TXT_DIR, txt_name)

        # 1. 强制读取图片尺寸
        try:
            with Image.open(img_path) as img:
                img_w, img_h = img.size
        except Exception:
            continue

        # 2. 构建图片信息
        coco_format["images"].append({
            "file_name": img_name,
            "height": img_h,
            "width": img_w,
            "id": image_id
        })

        # 3. 读取对应的 txt 标签
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 5: continue

                    cls_id = int(parts[0])
                    x_norm, y_norm, w_norm, h_norm = map(float, parts[1:5])

                    # --- 核心：YOLO 逆向还原为 COCO 坐标 ---
                    w_abs = w_norm * img_w
                    h_abs = h_norm * img_h
                    x_center = x_norm * img_w
                    y_center = y_norm * img_h

                    # COCO 需要的是 [左上角x, 左上角y, 宽, 高]
                    x_top_left = x_center - (w_abs / 2.0)
                    y_top_left = y_center - (h_abs / 2.0)

                    # 无中生有计算面积
                    area = w_abs * h_abs

                    coco_format["annotations"].append({
                        "id": annotation_id,
                        "image_id": image_id,
                        "category_id": cls_id + 1,  # YOLO是从0开始，COCO通常从1开始
                        "bbox": [x_top_left, y_top_left, w_abs, h_abs],
                        "area": area,
                        "iscrowd": 0  # 无中生有
                    })
                    annotation_id += 1

        image_id += 1

    # 4. 写入 JSON
    with open(JSON_SAVE_PATH, 'w', encoding='utf-8') as f:
        json.dump(coco_format, f, ensure_ascii=False, indent=4)

    print(f"成功打包为 COCO 格式！路径: {JSON_SAVE_PATH}")


if __name__ == '__main__':
    main()