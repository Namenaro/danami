import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as plt

if __name__ == "__main__":
    p = r'C:\Users\User\PycharmProjects\danami\dataset\data_om\omniglot-py\images_background\Alphabet_of_the_Magi\character01'
    p= os.path.join(p, "0709_01.png")

    img = cv.imread(p)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    sift = cv.SIFT_create()
    kp = sift.detect(gray, None)

    fig, axs = plt.subplots(figsize=(8, 8), dpi=60)
    cm = plt.get_cmap('seismic')
    axs.imshow(gray, cmap=cm, vmin=0, vmax=1)
    for curKey in kp:
        x = np.int(curKey.pt[0])
        y = np.int(curKey.pt[1])
        axs.scatter(x, y, s=200)
    plt.savefig("SIFT.png")






