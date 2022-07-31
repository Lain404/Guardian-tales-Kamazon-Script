import os
from utils import B_Automator
from datetime import datetime, timedelta
import time


# 启动并登录游戏到主界面
def enter_game(a: B_Automator):
    a.click_11_get_into_game()
    time.sleep(1)
    while a.is_there_img(img='close'):
        a.click('close')
        time.sleep(1)
    if a.is_there_img(img='领取奖励'):
        a.click('领取奖励')
        time.sleep(1)
        a.click('确认')


def back2havenhold(a: B_Automator):
    a.click_11_get_into_game()


# 点击事件直到另一事件出现
def click_untill(a: B_Automator, target='确认', till='瓶盖商店', untill=''):
    counter = 3
    while True:
        time.sleep(0.5)
        counter += 1
        print(f'点击[{target}] 直到出现[{till}] 直到不出现[{untill}] - {counter} ')
        if counter > 6:
            return -1
        elif counter < 0:
            return 1
        if a.is_there_img(img=target):
            print(f'找到 {target}')
            counter -= 1
            a.click(target, timeout=1)
        if till:
            if a.is_there_img(img=till):
                print(f'找到结束标记 {till}')
                counter -= 3
        if untill:
            if a.is_there_img(img=untill):
                print(f'找到继续标志 {untill}')
                counter += 1
        a.click(target, timeout=1)


# 选择战后奖励
def choose_reward(a: B_Automator, target=''):
    counter = 0
    while True:
        time.sleep(0.5)
        a.save_screenshot()
        # 选择逻辑 优先选高级 次选不选择 最后随机选择
        if xy := a.is_there_img(img='战利品高阶神器'):
            a.click_xy(xy=xy)
        elif xy := a.is_there_img(img='净化'):
            a.click_xy(xy=xy)
            a.click('确认')
            return 1
        elif xy := a.is_there_img(img='不选择可选'):
            a.click_xy(xy=xy)
            a.click('确认')
            return 1
        elif xy := a.is_there_img(img='战利品中阶神器'):
            a.click_xy(xy=xy)
        else:
            print('随机选择')
            a.click_xy(300, 400)
            a.click_xy(650, 400)
            a.click_xy(950, 400)
        a.click('选择')
        # 直接出现 确认 或者出现 处理多余神器
        counter = 0
        while counter < 10:
            time.sleep(0.3)
            if a.is_there_img(img='处理不可选'):
                print('战后奖励 - 处理多余神器')
                return del_item(a)
            if xy := a.is_there_img(img='确认'):
                a.click_xy(xy=xy)
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
        if counter > 10:
            print('似乎没有开始战斗，返回主界面')
            return -1
        if a.is_there_img(img='战斗中'):
            print('战斗开始', end='')
            break
    start_time = datetime.now()
    death_flag = 0
    while a.is_there_img(img='战斗中'):
        print('战斗中...', end='')
        if datetime.now() - start_time > timedelta(seconds=50):
            print('检测到超时可能，退出战斗。')
            a.click('战斗中')
            time.sleep(1)
            a.click('确认')
            time.sleep(3)
            return -1
        if 0 in a.get_hp():
            # 假设4个角色不会在一秒内同时暴毙
            print('检测到角色阵亡，退出战斗')
            a.click('战斗中')
            time.sleep(1)
            a.click('确认')
            time.sleep(3)
        time.sleep(1)
    print('战斗结束')
    return 1


# 进入事件
def into_event(a: B_Automator):
    print('进入事件\t', end='')
    time.sleep(3)
    # 判断是什么事件
    a.save_screenshot()
    if a.is_there_img(img='阿加莎店铺'):
        print('阿加莎店铺事件')
        a.click('退出')
        a.click('确认')
        return 1
    elif xy := a.is_there_img('确认'):
        a.click_xy(xy=xy)
    counter = 0
    while True:
        print('进入其他事件')
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
        if a.is_there_img(img='处理不可选'):
            while True:
                if del_item(a):
                    break
        else:
            if r1 or r2:
                return 1


def del_item(a: B_Automator):
    counter = 0
    print(f'进入处理多余神器 {counter}')
    if not a.is_there_img(img='处理不可选'):
        return -1
    while True:
        print(f'处理多余神器 循环 {counter}')
        counter += 1
        time.sleep(1)
        if not a.is_there_img(img='处理不可选'):
            return -1
        elif xy := a.is_there_img(img='处理任意低阶神器'):
            a.click_xy(xy=xy)
        elif xy := a.is_there_img(img='处理任意中阶神器'):
            a.click_xy(xy=xy)
        elif xy := a.is_there_img(img='event/摇钱树'):
            a.click_xy(xy=xy)
        else:
            # 第一个神器
            a.click_xy(652, 293)
        r1 = a.click('处理')
        r2 = a.click('确认')
        if r1 or r2 or counter > 2:
            break


