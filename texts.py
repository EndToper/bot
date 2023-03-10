
start = 'Приветствую вас! Вам выпала честь перенестись на континент Инврис! Сейчас пройдет церемония благославления и' \
        ' выбора специальности'

change_class = '''Внимательно посмотрите на ваши физические данные и магические способности, потому что пришло время выбрать
свой класс\n
Воин. Вы получаете:\n
Умение - двойная атака(пасс):\n
12,5% шанс нанести х2 урона\n
Начальное снаряжение:\n
Старый меч(1/12 физ урона)\n
Кольчуга(+10 хп)\n

Лучник. Вы получаете:\n 
Умение - вторая стрела(пасс):\n
10% шанс атаковать еще раз\n
Начальное снаряжение:\n
Старый лук(1/12 физ урона)\n
Проклеенный кожей доспех(+8 хп)\n

Инврисолог. Вы получаете:\n 
Умение - сильная магия(пасс):\n
+0,1 к сродству со всей магией\n
Начальное снаряжение:\n
Кинжал(1/8 физ урона)\n
Кожаный доспех(+6 хп)\n

Колдун. Вы получаете\n
Умение - запретные слова(пасс):\n
Вы можете сражаться с помощью магических фраз. Новые фразы вы узнаете с ростом уровня и в приключениях
Начальное снаряжение:\n
Железный меч с проклятьем(1/12 проклятого урона)\n
Проклеенный кожей доспех(+8 хп)\n'''


async def loc_text(location):
        loc = f'''Вы пришли на локацию {location}.\nВыберите, куда вы хотите пойти:'''
        return loc

async def loc_text_2(location,location2):
        return f'''Вы пришли в локацию {location}.\nВы пошли в локацию {location2}'''

from magic import spell
from equip import armors, weapons, jewelleries, all_armor_names
from classes import  basic_enemies

async def descriptions(key,name,intel,max_hp,level):
        mess = ''
        dam_type = {'fire': 'Огонь', 'phys': 'Физический урон', 'water': 'Вода', 'ice': 'Лед', 'electro': 'Молния',
               'space': 'Пространство', 'curse': 'Проклятье', 'poison': 'Яд', 'heal': 'Исцеление', 'melee': 'Ближняя атака'}
        if key == 'spells' or key == 'weapons':
                weapon = [item for item in spell + weapons if item.name == name][0]
                weapon_dam_type = [dam_type[item] for item in weapon.damage_type]
                weapon_dam_type = [item for item in weapon_dam_type if item != '']
                mess += ('Урон(средние значения без модификаторов): ' if 'heal' not in weapon.damage_type else ('Восстановление: ' if weapon.damage_type == ['heal'] or weapon.damage_type == ['space','heal'] else 'Восстановление/Урон(значения без модификаторов): ')) + f'{weapon.count}к{weapon.dice if key == "weapons" else intel}\n' +\
                        f'Тип урона(влияет на модификатор атаки): {", ".join(weapon_dam_type)}\n' + \
                        ("Уменьшение ловкости в " + str(weapon.nerf_dex) + " раз\n" if key == "weapons" and weapon.nerf_dex > 1 else ("Увеличение ловкости в " + str(round(1/weapon.nerf_dex)) + " раз\n" if key == "weapons" and weapon.nerf_dex > 1 else "")) + \
                        f'Ограничение по уровню: {str(weapon.level) if 0 < weapon.level <= 10 else (str(weapon.level) + ", специализированная магия(только для магов)" if weapon.level > 10 and key == "spells" else (str(weapon.level) + ", специализированная оружие лучников и воинов" if weapon.level > 10 and key == "weapons" else"нет"))}\n' +\
                        f'Утомление: {weapon.cast_cost if weapon.cast_cost > 0 else "нет"}'
        elif key == 'armors':
                armor = [item for item in armors + jewelleries if item.name == name][0]
                if armor.name in all_armor_names:
                        mess = 'Защита: +' + str(armor.defence) + ' очков здоровья\nОграничение по уровню:' + ('нет' if armor.level == 0 else (str(armor.level) if armor.level <= 10 else str(armor.level) + ', специализированная броня для воинов и лучников'))
                else:
                        resis = [item for item in armor.res.keys() if armor.res[item] != 1]

                        str_atack = ',\n'.join(['{name}: {num}'.format(name=dam_type[item], num=armor.res[item]) for item in resis])
                        mess = f'Модификатор защиты от урона определенного вида:\n{str_atack}\nОграничение по уровню: {armor.level if armor.level > 1 else "нет"}'

        elif key == 'mobs':
                monster = basic_enemies[name]
                monster_dam_type = [dam_type[item] for item in monster.dam_type]
                monster_dam_type = [item for item in monster_dam_type if item != '']
                monster_damage = monster.dam
                for elem in monster.dam_type:
                        if elem in ['fire', 'electro', 'ice', 'water', 'phys']:
                                monster_damage = monster_damage * monster.res[elem]
                        elif elem == 'poison':
                                monster_damage += monster.dex / monster.res['poison']
                        elif elem == 'curse':
                                monster_damage += round(monster.dex / 100 * max_hp)
                monster_damage = round(
                        monster_damage * (level / (2 * monster.dex) if level / (2 * monster.dex) > 1 else 1))
                mess = f'''Очки здоровья: {round(monster.hp / 1.2 * (level/(5*monster.dex) if level/(5*monster.dex) > 1 else 1))+1} - {round(monster.hp * 1.2 * (level/(5*monster.dex) if level/(5*monster.dex) > 1 else 1))+round(monster.hp / 1.2)}
Урон(критические значения): {round(monster_damage*0.1)} - {round(monster_damage)}
Тип урона(влияет на модификатор атаки): {", ".join(monster_dam_type)}
Сопротивления: {', '.join([dam_type[item2] for item2 in [item for item in monster.res.keys() if monster.res[item] > 1] if dam_type[item2] != ''])}
Слабости: {', '.join([dam_type[item2] for item2 in [item for item in monster.res.keys() if monster.res[item] < 1] if dam_type[item2] != ''])}
Возможный дроп: {', '.join([item for item in monster.drop.keys()])}
Количество опыта за убийство - {monster.xp}'''
        return mess

