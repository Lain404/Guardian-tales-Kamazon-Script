import uiautomator2 as u2
import time
import random
from cv import *
import cv2
import numpy as np
from PIL import Image
import os
from assets import _mark_path, _mark, all_mark_piece, search_mark, _coordinates
from datetime import datetime

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
            self.d = u2.connect_usb(f'127.0.0.1:{emulator_port}')
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

    def is_there_img(self, screen=0, img='battle', threshold=0.81, crop=0, debug=False):
        try:
            if type(screen) == int:  # it means get all stats from image name
                screen = self.realtime_screenshot()
            if not img.endswith('.jpg'):
                img = _mark_path.format(img)
            if not crop or len(crop) == 1:
                active_path = self.get_butt_stat(screen, [img], threshold, crop)
            else:
                # 默认传入一个box组 [[4],.....]
                result = []
                for box in crop:
                    active_path = self.get_butt_stat(screen, [img], threshold, box)
                    if img in active_path:
                        result.append(True)
                    else:
                        result.append(False)
                    return result
            if img in active_path:
                if debug:
                    print(debug, active_path, end='\n')
                return active_path[img]
            else:
                return False
        except:
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
            x += random.random() * random_click
            y += random.random() * random_click
        time.sleep(0.2)
        try:
            self.d.click(x, y)
            print(f"点击{usage}{x, y}", end=' ')
        except:
            print(f"{x, y}失败")

    def click(self, name, wait='', timeout=3):
        timeout = timeout * 3
        if name in _coordinates:
            x, y = _coordinates[name]
            self.click_xy(x, y, usage=name)
            time.sleep(0.5)
            return 1
        if not wait:
            wait = name
        while timeout:
            time.sleep(0.3)
            if xy := self.is_there_img(img=name):
                time.sleep(0.3)
                self.click_xy(xy=xy)
                return 1
            timeout -= 1
            if timeout <= 0:
                print(f'找不到-【{name}】，退出寻找')
                return -1

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

    def save_screenshot(self):
        path = "D:\_Projects\_Github\ADB\gt_scripts\img\\resource\\auto\\"
        name = str(datetime.now()).replace(':', '')
        path = path + name + '.jpg'
        print(f'保存图片到{path}')
        screen_shot_ = self.realtime_screenshot()
        cv2.imwrite(path, screen_shot_)

    def get_hp(self):
        screen = self.realtime_screenshot()
        # screen = cv_imread("D:\_Projects\_Github\ADB\gt_scripts\Screenshot_20220622-053824.png")
        # cv2.imshow('1', screen)
        # cv2.waitKey(0)
        # screen = UIMatcher.RotateClockWise90(screen)

        def count_none_zero(crop_img):
            hp = 0
            nhp = 0
            armor = 0
            hp_s = [47, 205, 74]
            armor_s = [161, 161, 161]
            nhp_s = [33, 54, 33]
            p_x, p_y, d = crop_img.shape
            # cv2.imshow('1', crop_img)
            # cv2.waitKey(0)
            for color in crop_img[0]:
                # [[3].....]
                if (color == hp_s).all():
                    hp += 1
                elif (color == nhp_s).all():
                    nhp += 1
                elif (color == armor_s).all():
                    armor += 1
                else:
                    pass
            if armor == 0:
                if hp == 0:
                    life = 0
                else:
                    life = hp / (hp + nhp)
            else:
                life = 1 + armor / (hp + 1)
            # (armor, hp, nhp, life)
            return round(life, 3)

        up = 125
        down = 132
        left = 25
        interval_x = 70
        bar_x = 50
        total_hp = []
        for i in range(4):
            total_hp.append(
                count_none_zero(screen[up + 2:up + 3, interval_x * i + left:interval_x * i + left + bar_x]))
        print('角色Hp ', total_hp)
        return total_hp


if __name__ == "__main__":
    # b = B_Automator()
    # b.save_screenshot()
    B_Automator.get_hp()
