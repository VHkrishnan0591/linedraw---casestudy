import cv2
import numpy as np
from PIL import Image
class Watermarkadder:
    
    def __init__(self):
        pass
    def watermark_at_top_right(self, image):
        logo = cv2.imread("app\static\THD_logo.jpg")
        image = np.array(image)
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        logo = cv2.resize(logo, None, fx=0.75, fy=0.75, interpolation=cv2.INTER_AREA)
        h1, w1, _ = image.shape
        h2, w2, _ = logo.shape
        # Calculate the position to place the smaller image on the larger image
        x_offset = w1 - w2
        y_offset = 0
        roi = image[y_offset:y_offset+h2, x_offset:x_offset+w2]
        result = cv2.addWeighted(roi, 0.8, logo, 0.2, 0)
        image[y_offset:y_offset+h2, x_offset:x_offset+w2] = result
        image  = Image.fromarray(image)
        return image