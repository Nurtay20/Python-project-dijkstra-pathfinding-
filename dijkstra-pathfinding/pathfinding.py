from tkinter import messagebox, Tk  # Импортируем модуль tkinter для отображения сообщений
import pygame  # Импортируем библиотеку pygame для работы с графикой и событиями
import sys  # Импортируем модуль sys для завершения программы

window_width = 800  # Ширина окна
window_height = 800  # Высота окна

window = pygame.display.set_mode((window_width, window_height))  # Создаем окно с заданными размерами

columns = 50  # Количество столбцов в сетке
rows = 50  # Количество строк в сетке

box_width = window_width // columns  # Ширина одной ячейки сетки
box_height = window_height // rows  # Высота одной ячейки сетки

grid = []  # Сетка, содержащая все ячейки
queue = []  # Очередь для алгоритма поиска пути
path = []  # Список для хранения найденного пути


class Box:
    def __init__(self, i, j):
        self.x = i  # Координата x ячейки в сетке
        self.y = j  # Координата y ячейки в сетке
        self.start = False  # Является ли ячейка стартовой точкой
        self.wall = False  # Является ли ячейка стеной
        self.target = False  # Является ли ячейка целевой точкой
        self.queued = False  # Была ли ячейка добавлена в очередь
        self.visited = False  # Была ли ячейка посещена
        self.neighbours = []  # Список соседних ячеек
        self.prior = None  # Предыдущая ячейка на пути

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width,
                                      self.y * box_height, box_width - 2,
                                      box_height - 2))  # Рисуем ячейку с заданным цветом

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])  # Добавляем соседа слева
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])  # Добавляем соседа справа
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])  # Добавляем соседа сверху
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])  # Добавляем соседа снизу


# Создаем сетку
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))  # Создаем объект Box для каждой ячейки и добавляем в массив
    grid.append(arr)  # Добавляем массив ячеек в сетку

# Устанавливаем соседей для каждой ячейки
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()  # Устанавливаем соседей для текущей ячейки


def main():
    begin_search = False  # Флаг для начала поиска пути
    target_box_set = False  # Флаг, указывающий, что целевая точка установлена
    searching = True  # Флаг для продолжения поиска
    target_box = None  # Целевая ячейка
    start_box_set = False  # Флаг, указывающий, что стартовая точка установлена

    while True:
        for event in pygame.event.get():
            # Закрытие окна
            if event.type == pygame.QUIT:
                pygame.quit()  # Завершаем работу pygame
                sys.exit()  # Завершаем программу
            # Управление мышью
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левый клик мыши
                    x, y = pygame.mouse.get_pos()  # Получаем позицию курсора
                    i = x // box_width
                    j = y // box_height
                    if not start_box_set and not grid[i][j].wall:
                        start_box = grid[i][j]  # Устанавливаем стартовую ячейку
                        start_box.start = True
                        start_box.visited = True
                        queue.append(start_box)  # Добавляем стартовую ячейку в очередь
                        start_box_set = True

            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Рисуем стену
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                # Устанавливаем целевую точку
                if event.buttons[2] and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]  # Устанавливаем целевую ячейку
                    target_box.target = True
                    target_box_set = True
            # Начало алгоритма
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)  # Извлекаем первую ячейку из очереди
                current_box.visited = True
                if current_box == target_box:
                    searching = False  # Поиск завершен, если текущая ячейка - целевая
                    while current_box.prior != start_box:
                        path.append(current_box.prior)  # Восстанавливаем путь
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box  # Устанавливаем предшественника
                            queue.append(neighbour)  # Добавляем соседа в очередь
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")  # Сообщение, если решения нет
                    searching = False

        window.fill((0, 0, 0))  # Заполняем окно черным цветом

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (100, 100, 100))  # Рисуем ячейку серым цветом

                if box.queued:
                    box.draw(window, (200, 0, 0))  # Рисуем ячейку, добавленную в очередь, красным цветом
                if box.visited:
                    box.draw(window, (0, 200, 0))  # Рисуем посещенную ячейку зеленым цветом
                if box in path:
                    box.draw(window, (0, 0, 200))  # Рисуем путь синим цветом

                if box.start:
                    box.draw(window, (0, 200, 200))  # Рисуем стартовую ячейку бирюзовым цветом
                if box.wall:
                    box.draw(window, (10, 10, 10))  # Рисуем стену черным цветом
                if box.target:
                    box.draw(window, (200, 200, 0))  # Рисуем целевую ячейку желтым цветом

        pygame.display.flip()  # Обновляем экран


main()  # Запускаем основную функцию