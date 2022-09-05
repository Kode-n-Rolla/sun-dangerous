import pygame, random, sys
from pygame.locals import *

"""Игровые константы(размеры, скорость, цвета)"""
WINDOW_WIDTH = 600 # Ширина
WINDOW_HEIGHT = 600 # Высота
TEXT_COLOR = (0, 0, 0) # Цвет текста
BACKGROUND_COLOR = (255, 255, 255) # Цвет фона
FPS = 60 # Скорость игры
PROBLEMS_MIN_SIZE = 10 # Минимальный размер падающих элементов
PROBLEMS_MAX_SIZE = 40 # Максимальный размер падающих элементов
PROBLEMS_MIN_SPEED = 1 # Минимальная скорость п.э.
PROBLEMS_MAX_SPEED = 8 # Максимальная скорость п.э.
ADD_NEW_PROBLEMS = 6 # Добавление п.э.
PLAYER_MOVE_RATE = 5 # Кол-во пикселей при одном перемещении игрока

"""Функция закрытия игры"""
def terminate():
    pygame.quit()
    sys.exit()

"""Функция ожидания нажатия клавиши от игрока"""
def wait_for_player_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

"""Функция проверки соприкосновения игрока с падающими элементами"""
def player_touch_problems(player_rect, problems: list) -> bool:
    for p in problems:
        if player_rect.colliderect(p['rect']):
            return True
    return False

"""
Функция вывода на игровое поле переданную переменную text с параметрами:
font - шрифт
surface - объект, на котором будет отображаться текст
x, y - координаты отображения 
"""
def draw_text(text: str, font, surface, x: float, y: float):
    text_obj = font.render(text, 1, TEXT_COLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


pygame.init() # Запуск игры
main_clock = pygame.time.Clock() # Контроль скорость игры
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))#, pygame.FULLSCREEN)# Отображение игрового поля
pygame.display.set_caption('So L!fe') # Title игры
pygame.mouse.set_visible(False) # Видимость курсора мышки

# Настройка шрифтов
title_font = pygame.font.SysFont('Courier New', 50, True)
font = pygame.font.SysFont('Courier New', 30)
italics_font = pygame.font.SysFont('Times New Roman', 30, False, True)
instruction_font = pygame.font.SysFont('Courier New', 17)

# Настройка звуков
game_over_sound = pygame.mixer.Sound('gameover.wav')
lose_heart = pygame.mixer.Sound('bing.wav')
pygame.mixer.music.load('background.mid')

# Настройка изображений
player_image = pygame.image.load('player.png')
player_rect = player_image.get_rect()
problem_image = pygame.image.load('problem.png')
heart_image = pygame.image.load('heart.png')
heart_rect = heart_image.get_rect()

# Вывод начального экрана
window_surface.fill(BACKGROUND_COLOR)
draw_text('Sun Dangerous', title_font, window_surface, (WINDOW_WIDTH / 3) - 100, (WINDOW_HEIGHT / 3))
draw_text('Press any key to start.', italics_font, window_surface, (WINDOW_WIDTH / 5) + 40, (WINDOW_HEIGHT / 3) + 70)
draw_text('↑(w), ←(a), ↓(s), →(d), mouse - move', instruction_font, window_surface, (WINDOW_WIDTH / 3) - 85, 400)
draw_text('z & x - cheat cods', instruction_font, window_surface, (WINDOW_WIDTH / 3) + 5, 420)
draw_text('ESC - quit', instruction_font, window_surface, (WINDOW_WIDTH / 3) + 40, 440)

pygame.display.update()
wait_for_player_press_key()