# 进入卡马逊
def enter_camazon(a: B_Automator, level=4, item_support=1):
    a.click('探险')
    time.sleep(1)
    a.click('卡马逊乐园')
    a.click('确认', timeout=3)
    time.sleep(2)  # 等待
    if not a.is_there_img(img='挑战结束'):  # 不完全条件
        time.sleep(2)
        a.click('挑战')
        print('进入难度选择')
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
        time.sleep(1)
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
        a.click('确认')
        a.click_xy(640, 550)  # 存在两个确认，要点中间那个。
    elif a.is_there_img(img='瓶盖商店'):
        while True:
            print('进入挑战界面')
            time.sleep(0.5)
            if xy := a.is_there_img(img='确认'):
                if a.is_there_img(img='神器到达上限'):
                    del_item(a)
                else:
                    a.click_xy(xy=xy)
                # click_untill(a, target='确认', till='挑战结束')
            elif xy := a.is_there_img(img='进入'):
                a.click_xy(xy=xy)
                # click_untill(a, target='进入', till='战斗中')
            elif a.is_there_img(img='选择战利品'):
                print('\n进入战后奖励选择')
                r = choose_reward(a)
            elif result := a.is_there_img(img='pointer'):
                x_limit = 1100
                y_limit = 386
                if result[0] > x_limit and result[1] + 60 < y_limit:
                    print('箭头位于禁区，拖拽')
                    a.drag(600, 400, 400, 600)
                    continue
                print('点击箭头下方进入战斗或事件')
                # result = a.is_there_img(img='pointer')
                if result:
                    a.click_xy(result[0], result[1] + 60)
                    time.sleep(4)
                    # 此时应该进入战斗或者事件页面，如果不是则退出
                counter = 0
                while True:
                    time.sleep(0.5)
                    print('路径选择界面\n')
                    counter += 1
                    if counter > 1:
                        break
                    if a.is_there_img(img='普通战斗'):
                        a.click('进入')
                        ret = into_battle(a)
                        if ret == -1:
                            break
                        counter = 0
                        while True:
                            print('战斗结束阶段')
                            time.sleep(1.8)
                            if a.is_there_img(img='无法战斗'):
                                print('存在无法战斗成员')
                                break
                            elif xy := a.is_there_img(img='确认'):
                                # a.click('确认')
                                a.click_xy(xy=xy)
                            elif a.is_there_img(img='选择战利品'):
                                print('\n进入战后奖励选择')
                                r = choose_reward(a)
                                if r:
                                    print('战利品选择结束')
                                    break
                            elif a.is_there_img(img='挑战结束'):
                                counter += 1
                                r = a.click('确认')
                                if counter > 3 or r:
                                    break
                    elif a.is_there_img(img='选择效果'):
                        while not a.is_there_img(img='选择'):
                            time.sleep(0.3)
                            if choose_effect(a):
                                break
                    elif a.is_there_img(img='事件'):
                        while True:
                            print('进入事件')
                            time.sleep(0.3)
                            if into_event(a):
                                break
                    elif a.is_there_img(img='处理不可选'):
                        while True:
                            if del_item(a):
                                break
                    elif a.is_there_img(img='阿加莎店铺'):
                        while True:
                            print('进入阿加莎商店')
                            time.sleep(0.3)
                            if click_untill(a, target='退出'):
                                a.click('确认')
                                break
                    elif xy := a.is_there_img(img='确认'):
                        a.click_xy(xy=xy)

            else:
                result1 = a.is_there_img(img='pointer')
                result2 = a.is_there_img(img='瓶盖商店')
                # 处在卡马逊界面但是无法点击下一个事件的两种情况
                # 需要拖屏  被其他事件(多是 确认事件)挡住
                if result2 and not result1:
                    print('drag')
                    a.drag(600, 400, 400, 600)
                if a.is_there_img(img='确认'):
                    a.click('确认')


# 日常
def daliy_quest(a: B_Automator):
    a.click('探险')
    time.sleep(2)
    a.click('圆形角斗场')
    time.sleep(1)
    a.click('确认')  # 存在战斗记录的话
    if a.is_there_img(img='角斗场开始战斗'):
        while True:
            if xy := a.is_there_img(img='44确认'):
                # a.click('44确认')
                a.click_xy(xy=xy)
            elif a.is_there_img(img='角斗场开始战斗'):
                a.click("确认", timeout=2)  # 活动积分
                a.click("角斗场开始战斗")
                time.sleep(1)
                if a.is_there_img(img='44无票'):
                    print('无票')
                    a.click('确认')
                    back2havenhold(a)
                    break
                a.click("角斗场开始战斗2")

                while a.is_there_img(img='战斗倍速'):
                    time.sleep(1)
                    print('44战斗中')
                if a.is_there_img(img='本场结果'):
                    a.click('44确认')
            elif a.is_there_img(img='角斗场开始战斗_无票'):
                print('44无票退出')
                break
            elif xy := a.is_there_img(img='确认'):
                # a.click('确认')
                a.click_xy(xy=xy)
            elif xy := a.is_there_img(img='44确认'):
                # a.click('44确认')
                a.click_xy(xy=xy)
    # 卡马逊 难度5 道具支援第九个
    # 箭头下方 神器 bug


def test(a: B_Automator):
    a.click('探险')
    time.sleep(1)
    # 画面存在了 但是点击响应需要延迟？
    a.click('圆形角斗场')


if __name__ == "__main__":
    a = B_Automator()
    a.start()
    enter_game(a)
    # test(a)
    # daliy_quest(a)
    # choose_reward(a)
    enter_camazon(a, level=4, item_support=9)

    # a.test()
