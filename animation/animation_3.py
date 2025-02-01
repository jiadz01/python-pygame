'''animation_3.py   动画示例 3   对animation_1.py修改  2022.10.29
a.本例用pygame中time模块的 pygame.time.get_ticks(),以毫秒为单位获取当前时间,
  来计算和控制动画的每帧间隔(帧速率),从而不再影响游戏主循环画面刷新和主循环中
  执行其它命令的速度,游戏不易卡顿.
b.单独设置(拷贝)动画每帧的矩形框(Rect对象)进行绘制处理,更好理解和掌握相关语句.
c.本例用图片文件 RC.png,总图中有8帧人物不同动态的分图片.
本例用Surface模块中的方法blit(source, dest, area=None, special_flags=0)实现.
利用第三个参数area(Rect对象)在循环绘图过程中,将变化的每帧图按秩序绘制在屏幕上,
利用人类"视觉暂留"(约0.1-0.4秒)现象,实现动画效果(就象放映电影).
1.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此程序.
2.图片文件 RC.png 需在本程序同一目录中,或在程序的文件名字符串中指明它磁盘目录路径.
'''
# 导入所需的模块
import pygame # 导入pygame模块,调用其对象、类和函数等前加pygame.
import sys # 导入python内置sys模块,调用其对象、类和函数等前加sys.

FPS = 60 # 设置画面刷新的帧率,即每秒内刷新次数(帧画面)
SIZE = WIDTH, HEIGHT = 640, 480 # 设置游戏窗口宽和高,3个大写为全局变(常)量
interval = 80 # 设置动画画面的间隔时间 80 毫秒,数字越小动画人物的动作越快
# 设置窗口颜色(即背景颜色),有关颜色模式详见调色工具color_rgb.py
windowColor = (36,186,255) # 元组变量, RGB255颜色模式值(还可用列表变量)

pygame.init() # 初始化pygame游戏引擎

# 初始化游戏窗口屏幕显示
screen = pygame.display.set_mode(SIZE)
screen.fill(windowColor) # 用fill()方法填充screen对象单一色背景
pygame.display.update() # 无参数吋就完全等效flip()
pygame.display.set_caption('Animation example 3 ') # 设置游戏窗口的标题

image = pygame.image.load('RC.png') # 从文件加载总图片,转换成Surface对象
personFrame = 8 # 设置总图帧数，本例总图中有8帧人物不同动态的分图片
personRect = image.get_rect() # 获取总图的Rect，以此计算出单帧Rect的宽和高
frameRect = personRect.copy() # 将personRect拷贝到frameRect供动画每帧矩形框用
frameRect.width = abs( personRect.width / personFrame ) # 获取每一帧的Rect宽
#frameRect.x = 0 # 设置每一帧图片的起始 x 轴坐标值 (相对于总图的Rect) 黙认,可省略
#frameRect.y = 0 # 设置每一帧图片的起始 y 轴坐标值 (相对于总图的Rect) 黙认,可省略
# 设置动画人物在显示窗口的位置
personRect.x = WIDTH/2 - frameRect.width/2 # 设置动画人物 X 轴坐标值 (窗口中央)
personRect.y = HEIGHT/2 - frameRect.height/2 # 设置动画人物 Y 轴坐标值 (窗口中央)

# 从总图中获取每帧图像以循环方式绘动画图像
clock = pygame.time.Clock()  # 设置pygame时钟对象
n = 0 # 初始化帧计数变量,0-总图的第一帧
# 用pygame中time模块的 pygame.time.get_ticks(),以毫秒为单位获取当前时间
lastTime = currentTime = pygame.time.get_ticks() # 同时赋值给2个变量,协助控制动画帧速率
while True: # 游戏主循环
    for event in pygame.event.get(): # 用for循环遍历事件队列,弹出获取并从队列删除,一定要写
        if event.type == pygame.QUIT: # 当用户按下窗口的关闭按钮
            pygame.quit() # 卸载所有pygame模块
            sys.exit() # 终止程序，退出游戏主循环,关闭游戏窗口
    currentTime = pygame.time.get_ticks() # 以毫秒为单位获取时间,赋值给currentTime
    if currentTime >= lastTime + interval: # 如达到设定间隔时间,则准备画下帧
        if n < personFrame:
            frameRect.x = frameRect.width * n # 改变帧图片的起始 x 轴坐标值到下一帧起始位
            n += 1
        else:
            n = 0 # 帧计数变量回到总图的第一帧
        lastTime = currentTime

    screen.fill(windowColor) # 用fill()方法填充screen对象单一色背景 (清屏)
    # 将总图image按frameRect矩形所确定帧,以personRect确定的窗口坐标绘制在screen
    screen.blit(image,personRect,frameRect)
    pygame.display.update() # 完整显示 Surface,更新整个显示器的内容,是flip()的优化版本
    clock.tick(FPS)  # 用时钟对象控制每秒执行FPS次 (主循环帧画面刷新)