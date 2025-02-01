'''animation_trans1.py   将PNG格式图片单一背景颜色转换为透明   2022.11.13
介绍二种方法: (要预先确知背景颜色RGB值)
1. 用 image = pygame.image.load("PNG格式图片文件名").convert_alpha()语句,
   将PNG格式图片文件从磁盘加载,并转换成Surface对象image,
   然后用Surface模块中的方法 image.set_colorkey(color)将背景色设置为透明.
   该背景透明的Surface对象image在所属程序模块中有效,存盘无效,应使用下边方法.
2. 自创建将PNG格式图片单一背景颜色转换为透明的函数 transparent(),
   对用 pygame.image.load("PNG格式图片").convert_alpha()语句加载并转换成Surface对象,
   for循环嵌套遍历该对象(图片)各点,用Surface模块中的方法get_at()获取一个像素颜色值,
   用set_at()设置一个像素颜色值,将单一背景颜色值的alpha设置为0,使背景颜色透明.
   再把透明背景色的图片以新的PNG格式图片文件存盘,供程序调用.
   参数: fileName_0--将被转换背景色为透明源文件.png
         fileName_1--转换后文件.png
         color--原图背景色RGB/RGBA颜色值,元组变量
                A位是颜色RGB值的alpha值,A=255是背景该像素点不透明
   transparent()函数可被其它程序导入后调用.
3. 本程序Animation()函数与animation_n.py的同名函数的一个参数(图片)有区别,
   本程序不是传图片文件名而是直接传图片的Surface对象.
运行本程序进行文件转换效果演示:
1.移动鼠标在游戏窗口右上角处"X"关闭按钮,点击鼠标左键退出此程序.
2.图片文件 RC.png和r.png 需在本程序同一目录中,或在程序的文件名字符串中指明它磁盘目录路径.
  本程序r.png图片背景色是白色,背景颜色RGB值=(255,255,255)
'''
import sys  # 导入python内置sys模块,调用其对象、类和函数等前加sys.
import pygame  # 导入pygame模块,调用其对象、类和函数等前加pygame.


# 自创建将PNG格式图片单一背景颜色转换为透明的函数
def transparent(fileName_0, fileName_1, color ):
    # fileName_0--将被转换背景色为透明源文件.png  fileName_1--转换后文件.png
    # color--原图背景色RGBA颜色值,元组变量,末位是颜色RGB值的alpha值=255是不透明
    image = pygame.image.load(fileName_0).convert_alpha() # 从文件加载图片
    backdrop = (color[0],color[1],color[2],0) # 设置背景颜色RGBA值的alpha值=0,透明
    # 对图像中的所有像素点进行遍历,凡该点与背景色相同的像素的alpha值=0,该点透明
    # 用Surface模块中的方法get_at()获取一个像素颜色值,用set_at()设置一个像素颜色值
    #for x in range(image.get_width()): # for循环嵌套,竖(y)行扫描遍历图片各点
    #    for y in range(image.get_height()): # 本2条循环嵌套语句等效下边2条
    for y in range(image.get_height()): # for循环嵌套,横(x)行扫描遍历图片各点
        for x in range(image.get_width()): # 本2条循环嵌套语句等效上边2条
           if image.get_at((x, y)) == (color): # 如果该点与背景色相同
              image.set_at((x, y), backdrop) # 则该点颜色的alpha值=0,该点透明

    pygame.image.save(image, fileName_1) # 将透明背景色的图片以文件fileName_1存盘

# 自创建子类动画Animation(),它继承的父类是pygame.sprite.Sprite类
class Animation(pygame.sprite.Sprite):
    # 参数: image-图片Surface对象  rows-行数  columns-列数  rate-子图变更间隔
    # position- 绘制子图在窗口初始坐标位值,默认值x=0 y=0
    def __init__(self, image, rows, columns, rate, position=[0,0]):
        pygame.sprite.Sprite.__init__(self) #让父类的属性与子类关联才能使用
        #super().__init__() #让父类的属性与子类关联,同上条等效,选其一即可
        self.master_image = image # image图片Surface对象
        # 获取大图片Surface对象的矩形区域(大图的Rect对象)
        self.rect = self.master_image.get_rect()
        # 将大图片Rect对象拷贝到self.frameRect供动画小图每帧矩形框用
        self.frameRect = self.rect.copy() # 将rect拷贝到frameRect供动画每帧矩形框用
        self.frameRect.width = self.rect.width // columns # 计算出每帧的宽,商取整数
        self.frameRect.height = self.rect.height // rows # 计算出每帧的高,商取整数
        self.frame = 0 # 初始化帧序号,第一帧序号=0
        self.last_frame = columns * rows - 1 # 最后一帧序号(不减1就是小图总数)
        self.columns = columns # 子图在大图排列的列数
        self.rate = rate # 不同帧子图变更播放间隔毫秒数,控制动画动作快慢
        self.old_frame = self.last_frame # 前一帧序号,初始化时放在最后一帧序号
        self.last_time = 0 # 初始化前一帧播放时间
        self.current_time = 0 # 初始化现拟播放帧时间
        # 初始化大图片的Rect对象 self.rect 坐标的属性值=position,当用group.update()更新帧
        # image时,系统将自动(默认)调用self.rect,取rect坐标的属性值为帧image在窗口的坐标位值
        self.rect.x, self.rect.y = position

    # 自定义的动画更新方法(每执行一次绘一帧),调用需传递参数: time=调用时的系统现时毫秒数
    def update(self, time):
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
    pygame.display.set_caption('Animation_Transparent   example 1  ') # 设置游戏窗口的标题

    # 调用自创函数转换文件,r2.png文件背景色白色(255,255,255)透明
    transparent('r.png','r2.png',(255,255,255))
    # 从磁盘文件加载图片,转换成Surface对象
    RC = pygame.image.load('RC.png').convert_alpha()
    r = pygame.image.load('r.png').convert_alpha()
    #r.set_colorkey((255,255,255)) # Surface对象r背景色白色(255,255,255)透明
    r2 = pygame.image.load('r2.png').convert_alpha()

    position = [230,80] # 设置person在窗口坐标,x=230  y=80
    position_r = [30,80] # 设置r在窗口坐标,x=30  y=80
    position_r2 = [460,80] # 设置r2在窗口坐标,x=460  y=80

    # 调用自创建子类Animation()创建实例   5个参数按排列顺序分别是: 1.图片的Surface对象
    # 2.总图行数  3.总图列数  4.不相同的子图播放间隔毫秒数  5.子图在窗口坐标位值
    person = Animation(RC, 1, 8, 80, position)
    person_r = Animation(r, 1, 7, 160, position_r)
    person_r2 = Animation(r2, 1, 7, 160, position_r2)

    # 用sprite模块的Group()类创建一个sprite对象的管理容器group
    group = pygame.sprite.Group()
    # 用sprite模块的Group()类的add()方法将3个sprite实例加入到管理容器group
    group.add(person,person_r,person_r2)
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
        group.update(currentTime)
        # 用sprite模块的Group()类的绘画方法draw(),此时它自动将容器内各更新的精灵对象
        # self.image以self.rect所带的x,y坐标值,绘制在窗口screen
        group.draw(screen)
        # 调pygame的显示控制模块display中的update()函数
        pygame.display.update() # 完整显示窗口,更新整个显示器的内容,是flip()的优化版本
        clock.tick(FPS)  # 用时钟对象控制每秒执行FPS次 (主循环帧画面刷新)