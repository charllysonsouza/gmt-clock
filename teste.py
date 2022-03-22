import math
from tkinter import *
import time

my_w = Tk()
width, height = 610, 610
c_width, c_height = width-5, height-5
d = str(width) + "x" + str(height)
my_w.geometry(d)

c1 = Canvas(my_w, width=c_width, height=c_height, bg='lightgreen')
c1.grid(row=0, column=0, padx=5)
dial = c1.create_oval(10, 10, 600, 600, width=10, outline='#ff0000', fill='#FFFFFF')
x, y = width/2, height/2
x1, y1, x2, y2 = x, y, x, 10
r1 = 280
r2 = 230
in_degree = 0
romans = iter(['12', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI'])
for i in range(0, 60):
    in_radian = math.radians(in_degree)
    if i % 5 == 0:
        ratio = 0.85
        t1 = x + r2 * math.sin(in_radian)
        t2 = y + r2 * math.cos(in_radian)
        c1.create_text(t1, t2, fill='blue', font='Times 25 bold', text=next(romans))
    else:
        ratio = 0.89
    x1 = x+ratio*r1*math.sin(in_radian)
    y1 = y-ratio*r1*math.cos(in_radian)
    x2 = x + r1 * math.sin(in_radian)
    y2 = y - r1 * math.cos(in_radian)
    c1.create_line(x1, y1, x2, y2, width=1)
    in_degree += 6

center = c1.create_oval(x-8, y-8, x+8, y+8, fill='#c0c0c0')

my_w.mainloop()
