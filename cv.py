import cv2, numpy as np
from utils import *
import matplotlib.pylab as plt
import os
import uiautomator2 as u2
import time

plt.figure(figsize=(2, 3))
plt.axis('off')


def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img


class UIMatcher:
    def __init__(self):
        self.show = 0

    def show_pic(self):
        self.show = 1

    @staticmethod
    def test_weight(screen, template, crop=0):

        _screen = cv_imread(screen)
        if crop:
            print(crop, _screen.shape)
            _screen = _screen[crop[0]:crop[1], crop[2]:crop[3]]
            cv2.imshow('1', _screen)
            cv2.waitKey(0)
        _template = cv_imread(template)
        res = cv2.matchTemplate(_screen, _template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print(min_val, max_val, min_loc, max_loc)

    @staticmethod
    def RotateClockWise90(img):
        trans_img = cv2.transpose(img)
        new_img = cv2.flip(trans_img, 0)
        return new_img

    @staticmethod
    def findpic(screen, template_paths=['img/battle.jpg'], crop=0):
        if screen.shape[0] > screen.shape[1]:
            screen = UIMatcher.RotateClockWise90(screen)
        screen_show = screen.copy()
        if crop:
            screen = screen[crop[0]:crop[1], crop[2]:crop[3]]
        centeral = []
        max_vals = []

        for template_path in template_paths:
            template = cv_imread(template_path)
            h, w = template.shape[:2]  # rows->h, cols->w
            res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            x = (max_loc[0] + w // 2) / screen.shape[1]
            y = (max_loc[1] + h // 2) / screen.shape[0]
            centeral.append([x, y])
            max_vals.append(max_val)
            if max_val > 0.8:
                cv2.rectangle(screen_show, (int(max_loc[0]), int(max_loc[1])),
                              (int(max_loc[0] + w), int(max_loc[1] + h)), (0, 0, 255), 2)
                cv2.putText(screen_show, str(round(max_val, 3)) + os.path.basename(template_path),
                            (int(max_loc[0]), int(max_loc[1]) - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
        plt.cla()
        img4 = cv2.cvtColor(screen_show, cv2.COLOR_BGR2RGB)
        img4 = np.rot90(img4, -1)
        plt.imshow(img4)
        plt.pause(0.01)
        return centeral, max_vals

    @staticmethod
    def find_highlighted(screen):

        if screen.shape[0] > screen.shape[1]:
            screen = UIMatcher.RotateClockWise90(screen)
        gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        ret, binary = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
        index_1 = np.mean(np.argwhere(binary[63:, :] == 255), axis=0).astype(int)

        screen = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
        cv2.circle(screen, (index_1[1], index_1[0] + 63), 10, (255, 0, 0), -1)

        plt.cla()
        plt.imshow(screen)
        plt.pause(0.01)
        print(len(np.argwhere(binary == 255)), len(np.argwhere(binary == 0)))
        return index_1[1] / screen.shape[1], (index_1[0] + 63) / screen.shape[0]


if __name__ == "__main__":

    crops = [200, 540, 890, 1020]
    for i in range(4):
        crops[i] = int(crops[i] // 1.333)
    UIMatcher.test_weight('img/start.jpg', 'img/ready.jpg', crop=crops)

