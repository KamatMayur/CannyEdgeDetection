from scipy.ndimage import convolve
import numpy as np

PI = 180

class cannyEdgeDetector:
    def __init__(self, imgs, sigma=1, kernel_size=3, weak_pixel=75, strong_pixel=255, lowthreshold=20, highthreshold=40):
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
    

    def gaussian_kernel(self):
        size = int(self.kernel_size) // 2
        x, y = np.mgrid[-size:size+1, -size:size+1]
        normal = 1 / (2.0 * np.pi * self.sigma**2)
        g =  np.exp(-((x**2 + y**2) / (2.0*self.sigma**2))) * normal
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
        theta = np.arctan2(magy, magx)
        theta = np.rad2deg(theta) + 180
        return (mag, theta)
  
    
    def non_max_suppression(self, mag, grad):
        for i in range(1, mag.shape[0] - 1):
            for j in range(1, mag.shape[1] - 1):

                direction = grad[i, j]
        
                if (0 <= direction < PI / 8) or (15 * PI / 8 <= direction <= 2 * PI):
                    before_pixel = mag[i, j - 1]
                    after_pixel = mag[i, j + 1]
        
                elif (PI / 8 <= direction < 3 * PI / 8) or (9 * PI / 8 <= direction < 11 * PI / 8):
                    before_pixel = mag[i + 1, j - 1]
                    after_pixel = mag[i - 1, j + 1]
        
                elif (3 * PI / 8 <= direction < 5 * PI / 8) or (11 * PI / 8 <= direction < 13 * PI / 8):
                    before_pixel = mag[i - 1, j]
                    after_pixel = mag[i + 1, j]
        
                else:
                    before_pixel = mag[i - 1, j - 1]
                    after_pixel = mag[i + 1, j + 1]
                if mag[i, j] <= before_pixel or mag[i, j] <= after_pixel:
                    mag[i, j] = 0
     
        return  mag




    def threshold(self, image):
        
        output = np.zeros(image.shape).astype(np.uint8)
        strong_row, strong_col = np.where(image >= self.highThreshold)
        weak_row, weak_col = np.where((image <= self.highThreshold) & (image >= self.lowThreshold))
    
        output[strong_row, strong_col] = self.strong_pixel
        output[weak_row, weak_col] = self.weak_pixel
    
        return output

    def hysteresis(self, image):
        row, col = image.shape
        for i in range(row):
            for j in range(col):
                if i == 0 or j  == 0 or i == row-1 or j == col-1:
                    if image[i, j] == self.weak_pixel:
                        image[i][j] = 0
                       
                else:
                    if image[i, j] == self.weak_pixel:
                        if image[i, j + 1] == 255 or image[i, j - 1] == 255 or image[i - 1, j] == 255 or image[i + 1, j] == 255 or image[i - 1, j - 1] == 255 or image[i + 1, j - 1] == 255 or image[i - 1, j + 1] == 255 or image[i + 1, j + 1] == 255:
                            image[i, j] = 255
                        else:
                            image[i, j] = 0
                    
        return image

    def detect(self):
         
        self.img_smoothed = convolve(self.imgs, self.gaussian_kernel())
        self.gradientMat, self.thetaMat = self.sobel_gradient(self.img_smoothed)
        self.nonMaxImg = self.non_max_suppression(self.gradientMat, self.thetaMat)
        self.thresholdImg = self.threshold(self.nonMaxImg)
        self.img_final = self.hysteresis(self.thresholdImg)
        return self.img_final