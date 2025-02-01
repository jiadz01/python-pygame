''' overlap_2.py   mask的精准碰撞检测示范程序2  对overlap_1.py修改  2022.10.10
本例用自创建类角色Role(),类Role()它继承的父类是pygame.sprite.Sprite类,
注意与overlap_1.py语句对照,可更好理解类和面向对象编程技术.
本例用Pygame中处理图形遮罩(位掩码,掩膜)的模块mask,创建记录该角色Surface对象的透明点
和不透明点的 mask对象,用模块mask类的overlap(other, offset)方法,实现精确到1个像素级
别的的碰撞检测,原理是测试两个子画面之间的位掩码(掩膜)是否重叠.
或用pygame.mask.from_threshold()确定某颜色的部份图形实现碰撞,(可将下边语句后 # 注
释带 * 的语句第二个参数值 3 改为 4 ),此时颜色参数必须是RGB255颜色模式值.
通过本例运行并与程序语句对照,可更好理解这种精准碰撞检测方法,学习编程技术.
1.用鼠标移动蓝色小球去碰撞红色箭头,在窗口标题栏将显示碰撞参数值,窗口背色也会发生改变.
2.如果发生碰撞,则在2个Mask掩码第一个重叠交点坐标位置绘出一个黄色小圆点.
3.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此游戏程序.
4.按键盘q或Q键,退出此游戏程序.
5.程序中的RGB255颜色模式值(元组变量,还可用列表变量),可参考调色工具color_rgb.py
6.调用自创建类Role()时,可将第二个参数改为如下数字以获得各种形状图形:
     0-圆型  1-中空白圆环形  2-三角形  3-箭头形  4-二种颜色箭头形,实现某颜图形碰撞
'''
import pygame # 导入pygame模块,调用其对象、类和函数等前加pygame.

FPS = 60 # 设置画面刷新的帧率,即每秒内刷新次数(帧画面)
width = 640 # 设置游戏窗口宽的变量
height = 480 # 设置游戏窗口高的变量

# 使用pygame之前必须用这条命令初始化.
pygame.init() # 初始化pygame游戏引擎
# 创建游戏主窗口surface对象screen,并设置主屏窗口大小
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()  # 设置pygame时钟对象

# 自创建类角色Role,它继承的父类是pygame.sprite.Sprite类,用来创建各种角色图形
class Role(pygame.sprite.Sprite):
    # 类的专有方法__init__(),调用时自动传入调用实参self
    # size列表变量参数,画角色图像的Surface宽和高
    # position列表变量参数,图像初始位置
    # number整数变量参数,绘制图形的形状: 0-圆型  1-中空白圆环形  2-三角形
    #          3-箭头形  4-充填二种颜色箭头形,实现某颜色color1的部份图形碰撞
    # color1 图像充填的颜色
    # color2 图像充填箭头身体部份(四边形)的颜色,默认值为无
    def __init__(self, size, number, position, color1, color2=None):
        pygame.sprite.Sprite.__init__(self) #让父类的属性与子类Role关联才能使用
        #super().__init__() #让父类的属性与子类Role关联,同上条等效,选其一即可
        # 创建一个roleSize大小用于绘制图形的Surface对象
        self.image = pygame.Surface(size)
        self.image.fill((0,0,0))  # 将这个Surface对象底色充填为黑色
        self.image.set_colorkey((0,0,0)) # 设置Surface对象中颜色(0,0,0)为透明
        if number <= 1: # 绘:0-圆型  1-中空白圆环形
            # 由Surface宽和高最窄幅计算确定圆半径 r
            if size[0] <= size[1]:
                r = size[0]/2
            else:
                r = size[1]/2
            # 确定圆环的环宽
            if number == 1:
                width = int(r/6) # 中空白圆环形的color1色环宽,必须是整数型
            else:
                width = 0 # 整个图形都充填color1色,该参数默认值=0
            # 用绘图模块draw在Surface对象,坐标x=size[0]/2, y=size[1]/2上
            # 画颜色=color1,半径=r的圆形
            pygame.draw.circle(self.image,color1,(size[0]/2,size[1]/2),r,width)
        elif number == 2: # 绘三角形
            # 由Surface宽和高计算确定三角形型三个顶点坐标列表变量p
            p = [(0,size[1]),(size[0],size[1]),(size[0]/2,0)]
            # 用绘图模块draw在Surface对象,以多边形顶点列表变量p,画颜色=color1绘三角形
            pygame.draw.polygon(self.image,color1,p)
        elif number >= 3: # 绘箭头图形
            if color2 == None:
                color = color1 # 箭头箭身同颜色
            else:
                color = color2 # 箭身颜色=color2
            p = [(0,size[1]/2),(size[0],size[1]/2),(size[0]/2,0)]
            # 用绘图模块draw在Surface对象,以多边形顶点列表变量p,画颜色=color1绘三角形
            pygame.draw.polygon(self.image,color1,p)
            # 用绘图模块draw在Surface对象,以多边形顶点列表变量p,画颜色=color1绘四边形
            p = [(size[0]/4,size[1]/2),(size[0]/4,size[1]),
                    (size[0]/4*3,size[1]),(size[0]/4*3,size[1]/2)]
            pygame.draw.polygon(self.image,color,p)
        # 获取角色图片Surface对象的矩形区域(图像的位置Rect对象)
        # 同时center=position设置角色的Rect对象初始位置
        self.rect = self.image.get_rect(center=position)
        # 用Pygame中处理图形遮罩的模块 mask,
        # 创建记录该角色Surface对象的透明点和不透明点的 mask
        if number == 4:
            # 用pygame.mask.from_threshold()创建某颜色color1的部份图形实现碰撞
            # color1此时颜色参数必须是RGB255颜色模式值
            self.mask = pygame.mask.from_threshold(self.image,color1,(1,1,1,255))
        else:
            # 创建图形Surface对象的透明点和不透明点的 mask对象(掩膜)
            self.mask = pygame.mask.from_surface(self.image)

