#orz


from lib.attr_net import db,threshold, get_attr_net,recognize_attr,get_all_nets
from lib.obj_detetor import *
from lib.peason_layout import parse_layout

attr_net=get_attr_net()
# attrs=[[1,4],[4,7]]
# all_nets=get_all_nets(attrs)


def parse_image(image_key):
    org_img=get_pedestrian_image(image_key)
    pick=get_peason_bbox(org_img)
    pedestrian_attr=[]
    image_list=crop_pedestrian_image(org_img,pick)

    for img in image_list:
        img_info=parse_one_pedestrian(img)
        pedestrian_attr.append(img_info)
    return pedestrian_attr




def parse_one_pedestrian(img):
    img_info={}
    img_info['attr']={}
    attr, _, score, _ = recognize_attr(attr_net, img, db.attr_group, threshold)
    for i in range(len(attr)):
        img_info['attr'][db.attr_eng[i][0][0]]=attr[i]
        # if attr[i]>0 or "Female"in db.attr_eng[i][0][0]:
        #     img_info['attr'].append("{0}  ------ {1}:            \
        #      {2}\n".format(db.attr_eng[i][0][0],db.attr_ch[i][0][0].encode('utf-8'),attr[i]))
    img_info['layout']=parse_layout(img)
    return img_info

def get_all_attrs(img):
    attrs_info={}
    for attr in attrs:
        start=attr[0]
        attr_net=all_nets[start]
        attr, _, score, _ = recognize_attr(attr_net, img, db.attr_group, threshold)
        for i in range(len(attr)):
            attrs_info[db.attr_eng[i+start][0][0]]=attr[i]
    return attrs_info
