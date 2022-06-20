import uiautomator2 as u2
import time
import random
from cv import *
import cv2
import numpy as np
from PIL import Image
import os
from assets import _mark_path, _mark, all_mark_piece, search_mark, _coordinates

app_name = "com.bilibili.snake"
emulator_port = 11509
adb_connect_link = f'adb connect 127.0.0.1:{emulator_port}'
Height = 1280
Width = 800
# 点击坐标随机偏移值
random_click = 0


class B_Automator:
    def __init__(self):
        self.app_name = app_name
        self.d = None
        self.dWidth = Width
        self.dHeight = Height

    def start(self):
        try:
            connect_result = os.popen("adb devices").read()
            while True:
                if '无法连接' in connect_result:
                    os.popen(adb_connect_link)
                    print('连接失败，正在重新建立连接')
                    time.sleep(2)
                else:
                    break
            self.d = u2.connect_usb()
            print(self.d)
        except Exception as e:
            print('链接错误', e)

        print()
        self.appRunning = False
        os.system('python -m uiautomator2 init')  # 必须
        print('正在拉起应用.', end='')
        while True:
            # 判断进程是否在前台, 最多等待20秒，否则唤醒到前台
            if self.d.app_wait(self.app_name, front=True, timeout=1):
                if not self.appRunning:
                    time.sleep(1)
                    print(',', end='')
                self.appRunning = True
                return True
            else:
                self.app = self.d.session(self.app_name)
                self.appRunning = False
                continue

    def is_there_img(self, screen=0, img='battle', threshold=0.8, crop=0, debug=False):
        if type(screen) == int:  # it means get all stats from image name
            screen = self.realtime_screenshot()
        if not img.endswith('.jpg'):
            img = _mark_path.format(img)

        active_path = self.get_butt_stat(screen, [img], threshold, crop)
        if img in active_path:
            if debug:
                print(debug, active_path, end='\n')
            return active_path[img]
        else:
            return False

    def test_thershold(self, screen_shot, template_paths, threshold=0.8):
        screen_shot = np.array(Image.open(f'{screen_shot}'))
        zhongxings, max_vals = UIMatcher.findpic(screen_shot, template_paths=template_paths)
        print(f"{name[3:-4]}-{round(max_vals[i], 3):.4f}{zhongxings}", end=' ')

    def get_butt_stat(self, screen_shot, template_paths, threshold=0.8, crop=0):
        # 此函数输入要判断的图片path,屏幕截图, 阈值,   返回大于阈值的path,坐标字典,
        return_dic = {}
        zhongxings, max_vals = UIMatcher.findpic(screen_shot, template_paths=template_paths, crop=crop)
        # enumerate 枚举所有图片  多个图片则返回最后一个
        for i, name in enumerate(template_paths):
            print(f"{name[4:-4]}-{round(max_vals[i], 3):.3f}", end=' ')
            if max_vals[i] > threshold:
                return_dic[name] = (zhongxings[i][0] * Height, zhongxings[i][1] * Width)
        return return_dic

    def click_xy(self, x=1, y=1, xy=None, usage=''):
        if xy:
            x = xy[0]
            y = xy[1]
        if x < 1 and y < 1:
            x = self.dWidth * x
            y = self.dHeight * y
        else:
            x += random.random()*random_click
            y += random.random()*random_click
        time.sleep(0.4)
        try:
            self.d.click(x, y)
            print(f"点击{usage}{x, y}", end=' ')
        except:
            print(f"{x, y}失败")

    def click(self, name, wait='', timeout=3):
        if name in _coordinates:
            x, y = _coordinates[name]
            self.click_xy(x, y, usage=name)
            time.sleep(timeout)
            return 1
        if not wait:
            wait = name

        while not self.is_there_img(img=wait):
            time.sleep(1)
            timeout -= 1
            if timeout == 0:
                print(f'找不到-{name}')
                return -1
        print(f'\n查从画面寻找{name}的坐标')
        if self.is_there_img(img=name):
            x, y = self.is_there_img(img=name)
            self.click_xy(x, y)
            time.sleep(timeout)
            return 1
        else:
            raise ValueError('找不到，退出寻找')


    def pinch(self):
        self.d.pinch_in(percent=100, steps=10)
        self.d.pinch_out()

    def drag(self, sx, sy, ex, ey):
        self.d.drag(sx, sy, ex, ey)

    def home(self):
        if self.is_there_img('battle'):
            return 1
        return 0

    def cv_imread(self, file_path):
        cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
        return cv_img

    def realtime_screenshot(self):
        return self.d.screenshot(format="opencv")

    def test(self):
        while 1:
            screen_shot_ = self.realtime_screenshot()
            time.sleep(5)
            count = 0
            for i in _mark:
                count += 1
                _mark_pic, threshold, usage = all_mark_piece(i)
                self.is_there_img(screen=screen_shot_, img=_mark_pic, threshold=threshold, debug=usage)
                if count % 8 == 0:
                    print('\n')

    def click_11_get_into_game(self):
        while not self.is_there_img(img='battle'):
            time.sleep(0.5)
            print('点击左上角进入游戏')
            self.click_xy(1, 1)
        self.dWidth, self.dHeight = self.d.window_size()
        print('进入浮游城')
        return True
