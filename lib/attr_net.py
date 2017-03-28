

caffe_path ="/data/my_rap_network/caffe/python/"
# caffe_path ="/data/py-faster-rcnn/lib/roi_data_layer"
model_path ="/data/my_rap_network/lib"

import sys
sys.path.append(model_path)
sys.path.append(caffe_path)

import caffe as attr_caffe
from wpal_net.recog import recognize_attr
from utils.rap_db import RAP
import numpy as np



par_set_id=0
db_path="/data/RAP"
db = RAP(db_path, par_set_id)
# img_path=db.get_img_path(1)
threshold = np.ones(db.num_attr) * 0.5

def get_attr_net(start=0,end=3):
    net_dir="/data/my_rap_network"
    caffemodel=net_dir+"/data/snapshots/VGG_S_MLL_RAP/0/"+"attr{0}_{1}".format(start,end)+"/RAP/vgg_s_mll_rap_iter_100.caffemodel"
    prototxt=net_dir+"/models/VGG_S_MLL_RAP/train_net_dir/"+""+"test_net_{0}_{1}.prototxt".format(start,end)

    attr_net = caffe_attr.Net(prototxt, caffemodel, caffe_attr.TEST)
    attr_net.name = "rap_test"
    return attr_net


#
def get_all_nets(items):
    all_nets={}
    for attr in attrs:
        start=attr[0]
        end=attr[1]
        all_nets[start]=get_attr_net(start,end)
    return all_nets

# get_attr_net()

#import cv2
