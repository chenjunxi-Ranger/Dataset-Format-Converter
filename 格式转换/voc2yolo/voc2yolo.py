import os
import xml.etree.ElementTree as ET

CLASSES=[]#数据集类别名称
CLASS_TO_INDEX={cls:idx for idx,cls in enumerate(CLASSES)}
XML_dir=''#存放voc格式的目录
TXT_dir=''#存放转换后的yolo格式的目录

def convert_box(size,box):
    """
    :param size: (width,height)
    :param box: (xmin,ymin,xmax,ymax)
    :return: 归一化后的(x_center, y_center, w, h)
    """
    dw=1.0/size[0]
    dh=1.0/size[1]
    #中心坐标
    x_center=(box[0]+box[2])/2.0
    y_center=(box[1]+box[3])/2.0
    #宽高
    w=box[2]-box[0]
    h=box[3]-box[1]
    #归一化
    x_center=x_center*dw
    w=w*dw
    y_center=y_center*dh
    h=h*dh
    return (x_center,y_center,w,h)


def convert_annotation(xml_file_path,txt_file_path):
    """
    解析单个xml文件转换为txt文件
    """
    in_file=open(xml_file_path,mode='r',encoding='utf-8')
    out_file=open(txt_file_path,mode='w',encoding='utf-8')

    tree=ET.parse(in_file)
    root=tree.getroot()

    #读取图片的尺寸
    size=root.find('size')
    if size is None:
        print("缺少size")
        return

    #读取宽高
    w=int(size.find('width').text)
    h=int(size.find('height').text)
    if w==0 or h==0:
        print("找不到尺寸")
        return 

    #找所有object
    for obj in root.iter('object'):
        cls=obj.find('name').text

        if cls not in CLASSES:
            continue
        #获取标签
        label=CLASS_TO_INDEX[cls]
        #提取边界
        xmlbox=obj.find('bndbox')
        if xmlbox is None:
            print("没找到box")
            continue
        box=(float(xmlbox.find('xmin').text),float(xmlbox.find('ymin').text),
             float(xmlbox.find('xmax').text),float(xmlbox.find('ymax').text),)

        #转换后的格式
        txt_format=convert_box((w,h),box)
        out_file.write(str(label)+' '+" ".join([f"{a:.6f}" for a in txt_format]) + '\n')

    in_file.close()
    out_file.close()


if __name__ =='__main__':
    #没有txt文件则创建
    if not os.path.exists(TXT_dir):
        os.makedirs(TXT_dir)
    #获取所有xml文件
    xml_files=[]
    for f in os.listdir(XML_dir):
        if  f.endswith('.xml'):
            xml_files.append(f)

    for xml_name in xml_files:
        xml_path=os.path.join(XML_dir,xml_name)
        txt_name=xml_name.replace('.xml','.txt')
        txt_path=os.path.join(TXT_dir,txt_name)

        convert_annotation(xml_path,txt_path)