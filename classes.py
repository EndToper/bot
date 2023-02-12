class GameClass:
    def __init__(self,
                 name: str,
                 physical_damage_bonus: float,
                 damage_by_arrows_bonus: float,
                 fire_damage_bonus: float,
                 water_damage_bonus: float,
                 electro_damage_bonus: float,
                 space_damage_bonus: float,
                 curses_damage_bonus: float,
                 heal_bonus: float,
                 ability_number,
                 type: str, ):
        self.pdb = physical_damage_bonus
        self.dab = damage_by_arrows_bonus
        self.fdb = fire_damage_bonus
        self.wdb = water_damage_bonus
        self.edb = electro_damage_bonus
        self.sdb = space_damage_bonus
        self.cdb = curses_damage_bonus
        self.heal = heal_bonus
        self.name = name
        self.ability_number = ability_number
        self.type = type


class Enemy:
    def __init__(self, name, hp: int, dex, damage, damage_type, resistance, drop, xp, boss):
        self.name = name
        self.hp = hp
        self.dex = dex
        self.dam = damage
        self.dam_type = damage_type
        self.res = resistance
        self.drop = drop
        self.xp = xp
        self.boss = boss


# {'fire':,'water':,'electro':,'poison':,'curse':,'phys':,'space':,'ice':,'heal':0,'melee':1}
# '':Enemy('',0,0,0,[''],{'fire':,'water':,'electro':,'poison':,'curse':,'phys':,'space':,'ice':,'heal':0,'melee':1},{},10,False)
drop_cost = {"Коготь":60,"Желтый инврис":20,"Шкура волка":70,"Ветка Лешего":1000,"Ядовитый инврис":20,"Слеза водного духа":360,
             "Ледяной инврис":150,"Хвост наги":700,"Проклятый инврис":350,"Тень":1000,"Демонический инврис":500,
             "Перо ворона-пересмешника":1230,"Призмариновый инврис":100,"Чернила, пропитанные инврисом":560,
             "Жидкость окаменения":2000,"Ядовитая трава":40,"Ядро":60,"Ядовитая оболочка":60,"Огненный инврис":120,
             "Электрический инврис":1000,"Корень мандрагоры":200,"Проклятый огненный инврис":1700,"Металлический камень":400,
             "Металлический инврис":400,"Огнекровь":450,"Лавовый инврис":450,'Заряженное ядро':800,
             'Воспламенившийся инврис':1000,'Проклятый ядовитый инврис':450,'Пространственный инврис':4000,
             'Инврис с замороженным пространством':8000}
