'''happyBirthday_5.py         对happyBirthday_4.py修改   2022.8.22
本例改写了原继承父类是pygame.sprite.Sprite类的子类Gift(),现类名为Role(),
增加了不同角色的移动方法,将所有图片角色(gift,boss,immortal),
都以不同实参调该类Role(),统一创建为Sprite对象进行处置.
本例用pygame编写的生日祝福,游戏编程最基本的入门结构:
  1.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此游戏程序.
  2.按键盘q或Q键,退出此游戏程序.
  3.图片文件bg1.png, gift1.png, gift2.png, gift3.png, singapore2.jpg,
           hie.png和immortal.png.
    音乐文件Rise03.wav, ballVoice.wav, coin01.wav, suction.wav
           和happyBirthday.mp3.
    字体格式文件ALGER.ttf.
    以上共计13个文件需拷贝到本程序同一目录中,
    或在程序的文件名字符串中指明它磁盘目录路径(修改相关语句)后才能正常运行.
  4.在窗口中由用户按下4个方向(上下左右)键进行精灵(boss)移动,接受下落的礼物.
    接受到礼物则加记1分,如果礼物下落出窗口底部则减记1分.
    当总分到达6分时,将有圣诞老人空降新加坡给你带来祝福.
'''
# 导入所需的模块
import sys # 导入python内置sys模块,调用其对象、类和函数等前加sys.
import random # 导入python内置random模块,调用其对象、类和函数等前加random.
import pygame # 导入pygame模块,调用其对象、类和函数等前加pygame.

FPS = 60 # 设置画面刷新的帧率,即每秒内刷新次数(帧画面),数字越小跳动越慢
SIZE = WIDTH, HEIGHT = 800, 600 # 设置游戏窗口宽和高,3个大写为全局常量
# 设置gift图形的Rect 2组y轴移动偏移量,表现为gift落下的2个不同速度
giftSpeed = [ 2,1 ] # 列表变量,在生成实参时进行组合
bossSpeed = 26 # 设置boss图形Rect的x或y轴移动偏移量,表现为移动速度
# 设置immortal图形Rect的移动偏移量x=2 y=0,表现为左右移动速度
immortalSpeed = [2,0] # 列表变量
# 设置字体text2的Rect移动偏移量x=-3,y=0 表现为x轴方向从右向左移动
text2Speed = [-3,0] # 列表变量

giftNumber = 3 # 设置gift的个数
gift_size = [[80,80],[70,70]] # gift图像缩放的宽和高,2组不同大小
giftGenerateTime = giftNumber * 60 #初始化控制生成gift间距的计数变量
choice = 0 # 初始化循环选择列表项的変量

# 自创建退出游戏程序函数
def doExit():
    pygame.quit() # 卸载所有pygame模块
    sys.exit() # 终止程序，退出游戏主循环,关闭游戏窗口

# 自创建将游戏得分数转变成可显示的surface对象函数
# 参数font是字体对象(Font object)变量,参数x是数字变量
def showScore(font,x):
      # 用字符串类的 format() 方法进行复杂变量替换和值格式化
      # 将得分数x转化成字符串
      characterString = "Score: {} ".format(x)
      if x < 0:
            color = (255,0,0) # 当数字为负数时字体显示为红色
      else:
            color = (18,255,88) # 当数字为正数时字体显示颜色
      # 用Font类的render()方法将字串创建成可显示的文本Surface对象
      # render()第一个参数:文本内容字符串,第二个参数:字体是否平滑,
      # 第三个参数:字体颜色值,第四个参数:背景颜色值(省略则是透明).
      text = font.render(characterString,True,color) # text是Surface对象
      return text # 返回显示得分数x的Surface对象

