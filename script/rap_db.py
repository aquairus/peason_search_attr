# mkdir Annotations
# mkdir -r ImageSets/Main
# mv RAP_dataset JPEGImages


#!/usr/bin/env python

# --------------------------------------------------------------------

import os.path as osp
import numpy as np
import scipy.io as sio

# import evaluate
# from wpal_net.config import cfg

class RAP:
    def __init__(self, db_path, par_set_id):
        self._db_path = db_path

        rap = sio.loadmat(osp.join(self._db_path, 'RAP_annotation', 'RAP_annotation.mat'))['RAP_annotation']

        self._partition = rap[0][0][0]
        self.labels = rap[0][0][1]
        self.attr_ch = rap[0][0][2]
        self.attr_eng = rap[0][0][3]
        self.num_attr = self.attr_eng.shape[0]
        self.position = rap[0][0][4]
        self._img_names = rap[0][0][5]
        self.attr_exp = rap[0][0][6]

        self.attr_group = [range(1, 4), range(4, 7), range(7, 9), range(9, 11), range(30, 36), ]

        self.flip_attr_pairs = [(54, 55)]

        self.expected_loc_centroids = np.ones(self.num_attr, dtype=int) * 2
        self.expected_loc_centroids[9:16] = 1
        self.expected_loc_centroids[35:43] = 1

        """In our model, labels should be all between 0 and 1.
        Some labels are set to 2 in the RAP database, usually meaning the label is unknown or unsure.
        We change it to 0.5 as a more reasonable value expression.
        """
        self.labels = np.array([[0.5 if x == 2 else x for x in line] for line in self.labels])

        self.test_ind = None
        self.train_ind = None
        self.label_weight = None
        self.set_partition_set_id(par_set_id)

    # def evaluate_mA(self, attr, inds):
    #     cut_attr = [x[0:cfg.TEST.MAX_NUM_ATTR] for x in attr]
    #     cut_gt = [x[0:cfg.TEST.MAX_NUM_ATTR] for x in self.labels[inds]]
    #     return evaluate.mA(cut_attr, cut_gt)

    # def evaluate_example_based(self, attr, inds):
    #     cut_attr = [x[0:cfg.TEST.MAX_NUM_ATTR] for x in attr]
    #     cut_gt = [x[0:cfg.TEST.MAX_NUM_ATTR] for x in self.labels[inds]]
    #     return evaluate.example_based(cut_attr, cut_gt)

    def set_partition_set_id(self, par_set_id):
        self.train_ind = self._partition[par_set_id][0][0][0][0][0] - 1
        self.test_ind = self._partition[par_set_id][0][0][0][1][0] - 1
        pos_cnt = sum(self.labels[self.train_ind])
        self.label_weight = pos_cnt / self.train_ind.size

    def get_img_path(self, img_id):
        return osp.join(self._db_path, 'JPEGImages', self._img_names[img_id][0][0])


if __name__ == '__main__':
    db_path="/Users/apple/desktop/RAP"
    db = RAP(db_path, 0)
    print db._partition.shape
    print db._partition[0][0][0][0][1].shape
    print db._partition[1][0][0][0][1].shape
    print "Labels:", db.labels.shape
    print db.train_ind.shape
    print 'Max training index: ', max(db.train_ind)
    print db.get_img_path(0)
    print db.num_attr
    print db.label_weight
    print db.attr_eng[0][0][0]
    print db.attr_eng[1][0][0]
