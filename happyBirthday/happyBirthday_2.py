'''happyBirthday_2.py         对happyBirthday_1.py扩展修改   2022.7.9
自创建将游戏得分数转变成可显示的surface对象函数showScore(),让程序便于维护
本例用pygame编写的生日祝福,游戏编程最基本的入门结构:
  1.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此游戏程序.
  2.按键盘q或Q键,退出此游戏程序.
  3.图片文件bg1.png, gift1.png, singapore2.jpg, hie.png和immortal.png.
    音乐文件Rise03.wav, ballVoice.wav和happyBirthday.mp3.
    字体格式文件ALGER.ttf.
    以上共计9个文件需拷贝到本程序同一目录中,
    或在程序的文件名字符串中指明它磁盘目录路径后才能正常运行.
  4.在窗口中由用户按下4个方向(上下左右)键进行精灵(boss)移动,接受下落的礼物.
    接受到礼物则加记1分,如果礼物下落出窗口底部则减记1分.
    当总分到达6分时,将有圣诞老人空降新加坡给你带来祝福.
'''
# 导入所需的模块
import sys # 导入python内置sys模块,调用其对象、类和函数等前加sys.
import random # 导入python内置random模块,调用其对象、类和函数等前加random.
import pygame # 导入pygame模块,调用其对象、类和函数等前加pygame.

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

# 使用pygame之前必须用这条命令初始化.
pygame.init() # 初始化pygame游戏引擎

FPS = 60 # 设置画面刷新的帧率,即每秒内刷新次数(帧画面),数字越小跳动越慢
size = width, height = 800, 600 # 设置游戏窗口宽和高,及对应的3个变量
giftSpeed = [ 0,2 ] # 列表变量,设置所绘图形Rect的y轴移动偏移量,表现为gift向下移动速度
bossSpeed = 26 # 设置boss图形Rect的x或y轴移动偏移量,表现为移动速度.
immortalSpeed = [2,0] # 列表变量,设置所绘图形Rect的x轴移动偏移量,表现为左右移动速度
text2Speed = [-3,0] # 列表变量,设置字体Rect的y=0,x轴移动偏移量,表现为x轴方向移动速度
# 创建游戏主窗口surface对象screen,参数size是二元组变量:窗口的宽和高
screen = pygame.display.set_mode(size)
# 设置现显示游戏窗口的标题，可以是说明游戏名称等字符串
pygame.display.set_caption('Happy Birthday 2022.7.7')

# 从文件加载2个窗口背景图片,转换成Surface对象,图片字符串文件名可带有文件的路径.
bg1 = pygame.image.load("bg1.png").convert()
bg2 = pygame.image.load("singapore2.jpg").convert()
# 2个背景图片Surface对象大小缩放到与游戏窗口screen大小
bg1 = pygame.transform.scale(bg1, (size))
bg2 = pygame.transform.scale(bg2, (size))

# 从文件加载3个图片,转换成Surface对象,图片字符串文件名可带有文件的路径.
gift = pygame.image.load("gift1.png").convert_alpha()
boss = pygame.image.load("hie.png").convert_alpha()
immortal = pygame.image.load("immortal.png").convert_alpha()
# 把2个图片大小缩放到参数要求,第二个参数可是元组或列表变量:图像缩放的宽和高
gift = pygame.transform.scale(gift, [80, 80])
boss = pygame.transform.scale(boss, [80, 120])
# 获取图片Surface对象的矩形区域(图像的位置Rect对象)
giftRect = gift.get_rect()
bossRect = boss.get_rect()
immortalRect = immortal.get_rect()
# 设置gift初始位置
giftRect.x = random.randint(0,width-100) #从0到width-100中随机生成x
giftRect.y = 0
# 设置boss初始位置在窗口中央
bossRect.center = [width/2,height/2]
# 设置immortal初始坐标位置
immortalRect.left = 0 # 相当是x=0
immortalRect.top = 60 # 相当是y=60
# 用blit()方法将图片Surface对象绘制在screen上
screen.blit(bg1, (0,0)) # 参数0,0是背景图bg1与窗口重叠
# 调pygame的显示控制模块display中的函数将图绘制在游戏窗口screen
pygame.display.update() # 无参数吋就完全等效flip()

# 用pygame的mixer模块中的Sound类,从文件或缓冲区对象创建新的音效Sound对象
# 字符串中的文件名可带有文件的路径
voice1 = pygame.mixer.Sound('Rise03.wav') # gigt碰精灵后消失声
voice2 = pygame.mixer.Sound('ballVoice.wav') # gift落出窗口扣分声效
# 用Sound类的方法set_volume(n)设置该音效音量大小,
voice1.set_volume(0.8) # 音量大小参数n范围0.0---1.0
voice2.set_volume(0.6) # 音量大小参数n范围0.0---1.0

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
text1Rect.x = 6 # 设置显示text初始x轴坐标
text1Rect.y = 6 # 设置显示text初始y轴坐标
text2Rect.left = width # 设置显示text2初始left边,x轴坐标
text2Rect.bottom = 200 # 设置显示text2初始bottom边,y轴坐标
# 因处理移动方法不同,将boss的Rect对象拷贝,以便boss移动时擦除旧图片
old_bossRect = bossRect.copy() # old_bossRect是Rect对象

# create an object to help track time
clock = pygame.time.Clock()  # 设置pygame时钟对象

