'''animation_5.py   动画示例 5   对animation_4.py修改   2022.11.3
在animation_4.py的基础上,改用sprite模块的Group()类创建一个sprite对象的管理容器,来实现
每帧更新与绘制. Group()类对默认自动调用的更新方法名称: update()和变量名: self.image
 self.rect 是固定命名,不得更改. 故对自创建子类动画Animation()进行了局部改写,注意区别.
 具体新增或变化语句,详见下边语句后 # 注释带 ** 的语句.
a.本例用Surface模块中的方法 Surface.subfurface() 根据父表面的一部分区域创建新子表面.
  将大图按帧的矩形方框提取每块小图(帧子表面Surface对象),再将变化的每帧图按秩序绘制在
  屏幕上,利用人类"视觉暂留"(约0.1-0.4秒)现象,实现动画效果(就象放映电影).
b.以pygame的sprite模块中名为精灵Sprite类为父类(基类),创建一个子类Animation来实现编程,
  该子类还新加一个动画绘制方法(每执行一次绘一帧)update().
  同时采用控制不相同帧子图变更播放间隔毫秒数的算法,控制动画动作快慢.
c.本例程序总体结构(写法)是规范的,可供其它程序导入后,调用类Animation().
d.大图内小图帧的矩形方框参数计算公式如下:  使用frame变量来表示帧序号(即第几帧小图序号)
  帧宽度 frameRect.width = 大图片宽度 rect.width / 列数 columns
  帧高度 frameRect.height = 大图片高度 rect.height / 行数 rows
  帧坐标x  frameRect.x = (帧序号 frame % 列数 columns ) * 帧宽度 frameRect.width
  帧坐标y frameRect.y = (帧序号 frame // 列数 columns ) * 帧高度 frameRect.height
注意:帧坐标X,Y是帧的矩形方框左上角坐标值,以大图左上角坐标为基准起点(0,0).
     帧序号=0,1,2,3.......  是从0开始计算,即第一帧序号是0.行和列的索引也都是从0开始的.
     列数是指大图中小图排列的列数(可理解为竖行数?而不是小图总数).

1.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此程序.
2.图片文件 RC.png 需在本程序同一目录中,或在程序的文件名字符串中指明它磁盘目录路径.
'''
# 导入所需的模块
import pygame # 导入pygame模块,调用其对象、类和函数等前加pygame.
import sys # 导入python内置sys模块,调用其对象、类和函数等前加sys.

