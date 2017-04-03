#!flask/bin/python


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import PIL
from PIL import Image
import cv2
from lib.image_parser import parse_image
from elasticsearch import Elasticsearch
es=Elasticsearch("222.29.193.166:9200")

if __name__ == '__main__':


    vc = cv2.VideoCapture('/home/chenxinyuan/data/peason_search_attr/static/video/test_120_r1.mp4')

    index=1

    if vc.isOpened():
        rval , frame = vc.read()
    else:
        rval = False

    es.indices.delete(index='peason_video' )
    es.indices.create(index='peason_video', ignore=400)

    while rval:
        rval, frame = vc.read()
        if frame:
            pedestrian_attr=parse_image(frame)
            for peason in pedestrian_attr:
                peason['time']=index
                res = es.index(index="peason_video", doc_type='peason', body=peason)
                print peason
                print res
        index += 1
        # cv2.imwrite('result/'+str(index) + '.jpg',frame)
    ##app.run(host='0.0.0.0', port=8888)
