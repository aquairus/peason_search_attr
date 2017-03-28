caffe_path ="/data/py-faster-rcnn/caffe-fast-rcnn/python"
model_path ="/data/py-faster-rcnn/lib"

import sys
sys.path.append(model_path)
sys.path.append(caffe_path)



from fast_rcnn.config import cfg
import fast_rcnn.test
from fast_rcnn.nms_wrapper import nms


import numpy as np
import scipy.io as sio
import caffe, os, sys, cv2


CLASSES = ('__background__',
           'up', 'mid', 'leg',)

cfg.TEST.HAS_RPN = True
prototxt = '/data/py-faster-rcnn/models/pascal_voc/VGG_CNN_M_1024/faster_rcnn_end2end/test.prototxt'
caffemodel = '/data/py-faster-rcnn/output/faster_rcnn_end2end/voc_2007_trainval/vgg_cnn_m_1024_faster_rcnn_iter_70000.caffemodel'
caffe.set_device(0)
cfg.GPU_ID = 0
net = caffe.Net(prototxt, caffemodel, caffe.TEST)

def vis_detections(im, class_name, dets, thresh=0.5):

    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return []
    return inds



def parse_layout(im):

    scores, boxes = fast_rcnn.test.im_detect(net, im)

    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    CONF_THRESH = 0.8
    NMS_THRESH = 0.3
    results={}
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        bbox=vis_detections(im, cls, dets, thresh=CONF_THRESH)
        results[cls]=bbox
    return results





# print '\n\nLoaded network {:s}'.format(caffemodel)
# im_names = 'data/VOCdevkit2007/VOC2007/JPEGImages/422.png'


# demo(net, im_names)





# def vis_detections(im, class_name, dets, thresh=0.5):
#     """Draw detected bounding boxes."""
#     inds = np.where(dets[:, -1] >= thresh)[0]
#     if len(inds) == 0:
#         return
#
#     im = im[:, :, (2, 1, 0)]
#     fig, ax = plt.subplots(figsize=(12, 12))
#     ax.imshow(im, aspect='equal')
#     for i in inds:
#         bbox = dets[i, :4]
#         score = dets[i, -1]
#
#         ax.add_patch(
#             plt.Rectangle((bbox[0], bbox[1]),
#                           bbox[2] - bbox[0],
#                           bbox[3] - bbox[1], fill=False,
#                           edgecolor='red', linewidth=3.5)
#             )
#         ax.text(bbox[0], bbox[1] - 2,
#                 '{:s} {:.3f}'.format(class_name, score),
#                 bbox=dict(facecolor='blue', alpha=0.5),
#                 fontsize=14, color='white')
#
#     ax.set_title(('{} detections with '
#                   'p({} | box) >= {:.1f}').format(class_name, class_name,
#                                                   thresh),
#                   fontsize=14)
#     plt.axis('off')
#     plt.tight_layout()
#     plt.draw()
