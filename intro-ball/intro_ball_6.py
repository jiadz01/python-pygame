'''intro_ball_6.py 弹跳的球6  对intro_ball_5.py扩展修改    2022.6.22
pygame提供了多种碰撞的检测方法:包括矩形碰撞检测、圆形碰撞检测和使用mask的精准碰撞检测.
本例自创建检测2个矩形(Rect)a,b是否碰撞函数collision_check(),来检测碰撞.
自创建退出游戏程序函数doExit().
本例示范游戏编程最基本的入门结构,内容是一个彩色球在有背景的游戏窗口中自动弹跳,
和图像bass由用户控制它上下左右进行移动:
  1.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此游戏程序.
  2.按键盘q或Q键,退出此游戏程序.
  3.图片文件intro_ball.gif,singapore2.jpg和mouse.png,音乐文件ballVoice.wav
    和home.wav需在本程序同一目录中,或在程序的文件名字符串中指明它磁盘目录路径.
  4.用户按下4个方向(上下左右)键进行精灵(mouse)移动,检测它是否与弹跳的球发生碰撞,
    如有碰撞则球消失,另一个新球再从顶部弹出.
'''
# 导入所需的模块
import sys # 导入python内置sys模块,调用其对象、类和函数等前加sys.
import random # 导入python内置random模块,调用其对象、类和函数等前加random.
import pygame # 导入pygame模块,调用其对象、类和函数等前加pygame.

# 自创建检测2个矩形(Rect)a,b是否碰撞(图形有重叠区域)函数
# 参数a,b是矩形(Rect)变量,参数aResize,bResize是对应的调整数,默认值=0
# 对应的调整数参数可省略,具体大小可据实验确定,调节2个矩形碰撞(重叠)界线
def collision_check(a, b,aResize=0,bResize=0):
    # a碰b之间的矩形区域是否有交汇,x轴与y轴是否有重叠表达式
    expression1 = (b.x <= a.x + a.width-aResize <= b.x + b.width-bResize)
    expression2 = (b.y <= a.y + a.height-aResize <= b.y + b.height-bResize)
    # b碰a之间的矩形区域是否有交汇,x轴与y轴是否有重叠表达式
    expression3 = (a.x <= b.x + b.width-bResize <= a.x + a.width-aResize)
    expression4 = (a.y <= b.y + b.height-bResize <= a.y + a.height-aResize)
    # 对表达式判定是否发生碰撞
    if (expression1 and expression2) or (expression3 and expression4):
          return True # 判定发生碰撞,返回True布尔值
    else:
          return False # 没有发生碰撞,返回False布尔值

# 自创建退出游戏程序函数
def doExit():
    pygame.quit() # 卸载所有pygame模块
    sys.exit() # 终止程序，退出游戏主循环,关闭游戏窗口

# 使用pygame之前必须用这条命令初始化.
pygame.init() # 初始化pygame游戏引擎

FPS = 60 # 设置画面刷新的帧率,即每秒内刷新次数(帧画面),数字越小跳动越慢
size = width, height = 640, 480 # 设置游戏窗口宽和高,及对应的3个变量
ballSpeed = [ 5,5 ] # 列表变量,设置所绘图形Rect的x,y轴移动偏移量,表现为ball移动速度.
bossSpeed = 26 # 设置boss图形Rect的x或y轴移动偏移量,表现为移动速度.
# 创建游戏主窗口surface对象screen,参数size是二元组变量:窗口的宽和高
screen = pygame.display.set_mode(size)
# 设置现显示游戏窗口的标题，可以是说明游戏名称等字符串
pygame.display.set_caption('Intro ball 6')

# 从文件加载窗口背景图片,转换成Surface对象bg,图片字符串文件名可带有文件的路径.
bg = pygame.image.load("singapore2.jpg").convert()
# 背景图片Surface对象bg大小缩放到与游戏窗口screen大小
bg = pygame.transform.scale(bg, (size))

# 从文件加载2个图片,转换成Surface对象,图片字符串文件名可带有文件的路径.
ball = pygame.image.load("intro_ball.gif").convert_alpha()
boss = pygame.image.load("mouse.png").convert_alpha()
# 用transform模块的scale()方法
# 把2个图片大小缩放到参数要求,第二个参数可是元组或列表变量:图像缩放的宽和高
ball = pygame.transform.scale(ball, [40, 40])
boss = pygame.transform.scale(boss, [60, 90])
# 获取图片Surface对象的矩形区域(图像的位置Rect对象)
ballRect = ball.get_rect()
bossRect = boss.get_rect()
bossRect.center = [width/2,height/2] # 设置boss初始位置在窗口中央

# 用blit()方法将图片Surface对象绘制在screen上
screen.blit(bg, (0,0)) # 参数0,0是背景图bg与窗口重叠
#screen.blit(boss,bossRect) # 绘制boss在窗口中央
# 调pygame的显示控制模块display中的函数将图绘制在游戏窗口screen
pygame.display.update() # 无参数吋就完全等效flip()

# 用pygame的mixer模块中的Sound类,从文件或缓冲区对象创建新的音效Sound对象
# 字符串中的文件名可带有文件的路径
voice1 = pygame.mixer.Sound('ballVoice.wav') # 球碰窗口边弹回声
voice2 = pygame.mixer.Sound('suction.wav') # 球碰精灵后消失声
# 用Sound类的方法set_volume(n)设置该音效音量大小,
voice1.set_volume(0.6) # 音量大小参数n范围0.0---1.0
voice2.set_volume(0.8) # 音量大小参数n范围0.0---1.0

