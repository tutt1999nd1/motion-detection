import cv2


class WriteImage:
    def __init__(self, file, frame):
        self.file = file
        self.frame = frame

    def write_image(self):
        cv2.imwrite('images/' + str(self.file) + '.jpg', self.frame)