top_score = 0
while True:
    problems = []
    score = 0
    HEARTS = 3 # Переменная кол-ва жизней игрока
    player_rect.topleft = (WINDOW_WIDTH / 2.2, WINDOW_HEIGHT - 50) # Первоначальное местоположение игрока
    move_left = move_right = move_up = move_down = False # Переменные перемещения игрока
    reverse_cheat = slow_cheat = False # Читы обратного движения и замедления п.э.
    problem_add_count = 0 # Переменная для добавления новых п.э.
    pygame.mixer.music.play(-1, 0.0) # Начало проигрывания фоновой музыки (-1 повтор, 0.0 - время начала проигрывания)

    while True:
        score += 1

        for event in pygame.event.get():
            # Проверка на событие выхода из игры
            if event.type == QUIT:
                terminate()
            # Проверка события на нажатие клавиши
            if event.type == KEYDOWN:
                # Проверка нажатия z и x для использования чит-кодов
                if event.key == K_z:
                    reverse_cheat = True
                if event.key == K_x:
                    slow_cheat = True
                # Нажатие клавиш перемещения
                if event.key == K_LEFT or event.key == K_a:
                    move_right = False
                    move_left = True
                if event.key == K_RIGHT or event.key == K_d:
                    move_right = True
                    move_left = False
                if event.key == K_UP or event.key == K_w:
                    move_down = False
                    move_up = True
                if event.key == K_DOWN or event.key == K_s:
                    move_up = False
                    move_down = True

            # Проверка события отжатия клавиш
            if event.type == KEYUP:
                if event.key == K_z:
                    reverse_cheat = False
                    score = 0 # Результат приравнивается 0, для того, чтобы играть честно
                if event.key == K_x:
                    slow_cheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT or event.key == K_a:
                    move_left= False
                if event.key == K_RIGHT or event.key == K_d:
                    move_right = False
                if event.key == K_UP or event.key == K_w:
                    move_up = False
                if event.key == K_DOWN or event.key == K_s:
                    move_down = False

            # Проверка события на движение мышки
            if event.type == MOUSEMOTION:
                player_rect.centerx = event.pos[0]
                player_rect.centery = event.pos[1]

        # Добавление новых п.э.
        if not reverse_cheat and not slow_cheat:
            problem_add_count += 1
        if problem_add_count == ADD_NEW_PROBLEMS:
            problem_add_count = 0
            # Создание п.э.
            problem_size = random.randint(PROBLEMS_MIN_SIZE, PROBLEMS_MAX_SIZE)
            new_problem = {'rect': pygame.Rect(
                            random.randint(0, WINDOW_WIDTH-problem_size), 0-problem_size, problem_size, problem_size),
                                'speed': random.randint(PROBLEMS_MIN_SPEED, PROBLEMS_MAX_SPEED),
                                'surface': pygame.transform.scale(problem_image, (problem_size, problem_size)),
                            }
            problems.append(new_problem)

        # Перемещение игрока
        if move_left and player_rect.left > 0:
            # move_ip(5,10) - переместит объект на 5 пикселей вправо и 10 вниз
            # move_ip(-5,-10) - переместит объект на 5 пикселей влево и 10 вверх
            player_rect.move_ip(-1 * PLAYER_MOVE_RATE, 0)
        if move_right and player_rect.right < WINDOW_WIDTH:
            player_rect.move_ip(PLAYER_MOVE_RATE, 0)
        if move_up and player_rect.top > 0:
            player_rect.move_ip(0, -1 * PLAYER_MOVE_RATE)
        if move_down and player_rect.bottom < WINDOW_HEIGHT:
            player_rect.move_ip(0, PLAYER_MOVE_RATE)

        # Перемещение п.э.
        for p in problems:
            if not reverse_cheat and not slow_cheat:
                p['rect'].move_ip(0, p['speed']) # Обычная скорость падения п.э.
            elif reverse_cheat: # Обратное движение п.э.
                p['rect'].move_ip(0, -5)
            elif slow_cheat:
                p['rect'].move_ip(0, 1) # Замедление п.э.

        # Удаление упавших за предел игрового поля п.э.
        for p in problems[:]:
            if p['rect'].top > WINDOW_HEIGHT:
                problems.remove(p)

        # Отображение в окне игрового поля
        window_surface.fill(BACKGROUND_COLOR)

        # Отображение кол-ва очков, лучшего результата и кол-ва жизней
        draw_text(f'Score: {score}', font, window_surface, 10, 0)
        draw_text(f'Top score: {top_score}', font, window_surface, 10, 40)
        draw_text(f'-{HEARTS}', font, window_surface, 530, 10)
        heart_rect.topleft = (500, 10)
        # Отображение спрайта жизней
        window_surface.blit(heart_image, heart_rect)

        # Оторбражение спрайта игрока
        window_surface.blit(player_image, player_rect)

        # Отображение спрайта каждого п.э.
        for p in problems:
            window_surface.blit(p['surface'], p['rect'])

        # Обновление окна
        pygame.display.update()

        # Проверка на столкновение
        if player_touch_problems(player_rect, problems):
            HEARTS -= 1 # -1 жизнь
            if HEARTS < 1:
                pygame.display.update()
                draw_text(f'-{HEARTS}', font, window_surface, 530, 10)
                if score > top_score:
                    top_score = score
                break

            lose_heart.play()
            draw_text(f'You still have {HEARTS} tries.', font, window_surface,
                                                (WINDOW_WIDTH / 3) - 100, (WINDOW_HEIGHT / 3) + 60)
            draw_text('Press key to continue.', font, window_surface,
                                                (WINDOW_WIDTH / 3) - 90, (WINDOW_HEIGHT / 3) + 100)
            pygame.display.update()
            wait_for_player_press_key()
            player_rect.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
            move_left = move_right = move_up = move_down = False
            reverse_cheat = slow_cheat = False
            problems = []

        main_clock.tick(FPS) # Приостановка игры для взаимодействия с игроком

    # Воспроизведения звуков, сигнализирующих окончание игры
    pygame.mixer.music.stop()
    game_over_sound.play()

    # Вывод текста на экран, говорящий о конце игры
    draw_text('GAME OVER!', title_font, window_surface, (WINDOW_WIDTH / 3) - 50, (WINDOW_HEIGHT / 3) + 35)
    draw_text('Press key to start a new game.', font, window_surface, (WINDOW_WIDTH / 3) - 160, (WINDOW_HEIGHT / 3) + 115)
    pygame.display.update()
    wait_for_player_press_key()

    game_over_sound.stop()