class Equip:
    def __init__(self, hp, damage_type, count, dice, name, level, type_char, nerf_dex, materials, cast_cost):
        self.defence = hp
        self.damage_type = damage_type
        self.count = count
        self.dice = dice
        self.name = name
        self.level = level
        self.type_char = type_char
        self.nerf_dex = nerf_dex
        self.cost = round((dice * 2 + count * 10) * (level + 1) / nerf_dex) if hp == 0 else (
            round((hp * 4) * (level + 1) * 5 / nerf_dex)
            if round((hp * 4) * (level + 1) * 5 / nerf_dex) < 1500 else round((hp * 4) * level / nerf_dex))
        self.req = materials
        self.cast_cost = cast_cost


class Jewellery:
    def __init__(self, name, resistance, cost, materials):
        self.name = name
        self.res = resistance
        self.cost = cost
        self.req = materials
        self.level = round(cost/100)


weapons = [Equip(0, ['phys', 'melee'], 1, 12, 'Старый меч', 0, 'bod', 1, None, 0),
           Equip(0, ['phys', 'melee'], 1, 8, 'Кинжал', 0, 'bod', 1, None, 0),
           Equip(0, ['phys'], 1, 12, 'Старый лук', 0, 'dex', 1, None, 0),
           Equip(0, ['curse', 'melee'], 1, 12, 'Железный меч с проклятьем', 0, 'bod', 1, None, 0),
           Equip(0, ['phys', 'melee'], 1, 16, 'Стальной меч', 0, 'bod', 1, None, 0),
           Equip(0, ['phys', 'melee'], 1, 20, 'Булава', 0, 'bod', 1.5, None, 0),
           Equip(0, ['phys', 'melee'], 1, 24, 'Хороший железный меч', 3, 'bod', 1, None, 0),
           Equip(0, ['phys', 'melee'], 1, 40, 'Секира', 3, 'bod', 2, None, 0),
           Equip(0, ['phys'], 1, 10, 'Хороший лук', 3, 'dex', 1.5, None, 0),
           Equip(0, ['phys', 'melee'], 1, 60, 'Боевой молот', 5, 'bod', 2.5, None, 0),
           Equip(0, ['phys', 'melee'], 1, 30, 'Хороший стальной меч', 5, 'bod', 1.5, None, 0),
           Equip(0, ['phys'], 1, 40, 'Арбалет', 5, 'dex', 3, None, 0),
           Equip(0, ['phys', 'melee'], 2, 30, 'Легкий стальной меч', 10, 'bod', 1, None, 0),
           Equip(0, ['phys', 'melee'], 2, 60, 'Алебарда', 10, 'bod', 2, ['Желтый инврис'], 0),
           Equip(0, ['phys', 'fire'], 2, 20, 'Механическая винтовка', 10, 'dex', 1,
                 ['Желтый инврис', 'Желтый инврис', 'Желтый инврис', 'Ядро'], 0),
           Equip(0, ['phys', 'melee', 'poison'], 3, 30, 'Ядовитый меч', 15, 'bod', 1,
                 ['Ядовитый инврис', 'Ядовитый инврис', 'Ядовитый инврис', 'Ядовитый инврис'], 3),
           Equip(0, ['phys', 'melee', 'fire'], 3, 30, 'Огненный меч', 15, 'bod', 1,
                 ['Огненный инврис', 'Огненный инврис', 'Огненный инврис', 'Огненный инврис'], 3),
           Equip(0, ['phys', 'water'], 3, 20, 'Водная пушка', 15, 'dex', 0.9,
                 ['Призмариновый инврис', 'Призмариновый инврис', 'Призмариновый инврис', 'Призмариновый инврис',
                  'Призмариновый инврис', 'Желтый инврис', 'Ядро'], 2),
           Equip(0, ['phys'], 3, 40, 'Желтый арбалет', 15, 'dex', 2.5,
                 ['Желтый инврис', 'Желтый инврис', 'Желтый инврис', 'Желтый инврис', 'Желтый инврис', 'Желтый инврис'],
                 0),
           Equip(0, ['phys'], 3, 50, 'Желтая булава', 15, 'bod', 3.5,
                 ['Желтый инврис', 'Желтый инврис', 'Желтый инврис', 'Желтый инврис', 'Желтый инврис', 'Желтый инврис'],
                 0),
           Equip(0, ['phys', 'melee', 'electro'], 4, 30, 'Магический электрический меч', 25, 'bod', 1.5,
                 ['Электрический инврис', 'Электрический инврис', 'Электрический инврис', 'Электрический инврис'], 4),
           Equip(0, ['phys', 'melee', 'curse'], 3, 30, 'Проклятый меч', 25, 'bod', 1.2,
                 ["Проклятый инврис", "Проклятый инврис", "Проклятый инврис", "Проклятый инврис"], 0),
           Equip(0, ['phys', 'melee', 'ice'], 4, 30, 'Ледяной меч', 25, 'bod', 1.2, ["Ледяной инврис"], 5),
           Equip(0, ['space', 'electro', 'phys', 'poison'], 5, 30, 'Электроарбалет с ядовитыми стрелами', 25, 'dex',
                 2.5,
                 ['Электрический инврис', 'Электрический инврис', 'Желтый инврис', 'Желтый инврис', 'Желтый инврис',
                  "Ядовитая трава", "Ядовитая трава", "Ядро", "Ядро"], 6),
           Equip(0, ['phys', 'electro'], 4, 30, 'Электромагическая винтовка', 25, 'dex', 1,
                 ['Электрический инврис', 'Электрический инврис', 'Электрический инврис', 'Электрический инврис',
                  "Ядро", "Ядро"], 4),
           Equip(0, ['phys', 'melee', 'poison'], 5, 30, 'Сильно ядовитый кинжал', 35, 'bod', 1.5,
                 ["Проклятый ядовитый инврис", "Проклятый ядовитый инврис", "Проклятый ядовитый инврис",
                  "Проклятый ядовитый инврис"], 4),
           Equip(0, ['phys', 'melee'], 10, 30, 'Инврисововый железный молот', 35, 'bod', 5.5,
                 ["Металлический камень", "Металлический камень", "Металлический камень", "Металлический камень",
                  "Металлический инврис", "Металлический инврис", "Металлический инврис"], 0),
           Equip(0, ['phys', 'fire'], 5, 35, 'Лавовая винтовка', 35, 'dex', 1,
                 ["Лавовый инврис", "Лавовый инврис", "Лавовый инврис", "Огнекровь", "Огнекровь",
                  'Проклятый огненный инврис', "Огненный инврис", "Ядро", "Ядро"], 4),
           Equip(0, ['phys', 'melee', 'poison', 'fire', 'electro', 'space'], 8, 20, 'Инврисэнтовый меч', 50, 'bod', 1.5,
                 ['Ядовитый инврис', 'Огненный инврис', 'Электрический инврис', 'Ядовитый инврис', 'Огненный инврис',
                  'Электрический инврис', 'Ядовитый инврис', 'Огненный инврис', 'Электрический инврис',
                  'Пространственный инврис', "Ветка Лешего"], 20),
           Equip(0, ['phys', 'melee', 'space'], 7, 30, 'Пространственный меч', 50, 'bod', 1.7,
                 ['Пространственный инврис', 'Пространственный инврис', "Ветка Лешего"], 6),
           Equip(0, ['phys', 'poison', 'electro', 'curse'], 6, 35, 'Ядовитая винтовка', 50, 'dex', 1,
                 ["Ядро", "Ядро", "Ядро", 'Ядовитый инврис', 'Ядовитый инврис', 'Ядовитый инврис',
                  'Электрический инврис', 'Электрический инврис', 'Проклятый огненный инврис', 'Желтый инврис',
                  'Желтый инврис', 'Желтый инврис'], 6),
           Equip(0, ['phys'], 0, 0, 'Пусто', 0, 'bod', 1, None, 0)]