# 自创建子类动画Animation(),它继承的父类是pygame.sprite.Sprite类
class Animation(pygame.sprite.Sprite):
    # 参数: fileName-载入整张图片文件名  rows-行数  columns-列数  rate-子图变更间隔
    # position- 绘制子图在窗口初始坐标位值,默认值x=0 y=0
    def __init__(self, fileName, rows, columns, rate, position=[0,0]): # **
        pygame.sprite.Sprite.__init__(self) #让父类的属性与子类关联才能使用
        #super().__init__() #让父类的属性与子类关联,同上条等效,选其一即可
        # 从文件加载大图片,转换成Surface对象,图片字符串文件名可带有文件的路径
        self.master_image = pygame.image.load(fileName).convert_alpha()
        # 获取大图片Surface对象的矩形区域(大图的Rect对象)
        self.rect = self.master_image.get_rect() # **
        # 将大图片Rect对象拷贝到self.frameRect供动画小图每帧矩形框用
        self.frameRect = self.rect.copy() # 将rect拷贝到frameRect供动画每帧矩形框用 **
        #self.frameRect.width = abs(self.rect.width / columns) # 计算出每帧的宽,商取整数
        self.frameRect.width = self.rect.width // columns # 计算出每帧的宽,同上条等效 **
        self.frameRect.height = self.rect.height // rows # 计算出每帧的高,商取整数 **
        self.frame = 0 # 初始化帧序号,第一帧序号=0
        self.last_frame = columns * rows - 1 # 最后一帧序号(不减1就是小图总数)
        self.columns = columns # 子图在大图排列的列数
        self.rate = rate # 不同帧子图变更播放间隔毫秒数,控制动画动作快慢
        self.old_frame = self.last_frame # 前一帧序号,初始化时放在最后一帧序号
        self.last_time = 0 # 初始化前一帧播放时间
        self.current_time = 0 # 初始化现拟播放帧时间
        # 初始化大图片的Rect对象 self.rect 坐标的属性值=position,当用group.update()更新帧
        # image时,系统将自动(默认)调用self.rect,取rect坐标的属性值为帧image在窗口的坐标位值
        self.rect.x, self.rect.y = position # **

    # 自定义的动画更新方法(每执行一次绘一帧),调用需传递参数: time=调用时的系统现时毫秒数
    def update(self, time): # **
        # 本更新方法update用于group.update()命令,只是方法的命名不能改动
        self.current_time = time # 获取参数传递的现时毫秒数
        if self.frame != self.old_frame: # 如果现帧序号与已播放帧号不同,则创建拟播帧image
            # 按公式计算现帧序号对应的帧的frameRect矩形方框(Rect对象)的x,y值
            self.frameRect.x = (self.frame % self.columns) * self.frameRect.width
            self.frameRect.y = (self.frame // self.columns) * self.frameRect.height
            # 根椐父对象master_image以帧的矩形方框frameRect,创建子Surface对象image
            self.image = self.master_image.subsurface(self.frameRect)
            self.old_frame = self.frame # frame赋值给old_frame以便计算下一帧image

        if self.current_time > self.last_time + self.rate: # 如大于换帧间隔毫秒数
            self.frame += 1 #  帧序号加 1,拟播放下一帧图
            self.last_time = self.current_time # 赋值给last_time以便计算下一帧时间
            if self.frame > self.last_frame: # 如果帧序号大于该总图最一帧,则从头循环
                self.frame = 0 # 回到第一帧,循环播放
        # **
#程序实际执行起点
if __name__ == "__main__":   # execute only if run as a script
    FPS = 60 # 设置画面刷新的帧率,即每秒内刷新次数(帧画面)
    SIZE = WIDTH, HEIGHT = 640, 480 # 设置游戏窗口宽和高,3个大写为全局变(常)量
    # 设置窗口颜色(即背景颜色),有关颜色模式详见调色工具color_rgb.py
    windowColor = (36,186,255) # 元组变量, RGB255颜色模式值(还可用列表变量)

    pygame.init() # 初始化pygame游戏引擎

    # 初始化游戏窗口屏幕显示
    screen = pygame.display.set_mode(SIZE)
    screen.fill(windowColor) # 用fill()方法填充screen对象单一色背景
    pygame.display.set_caption('Animation example 5 ') # 设置游戏窗口的标题

    position1 = [80,80] # 设置person1在窗口坐标,x=80  y=80
    # 调用自创建子类Animation()创建实例 person1,参数:总图文件名  总图行数=1 总图列数=8
    # 不相同的子图播放间隔毫秒数=80   子图坐标位值x=80  y=80
    person1 = Animation('RC.png', 1, 8, 80, position1) # **

    position2 = [380,80] # 设置person2在窗口坐标,x=380  y=80
    # 调用自创建子类Animation()创建实例 person2,参数:总图文件名  总图行数=1 总图列数=8
    # 不相同的子图播放间隔毫秒数=80   子图坐标位值x=80  y=80
    person2 = Animation('RC.png', 1, 8, 160, position2) # **

    # 用sprite模块的Group()类创建一个sprite对象的管理容器group
    group = pygame.sprite.Group() # **
    # 用sprite模块的Group()类的add()方法将2个sprite实例加入到管理容器group
    group.add(person1,person2) # **

    clock = pygame.time.Clock()  # 设置pygame时钟对象
    # 从总图中获取每帧图像以循环方式绘动画图像
    while True: # 游戏主循环
        for event in pygame.event.get(): # 用for循环遍历事件队列,弹出获取并从队列删除,一定要写
            if event.type == pygame.QUIT: # 当用户按下窗口的关闭按钮
                pygame.quit() # 卸载所有pygame模块
                sys.exit() # 终止程序，退出游戏主循环,关闭游戏窗口

        screen.fill(windowColor) # 用fill()方法填充screen对象单一色背景 (清屏)
        # 用pygame中time模块的 pygame.time.get_ticks(),以毫秒为单位获取当前时间
        currentTime = pygame.time.get_ticks() # 赋值给变量,用于参数传递

        # 用sprite模块的Group()类的更新方法update()更新一帧图,此时它自动调自创子类同名方法
        # update()对Surface对象self.image处值
        group.update(currentTime) # **
        # 用sprite模块的Group()类的绘画方法draw(),此时它自动将容器内各更新的精灵对象
        # self.image以self.rect所带的x,y坐标值,绘制在窗口screen
        group.draw(screen) # **
        # 调pygame的显示控制模块display中的update()函数
        pygame.display.update() # 完整显示窗口,更新整个显示器的内容,是flip()的优化版本
        clock.tick(FPS)  # 用时钟对象控制每秒执行FPS次 (主循环帧画面刷新)