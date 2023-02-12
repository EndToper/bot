from sql import Database
from aiogram import types
from classes import basic_enemies, Enemy, GameClass
import random as r
import texts
from map import locations
from equip import armors, weapons, jewelleries, all_weapon_names, all_armor_names, all_jewelery_names
from magic import spell

monsters_from_loc = {'Лес': ['goblin', 'wolf', 'leshii'], 'Перелески': ['goblin', 'wolf', 'leshii'],
                     "Луг":['parasite','poison-slime','flower-fairy'], "Озеро":['nakki','morgena','mermaid'],
                     "Цветочный луг":['flower-fairy','mandragora','flower-fairy-king'],
                     "Побережье":['long-necked-sea-serpent','gigantic-octopus','gorgona'],
                     "Скалистое побережье":['long-necked-sea-serpent','gigantic-octopus','gorgona'],
                     "Темный лес":['naga','shadow','raven-mockingbird'],
                     "Скалы":['stonlem','salamandra','anchimayen'],
                     "Инврисовый лес":['dryad','envrisent','elder-envrisent'],
                     "Темный инврисовый лес":['raven-mockingbird','distortion-envrisent','used-distortion-envrisent']}

monsters = ['Гоблин','Волк','Леший','Травяной паразит','Ядовитая слизь','Дух цветов',
            'Накки','Морге́на','Русалка','Мандрагора','Король духов цветов',
            'Длинношеий морской змей','Гигантский осьминог','Медуза Горгона',
            'Воин наги','Тень','Ворон-пересмешник','Камнелем',
            'Саламандра','Анчимайен, мальчик-шаровая-молния',
            'Древесный живой инврис','Инврисэнт',
            'Древний инврисэнт','Искаженный инврисэнт',
            'Сросшиеся искаженные инврисэнты']

classless = GameClass('Бесклассовый', 0, 0, 0, 0, 0, 0, 0, 0, [0], 'classless')
mage = GameClass('Инврисолог', 1, 1, 1.05, 1.05, 1.05, 1.1, 1, 1.05, [3], 'mage')
warrior = GameClass('Воин', 1.1, 1, 1, 1, 1, 1, 1, 1, [1], 'warrior')
archer = GameClass('Лучник', 1.1, 1.1, 1, 1, 1, 1, 1, 1, [2], 'archer')
warlock = GameClass('Колдун', 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 1.15, 0.85, [4], 'warlock')

classes_by_name = {'classless': classless, 'mage': mage, 'warrior': warrior, 'archer': archer, 'warlock': warlock}
available_slots = ['Броня', 'Главное_оружие', 'Второе_оружие', 'Украшение']
slots_to_massive = {'equip_armor': all_armor_names, 'equip_weapon': all_weapon_names, 'equip_weapon2': all_weapon_names,
                    "equip_jewellery": jewelleries}
slots_name_to_column = {"Броня": "equip_armor", "Главное_оружие": "equip_weapon", "Второе_оружие": "equip_weapon2",
                        "Украшение": "equip_jewellery"}
available_magic_slots = ['1', '2', '3']
number_by_name = {'Гоблин':0,'Волк':1,'Леший':2,'Травяной паразит':3,'Ядовитая слизь':4,'Дух цветов':5,
            'Накки':6,'Морге́на':7,'Русалка':8,'Мандрагора':9,'Король духов цветов':10,
            'Длинношеий морской змей':11,'Гигантский осьминог':12,'Медуза Горгона':13,
            'Воин наги':14,'Тень':15,'Ворон-пересмешник':16,'Камнелем':17,
            'Саламандра':18,'Анчимайен, мальчик-шаровая-молния':19,
            'Древесный живой инврис':20,'Инврисэнт':21,
            'Древний инврисэнт':22,'Искаженный инврисэнт':23,
            'Сросшиеся искаженные инврисэнты':24}


name_damage = {'fire': 'огнем', 'phys': 'физической силой', 'water': 'водой', 'ice': 'льдом', 'electro': 'молнией',
               'space': 'пространством', 'curse': 'проклятьем', 'poison': 'ядом', 'heal': '', 'melee': ''}

async def get_money(money):
    gold = money // 1000
    silver = (money - gold * 1000) // 10
    bronze = money - gold * 1000 - silver * 10
    return f'{gold} золотых, {silver} серебряных, {bronze} медяков'