weapons += [Equip(0, ['phys', 'poison', 'water'], 6, 40, 'Лук Лешего', 0, ['dex'], 1,
                  ['Воспламенившийся инврис', "Ветка Лешего", "Ветка Лешего", "Ветка Лешего", "Ветка Лешего",
                   'Проклятый ядовитый инврис', 'Проклятый ядовитый инврис'], 0),
            Equip(0, ['space', 'curse', 'water'], 2, 100, 'Амулет [Чары сирен]', 0, 'int', 1,
                  ['Воспламенившийся инврис', "Слеза водного духа", "Слеза водного духа", "Слеза водного духа",
                   'Сердце сирены'], 10),
            Equip(0, ['space', 'melee', 'phys'], 1, 100, 'Теневой клинок', 0, ['dex', 'bod'], 1,
                  ['Воспламенившийся инврис', "Тень", "Тень", "Тень", "Тень", "Тень", "Тень", "Тень", "Ветка Лешего"],
                  2),
            Equip(0, ['space', 'curse', 'fire', 'electro', 'ice', 'water', 'poison', 'heal'], 30, 30,
                  'Зачарованное перо', 0, 'int', 1,
                  ['Воспламенившийся инврис', "Перо ворона-пересмешника", "Перо ворона-пересмешника",
                   "Перо ворона-пересмешника", "Проклятый инврис", "Проклятый инврис", "Проклятый инврис",
                   "Проклятый инврис"], 1),
            Equip(0, ['space'], 1, 800, 'Инврисовая тетрадь', 0, 'dex', 1,
                  ['Воспламенившийся инврис', "Чернила, пропитанные инврисом", "Чернила, пропитанные инврисом",
                   "Чернила, пропитанные инврисом", "Чернила, пропитанные инврисом", "Чернила, пропитанные инврисом",
                   "Проклятый инврис", "Проклятый инврис", "Проклятый инврис"], 20),
            Equip(0, ['space', 'curse'], 100, 3, 'Щит Горгоны', 0, ['dex', 'bod'], 1,
                  ['Воспламенившийся инврис', 'Жидкость окаменения', 'Жидкость окаменения', 'Жидкость окаменения',
                   'Демонический инврис', 'Демонический инврис', "Желтый инврис", "Желтый инврис", "Желтый инврис"], 5),
            Equip(0, ['space'], 100, 10, 'Искажающий пространство шар', 0, 'dex', 1,
                  ['Воспламенившийся инврис', 'Пространственный инврис', 'Пространственный инврис',
                   'Пространственный инврис', 'Пространственный инврис', 'Пространственный инврис',
                   'Пространственный инврис', 'Инврис с замороженным пространством',
                   'Инврис с замороженным пространством'], 50),
            Equip(0, ['space', 'electro'], 20, 20, 'Цепной электромеч', 0, ['dex', 'bod'], 1,
                  ['Воспламенившийся инврис', 'Заряженное ядро', "Ядро", "Ядро", "Ядро", "Ядро", 'Электрический инврис',
                   'Электрический инврис', 'Электрический инврис', 'Электрический инврис', 'Электрический инврис',
                   'Электрический инврис', 'Электрический инврис', 'Электрический инврис', 'Электрический инврис',
                   'Электрический инврис'], 7),
            Equip(0, ['space', 'phys'], 10, 40, 'Магическая винтовка', 0, ['dex'], 1,
                  ['Воспламенившийся инврис', 'Пространственный инврис', 'Пространственный инврис',
                   'Пространственный инврис', 'Пространственный инврис', 'Пространственный инврис',
                   'Пространственный инврис', 'Инврис с замороженным пространством',
                   'Инврис с замороженным пространством'], 5)]

