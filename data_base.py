from CONSTANTS import CURSOR, CON


def new_game():  # новая игра
    new_game_statistics()
    CURSOR.execute('UPDATE progress SET player_pos = "46, 377", oxygen = 100, health = 100,\
     ship_1 = 0, ship_2 = 0, ship_3 = 0, ship_4 = 0, unknown_reactor = 0, was_died = 0')
    CON.commit()
    dict = {'steps': 0, 'monsters': 0, 'time': 0, 'bites': 0}
    return (46, 377), 100, 100, [0, 0, 0, 0, 0], dict
    # y и x поменялись местами


def new_save(pos_y, pos_x, ox, hp, progress, was_died, dict):  # создать новое сохранение
    save_statistics(dict)
    CURSOR.execute(f'UPDATE progress SET player_pos = "{pos_y}, {pos_x}", oxygen = {ox},\
     health = {hp}, ship_1 = {progress[0]}, ship_2 = {progress[1]},\
      ship_3 = {progress[2]}, ship_4 = {progress[3]}, unknown_reactor = {progress[4]},\
       was_died = "{was_died}"')
    CON.commit()


def get_save():  # получить сохраненные данные
    items = list(CURSOR.execute("SELECT * FROM progress").fetchall()[0])[:-2]
    pos = items.pop(0).split(', ')
    ox = items.pop(0)
    hp = items.pop(0)
    was_died = bool(items.pop(-1))
    progress = items
    return pos, ox, hp, progress, was_died


def get_music_volume():
    return CURSOR.execute("""SELECT music_volume FROM progress""").fetchone()[0]


def get_effects_volume():
    return CURSOR.execute("""SELECT effects_volume FROM progress""").fetchone()[0]


def set_music_volume(volume):
    CURSOR.execute("""UPDATE progress SET music_volume = music_volume + ?""", (volume,))
    CON.commit()


def set_effects_volume(volume):
    CURSOR.execute("""UPDATE progress SET effects_volume = effects_volume + ?""", (volume,))
    CON.commit()


def get_statistics():
    steps, monsters, time, bites = CURSOR.execute('SELECT * FROM statistics').fetchall()[0]
    print(steps, monsters, time, bites)
    dict = {'steps': steps, 'monsters': monsters, 'time': time, 'bites': bites}
    return dict


def new_game_statistics():
    CURSOR.execute('UPDATE statistics SET steps = 0, monsters = 0, time = 0, bites = 0')
    CON.commit()


def save_statistics(dict):
    CURSOR.execute(f'UPDATE statistics SET steps = {dict["steps"]},\
     monsters = {dict["monsters"]}, time = {dict["time"]}, bites = {dict["bites"]}')
    CON.commit()