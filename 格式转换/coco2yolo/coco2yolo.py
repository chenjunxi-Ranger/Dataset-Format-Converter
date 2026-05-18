import os
import json
from collections import defaultdict

JSON_FILE_PATH='coco/train2017.json'
YOLO_TXT_DIR='yolo'

def get_yolo_format(size,bbox):
    """
    size(width,height),bbox[x_min,y_min,width,weight]
    """
    x_min,y_min,obj_width,obj_height=bbox[0],bbox[1],bbox[2],bbox[3]
    width=size[0]
    height=size[1]
    #转为yolo格式
    x_center=x_min+(obj_width/2.0)
    y_center=y_min+(obj_height/2.0)

    return x_center/width,y_center/height,obj_width/width,obj_height/height

if __name__ =='__main__':
    if not os.path.exists(YOLO_TXT_DIR):
        os.makedirs(YOLO_TXT_DIR)

    with open(JSON_FILE_PATH,'r',encoding='utf-8') as f:
        coco_data=json.load(f)

    #COCO 的 ID 可能是 1,2,3... 甚至不连续，YOLO 必须是 0,1,2...，构建ID映射表
    coco_id_to_yolo_id={}
    yolo_idx_to_name={}
    for idx,category in enumerate(coco_data['categories']):
        coco_id=category['id']
        category_name=category['name']

        coco_id_to_yolo_id[coco_id]=idx
        yolo_idx_to_name[idx]=category_name

    #image_id->image_infor
    image_id_to_image={}
    for image in coco_data['images']:
        image_id_to_image[image['id']]=image

    #将annotation按image_id分组
    image_id_to_annotation=defaultdict(list)
    for annotation in coco_data['annotations']:
        image_id_to_annotation[annotation['image_id']].append(annotation)

    #遍历image_id
    for image_id,image_info in image_id_to_image.items():
        file_name=image_info['file_name']
        width=image_info['width']
        height=image_info['height']

        if width==0 or height==0:
            print("宽高为0")
            continue

        txt_name=os.path.splitext(file_name)[0]+'.txt'
        txt_path=os.path.join(YOLO_TXT_DIR,txt_name)

        annotation=image_id_to_annotation[image_id]

        with open(txt_path,'w',encoding='utf-8') as txt_file:
            for ann in annotation:
                if ann.get('iscrowd', 0) == 1:
                    continue
                #转为yolo_id
                coco_category_id=ann['category_id']
                yolo_id=coco_id_to_yolo_id[coco_category_id]
                #bbox[x_min,y_min,width,weight]
                bbox=ann['bbox']
                x_center,y_center,nor_w,nor_h=get_yolo_format((width,height),bbox)

                txt_line=f"{yolo_id} {x_center:.6f} {y_center:.6f} {nor_w:.6f} {nor_h:.6f}\n"
                txt_file.write(txt_line)
