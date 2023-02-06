import asyncio
import random as r
from aiogram import Bot, Dispatcher, executor, types

import map
from sql import Database
import os
import config
from aiogram.dispatcher.filters import Text
from classes import GameClass, Enemy, basic_enemies
from magic import spell
from map import locations, paths_level
from equip import armors, weapons, jewelleries, all_weapon_names, all_armor_names

classless = GameClass('Бесклассовый', 0, 0, 0, 0, 0, 0, 0, 0, [0], 'classless')
mage = GameClass('Инврисолог', 1, 1, 1.05, 1.05, 1.05, 1.1, 1, 1.05, [3], 'mage')
warrior = GameClass('Воин', 1.1, 1, 1, 1, 1, 1, 1, 1, [1], 'warrior')
archer = GameClass('Лучник', 1.1, 1.1, 1, 1, 1, 1, 1, 1, [2], 'archer')
warlock = GameClass('Колдун', 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 1.15, 0.85, [4], 'warlock')

classes_by_name = {'classless': classless, 'mage': mage, 'warrior': warrior, 'archer': archer, 'warlock': warlock}
available_slots = ['Броня', 'Главное_оружие', 'Второе_оружие', 'Украшение']
slots_to_massive = {'Броня': all_armor_names, 'Главное_оружие': all_weapon_names, 'Второе_оружие': all_weapon_names,
                    'Украшение': jewelleries}
slots_name_to_column = {"Броня": "equip_armor", "Главное_оружие": "equip_weapon", "Второе_оружие": "equip_weapon2",
                        "Украшение": "equip_jewellery"}
available_magic_slots = ['1', '2', '3']
monsters_from_loc = {'Лес': ['goblin', 'wolf', 'leshii'], 'Перелески': ['goblin', 'wolf', 'leshii'],
                     "Луг":['parasite','poison-slime','flower-king'], "Озеро":['nakki','morgena','mermaid'],
                     "Цветочный луг":['flower-fairy','mandragora','flower-fairy-king'],
                     "Побережье":['long-necked-sea-serpent','gigantic_octopus','gorgona'],
                     "Темный лес":['naga','shadow','raven-mockingbird'],
                     "Скалы":['stonlem','salamandra','anchimayen'],
                     "Инврисовый лес":['dryad','envrisent','elder-envrisent'],
                     "Темный инврисовый лес":['raven-mockingbird','distortion-envrisent','used-distortion-envrisent']}

name_damage = {'fire': 'огнем', 'phys': 'физической силой', 'water': 'водой', 'ice': 'льдом', 'electro': 'молнией',
               'space': 'пространством', 'curse': 'проклятьем', 'poison': 'ядом', 'heal': '', 'melee': ''}

import texts

bot = Bot(token=os.environ.get("TOKEN"))
dp = Dispatcher(bot)


async def get_money(money):
    gold = money // 1000
    silver = (money - gold * 1000) // 10
    bronze = money - gold * 1000 - silver * 10
    return f'{gold} золотых, {silver} серебряных, {bronze} медяков'


async def change_loc(message: types.Message):
    loc_obj = None
    await Database.create()
    location = await Database().fetchone(f"SELECT location FROM players_stat WHERE telegram_id={message.chat.id}")
    location = location[0]
    for elem in locations:
        if elem.title == location:
            loc_obj = elem
    if 'town' in location:
        hp = await Database().fetchone(f"SELECT max_hp FROM players_stat WHERE telegram_id={message.chat.id}")
        hp = hp[0]
        await Database().exec_and_commit(sql=f"UPDATE players_stat SET hp = ?"
                                             f" WHERE telegram_id = ?",
                                         parameters=(hp, message.chat.id))
    keyboard = types.InlineKeyboardMarkup()
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
                                                callback_data=f"attack_{result[i]}_{inv[i].type_char}_{monster.name}_{monster.hp}"))
    await message.answer("Выберите способ атаки", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith="attack_")
