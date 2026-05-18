import os
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import defaultdict

JSON_FILE_PATH='coco/train2017.json'
XML_DIR='voc'

def create_xml_tree(image_info,annotations,category_dict):
    """
    为一张图片创建voc格式的xml树
    """
    #根节点
    annotation=ET.Element('annotation')
    #基础信息
    ET.SubElement(annotation,'folder').text=''
    ET.SubElement(annotation,'filename').text=str(image_info['file_name'])
    size=ET.SubElement(annotation,'size')
    ET.SubElement(size,'width').text=str(image_info['width'])
    ET.SubElement(size,'height').text=str(image_info['height'])
    ET.SubElement(size,'depth').text='3'

    #添加object
    for ann in annotations:
        category_id=ann['category_id']
        if category_id not in category_dict:
            continue
        #[xmin,ymin,width,height]->[xmin,ymin,xmax,ymax]
        bbox=ann['bbox']
        x_min=int(round(bbox[0]))
        y_min=int(round(bbox[1]))
        x_max=int(round(bbox[0]+bbox[2]))
        y_max=int(round(bbox[1]+bbox[3]))
        x_min=max(x_min,0)
        y_min=max(y_min,0)
        x_max=min(image_info['width'],x_max)
        y_max=min(image_info['height'],y_max)

        if x_min>=x_max or y_min>=y_max:
            continue

        #构建object节点
        obj=ET.SubElement(annotation,'object')
        ET.SubElement(obj,'name').text=category_dict[category_id]
        ET.SubElement(obj,'pose').text='Unspecified'
        ET.SubElement(obj,'truncated').text='0'
        ET.SubElement(obj,'difficult').text=str(ann.get('iscrowd',0))

        #bndbox节点
        bndbox=ET.SubElement(obj,'bndbox')
        ET.SubElement(bndbox,'xmin').text=str(x_min)
        ET.SubElement(bndbox,'ymin').text=str(y_min)
        ET.SubElement(bndbox,'xmax').text=str(x_max)
        ET.SubElement(bndbox,'ymax').text=str(y_max)

    return annotation

def save_xml(element,save_path):
    """
    将elementtree写入内存
    """
    xml_string=ET.tostring(element,encoding='utf-8')
    reparsed=minidom.parseString(xml_string)
    pretty_xml_str = reparsed.toprettyxml(indent="  ")

    with open(save_path,'w',encoding='utf-8') as f:
        f.write(pretty_xml_str)


if __name__ =='__main__':
    if not os.path.exists(XML_DIR):
        os.makedirs(XML_DIR)

    with open(JSON_FILE_PATH,'r',encoding='utf-8') as f:
        coco_data=json.load(f)

    #id->name
    category_id_to_name={}
    for cat in coco_data['categories']:
        category_id_to_name[cat['id']]=cat['name']
    #image_id->image_info
    image_id_to_image={}
    for img in coco_data['images']:
        image_id_to_image[img['id']]=img
    #image_id->annotation
    image_id_to_annotation=defaultdict(list)
    for ann in coco_data['annotations']:
        image_id_to_annotation[ann['image_id']].append(ann)

    for image_id,image_info in image_id_to_image.items():
        filename=image_info['file_name']
        annotations=image_id_to_annotation[image_id]
        xml_tree=create_xml_tree(image_info,annotations,category_id_to_name)
        xml_name=os.path.splitext(filename)[0]+'.xml'
        save_path=os.path.join(XML_DIR,xml_name)
        save_xml(xml_tree,save_path)