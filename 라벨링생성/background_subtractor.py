import cv2 
from config import *
import numpy as np 

class BackgroundSub():
    def __init__(self) -> None:
        self.fgbg = cv2.createBackgroundSubtractorKNN(detectShadows=False)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))

    def execute(self, frame):
        background_extraction_mask = self.fgbg.apply(frame)
        background_extraction_mask = cv2.morphologyEx(background_extraction_mask, cv2.MORPH_OPEN, self.kernel)
        background_extraction_mask = np.stack((background_extraction_mask,)*3, axis=-1)
        bitwise_image = cv2.bitwise_and(frame, background_extraction_mask)
        hsv_frame = cv2.cvtColor(bitwise_image, cv2.COLOR_BGR2HSV)
        vue_mean = np.mean(hsv_frame[:,:,2])
        return vue_mean