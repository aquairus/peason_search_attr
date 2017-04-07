#!flask/bin/python


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import PIL
from PIL import Image
import cv2
from lib.image_parser import parse_image,parse_frame
from lib.es_query import get_esquery,check_peason
from elasticsearch import Elasticsearch
es=Elasticsearch("222.29.193.166:9200")

if __name__ == '__main__':


    vc = cv2.VideoCapture('static/video/test_120_r1.mp4')

    idx=1

    if vc.isOpened():
        rval , frame = vc.read()
    else:
        rval = False

    try:
        es.indices.delete(index='peason_video' )
    except BaseException,e:
        print 'no index before'

    es.indices.create(index='peason_video', ignore=400)

    while rval:
        draw_im,pedestrian_attr=parse_frame(frame)
        for peason in pedestrian_attr:
            peason['time']=idx
            peason['tag']=''
            for k,v in peason['attr'].items():
                k=k.replace("-",'')
                peason[k]=v
                peason['tag']+=k+" "
            peason.pop("attr")
            if check_peason(peason):
                res = es.index(index="peason_video", doc_type='peason', body=peason)
                print res
        cv2.imwrite('static/img/'+str(idx) + '.jpg',draw_im)
        print idx
        idx += 1
        rval, frame = vc.read()
        # cv2.imwrite('result/'+str(index) + '.jpg',frame)
    ##app.run(host='0.0.0.0', port=8888)
