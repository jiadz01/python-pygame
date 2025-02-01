'''intro_ball_7.py 弹跳的球7  对intro_ball_2.py扩展修改    2022.7.22
本例是每帧画面全部重新画(刷新)方式.
自创建Sprite类的子类Ball(),可生成许多不同图形,不同大小和不同移动速度的弹跳球实例.
注意我发现:只能按本例方式调用类Ball()生成各个球的self.speed值,
     否则程序运行出现异常(bug?),这些语句后边#标注有**
自创建检测2个矩形(Rect)a,b是否碰撞函数collision_check().
自创建退出游戏程序函数doExit().
本例示范游戏编程较为规范结构,内容是n个彩色球在游戏窗口中自动弹跳,
和图像bass由用户控制它上下左右进行移动:
  1.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此游戏程序.
  2.按键盘q或Q键,退出此游戏程序.
  3.图片文件intro_ball.gif,ball.png和mouse.png,
    音乐文件ballVoice.wav,suction.wav和home.wav,
    需在本程序同一目录中,或在程序的文件名字符串中指明它磁盘目录路径.
  4.用户按下4个方向(上下左右)键进行精灵boss移动,检测它是否与弹跳的球发生碰撞,
    如有碰撞则球消失,另一个相同新球再从顶部弹出.
'''
# 导入所需的模块
import sys # 导入python内置sys模块,调用其对象、类和函数等前加sys.
import random # 导入python内置random模块,调用其对象、类和函数等前加random.
import pygame # 导入pygame模块,调用其对象、类和函数等前加pygame.

FPS = 30 # 设置画面刷新的帧率,即每秒内刷新次数(帧画面),数字越小跳动越慢
SIZE = WIDTH, HEIGHT = 640, 480 # 设置游戏窗口宽和高,3个大写为全局变量
ball_size = [[40,40],[50,50],[60,60]] # 图像缩放的宽和高,3组不同大小
ballNumber = 6 # 设置弹跳球的个数
ballGenerateTime = ballNumber * 90 #初始化控制生成弹跳球间距的计数变量
# 设置弹跳球的x,y轴移动偏移量,列表变量,有多项值供组合选择
ballSpeed = [ 2,5,4,3 ] # 列表变量,选择ball移动速度和方向 **
bossSpeed = 26 # 设置boss图形Rect的x或y轴移动偏移量,表现为移动速度.
choice = 0 # 初始化循环选择列表项的変量

# 使用pygame之前必须用这条命令初始化.
pygame.init() # 初始化pygame游戏引擎
# 创建游戏主窗口surface对象screen,参数size是二元组变量:窗口的宽和高
screen = pygame.display.set_mode(SIZE)
# 设置现显示游戏窗口的标题，可以是说明游戏名称等字符串
pygame.display.set_caption('Intro ball 7')

# 从文件加载2个ball图片,转换成Surface对象,图片字符串文件名可带有文件的路径.
image_1 = pygame.image.load("intro_ball.gif").convert_alpha()
image_2 = pygame.image.load("ball.png").convert_alpha()
ball_image = [image_1,image_2] # 设置球的2个不同图片Surface对象列表
# 用pygame的mixer模块中的Sound类,从文件或缓冲区对象创建新的音效Sound对象
# 字符串中的文件名可带有文件的路径
voice1 = pygame.mixer.Sound('ballVoice.wav') # 球碰窗口边弹回声
voice2 = pygame.mixer.Sound('suction.wav') # 球碰精灵后消失声
# 用Sound类的方法set_volume(n)设置该音效音量大小,
voice1.set_volume(0.5) # voice1音量大小参数n范围0.0---1.0
voice2.set_volume(0.5) # voice2音量大小参数n范围0.0---1.0
ball_voice = [voice1,voice2] # 设置球的2个不同图片音效Sound对象列表
ball_list = [] # 初始化存放弹跳球(Surface对象)列表

# 自创建球子类Ball,它继承的父类是pygame.sprite.Sprite类
class Ball(pygame.sprite.Sprite):
    # 类的专有方法__init__(),调用时自动传入调用实参self
    # image 球的的Surface对象名参数
    # ballSize列表变量参数,ball图像缩放的宽和高
    # position列表变量参数,初始ball位置
    # speed列表变量参数,所绘ball图形Rect的x,y轴移动偏移量,表现为两轴方向移动速度
    # voice音效Sound对象变量参数,当球碰到窗口边被弹回时发碰撞音效声
    def __init__(self, image, ballSize, position,speed ,voice):
        pygame.sprite.Sprite.__init__(self) #让父类的属性与子类Ball关联才能使用
        # 用transform模块的scale方法,将球图片Surface对象缩放到参数ballSize要求大小
        self.ball = pygame.transform.scale(image, ballSize)
        # 获取球图片Surface对象的矩形区域(图像的位置Rect对象)
        self.rect = self.ball.get_rect()
        # 设置球的初始位置
        self.rect.left, self.rect.top = position
        self.speed = speed # 设置球的移动速度和方向 **
        self.voice = voice # 设置球的音效声
        self.size = ballSize # 设置球的大小

    # 定义ball移动(弹跳)方法,移动Rect对象
    def move(self):
        # 调用Rect方法move(x,y),移动Rect对象.  x,y是对应坐标轴移动偏移量
        self.rect = self.rect.move(self.speed)
        # 检测图像的位置Rect对象碰到显示窗口左右边缘,x坐标轴方向
        if self.rect.left < 0 or self.rect.right > WIDTH:
            # 将列表变量第1项值取负后重新赋回,改变移动方向
            self.speed[0] = -self.speed[0]
        # 检测图像的位置Rect对象碰到显示窗口上下边缘,y坐标轴方向
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            # 将列表变量第2项值取负后重新赋回,即改变移动方向
            self.speed[1] = -self.speed[1]

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

