import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((500, 500))


def set_difficulty(value, difficulty):
    pass


def start_the_game():
    # Начало игры
    pass


menu = pygame_menu.Menu('Отбери звезду ', 500, 500,
                                        theme = pygame_menu.themes.THEME_GREEN)
menu.add.label('у звездоноса')
menu.add.text_input('Ваше имя:', default='Игрок1')
menu.add.selector('Сложность:', [('Легко', 1), ('Средне', 2), ('Сложно', 3)], onchange=set_difficulty)
menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)

menu.mainloop(surface)
