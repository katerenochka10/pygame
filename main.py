import os
import sys
import pygame
import pygame_menu
import random
import time

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60
x, y = 0, 0
ch = 0
ch1 = 0
ufoven_clojoncty = 0
result = 0
slojnost = 2000

pole = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]

f = open('data/map.txt', 'w+')
f.seek(0)
f.write('\n'.join([''.join(i) for i in pole]))
f.close()

def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку  клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global slojnost
    surface = pygame.display.set_mode((500, 500))

    def set_difficulty(value, difficulty):
        pass

    def start_the_game():
        def random_zvezdonos():
            global x, y
            f = open('data/map.txt', 'w+')
            pole[x][y] = '.'
            f.seek(0)
            x = random.randint(0, len(pole) - 1)
            y = random.randint(0, len(pole[x]) - 1)
            pole[x][y] = '#'
            f.write('\n'.join([''.join(i) for i in pole]))
            f.close()

        def get_click(samas):
            return get_cell(samas)

        def get_cell(mouse_pos):
            cell_x = (mouse_pos[0] - 0) // 50
            cell_y = (mouse_pos[1] - 0) // 50
            if cell_x < 0 or cell_x >= 50 or cell_y < 0 or cell_y >= 50:
                return None
            return cell_x, cell_y


        # Начало игры
        global x, y, ch, ch1, result
        f = open('data/map.txt', 'w+')
        f.seek(0)
        x = random.randint(0, len(pole) - 1)
        y = random.randint(0, len(pole[x]) - 1)
        pole[x][y] = '#'
        f.write('\n'.join([''.join(i) for i in pole]))
        f.close()
        player, level_x, level_y = generate_level(load_level('map.txt'))
        running = True
        MYEVENTTYPE = pygame.USEREVENT + 1
        pygame.time.set_timer(MYEVENTTYPE, slojnost)
        tic = time.perf_counter()
        while running:
            # внутри игрового цикла ещё один цикл
            # приема и обработки сообщений
            player, level_x, level_y = generate_level(load_level('map.txt'))
            for event in pygame.event.get():
                # при закрытии окна
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.K_ESCAPE:

                if ch1 < 30:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if get_click(event.pos) == (y, x):
                            ch += 1
                            ch1 += 1 # K_ESCAPE
                            random_zvezdonos()
                            pygame.time.set_timer(MYEVENTTYPE, slojnost)
                            pygame.display.flip()
                            print(ch)
                    if event.type == MYEVENTTYPE:
                        random_zvezdonos()
                        ch1 += 1
                elif ch1 == 30:
                    toc = time.perf_counter()
                    result = toc - tic
                    ch1 += 1
                    print(result)
            screen.fill('black')
            all_sprites.draw(screen)
            player_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()

    menu = pygame_menu.Menu('Отбери звезду ', 500, 500,
                            theme=pygame_menu.themes.THEME_GREEN)
    menu.add.label('у звездоноса')
    player_name = menu.add.text_input('Введите имя : ')
    sloj = menu.add.selector('Сложность:', [('Легко', 1), ('Средне', 2), ('Сложно', 3)], onchange=set_difficulty)
    menu.add.button('Играть', start_the_game)
    menu.add.button('Выход', pygame_menu.events.EXIT)
    if sloj[1]:
        slojnost = 5000
    elif sloj[2]:
        slojnost = 3500
    elif sloj[3]:
        slojnost = 2000
    print(slojnost, sloj)
    menu.mainloop(surface)


tile_images = {
    'wall': load_image('zvezdonos.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y

start_screen()