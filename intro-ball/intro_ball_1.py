'''intro_ball_1.py 弹跳的球1   2022.6.2
pygame是python一款专门用来开发视频游戏的软件包,底层主要是SDL库实现,
是开发2D电子游戏的一个性能比较高的游戏框架.需要从https://www.pygame.org
或者用Python包 (软件库) 管理工具pip下载并安装第三方专用模块pygame.
本例示范游戏编程最基本的入门结构,内容是一个彩色球在游戏窗口中自动弹跳:
  1.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此游戏程序.
  2.图片文件intro_ball.gif需在本程序同一目录中或在程序中指明它所在磁盘目录路径.
'''
# 导入所需的模块
import sys # 导入python内置sys模块,调用其对象、类和函数等前加sys.
import pygame # 导入pygame模块,调用其对象、类和函数等前加pygame.

# 使用pygame之前必须用这条命令初始化.
pygame.init() # 初始化pygame游戏引擎

FPS = 60 # 设置画面刷新的帧率,即每秒内刷新次数(帧画面),数字越小跳动越慢
width = 640 # 设置游戏窗口宽的变量
height = 480 # 设置游戏窗口高的变量
size = (width, height) # 设置游戏窗口大小的元组变量
#size = width, height = 640, 480 # 上述3条命令可用此1条命令写法,功能相同
speed = [ 5,5 ] # 列表变量,设置所绘图形Rect的x,y轴移动偏移量,表现为两轴方向移动速度.
# 设置窗口颜色(即背景颜色),有关颜色模式详见调色工具color_rgb.py
windowColor = (0,86,76) # 元组变量, RGB255颜色模式值(还可用列表变量)
#windowColor = '#002E4C' # 字符串变量,设置窗口颜色,十六进制颜色模式值,等效

# 创建游戏主窗口surface对象screen,参数size是二元组变量:窗口的宽和高
screen = pygame.display.set_mode(size)
# 设置现显示游戏窗口的标题，可以是说明游戏名称等字符串
pygame.display.set_caption('Intro ball 1') # 也可不用,使用默认名pygame window
# 从文件加载图片,转换成Surface对象,字符串文件名可带有文件的路径.
ball = pygame.image.load("intro_ball.gif")
# 获取ball图片Surface对象的矩形区域(图像的位置Rect对象)
ballRect = ball.get_rect()
# create an object to help track time
clock = pygame.time.Clock()  # 设置pygame时钟对象
# 游戏主循环 game loop
while True:
    clock.tick(FPS)  # 用时钟对象控制每秒执行FPS次(帧画面刷新)
    # Pygame处理事件的结构(即事件队列方式，该栈结构遵循遵循“先到先处理”的基本原则)
    # 这个for循环遍历弹出事件语句一定要写，要不事件栈满了之后程序就会卡死
    for event in pygame.event.get(): # 用for循环遍历事件队列,弹出获取并从队列删除
        # 判断用户是否点了"X"关闭按钮,并执行if代码段
        if event.type == pygame.QUIT: # 当用户按下窗口的关闭按钮
            pygame.quit() # 卸载所有pygame模块
            sys.exit() # 终止程序，退出游戏主循环,关闭游戏窗口
    # 调用Rect方法move(x,y),移动Rect对象.  x,y是对应坐标轴移动偏移量
    ballRect = ballRect.move(speed)
    # 检测图像的位置Rect对象碰到显示窗口左右边缘,x坐标轴方向
    if ballRect.left < 0 or ballRect.right > width:
        # 将列表变量第1项值取负后重新赋回,改变移动方向
        speed[0] = -speed[0]
    # 检测图像的位置Rect对象碰到显示窗口上下边缘,y坐标轴方向
    if ballRect.top < 0 or ballRect.bottom > height:
        # 将列表变量第2项值取负后重新赋回,即改变移动方向
        speed[1] = -speed[1]
    # 用Surface的方法处理图像(Surface对象)
    screen.fill(windowColor) # 用fill()方法填充screen对象单一色背景(清屏)
      # 用blit()方法将ball图像,按ballRect指定的Rect对象的区域,绘制在screen上
    screen.blit(ball, ballRect) # 参数ball变量也是Surface对象
    # 调pygame的显示控制模块display中的函数,将待显示的Surface对象显示到屏幕上
    pygame.display.flip() # 将完整显示 Surface 更新到屏幕,更新整个显示器的内容
    #pygame.display.update() # 只允许更新屏幕变动的部分,是flip()的优化版本