# 调自创建类Role()创建拟静止不动的红色箭头图形实例,red对象
# 可将第二个参数改为:0-圆型 1-中空白圆环形 2-三角形 3-箭头形 4-二种颜色箭头形,实现某颜图形碰撞
red = Role((80,80),3,(width/2,height/2),(255,0,0),(106,28,206)) # *

# 调自创建类Role()创建拟用鼠标移动的蓝色圆形图形实例,blue对象
blue = Role((40,40),0,(0,0),'blue')

# 调自创建类Role()创建显示碰撞点的黄色圆形小点实例,yellow对象
yellow = Role((6,6),0,(0,0),(255,222,126))

# 游戏主循环 game loop
game_on = True # 只有当 game_on = False才会退出循环
while game_on:
    # Pygame处理事件的结构(即事件队列方式，该栈结构遵循遵循“先到先处理”的基本原则)
    # 这个for循环遍历弹出事件语句一定要写，要不事件栈满了之后程序就会卡死
    for event in pygame.event.get(): # 用for循环遍历事件队列,弹出获取并从队列删除
        # 判断用户是否点了"X"关闭按钮,并执行if代码段
        if event.type == pygame.QUIT: # 当用户按下窗口的关闭按钮
            game_on = False
        # 判断用户是否按键盘
        if event.type == pygame.KEYDOWN:
            # 判断用户是否按键盘q或Q键,如果是则退出游戏程序
            if event.key == pygame.K_q:
                game_on = False

    # 用Pygame中mouse模块的pygame.mouse.get_pos()获取鼠标光标位置坐标值
    blue.rect.center = pygame.mouse.get_pos() # 移动蓝色圆形图形到光标位置

    # 用Pygame中处理图形遮罩的模块 mask中类的overlap(other, offset)方法
    # 来检测是否碰撞,offset是一个元组，元组中分别为两个rect的x坐标差值和y坐标差值
    # 注意这两个rect的坐标值在算式中的位置,与命令中的两个mask对应位置相关,
    # 即offset中的被减数和减数次序不能错误,次序不能交换
    offset = red.rect.x -blue.rect.x , red.rect.y - blue.rect.y
    # 返回的point是相对于blueMask的偏移量 (2个Mask掩码第一个重叠交点)
    point = blue.mask.overlap(red.mask,offset) # 无碰撞则返回 None
    if point: # 如发生碰撞
        # 计算第一位碰撞点在显示窗口中的坐标值 coordinate
        coordinate = blue.rect.x + point[0],blue.rect.y + point[1]
        # 将各变量转成字符串(info)供显示
        info = ' Collision point coordinate='+str(coordinate) \
                   +' , point=' + str(point) + ' ,  offset=' + str(offset)
        # 在显示游戏窗口标题栏中，显示碰撞点信息参数
        pygame.display.set_caption(info)
        screen.fill((66,96,118)) # 填充screen对象浅灰蓝色背景 (效果清屏)
    else:
        # 设置显示游戏窗口的标题，可以是说明等字符串
        pygame.display.set_caption('Pygame example: overlap_2.py      ( No collision )')
        screen.fill((16,116,26)) # 填充screen对象绿色背景 (效果清屏)

    # 用blit()方法将图像,按Rect对象的区域,绘制在screen上
    screen.blit(red.image,red.rect) # 绘制红色箭头图形
    screen.blit(blue.image,blue.rect) # 绘制鼠标移动的蓝色圆形图形

    if point != None: # 如发生碰撞,与上一个if语句效果一样
        yellow.rect.center = coordinate # 设置碰撞点的黄色圆形小点坐标位置
        screen.blit(yellow.image,yellow.rect) # 在窗口图像最上层绘制黄色圆形小点

    # 调pygame的显示控制模块display中的update()函数
    pygame.display.update() # 显示 Surface,更新整个显示器的内容
    clock.tick(FPS)  # 用时钟对象控制每秒执行FPS次(帧画面刷新)

pygame.quit() # 卸载所有pygame模块,关闭游戏窗口