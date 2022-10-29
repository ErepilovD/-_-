import pygame as pg
from heapq import *
from random import random


def get_circle(x, y): # создание круг
    return (x * TILE + TILE // 2, y * TILE + TILE // 2), TILE // 4


def get_rect(x, y): # создание квадрата
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


def get_next_nodes(x, y): # проверяем наличие соседа
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]


def heuristic(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])


cols, rows = 5, 5 # определяем кол-во ячеек
TILE = 100 # задаем размер ячейке

pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()



grid = ['87654','76543','65432','54321','43210'] # манхэтенское расстояние
grid = [[int(char) for char in string ] for string in grid]
grid = [[True if random() < 0.2  else False for col in range(cols)] for row in range(cols)] #определяем создание препятствий(стен)
graph = {}

for y, row in enumerate(grid): # проверяем наличие соседей для каждого элемента  и составляем из этого массив
    for x, col in enumerate(row):
        graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# начальные параметры
start = (0, 0)
goal = (4 ,4)
queue = []
heappush(queue, (0, start))
cost_visited = {start: 0}
visited = {start: None}

bg = pg.image.load('img2.png').convert() # ФОН 
bg = pg.transform.scale(bg, (cols * TILE, rows * TILE))

max_tile = 0
max_vertex = 0
Win = 0

while True:
    # заполняем экран
    sc.blit(bg, (0, 0))
    # раскрашиваем клетки
    [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5) for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
    [pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y), 1) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(*xy)) for _, xy in queue]
    pg.draw.circle(sc, pg.Color('purple'), *get_circle(*goal))

    # сохраним максимальное количество вершин графа ей пришлось одновременно удерживать в памяти
    if len(visited) > max_tile:
        max_tile = len(visited)
    
    # сохраним количество вершин графа ей пришлось раскрыть
    if len(visited) > max_vertex:
        max_vertex = len(visited)

    # Деикстра
    if queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            queue = []
            continue

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            neigh_cost, neigh_node = next_node
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + heuristic(neigh_node, goal)
                heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node

    clock.tick(5)
    # отрисовка
    path_head, path_segment = cur_node, cur_node
    while path_segment:
        pg.draw.circle(sc, pg.Color('brown'), *get_circle(*path_segment))
        path_segment = visited[path_segment]
    pg.draw.circle(sc, pg.Color('blue'), *get_circle(*start))
    pg.draw.circle(sc, pg.Color('magenta'), *get_circle(*path_head))

    if get_rect(*path_head) == get_rect(*goal):
        break
    if Win == get_rect(*path_head):
        Win = True
        break
    else:
        Win = get_rect(*path_head)


    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(10)

if Win == True:
    print('\nYou shall not pass!!! © Гендальф')
else:
    print('\nАлгоритм дошелдо конца. Хоть кто-то...')

print('Максимальное количество вершин графа в памяти:' + str(max_tile))
print('Количество вершин графа раскрыто:' + str(max_vertex))
print('По этим квадратам ходим:', visited.keys())
