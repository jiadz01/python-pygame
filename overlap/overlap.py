''' overlap.py   mask的精准碰撞检测示范程序 对overlap_3.py修改  2022.10.16
本例扩展了自创建类Role(),定义图形移动(上下移动)方法,用它创建了5个不同形状上下移动的图形.
本例用Pygame中的 sprite 模块的 spritecollideany(sprite,group,collided=None )
和 collide_mask(sprite1, sprite2) 命令,实现精确到1个像素级别的的碰撞检测.
通过本例运行并与overlap_1.py,overlap_2.py,overlap_3.py程序语句对照,
可更好理解sprite模块精准碰撞检测方法,学习编程技术.
1.用鼠标移动蓝色小球去碰撞5个不同形状上下移动的图形,在窗口标题栏将显示碰撞参数值,
  窗口背色也会发生改变.
2.如果发生碰撞,则在2个Mask掩码第一个重叠交点坐标位置绘出一个黄色小圆点.
3.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此游戏程序.
4.按键盘q或Q键,退出此游戏程序.
5.程序中的RGB255颜色模式值(元组变量,还可用列表变量),可参考调色工具color_rgb.py
'''
import sys # 导入python内置sys模块,调用其对象、类和函数等前加sys.
import pygame # 导入pygame模块,调用其对象、类和函数等前加pygame.

FPS = 30 # 设置画面刷新的帧率,即每秒内刷新次数(帧画面)
width = 640 # 设置游戏窗口宽的变量
height = 480# 设置游戏窗口高的变量

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
    def __init__(self, size, number, position, color1, color2=None, speed=None):
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
        self.speed = speed # 图形上下移动速度,如果speed=None则此命令不执行
        # 用Pygame中处理图形遮罩的模块 mask,
        # 创建记录该角色Surface对象的透明点和不透明点的 mask
        if number == 4:
            # 用pygame.mask.from_threshold()创建某颜色color1的部份图形实现碰撞
            # color1此时颜色参数必须是RGB255颜色模式值, 或加pygame.Color(color)
            #self.mask = pygame.mask.from_threshold(self.image,pygame.Color(color1),(1,1,1,255))
            self.mask = pygame.mask.from_threshold(self.image,color1,(1,1,1,255))
        else:
            # 创建图形Surface对象的透明点和不透明点的 mask对象(掩膜)
            self.mask = pygame.mask.from_surface(self.image)

    # 定义Role画在游戏窗上(Surface)的方法
    def draw(self,screen):
        screen.blit(self.image,self.rect)

    # 定义图形移动(上下移动)方法,移动Rect对象
    def move(self):
        # 调用Rect方法move(x,y),移动Rect对象.  x,y是对应坐标轴移动偏移量
        self.rect = self.rect.move(self.speed)
        # 检测图像的位置Rect对象碰到显示窗口上下边缘,y坐标轴方向
        if self.rect.top < 0 or self.rect.bottom > height:
            # 将列表变量第2项值取负后重新赋回,即改变移动方向
            self.speed[1] = -self.speed[1]

# 自创建退出游戏程序函数
def doExit():
    pygame.quit() # 卸载所有pygame模块
    sys.exit() # 终止程序，退出游戏主循环,关闭游戏窗口

