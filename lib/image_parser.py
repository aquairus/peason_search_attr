#orz


from lib.attr_net import db,threshold, get_attr_net,recognize_attr
from lib.obj_detetor import *

attr_net=get_attr_net()


def parse_image(image_key):
    org_img=get_pedestrian_image(image_key)
    pick=get_peason_bbox(org_img)
    pedestrian_attr=[]
    image_list=crop_pedestrian_image(org_img,pick)

    for img in image_list:
        img_info=parse_one_pedestrian(img)
        pedestrian_attr.append(img_info)
    return pedestrian_attr

        # {}
        # img_info['attr']=[]
        # attr, _, score, _ = recognize_attr(attr_net, img, db.attr_group, threshold)
        # for i in range(len(attr)):
        #     if attr[i]>0 or "Female"in db.attr_eng[i][0][0]:
        #         img_info['attr'].append("{0}  ------ {1}:            \
        #          {2}\n".format(db.attr_eng[i][0][0],db.attr_ch[i][0][0].encode('utf-8'),attr[i]))
        #
    #     pedestrian_attr.append(img_info)
    #
    # return pedestrian_attr

def parse_one_pedestrian(img):
    img_info={}
    img_info['attr']=[]
    attr, _, score, _ = recognize_attr(attr_net, img, db.attr_group, threshold)
    for i in range(len(attr)):
        if attr[i]>0 or "Female"in db.attr_eng[i][0][0]:
            img_info['attr'].append("{0}  ------ {1}:            \
             {2}\n".format(db.attr_eng[i][0][0],db.attr_ch[i][0][0].encode('utf-8'),attr[i]))
    return img_info
