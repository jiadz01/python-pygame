'''intro_ball_4.py 弹跳的球4  对intro_ball_3.py扩展修改    2022.6.6
用pygame的mixer模块的函数方法对象等增加游戏的运动物体的碰撞音响效果.
用pygame中的music模块(控制音频流)的函数方法对象等加入游戏背景音乐.
Pygame支持的声音格式有限,一般使用 .ogg  .wav .mp3 等的文件格式,需测试与查询.
新增事件处理,按键盘q或Q键,也可退出此游戏程序.
本例示范游戏编程最基本的入门结构,内容是一个彩色球在有背景的游戏窗口中自动弹跳:
  1.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此游戏程序.
  2.按键盘q或Q键,退出此游戏程序.
  3.图片文件intro_ball.gif和singapore2.jpg,音乐文件ballVoice.wav和home.wav
    需在本程序同一目录中,或在程序的文件名字符串中指明它所存放在磁盘目录路径.
'''
# 导入所需的模块
import sys # 导入python内置sys模块,调用其对象、类和函数等前加sys.
import pygame # 导入pygame模块,调用其对象、类和函数等前加pygame.

# 使用pygame之前必须用这条命令初始化.
pygame.init() # 初始化pygame游戏引擎
#pygame.mixer.init() # 初始化混音器模块,有上条命令后可不用写

FPS = 60 # 设置画面刷新的帧率,即每秒内刷新次数(帧画面),数字越小跳动越慢
width = 640 # 设置游戏窗口宽的变量
height = 480 # 设置游戏窗口高的变量
size = (width, height) # 设置游戏窗口大小的元组变量
#size = width, height = 640, 480 # 上述3条命令可用此1条命令写法,功能相同
speed = [ 5,5 ] # 列表变量,设置所绘图形Rect的x,y轴移动偏移量,表现为两轴方向移动速度.
# 创建游戏主窗口surface对象screen,参数size是二元组变量:窗口的宽和高
screen = pygame.display.set_mode(size)
# 设置现显示游戏窗口的标题，可以是说明游戏名称等字符串
pygame.display.set_caption('Intro ball 4') # 也可不用,使用默认名pygame window

# 从文件加载窗口背景图片,转换成Surface对象bg,图片字符串文件名可带有文件的路径.
#bg = pygame.image.load("singapore2.jpg")
bg = pygame.image.load("singapore2.jpg").convert() # 用本条命令取代上条命令可执行更快
# 背景图片Surface对象bg大小缩放到与游戏窗口screen大小
bg = pygame.transform.scale(bg, (size))
# 用blit()方法将背景图片Surface对象bg绘制在screen上
screen.blit(bg, (0,0)) # 参数0,0是背景图与窗口重叠
# 调pygame的显示控制模块display中的函数将背景图全图绘制在游戏窗口screen
pygame.display.update() # 无参数吋就完全等效flip()

# 从文件加载图片,转换成Surface对象,图片字符串文件名可带有文件的路径.
#icon = pygame.image.load("intro_ball.gif")
icon = pygame.image.load("intro_ball.gif").convert_alpha() # 用本条命令取代上条命令
# 用transform模块的scale()方法
# 图片大小缩放到60X60,第二个参数可是元组或列表变量:图像缩放的宽和高
ball = pygame.transform.scale(icon, [60, 60])
# 获取ball图片Surface对象的矩形区域(图像的位置Rect对象)
ballRect = ball.get_rect()

# 用pygame的mixer模块中的Sound类,从文件或缓冲区对象创建新的音效Sound对象
# 字符串中的文件名可带有文件的路径
voice = pygame.mixer.Sound('ballVoice.wav')
# 用Sound类的方法set_volume(n)设置该音效音量大小,
voice.set_volume(0.6) # 音量大小参数n范围0.0---1.0

# 用pygame中的music模块(控制音频流)加入游戏背景音乐
  # 从文件加载背景音乐,字符串中的文件名可带有文件的路径
pygame.mixer.music.load('home.wav')
#pygame.mixer.music.load('happyBirthday.mp3')
  # 设置音量大小,音量大小参数范围0.0---1.0
pygame.mixer.music.set_volume(0.5)
  # 开始播放,整数字参数n系播放循环次数(n+1),-1是一直循环播放
pygame.mixer.music.play(-1)

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
        # 判断用户是否按键盘q或Q键,如果是则退出游戏程序
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit() # 卸载所有pygame模块
            sys.exit() # 终止程序，退出游戏主循环,关闭游戏窗口

    # 调用Rect方法move(x,y),移动Rect对象.  x,y是对应坐标轴移动偏移量
    newBallRect = ballRect.move(speed)

    # 检测图像的位置Rect对象碰到显示窗口左右边缘,x坐标轴方向
    if newBallRect.left < 0 or newBallRect.right > width:
        # 当球碰到窗口左右边被弹回时发碰撞音效声
        pygame.mixer.Sound.play(voice)
        # 将列表变量第1项值取负后重新赋回,改变移动方向
        speed[0] = -speed[0]
    # 检测图像的位置Rect对象碰到显示窗口上下边缘,y坐标轴方向
    if newBallRect.top < 0 or newBallRect.bottom > height:
        # 当球碰到窗口上下边被弹回时发碰撞音效声
        pygame.mixer.Sound.play(voice)
        # 将列表变量第2项值取负后重新赋回,即改变移动方向
        speed[1] = -speed[1]

    # 用Surface的方法处理图像(Surface对象)
      # 用blit()方法重新绘制背景指定区域，等同于擦除变动的旧图片效果
      # 下边2个Rect对象参数,前个是指区域(取位置左上角坐标),后个是指定图片对象范围
    screen.blit(bg,ballRect,ballRect) # 详见文档说明
      # 用blit()方法将ball移动后图像,按Rect对象的区域,绘制在screen上
    screen.blit(ball,newBallRect)

    # 调pygame的显示控制模块display中的update()函数,参数用列表方式传递每一帧图片
    # 变化的区域(Rect对象),将只对变动的Surface区域进行刷新显示到屏幕上
    pygame.display.update([ballRect,newBallRect])

    ballRect = newBallRect # 将已移动的Rect存入变量,以便再移动时擦除旧图片