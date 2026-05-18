import os
import json
import xml.etree.ElementTree as ET

CLASSES=['other','A220','Boeing787','Boeing737','A320/321','ARJ21','A330']
CLASS_TO_LABEL={cls:idx+1 for idx,cls in enumerate(CLASSES)}
VOC_DIR='Annotations'
COCO_DIR='COCO'
COCO_DIR_PATH=os.path.join(COCO_DIR,'instances_train.json')

def generate_coco_format():
    """
    初始化coco格式的json结构
    """
    coco_format={
        "info":{"description": "Converted from VOC format"},
        "licenses":[],
        "images":[],#图像
        "annotations":[],#标注框
        "categories":[],#类别
    }
    for cls,idx in CLASS_TO_LABEL.items():
        coco_format["categories"].append({"supercategory": "none",
                                          "id":idx,
                                          "name":cls})
    return coco_format

def get_bndbox(xmlbox):
    """
    提取box边界框，转为coco格式[x_min,y_min,width,weight]
    """
    x_min=float(xmlbox.find('xmin').text)
    y_min=float(xmlbox.find('ymin').text)
    x_max=float(xmlbox.find('xmax').text)
    y_max=float(xmlbox.find('ymax').text)
    #宽高
    width=x_max-x_min
    height=y_max-y_min
    #面积
    area=width*height
    return [x_min,y_min,width,height],area

if __name__ =='__main__':
    if not os.path.exists(COCO_DIR):
        os.makedirs(COCO_DIR)

    coco_format=generate_coco_format()

    #image和annotation的id
    image_id=1
    annotation_id=1

    xml_files=[]
    for f in os.listdir(VOC_DIR):
        if not f.endswith('.xml'):
            continue
        xml_files.append(f)

    for xml_name in xml_files:
        xml_path=os.path.join(VOC_DIR,xml_name)

        infile=open(xml_path,mode='r',encoding='utf-8')
        tree=ET.parse(infile)
        root=tree.getroot()
        #图片信息
        filename_node = root.find('filename')
        if filename_node is not None and filename_node.text:
            file_name = filename_node.text
        else:
            file_name = xml_name.replace('.xml', '.jpg')
        size=root.find('size')
        if size is None:
            print("无size")
            continue

        width=int(size.find('width').text)
        height=int(size.find('height').text)
        if width==0 or height==0:
            print("宽高为0")
            continue

        image_info={
            "file_name":file_name,
            "height":height,
            "width":width,
            "id":image_id
        }
        coco_format["images"].append(image_info)
        #标注信息
        for obj in root.iter('object'):
            cls=obj.find('name').text
            if cls not in CLASSES:
                continue

            category_id=CLASS_TO_LABEL[cls]

            xml_box=obj.find('bndbox')
            if xml_box is None:
                print("没找到box")
                continue

            coco_box,area=get_bndbox(xml_box)
            difficult = obj.find('difficult')
            is_difficult = int(difficult.text) if difficult is not None else 0

            annotation_info={
                "id":annotation_id,
                "image_id":image_id,
                "category_id":category_id,
                "bbox":coco_box,
                "area":area,
                "iscrowd":is_difficult
            }
            coco_format["annotations"].append(annotation_info)
            annotation_id+=1
        image_id+=1
        infile.close()

    with open(COCO_DIR_PATH,'w',encoding='utf-8') as f:
        json.dump(coco_format,f,ensure_ascii=False,indent=4)