# 程序主函数main()
def main():
    # 设置拟生成5个静止不动图形实例的参数
    sizes = [(40,40),(70,70),(30,30),(80,80),(80,80)] # 画图像的Surface宽和高,列表变量
    # 据窗口宽的1/6和高的1/3为图形坐标基础值,各图的坐标是它们整倍数,均匀分布在窗口中
    w_x, h_y = width/6, height/3 # w_x是x轴坐标值,h_y是y轴坐标值
    # 设置5个图形坐标值列表
    positions = [(w_x,h_y),(w_x*3,h_y),(w_x*5,h_y),(w_x*2,h_y*2),(w_x*4,h_y*2)]
    color1s = [(0,186,255),'red','green','red',(255,16,18)] # 画图像的颜色值列表
    color2 = (106,28,206) # 箭头箭身颜色
    image_list = [] # 初始化存放5个静止不动的图形实例image(sprite对象)列表
    # 用sprite模块的Group()类创建一个sprite对象的管理容器group
    group = pygame.sprite.Group() # 检测精灵碰撞时调用
    # 利用for循环调自创建类Role()创建生成5个上下移动图形实例
    for n in range(5):
        sp = [0,1] # 设置图形上下移动速度x=0,y=1
        if n >= 3:
            # 调自创建类Role()创建箭头图形实例image
            image = Role(sizes[n], n, positions[n], color1s[n], color2, speed=sp)
        else:
            # 调自创建类Role()创建非箭头外的其它图形实例image
            image = Role(sizes[n], n, positions[n], color1s[n], speed=sp)
        # 利用列表方法append()将生成的图形实例添加入到image_list列表中
        image_list.append(image)
        # 利用Group的add()方法,将生的糈灵对象image加入容器
        group.add(image)

    # 调自创建类Role()创建拟用鼠标移动的蓝色圆形图形实例,blue对象
    blue = Role((40,40),0,(0,0),'blue')

    # 调自创建类Role()创建显示碰撞点的黄色圆形小点实例,yellow对象
    yellow = Role((6,6),0,(0,0),(255,222,126))

    # 游戏主循环 game loop
    while True:
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

        # 用Pygame中mouse模块的pygame.mouse.get_pos()获取鼠标光标位置坐标值
        blue.rect.center = pygame.mouse.get_pos() # 移动蓝色圆形图形到光标位置

        point = None # 设置Mask的偏移量变量=None
        # 用Pygame中sprite模块的spritecollideany(sprite,group,collided=None ) 第3个参数是一个回调函数
        # 首先简单测试子画面sprite是否与组中group的任何项内容重叠相交,重叠返回该项内容，否则返回None
        one = pygame.sprite.spritecollideany(blue,group,pygame.sprite.collide_mask )
        # 如首先简单测有发生碰撞,则获取第一个重叠交点
        if one != None: # 如发生碰撞
            # 用Pygame中sprite模块的collide_mask(sprite1, sprite2),测试两个子画面的位掩码是否重叠
            # 是重叠返回掩模之间的第一个碰撞点(2个Mask掩码第一个重叠交点),否则返回None
            point = pygame.sprite.collide_mask(blue,one) # point元组变量,(int, int)

        if point: # 如发生碰撞,获取第一个重叠交点
            # 计算第一位碰撞点在显示窗口中的坐标值 coordinate (元组变量)
            coordinate = blue.rect.x + point[0], blue.rect.y + point[1]
            # 将各变量转成字符串(info)供显示
            info = ' Collision point coordinate='+str(coordinate) \
                          +' , point=' + str(point)
            # 在显示游戏窗口标题栏中，显示碰撞点信息参数
            pygame.display.set_caption(info)
            screen.fill((66,96,118)) # 填充screen对象浅灰蓝色背景 (效果清屏)
        else:
            # 设置显示游戏窗口的标题，可以是说明等字符串
            pygame.display.set_caption('Pygame example: overlap.py      ( No collision )')
            screen.fill((16,116,26)) # 填充screen对象绿色背景 (效果清屏)

        # 用for ..in迭代列表,遍历整个image_list列表,
        # 用Role()的draw在游戏窗上(screen) 绘制图像方法将图形实例绘制在screen上
        for each in image_list:
            each.move()
            each.draw(screen) # 图形实例绘制在screen上

        # 用blit()方法将图像,按Rect对象的区域,绘制在screen上
        screen.blit(blue.image,blue.rect) # 绘制鼠标移动的蓝色圆形图形

        if point != None: # 如发生碰撞,与上一个if语句效果一样
            yellow.rect.center = coordinate # 设置碰撞点的黄色圆形小点坐标位置
            screen.blit(yellow.image,yellow.rect) # 在窗口图像最上层绘制黄色圆形小点

        # 调pygame的显示控制模块display中的update()函数
        pygame.display.update() # 显示 Surface,更新整个显示器的内容
        clock.tick(FPS)  # 用时钟对象控制每秒执行FPS次(帧画面刷新)

#程序实际执行起点
if __name__ == "__main__":   # execute only if run as a script
    main()    #从这里开始执行本程序命令,调用程序主函数main()