# 自创建类角色Role,它继承的父类是pygame.sprite.Sprite类,
class Role(pygame.sprite.Sprite):
    # 类的专有方法__init__(),调用时自动传入调用实参self
    # image 的Surface对象名参数
    # roleSize列表变量参数,角色图像缩放的宽和高
    # position列表变量参数,初始角色位置
    # speed列表变量参数,所绘角色图形Rect的x,y轴移动偏移量,默认值为无
    # voice音效Sound对象变量参数,当角色因某事件时发出的音效声,默认值为无
    def __init__(self, image, roleSize, position,speed=None ,voice=None):
        pygame.sprite.Sprite.__init__(self) #让父类的属性与子类Role关联才能使用
        # 角色图片Surface对象缩放到参数roleSize要求大小
        self.role = pygame.transform.scale(image, roleSize)
        # 获取角色图片Surface对象的矩形区域(图像的位置Rect对象)
        self.rect = self.role.get_rect()
        # 设置角色的初始位置
        self.rect.left, self.rect.top = position
        self.speed = speed # 设置角色的移动速度和方向,列表变量 **
        self.voice = voice # 设置角色的音效声
        #self.size = roleSize # 设置角色的宽和高,列表变量

    # 定义gift移动(落下)方法,移动Sprite对象
    def gift_move(self):
        global score,text1,text1Rect #设置为全局变量,以便在调用函数中传递数据
        # 调用Rect方法move(x,y),移动Rect对象.  x,y是对应坐标轴移动偏移量
        self.rect = self.rect.move(self.speed)

        # 检测gift图像的位置Rect对象下落出显示窗口底边缘,y坐标轴方向
        if self.rect.top >= HEIGHT:
            pygame.mixer.Sound.play(self.voice) # gift落出窗口扣分声效
            score -= 1 # 记分变量减1分,等效score=score-1
            # 调自创建函数将游戏得分数score转变成可显示的surface对象text1
            text1 = showScore(fon1,score)
            text1Rect =text1.get_rect() # textRect1是text1的Rect对象
            # 对gift图像的位置Rect重新赋值,重新随机从窗口顶部落下
            self.rect.x = random.randint(0,WIDTH-100) #从0到width-100中随机生成x
            self.rect.bottom = 0 # 设置y坐标

    # 定义immortal左右移动方法,移动Sprite对象
    def immor_move(self):
        # 调用Rect方法move(x,y),移动Rect对象  x,y是对应坐标轴移动偏移量
        self.rect = self.rect.move(self.speed) # 圣诞老人移动
        # 检测Immortal图像的位置碰到显示窗口左右边缘,x坐标轴方向
        if self.rect.left < 0 or self.rect.right > WIDTH:
          # 将列表变量第1项值取负后重新赋回,改变x坐标轴移动方向
          self.speed[0] = -self.speed[0]

# 使用pygame之前必须用这条命令初始化.
pygame.init() # 初始化pygame游戏引擎

# 创建游戏主窗口surface对象screen,参数size是二元组变量:窗口的宽和高
screen = pygame.display.set_mode(SIZE)
# 设置现显示游戏窗口的标题，可以是说明游戏名称等字符串
pygame.display.set_caption('Happy Birthday 2022.7.7')

# 从文件加载2个窗口背景图片,转换成Surface对象,图片字符串文件名可带有文件的路径.
bg1 = pygame.image.load("bg1.png").convert()
bg2 = pygame.image.load("singapore2.jpg").convert()
# 2个背景图片Surface对象大小缩放到与游戏窗口screen大小
bg1 = pygame.transform.scale(bg1, (SIZE))
bg2 = pygame.transform.scale(bg2, (SIZE))

# 从文件加载3个gift图片,转换成Surface对象,图片字符串文件名可带有文件的路径.
image_1 = pygame.image.load("gift1.png").convert_alpha()
image_2 = pygame.image.load("gift2.png").convert_alpha()
image_3 = pygame.image.load("gift3.png").convert_alpha()
# 设置3个不同gift图片Surface对象列表
gift_image = [image_1,image_2,image_3]
# 初始化存放gift(Sprite对象)列表
gift_list = []
# 用pygame的mixer模块中的Sound类,从文件或缓冲区对象创建新的音效Sound对象
# 字符串中的文件名可带有文件的路径,gift落出窗口扣分声效
voice1 = pygame.mixer.Sound('ballVoice.wav') # 音效Sound对象1
voice2 = pygame.mixer.Sound('coin01.wav') # 音效Sound对象2
voice3 = pygame.mixer.Sound('suction.wav') # 音效Sound对象3
# 用Sound类的方法set_volume(n)设置该音效音量大小,
voice1.set_volume(0.4) # voice1音量大小参数n范围0.0---1.0
voice2.set_volume(0.7) # voice2音量大小参数n范围0.0---1.0
voice3.set_volume(0.5) # voice2音量大小参数n范围0.0---1.0
gift_voice = [voice1,voice2,voice3] # 设置3个不同图片音效Sound对象列表