# 游戏主循环 1
game_on = True # 只有当 game_on = False才会退出循环1
while game_on:
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
    # 调用Rect方法move(x,y),移动Rect对象gift.  x,y是对应坐标轴移动偏移量
    newGiftRect = giftRect.move(giftSpeed)

    # 检测gift图像的位置Rect对象下落出显示窗口底边缘,y坐标轴方向
    if newGiftRect.top >= height:
        pygame.mixer.Sound.play(voice2) # gift落出窗口扣分声效
        score -= 1 # 记分变量减1分,等效score=score-1
        # 调自创建函数将游戏得分数score转变成可显示的surface对象text1
        text1 = showScore(fon1,score)
        # 对gift图像的位置Rect重新赋值,重新随机从窗口顶部落下
        newGiftRect.x = random.randint(0,width-100) #从0到width-100中随机生成x
        newGiftRect.bottom = 0 # 设置y坐标

    # 检测并处理2个Rect对象gift,boss是否碰撞
    # 用Rect模块中的colliderect()方法来检测是否有重叠发生
    if newGiftRect.colliderect(bossRect):
          # 当gift碰到boss后被吸入消失时音效声
          pygame.mixer.Sound.play(voice1)
          # 根据下边对Rect的x,y坐标设置,gift从窗口顶部重新落下
          newGiftRect.x = random.randint(0,width-100) #从0到width-100中随机生成x
          newGiftRect.bottom = 0 # 设置y坐标
          if giftSpeed[1] < 6: # 当下落(y)速度低于6时,增加0.5
              giftSpeed[1] = giftSpeed[1] + 0.5
          score += 1 # 记分变量加1分,等效score=score+1
          # 调自创建函数将游戏得分数score转变成可显示的surface对象text1
          text1 = showScore(fon1,score)
          if score >= 6: # 如得分到达6分则退出本循环 1
                game_on = False

    # 用Surface的方法处理图像(Surface对象)
      # 用blit()方法重新绘制背景指定区域，等同于擦除变动的旧图片效果
      # 下边3个Rect对象参数,前个是指区域(取位置左上角坐标),后个是指定图片对象范围
    screen.blit(bg1,giftRect,giftRect)
    screen.blit(bg1,old_bossRect,old_bossRect)
    screen.blit(bg1,text1Rect,text1Rect)
      # 用blit()方法将移动后图像,按Rect对象的区域,绘制在screen上
    screen.blit(gift,newGiftRect)
    screen.blit(boss,bossRect)
    screen.blit(text1,text1Rect) # 此文本不移动,在左上角原位重写

    # 调pygame的显示控制模块display中的update()函数,参数用列表方式传递每一帧图片
    # 变化的区域(Rect对象),将只对变动的Surface区域进行刷新显示到屏幕上
    pygame.display.update([giftRect,newGiftRect,old_bossRect,bossRect,text1Rect])

    giftRect = newGiftRect # 将已移动gift的Rect存入变量,以便再移动时擦除旧图片
    # 因处理移动方法不同,将已移动boss的Rect对象拷贝,以便再移动时擦除旧图片
    old_bossRect = bossRect.copy() # 用Rect模块中的copy()方法拷贝

# 换背景和播音乐,第2部份生日祝福开始
screen.blit(bg2, (0,0)) # 参数0,0是背景图bg2与窗口重叠
pygame.display.update() # 无参数吋就完全等效flip()
# 开始播放背景音乐,整数字参数n系播放循环次数(n+1),-1是一直循环播放
pygame.mixer.music.play(-1)
# 游戏主循环 2
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
    # 调用Rect方法move(x,y),移动Rect对象  x,y是对应坐标轴移动偏移量
    newImmortalRect = immortalRect.move(immortalSpeed) # 圣诞老人移动
    newText2Rect = text2Rect.move(text2Speed) # 生日祝福文字移动

    # 检测Immortal图像的位置碰到显示窗口左右边缘,x坐标轴方向
    if newImmortalRect.left < 0 or newImmortalRect.right > width:
        # 将列表变量第1项值取负后重新赋回,改变x坐标轴移动方向
        immortalSpeed[0] = -immortalSpeed[0]
    # 检测文本图像的位置Rect对象的右边碰到显示窗口左边缘(x坐标轴方向)
    if newText2Rect.right <= 0 :
          newText2Rect.left = width # 将对应的位置Rect对象x值设回起点坐标
    # 用Surface的方法处理图像(Surface对象)
      # 用blit()方法重新绘制背景指定区域，等同于擦除变动的旧图片效果
      # 下边2个Rect对象参数,前个是指区域(取位置左上角坐标),后个是指定图片对象范围
    screen.blit(bg2,immortalRect,immortalRect)
    screen.blit(bg2,text2Rect,text2Rect)
      # 用blit()方法将移动后图像,按Rect对象的区域,绘制在screen上
    screen.blit(immortal,newImmortalRect)
    screen.blit(text2,newText2Rect)

    # 调pygame的显示控制模块display中的update()函数,参数用列表方式传递每一帧图片
    # 变化的区域(Rect对象),将只对变动的Surface区域进行刷新显示到屏幕上
    pygame.display.update([immortalRect,newImmortalRect,text2Rect,newText2Rect])

    immortalRect = newImmortalRect # 将已移动的Rect存入变量,以便再移动时擦除旧图片
    text2Rect = newText2Rect # 将已移动text的Rect存入变量,以便再移动时擦除旧图片