# 程序主函数main()
def main():
    global ballNumber,ballGenerateTime,choice # 设置为全局变量

    # 设置窗口颜色(即背景颜色),有关颜色模式详见调色工具color_rgb.py
    windowColor = (0,86,76) # 元组变量, RGB255颜色模式值(还可用列表变量)

    boss = pygame.image.load("mouse.png").convert_alpha()
    # 把bass图片大小缩放到参数要求,第二个参数可是元组或列表变量:图像缩放的宽和高
    boss = pygame.transform.scale(boss, [60, 90])
    # 获取图片Surface对象的矩形区域(图像的位置Rect对象)
    bossRect = boss.get_rect()
    bossRect.center = [WIDTH/2,HEIGHT/2] # 设置boss初始位置在窗口中央

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
        screen.fill(windowColor) # 用fill()方法填充screen对象单一色背景(清屏)

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
                  if bossRect.bottom < HEIGHT: # boss底未超出窗口底就向下移动
                      bossRect.y = bossRect.y+bossSpeed # 增大y轴值
                # 判断用户是否按键盘left arrow 键
                if event.key == pygame.K_LEFT:
                  if bossRect.left > 0: # boss左边未超出窗口左边就向左移动
                      bossRect.x = bossRect.x-bossSpeed # 减小x轴值
                # 判断用户是否按键盘right arrow 键
                if event.key == pygame.K_RIGHT:
                  if bossRect.right < WIDTH: # boss右边未超出窗口右边就向右移动
                      bossRect.x = bossRect.x+bossSpeed # 增大x轴值

        # 调自创建球子类Ball(),按一定间隔生成弹跳球语句块
        if ballNumber > 0 and ballGenerateTime % 90 == 0:
              # 循环选择ball_image列表中2个图片球的的Surface对象名
              image = ball_image[choice % 2]
              # 循环选择ball_size列表中3个球的大小项值,每项值也又是列表
              ballSize = ball_size[choice % 3]
              # 从0到WIDTH-ballSize[0]的数字中
              # 用random模块函数随机生成ball的x轴坐标值
              ball_x = random.randint(0,WIDTH-ballSize[0])
              position = [ball_x, 0] # 初始ball位置,其中y轴坐标=0
              # 循环选择ballSpeed列表中的4个值
              x = ballSpeed[choice % 4] # **
              speed = [x,x] # 组合生成ball移动速度和方向 ** 每次都要独立生成?
              if ball_x > WIDTH/2: # **
                    speed[0] = -speed[0] # 让球是从右边向左边移动 **
              # 循环选择ball_voice列表中的2个值,与球图片对应
              voice = ball_voice[choice % 2] # 此球碰撞音效声
              # 用上边生成的5个参数,调自创建球子类Ball(),生成对应的弹跳球
              ball = Ball(image, ballSize, position,speed, voice)
              # 利用列表方法append()将生成的球对象添加入到ball_list列表中
              ball_list.append(ball)
              # 调整控制变量值
              ballNumber -= 1 #等效ballNumber=ballNumber-1
              choice += 1 # 等效choice=choice+1
        # 调整间隔控制变量值
        if ballGenerateTime > 0: #当ballGenerateTime>0时,每循环一次减1
            ballGenerateTime -= 1

        # 每次主循环用for ..in迭代弹跳球列表,遍历整个ball_list列表
        # 让列表中所有弹跳球(Surface对象)移动并绘制在screen上
        # 与boss发生碰撞的球重新随机从上边生成下落
        for each in ball_list:
            # 调用自创建球子类Ball()中的方法move()移动 (移动Rect对象)
            each.move()
            # 检测并处理弹跳球与bossRect是否碰撞
            # 调自创建检测2个矩形(Rect)是否碰撞函数collision_check()
            if collision_check(each.rect,bossRect):
            #if collision_check(eachBall.rect,bossRect,8,6): # 增加碰撞调整值
                # 当球碰到精灵后被吸入消失时音效声
                pygame.mixer.Sound.play(each.voice)
                # 根据下边对Rect的x,y坐标设置,球从窗口顶部重新落下
                # 用random模块函数随机生成碰撞ball的x轴坐标值
                each.rect.x = random.randint(0,WIDTH-each.size[0])
                each.rect.y = 0 # 碰撞ball的y轴坐标=0
                each.speed[1] = abs(each.speed[1]) # 回到原来正值
                if each.rect.x > WIDTH/2:
                      each.speed[0] = -abs(each.speed[0]) # 让球是从右边向左边移动
                else:
                      each.speed[0] = abs(each.speed[0])
            # 用blit()方法将ball移动后图像,按Rect对象的区域,绘制在screen上
            screen.blit(each.ball,each.rect)

        # 用blit()方法将boss移动后图像,按Rect对象的区域,绘制在screen上
        screen.blit(boss,bossRect)

        # 调pygame的显示控制模块display中的函数,将待显示的Surface对象显示到屏幕上
        # update()无参数吋就完全等效flip(),将完整显示 Surface,更新整个显示器的内容
        pygame.display.update() # 是flip()的优化版本

#程序实际执行起点
if __name__ == "__main__":   # execute only if run as a script
    main()    #从这里开始执行本程序命令,调用程序主函数main()