# 从文件加载boss图片,转换成Surface对象,图片字符串文件名可带有文件的路径.
image_0 = pygame.image.load("hie.png").convert_alpha()
# 用pygame的mixer模块中的Sound类,从文件或缓冲区对象创建新的音效Sound对象
voice0 = pygame.mixer.Sound('Rise03.wav') # 用于boss碰gift后消失声
# 设置boss初始位置在窗口中央
bossPosition = [WIDTH/2,HEIGHT/2]
# 调自创建子类Role(),生成对应的boss实例,Sprite对象,
# 因无speed实参传递(移动方式不同),故最后的实参要以voice=voice0方式传递
boss = Role(image_0, [80, 120], bossPosition, voice=voice0)

# 从文件加载immortal图片,转换成Surface对象,图片字符串文件名可带有文件的路径
image_4 = pygame.image.load("immortal.png").convert_alpha()
immortalPosition = [0 , 60] # 设置immortal初始坐标位置
immortalSize = [290 , 473] # 设置immortal初始图像缩放的宽和高
# 调自创建子类Role(),生成immortal实例,Sprite对象,无voice实参传递
immortal = Role(image_4, immortalSize, immortalPosition,immortalSpeed)

# 用pygame中的music模块(控制音频流)加入游戏背景音乐
  # 从文件加载背景音乐,字符串中的文件名可带有文件的路径
pygame.mixer.music.load('happyBirthday.mp3')
  # 设置音量大小,音量大小参数范围0.0---1.0
pygame.mixer.music.set_volume(0.5)
# 用font模块Font类,从磁盘文件创建新的字体对象(Font object)
# 从pygame系统中选字体,参数30是指字体大小
fon1 = pygame.font.SysFont('candara', 30, bold=False, italic=False)
# 从同目录中自带字体格式文件(*.ttf)中选字体
fon2 = pygame.font.Font('ALGER.ttf',60) # 参数60是指字体大小
score = 0 # 初始化计算收到礼物数(数字变量)
# 调自创建函数将游戏得分数score转变成可显示的Surface对象text1
text1 = showScore(fon1,score)
text = "Hi YiChen.    Happy birthday!    Grandpa and grandma love you!"
# 用Font类的render()方法创建文本text的Surface对象text2
text2 = fon2.render(text,True,'pink')
# 获取文本图片Surface对象的矩形区域(文本图像的位置Rect对象)
text1Rect =text1.get_rect() # textRect1是text1的Rect对象
text2Rect =text2.get_rect() # textRect2是text2的Rect对象
# 用Rect对象具有的多个虚拟属性center,left....设置显示Rect对象初始位置
text1Rect.x = 6 # 设置显示text1初始x轴坐标
text1Rect.y = 6 # 设置显示text1初始y轴坐标
text2Rect.left = WIDTH # 设置显示text2初始left边,x轴坐标
text2Rect.bottom = 200 # 设置显示text2初始bottom边,y轴坐标

# create an object to help track time
clock = pygame.time.Clock()  # 设置pygame时钟对象