basic_enemies = {'goblin': Enemy('Гоблин', 20, 4, 4, ['phys'],
                                 {'fire': 0.9, 'water': 0.9, 'electro': 0.9, 'poison': 0.9, 'curse': 0.9, 'phys': 0.8,
                                  'space': 0.85, 'ice': 0.9, 'heal': 0, 'melee': 1}, {'Коготь': 10, 'Желтый инврис': 5},
                                 10, False),
                 'wolf': Enemy('Волк', 35, 8, 6, ['phys'],
                               {'fire': 0.7, 'water': 1, 'electro': 0.7, 'poison': 1, 'curse': 0.7, 'phys': 1.2,
                                'space': 0.9, 'ice': 1, 'heal': 0, 'melee': 1},
                               {'Шкура волка': 50, 'Желтый инврис': 25}, 50, False),
                 'leshii': Enemy('Леший', 80, 15, 10, ['poison', 'phys'],
                                 {'fire': 0.5, 'water': 1, 'electro': 0.7, 'poison': 1, 'curse': 10, 'phys': 2,
                                  'space': 1.3, 'ice': 1, 'heal': 0, 'melee': 1}, {'Ветка Лешего': 100, 'Ядовитый инврис': 50},
                                 200, True),
                 'nakki': Enemy('Накки', 40, 8, 8, ['water'],
                                {'fire': 0.6, 'water': 1.5, 'electro': 0.5, 'poison': 1.1, 'curse': 1.1, 'phys': 1,
                                 'space': 0.9, 'ice': 0.8, 'heal': 0, 'melee': 1},
                                {'Ледяной инврис': 10, 'Слеза водного духа': 1}, 40, False),
                 'morgena': Enemy('Морге́на', 80, 10, 12, ['water'],
                                  {'fire': 0.7, 'water': 1.7, 'electro': 0.6, 'poison': 1.15, 'curse': 1.15, 'phys': 1,
                                   'space': 0.9, 'ice': 0.85, 'heal': 0, 'melee': 1},
                                  {'Ледяной инврис': 25, 'Слеза водного духа': 10}, 150, False),
                 'mermaid': Enemy('Русалка', 140, 12, 15, ['water'],
                                  {'fire': 0.9, 'water': 1.7, 'electro': 0.7, 'poison': 1.25, 'curse': 1.25, 'phys': 1,
                                   'space': 0.9, 'ice': 0.9, 'heal': 0, 'melee': 1},
                                  {'Ледяной инврис': 45, 'Слеза водного духа': 20}, 300, False),
                 'naga': Enemy('Воин наги', 90, 20, 10, ['poison'],
                               {'fire': 1, 'water': 1, 'electro': 0.7, 'poison': 2, 'curse': 0.8, 'phys': 0.75,
                                'space': 0.9, 'ice': 0.9, 'heal': 0, 'melee': 1},
                               {'Ядовитый инврис': 10, 'Хвост наги': 5}, 150, False),
                 'shadow': Enemy('Тень', 180, 12, 2, ['curse'],
                                 {'fire': 0.7, 'water': 0.7, 'electro': 0.7, 'poison': 2, 'curse': 2, 'phys': 1.5,
                                  'space': 0.9, 'ice': 0.7, 'heal': 0, 'melee': 1}, {'Проклятый инврис': 20, 'Тень': 5},
                                 250, False),
                 'raven-mockingbird': Enemy('Ворон-пересмешник', 290, 15, 20, ['poison', 'phys', 'curse'],
                                            {'fire': 3, 'water': 1.5, 'electro': 0.8, 'poison': 2, 'curse': 1.8,
                                             'phys': 0.9, 'space': 0.9, 'ice': 0.9, 'heal': 0, 'melee': 0.5},
                                            {'Демонический инврис': 10, 'Перо ворона-пересмешника': 10}, 400, False),
                 'long-necked-sea-serpent': Enemy('Длинношеий морской змей', 70, 15, 12, ['water'],
                                                  {'fire': 0.7, 'water': 1.7, 'electro': 0.5, 'poison': 1.6, 'curse': 1,
                                                   'phys': 1, 'space': 0.9, 'ice': 1.7, 'heal': 0, 'melee': 1},
                                                  {'Призмариновый инврис': 10}, 100, False),
                 'gigantic-octopus': Enemy('Гигантский осьминог', 140, 15, 14, ['water','poison'],
                                           {'fire': 0.7, 'water': 1.7, 'electro': 0.7, 'poison': 0.9, 'curse': 1,
                                            'phys': 1, 'space': 0.9, 'ice': 1.7, 'heal': 0, 'melee': 1.2},
                                           {'Призмариновый инврис': 40,'Чернила, пропитанные инврисом':25}, 200, False),
                 'gorgona': Enemy('Медуза Горгона', 300, 17, 2, ['curse'],
                                           {'fire': 1, 'water': 1, 'electro': 0.7, 'poison': 0.7, 'curse': 1.5,
                                            'phys': 0.7, 'space': 0.75, 'ice': 1, 'heal': 0, 'melee': 1.5},
                                           {'Призмариновый инврис': 80, 'Жидкость окаменения': 15,'Демонический инврис':10}, 500,
                                           False),
                 'parasite': Enemy('Травяной паразит', 25, 5, 4, ['poison','water'],
                                           {'fire': 0.5, 'water': 0.9, 'electro': 0.8, 'poison': 0.9, 'curse': 1,
                                            'phys': 1, 'space': 0.9, 'ice': 1, 'heal': 0, 'melee': 0.8},
                                           {'Ядовитый инврис': 10,'Ядовитая трава':25}, 10, False),
                 'poison-slime': Enemy('Ядовитая слизь', 35, 10, 8, ['poison','phys'],
                                           {'fire': 0.5, 'water': 0.9, 'electro': 0.8, 'poison': 1.2, 'curse': 1,
                                            'phys': 1.2, 'space': 0.3, 'ice': 0.8, 'heal': 0, 'melee': 1.8},
                                           {'Ядовитый инврис': 50,'Ядро':50,'Ядовитая оболочка':5}, 50, False),
                 'flower-fairy': Enemy('Дух цветов', 50, 8, 10, ['fire','water','ice','electro'],
                                           {'fire': 1.1, 'water': 1.1, 'electro': 1.2, 'poison': 0.7, 'curse': 0.7,
                                            'phys': 0.75, 'space': 0.8, 'ice': 1.1, 'heal': 0, 'melee': 1},
                                           {'Огненный инврис': 25,'Ледяной инврис': 15,'Электрический инврис': 5,
                                            'Призмариновый инврис': 5}, 90, False),
                 'mandragora': Enemy('Мандрагора', 90, 7, 15, ['phys'],
                                           {'fire': 1, 'water': 1, 'electro': 0.8, 'poison': 0.7, 'curse': 0.7,
                                            'phys': 1.75, 'space': 0.8, 'ice': 1, 'heal': 0, 'melee': 1},
                                           {'Желтый инврис':50,'Корень мандрагоры':40}, 140, False),
                 'flower-fairy-king': Enemy('Король духов цветов', 290, 10, 15, ['fire','water','ice','electro'],
                                           {'fire': 1.2, 'water': 1.2, 'electro': 1.3, 'poison': 0.7, 'curse': 0.7,
                                            'phys': 0.75, 'space': 0.9, 'ice': 1.2, 'heal': 0, 'melee': 1},
                                           {'Огненный инврис': 30,'Ледяной инврис': 20,'Электрический инврис': 10,
                                            'Призмариновый инврис': 15,'Проклятый огненный инврис':10}, 290, False),
                 'dryad': Enemy('Древесный живой инврис', 400, 15, 20, ['electro','poison','phys'],
                                {'fire': 0.8, 'water': 1, 'electro': 1.2, 'poison': 0.7, 'curse': 1.2,
                                 'phys': 0.75, 'space': 0.9, 'ice': 1, 'heal': 0, 'melee': 1},
                                {'Проклятый ядовитый инврис': 35,'Электрический инврис': 25,'Желтый инврис': 15},
                                200, False),
                 'envrisent': Enemy('Инврисэнт', 600, 25, 20, ['curse','poison','phys'],
                                {'fire': 0.8, 'water': 1, 'electro': 1.2, 'poison': 0.7, 'curse': 1.2,
                                 'phys': 0.5, 'space': 0.9, 'ice': 1, 'heal': 0, 'melee': 1},
                                {'Проклятый ядовитый инврис': 50,'Проклятый инврис': 45,'Желтый инврис': 25},
                                500, False),
                 'elder-envrisent': Enemy('Древний инврисэнт', 700, 20, 30, ['curse','poison','phys'],
                                {'fire': 1.4, 'water': 1.8, 'electro': 1.4, 'poison': 1, 'curse': 1.2,
                                 'phys': 2, 'space': 0.9, 'ice': 1.3, 'heal': 0, 'melee': 1},
                                {'Проклятый ядовитый инврис': 85,'Проклятый инврис': 75,'Желтый инврис': 50,'Пространственный инврис':5},
                                800, True),
                 'distortion-envrisent': Enemy('Искаженный инврисэнт', 750, 25, 25, ['electro','fire','poison','phys'],
                                {'fire': 1.8, 'water': 1, 'electro': 1.2, 'poison': 0.7, 'curse': 1.2,
                                 'phys': 0.75, 'space': 0.5, 'ice': 1, 'heal': 0, 'melee': 1},
                                {'Проклятый ядовитый инврис': 35,'Пространственный инврис': 45,'Желтый инврис': 15},
                                550, False),
                 'fused-distortion-envrisent': Enemy('Сросшиеся искаженные инврисэнты', 1000, 17, 55,
                                                     ['water','electro','poison','phys'],
                                {'fire': 1.8, 'water': 2, 'electro': 2.2, 'poison': 1.7, 'curse': 2.2,
                                 'phys': 1.75, 'space': 1.0, 'ice': 1, 'heal': 0, 'melee': 1},
                                {'Проклятый ядовитый инврис': 35,'Пространственный инврис': 85,'Инврис с замороженным пространством': 65},
                                900, False),
                 'stonlem': Enemy('Камнелем', 80, 8, 40, ['phys'],
                                {'fire': 1.2, 'water': 1.8, 'electro': 1.5, 'poison': 1.7, 'curse': 2.2,
                                 'phys': 1.75, 'space': 0.5, 'ice': 1, 'heal': 0, 'melee': 1},
                                {'Желтый инврис': 55,'Металлический инврис': 75,'Металлический камень': 35},
                                190, False),
                 'salamandra': Enemy('Саламандра', 240, 8, 40, ['phys','fire'],
                                {'fire': 2.2, 'water': 1, 'electro': 0.7, 'poison': 1.7, 'curse': 2.2,
                                 'phys': 1.75, 'space': 0.8, 'ice': 0.5, 'heal': 0, 'melee': 1},
                                {'Желтый инврис': 55,'Лавовый инврис': 75,'Огнекровь': 35},
                                290, False),
                 'anchimayen': Enemy('Анчимайен, мальчик-шаровая-молния', 440, 30, 25, ['phys','electro'],
                                {'fire': 0.7, 'water': 0.6, 'electro': 2.7, 'poison': 1, 'curse': 1.2,
                                 'phys': 1.75, 'space': 0.8, 'ice': 0.5, 'heal': 0, 'melee': 1},
                                {'Желтый инвриc': 55,'Электрический инврис': 100,'Заряженное ядро': 35,'Воспламенившийся инврис':1},
                                490, False)
                 }

