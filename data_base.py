from CONSTANTS import *


def new_game():  # новая игра
    CURSOR.execute('UPDATE progress SET player_pos = "46, 377", oxygen = 100, health = 100,\
     ship_1 = 0, ship_2 = 0, ship_3 = 0, ship_4 = 0, unknown_reactor = 0, was_died = 0')
    CON.commit()
    return (46, 377), 100, 100, [0, 0, 0, 0, 0]
    # y и x поменялись местами


def new_save(pos_y, pos_x, ox, hp, progress, was_died):  # создать новое сохранение
    CURSOR.execute(f'UPDATE progress SET player_pos = "{pos_y}, {pos_x}", oxygen = {ox},\
     health = {hp}, ship_1 = {progress[0]}, ship_2 = {progress[1]},\
      ship_3 = {progress[2]}, ship_4 = {progress[3]}, unknown_reactor = {progress[4]},\
       was_died = "{was_died}"')
    CON.commit()


def get_save():  # получить сохраненные данные
    items = list(CURSOR.execute("SELECT * FROM progress").fetchall()[0])
    pos = items.pop(0).split(', ')
    ox = items.pop(0)
    hp = items.pop(0)
    was_died = bool(items.pop(-1))
    progress = items
    return pos, ox, hp, progress, was_died
