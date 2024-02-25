"""
这是主程序，主要实现了界面的呈现，并且整合了游戏的所有功能
运行此文件就可以开始游戏了
"""
import tkinter as tk
from tkinter import *
import wzq
import datetime
from PIL import ImageTk, Image
from ttkbootstrap.constants import *
import tkinter.font as tkf
import AI

a = datetime.datetime.now()
a = str(a)
time = a[:10] + ' ' + a[11:13]+':'+a[14:16]


class Window:
    def __init__(self):
        self.lb = 0
        self.lw = 0
        self.w = tk.Tk()
        self.w.resizable(False, False)
        self.w.geometry('600x600+600+200')
        self.rank = dict()
        self.autosize(600, 600)
        img1 = Image.open('UI/人人.jpg')
        img1 = img1.resize((220, 70))
        photo1 = ImageTk.PhotoImage(img1)
        button1 = Button(self.w, image=photo1, height=50, width=200, bd=2, bg='Wheat', command=self.enter,
                         cursor='star', relief=RIDGE)
        button1.place(x=195, y=250)

        img2 = Image.open('UI/人机.jpg')
        img2 = img2.resize((220, 70))
        photo2 = ImageTk.PhotoImage(img2)
        button2 = Button(self.w, image=photo2, height=50, width=200, bd=2, bg='Wheat', cursor='heart', relief=RIDGE
                         , command=AI.play)
        button2.place(x=195, y=330)

        img3 = Image.open('UI/记录.jpg')
        img3 = img3.resize((220, 70))
        photo3 = ImageTk.PhotoImage(img3)
        button3 = tk.Button(self.w, image=photo3, height=50, width=200, bd=2, bg='Wheat', command=self.history,
                            cursor='circle', relief=RIDGE)
        button3.place(x=195, y=410)

        img4 = Image.open('UI/排名.jpg')
        img4 = img4.resize((220, 70))
        photo4 = ImageTk.PhotoImage(img4)
        button4 = tk.Button(self.w, image=photo4, height=50, width=200, bd=2, bg='Wheat', cursor='pirate', relief=RIDGE,
                            command=self.Rank)
        button4.place(x=195, y=490)
        self.w.mainloop()

    def play(self):
        r = wzq.play()
        if r == 1:
            res = '黑方获胜'
            b = 1
            w = 0
        else:
            res = '白方获胜'
            w = 1
            b = 0
        f = open('History/对战记录.txt', mode='a')
        F = open('History/胜率.txt', 'a')
        f.write('\n')
        F.write('\n')
        pb = self.lb.get()
        f.write('黑方: ' + str(pb) + ' ')
        F.write(str(pb) + ':' + str(b))
        pw = self.lw.get()
        F.write('\n')
        f.write('白方: ' + str(pw) + ' ')
        F.write(str(pw) + ':' + str(w))
        f.write('时间: ' + str(time) + ' ' + res)
        f.close()
        F.close()

    def history(self):
        window2 = Toplevel()
        window2.title('对战记录')
        window2.geometry('600x400+500+400')
        f = open('History/对战记录.txt', 'r')
        f.seek(0)
        text = Text(window2)
        font = tkf.Font(family='Times', size=14)
        info = f.read()
        f.seek(0)
        for lines in info:
            text.insert('insert', lines)
            text.config(font=font, foreground='black')
            text.insert('end', '')
        text.pack()
        window2.mainloop()

    def Rank(self):
        f = open('History/胜率.txt', 'r')
        f.seek(0)
        for lines in f:
            lines = lines.split(':')
            self.rank.setdefault(lines[0], [])
            self.rank[lines[0]].append(int(lines[1]))
        new_rank = self.rank.copy()
        self.rank.clear()
        f.close()
        count = 0
        for k in new_rank.keys():
            for i in new_rank[k]:
                if i == 1:
                    count += 1
            sl = float(count / len(new_rank[k]))
            count = 0
            new_rank[k] = sl
        new_rank = sorted(new_rank.items(), key=lambda I: I[1], reverse=True)
        window3 = Toplevel()
        window3.title('查看排名')
        window3.geometry('600x400+500+400')
        text = Text(window3)
        font = tkf.Font(family='Times', size=14)
        for k in new_rank:
            count += 1
            text.insert('insert', 'NO.' + str(count) + '     ')
            text.insert('insert', 'player: ' + str(k[0]) + '\n' + (' 胜率: ' + str(('{:.1f}%'.format(k[1] * 100))))
                        )
            text.config(font=font, foreground='black')
            text.insert('end', '\n')
        text.pack()
        window3.mainloop()

    def enter(self):
        window1 = tk.Toplevel()
        window1.title("开始")
        window1.geometry('500x300+574+232')
        tk.Label(window1, text='黑方玩家名称:', font=("Times", 15, "bold")).grid(row=0, column=1)
        tk.Label(window1, text='白方玩家名称:', font=("Times", 15, "bold")).grid(row=5, column=1)
        self.lb = tk.Entry(window1, relief=GROOVE, width=20)
        self.lb.grid(row=0, column=2)
        Label(window1).grid(row=3, column=2)
        self.lw = tk.Entry(window1, relief=GROOVE, width=20)
        self.lw.grid(row=5, column=2)
        Label(window1).grid(row=7, column=2)
        img1 = Image.open("UI/start.jpg")
        img1 = img1.resize((220, 100))
        photo1 = ImageTk.PhotoImage(img1)
        Button(window1, command=self.play, image=photo1, bd=2, cursor='cross', relief=RIDGE).grid(row=10, column=2)
        window1.mainloop()

    def resize(self, w, h, w_box, h_box, pil_image):
        f1 = w_box / w
        f2 = h_box / h
        factor = min(f1, f2)
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def autosize(self, w_box, h_box):
        global canvas, tk_image
        pil_image = Image.open('UI/无按钮.jpg')
        w, h = pil_image.size
        pil_image_resized = self.resize(w, h, w_box, h_box, pil_image)
        tk_image = ImageTk.PhotoImage(pil_image_resized)
        canvas = tk.Canvas(self.w, width=w_box, height=h_box)
        canvas.place(x=0, y=0)
        canvas.create_image(w_box // 2, h_box // 2, image=tk_image)
        self.w.geometry("%dx%d" % (w_box, h_box))


win = Window()
