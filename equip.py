class Equip:
    def __init__(self, hp, damage_type, count, dice, name, level, type_char, nerf_dex, material,cast_cost):
        self.defence = hp
        self.damage_type = damage_type
        self.count = count
        self.dice = dice
        self.name = name
        self.level = level
        self.type_char = type_char
        self.nerf_dex = nerf_dex
        self.cost = round((dice * 2 + count * 10)*(level+1)/nerf_dex) if hp == 0 else (round((hp*4)*(level+1)*5/nerf_dex)
        if round((hp*4)*(level+1)*5/nerf_dex) < 1500 else round((hp*4)*level/nerf_dex))
        self.req = material
        self.cast_cost = cast_cost

class Jewellery:
    def __init__(self,name,defence):
        self.name = name
        self.res = defence


weapons = [Equip(0, ['phys', 'melee'], 1, 12,'Старый меч',0,'bod',1,None,0),
           Equip(0, ['phys', 'melee'], 1, 4, 'Кинжал',0,'bod',1,None,0),
           Equip(0, ['phys'], 1, 12, 'Старый лук',0,'dex',1,None,0),
           Equip(0, ['curse', 'melee'], 1, 12, 'Железный меч с проклятьем',0,'bod',1,None,0),
           Equip(0, ['phys', 'melee'], 1, 16,'Стальной меч',0,'bod',1,None,0),
           Equip(0, ['phys', 'melee'], 1, 20, 'Булова', 0, 'bod', 1.5,None,0),
           Equip(0, ['phys', 'melee'], 1, 24, 'Хороший железный меч', 3, 'bod', 1, None,0),
           Equip(0, ['phys', 'melee'], 1, 40, 'Секира', 3, 'bod', 2, None,0),
           Equip(0, ['phys'], 1, 10, 'Хороший лук', 3, 'dex', 1.5, None,0),
           Equip(0, ['phys', 'melee'], 1, 60, 'Боевой молот', 5, 'bod', 2.5, None,0),
           Equip(0, ['phys', 'melee'], 1, 30, 'Хороший стальной меч', 5, 'bod', 1.5, None,0),
           Equip(0, ['phys'], 1, 40, 'Арболет', 5, 'dex', 3, None,0),
           Equip(0, ['phys', 'melee'], 2, 30, 'Легкий стальной меч', 10, 'bod', 1, None,0),
           Equip(0, ['phys', 'melee'], 2, 60, 'Алебарда', 10, 'bod', 2, ['Желтый инврис'],0),
           Equip(0, ['phys', 'fire'], 2, 20, 'Механическая винтовка', 10, 'dex', 1, ['Желтый инврис','Ядро'],0),
           Equip(0, ['phys', 'melee','poison'], 3, 30, 'Ядовитый меч', 15, 'bod', 1, ['Ядовитый инврис'],3),
           Equip(0, ['phys', 'melee','fire'], 3, 30, 'Огненный меч', 15, 'bod', 1, ['Огненный инврис'],3),
           Equip(0, ['phys', 'melee','electro'], 4, 30, 'Магический меч', 25, 'bod', 1, ['Электрический инврис'],4),
           Equip(0, ['phys', 'melee','poison','fire','electro','space'], 8, 30, 'Инврисэнтовый меч', 50, 'bod', 1, ['Ядовитый инврис','Огненный инврис','Электрический инврис'],10),
           Equip(0, ['phys', 'melee','space'], 7, 30, 'Пространственный меч', 50, 'bod', 1, ['Пространственный инврис','Пространственный инврис'],6),
           Equip(0, ['phys', 'melee','curse'], 3, 30, 'Проклятый меч', 25, 'bod', 1, ["Проклятый инврис"],0),
           Equip(0, ['phys', 'melee','poison'], 5, 30, 'Сильно ядовитый меч', 35, 'bod', 1, ["Проклятый ядовитый инврис"],4),
           Equip(0, ['phys', 'melee','ice'], 5, 30, 'Ледяной меч', 25, 'bod', 1, ["Ледяной инврис"],5),
           Equip(0, ['phys'],0,0,'Пусто',0,'bod',1,None,0)]

weapons += []

armors = [Equip(10, ['air'], 0, 0,'Кольчуга',0,'bod',1,None,0),
         Equip(8, ['air'], 0, 0,'Проклеенный кожей доспех',0,'bod',1, None,0),
         Equip(6, ['air'], 0, 0, 'Кожаный доспех',0,'bod',1,None,0),
         Equip(0, ['air'],0,0,'Пусто',0,'bod',1,None,0),
         Equip(20, ['air'],0,0,'Латный доспех',5,'bod',1,None,0),
         Equip(30, ['air'],0,0,'Броня из желтого инвриса',10,'bod',1,['Желтый инврис','Желтый инврис'],0),
         Equip(50, ['air'],0,0,'Броня из пластин желтого инвриса',20,'bod',1,['Желтый инврис','Желтый инврис','Желтый инврис','Желтый инврис'],0),
         Equip(100, ['air'],0,0,'Броня из яда',25,'bod',1,['Ядовитая оболочка','Ядовитый инврис','Ядовитая трава'],0),
         Equip(200, ['air'],0,0,'Броня из металлического инвриса',35,'bod',1,["Металлический инврис","Металлический инврис",
                                                                              "Металлический камень","Металлический камень"],0),
         Equip(300, ['air'],0,0,'Пространственная броня',45,'bod',1,['Пространственный инврис','Пространственный инврис',
                                                                     'Инврис с замороженным пространством','Инврис с замороженным пространством'],0)]

jewelleries = []


all_equip = jewelleries+weapons+armors

all_weapon_names = [item.name for item in weapons]
all_armor_names = [item.name for item in armors]
all_jewelery_names = []
