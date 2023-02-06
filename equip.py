class Equip:
    def __init__(self, hp, damage_type, count, dice, title, name, level, type_char):
        self.defence = hp
        self.damage_type = damage_type
        self.count = count
        self.dice = dice
        self.title = title
        self.name = name
        self.level = level
        self.type_char = type_char


weapons = [Equip(0, ['phys', 'melee'], 1, 6, 'old-sword','Старый меч',0,'bod'),
           Equip(0, ['phys', 'melee'], 1, 4, 'dagger','Кинжал',0,'bod'),
           Equip(0, ['phys'], 1, 6, 'old-bow','Старый лук',0,'dex'),
           Equip(0, ['curse', 'melee'], 1, 6, 'iron_sword_cursed','Железный меч с проклятьем',0,'bod'),
           Equip(0, ['phys'],0,0,'air','Пусто',0,'bod')]

armors = [Equip(10, ['air'], 0, 0, 'chain_mail','Кольчуга',0,'bod'),
         Equip(8, ['air'], 0, 0, 'leather_taped_armor','Проклеенный кожей доспех',0,'bod'),
         Equip(6, ['air'], 0, 0, 'leather_armor','Кожаный доспех',0,'bod'),
         Equip(0, ['air'],0,0,'air','Пусто',0,'bod')]

jewelleries = []


all_weapon_names = ['Старый меч','Кинжал','Старый лук','Железный меч с проклятьем']
all_armor_names = ['Кольчуга','Проклеенный кожей доспех','Кожаный доспех']
