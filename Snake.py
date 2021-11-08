import pygame
from pygame import *
import random
from time import sleep
import time
import turtle
from googleapiclient.discovery import build
from google.oauth2 import service_account
import re




# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 480  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
#ЦВЕТА
BACKGROUND_COLOR = "#ffffff"
WHITE_COLOR = (255, 255, 255)
GREEN_COLOR = (0, 255, 0)
GRAY_COLOR = (128, 128, 128)
BLACK_COLOR = (0, 0, 0)
APPLE_COLOR = (219,180,61)

# Размеры и отрисовка поля
SQUARE_WIDTH = SQUARE_HEIGHT = 39 #поле квадратное 40 на 40 пикселей с рамкой в 1 пиксель
SQUARE_MARGIN = 1 # рамка в 1 пиксель
SQUARE_COLOR = "#FF6262"






def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    pygame.font.init()  # Инициация текста, обязательно нужно вызывать в начале
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    #pygame.display.set_caption("Snake")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом
    myfont = pygame.font.SysFont('Comic Sans MS', 50) # фонт для pygame.font.init()

    OPTIONS_MUSIC = False #опции включение/отключение музыки в начале игры
    OPTIONS_ACCELERATION = True #опции включение/отключение ускорения в начале игры
    Loginscreen = True  # страница загрузки
    start_timer = time.time()  # таймер
    TIMER_TEXT = True  # переменная для таймера текста
    RATING_TEXT = True #переменна для текста рейтинга
    PLAYER_IN_TOP = False # переменная игрока который в топ 10 рейтинга
    CHECK_DUPLICATE = False # проверка дублирующей записи с игроком
    DUPLICATE_FOUND = False # переменная, когда дублирующая запись найдена
    y_rating = 100 #положение текста рейтинга по у
    userID = open('userID.txt', encoding='utf-8') #открываем файл с ником
    NICKNAME = userID.read() #присваиваем значение из файла (в начале пустое, т.к. ник не введен)
    score = 0 #счёт пока 0

    #rating = [[NICKNAME, score]] #для формирования рейтинга для добавления в гугл шитс

    # Google Sheets
    SERVICE_ACCOUNT_FILE = 'keys.json'  # обозначаем ключ доступа к таблице
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # ресурс на котором таблица находится
    creds = None  # задаем переменную None (хз зачем)
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)  # задаем в переменную ключ и ресурс
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1A5cf_Cwz688MrwN_ki0gh6nZB7xttkEJ8bmqkL-1zvQ'  # это наша таблица в https://docs.google.com/
    # SAMPLE_RANGE_NAME = 'Class Data!A2:E'
    service = build('sheets', 'v4', credentials=creds)  # хз (компонуем все в сервис походу)
    # Call the Sheets API
    sheet = service.spreadsheets()  # переменная для упрощения без нее можно было бы написать service.spreadsheets()

    #=================Получение данных по РЕЙТИНГУ ====================================================================

    data_nick = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                   range="snake_rating!C1:D10",
                                   valueRenderOption='UNFORMATTED_VALUE').execute()  # сбор результата всей таблицы
    player_values = data_nick.get('values', [])  # компоновка результата игроков таблицы в список
    data_nick = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                   range="snake_rating!E1:E10",
                                   valueRenderOption='UNFORMATTED_VALUE').execute()  # сбор результата всей таблицы
    score_values = data_nick.get('values', [])  # компоновка результата очков таблицы в список


    #==================Получение данных для дубликатов имён ===========================================================

    data_nick = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                   range="snake_rating!A:A",
                                   valueRenderOption='UNFORMATTED_VALUE').execute()  # сбор результата всей таблицы
    players_values = data_nick.get('values',
                                   [])  # компоновка результата игроков таблицы в список
    data_nick = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                   range="snake_rating!B:B",
                                   valueRenderOption='UNFORMATTED_VALUE').execute()  # сбор результата всей таблицы
    scores_values = data_nick.get('values', [])  # компоновка результата очков таблицы в список

    #==================================================================================================================

    def update():
        rating = [[NICKNAME, str(score)]]  # для формирования рейтинга для добавления в гугл шитс
        sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='snake_rating!A1',
                                        valueInputOption='USER_ENTERED',
                                        body={'values': rating}).execute()  # ввод результата


    def add():
        rating = [[NICKNAME, str(score)]]  # для формирования рейтинга для добавления в гугл шитс
        sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='snake_rating!A1',
                                         valueInputOption='USER_ENTERED', insertDataOption='OVERWRITE',
                                         body={'values': rating}).execute()
    while Loginscreen:
        timer = time.time() - start_timer  # Начало отсчета времени в секундах (настоящее время - время старта)
        if not NICKNAME.isalpha():  # Если в имени содержатся знаки не из алфавита
            NICKNAME = None  # возвращаем дефолтное значение
        while NICKNAME == 'None' or NICKNAME == None or NICKNAME == '': #пока ник не введен
            accfont = pygame.font.SysFont('Comic Sans MS', 30)  # фонт для pygame.font.init()
            textsurface = accfont.render('в имени не должно быть пробелов', False, (0, 0, 0))
            screen.blit(textsurface, (180, 180))  # выводим на экран в координатах ху
            turtle.setup(0, 0) #устанавливаем размеры окна туртл для ввода данных
            wn = turtle.Screen() #создаем окно
            NICKNAME = wn.textinput("Имя", "Введите ваше имя:") #создаем диалоговое окно для ввода имени
            if NICKNAME: #если имя введено
                if not NICKNAME.isalpha(): # Если в имени содержатся знаки не из алфавита
                    accfont = pygame.font.SysFont('Comic Sans MS', 30)  # фонт для pygame.font.init()
                    textsurface = accfont.render('максимальная длина имени 8 символов', False, (0, 0, 0))
                    screen.blit(textsurface, (180, 180))  # выводим на экран в координатах ху
                    textsurface = accfont.render('в имени не должно быть пробелов и цифр', False, (255, 145, 50))
                    screen.blit(textsurface, (180, 180))  # выводим на экран в координатах ху
                    pygame.display.update()  # обновление и вывод всех изменений на экран
                    NICKNAME = None #возвращаем дефолтное значение
                else:
                    max_symbols = len(NICKNAME)  # получаем длину слова
                    if max_symbols <= 8: #если меньше или равно 8 буквам
                        accfont = pygame.font.SysFont('Comic Sans MS', 30)  # фонт для pygame.font.init()
                        textsurface = accfont.render('в имени не должно быть пробелов и цифр', False, (0, 0, 0))
                        screen.blit(textsurface, (180, 180))  # выводим на экран в координатах ху
                        textsurface = accfont.render('максимальная длина имени 8 символов', False, (0, 0, 0))
                        screen.blit(textsurface, (180, 180))  # выводим на экран в координатах ху
                        pygame.display.update()  # обновление и вывод всех изменений на экран
                        userID = open('userID.txt', 'w', encoding='utf-8')  # открываем для записи .тхт
                            # записываем в фаил никнейм (он сохранится, чтобы потом не вводить заного)
                        userID.write(NICKNAME)
                        userID.close() #закрываем файл
                        turtle.bye()  # закрываем окно туртл

                    else:
                        accfont = pygame.font.SysFont('Comic Sans MS', 30)  # фонт для pygame.font.init()
                        textsurface = accfont.render('в имени не должно быть пробелов', False, (0, 0, 0))
                        screen.blit(textsurface, (180, 180))  # выводим на экран в координатах ху
                        textsurface = accfont.render('максимальная длина имени 8 символов', False, (255, 145, 50))
                        screen.blit(textsurface, (180, 180))  # выводим на экран в координатах ху
                        pygame.display.update()  # обновление и вывод всех изменений на экран
                        NICKNAME = None #возвращаем дефолтное значение

        if not CHECK_DUPLICATE:
            CHECK_DUPLICATE = True
            for i in range(9):
                if not PLAYER_IN_TOP:  # проверка если не найден игрок в топ 10
                    # перебираем имена и переводим в строку без лишних символов
                    player_name = re.sub(r'([][`, .1234567890\'])', r'' '', str(player_values[i]))
                    if str(player_name) == str(NICKNAME):  # если имя игрока совпадает с введенным никнеймом
                        name_index = i  # сохраняем индекс записи
                        PLAYER_IN_TOP = True  # переменная найденного игрока
                else:
                    # перебираем дальше имена и переводим в строку без лишних символов
                    player_name = re.sub(r'([][`, .1234567890\'])', r'' '', str(player_values[i]))
                    if str(player_name) == str(NICKNAME):  # если имя игрока совпадает с введенным никнеймом
                        duplicate_index = i  # сохраняем индекс дубликата
                        # переводим счёт игрока в строку
                        duplicate_score = re.sub(r'([][`,\'])', r'' '', str(score_values[duplicate_index]))
                        try:
                            for i in range(9999): # Перебираем имена и счёт игроков
                                duplicate_player_name = re.sub(r'([][`, .:1234567890\'])', r'' '', str(players_values[i]))
                                duplicate_scores_values = re.sub(r'([][`:,\'])', r'' '', str(scores_values[i]))
                                # Если дубликат из рейтинга равен дубликату из списка очков и игроков
                                if str(duplicate_score) == str(duplicate_scores_values) and str(duplicate_player_name) == str(NICKNAME):
                                    # т.к. индекс начинается с 0, а ячейки с 1, то прибавляем 1 к индексу
                                    duplicate_cell_index = i + 1
                                    # Создаем запрос для удаления из таблицы гугл
                                    SAMPLE_SPREADSHEET_CELL = 'snake_rating!A' + str(duplicate_cell_index) + ':B' + str(duplicate_cell_index)
                                    sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                         range=SAMPLE_SPREADSHEET_CELL).execute()
                                    DUPLICATE_FOUND = True

                        except IndexError:
                            break

        if RATING_TEXT:
            if DUPLICATE_FOUND: # Если дублирующая запись найдена, то сделать запрос еще раз
                DUPLICATE_FOUND = False
                data_nick = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                               range="snake_rating!C1:D10",
                                               valueRenderOption='UNFORMATTED_VALUE').execute()  # сбор результата всей таблицы
                player_values = data_nick.get('values', [])  # компоновка результата игроков таблицы в список
                data_nick = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                               range="snake_rating!E1:E10",
                                               valueRenderOption='UNFORMATTED_VALUE').execute()  # сбор результата всей таблицы
                score_values = data_nick.get('values', [])  # компоновка результата очков таблицы в список
                # ВЫВОД НА ЭКРАН ТАБЛИЦЫ РЕЙТИНГА
            RATING_TEXT = False
            y_rating -= 10
            rating_font = pygame.font.SysFont('Comic Sans MS', 20)  # фонт для pygame.font.init()
            textsurface = rating_font.render('RATINGS: ', False, (255, 145, 50))
            screen.blit(textsurface, (10, y_rating))  # выводим на экран в координатах ху
            y_rating += 10
            try:
                for i in range(9):
                    y_rating += 20
                    textsurface = rating_font.render(re.sub(r'([][`,\'])', r'' '', str(player_values[i])), False, (255, 145, 50))
                    screen.blit(textsurface, (20, y_rating))  # выводим на экран в координатах ху
                    textsurface = rating_font.render(re.sub(r'([][`,\'])', r' ' '', str(score_values[i])), False, (255, 145, 50))
                    screen.blit(textsurface, (140, y_rating))  # выводим на экран в координатах ху
            except IndexError:
                pass


        if TIMER_TEXT:
            textsurface = myfont.render('Вы не ввели имя...', False, (0, 0, 0))  # создаем текстуру с текстом
            screen.blit(textsurface, (40, 40))  # выводим на экран в координатах ху
            pygame.display.update()  # обновление и вывод всех изменений на экран
            textsurface = myfont.render('SNAIL TAIL', False, (40, 255, 0))  # создаем текстуру с текстом
            screen.blit(textsurface, (240, 40))  # выводим на экран в координатах ху
            pygame.display.update()  # обновление и вывод всех изменений на экран
            end_timer_text = timer + 1
            end_timer_text2 = timer + 2
            TIMER_TEXT = False
        if timer >= end_timer_text:
            textsurface = myfont.render('SNAIL TAIL', False, (0, 0, 0))  # создаем текстуру с текстом
            screen.blit(textsurface, (240, 40))  # выводим на экран в координатах ху
            pygame.display.update()  # обновление и вывод всех изменений на экран
            if timer >= end_timer_text2:
                TIMER_TEXT = True

        textsurface = myfont.render(str(NICKNAME), False, (255, 200, 50))  # создаем текстуру с текстом
        screen.blit(textsurface, (40, 400))  # выводим на экран в координатах ху
        pygame.display.update()  # обновление и вывод всех изменений на экран
        textsurface = myfont.render('start game', False, (255, 0, 50))  # создаем текстуру с текстом
        screen.blit(textsurface, (240, 240))  # выводим на экран в координатах ху
        pygame.display.update()  # обновление и вывод всех изменений на экран

        if OPTIONS_ACCELERATION:
            accfont = pygame.font.SysFont('Comic Sans MS', 30)  # фонт для pygame.font.init()
            textsurface = accfont.render('acceleration OFF', False, (0, 0, 0))  # создаем текстуру с текстом
            screen.blit(textsurface, (240, 180))  # выводим на экран в координатах ху
            textsurface = accfont.render('acceleration ON', False, (255, 0, 50))  # создаем текстуру с текстом
            screen.blit(textsurface, (240, 180))  # выводим на экран в координатах ху
            pygame.display.update()  # обновление и вывод всех изменений на экран
        else:
            accfont = pygame.font.SysFont('Comic Sans MS', 30)  # фонт для pygame.font.init()
            textsurface = accfont.render('acceleration ON', False, (0, 0, 0))  # создаем текстуру с текстом
            screen.blit(textsurface, (240, 180))  # выводим на экран в координатах ху
            textsurface = accfont.render('acceleration OFF', False, (255, 0, 50))  # создаем текстуру с текстом
            screen.blit(textsurface, (240, 180))  # выводим на экран в координатах ху
            pygame.display.update()  # обновление и вывод всех изменений на экран

        if OPTIONS_MUSIC:
            musfont = pygame.font.SysFont('Comic Sans MS', 30)  # фонт для pygame.font.init()
            textsurface = musfont.render('music OFF', False, (0, 0, 0))  # создаем текстуру с текстом
            screen.blit(textsurface, (520, 180))  # выводим на экран в координатах ху
            textsurface = musfont.render('music ON', False, (255, 0, 50))  # создаем текстуру с текстом
            screen.blit(textsurface, (520, 180))  # выводим на экран в координатах ху
            pygame.display.update()  # обновление и вывод всех изменений на экран
        else:
            musfont = pygame.font.SysFont('Comic Sans MS', 30)  # фонт для pygame.font.init()
            textsurface = musfont.render('music ON', False, (0, 0, 0))  # создаем текстуру с текстом
            screen.blit(textsurface, (520, 180))  # выводим на экран в координатах ху
            textsurface = musfont.render('music OFF', False, (255, 0, 50))  # создаем текстуру с текстом
            screen.blit(textsurface, (520, 180))  # выводим на экран в координатах ху
            pygame.display.update()  # обновление и вывод всех изменений на экран


        for event in pygame.event.get():  # Обрабатываем события
            if event.type == QUIT:
                raise SystemExit ("QUIT")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                if 520 <= x_mouse <= 650 and 163 <= y_mouse <= 216:
                    OPTIONS_MUSIC ^= True
                    if OPTIONS_MUSIC:
                        pygame.mixer.music.load('sounds\JustSimplySong.mp3')  # Проигрываем музыку
                        pygame.mixer.music.play(-1, 0.0)  # зацикливание
                    else:
                        pygame.mixer.music.stop()



                if 245 <= x_mouse <= 460 and 163 <= y_mouse <= 216:
                    OPTIONS_ACCELERATION ^= True

                if 250 <= x_mouse <= 450 and 264 <= y_mouse <= 345:
                    textsurface = myfont.render(str(NICKNAME), False, (0, 0, 0))  # создаем текстуру с текстом
                    screen.blit(textsurface, (40, 400))  # выводим на экран в координатах ху
                    textsurface = myfont.render('SNAIL TAIL', False, (0, 0, 0))  # создаем текстуру с текстом
                    screen.blit(textsurface, (240, 40))  # выводим на экран в координатах ху
                    accfont = pygame.font.SysFont('Comic Sans MS', 30)  # фонт для pygame.font.init()
                    textsurface = accfont.render('acceleration OFF', False, (0, 0, 0))  # создаем текстуру с текстом
                    screen.blit(textsurface, (240, 180))  # выводим на экран в координатах ху
                    textsurface = accfont.render('acceleration ON', False, (0, 0, 0))  # создаем текстуру с текстом
                    screen.blit(textsurface, (240, 180))  # выводим на экран в координатах ху
                    textsurface = myfont.render('start game', False, (0, 0, 0))  # создаем текстуру с текстом
                    screen.blit(textsurface, (240, 240))  # выводим на экран в координатах ху
                    musfont = pygame.font.SysFont('Comic Sans MS', 30)  # фонт для pygame.font.init()
                    textsurface = musfont.render('music ON', False, (0, 0, 0))  # создаем текстуру с текстом
                    screen.blit(textsurface, (520, 180))  # выводим на экран в координатах ху
                    textsurface = musfont.render('music OFF', False, (0, 0, 0))  # создаем текстуру с текстом
                    screen.blit(textsurface, (520, 180))  # выводим на экран в координатах ху
                    y_rating = 100 #устанавливаем изначальые координаты для таблицы рейтинга
                    y_rating -= 10 # повторяем все манипуляции только с черным цветом
                    rating_font = pygame.font.SysFont('Comic Sans MS', 20)  # фонт для pygame.font.init()
                    textsurface = rating_font.render('RATINGS: ', False, (0, 0, 0))
                    screen.blit(textsurface, (10, y_rating))  # выводим на экран в координатах ху
                    y_rating += 10
                    try:

                        for i in range(10):
                            y_rating += 20
                            textsurface = rating_font.render(re.sub(r'([][`,\'])', r'' '', str(player_values[i])),
                                                             False, (0, 0, 0))
                            screen.blit(textsurface, (20, y_rating))  # выводим на экран в координатах ху
                            textsurface = rating_font.render(re.sub(r'([][`,\'])', r' ' '', str(score_values[i])),
                                                             False, (0, 0, 0))
                            screen.blit(textsurface, (140, y_rating))  # выводим на экран в координатах ху
                    except IndexError:
                        pass
                    pygame.display.update()  # обновление и вывод всех изменений на экран
                    Loginscreen = False  # страница загрузки


    # Навигация в начале
    RIGHT = True
    DOWN = False
    LEFT = False
    UP = False
    button_pressed = True

    #Яблоко
    APPLE = False #обозначаем, что в начале яблока на поле нет
    #Длина змейки
    TAIL = 3 #хвост змейки
    start_timer = time.time() #таймер
    loop_count = 0
    PRAISE = 40 #переменная для фразы восхваления (easy , not bad, awesome, unstoppable, godlike, etc)
    ACCELERATION = False #ускорения в начале нет
    TIMER_TEXT = True #переменная для таймера текста
    x = 40 #Начальные координаты спавна змейки по х
    y = 240 #Начальные координаты спавна змейки по у
    mas = [] #создаем пустой массив для отрисовки змейки (квадаратов 40 на 40)
    mas_a = [] #создаем отдельный массив для отрисовки яблок (на всякий случай)
    mas_coord_x = [] #создаем массив с координатами x для записи последовательности изменения координат
    mas_coord_y = [] #создаем массив с координатами y для записи последовательности изменения координат
    ONE_CALL = True #переменная одного обращения к звуковому файлу
    AUTO = False #Режим автоматизации
    clock = pygame.time.Clock() #время в секундах и фпс

    while True:  # Основной цикл программы
        loop_count += 1 #переменная для отсчета старта
        if loop_count == 4:
            if OPTIONS_ACCELERATION: #если в опция включена аккселерация
                ACCELERATION = True
        if ACCELERATION: #ускорение в начале
            speed = 10 # скорость 0.1 сек
            if TAIL >= 25: # на 25 длине хвоста скорость становится 0.1 сек
                speed = (1 * TAIL) / 2.5 #возврат к базовому ускорению
        else:
            speed = (1 * TAIL) / 2.5 # базовое ускорение
        snake_speed = speed # вывод скорости в шапку

        if AUTO: #если авто режим
            if TAIL>= 150:
                clock.tick(speed)  # реальная скорость
            else:
                clock.tick(240)  # быстрая скорость чтоб не ждать
        else:
            clock.tick(speed)  # реальная скорость


        timer = time.time() - start_timer  # Начало отсчета времени в секундах (настоящее время - время старта)
        score = str("{:.0f}".format(speed * TAIL * timer ))
        # пишем в шапку инфу (название, скорость итд)
        pygame.display.set_caption('SNAKE               ' + 'SPEED: ' + str("{:.0f}".format(snake_speed)) +
                                   '    SCORE: ' + str(score) +'     TAIL: '+str(TAIL))

        mas_coord_x_all = mas_coord_x.copy() #копируем список всех значений массива х в переменную
        mas_coord_y_all = mas_coord_y.copy() #копируем список всех значений массива y в переменную

        # Обрабатываем события
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit("QUIT")

            elif event.type == pygame.KEYDOWN: #событие нажатия кнопки
                if event.key == pygame.K_SPACE: # если нажат пробел
                    ACCELERATION ^= True #переключаем аккселерацию (ускорение змейки)
                if event.key == pygame.K_RIGHT:
                    if LEFT or button_pressed: # если нажата левая клавиша или в этом цикле уже была нажата клавиша
                        pass
                    else:
                        button_pressed = True #в противном случае нажимаем клавишу
                        RIGHT = True
                        LEFT = False
                        UP = False
                        DOWN = False
                if event.key == pygame.K_DOWN:
                    if UP or button_pressed:
                        pass
                    else:
                        button_pressed = True
                        RIGHT = False
                        LEFT = False
                        UP = False
                        DOWN = True
                if event.key == pygame.K_LEFT:
                    if RIGHT or button_pressed:
                        pass
                    else:
                        button_pressed = True
                        RIGHT = False
                        LEFT = True
                        UP = False
                        DOWN = False
                if event.key == pygame.K_UP:
                    if DOWN or button_pressed:
                        pass
                    else:
                        button_pressed = True
                        RIGHT = False
                        LEFT = False
                        UP = True
                        DOWN = False

        button_pressed = False  # Проверка нажатия кнопки для ограничения нажатия еще одной кнопки за один цикл

        #Тестовая автоматизация для проверки на ошибки
        if AUTO:
            if x >= 760:
                RIGHT = False
                if UP:
                    LEFT = True
                    UP = False
                else:
                    UP = True
            if x <= 0:
                LEFT = False
                if UP:
                    RIGHT = True
                    UP = False
                else:
                    UP = True





        # ЛОГИКА ПОВОРОТОВ
        if RIGHT: #если движение направо то х + 40 (один шаг змейки)
            if x >= 760: #если координаты за экраном
                x = 0 #измегняем на 0 (с другой стороны экрана)
            else:
                x = x + 40 #Шаг змейки
        if DOWN:
            if y >= 440:
                y = 0
            else:
                y = y + 40 #Шаг змейки
        if LEFT:
            if x <= 0:
                x = 760
            else:
                x = x - 40 #Шаг змейки
        if UP:
            if y <= 0:
                y = 440
            else:
                y = y - 40 #Шаг змейки

        #НАЧАЛЬНЫЙ ОТСЧЁТ
        if loop_count == 1:
            textsurface = myfont.render(' READY', False, (40, 255, 0))  # создаем текстуру с текстом
            screen.blit(textsurface, (280, 160))  # выводим на экран в координатах ху
            pygame.display.update()  # обновление и вывод всех изменений на экран
            sleep(1) #ждем секунду
        if loop_count == 2:
            textsurface = myfont.render(' READY', False, (0, 0, 0))  # убираем текстуру с текстом
            screen.blit(textsurface, (280, 160))  # выводим на экран в координатах ху
            pygame.display.update()  # обновление и вывод всех изменений на экран
            textsurface = myfont.render('STEADY', False, (40, 255, 0))  # создаем текстуру с текстом
            screen.blit(textsurface, (280, 160))  # выводим на экран в координатах ху
            pygame.display.update()  # обновление и вывод всех изменений на экран
            sleep(1) #ждем секунду
        if loop_count == 3:
            textsurface = myfont.render('STEADY', False, (0, 0, 0))  # убираем текстуру с текстом
            screen.blit(textsurface, (280, 160))  # выводим на экран в координатах ху
            pygame.display.update()  # обновление и вывод всех изменений на экран
            textsurface = myfont.render('GO', False, (40, 255, 0))  # создаем текстуру с текстом
            screen.blit(textsurface, (340, 160))  # выводим на экран в координатах ху
            pygame.display.update()  # обновление и вывод всех изменений на экран
        if loop_count == 14:
            textsurface = myfont.render('GO', False, (0, 0, 0))  # создаем текстуру с текстом
            screen.blit(textsurface, (340, 160))  # выводим на экран в координатах ху
            pygame.display.update()  # обновление и вывод всех изменений на экран



        # создание текста за достижения (Streaks)
        if TAIL >= PRAISE: #если хвост больше переменной PRAISE
            if TIMER_TEXT: #если таймер для текста еще не активирован
                end_timer_text = timer + 1 #записываем один раз в таймер значение в 1 секунду
                TIMER_TEXT = False #больше не обращаемся сюда
            elif PRAISE == 40: #если PRAISE 15, то пишем текст
                if ONE_CALL: #если истинно, то обращаемся
                    dominating_sound = pygame.mixer.Sound('sounds/dominating.mp3') #назначаем звук
                    dominating_sound.play(0) #проигрываем 1 раз
                    ONE_CALL = False  # больше сюда не обращаемся
                textsurface = myfont.render('Dominating!', False, (40, 255, 0)) #создаем текстуру с текстом
                screen.blit(textsurface, (280, 0)) #выводим на экран в координатах ху
                pygame.display.update()  # обновление и вывод всех изменений на экран

            elif PRAISE == 60:
                if ONE_CALL:  # если истинно, то обращаемся
                    unstop_sound = pygame.mixer.Sound('sounds/unstop.mp3')
                    unstop_sound.play(0)
                    ONE_CALL = False  # больше сюда не обращаемся
                textsurface = myfont.render('Unstoppable!', False, (40, 255, 0))
                screen.blit(textsurface, (280, 0))

            elif PRAISE == 80:
                if ONE_CALL:  # если истинно, то обращаемся
                    wicked_sound = pygame.mixer.Sound('sounds/wicked.mp3')
                    wicked_sound.play(0)
                    ONE_CALL = False  # больше сюда не обращаемся
                textsurface = myfont.render('Wicked sick!', False, (255, 215, 0))
                screen.blit(textsurface, (280, 0))
            elif PRAISE == 100:
                if ONE_CALL:  # если истинно, то обращаемся
                    godlike_sound = pygame.mixer.Sound('sounds/godlike.mp3')
                    godlike_sound.play(0)
                    ONE_CALL = False  # больше сюда не обращаемся
                textsurface = myfont.render('Godlike!', False, (252, 15, 192))
                screen.blit(textsurface, (280, 0))
            elif PRAISE == 120:
                if ONE_CALL:  # если истинно, то обращаемся
                    holy_sound = pygame.mixer.Sound('sounds/holy.mp3')
                    holy_sound.play(0)
                    ONE_CALL = False  # больше сюда не обращаемся
                textsurface = myfont.render('Holy shit!', False, (8, 232, 222))
                screen.blit(textsurface, (240, 0))
            elif PRAISE == 140:
                if ONE_CALL:  # если истинно, то обращаемся
                    ownage_sound = pygame.mixer.Sound('sounds/ownage.mp3')
                    ownage_sound.play(0)
                    ONE_CALL = False  # больше сюда не обращаемся
                textsurface = myfont.render('Ownage!', False, (255, 0, 51))
                screen.blit(textsurface, (240, 0))
            if timer >= end_timer_text: #если прошло больше секунды с момента появления текста
                if not APPLE: # если на поле нет яблока
                    PRAISE += 20 #прибавляем переменную до следующего достижения
                    ONE_CALL = True #переменная для обращения к след звуку по цепочке
                    TIMER_TEXT = True #переменная для обращения к след таймеру для текста по цепочке
                    if PRAISE == 60:
                        textsurface = myfont.render('Dominating!', False, (0, 0, 0))  # убираем текстуру с текстом
                        screen.blit(textsurface, (280, 0))  # выводим на экран в координатах ху
                    elif PRAISE == 80:
                        textsurface = myfont.render('Unstoppable!', False, (0, 0, 0))
                        screen.blit(textsurface, (280, 0))  # выводим на экран в координатах ху
                    elif PRAISE == 100:
                        textsurface = myfont.render('Wicked sick!', False, (0, 0, 0))
                        screen.blit(textsurface, (280, 0))  # выводим на экран в координатах ху
                    elif PRAISE == 120:
                        textsurface = myfont.render('Godlike!', False, (0, 0, 0))
                        screen.blit(textsurface, (280, 0))  # выводим на экран в координатах ху
                    elif PRAISE == 140:
                        textsurface = myfont.render('Holy shit!', False, (0, 0, 0))
                        screen.blit(textsurface, (240, 0))
                    elif PRAISE == 160:
                        if OPTIONS_MUSIC:
                            pygame.mixer.music.stop()  # останавливаем музыку
                            pygame.mixer.music.load('sounds\KorsakovFlightoftheBumblebee.mp3')  # Проигрываем музыку
                            pygame.mixer.music.play(0, 0.0)  # зацикливание

                        textsurface = myfont.render('Ownage!', False, (0, 0, 0))
                        screen.blit(textsurface, (240, 0))
                    pygame.display.update()  # обновление и вывод всех изменений на экран






        # ЛОГИКА ЗМЕЙКИ
        #рисуем зеленый квадрат на экране
        mas.append(pygame.draw.rect(screen, GREEN_COLOR, (x, y, SQUARE_WIDTH, SQUARE_HEIGHT)))
        pygame.display.update()  # обновление и вывод всех изменений на экран
        mas_coord_x.append(x) #добавляем в массив координаты х
        mas_coord_y.append(y) #добавляем в массив координаты у
        if len(mas_coord_x) > TAIL: #Если индекс массива больше хвоста
            TAIL_x = mas_coord_x[0] #Присваиваем переменной х нулевой индекс
            TAIL_y = mas_coord_y[0] #Присваиваем переменной у нулевой индекс

            if TAIL_x == APPLE_X and TAIL_y == APPLE_Y: #если совпадают координаты с яблоком
                pass #то не рисуем черный квадрат
            else:
                # рисуем черный квадрат и удаляем 0 индекс, т.к. там больше нет хвоста
                mas.append(pygame.draw.rect(screen, BLACK_COLOR, (TAIL_x, TAIL_y, SQUARE_WIDTH, SQUARE_HEIGHT)))
            pygame.display.update()  # обновление и вывод всех изменений на экран
            mas_coord_x.pop(0) # удаляем нулевой индекс x
            mas_coord_y.pop(0) # удаляем нулевой индекс y


        # Логика создания яблока
        if not APPLE:  # если нет яблока создаем в рандомной точке
            APPLE_X = random.randint(0, 19) * 40
            APPLE_Y = random.randint(0, 11) * 40
            COORDINATE_BLOCKED = False  # переменная если произошел респ яблока на змейке
            try:
                for i in range(TAIL):  # цикл для перебора всех индексов в зависимости от длины хвоста
                    # если координаты респа яблока равны координатам в массиве змейки
                    if APPLE_X == mas_coord_x_all[i] and APPLE_Y == mas_coord_y_all[i]:
                        COORDINATE_BLOCKED = True  # координаты заблокированы
                        break
                if not COORDINATE_BLOCKED:  # если координаты незаблокированы
                    # рисуем яблоко
                    mas_a.append(pygame.draw.rect(screen, APPLE_COLOR, (APPLE_X, APPLE_Y, SQUARE_WIDTH, SQUARE_HEIGHT)))
                    pygame.display.update()  # обновление и вывод всех изменений на экран
                    APPLE = True  # обозначаем что яблоко есть
            except IndexError:
                pass
        else:  # если яблоко есть
            if x == APPLE_X and y == APPLE_Y:  # если голова совпадает с точкой координат яблока
                TAIL = TAIL + 1  # прибавляем 1 хвост
                apple_sounds = ['sounds/eating-apple1.mp3', 'sounds/eating-apple2.mp3',
                                'sounds/eating-apple3.mp3','sounds/eating-apple4.mp3','sounds/eating-apple5.mp3',
                                'sounds/eating-apple6.mp3','sounds/eating-apple7.mp3']  #записываем массив звуков
                apple_sound = pygame.mixer.Sound(apple_sounds[random.randint(0, 6)]) # проигрываем рандомный звук
                apple_sound.play(0)
                mas_a.pop(0)  # удаляем индекс из массива яблока
                APPLE = False  # обозначаем, что яблока нет


        #Логика повреждений
        # Получение координат головы и хвоста
        index = 0 #Индекс
        for i in range(TAIL): # цикл для перебора всех индексов в зависимости от длины хвоста
            try:
                if x == mas_coord_x_all[index] and y == mas_coord_y_all[index]: #Находим соответствие координат ху
                    if PLAYER_IN_TOP: # если игрок в топ 10
                        min_score = re.sub(r'([][`,\'])', r'' '', str(score_values[name_index])) # получаем его очки
                        if int(min_score) < int(score):  # если набранные очки больше пердыдущих то
                            add()  # добавляем запись
                    else:  # если игрок не в топ 10
                        min_score = re.sub(r'([][`,\'])', r'' '', str(score_values[9]))  # узнаем 10 место в рейтинге
                        if int(min_score) < int(score):   #  если 10 место меньше чем набранные очки то
                            add()                 #    добавляем запись
                    pygame.mixer.music.stop()  # останавливаем музыку
                    pygame.mixer.music.load('sounds\game-over.wav')  # Проигрываем музыку
                    pygame.mixer.music.play(0, 0.0)  # зацикливание 0
                    myfont = pygame.font.SysFont('Comic Sans MS', 70)  # фонт для pygame.font.init()
                    textsurface = myfont.render('YOU LOOSE (-_-)', True, (255, 0, 51))
                    screen.blit(textsurface, (80, 40))
                    pygame.display.update()  # обновление и вывод всех изменений на экран
                    sleep(1)
                    textsurface = myfont.render('YOU SCORE: ' + str(score), True, (255, 0, 51))
                    screen.blit(textsurface, (40, 200))
                    pygame.display.update()  # обновление и вывод всех изменений на экран
                    sleep(2)
                    myfont = pygame.font.SysFont('Comic Sans MS', 50)  # фонт для pygame.font.init()
                    textsurface = myfont.render('press space to new game', True, (255, 0, 51))
                    screen.blit(textsurface, (120, 360))
                    pygame.display.update()  # обновление и вывод всех изменений на экран
                    LOOSE = True
                    while LOOSE:
                        # Обрабатываем события снова
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                raise SystemExit("QUIT")
                            elif event.type == pygame.KEYDOWN:  # событие нажатия кнопки
                                if event.key == pygame.K_SPACE:  # если нажат пробел
                                    # если эта переменная установлена в True , откроется окно черепахи,
                                    # если нет, вы получите ошибку turtle.Terminator
                                    turtle._RUNNING = True
                                    main() #перезапуск кода

                else:
                    index += 1 #если не нашли, то индекс + 1
            except IndexError: #Исключение необходимо, т.к в начале массив только записывается
                pass

        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
