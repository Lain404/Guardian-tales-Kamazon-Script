# Guardian-tales-Kamazon-Script
  ### 基于python和adb的一个自动刷卡马逊瓶盖的脚本
  + *原理*
    获取模拟器屏幕截图判断游戏状态，通过adb运行命令执行脚本

 + *环境*
 
    模拟器（分辨率1280\*800）  
    python3    
    uiautomator2  

 + *目前完成*

    简单的循环卡马逊逻辑  
    随机的事件选择逻辑  
    简单的处理逻辑  
    检测hp，战斗失败或者超时时回城  
    
 + *后续可能*
    50% 优化事件和道具选择  
    
    

 适合打打难度34的养老咸鱼玩家，减少卡马逊坐牢时间。
 
 图片文件在assets.py和img文件夹中，模拟器交互在utils.py中，执行逻辑在gt_auto_farm.py中，图片处理在cv.py中，部分函数参考pcrfarm项目。
