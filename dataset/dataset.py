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
    def __init__(self, contast_sample_len, train_len=10, class_num=None):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(dir_path, './data_om')
        self.ominset = datasets.Omniglot(root=path, download=True, transform=None)
        self.train_len = train_len
        self.class_num = class_num

        self.class_pics = None
        self.contrast_cogmaps = None
        self.contast_sample_len = contast_sample_len


    def reset_class_num(self, new_class_num):
        self.class_num = new_class_num
        self.class_pics = None
        self.contrast_cogmaps = None

    def get_etalon(self):
        if self.class_pics is None:
            self.class_pics = self.get_all_pics_for_class(self.class_num)
        return self.class_pics[0]

    def get_train(self):
        if self.class_pics is None:
            self.class_pics = self.get_all_pics_for_class(self.class_num)
        return self.class_pics[1:self.train_len]

    def get_test(self):
        if self.class_pics is None:
            self.class_pics = self.get_all_pics_for_class(self.class_num)
        return self.class_pics[self.train_len:]

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

    def get_contrast_cogmaps(self):
        if self.contrast_cogmaps is None:
            contrast_pics = self.get_contrast_pics(self.contast_sample_len)
            self.contrast_cogmaps=[]
            for pic in contrast_pics:
                self.contrast_cogmaps.append(Cogmap(pic))
        return self.contrast_cogmaps
