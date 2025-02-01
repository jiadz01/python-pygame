'''text_01.py     文本图像入门案例 01       2022.6.1
pygame是python一款专门用来开发视频游戏的软件包,底层主要是SDL库实现,
是开发2D电子游戏的一个性能比较高的游戏框架.需要从https://www.pygame.org
或者用Python包 (软件库) 管理工具pip下载并安装第三方专用模块pygame.
本例示范游戏编程最基本的入门结构,并将文本内容显示在游戏窗口中:
  1.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此游戏程序.
  2.本例由一系列连续静止的文本图片构成,故没有设置pygame时钟对象和控制刷新动态图像频率等语句.
  3.字体文件ALGER.ttf需在本程序同一目录中或在程序中指明它所在磁盘目录路径.
    也可换成计算机磁盘上字体文件目录中的其它你喜爱的字体文件(文件类型.ttf).
  4.RGB255颜色模式值和颜色十六进制码是怎么产生与选取,可详见turtle目录自编工具color_rgb.py
  5.pygame通过事件队列来处理其所有事件消息传递,事件队列有上限,要不事件栈满了之后程序就
    会卡死,所以游戏主循环中(每一帧中)都要用以下其中一个方法来处理事件：
    pygame.event.get(),pygame.event.pump(), pygame.event.wait(),
    pygame.event.peek() 或者 pygame.event.clear()
'''
#导入所需的模块
import sys # 导入python内置sys模块,调用其对象、类和函数等前加sys.
import pygame # 导入pygame模块,调用其对象、类和函数等前加pygame.
# 使用pygame之前必须用这条命令初始化.
pygame.init() # 初始化pygame游戏引擎
# 创建游戏主窗口surface对象screen,并设置主屏窗口大小
screen = pygame.display.set_mode((400,400))
# 设置现显示游戏窗口的标题，可以是说明游戏名称等字符串
pygame.display.set_caption('Pygame example: text_01') # 也可不用,使用默认名pygame window

# 用font模块Font类,从磁盘文件创建新的字体对象(Font object)
# 第一个参数是可带路径的文件名字符串,第二个参数字体的大小值,  f是新的Font对象
#f = pygame.font.Font('C:/Windows/Fonts/stcaiyun.ttf',60) # 微软windows操作系统用
#f = pygame.font.SysFont('candara', 60, bold=False, italic=False) # 从py系统中选字体
f = pygame.font.Font('ALGER.ttf',60)

# draw text on a new Surface 用Font类的render()方法创建文本Surface对象
# render()第一个参数:文本内容字符串,第二个参数:字体是否平滑,
# 第三个参数:字体颜色值,第四个参数:字体背景颜色值.
text = f.render("Hi YiChen !",True,(255,0,0),(0,0,0)) # text是Surface对象
# 获取text文本图片Surface对象的矩形区域(文本图像的位置Rect对象)
textRect =text.get_rect() # textRect是Rect对象
# 用Rect对象具有的多个虚拟属性之一center设置显示Rect对象居游戏窗口中
textRect.center = (200,200)
# 用Surface的方法处理图像(Surface对象)
# 用blit()方法将text文本图像,按textRect指定的Rect对象的区域,绘制在screen上
screen.blit(text,textRect)
# 游戏主循环 game loop
while True:
    # Pygame处理事件的结构(即事件队列方式，该栈结构遵循遵循“先到先处理”的基本原则)
    # 这个for循环遍历弹出事件语句一定要写，要不事件栈满了之后程序就会卡死
    for event in pygame.event.get(): # 用for循环遍历事件队列,弹出获取并从队列删除
        # 判断用户是否点了"X"关闭按钮,并执行if代码段
        if event.type == pygame.QUIT:
            pygame.quit() # 卸载所有pygame模块
            sys.exit() # 终止程序运行，退出游戏主循环,关闭游戏窗口
    # 调pygame的显示控制模块display中的函数,将待显示的Surface对象显示到屏幕上
    pygame.display.flip() #更新屏幕内容screen