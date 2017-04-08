from __future__ import print_function
import cv2
# import matplotlib.pyplot as plt
import numpy as np
import sys
from imutils.object_detection import non_max_suppression
from imutils import paths
import imutils
from PIL import Image, ImageEnhance, ImageFilter
from dehaze_lib import *
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


imagePath="/Users/apple/desktop/2.jpg"

def get_peason_bbox(image):

    # (rects, weights) = hog.detectMultiScale(image,hitThreshold=0.6, winStride=(2,4),padding=(12, 12), scale=1.08)
    (rects, weights) = hog.detectMultiScale(image,hitThreshold=0.2,winStride=(4, 4),padding=(16, 16), scale=1.04)
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    print (weights)
    pick = non_max_suppression(rects, probs=weights, overlapThresh=0.6)
    print (pick)
    for p in pick:
        if p[0]<1:
            p[0]=1
        if p[1]<1:
            p[1]=1
    return pick


def pil_enhence(cv2_img):
    #m = deHaze(cv2_img/255.0)*255
    #cv2_img=deHaze(cv2_img/255.0)*255
    pil_img = Image.fromarray(cv2_img)
    im_enhance =ImageEnhance.Color(pil_img).enhance(1.1)
    #pil_img
    #.filter(ImageFilter.SHARPEN)
     #ImageEnhance.Color(pil_img).enhance(2)
    im_enhance=im_enhance.filter(ImageFilter.SHARPEN)
    result_img = np.array(im_enhance, dtype=np.uint8)

    return result_img

def get_pedestrian_image(image_key):
    image = cv2.imread(image_key)
    image=pil_enhence(image)
    scale=850.0/image.shape[1]

    image = imutils.resize(image, width=min(850, image.shape[1]))
    return   image

def get_pedestrian_frame(frame):
    image=pil_enhence(frame)
    scale=850.0/image.shape[1]
    print (image.shape)
    image = imutils.resize(image, width=min(850, image.shape[1]))
    print (image.shape)
    return   image

def draw_rectangle(image,pick):

    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
    return image

def crop_pedestrian_image(image,pick):
    img_list=[]
    for (xA, yA, xB, yB) in pick:
        new_img = image.copy()
        crop_img = new_img[ yA:yB,xA:xB]
        img_list.append(crop_img)
        # cv2.imshow("cropped", crop_img)
        # cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
    return img_list


if __name__ == '__main__':
    print ("hi")