async def attack(call: types.CallbackQuery):
    await Database.create()
    attack = call.data.split("_")[1]
    char_type = call.data.split("_")[2]
    m_name = call.data.split("_")[3]
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
    print(chars)
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
        for i in range(2 * weapon.count if r.randint(1, 10) == 1 and classes_by_name[
            pl_class].type == 'archer' else weapon.count):
            weapon_damage += r.randint(1, weapon.dice)
        damage = weapon_damage
        damage += chars[0] / 2 if char_type == 'bod' else chars[1] / 2
        rw = r.randint(1, 1000)
        damage = damage * 2 if rw <= 125 and classes_by_name[pl_class].type == 'warrior' else damage
    elif char_type == 'int':
        for elem in spell:
            if attack == elem.name:
                weapon = elem
        magic_damage = 0
        for i in range(weapon.count):
            magic_damage += r.randint(1, chars[2])
        for elem in weapon.damage_type:
            magic_damage = magic_damage * (
                    bonus[elem] + (element if elem in ['fire', 'electro', 'water', 'ice'] else 0) + (
                0.1 if classes_by_name[pl_class].type == 'mage' else 0))
        damage = magic_damage if 'heal' not in weapon.damage_type else 0
    resistance = 1
    curse_dam = 0
    for dt in weapon.damage_type:
        resistance = resistance * monster.res[dt]
    damage = round(damage / resistance) if resistance > 0 else 0
    monster.hp -= damage
    if weapon.damage_type == 'poison':
        monster.hp -= chars[3]
    if weapon.damage_type == 'curse':
        curse_dam = chars[3] / 100 * max_hp if chars[3] < 50 else 0.5 * max_hp
        curse_dam = curse_dam if curse_dam < 50 else 50
        curse_dam = curse_dam if pl_class.type == 'warlock' else 10
        monster.hp -= curse_dam
    monster_damage = r.randint(1, monster.dam)
    for elem in monster.dam_type:
        if elem in ['fire', 'electro', 'ice', 'water', 'phys']:
            monster_damage = monster_damage * monster.res[monster.dam_type]
        elif elem == 'poison':
            monster_damage += monster.dex/monster.res['poison']
        elif elem == 'curse':
            monster_damage += round(monster.dex / 100 * max_hp)
    monster_damage = round(monster_damage)
    damages = []
    print(monster_damage)
    for elem in weapon.damage_type:
        damages.append(name_damage[elem])
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
    print(monster_damage)
    hp -= monster_damage
    await call.message.answer(
        f'Вы нанесли монстру {damage + (chars[3] if "poison" in weapon.damage_type else 0) + curse_dam}'
        f' урона {", ".join(damages)}\n Вам нанесено {monster_damage} урона {name_damage[monster.dam_type]}')
    if 'heal' in weapon.damage_type:
        hp = hp + 2*round(magic_damage) + 1 if hp + 2*round(magic_damage) + 1 < max_hp else max_hp
        print(hp)
        await call.message.answer(f'Вы восстановили {round(magic_damage) + 1} хитов')
    await Database().exec_and_commit(sql=f"UPDATE players_stat SET hp = ?"
                                         f" WHERE telegram_id = ?",
                                     parameters=(hp, call.message.chat.id))
    money = await Database().fetchone(f"SELECT money FROM players_inventory WHERE telegram_id={call.message.chat.id}")
    money = int(money[0])
    if hp >= 0 and monster.hp > 0:
        await fight(call.message, monster)
    if monster.hp <= 0:
        await call.message.answer(f'Вы победили монстра "{monster.name}"')
        levels = await Database().fetchone(
            f"SELECT level, exp FROM players_stat WHERE telegram_id={call.message.chat.id}")
        await Database().exec_and_commit(sql=f"UPDATE players_stat SET hp = ?"
                                             f" WHERE telegram_id = ?",
                                         parameters=(round(max_hp / 2), call.message.chat.id))
        level = int(levels[0])
        exp = int(levels[1])
        exp += monster.xp
        if exp > (level + 1) * 100:
            exp -= (level + 1) * 100
            level += 1
            rint = r.randint(1, 4)
            count = r.randint(1, 3)
            chars[rint] += count
            last_body = await Database().fetchone(
                f"SELECT last_body, inventory_size FROM players_inventory WHERE telegram_id={call.message.chat.id}")
            size = int(last_body[1])
            last_body = int(last_body[0])
            size = size + ((chars[0] - last_body) * 2 if chars[0] > last_body else size)
            await Database().exec_and_commit(sql=f"UPDATE players_inventory SET inventory_size = ?, last_body = ?"
                                                 f" WHERE telegram_id = ?",
                                             parameters=(size, chars[0], call.message.chat.id))
            await call.message.answer(
                f'Вы повысили уровень.\nХарактеристика {["Телосложение", "Ловкость", "Интеллект", "Харизма"][rint]} увеличена на {count}')
            await Database().exec_and_commit(
                sql=f"UPDATE players_stat SET body = ?, dexterity = ?, intellect = ?, wisodm = ?,"
                    f" WHERE telegram_id = ?",
                parameters=(chars[0], chars[1], chars[2], chars[3], call.message.chat.id))
        await Database().exec_and_commit(sql=f"UPDATE players_stat SET level = ?, exp = ?, hp = ?, max_hp = ?"
                                             f" WHERE telegram_id = ?",
                                         parameters=(level, exp, hp + (chars[0] - last_body)*5,max_hp + (chars[0] - last_body)*5, call.message.chat.id))
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


