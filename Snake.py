from tkinter import *
import random

#Глобальные переменные:
WIDTH = 860
HEIGHT = 640
SEG_SIZE = 20
IN_GAME = True
apples = 0

#Вспомогательные функции:
def create_block():
    """создаёт блок 'еды' в случайной позиции на карте"""
    global BLOCK
    pos_x = SEG_SIZE * (random.randint(1, (WIDTH-SEG_SIZE)/SEG_SIZE))
    pos_y = SEG_SIZE * (random.randint(1, (HEIGHT-SEG_SIZE)/SEG_SIZE))
    #Блок-кружок красного цвета
    BLOCK = canv.create_oval(pos_x, pos_y,pos_x + SEG_SIZE,
                             pos_y + SEG_SIZE, fill="red")


def main():
    global IN_GAME
    global apples
    if IN_GAME:
        #Двигаем змейку
        s.move()
        #Определяем координаты головы:
        head_coords = canv.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
        #Столкновение с границами экрана:
        if x1 < 0 or x2 > WIDTH or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
        #Поедание яблок:
        elif head_coords == canv.coords(BLOCK):
            s.add_segment()
            canv.delete(BLOCK)
            create_block()
            apples = apples + 1
        #Столкновение с блоком змеи:
        else:
            for index in range(len(s.segments)-1):
                if canv.coords(s.segments[index].instance) == head_coords:
                    IN_GAME = False

        #Движение змеи,чем меньше цифра-тем выше скорость:
        root.after(110,main)
    #Если не в игре, выводим сообщение о проигрыше:
    else:
        t = "ТЫ ПРОИГРАЛ!\nТвой счёт: " + str(apples)
        canv.create_text(WIDTH/2, HEIGHT/2,
                        text=t,
                        font="Arial 20",
                        fill="#ff0000")



class Segment(object):
    def __init__(self, x, y):
        self.instance = canv.create_rectangle(x, y,
        x+SEG_SIZE, y+SEG_SIZE, fill='white')


class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        #Список доступных направлений движения:
        self.mapping = {"Down": (0,1),"Up": (0,-1),
                        "Left": (-1,0),"Right": (1,0)}
        #Изначально змейка движется вправо:
        self.vector = self.mapping["Right"]

    def move(self):
        """Двигает змейку в заданном направлении"""
        #Перебираем все сегменты, кроме первого:
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = canv.coords(self.segments[index+1].instance)
            #Задаём каждому сегменту позицию сегмента, стоящего следующим:
            canv.coords(segment, x1, y1, x2, y2)

        #Получаем координаты сегмента перед 'головой':
        x1, y1, x2, y2 = canv.coords(self.segments[-2].instance)
        #Помещаем голову в направлении вектора движения:
        canv.coords(self.segments[-1].instance,
                    x1+self.vector[0]*SEG_SIZE,
                    y1+self.vector[1]*SEG_SIZE,
                    x2+self.vector[0]*SEG_SIZE,
                    y2+self.vector[1]*SEG_SIZE)

    def change_direction(self, event):
        """Изменяет направление движения змейки"""
        #'event' передаст символ нажатой клавиши.
        #Если эта клавиша в списке доступных направлений,
        #изменяем направление:
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def add_segment(self):
        """Добавляет сегмент змейки"""
        #Определяем последний сегмент
        last_seg = canv.coords(self.segments[0].instance)
        #Определяем координаты для следующиего сегмента:
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        #Добавляем ещё один сегмент в заданных координатах:
        self.segments.insert(0, Segment(x,y))


root = Tk()
root.title("Змейка v 0.1.2")

#Игровое поле:
canv = Canvas(root,width=WIDTH, height=HEIGHT, bg='#005500')
canv.grid()
canv.focus_set()

#Создаём набор сегментов:
segments = [Segment(SEG_SIZE,SEG_SIZE),
            Segment(SEG_SIZE*2,SEG_SIZE),
            Segment(SEG_SIZE*3,SEG_SIZE)]

#Сама змейка:
s = Snake(segments)

#Реагируем на нажатие клавиш:
canv.bind("<KeyPress>", s.change_direction)

create_block()
main()
root.mainloop()
