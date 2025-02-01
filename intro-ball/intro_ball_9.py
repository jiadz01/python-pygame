'''intro_ball_9.py 弹跳的球9  对intro_ball_8.py扩展修改    2022.7.28
两个球之间碰撞则改变它们弹跳方向.
本例用sprite模块的spritecollide()方法检测某个精灵是否与指定的组group中的其它精灵
发生碰撞,调用时有四个参数:被测精灵,  精灵组, 是否删除发生碰撞精灵,  回调函数.
用回调函数pygame.sprite.collide_circle()专门用于检测两个圆之间是否发生碰撞.
详见pygame文档sprite模块的spritecollide()方法说明部份.
自创建Sprite类的子类Ball(),可生成许多不同图形,不同大小和不同移动速度的弹跳球实例.
在该类属性中增加:利用列表方法append()将生成的球对象添加入到ball_list列表中.
注意:只能按本例方式调用类Ball()生成各个球的self.speed值,
     否则程序运行出现异常(bug?),这些语句后边#标注有**
自创建退出游戏程序函数doExit().
本例用Rect模块中的colliderect()方法来检测球与bass是否碰撞(有重叠发生).
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
pygame.display.set_caption('Intro ball 9')

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
# 用sprite模块的Group()类创建一个sprite对象的管理容器group
group = pygame.sprite.Group() # 检测精灵碰撞时调用
rectangle_list = [] # 初始化存放更新部份显示区域(Rect对象)列表

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
        self.speed = speed # 设置球的移动速度和方向,列表变量 **
        self.voice = voice # 设置球的音效声
        self.size = ballSize # 设置球的宽和高,列表变量
        self.old_rect = self.rect # 初始化保留球移动前的位置
        # 设置该ball的半径值,供collide_circle(left,right)函数自动调入
        self.radius = self.rect.width / 2

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

    # 初始化游戏窗口屏幕显示
    screen.fill(windowColor) # 用fill()方法填充screen对象单一色背景
    # 调pygame的显示控制模块display中的函数将图绘制在游戏窗口screen
    pygame.display.update() # 无参数吋就完全等效flip()

    # 用pygame中的music模块(控制音频流)加入游戏背景音乐
      # 从文件加载背景音乐,字符串中的文件名可带有文件的路径
    pygame.mixer.music.load('home.wav')
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
              speed = [x,x] # 组合生成ball移动速度和方向 **
              if ball_x > WIDTH/2: # **
                    speed[0] = -speed[0] # 让球是从右边向左边移动 **
              # 循环选择ball_voice列表中的2个值,与球图片对应
              voice = ball_voice[choice % 2] # 此球碰撞音效声
              # 用上边生成的5个参数,调自创建球子类Ball(),生成对应的弹跳球
              ball = Ball(image, ballSize, position,speed, voice)
              # 利用列表方法append()将生成的球对象添加入到ball_list列表中
              ball_list.append(ball)
              # 利用Group的add()方法,将生的糈灵ball加入容器
              group.add(ball)
              # 调整控制变量值
              ballNumber -= 1 #等效ballNumber=ballNumber-1
              choice += 1 # 等效choice=choice+1
        # 调整间隔控制变量值
        if ballGenerateTime > 0: #当ballGenerateTime>0时,每循环一次减1
            ballGenerateTime -= 1

        # 每次主循环用for ..in迭代弹跳球列表,遍历整个列表
        # 完成:1.移动弹跳球 2.处理球之间是否碰撞 3.处理弹跳球与boss是否碰撞
        # 与boss发生碰撞的球重新随机从上边生成下落 4.区域清屏重画
        for each in ball_list:
            # 1.调用自创建球子类Ball()中的方法move()移动 (移动Rect对象)
            each.move()

            # 2.用sprite模块的spritecollide()方法检测弹跳球之间是否碰撞
            # 如碰撞则改变弹跳球方向,collide_circle检测两个圆之间是否发生碰撞回调函数
            # 用for ..in遍历整个group(sprite对象,管理容器)
            group.remove(each) # 用remove()方法暂时从容器移出待测试碰撞球
            # 将待测试球与容器中的其它球进行测试是否有碰撞
            if pygame.sprite.spritecollide(each, group, False, pygame.sprite.collide_circle):
                if each.rect.left > 0 and each.rect.right < WIDTH:
                    each.speed[0] = -each.speed[0]
                if each.rect.top > 0 and each.rect.bottom < HEIGHT:
                    each.speed[1] = -each.speed[1]
                # 防止两个碰撞球粘贴在窗口顶部线
                if each.rect.top <= 0 : # 将符合此条件球改变x轴坐标值
                  while pygame.sprite.spritecollide(each, group, False,
                                                    pygame.sprite.collide_circle):
                      # 重新设置随机ball的x轴坐标值,不发生碰撞退出while循环
                      each.rect.x = random.randint(0,WIDTH-each.size[0])
            group.add(each) # 用add()方法将上边暂时从容器移出待测试球,加回group

            # 3.检测并处理弹跳球与boss是否碰撞(有重叠发生)
            # 用Rect模块中的colliderect()方法来检测是否碰撞
            if each.rect.colliderect(bossRect):
                # 当球碰到精灵后被吸入消失时音效声
                pygame.mixer.Sound.play(each.voice)
                # 根据下边对Rect的x,y坐标设置,球从窗口顶部重新落下
                # 用random模块函数随机生成碰撞ball的x轴坐标值
                each.rect.x = random.randint(0,WIDTH-each.size[0])
                each.rect.y = 0 # 碰撞ball的y轴坐标=0
                # 判定新落下位置不能有与其它球发生碰撞(两球粘在一起而抖动)
                group.remove(each) # 用remove()方法暂时从容器移出待测试碰撞球
                while pygame.sprite.spritecollide(each, group, False,
                                                  pygame.sprite.collide_circle):
                    # 重新设置随机ball的x轴坐标值,不发生碰撞退出while循环
                    each.rect.x = random.randint(0,WIDTH-each.size[0])
                group.add(each) # 用add()方法将上边暂时从容器移出待测试球,加回group
                each.speed[1] = abs(each.speed[1]) # 回到原来正值
                if each.rect.x > WIDTH/2: # 如果球将从顶部右边落下时
                    each.speed[0] = -abs(each.speed[0]) # 让球是从右边向左边移动
                else:
                    each.speed[0] = abs(each.speed[0])

            # 4.对列表遍历的(每个)球进行清屏重画和将变化的rect添加到参数列表
             # 原球位置区域填充单一色背景(清屏)
            screen.fill(windowColor,each.old_rect)
             # 用blit()方法将ball移动后图像,按Rect对象的区域,绘制在screen上
            screen.blit(each.ball,each.rect)
             # 将更新部份显示区域(Rect对象)添加入rectangle_list列表
            rectangle_list.append(each.old_rect)
            rectangle_list.append(each.rect)
             # 保留球移动的位置,将是下次移动前位置
            each.old_rect = each.rect

        # 用Surface的方法处理boss图像(Surface对象)
          # 用fill()方法将在screen上boss原位置区域填充单一色背景(清屏)
        screen.fill(windowColor,old_bossRect)
          # 用blit()方法将bass移动后图像,按Rect对象的区域,绘制在screen上
        screen.blit(boss,bossRect)
        # 将更新部份显示区域(Rect对象)添加入rectangle_list列表
        rectangle_list.append(old_bossRect)
        rectangle_list.append(bossRect)
        # 因处理移动方法不同,将已移动boss的Rect对象拷贝,以便再移动时擦除旧图片
        old_bossRect = bossRect.copy() # 用Rect模块中的copy()方法拷贝

        # 调pygame的显示控制模块display中的update()函数,参数用列表方式传递每一帧图片
        # 变化的区域(Rect对象),将只对变动的Surface区域进行刷新显示到屏幕上
        pygame.display.update(rectangle_list)
        # 用列表方法clear()将列表中的全部元素删除,为下一帧画面刷新作好准备
        rectangle_list.clear()

#程序实际执行起点
if __name__ == "__main__":   # execute only if run as a script
    main()    #从这里开始执行本程序命令,调用程序主函数main()