@dp.callback_query_handler(text_startswith="go_")
async def go(call: types.CallbackQuery):
    await Database.create()
    location = await Database().fetchone(f"SELECT location FROM players_stat WHERE telegram_id={call.message.chat.id}")
    location = location[0]
    level = await Database().fetchone(f"SELECT level FROM players_stat WHERE telegram_id={call.message.chat.id}")
    level = level[0]
    location2 = call.data.split("_")[1]
    loc = None
    loc2 = None
    for elem in locations:
        if elem.title == location:
            loc = elem
    for elem in locations:
        if elem.title == location2:
            loc2 = elem
    if level >= paths_level[loc2.title]:
        await call.message.edit_text(await texts.loc_text_2(loc.name, loc2.name))
        await Database().exec_and_commit(sql="UPDATE players_stat SET location = ? WHERE telegram_id = ?",
                                         parameters=(location2, call.from_user.id))
        await call.answer()
        rand = r.randint(1, 20)
        if rand <= 10 and 'path' not in loc2.title and 'town' not in loc2.title:
            await call.message.answer(f'Вы встрели в локации {loc2.name} монстра. Приготовтесь к битве')
            await fight(call.message, await create_monster(loc2))
        else:
            await change_loc(call.message)
    else:
        await call.answer(f"Для прохода в локацю {loc2.name} требуется {paths_level[loc2.title]} уровень")


@dp.callback_query_handler(text="warrior")
async def become_warrior(call: types.CallbackQuery):
    await Database.create()
    await Database().exec_and_commit(sql="UPDATE players_stat SET class = ? WHERE telegram_id = ?",
                                     parameters=('warrior', call.from_user.id))
    await Database().exec_and_commit(sql="UPDATE players_inventory SET inventory = ? WHERE telegram_id = ?",
                                     parameters=('Кольчуга/Старый меч', call.from_user.id))
    await call.answer("Вы успешно сменили свой класс на Воина!")
    await call.message.edit_text(f"Вы выбрали класс Воин")
    await change_loc(call.message)


@dp.callback_query_handler(text="archer")
async def become_archer(call: types.CallbackQuery):
    await Database.create()
    await Database().exec_and_commit(sql="UPDATE players_stat SET class = ? WHERE telegram_id = ?",
                                     parameters=('archer', call.from_user.id))
    await Database().exec_and_commit(sql="UPDATE players_inventory SET inventory = ? WHERE telegram_id = ?",
                                     parameters=('Старый лук/Проклеенный кожей доспех', call.from_user.id))
    await call.answer("Вы успешно сменили свой класс на Лучника!")
    await call.message.edit_text(f"Вы выбрали класс Лучник")
    await change_loc(call.message)


@dp.callback_query_handler(text="mage")
async def become_archer(call: types.CallbackQuery):
    await Database.create()
    await Database().exec_and_commit(sql="UPDATE players_stat SET class = ? WHERE telegram_id = ?",
                                     parameters=('mage', call.from_user.id))
    await Database().exec_and_commit(sql="UPDATE players_inventory SET inventory = ? WHERE telegram_id = ?",
                                     parameters=('Кинжал/Кожаный доспех', call.from_user.id))
    await call.answer("Вы успешно сменили свой класс на Мага!")
    await call.message.edit_text(f"Вы выбрали класс Маг")
    await change_loc(call.message)


@dp.callback_query_handler(text="warlock")
async def become_archer(call: types.CallbackQuery):
    await Database.create()
    await Database().exec_and_commit(sql="UPDATE players_stat SET class = ? WHERE telegram_id = ?",
                                     parameters=('warlock', call.from_user.id))
    await Database().exec_and_commit(sql="UPDATE players_inventory SET inventory = ? WHERE telegram_id = ?",
                                     parameters=(
                                         'Железный меч с проклятьем/Проклеенный кожей доспех', call.from_user.id))
    await call.answer("Вы успешно сменили свой класс на Колдуна!")
    await call.message.edit_text(f"Вы выбрали класс Колдун")
    await change_loc(call.message)


