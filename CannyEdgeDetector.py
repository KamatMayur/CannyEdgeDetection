from cmath import inf
from scipy import ndimage
from scipy.ndimage import convolve

from scipy import misc
import numpy as np

class cannyEdgeDetector:
    def __init__(self, imgs, sigma=1, kernel_size=3, weak_pixel=75, strong_pixel=255, lowthreshold=0.05, highthreshold=0.15):
        self.imgs = imgs
        self.imgs_final = []
        self.img_smoothed = None
        self.gradientMat = None
        self.thetaMat = None
        self.nonMaxImg = None
        self.thresholdImg = None
        self.weak_pixel = weak_pixel
        self.strong_pixel = strong_pixel
        self.sigma = sigma
        self.kernel_size = kernel_size
        self.lowThreshold = lowthreshold
        self.highThreshold = highthreshold
        return 
    
    def gaussian_kernel(self, size, sigma=1):
        size = int(size) // 2
        x, y = np.mgrid[-size:size+1, -size:size+1]
        normal = 1 / (2.0 * np.pi * sigma**2)
        g =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
        return g
    
    def sobel_gradient(self, imgs):
        Sx = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
            ])
        Sy = np.array([
            [1, 2, 1], 
            [0, 0, 0], 
            [-1, -2, -1]
            ])

        img = np.asarray(imgs).astype(float)

        magx = convolve(img, Sx).astype(float)
        magy = convolve(img, Sy).astype(float)
        mag = (magx**2 + magy**2)**0.5
        mag *= (255/mag.max())
        mag = mag.astype(np.uint8)

        theta = np.empty(shape=mag.shape)
        theta = np.arctan(magy, magx)
        theta = np.array(theta)
        theta *= (255/theta.max())
        theta = theta.astype(np.uint8)
        print(type(theta))
        return theta

    
    def detect(self):
         
        self.img_smoothed = convolve(self.imgs, self.gaussian_kernel(self.kernel_size, self.sigma))
        self.gradientMat = self.sobel_gradient(self.img_smoothed)
        return self.gradientMat