armors = [Equip(0, ['air'], 0, 0, 'Пусто', 0, 'bod', 1, None, 0),
          Equip(6, ['air'], 0, 0, 'Кожаный доспех', 0, 'bod', 1, None, 0),
          Equip(8, ['air'], 0, 0, 'Проклеенный кожанный доспех', 0, 'bod', 1, None, 0),
          Equip(10, ['air'], 0, 0, 'Кольчуга', 0, 'bod', 1, None, 0),
          Equip(20, ['air'], 0, 0, 'Латный доспех', 5, 'bod', 1, None, 0),
          Equip(30, ['air'], 0, 0, 'Броня из желтого инвриса', 10, 'bod', 1, ['Желтый инврис', 'Желтый инврис'], 0),
          Equip(50, ['air'], 0, 0, 'Пропитанная инврисом шкура волка', 10, 'bod', 1,
                ['Желтый инврис', "Шкура волка", "Шкура волка", "Шкура волка"], 0),
          Equip(75, ['air'], 0, 0, 'Броня из пластин желтого инвриса', 20, 'bod', 1,
                ['Желтый инврис', 'Желтый инврис', 'Желтый инврис', 'Желтый инврис'], 0),
          Equip(125, ['air'], 0, 0, 'Броня из яда', 25, 'bod', 1,
                ['Ядовитая оболочка', 'Ядовитый инврис', 'Ядовитая трава'], 0),
          Equip(220, ['air'], 0, 0, 'Броня из металлического инвриса', 35, 'bod', 1,
                ["Металлический инврис", "Металлический инврис",
                 "Металлический камень", "Металлический камень"], 0),
          Equip(310, ['air'], 0, 0, 'Пространственная броня', 45, 'bod', 1,
                ['Пространственный инврис', 'Пространственный инврис',
                 'Инврис с замороженным пространством', 'Инврис с замороженным пространством'], 0)]

