import cv2
import numpy as np


class_idx = 0
sample_idx = 0


# For taking sample points from image
class UiImage():
    def __init__(self, ui_name='image', param={}):
        self.ui_name = ui_name
        cv2.namedWindow(self.ui_name)
        cv2.setMouseCallback(self.ui_name, lambda *args:self.on_mouse(*args), param)

    def __call__(self, img, flags=cv2.IMREAD_UNCHANGED):
        if isinstance(img, str):
            img = cv2.imread(img,flags)

        self.img = img
        cv2.imshow(self.ui_name, img)

    def wait(self, delay=0):
        cv2.waitKey(delay) #ms
        if cv2.getWindowProperty(self.ui_name, cv2.WND_PROP_VISIBLE):
            cv2.destroyWindow(self.ui_name)

    def on_mouse(self, event, x, y, flags, param):
        pass


ui = UiImage(ui_name='image')

# 5 classes, 10 samples. Each sample is [x, y]
position = np.zeros((5,10,2),dtype=np.int32)

def on_mouse(event, x, y, flags, param):
    global class_idx, sample_idx

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Class {class_idx} sample {sample_idx}', x, y)
        position[class_idx][sample_idx][0] = x
        position[class_idx][sample_idx][1] = y

        sample_idx += 1
        if sample_idx >= 10:
            sample_idx = 0
            class_idx += 1
            if class_idx >= 5:
                print('Done')
                np.save('position.npy', position)
                exit()


ui.on_mouse = on_mouse
img = 'irabu_zhang1.bmp'
ui(img, flags=cv2.IMREAD_UNCHANGED)

ui.wait(delay=0)