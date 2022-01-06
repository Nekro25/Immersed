from CONSTANTS import *


def new_game():  # новая игра
    CURSOR.execute('UPDATE progress SET player_pos = "46, 377", oxygen = 100, health = 100,\
     ship_1 = "False", ship_2 = "False", ship_3 = "False", unknown_reactor = "False"')
    CON.commit()
    return (40, 366), 100, 100, [False, False, False, False]
    # y и x поменялись местами


def new_save(pos_y, pos_x, ox, hp, progress):  # создать новое сохранение
    CURSOR.execute(f'UPDATE progress SET player_pos = "{pos_y}, {pos_x}", oxygen = {ox},\
     health = {hp}, ship_1 = "{progress[0]}", ship_2 = "{progress[1]}",\
      ship_3 = "{progress[2]}", unknown_reactor = "{progress[3]}"')
    CON.commit()


def get_save():  # получить сохраненные данные
    items = list(CURSOR.execute("SELECT * FROM progress").fetchall()[0])
    pos = items.pop(0).split(', ')
    ox = items.pop(0)
    hp = items.pop(0)
    progress = items
    return pos, ox, hp, progress