jewelleries = [Jewellery("Пусто",
                         {'fire': 1, 'water': 1, 'electro': 1, 'poison': 1, 'curse': 1, 'phys': 1, 'space': 1, 'ice': 1,
                          'heal': 1, 'melee': 1}, 0, None),
               Jewellery("Коготь гоблина",
                         {'fire': 1, 'water': 1, 'electro': 1, 'poison': 1, 'curse': 1, 'phys': 1, 'space': 1, 'ice': 1,
                          'heal': 1, 'melee': 1.3}, 100, ["Коготь","Коготь"]),
               Jewellery("Зачарованный коготь гоблина",
                         {'fire': 1, 'water': 1, 'electro': 1, 'poison': 1, 'curse': 1, 'phys': 1.1, 'space': 1, 'ice': 1,
                          'heal': 1, 'melee': 1.5}, 250, ["Коготь","Коготь","Коготь","Желтый инврис","Желтый инврис","Желтый инврис","Желтый инврис","Желтый инврис"]),
               Jewellery("Ядовитая подвеска",
                         {'fire': 0.8, 'water': 1.05, 'electro': 1, 'poison': 1.3, 'curse': 1, 'phys': 1.05, 'space': 1, 'ice': 1,
                          'heal': 1, 'melee': 1}, 150, ["Ядовитый инврис","Ядовитый инврис","Ядовитый инврис","Ядовитая трава","Ядовитая трава","Ядовитая оболочка","Ядовитая оболочка"]),
               Jewellery("Цветочный амулет",
                         {'fire': 1.05, 'water': 1.05, 'electro': 1.1, 'poison': 0.9, 'curse': 0.9, 'phys': 0.85, 'space': 1, 'ice': 1.05,
                          'heal': 1, 'melee': 1}, 1000, ['Огненный инврис','Ледяной инврис','Призмариновый инврис','Электрический инврис']),
               Jewellery("Обработанная слеза водного духа",
                         {'fire': 0.9, 'water': 1.5, 'electro': 0.9, 'poison': 1, 'curse': 1, 'phys': 1, 'space': 1, 'ice': 1.2,
                          'heal': 1, 'melee': 1}, 1000, ['Ледяной инврис','Ледяной инврис',"Слеза водного духа"]),
               Jewellery("Слеза сирены",
                         {'fire': 0.85, 'water': 1.2, 'electro': 0.85, 'poison': 1, 'curse': 0.9, 'phys': 1, 'space': 1, 'ice': 1.2,
                          'heal': 1.5, 'melee': 1}, 1000, ["Слеза водного духа","Слеза водного духа","Слеза водного духа","Слеза водного духа",'Сердце сирены']),
               ]

all_equip = jewelleries + weapons + armors

all_weapon_names = [item.name for item in weapons]
all_armor_names = [item.name for item in armors]
all_jewelery_names = [item.name for item in jewelleries]
