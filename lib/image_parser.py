import lib.attr_net
import lib.peason_layout
from lib.obj_detetor import *

attrs=[[0,1],[24,30],[63,79],[75,83],[83,92]]
# [1,4],[4,7]]
all_nets=lib.attr_net.get_all_nets(attrs)


def parse_image(image_key):
    org_img=get_pedestrian_image(image_key)
    pick=get_peason_bbox(org_img)
    pedestrian_attr=[]
    image_list=crop_pedestrian_image(org_img,pick)
    print len(image_list)
    for idx,img in enumerate(image_list):
        img_info=parse_one_pedestrian(img)
        img_info["position"]=list(pick[idx].astype(int))
        pedestrian_attr.append(img_info)
    draw_annotation(org_img,pedestrian_attr)

    return pedestrian_attr


def draw_annotation(img,pedestrian_attr):
    for idx,info in enumerate(pedestrian_attr):
        (xA, yA, xB, yB)=info["position"]
        cv2.rectangle(img, (xA, yA), (xB, yB), (0, 0, 255), 2)
        for part in ["up","mid","leg"]:
            if info['layout'][part]:
                (xC, yC, xD, yD)=info['layout'][part]
                cv2.rectangle(img, (xC+xA, yC+yA), (xD+xA, yD+yA), (0, 255, 0), 2)
        for idx,line in enumerate(info["attr"].items()):
            print line

            cv2.putText(img,str(line) , ( xA, idx*35+yA ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 255, 0, 0 ), 2 )

    cv2.imwrite('./data/result.jpg', img)
    # return 0

def parse_one_pedestrian(img):
    img_info={}
    img_info['attr']=get_all_attrs(img)
    # {}
    # attr, _, score, _ = recognize_attr(attr_net, img, db.attr_group, threshold)
    # for i in range(len(attr)):
        # img_info['attr'][db.attr_eng[i][0][0]]=attr[i]
        # if attr[i]>0 or "Female"in db.attr_eng[i][0][0]:
        #     img_info['attr'].append("{0}  ------ {1}:            \
        #      {2}\n".format(db.attr_eng[i][0][0],db.attr_ch[i][0][0].encode('utf-8'),attr[i]))
    img_info['layout']=lib.peason_layout.parse_layout(img)
    return img_info

def get_all_attrs(img):
    attrs_info={}
    for attr in attrs:
        start=attr[0]
        single_attr_net=all_nets[start]
        if attr[1]-attr[0]==1:
            attr, _, score, _ = lib.attr_net.recognize_attr(single_attr_net, img, lib.attr_net.db.attr_group, lib.attr_net.threshold)
            attrs_info[lib.attr_net.db.attr_eng[start][0][0]]=int(round(attr[0]))
        else:
            attr, _, score, _ = lib.attr_net.recognize_attr(single_attr_net, img, lib.attr_net.db.attr_group)
            print attr
            max_index=attr.argmax()
            #for i in range(len(attr)):
            attrs_info[lib.attr_net.db.attr_eng[max_index+start][0][0]]=1
            #int(round(attr[max_index]))
    return attrs_info
