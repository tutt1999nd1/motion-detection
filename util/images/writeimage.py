import cv2
import os

class WriteImage:
    def __init__(self, file, frame):
        self.file = file
        self.frame = frame

    def write_image(self):
        status = cv2.imwrite('images/' + str(self.file) + '.jpg', self.frame)
        print(status)
