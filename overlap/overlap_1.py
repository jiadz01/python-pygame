''' overlap_1.py   mask的精准碰撞检测示范程序1   2022.10.6
pygame提供了多种碰撞的检测方法:包括矩形碰撞检测、圆形碰撞检测和使用mask的精准碰撞检测.
本例用Pygame中处理图形遮罩(位掩码,掩膜)的模块mask,创建记录该角色Surface对象的透明点
和不透明点的 mask对象,用模块mask类的overlap(other, offset)方法,实现精确到1个像素级
别的的碰撞检测,原理是测试两个子画面之间的位掩码(掩膜)是否重叠.
通过本例运行并与程序语句对照,可更好理解这种精准碰撞检测方法,学习编程技术.
1.用鼠标移动蓝色小球去碰撞红色箭头,在窗口标题栏将显示碰撞参数值,窗口背色也会发生改变.
2.如果发生碰撞,则在2个Mask掩码第一个重叠交点坐标位置绘出一个黄色小圆点.
3.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此游戏程序.
4.按键盘q或Q键,退出此游戏程序.
5.程序中的RGB255颜色模式值(元组变量,还可用列表变量),可参考调色工具color_rgb.py
6.或用pygame.mask.from_threshold()确定某颜色的部份图形实现碰撞,
  详见下边语句后 # 注释带 ** 的语句,可修改程序运行观察效果.
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

# 在Surface对象上画拟静止不动的红色箭头图形
redSurface = pygame.Surface((80,80)) # 创建一个80*80用于绘制图形的Surface对象
redSurface.fill((0,0,0))  # 将这个Surface对象底色充填为黑色
redSurface.set_colorkey((0,0,0)) # 设置Surface对象中颜色(0,0,0)为透明
redPoints1 = [(0,40),(40,0),(80,40)] # 设置三角形三个顶点坐标值
# 用Pygame中绘图模块draw在Surface对象上据三个顶点参数画红色三角形(箭头的尖端)
pygame.draw.polygon(redSurface,'red',redPoints1)
redPoints2 = [(20,40),(60,40),(60,80),(20,80)] # 设置四边形四个顶点坐标值
# 用Pygame中绘图模块draw在Surface对象上据四个顶点参数画紫色四边形(箭头的箭身)
pygame.draw.polygon(redSurface,(106,28,206),redPoints2)
# 获取箭头图形Surface对象的矩形区域(Rect对象),并设置显示箭头图形初始x,y轴坐标
redRect = redSurface.get_rect(center=(width/2,height/2))

# 用Pygame中处理图形遮罩的模块 mask中的pygame.mask.from_surface()
# 创建箭头图形Surface对象的透明点和不透明点的 mask对象(掩膜)redMask
redMask = pygame.mask.from_surface(redSurface) # **
# 或用pygame.mask.from_threshold()确定某颜色的部份图形实现碰撞
# 下边语句是仅红色箭头部份才实现碰撞,可将上条语句头加#注释掉后用下条语句实现
#redMask = pygame.mask.from_threshold(redSurface,(255,0,0),(1,1,1,255)) # **

# 在Surface对象上画拟用鼠标移动的蓝色圆形图形
blueSurface = pygame.Surface((40,40)) # 创建一个40*40用于绘制图形的Surface对象
blueSurface.fill((0,0,0))  # 将这个Surface对象底色充填为黑色
blueSurface.set_colorkey((0,0,0)) # 设置Surface对象中颜色(0,0,0)为透明
# 用Pygame中绘图模块draw在Surface对象坐标x=20,y=20上画蓝色半径=20的圆形
pygame.draw.circle(blueSurface,'blue',(20,20),20)
# 获取圆形图形Surface对象的矩形区域(Rect对象),并设置显示图形初始x,y轴坐标
blueRect = blueSurface.get_rect(x=0,y=0)
# 用Pygame中处理图形遮罩的模块 mask中的pygame.mask.from_surface()
# 创建蓝色圆形图形Surface对象的透明点和不透明点的 mask对象(掩膜)blueMask
blueMask = pygame.mask.from_surface(blueSurface)

# 在Surface对象上画显示碰撞点的黄色圆形小点
yellowSurface = pygame.Surface((6,6)) # 创建一个6*6用于绘制图形的Surface对象
yellowSurface.fill((0,0,0))  # 将这个Surface对象底色充填为黑色
yellowSurface.set_colorkey((0,0,0)) # 设置Surface对象中颜色(0,0,0)为透明
# 用Pygame中绘图模块draw在Surface对象坐标x=3,y=3上画黄色半径=3的圆形小点
pygame.draw.circle(yellowSurface,(255,222,126),(3,3),3)
# 获取圆形图形Surface对象的矩形区域(Rect对象),并设置显示图形初始x,y轴坐标
yellowRect = yellowSurface.get_rect(x=width,y=0)

game_on = True # 只有当 game_on = False才会退出循环
# 游戏主循环 game loop
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
    # 移动蓝色圆形图形到光标位置
    #blue_x,blue_y = pygame.mouse.get_pos()
    #blueRect.center = blue_x,blue_y
    blueRect.center = pygame.mouse.get_pos() # 等效上2条前注有#语句

    # 用Pygame中处理图形遮罩的模块 mask中类的overlap(other, offset)方法
    # 来检测是否碰撞,offset是一个元组，元组中分别为两个rect的x坐标差值和y坐标差值
    # 注意这两个rect的坐标值在算式中的位置,与命令中的两个mask对应位置相关,
    # 即offset中的被减数和减数次序不能错误,次序不能交换
    offset = redRect.x -blueRect.x , redRect.y - blueRect.y
    # 返回的point是相对于blueMask的偏移量 (2个Mask掩码第一个重叠交点)
    point = blueMask.overlap(redMask,offset) # 无碰撞则返回 None
    if point: # 如发生碰撞
        # 计算第一位碰撞点在显示窗口中的坐标值 coordinate
        coordinate = blueRect.x + point[0],blueRect.y + point[1]
        # 将各变量转成字符串(info)供显示
        info = ' Collision point coordinate='+str(coordinate)+ \
            ' , point=' + str(point) + ' ,  offset=' + str(offset)
        # 在显示游戏窗口标题栏中，显示碰撞点信息参数
        pygame.display.set_caption(info)
        screen.fill((66,96,118)) # 填充screen对象浅灰蓝色背景 (效果清屏)
    else:
        # 设置显示游戏窗口的标题，可以是说明等字符串
        pygame.display.set_caption('Pygame example: overlap_1.py    ( No collision )')
        screen.fill((16,116,26)) # 填充screen对象绿色背景 (效果清屏)

    # 用blit()方法将图像,按Rect对象的区域,绘制在screen上
    screen.blit(redSurface,redRect) # 绘制红色箭头图形
    screen.blit(blueSurface,blueRect) # 绘制鼠标移动的蓝色圆形图形

    if point != None: # 如发生碰撞,与上一个if语句效果一样
        yellowRect.center = coordinate # 设置碰撞点的黄色圆形小点坐标位置
        screen.blit(yellowSurface,yellowRect) # 在窗口图像最上层绘制黄色圆形小点

    # 调pygame的显示控制模块display中的update()函数
    pygame.display.update() # 显示 Surface,更新整个显示器的内容
    clock.tick(FPS)  # 用时钟对象控制每秒执行FPS次(帧画面刷新)

pygame.quit() # 卸载所有pygame模块,关闭游戏窗口