'''
该部分是由CNN卷积神经网络所编写的深度学习AI五子棋
实现了人机对战的部分
'''
import sys
from tkinter import *
from tkinter.ttk import *
from SGFfile import SGFflie
from CNN import myCNN
from robot import Robot
from tools import *
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'


class GoBang(object):

    def __init__(self):
        """
        初始化：
        someoneWin:标识是否有人赢了
        humanChessed:人类玩家是否下了
        IsStart:是否开始游戏了
        player:玩家是哪一方
        playmethod:模式，和robot下棋，还是和ai下棋
        bla_start_pos:黑棋开局时下在正中间的位置
        bla_chessed:保存黑棋已经下过的棋子
        whi_chessed:保存白棋已经下过的棋子
        board:棋盘
        window:窗口
        var:用于标记选择玩家颜色的一个变量
        var1:用于标记选择robot或者ai的一个变量
        can:画布，用于绘出棋盘
        net_board:棋盘的点信息
        robot:机器人
        sgf:处理棋谱
        cnn:cnnc神经网络
        """
        self.someoneWin = False
        self.humanChessed = False
        self.IsStart = False
        self.player = 0
        self.playmethod = 0
        self.bla_start_pos = [235, 235]
        self.whi_chessed = []
        self.bla_chessed = []
        self.board = self.init_board()
        self.window = Tk()
        self.var = IntVar()
        self.var.set(0)
        self.var1 = IntVar()
        self.var1.set(0)
        self.window.title("人机对战")
        self.window.geometry("600x470+500+300")
        self.window.resizable(False, False)
        self.can = Canvas(self.window, bg="FloralWhite", width=470, height=470)
        self.draw_board()
        self.can.grid(row=0, column=0)
        self.net_board = self.get_net_board()
        self.robot = Robot(self.board)
        self.sgf = SGFflie()
        self.cnn = myCNN()
        self.cnn.restore_save()

    def init_board(self):
        """初始化棋盘"""
        list1 = [[-1] * 15 for i in range(15)]
        return list1

    def draw_board(self):
        """画出棋盘"""

        for row in range(15):
            if row == 0 or row == 14:
                self.can.create_line((25, 25 + row * 30), (445, 25 + row * 30), width=2)
            else:
                self.can.create_line((25, 25 + row * 30), (445, 25 + row * 30), width=1)
        for col in range(15):
            if col == 0 or col == 14:
                self.can.create_line((25 + col * 30, 25), (25 + col * 30, 445), width=2)
            else:
                self.can.create_line((25 + col * 30, 25), (25 + col * 30, 445), width=1)
        self.can.create_oval(112, 112, 118, 118, fill="black")
        self.can.create_oval(352, 112, 358, 118, fill="black")
        self.can.create_oval(112, 352, 118, 358, fill="black")
        self.can.create_oval(232, 232, 238, 238, fill="black")
        self.can.create_oval(352, 352, 358, 358, fill="black")

    def get_nearest_po(self, x, y):
        """得到坐标（x, y）在棋盘各点中最近的一个点"""
        flag = 600
        position = ()
        for point in self.net_board:
            distance = get_distance([x, y], point)
            if distance < flag:
                flag = distance
                position = point
        return position

    def no_in_chessed(self, pos):
        """pos 没有下过"""
        whi_chess = self.check_chessed(pos, self.whi_chessed)
        bla_chess = self.check_chessed(pos, self.bla_chessed)
        return whi_chess == False and bla_chess == False

    def ai_no_in_chessed(self, pos, value):
        """
        ai预测出来的点是否已经下过，
        以及结合机器人计算出来的值，
        如果ai的点为下过，而且机器
        人预测出来的最大值小于400
        返回真
        """
        no_in_chessed = self.no_in_chessed(pos)
        return no_in_chessed and value < 4000

    def check_chessed(self, point, chessed):
        """检测是否已经下过了"""
        if len(chessed) == 0:
            return False
        flag = 0
        for p in chessed:
            if point[0] == p[0] and point[1] == p[1]:
                flag = 1
        if flag == 1:
            return True
        else:
            return False

    def have_five(self, chessed):
        """检测是否存在连五了"""
        if len(chessed) == 0:
            return False
        for row in range(15):
            for col in range(15):
                x = 25 + row * 30
                y = 25 + col * 30
                if self.check_chessed((x, y), chessed) == True and \
                        self.check_chessed((x, y + 30), chessed) == True and \
                        self.check_chessed((x, y + 60), chessed) == True and \
                        self.check_chessed((x, y + 90), chessed) == True and \
                        self.check_chessed((x, y + 120), chessed) == True:
                    return True
                elif self.check_chessed((x, y), chessed) == True and \
                        self.check_chessed((x + 30, y), chessed) == True and \
                        self.check_chessed((x + 60, y), chessed) == True and \
                        self.check_chessed((x + 90, y), chessed) == True and \
                        self.check_chessed((x + 120, y), chessed) == True:
                    return True
                elif self.check_chessed((x, y), chessed) == True and \
                        self.check_chessed((x + 30, y + 30), chessed) == True and \
                        self.check_chessed((x + 60, y + 60), chessed) == True and \
                        self.check_chessed((x + 90, y + 90), chessed) == True and \
                        self.check_chessed((x + 120, y + 120), chessed) == True:
                    return True
                elif self.check_chessed((x, y), chessed) == True and \
                        self.check_chessed((x + 30, y - 30), chessed) == True and \
                        self.check_chessed((x + 60, y - 60), chessed) == True and \
                        self.check_chessed((x + 90, y - 90), chessed) == True and \
                        self.check_chessed((x + 120, y - 120), chessed) == True:
                    return True
                else:
                    pass
        return False

    def check_win(self):
        """检测是否有人赢了"""
        if self.have_five(self.whi_chessed):
            label = Label(self.window, text="White Win!", background='AliceBlue', font=("华文楷体", 15, "bold"))
            label.place(relx=0, rely=0, x=480, y=40)
            return True
        elif self.have_five(self.bla_chessed):
            label = Label(self.window, text="Black Win!", background='PaleTurquoise', font=("华文楷体", 15, "bold"))
            label.place(relx=0, rely=0, x=480, y=40)
            return True
        else:
            return False

    def draw_chessed(self):
        """在棋盘中画出已经下过的棋子"""

        if len(self.whi_chessed) != 0:
            for tmp in self.whi_chessed:
                oval = pos_to_draw(*tmp[0:2])
                self.can.create_oval(oval, fill="white")

        if len(self.bla_chessed) != 0:
            for tmp in self.bla_chessed:
                oval = pos_to_draw(*tmp[0:2])
                self.can.create_oval(oval, fill="black")

    def draw_a_chess(self, x, y, player=None):
        """在棋盘中画一个棋子"""
        _x, _y = pos_in_qiju(x, y)
        oval = pos_to_draw(x, y)

        if player == 0:
            self.can.create_oval(oval, fill="black")
            self.bla_chessed.append([x, y, 0])
            self.board[_x][_y] = 1
        elif player == 1:
            self.can.create_oval(oval, fill="white")
            self.whi_chessed.append([x, y, 1])
            self.board[_x][_y] = 0
        else:
            print(AttributeError("请选择棋手"))
        return

    def AIrobotChess(self):
        """ai机器人下棋"""
        cnn_predict = self.cnn.predition(self.board)  # 预测

        if self.player % 2 == 0:
            """开局优化"""
            if len(self.bla_chessed) == 0 and len(self.whi_chessed) == 0:
                self.draw_a_chess(*self.bla_start_pos, 0)

            else:
                # 机器人计算出全局价值最大的点
                _x, _y, _ = self.robot.MaxValue_po(1, 0)
                newPoint = pos_in_board(_x, _y)

                if self.ai_no_in_chessed(cnn_predict, _):
                    self.draw_a_chess(*cnn_predict, 0)
                else:
                    self.draw_a_chess(*newPoint, 0)

    def chess(self, event):
        """下棋函数"""

        if self.someoneWin == True or self.IsStart == False:
            """判断是否有人赢了或者是否按了开始键"""
            return

        ex = event.x
        ey = event.y
        if not click_in_board(ex, ey):
            """检查鼠标点击的坐标是否在棋盘内"""
            return

        neibor_po = self.get_nearest_po(ex, ey)
        if self.no_in_chessed(neibor_po):

            if self.player == 0:
                self.draw_a_chess(*neibor_po, 1)
            else:
                self.draw_a_chess(*neibor_po, 0)

            self.someoneWin = self.check_win()
            if self.playmethod == 0:
                self.AIrobotChess()
            self.someoneWin = self.check_win()

    def get_net_board(self):
        """得到棋盘的点信息"""
        net_list = []
        for row in range(15):
            for col in range(15):
                point = pos_in_board(row, col)
                net_list.append(point)
        return net_list

    def resetButton(self):
        """重置按钮的回调函数，实现了整个棋盘重置"""
        self.someoneWin = False
        self.IsStart = False
        self.whi_chessed.clear()
        self.bla_chessed.clear()
        self.board = self.init_board()
        self.robot = Robot(self.board)
        label = Label(self.window, text="                 ", background="GhostWhite", font=("华文楷体", 15, "bold"))
        label.place(relx=0, rely=0, x=480, y=40)
        self.can.delete("all")
        self.draw_board()
        self.can.grid(row=0, column=0)

    def BakcAChess(self):
        """悔棋按钮的回调函数"""
        if self.someoneWin == False:
            if len(self.whi_chessed) != 0:
                p = self.whi_chessed.pop()
                x, y = pos_in_qiju(*p[0:2])
                self.board[x][y] = -1

            if self.player == 0 and len(self.bla_chessed) != 1:
                p = self.bla_chessed.pop()
                x, y = pos_in_qiju(*p[0:2])
                self.board[x][y] = -1

            elif self.player == 1 and len(self.bla_chessed) != 0:
                p = self.bla_chessed.pop()
                x, y = pos_in_qiju(*p[0:2])
                self.board[x][y] = -1

            else:
                pass

            self.can.delete("all")
            self.draw_board()
            self.draw_chessed()

    def startButton(self):
        """开始按钮的回调函数"""
        if self.IsStart == False:
            self.IsStart = True
            if self.player % 2 == 0:
                if self.playmethod == 0:
                    self.AIrobotChess()
                elif self.playmethod == 1:
                    pass
                self.draw_chessed()

    def createqipu(self):
        """将棋盘中的棋局生成棋盘"""
        qipu = []
        step = 0
        totalstep = len(self.whi_chessed) + len(self.bla_chessed)
        while step < totalstep:
            if totalstep == 0:
                break
            flag = int(step / 2)
            if step % 2 == 0:
                pos = pos_in_qiju(*self.bla_chessed[flag][0:2])
                qipu.append([*pos, 0, step + 1])
            else:
                pos = pos_in_qiju(*self.whi_chessed[flag][0:2])
                qipu.append([*pos, 1, step + 1])
            step += 1
        return qipu

    def start(self):
        """开始，主要实现一些按钮与按键"""
        b3 = Button(self.window, text="开始", command=self.startButton)
        b3.place(relx=0, rely=0, x=495, y=100)

        b1 = Button(self.window, text="重置", command=self.resetButton)
        b1.place(relx=0, rely=0, x=495, y=180)

        b2 = Button(self.window, text="悔棋", command=self.BakcAChess)
        b2.place(relx=0, rely=0, x=495, y=260)

        self.can.bind("<Button-1>", lambda x: self.chess(x))
        self.window.mainloop()


def play():
    game = GoBang()
    game.start()
    game.resetButton()
    game.whi_chessed = []
    game.bla_chessed = []
    del game
    sys.exit()