async def change_class(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Воин", callback_data="warrior"))
    keyboard.add(types.InlineKeyboardButton(text="Лучник", callback_data="archer"))
    keyboard.add(types.InlineKeyboardButton(text="Маг", callback_data="mage"))
    keyboard.add(types.InlineKeyboardButton(text="Колдун", callback_data="warlock"))
    await message.answer(texts.change_class, reply_markup=keyboard)


@dp.message_handler(commands=['inv', 'inventory'])
async def inventory(message: types.Message):
    await Database.create()
    res = await Database().fetchone(f"SELECT * FROM players_inventory WHERE telegram_id={message.from_user.id}")
    print(res)
    if res is None:
        await message.reply("Инвентарь доступен только приключенцам. \n"
                            "Вам нужно прибыть на континент Инврис для просмотра профиля.\n"
                            "(напишите /start или /go)")
    else:
        inv = res[2].split('/')
        inv2 = ', '.join(inv)
        print(inv, inv2)
        await message.reply(
            f"Ваш инвентарь имеет вместимость {res[1]}. Заполнено {len(inv) if res[2] != 'Пусто' else 0}/{res[1]}\n"
            f"Монеты: {await get_money(res[3])}\n"
            f"Инвентарь: {inv2}\n"
            f"Экипировка:\n"
            f"Броня: {res[5]}\n"
            f"Главное оружие: {res[6]}\n"
            f"Второе оружие: {res[7]}\n"
            f"Украшения: {res[8]}\n"
            f"Чтобы снарядить какую-либо вещь пропишите команду /equip <slot> <name>\n"
            f"Например /equip Броня Кольчуга\n"
            f"Чтоб снять предмет пропишите /equip <slot> Пусто")


@dp.message_handler(commands=['ml', 'sl', 'magic_list', 'spells_list'])
async def magic_list(message: types.Message):
    await Database.create()
    res = await Database().fetchone(f"SELECT magic_spell1,magic_spell2,magic_spell3 FROM players_inventory "
                                    f"WHERE telegram_id={message.from_user.id}")
    await message.reply(f'Заклинания:\nПервый слот: {res[0]}\nВторой слот: {res[1]}\nТретий слот: {res[2]}')


@dp.message_handler(commands=['mc', 'mag_chan', 'magic', 'magic_change'])
async def magic(message: types.Message):
    await Database.create()
    text = message.text.split(" ")
    if len(text) < 3:
        await message.reply("Неправильно введенная команда.\n Чтобы подготовить для боя магию пропишите команду"
                            " /magic <slot> <name>\nНапример /magic 1 Огненный шар\n")
    else:
        slot = text[1]
        if slot not in available_magic_slots:
            await message.reply(
                f"Выбран несуществующий слот. Выберите один из следующих слотов: {', '.join(available_magic_slots)}")
        else:
            slot = int(slot) - 1
            available_spell = []
            level = await Database().fetchone(
                f"SELECT level FROM players_stat WHERE telegram_id={message.from_user.id}")
            level = int(level[0])
            pl_class = await Database().fetchone(
                f"SELECT class FROM players_stat WHERE telegram_id={message.from_user.id}")
            pl_class = pl_class[0]
            pl_class = classes_by_name[pl_class]
            for elem in spell:
                if elem.level <= level and pl_class.type == 'mage':
                    available_spell.append(elem)
                elif elem.level <= level and elem.level <= 15:
                    available_spell.append(elem)
            available_spell_name = []
            for elem in available_spell:
                available_spell_name.append(elem.name)
            magic_spell = ''
            for i in range(2, len(text)):
                magic_spell += text[i] + " "
            magic_spell = magic_spell[0:len(magic_spell) - 1]
            print(magic_spell, available_spell)
            if magic_spell in available_spell_name:
                await Database().exec_and_commit(sql=f"UPDATE players_inventory SET {'magic_spell' + str(slot + 1)}"
                                                     f" = ? WHERE telegram_id = ?",
                                                 parameters=(magic_spell, message.from_user.id))
                await message.reply(f"Слот {slot + 1} был изменен на {magic_spell}")
            else:
                await message.reply(
                    f"""Вы не выучили заклинание "{magic_spell}".\nСписок доступных заклинаний: {', '.join(available_spell_name)}""")


@dp.message_handler(commands=['e', 'equip', 'equipment'])
async def equip(message: types.Message):
    await Database.create()
    armor = None
    text = message.text.split(" ")
    print(text, len(text))
    if len(text) < 3:
        await message.reply("Неправильно введенная команда.\n Чтобы снарядить какую-либо вещь пропишите команду"
                            " /equip <slot> <name>\nНапример /equip Броня Кольчуга\n")
    else:
        slot = text[1]
        if slot not in available_slots:
            await message.reply(
                f"Выбран несуществующий слот. Выберите один из следующих слотов: {', '.join(available_slots)}")
        else:
            inv = await Database().fetchone(
                f"SELECT inventory FROM players_inventory WHERE telegram_id={message.from_user.id}")
            inv = inv[0].split("/")
            equipment = ''
            for i in range(2, len(text)):
                equipment += text[i] + " "
            equipment = equipment[0:len(equipment) - 1]
            print(slots_to_massive[slot], equipment in slots_to_massive[slot])
            if equipment in inv and equipment in slots_to_massive[slot] or equipment == "Пусто":
                await Database().exec_and_commit(sql=f"UPDATE players_inventory SET {slots_name_to_column[slot]}"
                                                     f" = ? WHERE telegram_id = ?",
                                                 parameters=(equipment, message.from_user.id))
                if slot == "Броня":
                    for elem in armors:
                        if elem.name == equipment:
                            armor = elem
                    res = await Database().fetchone(
                        f"SELECT hp, max_hp, body FROM players_stat WHERE telegram_id={message.from_user.id}")
                    hp = res[0]
                    max_hp = res[1]
                    body = res[2]
                    dif = 5 * body + armor.defence - max_hp
                    hp += dif
                    await Database().exec_and_commit(sql=f"UPDATE players_stat SET hp = ?, max_hp = ?"
                                                         f" WHERE telegram_id = ?",
                                                     parameters=(hp, 5 * body + armor.defence, message.from_user.id))
                await message.reply(f"Слот {slot} был изменен на {equipment}")

            else:
                await message.reply(
                    f"У вас нет предмета {equipment} в инвентаре или {equipment} нельзя надеть на слот {slot}")


@dp.message_handler(commands=['p', 'profile', 'stat', 's', 'statistic'])
async def profile(message: types.Message):
    await Database.create()
    res = await Database().fetchone(f"SELECT * FROM players_stat WHERE telegram_id={message.from_user.id}")
    armor = await Database().fetchone(
        f"SELECT equip_armor FROM players_inventory WHERE telegram_id={message.from_user.id}")
    print(res)
    if res is None:
        await message.reply("Профиль доступен только приключенцам. \n"
                            "Вам нужно прибыть на континент Инврис для просмотра профиля.\n"
                            "(напишите /start или /go)")
    else:
        await message.reply(
            f"Приключенченское имя: {res[2]}\nКласс: {classes_by_name[res[4]].name}\nХиты здоровья:  {res[5]}/{res[6]}\n"
            f"Уровень: {res[7]} ({res[8]}/{(int(res[7]) + 1) * 100} единиц)\n<b>Характеристики</b>:\n"
            f"Телосложение: <b>{res[9]}</b> Ловкость: <b>{res[10]}</b>\n"
            f"Интеллект: <b>{res[11]}</b> Мудрость\харизма: <b>{res[12]}</b>\n<b>Родство с магией</b>:\n"
            f"Огонь: <b>{res[13]}</b> Вода(лед): <b>{res[14]}</b>\nМолния: <b>{res[15]}</b> Пространство: <b>{res[17]}</b>\n"
            f"<b><i>Бонус элементарной магии:</i></b> <b>+{res[16]}</b>\nДля просмотра инвентаря - /inventory",
            parse_mode="html")


@dp.message_handler(commands=['start', 'go'])
async def create_player(message: types.Message):
    await Database.create()
    chars = []
    for i in range(4):
        chars.append(r.randint(1, 8))
    for i in range(3):
        chars.append(round(r.random() * 1.5, 2))
    param = (
        message.from_user.id, message.from_user.username, 'town', 'classless', chars[0] * 5, chars[0] * 5, 0, 0,
        chars[0],
        chars[1], chars[2],
        chars[3], chars[4], chars[5], chars[6], round(r.random() * 0.2, 2),
        round(r.random() * 0.8, 2))
    param2 = (
        message.from_user.id, chars[0] + 2, "Пусто", 100, chars[0], "Пусто", "Пусто", "Пусто", "Пусто", "Огненный шар",
        "Быстрая молния", "Низшее исцеление")
    print(param)
    print(param2)
    res = await Database().fetchone(f"SELECT * FROM players_stat WHERE telegram_id={message.from_user.id}")
    if res is None:
        await message.answer(texts.start)
        await Database().exec_and_commit(
            sql="INSERT INTO players_stat VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            parameters=param)
        await Database().exec_and_commit(
            sql="INSERT INTO players_inventory VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", parameters=param2)
        await profile(message)
        await change_class(message)
    else:
        await message.answer("Вы уже отправились в приключение!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
