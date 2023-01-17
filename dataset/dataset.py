from cogmap import Cogmap

import numpy as np
import random
import torchvision.datasets as datasets
import os

def binarise_img(pic):
    pic = np.array(pic)
    new_img = np.zeros(pic.shape)
    for x in range(pic.shape[1]):
        for y in range(pic.shape[0]):
            if pic[y, x] == 0:
                new_img[y, x] = 1
    return new_img


class Dataset:
    def __init__(self, contast_sample_len, train_len=10, contrast_test_len=50, class_num=None):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(dir_path, './data_om')
        self.ominset = datasets.Omniglot(root=path, download=True, transform=None)

        self.TRAIN_TRUE_LEN = train_len
        self.TRAIN_CONTRAST_LEN = contast_sample_len
        self.TEST_CONTRAST_LEN = contrast_test_len

        self.class_num = class_num

        self.contrast_cogmaps_test = None
        self.contrast_cogmaps_TRAIN = None
        self.true_cogmaps_test = None
        self.true_cogmaps_TRAIN = None

        self.etalon_cogmap = None

    # ------- интерфейс к датасету------------------
    def get_TRUE_test(self):
        return self.true_cogmaps_test

    def get_TRUE_train(self):
        return self.true_cogmaps_TRAIN

    def get_CONTRAST_test(self):
        return self.contrast_cogmaps_test

    def get_CONTRAST_train(self):
        return self.contrast_cogmaps_TRAIN



    def reset_class_num(self, new_class_num):
        self.class_num = new_class_num

        class_pics = self.get_all_pics_for_class(self.class_num)
        etalon_pic = class_pics[0]
        train_true_pics = class_pics[1:self.TRAIN_TRUE_LEN]
        test_true_pics = class_pics[self.TRAIN_TRUE_LEN:]

        contrast_train_pics = self.get_contrast_pics(sample_size=self.TRAIN_CONTRAST_LEN)
        contrast_test_pics = self.get_contrast_pics(sample_size=self.TRAIN_CONTRAST_LEN)

        self.contrast_cogmaps_test = self.get_cogmaps_for_pics(contrast_test_pics)
        self.contrast_cogmaps_TRAIN = self.get_cogmaps_for_pics(contrast_train_pics)
        self.true_cogmaps_test = self.get_cogmaps_for_pics(test_true_pics)
        self.true_cogmaps_TRAIN = self.get_cogmaps_for_pics(train_true_pics)

        self.etalon_cogmap = Cogmap(etalon_pic)

    # ------- служебное------------------
    def get_contrast_pics(self, sample_size):
        contrast = []
        while True:
            if len(contrast) == sample_size:
                break
            i = random.randint(0, len(self.ominset)-1)
            if self.class_num != self.ominset[i][1]:
                contrast.append(binarise_img(self.ominset[i][0]))
        return contrast

    def get_all_pics_for_class(self, class_num):
        class_pics = []
        for i in range(len(self.ominset)):
            if class_num == self.ominset[i][1]:
                class_pics.append(binarise_img(self.ominset[i][0]))
        return class_pics


    def get_cogmaps_for_pics(self, pics):
        cogmaps = []
        for pic in pics:
            cogmaps.append(Cogmap(pic))
        return cogmaps