async def perfor_enhanc(chars, rint, count, call, hp, max_hp, exp, level):
    chars[rint] += count
    inv_chars = await Database().fetchone(
        f"SELECT last_body, inventory_size FROM players_inventory WHERE telegram_id={call.message.chat.id}")
    size = int(inv_chars[1])
    last_body = int(inv_chars[0])
    size = size + ((chars[0] - last_body) * 2 if chars[0] > last_body else 0)
    await Database().exec_and_commit(sql=f"UPDATE players_inventory SET inventory_size = ?, last_body = ? "
                                         f"WHERE telegram_id = ?",
                                     parameters=(int(size), int(chars[0]), call.message.chat.id))
    await Database().exec_and_commit(
        sql=f"UPDATE players_stat SET body = ?, dexterity = ?, intellect = ?, wisdom = ?"
            f" WHERE telegram_id = ?",
        parameters=(chars[0], chars[1], chars[2], chars[3], call.message.chat.id))
    await Database().exec_and_commit(sql=f"UPDATE players_stat SET level = ?, exp = ?, hp = ?, max_hp = ?"
                                         f" WHERE telegram_id = ?",
                                     parameters=(level, exp, hp + (chars[0] - last_body) * 5,
                                                 max_hp + (chars[0] - last_body) * 5, call.message.chat.id))
    await call.message.answer(
        f'Вы повысили уровень.\nХарактеристика {["Телосложение", "Ловкость", "Интеллект", "Харизма"][rint]} увеличена на {count}')


async def change_loc(message: types.Message):
    loc_obj = None
    await Database.create()
    location = await Database().fetchone(f"SELECT location FROM players_stat WHERE telegram_id={message.chat.id}")
    location = location[0]
    for elem in locations:
        if elem.title == location:
            loc_obj = elem
    keyboard = types.InlineKeyboardMarkup()
    if 'town' in location:
        hp = await Database().fetchone(f"SELECT max_hp FROM players_stat WHERE telegram_id={message.chat.id}")
        hp = hp[0]
        await Database().exec_and_commit(sql=f"UPDATE players_stat SET hp = ?"
                                             f" WHERE telegram_id = ?",
                                         parameters=(hp, message.chat.id))
        keyboard.add(types.InlineKeyboardButton(text='Зайти в магазин', callback_data=f"gshop"))
    for i in range(len(loc_obj.paths)):
        keyboard.add(types.InlineKeyboardButton(text=loc_obj.paths_name[i], callback_data=f"go_{loc_obj.paths[i]}"))
    text_loc = await texts.loc_text(loc_obj.name)
    await message.answer(text_loc, reply_markup=keyboard)


async def create_monster(loc):
    monsters = monsters_from_loc[loc.name]
    rand = r.randint(1, 100)
    monster_num = 0
    if rand <= 65:
        monster_num = 0
    elif 65 < rand <= 95:
        monster_num = 1
    elif 95 < rand <= 100:
        monster_num = 2
    monster_ex = basic_enemies[monsters[monster_num]]
    monster = Enemy(monster_ex.name, round(monster_ex.hp / 1.5) + r.randint(1, round(monster_ex.hp * 1.5)),
                    monster_ex.dex,
                    monster_ex.dam, monster_ex.dam_type, monster_ex.res, monster_ex.drop, monster_ex.xp,
                    monster_ex.boss)
    return monster


async def fight(message: types.Message, monster):
    await Database.create()
    res = await Database().fetchone(f"SELECT hp, max_hp FROM players_stat WHERE telegram_id={message.chat.id}")
    await message.answer(f"Ваш противник - {monster.name}\nХиты здоровья: {monster.hp}\nВаши хиты: {res[0]}/{res[1]}")
    result = await Database().fetchone(
        f"SELECT equip_weapon, equip_weapon2, magic_spell1, magic_spell2, magic_spell3 FROM players_inventory WHERE telegram_id={message.chat.id}")
    keyboard = types.InlineKeyboardMarkup()
    inv = []
    for elem in result:
        for elem2 in weapons:
            if elem == elem2.name:
                inv.append(elem2)
        for elem3 in spell:
            if elem == elem3.name:
                inv.append((elem3))
    for i in range(len(result)):
        keyboard.add(types.InlineKeyboardButton(text=result[i],
                                                callback_data=f"att_{result[i]}_{inv[i].type_char}_{number_by_name[monster.name]}_{monster.hp}"))
    await message.answer(text='Выберите способ атаки', reply_markup=keyboard)


