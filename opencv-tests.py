import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

fn = os.path.join(os.path.dirname(__file__), 'brooklyn.png')
img = cv2.imread(fn, 0)
# cv2.imshow('image', img)
# cv2.waitKey()
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()

