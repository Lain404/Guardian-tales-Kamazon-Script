import os
from utils import B_Automator
import time


# 启动并登录游戏到主界面
def enter_game(a: B_Automator):
    a.start()
    a.click_11_get_into_game()


# 点击事件直到另一事件出现
def click_untill(a: B_Automator, target='确认', till='瓶盖商店'):
    counter = 0
    while True:
        time.sleep(1)
        counter += 1
        if counter > 3:
            return -1
        if a.is_there_img(img=target):
            a.click(target, timeout=2)
            counter -= 1
        elif a.is_there_img(img=till):
            counter += 1
            return 1
        a.click(target, timeout=1)


# 选择战后奖励
def choose_reward(a: B_Automator, target=''):
    counter = 0
    while True:
        time.sleep(1)
        counter += 1
        if counter > 3:
            return -1
        # 选择逻辑 优先选高级 次选不选择 最后随机选择
        if a.is_there_img(img='高阶神器'):
            a.click_xy(xy=a.is_there_img(img='高阶神器'))
        elif a.is_there_img(img='不选择可选'):
            a.click_xy(xy=a.is_there_img(img='不选择可选'))
        else:
            a.click_xy(300, 400)
            a.click_xy(650, 400)
            a.click_xy(100, 400)
        r1 = a.click('选择')
        r2 = a.click('确认')
        if r1 or r2:
            return 1


# 选择恢复区效果
def choose_effect(a: B_Automator):
    print('\n恢复区-选择效果')
    counter = 0
    while True:
        time.sleep(1)
        counter += 1
        if counter > 3:
            return -1
        # 逻辑是优先选靠左的效果
        a.click_xy(900, 400)
        a.click_xy(600, 400)
        a.click_xy(300, 400)
        r1 = a.click('选择')
        r2 = a.click('确认')
        if r1 or r2:
            return 1


# 进入战斗
def into_battle(a: B_Automator):
    print('进入战斗\t', end='')
    counter = 0
    while True:
        time.sleep(1)
        counter += 1
        if counter > 3:
            print('似乎没有开始战斗，返回主界面')
            return -1
        if a.is_there_img(img='战斗中'):
            print('战斗开始', end='')
            break
    while a.is_there_img(img='战斗中'):
        print('战斗中...')
        time.sleep(3)
    print('战斗结束')
    return 1


# 进入事件
def into_event(a: B_Automator):
    print('进入事件\t', end='')
    counter = 0
    while True:
        time.sleep(1)
        counter += 1
        if counter > 3:
            return -1
        a.click_xy(835, 343)
        a.click_xy(835, 525)
        a.drag(835, 550, 835, 250)
        a.click_xy(835, 343)
        a.click_xy(835, 525)
        r1 = a.click('选择')
        r2 = a.click('确认')
        if r1 or r2:
            return 1


# 进入卡马逊
def enter_camazon(a: B_Automator, level=4, item_support=1):
    a.click('探险')
    a.click('卡马逊乐园')
    if not a.is_there_img(img='挑战结束'):
        a.click('挑战')
        if level < 4:
            a.click('卡马逊难度左', timeout=1, )
            a.click('卡马逊难度左', timeout=1)
            a.click(f'卡马逊难度{level % 3}', timeout=1)
        elif level < 7:
            a.click('卡马逊难度左', timeout=1)
            a.click('卡马逊难度左', timeout=1)
            a.click('卡马逊难度右', timeout=1)
            a.click(f'卡马逊难度{level % 3}', timeout=1)
        else:
            a.click('卡马逊难度右', timeout=1)
            a.click('卡马逊难度右', timeout=1)
            a.click(f'卡马逊难度{level % 3}', timeout=1)
        a.click('挑战副本')
        # 行走卡马逊进场动画
        # 可能出现的事件 支援神器
    else:
        pass
        # 直接进入，承接上次进度
    if a.is_there_img(img='支援神器'):
        item_coordinate = 0
        if item_coordinate:
            a.click_xy(xy=item_coordinate)
        a.click_xy(550 + 100 * (item_support % 5), 200 + 100 * (item_support // 5))
        a.click_xy(867, 679)
        a.click('确认')
    if a.is_there_img(img='瓶盖商店'):
        print('进入挑战界面,循环执行 寻找战斗-开始战斗-选择奖励  或者 寻找战斗-开始战斗-失败推出')
        while True:
            time.sleep(1)
            if a.is_there_img(img='确认'):
                click_untill(a, target='确认', till='挑战结束')
            elif a.is_there_img(img='pointer'):
                print('点击箭头下方进入战斗或事件')
                result = a.is_there_img(img='pointer')
                if result:
                    a.click_xy(result[0], result[1] + 60)
                    time.sleep(4)
                    # 此时应该进入战斗或者事件页面，如果不是则退出
                counter = 0
                while True:
                    time.sleep(1)
                    print('路径选择界面\n')
                    counter += 1
                    if counter > 1:
                        break
                    if a.is_there_img(img='普通战斗'):
                        a.click('进入', wait='普通战斗')
                        into_battle(a)
                        while True:
                            a.click('确认')
                            time.sleep(1)
                            if a.is_there_img(img='选择不可选'):
                                print('\n进入战后奖励选择')
                                r = choose_reward(a)
                                if r:
                                    break
                            elif a.is_there_img(img='瓶盖商店'):
                                print('噶了')
                    elif a.is_there_img(img='精英战斗'):
                        a.click('进入', wait='精英战斗')
                        into_battle(a)
                        while True:
                            a.click('确认')
                            time.sleep(1)
                            if choose_reward(a):
                                break
                    elif a.is_there_img(img='选择效果'):
                        while not a.is_there_img(img='选择'):
                            time.sleep(1)
                            if choose_effect(a):
                                break
                    elif a.is_there_img(img='事件'):
                        while True:
                            print('进入事件')
                            time.sleep(1)
                            if into_event(a):
                                break
                    elif a.is_there_img(img='处理不可选'):
                        while True:
                            print('处理多余神器')
                            time.sleep(1)
                            a.click_xy(652, 293)
                            r1 = a.click('处理')
                            r2 = a.click('确认')
                            if r1 or r2:
                                break
                    elif a.is_there_img(img='阿加莎店铺'):
                        while True:
                            print('阿加莎商店')
                            time.sleep(1)
                            if click_untill(a, target='退出'):
                                break
                    elif a.is_there_img(img='确认'):
                        while True:
                            print('确认')
                            time.sleep(1)
                            r = click_untill(a, target='确认')
                            if r:
                                break
            else:
                result1 = a.is_there_img(img='pointer')
                result2 = a.is_there_img(img='瓶盖商店')
                # 处在卡马逊界面但是无法点击下一个事件的两种情况
                # 需要拖屏  被其他事件(多是 确认事件)挡住
                if result2 and not result1:
                    print('drag')
                    a.drag(600, 400, 500, 500)
                if a.is_there_img(img='确认'):
                    click_untill(a)


if __name__ == "__main__":
    a = B_Automator()
    enter_game(a)
    # 卡马逊 难度5 道具支援第九个
    enter_camazon(a, level=5, item_support=9)
    # a.test()