async def attack(call: types.CallbackQuery):
    await Database.create()
    attack = call.data.split("_")[1]
    char_type = call.data.split("_")[2]
    m_name = monsters[int(call.data.split("_")[3])]
    m_hp = call.data.split("_")[4]
    await call.message.edit_text(f'Вы атакавали, используя {attack}')
    monster = None
    for elem in basic_enemies.values():
        if m_name == elem.name:
            monster = Enemy(elem.name, int(m_hp), elem.dex, elem.dam, elem.dam_type, elem.res, elem.drop, elem.xp,
                            elem.boss)
    weapon = None
    chars = await Database().fetchone(
        f"SELECT body, dexterity, intellect, wisdom FROM players_stat WHERE telegram_id={call.message.chat.id}")
    chars = [int(chars[0]), int(chars[1]), int(chars[2]), int(chars[3])]
    magic_affinity = await Database().fetchone(
        f"SELECT fire, water, electro, element, space FROM players_stat WHERE telegram_id={call.message.chat.id}")
    bonus = {'fire': float(magic_affinity[0]), 'water': float(magic_affinity[1]), 'electro': float(magic_affinity[2]),
             'space': float(magic_affinity[3]), 'ice': float(magic_affinity[1]), 'heal': 1, 'curse': 1,
             'poison': 1, 'melee': 1}
    element = float(magic_affinity[2])
    result = await Database().fetchone(
        f"SELECT hp, max_hp, class FROM players_stat WHERE telegram_id={call.message.chat.id}")
    hp = result[0]
    max_hp = result[1]
    pl_class = classes_by_name[result[2]]
    damage = 0
    if char_type == 'bod' or char_type == 'dex':
        for elem in weapons:
            if attack == elem.name:
                weapon = elem
        weapon_damage = 0
        for i in range(2 * weapon.count if r.randint(1, 10) == 1 and pl_class.type == 'archer' else weapon.count):
            weapon_damage += r.randint(1, weapon.dice)
        damage = weapon_damage
        damage += chars[0] / 1.5 if char_type == 'bod' and pl_class.type == 'warrior' else chars[0] / 2 if char_type == 'bod' else chars[1]/ 1.5 if char_type == 'dex' and pl_class.type == 'archer' else chars[1] / 2
        rw = r.randint(1, 1000)
        damage = damage * 2 if rw <= 125 and pl_class.type == 'warrior' else damage
    elif char_type == 'int':
        for elem in spell:
            if attack == elem.name:
                weapon = elem
        magic_damage = 0
        for i in range(weapon.count):
            magic_damage += r.randint(1, round(chars[2]*0.5) if chars[2] > 40 else (round(chars[2]*0.7) if chars[2] > 20 else chars[2])) * (0.5 if chars[2] > 40 else (0.7 if chars[2] > 20 else 1))
        for elem in weapon.damage_type:
            magic_damage = magic_damage * (bonus[elem]
                                           + (element if elem in ['fire', 'electro', 'water', 'ice'] else 0)
                                           + (0.1 if pl_class.type == 'mage' else 0))
        damage = magic_damage if 'heal' not in weapon.damage_type else 0
    resistance = 1
    curse_dam = 0
    for dt in weapon.damage_type:
        resistance = resistance * monster.res[dt]
    damage = round(damage / resistance) if resistance > 0 else 0
    monster.hp -= damage
    if 'poison' in weapon.damage_type:
        monster.hp -= chars[3]
    if 'curse' in weapon.damage_type:
        curse_dam = chars[3] / 100 * max_hp if chars[3] < 75 else 0.75 * max_hp
        curse_dam = curse_dam if pl_class.type == 'warlock' else curse_dam/10
        curse_dam = round(curse_dam)
        monster.hp -= curse_dam
    monster_damage = r.randint(1, monster.dam)
    for elem in monster.dam_type:
        if elem in ['fire', 'electro', 'ice', 'water', 'phys']:
            monster_damage = monster_damage * monster.res[elem]
        elif elem == 'poison':
            monster_damage += monster.dex/monster.res['poison']
        elif elem == 'curse':
            monster_damage += round(monster.dex / 100 * max_hp)
    monster_damage = round(monster_damage)
    damages = []
    for elem in weapon.damage_type:
        damages.append(name_damage[elem])
    mon_damages = []
    for elem in monster.dam_type:
        mon_damages.append(name_damage[elem])
    rand = r.randint(1, 100)
    if chars[1] > monster.dex and 'melee' not in weapon.damage_type:
        if rand < 85:
            monster_damage = 0
    elif round(chars[1] / monster.dex * 100 if chars[1] / monster.dex * 100 <= 80 else 80) > rand and 'melee' not in weapon.damage_type:
        monster_damage = 0
    elif round(chars[1] / monster.dex * 100) > rand and 'melee' in weapon.damage_type and round(
            chars[1] / monster.dex * 100) < 50:
        monster_damage = 0
    elif 50 > rand and round(chars[1] / monster.dex * 100) > 50 and 'melee' in weapon.damage_type:
        monster_damage = 0
    hp -= monster_damage
    await call.message.answer(
        f'Вы нанесли монстру {damage + (chars[3] if "poison" in weapon.damage_type else 0) + curse_dam}'
        f' урона {", ".join(damages)}\nВам нанесено {monster_damage} урона {", ".join(mon_damages)}')
    if 'heal' in weapon.damage_type:
        hp = hp + 4*round(magic_damage) + 1 if hp + 4*round(magic_damage) + 1 < max_hp else max_hp
        await call.message.answer(f'Вы восстановили {4*round(magic_damage) + 1} хитов')
    await Database().exec_and_commit(sql=f"UPDATE players_stat SET hp = ?"
                                         f" WHERE telegram_id = ?",
                                     parameters=(hp, call.message.chat.id))
    money = await Database().fetchone(f"SELECT money FROM players_inventory WHERE telegram_id={call.message.chat.id}")
    money = int(money[0])
    if hp >= 0 and monster.hp > 0:
        await fight(call.message, monster)
    if monster.hp <= 0:
        await call.message.answer(f'Вы победили монстра "{monster.name}"')
        res = await Database().fetchone(f"SELECT inventory, inventory_size FROM players_inventory WHERE telegram_id={call.message.chat.id}")
        inv = res[0]
        size = int(res[1])
        count = len(inv.split('/'))
        drop = ''
        for elem in monster.drop.keys():
            if r.randint(1,100) < monster.drop[elem] and count+1 <= size:
                drop = drop + "/" + elem
                count+=1
                await call.message.answer(f"Вы нашли {elem} в трупе монстра")
        print(drop)
        await Database().exec_and_commit(sql=f"UPDATE players_inventory SET inventory = ?"
                                             f" WHERE telegram_id = ?",
                                         parameters=(inv+drop, call.message.chat.id))
        levels = await Database().fetchone(
            f"SELECT level, exp FROM players_stat WHERE telegram_id={call.message.chat.id}")
        await Database().exec_and_commit(sql=f"UPDATE players_stat SET hp = ?"
                                             f" WHERE telegram_id = ?",
                                         parameters=(round(max_hp / 2) if hp < round(max_hp / 2) else hp, call.message.chat.id))
        level = int(levels[0])
        exp = int(levels[1])
        exp += monster.xp

        print('лвл монстра',monster.xp)
        await Database().exec_and_commit(sql=f"UPDATE players_stat SET exp = ?"
                                             f" WHERE telegram_id = ?",
                                         parameters=(exp, call.message.chat.id))
        if exp >= (level + 1) * 100:
            exp -= (level + 1) * 100
            print(exp)
            level += 1
            rint = r.randint(0, 3)
            count = r.randint(1, 3)
            if level % 5 != 0:
                await perfor_enhanc(chars,rint,count,call,hp,max_hp,exp,level)
            else:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text=f'Телосложение',
                                                        callback_data=f"choose_char_0_{exp}"))
                keyboard.add(types.InlineKeyboardButton(text=f'Ловкость',
                                                        callback_data=f"choose_char_1_{exp}"))
                keyboard.add(types.InlineKeyboardButton(text=f'Интеллект',
                                                        callback_data=f"choose_char_2_{exp}"))
                keyboard.add(types.InlineKeyboardButton(text=f'Мудрость/харизма',
                                                        callback_data=f"choose_char_3_{exp}"))
                await call.message.answer(f'Выберите характеристику, которую хотите повысить на 3',reply_markup=keyboard)

        await Database().exec_and_commit(sql=f"UPDATE players_inventory SET money = ?"
                                             f" WHERE telegram_id = ?",
                                         parameters=(money + 5, call.message.chat.id))
        await change_loc(call.message)
    if hp < 0 and monster.hp > 0:
        await call.message.answer(f"Вы погибли в битве с монстром")
        if money >= 50:
            money -= 50
            await call.message.answer(f"Вы воскресли в Торговом городе. За услуги жреца списано 5 серебряных монет")
            await Database().exec_and_commit(sql=f"UPDATE players_stat SET location = ?"
                                                 f" WHERE telegram_id = ?",
                                             parameters=('town', call.message.chat.id))
            await Database().exec_and_commit(sql=f"UPDATE players_inventory SET money = ?"
                                                 f" WHERE telegram_id = ?",
                                             parameters=(money, call.message.chat.id))
            await change_loc(call.message)
        else:
            await call.message.answer(f"Вы героически пали в бою. Ваше имя будут помнить на континенте Инврис...")
            await Database().exec_and_commit(sql=f"DELETE FROM players_stat WHERE telegram_id = ?",
                                             parameters=(call.message.chat.id,))
            await Database().exec_and_commit(sql=f"DELETE FROM players_inventory WHERE telegram_id = ?",
                                             parameters=(call.message.chat.id,))