# 游戏主循环 1
game_on = True # 只有当 game_on = False才会退出循环1
while game_on:
    clock.tick(FPS)  # 用时钟对象控制每秒执行FPS次(帧画面刷新)
    screen.blit(bg1, (0,0)) # 参数0,0是背景图bg1与窗口重叠,(效果是清屏)

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
            # 用户按下4个方向键,直接改变boss的Rect对象x或y轴坐标值,让它在窗口中移动
            # 判断用户是否按键盘up arrow 键
            if event.key == pygame.K_UP:
              if boss.rect.top > 0: # boss顶未超出窗口就向上移动bossSpeed变量值
                  boss.rect.y = boss.rect.y-bossSpeed # 减小y轴值
            # 判断用户是否按键盘down arrow 键
            if event.key == pygame.K_DOWN:
              if boss.rect.bottom < HEIGHT: # boss底未超出窗口底就向下移动
                  boss.rect.y = boss.rect.y+bossSpeed # 增大y轴值
            # 判断用户是否按键盘left arrow 键
            if event.key == pygame.K_LEFT:
              if boss.rect.left > 0: # boss左边未超出窗口左边就向左移动
                  boss.rect.x = boss.rect.x-bossSpeed # 减小x轴值
            # 判断用户是否按键盘right arrow 键
            if event.key == pygame.K_RIGHT:
              if boss.rect.right < WIDTH: # boss右边未超出窗口右边就向右移动
                  boss.rect.x = boss.rect.x+bossSpeed # 增大x轴值

    # 调自创建类Role,按一定时间间隔生成礼物语句块
    if giftNumber > 0 and giftGenerateTime % 60 == 0:
          # 循环选择gift_image列表中3个图片的Surface对象名
          image = gift_image[choice % 3]
          # 循环选择gift_size列表中2个gift的大小项值,每项值也又是列表
          giftSize = gift_size[choice % 2]
          # 从0到WIDTH-giftSize[0]的数字中
          # 用random模块函数随机生成gift的x轴坐标值
          gift_x = random.randint(0,WIDTH-giftSize[0])
          position = [gift_x, 0] # 初始gift位置,其中y轴坐标=0
          # 循环选择giftSpeed列表中的2个值
          y = giftSpeed[choice % 2] # **
          speed = [0,y] # 组合生成gift下落速度 **
          # 循环选择gift_voice列表中的3个值,与gift图片对应
          voice = gift_voice[choice % 3] # 此gift落出窗口扣分声效
          # 用上边生成的5个参数,调自创建子类Role(),生成对应的礼物,Sprite对象
          gift = Role(image, giftSize, position, speed, voice)
          # 利用列表方法append()将生成的对象添加入到gift_list列表中
          gift_list.append(gift)
          # 调整控制变量值
          giftNumber -= 1 #等效giftNumber=giftNumber-1
          choice += 1 # 等效choice=choice+1
    # 调整间隔控制变量值
    if giftGenerateTime > 0: #当giftGenerateTime>0时,每循环一次减1
        giftGenerateTime -= 1

    # 每次主循环用for ..in迭代gift列表,遍历整个列表
    # 完成:1.礼物落下,gift落出窗口扣分 2.处理gift与boss是否碰撞,与boss发生
    # 碰撞的gift重新随机从上边生成下落,加1分 3.区域清屏重画gift
    for each in gift_list:
        # 1.调用自创建类Role()中的方法gift_move()移动 (移动Sprite对象)
        each.gift_move()

        # 2.检测并处理2个Sprite对象gift,boss是否碰撞
        if pygame.sprite.collide_rect(each,boss):
              # 当gift碰到boss后被吸入消失时音效声
              pygame.mixer.Sound.play(boss.voice)
              # 根据下边对Rect的x,y坐标设置,gift从窗口顶部重新落下
              each.rect.x = random.randint(0,WIDTH-100) #从0到width-100中随机生成x
              each.rect.bottom = 0 # 设置y坐标
              if each.speed[1] < 6: # 当下落(y)速度低于6时,增加0.5
                  each.speed[1] = each.speed[1] + 0.1
              score += 1 # 记分变量加1分,等效score=score+1
              # 调自创建函数将游戏得分数score转变成可显示的surface对象text1
              text1 = showScore(fon1,score)
              if score >= 6: # 如得分到达6分则退出本循环 1
                    game_on = False

        # 3.对列表遍历的(每个)gift用blit()方法按Rect对象的区域,绘制在screen上
        screen.blit(each.role,each.rect)

    # 用Surface的blit()方法处理图像(Surface对象),绘制在screen上
    screen.blit(boss.role,boss.rect) # 移动后的boss绘制在screen上
    screen.blit(text1,text1Rect) # 此文本不移动,在左上角原位重写

    # 调pygame的显示控制模块display中的update()函数,刷新显示到屏幕上
    pygame.display.update() # 无参数吋就完全等效flip()

# 换背景和播音乐,第2部份生日祝福开始
# 开始播放背景音乐,整数字参数n系播放循环次数(n+1),-1是一直循环播放
pygame.mixer.music.play(-1)
# 游戏主循环 2
while True:
    clock.tick(FPS)  # 用时钟对象控制每秒执行FPS次(帧画面刷新)
    screen.blit(bg2, (0,0)) # 参数0,0是背景图bg2与窗口重叠,(效果是清屏)

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

    # 调用自创建类角色Role()中的方法immor_move()移动immortal圣诞老人
    immortal.immor_move() # immortal是Sprite对象
    text2Rect = text2Rect.move(text2Speed) # 生日祝福文字移动

    # 检测文本图像的位置Rect对象的右边碰到显示窗口左边缘(x坐标轴方向)
    if text2Rect.right <= 0 :
          text2Rect.left = WIDTH # 将对应的位置Rect对象x值设回起点坐标
    # 用Surface的blit()方法处理图像(Surface对象),绘制在screen上
    screen.blit(immortal.role,immortal.rect)
    screen.blit(text2,text2Rect)
    # 调pygame的显示控制模块display中的update()函数,刷新显示到屏幕上
    pygame.display.update() # 无参数吋就完全等效flip()