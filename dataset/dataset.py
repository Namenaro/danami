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
    def __init__(self, train_len=10, class_num=None):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(dir_path, './data_om')
        self.ominset = datasets.Omniglot(root=path, download=True, transform=None)
        self.train_len = train_len
        self.class_num = class_num

        self.class_pics = None
        if class_num is not None:
            self.class_pics = self.get_all_pics_for_class(class_num)

    def reset_class_num(self, new_class_num):
        self.class_num = new_class_num
        self.class_pics = self.get_all_pics_for_class(new_class_num)

    def get_etalon(self):
        return self.class_pics[0]

    def get_train(self):
        return self.class_pics[1:self.train_len]

    def get_test(self):
        return self.class_pics[self.train_len:]

    def get_contrast(self, sample_size):
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
