'''text_02.py     文本图像入门案例 02      对text_01.py扩展    2022.6.2
pygame是python一款专门用来开发视频游戏的软件包,底层主要是SDL库实现,
是开发2D电子游戏的一个性能比较高的游戏框架.需要从https://www.pygame.org
或者用Python包 (软件库) 管理工具pip下载并安装第三方专用模块pygame.
本例示范游戏编程最基本的入门结构,并将动态文本内容显示在游戏窗口中:
  1.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此游戏程序.
  2.本例由连续动态的文本图片构成,故设置pygame时钟对象和控制刷新图像频率等语句.
  3.字体文件ALGER.ttf需在本程序同一目录中或在程序中指明它所在磁盘目录路径.
    也可换成计算机磁盘上字体文件目录中的其它你喜爱的字体文件(文件类型.ttf).
  4.RGB颜色模式值和颜色十六进制码是怎么产生与选取,可详见turtle目录自编工具color_rgb.py
'''
#导入所需的模块
import sys # 导入python内置sys模块,调用其对象、类和函数等前加sys.
import pygame # 导入pygame模块,调用其对象、类和函数等前加pygame.
# 使用pygame之前必须用这条命令初始化.
pygame.init() # 初始化pygame游戏引擎

FPS = 30 # 设置画面刷新的帧率,即每秒内刷新次数(帧画面)
width = 640 # 设置游戏窗口宽的变量
height = 480 # 设置游戏窗口高的变量
speed1 = [ 0,-3 ] # 列表变量,设置所绘图形Rect的x=0,y轴移动偏移量,表现为y轴方向移动速度.
speed2 = [ -3,0 ] # 列表变量,设置所绘图形Rect的y=0,x轴移动偏移量,表现为x轴方向移动速度.
windowColor = (66,88,216) # 元组变量,设置窗口颜色, RGB255颜色模式值
text1Color = (255,0,0) # 文本颜色,还可设成字符串变量:"#F40100","red"等效
text2Color = (18,255,88)
# 创建游戏主窗口surface对象screen,并设置主屏窗口大小
screen = pygame.display.set_mode((width,height))
#screen.fill(windowColor) # 用fill()方法填充screen对象单一色背景
# 设置现显示游戏窗口的标题，可以是说明游戏名称等字符串
pygame.display.set_caption('Pygame example: text_02') # 也可不用,使用默认名pygame window

# 用font模块Font类,从磁盘文件创建新的字体对象(Font object)
# 第一个参数是可带路径的文件名字符串,第二个参数字体的大小值,  f是新的Font对象
#f = pygame.font.Font('C:/Windows/Fonts/stcaiyun.ttf',60) # 微软windows操作系统用
f1 = pygame.font.Font('ALGER.ttf',60)
f2 = pygame.font.SysFont('candara', 30, bold=False, italic=False) # 从py系统中选字体

# draw text on a new Surface 用Font类的render()方法创建文本Surface对象
# render()第一个参数:文本内容字符串,第二个参数:字体是否平滑,
# 第三个参数:字体颜色值,第四个参数:背景颜色值.
text1 = f1.render("Hi YiChen !",True,text1Color,windowColor) # text1是Surface对象
text2 = f2.render("Hello World !",True,text2Color) # text2是Surface对象
# 获取text文本图片Surface对象的矩形区域(文本图像的位置Rect对象)
text1Rect =text1.get_rect() # textRect1是text1的Rect对象
text2Rect =text2.get_rect() # textRect2是text2的Rect对象
# 用Rect对象具有的多个虚拟属性center,left....设置显示Rect对象初始位置
text1Rect.center = (width/2,height/2) # 设置显示text1居游戏窗口中
text2Rect.left = width # 设置显示text2初始left边,x轴坐标
text2Rect.bottom = height - 50 # 设置显示text2初始bottom边,y轴坐标
# 用Surface的方法处理图像(Surface对象)
# 用blit()方法将text文本图像,按textRect指定的Rect对象的区域,绘制在screen上
screen.blit(text2,text2Rect)
# create an object to help track time
clock = pygame.time.Clock()  # 设置pygame时钟对象
# 游戏主循环 game loop
while True:
    clock.tick(FPS)  # 用时钟对象控制每秒执行FPS次(帧画面)
    # Pygame处理事件的结构(即事件队列方式，该栈结构遵循遵循“先到先处理”的基本原则)
    # 这个for循环遍历弹出事件语句一定要写，要不事件栈满了之后程序就会卡死
    for event in pygame.event.get(): # 用for循环遍历事件队列,弹出获取并从队列删除
        # 判断用户是否点了"X"关闭按钮,并执行if代码段
        if event.type == pygame.QUIT:
            pygame.quit() # 卸载所有pygame模块
            sys.exit() # 终止程序运行，退出游戏主循环,关闭游戏窗口
    # 调用Rect方法move(x,y),移动Rect对象.  x,y是对应坐标轴移动偏移量
    text1Rect = text1Rect.move(speed1)
    text2Rect = text2Rect.move(speed2)
    # 检测文本图像1的位置Rect对象的底部碰到显示窗口上边缘(y坐标轴方向)
    if text1Rect.bottom <= 0 :
          text1Rect.y = height/2 # 将对应的位置Rect对象y值设回起点坐标
    # 检测文本图像2的位置Rect对象的右边碰到显示窗口左边缘(x坐标轴方向)
    if text2Rect.right <= 0 :
          text2Rect.left = width # 将对应的位置Rect对象x值设回起点坐标
    # 用Surface的方法处理图像(Surface对象)
    screen.fill(windowColor) # 用fill()方法填充screen对象单一色背景(清屏)
      # 用blit()方法将文本图像,按它们指定的Rect对象的区域,绘制在screen上
    screen.blit(text1,text1Rect)
    screen.blit(text2,text2Rect)
    # 调pygame的显示控制模块display中的函数,将待显示的Surface对象显示到屏幕上
    pygame.display.flip() #更新屏幕内容screen