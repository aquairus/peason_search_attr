from __future__ import print_function
import cv2
# import matplotlib.pyplot as plt
import numpy as np
import sys
from imutils.object_detection import non_max_suppression
from imutils import paths


import imutils

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


imagePath="/Users/apple/desktop/2.jpg"

def get_peason_bbox(image):

    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
        padding=(8, 8), scale=1.05)

    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    for p in pick:
        if p[0]<1:
            p[0]=1
        if p[1]<1:
            p[1]=1
    return pick

def get_pedestrian_image(image_key):
    image = cv2.imread(image_key)
    scale=400.0/image.shape[1]
    image = imutils.resize(image, width=min(400, image.shape[1]))
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