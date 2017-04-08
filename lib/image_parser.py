import lib.attr_net
import lib.peason_layout
from lib.obj_detetor import *
from lib.es_query import check_peason
attrs=[[0,1],[24,30],[51,55],[63,75],[75,83],[83,92]]
# [1,4],[4,7]]
all_nets=lib.attr_net.get_all_nets(attrs)



def parse_frame(frame):
    org_img=get_pedestrian_frame(frame)
    pick=get_peason_bbox(org_img)
    pedestrian_attr=[]
    image_list=crop_pedestrian_image(org_img,pick)
    #print len(image_list)
    for idx,img in enumerate(image_list):
        img_info=parse_one_pedestrian(img)
        img_info["position"]=list(pick[idx].astype(int))
        if check_peason(img_info):
            pedestrian_attr.append(img_info)
            #print img_info
    #draw_annotation(org_img,pedestrian_attr)
    draw_im=draw_annotation(org_img,pedestrian_attr)
    return draw_im,pedestrian_attr

def parse_image(image_key):
    org_img=get_pedestrian_image(image_key)
    pick=get_peason_bbox(org_img)
    pedestrian_attr=[]
    image_list=crop_pedestrian_image(org_img,pick)
    #print len(image_list)
    for idx,img in enumerate(image_list):
        img_info=parse_one_pedestrian(img)
        img_info["position"]=list(pick[idx].astype(int))
        if check_peason(img_info):
            pedestrian_attr.append(img_info)

    draw_im=draw_annotation(org_img,pedestrian_attr)

    return draw_im,pedestrian_attr


def draw_annotation(img,pedestrian_attr):
    img = cv2.copyMakeBorder(img, 0, 300, 0, 0,cv2.BORDER_CONSTANT, value=(255, 255, 255))
    for idx,info in enumerate(pedestrian_attr):
        (xA, yA, xB, yB)=info["position"]
        cv2.rectangle(img, (xA, yA), (xB, yB), (0, 0, 255), 2)
        for part in ["up","mid","leg"]:
            if info['layout'][part]:
                (xC, yC, xD, yD)=info['layout'][part]
                cv2.rectangle(img, (xC+xA, yC+yA), (xD+xA, yD+yA), (0, 255, 0), 2)
        for idx,line in enumerate(info["attr"].items()):
            #print line

            cv2.putText(img,str(line) , ( xA, idx*25+yB+50 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 0 ), 1 )
    return img



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
            # print attr
            max_index=attr.argmax()
            #for i in range(len(attr)):
            attrs_info[lib.attr_net.db.attr_eng[max_index+start][0][0]]=1
            #int(round(attr[max_index]))
    return attrs_info