# 用pygame中的music模块(控制音频流)加入游戏背景音乐
  # 从文件加载背景音乐,字符串中的文件名可带有文件的路径
pygame.mixer.music.load('home.wav')
#pygame.mixer.music.load('happyBirthday.mp3')
  # 设置音量大小,音量大小参数范围0.0---1.0
pygame.mixer.music.set_volume(0.5)
  # 开始播放,整数字参数n系播放循环次数(n+1),-1是一直循环播放
pygame.mixer.music.play(-1)
# 因处理移动方法不同,将boss的Rect对象拷贝,以便boss移动时擦除旧图片
old_bossRect = bossRect.copy() # old_bossRect是Rect对象

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
          doExit() # 调自创建退出游戏程序函数
        # 判断用户是否按键盘
        if event.type == pygame.KEYDOWN:
            # 判断用户是否按键盘q或Q键,如果是则退出游戏程序
            if event.key == pygame.K_q:
              doExit() # 调自创建退出游戏程序函数
            # 用户按下4个方向键,直接改变图标的Rect对象x或y轴坐标值,让它在窗口中移动
            # 判断用户是否按键盘up arrow 键
            if event.key == pygame.K_UP:
              if bossRect.top > 0: # boss顶未超出窗口就向上移动bossSpeed变量值
                  bossRect.y = bossRect.y-bossSpeed # 减小y轴值
            # 判断用户是否按键盘down arrow 键
            if event.key == pygame.K_DOWN:
              if bossRect.bottom < height: # boss底未超出窗口底就向下移动
                  bossRect.y = bossRect.y+bossSpeed # 增大y轴值
            # 判断用户是否按键盘left arrow 键
            if event.key == pygame.K_LEFT:
              if bossRect.left > 0: # boss左边未超出窗口左边就向左移动
                  bossRect.x = bossRect.x-bossSpeed # 减小x轴值
            # 判断用户是否按键盘right arrow 键
            if event.key == pygame.K_RIGHT:
              if bossRect.right < width: # boss右边未超出窗口右边就向右移动
                  bossRect.x = bossRect.x+bossSpeed # 增大x轴值
    # 调用Rect方法move(x,y),移动Rect对象ball.  x,y是对应坐标轴移动偏移量
    newBallRect = ballRect.move(ballSpeed)

    # 检测图像的位置Rect对象碰到显示窗口左右边缘,x坐标轴方向
    if newBallRect.left < 0 or newBallRect.right > width:
        # 当球碰到窗口左右边被弹回时发碰撞音效声
        pygame.mixer.Sound.play(voice1)
        # 将列表变量第1项值取负后重新赋回,改变移动方向
        ballSpeed[0] = -ballSpeed[0]
    # 检测图像的位置Rect对象碰到显示窗口上下边缘,y坐标轴方向
    if newBallRect.top < 0 or newBallRect.bottom > height:
        # 当球碰到窗口上下边被弹回时发碰撞音效声
        pygame.mixer.Sound.play(voice1)
        # 将列表变量第2项值取负后重新赋回,即改变移动方向
        ballSpeed[1] = -ballSpeed[1]

    # 检测并处理2个Rect对象newBallRect和bossRect是否碰撞
    # 调自创建检测2个矩形(Rect)是否碰撞函数collision_check()
    if collision_check(newBallRect,bossRect):
    #if collision_check(newBallRect,bossRect,8,6): # 增加碰撞调整值
          # 当球碰到精灵后被吸入消失时音效声
          pygame.mixer.Sound.play(voice2)
          # 根据下边对Rect的x,y坐标设置,球从窗口顶部重新落下
          newBallRect.x = random.randint(0,width-100) #从0到width-100中随机生成x
          newBallRect.y = 0
          #  将列表变量2项值都取绝对值后重新赋回,移动方向回到初始状态
          ballSpeed[0] = abs(ballSpeed[0])
          ballSpeed[1] = abs(ballSpeed[1])


    # 用Surface的方法处理图像(Surface对象)
      # 用blit()方法重新绘制背景指定区域，等同于擦除变动的旧图片效果
      # 下边2个Rect对象参数,前个是指区域(取位置左上角坐标),后个是指定图片对象范围
    screen.blit(bg,ballRect,ballRect)
    screen.blit(bg,old_bossRect,old_bossRect)
      # 用blit()方法将ball移动后图像,按Rect对象的区域,绘制在screen上
    screen.blit(ball,newBallRect)
    screen.blit(boss,bossRect)

    # 调pygame的显示控制模块display中的update()函数,参数用列表方式传递每一帧图片
    # 变化的区域(Rect对象),将只对变动的Surface区域进行刷新显示到屏幕上
    pygame.display.update([ballRect,newBallRect,old_bossRect,bossRect])

    ballRect = newBallRect # 将已移动ball的Rect存入变量,以便再移动时擦除旧图片
    # 因处理移动方法不同,将已移动boss的Rect对象拷贝,以便再移动时擦除旧图片
    old_bossRect = bossRect.copy() # 用Rect模块中的copy()方法拷贝