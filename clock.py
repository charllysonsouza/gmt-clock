from datetime import datetime, timedelta
from math import sin, cos, pi
from tkinter import *
import json

##
# Relógio analógico GMT
# @author Charllyson Souza
#


class Clock:

    ##
    # Construtor da classe Clock.
    # @param root uma instância de tk
    def __init__(self, root):

        ## uma variável de instância de Tk.
        self.root = root
        ## a compensação UTC (offset).
        self.delta = 0

        # a largura do Canvas.
        CANVAS_WIDTH = 610
        # a altura do Canvas.
        CANVAS_HEIGHT = 610

        ## o centro do Canvas em relação a largura.
        self.width_center = CANVAS_WIDTH/2
        ## o centro do Canvas em relação a altura.
        self.heigth_center = CANVAS_HEIGHT/2

        ## um dicionário no qual a chave é uma determinada região e a chave o seu deslocamento UTC.
        self.timezone = {}

        # Manipulando JSON para extrair as informações.
        try:
            f = open('./localtime.json', 'r')
            # returns JSON object as a dictionary
            data = json.load(f)
            for c in data['cities']:
                self.timezone[f"{c['region']} / {c['city']}"] = c['offset']
            f.close()
        except Exception as e:
            print(e)
            print('No localtion file available')

        ## instância do Canvas.
        self.canvas = Canvas(self.root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='black')
        self.canvas.pack(expand=TRUE, side=RIGHT)

        ## cor do ponteiro.
        self.timecolor = "white"

        # variável que irá conter a opção seleciona no OptionMenu.
        value_inside = StringVar(value="Select a timezone")

        ## Menu de opções para selecionar a timezone desejada.
        self.menu = OptionMenu(self.root, value_inside, *self.timezone, command=self.select_gmtTime)
        self.menu.config(width=18, relief=FLAT, bg='lightblue')
        self.canvas.create_window(100, 30, window=self.menu, anchor=CENTER)

        ## Label contendo a data corrente e o deslocamento UTC selecionado.
        self.label = Label(self.root, bg='black', fg='lightblue', justify=LEFT, anchor=E,
                           font=('Helvetic', '10', 'italic'))
        self.canvas.create_window(530, 570, window=self.label, anchor=CENTER)

        # Desenha o círculo do relógio.
        self.create_circle(250, 5)

        # Desenha o centro do relógio.
        self.canvas.create_oval(self.width_center - 9, self.heigth_center - 9, self.width_center + 9,
                                self.heigth_center + 9, fill='white', outline='red', width=3)

        self.draw_circles_of_clock()
        self.poll()

    ## Configura o deslocamento UTC da variável delta de acordo com a opção selecionada.
    # @param variable contém a opção selecionada através do menu
    def select_gmtTime(self, variable):
        self.delta = self.timezone[variable]

    ##
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

    ##
    # Desenha um ponteiro.
    # Atribuindo-se o tag 'handles' aos ponteiros do relógio, a animação dos ponteiros
    # pode ser feita sem ter de redesenhar o canvas completamente.
    #
    # @param angle ângulo do ponteiro
    # @param len comprimento do ponteiro
    # @param wid largura do ponteiro
    # @param typeHandle o estilo de ponta do ponteiro gmt
    #
    def draw_handle(self, angle, len, wid=None, typeHandle=None):
        x, y = self.polar2Cartesian(angle, len)
        cx, cy = self.polar2Cartesian(angle, 0.05)

        self.canvas.create_line((self.width_center-cx), (self.heigth_center-cy), (self.width_center+x),
                                (self.heigth_center-y), fill=self.timecolor, tags='handles', width=wid, capstyle=ROUND,
                                arrow=typeHandle)

    ##
    # Desenha os três ponteiros do relógio.
    def paint_hms(self):
        # remove apenas os ponteiros
        self.canvas.delete('handles')

        # Para o fuso horário do Rio de Janeiro, self.delta vale -3.
        # (três horas para trás ou duas, no horário de verão).

        # hora, minutos e segundos: tempo UTC + delta horas.
        year, mon, day, h, m, s = datetime.timetuple(datetime.utcnow()+timedelta(hours=self.delta))[0:6]

        # Define o título da janela com relógio digital
        self.root.title('%02i:%02i:%02i' % (h, m, s))

        # configura o deslocamento e data atual
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

    ## Movimenta o relógio, redesenhando os ponteiros após um certo intervalo de de tempo.
    #
    def poll(self):
        # só é necessário redesenhar os ponteiros
        self.paint_hms()
        self.root.after(200, self.poll)

    ## Desenha o círculo que envolve os ponteiros.
    # @param radius tamanho do raio
    # @param wid espessura da linha do círculo
    def create_circle(self, radius, wid=None):  # center coordinates, radius
        x0 = self.width_center - radius
        y0 = self.heigth_center - radius
        x1 = self.width_center + radius
        y1 = self.heigth_center + radius
        return self.canvas.create_oval(x0, y0, x1, y1, outline='red', width=wid)

    ## Desenha os círculos que auxiliam na identificação do horário
    # - Desenha 12 círculos no interior para as horas
    # - Desenha 24 círculos no exterior para o ponteiro gmt para saber se a hora é AM ou PM
    def draw_circles_of_clock(self):
        r1 = 265
        r2 = 235
        hours_degree = 0
        gmt_degree = 0
        for i in range(24):
            if i < 12:
                t1 = self.width_center + r2 * sin(hours_degree)
                t2 = self.heigth_center + r2 * cos(hours_degree)
                self.canvas.create_oval(t1 - 10, t2 - 10, t1 + 10, t2 + 10, fill='gray', outline='red')
                hours_degree += pi/6

            t1 = self.width_center + r1 * sin(gmt_degree)
            t2 = self.heigth_center + r1 * cos(gmt_degree)
            self.canvas.create_oval(t1 - 10, t2 - 10, t1 + 10, t2 + 10, fill='gray', outline='red')
            gmt_degree += pi/12


instancia = Tk()
instancia.title('clock')
Clock(instancia)

instancia.mainloop()
