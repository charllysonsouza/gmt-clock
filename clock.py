import math
from datetime import datetime, timedelta
from math import sin, cos, pi, radians
from tkinter import *
import json
# import pytz
# from timezonefinder import TimezoneFinder


class Clock:

    def __init__(self, root, delta=0):

        self.root = root
        self.delta = delta
        CANVAS_WIDTH = 610
        CANVAS_HEIGHT = 610
        self.width_center = CANVAS_WIDTH/2
        self.height_center = CANVAS_HEIGHT/2

        self.circlesize = 5

        self.places = []
        self.regions = {}
        self.timezone = "Greenwich"
        self.local = "Greenwich"

        try:
            f = open('./localtime.json', 'r')
            # returns JSON object as a dictionary
            data = json.load(f)
            for c in data['cities']:
                self.places.append((c['coordinates']['latitude'], c['coordinates']['longitude']))
                self.regions[f"{c['region']}/{c['city']}"] = c['offset']
            f.close()
        except Exception as e:
            print(e)
            print('No localtion file available')

        self.frame = Frame(self.root)
        self.frame.pack()

        self.canvas = Canvas(self.frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='black')
        self.canvas.pack(expand=TRUE, side=RIGHT)
        self.timecolor = "white"

        self.value_inside = StringVar(value="Select a timezone")

        self.menu = OptionMenu(self.frame, self.value_inside, *self.regions, command=self.select_gmtTime)
        self.menu.config(width=18, relief=FLAT, bg='lightblue')
        self.canvas.create_window(100, 30, window=self.menu, anchor=CENTER)

        self.label = Label(self.frame, bg='black', fg='lightblue', justify=LEFT, anchor=E,
                           font=('Helvetic', '10', 'italic'))
        self.canvas.create_window(530, 570, window=self.label, anchor=CENTER)

        self.create_circle(250, 5)
        self.canvas.create_oval(self.width_center - 9, self.height_center - 9, self.width_center + 9,
                                self.height_center + 9, fill='white', outline='red', tags='circle', width=3)

        self.draw_linesofclock()

        self.poll()

    def select_gmtTime(self, variable):
        self.delta = self.regions[variable]

    # Converte um vetor de coordenadas polares para cartesianas.
    # - Note que três horas está em 0º
    # - Para o relógio, no entanto, 0º está em doze horas.
    #
    # @param angle  ângulo do vetor
    # @param radius comprimento do vetor
    # @return um ponto 2D
    def polar2Cartesian(self, angle, radius=1.0):
        angle = pi / 2 - angle
        return radius * cos(angle), radius * sin(angle)

    # Desenha um ponteiro
    # Atribuindo-se o tag 'handles' aos ponteiros do relógio, a animação dos ponteiros
    # pode ser feita sem ter de redesenhar o canvas completamente
    #
    # @param angle ângulo do ponteiro
    # @param len comprimento do ponteiro
    # @param wid largura do ponteiro.
    #
    def draw_handle(self, angle, len, wid=None, typeHandle=None):
        x, y = self.polar2Cartesian(angle, len)
        cx, cy = self.polar2Cartesian(angle, 0.05)

        self.canvas.create_line((self.width_center-cx), (self.height_center-cy), (self.width_center+x),
                                (self.height_center-y), fill=self.timecolor, tags='handles', width=wid, capstyle=ROUND,
                                arrow=typeHandle)

    # Desenha os três ponteiros do relógio
    def paint_hms(self):
        # remove apenas os ponteiros
        self.canvas.delete('handles')

        # Para o fuso horário do Rio de Janeiro, self.delta vale -3
        # (três horas para trás ou duas, no horário de verão).

        # hora, minutos e segundos: tempo UTC + delta horas
        year, mon, day, h, m, s = datetime.timetuple(datetime.utcnow()+timedelta(hours=self.delta))[0:6]

        self.root.title('%02i:%02i:%02i' % (h, m, s))
        self.label.config(text="UTC %i\n%02i/%02i/%04i" % (self.delta, day, mon, year))

        oneMin = pi / 30  # um minuto vale 6 graus
        fiveMin = pi / 6  # cinco minutos ou uma hora vale 30 graus
        gmt_handle = pi / 12  # a hora do gmt equivale 15 graus

        hora = fiveMin * (h + m / 60.0)
        minutos = oneMin * (m + s / 60.0)
        segundos = oneMin * s
        gmt = gmt_handle * (h + m / 60.0)

        w = self.canvas.winfo_width()/2

        self.timecolor = 'red'
        self.draw_handle(hora, 0.45 * w, 10)  # ponteiro das horas
        self.timecolor = 'darkgray'
        self.draw_handle(minutos, 0.65 * w, 10)  # ponteiro dos minutos
        self.timecolor = 'white'
        self.draw_handle(segundos, 0.7 * w, 3.6)  # ponteiro dos segundos
        self.timecolor = 'lightgray'
        self.draw_handle(gmt, 0.83 * w, 2, 'last')

    # Movimenta o relógio, redesenhando os ponteiros após um certo intervalo de de tempo.
    #
    def poll(self):
        # só é necessário redesenhar os ponteiros
        self.paint_hms()
        self.root.after(200, self.poll)

    def create_circle(self, r, wid=None):  # center coordinates, radius
        x0 = self.width_center - r
        y0 = self.height_center - r
        x1 = self.width_center + r
        y1 = self.height_center + r
        return self.canvas.create_oval(x0, y0, x1, y1, outline='red', width=wid)

    def draw_linesofclock(self):
        r1 = 265
        r2 = 235
        hours_degree = 0
        gmt_degree = 0
        h = (['12', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI'])
        for i in range(0, 24):
            hours_radian, gmt_radian = radians(hours_degree), radians(gmt_degree)
            if i <= 12:
                ratio = 0.85
                t1 = self.width_center + r2 * sin(hours_radian)
                t2 = self.height_center + r2 * cos(hours_radian)
                self.canvas.create_oval(t1 - 10, t2 - 10, t1 + 10, t2 + 10, fill='gray', outline='red')
                hours_degree += 30

            t1 = self.width_center + r1 * sin(gmt_degree)
            t2 = self.height_center + r1 * cos(gmt_degree)
            self.canvas.create_oval(t1 - 10, t2 - 10, t1 + 10, t2 + 10, fill='gray', outline='red')
            gmt_degree += pi/12

            # if i % 5 == 0:
            # else:
            #     ratio = 0.89
            # x1 = self.width_center + ratio * r1 * sin(in_radian)
            # y1 = self.height_center - ratio * r1 * cos(in_radian)
            # x2 = self.width_center + r1 * sin(in_radian)
            # y2 = self.height_center - r1 * cos(in_radian)
            # self.canvas.create_line(x1, y1, x2, y2, width=2, fill='white')
            # in_degree += 6


instancia = Tk()
instancia.title('clock')
Clock(instancia)

instancia.mainloop()
