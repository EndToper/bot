import asyncio
import random as r
from aiogram import Bot, Dispatcher, executor, types

from sql import Database
import os
import config
from aiogram.dispatcher.filters import Text
from classes import GameClass, Enemy, basic_enemies
from magic import spell
from map import locations, paths_level
from equip import armors, weapons, all_equip
from auxiliary import change_loc, get_money, perfor_enhanc, classes_by_name, available_slots, \
    slots_to_massive, slots_name_to_column, available_magic_slots, number_by_name, all_weapon_names, \
    all_armor_names, all_jewelery_names
from fighting import create_monster, attack as att2, fight
from classes import drop_cost
from collections import Counter

import texts

bot = Bot(token=os.environ.get("TOKEN"))
dp = Dispatcher(bot)

info_dict = {'weapons': [item for item in all_weapon_names if item != 'Пусто'], 'armors':
    [item for item in all_armor_names if item != 'Пусто'] + [item for item in all_jewelery_names if item != 'Пусто'],
             'spells': [item.name for item in spell], 'mobs': [item for item in basic_enemies.keys()]}


@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Оружие", callback_data="info_weapons_0"))
    keyboard.add(types.InlineKeyboardButton(text="Броня и украшения", callback_data="info_armors_0"))
    keyboard.add(types.InlineKeyboardButton(text="Магия", callback_data="info_spells_0"))
    keyboard.add(types.InlineKeyboardButton(text="Монстры", callback_data="info_mobs_0"))
    await message.answer('О чем хотите узнать?', reply_markup=keyboard)


@dp.callback_query_handler(text_startswith="info_")
async def info_call(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    page = int(call.data.split("_")[2])
    direct = call.data.split("_")[1]
    if 5 * page + 5 < len(info_dict[direct]):
        keyboard.add(types.InlineKeyboardButton(text=f'Следующая страница ->',
                                                callback_data=f"info_{direct}_{page + 1}"))
    from_num = 5 * page if 5 * page < len(info_dict[direct]) else len(info_dict[direct])
    to_num = 5 * page + 5 if 5 * page + 5 < len(info_dict[direct]) else len(info_dict[direct])
    print(from_num, to_num)
    for i in range(from_num, to_num):
        keyboard.add(types.InlineKeyboardButton(
            text=f'''{info_dict[direct][i] if direct != 'mobs' else basic_enemies[info_dict[direct][i]].name}'''
            , callback_data=f"getinfo_{direct}_{i}"))
    if page > 0:
        keyboard.add(types.InlineKeyboardButton(text=f'<- Предыдущая страница',
                                                callback_data=f"info_{direct}_{page - 1}"))
    await call.message.edit_text(f"Что хотите узнать?", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith="getinfo_")
async def info_call(call: types.CallbackQuery):
    i = int(call.data.split("_")[2])
    direct = call.data.split("_")[1]
    name = info_dict[direct][i]
    await call.message.edit_text(f"{name if direct != 'mobs' else basic_enemies[name].name}")
    await call.message.answer_photo(protect_content=True,
                                    photo=types.InputFile(f"./assets/{direct}/{name}.png")) if os.path.exists(
        f"./assets/{direct}/{name}.png") else await call.answer("Картинку еще не завезли :(")
    await Database.create()
    chars = await Database().fetchone(
        f"SELECT intellect, max_hp, level FROM players_stat WHERE telegram_id={call.message.chat.id}")
    mess = await texts.descriptions(direct, name, chars[0], chars[1], chars[2])
    await call.message.answer(mess)


@dp.callback_query_handler(text_startswith="att_")
async def attack(call: types.CallbackQuery):
    await att2(call)


@dp.callback_query_handler(text_startswith="choose_char")
async def choose_char(call: types.CallbackQuery):
    await Database.create()
    rint = int(call.data.split("_")[2])
    chars = await Database().fetchone(
        f"SELECT body, dexterity, intellect, wisdom FROM players_stat WHERE telegram_id={call.message.chat.id}")
    chars = [int(chars[0]), int(chars[1]), int(chars[2]), int(chars[3])]
    count = 3
    stats = await Database().fetchone(
        f"SELECT hp, max_hp FROM players_stat WHERE telegram_id={call.message.chat.id}")
    hp = int(stats[0])
    max_hp = int(stats[1])
    await perfor_enhanc(chars, rint, count, call, hp, max_hp)
    await call.message.edit_text(
        f"""Вы повысили {'Телосложение' if rint == 0 else ('Ловкость' if rint == 1 else ('Интеллект' if rint == 2 else "Мудрость/харизма"))} на 3""")


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
        await call.message.edit_text(await texts.loc_text_2(loc.name,
                                                            loc2.name)) if call.message.text is not None else await call.message.edit_caption(
            await texts.loc_text_2(loc.name, loc2.name))
        await Database().exec_and_commit(sql="UPDATE players_stat SET location = ? WHERE telegram_id = ?",
                                         parameters=(location2, call.from_user.id))
        await call.answer()
        rand = r.randint(1, 20)
        if rand <= 10 and 'path' not in loc2.title and 'town' not in loc2.title:
            await call.message.answer(f'Вы встрели в локации {loc2.name} монстра. Приготовтесь к битве')
            monster = await create_monster(loc2, call)
            if monster.type == 'monster':
                await fight(call.message, monster, 0)
            elif monster.type == 'boss':
                await fight(call.message, monster, 0)
            elif monster.type == 'npc':
                pass
        else:
            await change_loc(call.message)
    else:
        await call.answer(f"Для прохода в локацю {loc2.name} требуется {paths_level[loc2.title]} уровень")


@dp.callback_query_handler(text_startswith="gshop")
async def shop(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'Ассортимент',
                                            callback_data=f"shopb_0"))
    keyboard.add(types.InlineKeyboardButton(text=f'Продажа',
                                            callback_data=f"sell_0"))
    await call.message.edit_text(f"Вы зашли в магазин. Вы будете продовать или покупать?",
                                 reply_markup=keyboard) if call.message.text is not None else await call.message.edit_caption(
        caption="Вы зашли в магазин. Вы будете продовать или покупать?", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith="shopb")
async def shop(call: types.CallbackQuery):
    await Database.create()
    level = await Database().fetchone(
        f"SELECT level FROM players_stat WHERE telegram_id={call.message.chat.id}")
    level = int(level[0])
    page = int(call.data.split("_")[1])
    all_availabe_equip = [item if item.level <= level and item.cost > 0 else None for item in all_equip]
    all_availabe_equip = [item for item in all_availabe_equip if item is not None]
    location = await Database().fetchone(f"SELECT location FROM players_stat WHERE telegram_id={call.message.chat.id}")
    location = location[0]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'Выйти',
                                            callback_data=f"go_{location}"))
    keyboard.add(types.InlineKeyboardButton(text=f'Продажа',
                                            callback_data=f"sell_0"))
    if 5 * page + 5 < len(all_availabe_equip):
        keyboard.add(types.InlineKeyboardButton(text=f'Следующая страница ->',
                                                callback_data=f"shopb_{page + 1}"))
    from_num = 5 * page if 5 * page < len(all_availabe_equip) else len(all_availabe_equip)
    to_num = 5 * page + 5 if 5 * page + 5 < len(all_availabe_equip) else len(all_availabe_equip)
    print(from_num, to_num)
    for i in range(from_num, to_num):
        keyboard.add(types.InlineKeyboardButton(
            text=f'{all_availabe_equip[i].name}, Стоимость: {all_availabe_equip[i].cost} медяков'
            , callback_data=f"buy_{i}"))
    if page > 0:
        keyboard.add(types.InlineKeyboardButton(text=f'<- Предыдущая страница',
                                                callback_data=f"shopb_{page - 1}"))
    await call.message.edit_text(f"Чего изволите купить?",
                                 reply_markup=keyboard) if call.message.text is not None else await call.message.edit_caption(
        caption=f"Чего изволите купить?", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith="sell")
async def sell(call: types.CallbackQuery):
    await Database.create()
    inv = await Database().fetchone(
        f"SELECT inventory FROM players_inventory WHERE telegram_id={call.message.chat.id}")
    inv = inv[0].split("/")
    page = int(call.data.split("_")[1])
    location = await Database().fetchone(f"SELECT location FROM players_stat WHERE telegram_id={call.message.chat.id}")
    location = location[0]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'Выйти',
                                            callback_data=f"go_{location}"))
    keyboard.add(types.InlineKeyboardButton(text=f'Ассортимент',
                                            callback_data=f"shopb_0"))
    if 5 * page + 5 < len(inv):
        keyboard.add(types.InlineKeyboardButton(text=f'Следующая страница ->',
                                                callback_data=f"sell_{page + 1}"))
    from_num = 5 * page if 5 * page < len(inv) else len(inv)
    to_num = 5 * page + 5 if 5 * page + 5 < len(inv) else len(inv)
    for i in range(from_num, to_num):
        keyboard.add(types.InlineKeyboardButton(text=f'{inv[i]}'
                                                , callback_data=f"itemsell_{i}"))
    if page > 0:
        keyboard.add(types.InlineKeyboardButton(text=f'<- Предыдущая страница',
                                                callback_data=f"sell_{page - 1}"))
    await call.message.edit_text(f"Что хотите продать",
                                 reply_markup=keyboard) if call.message.text is not None else await call.message.edit_caption(
        f"Что хотите продать", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith="itemsell")
async def itemsell(call: types.CallbackQuery):
    await Database.create()
    inv = await Database().fetchone(
        f"SELECT inventory FROM players_inventory WHERE telegram_id={call.message.chat.id}")
    inv = inv[0].split("/")
    item = inv[int(call.data.split("_")[1])]
    item_cost = [i.cost * 0.9 for i in all_equip if i.name == item]
    item_cost = item_cost[0] if item_cost != [] else drop_cost[item]
    item_cost = round(item_cost)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'Да',
                                            callback_data=f"""sold_{int(call.data.split("_")[1])}"""))
    keyboard.add(types.InlineKeyboardButton(text=f'Нет',
                                            callback_data=f"""sell_0"""))
    await call.message.edit_text(f"Уверены, что хотите продать {item} за {item_cost} медяков",
                                 reply_markup=keyboard) if call.message.text is not None else await call.message.edit_caption(
        f"Уверены, что хотите продать {item} за {item_cost} медяков", reply_markup=keyboard)
    print(item_cost)


@dp.callback_query_handler(text_startswith="sold")
async def sold(call: types.CallbackQuery):
    await Database.create()
    inv = await Database().fetchone(
        f"SELECT inventory, money FROM players_inventory WHERE telegram_id={call.message.chat.id}")
    money = int(inv[1])
    inv = inv[0].split("/")
    index = int(call.data.split("_")[1])
    item = inv[index]
    item_cost = [i.cost * 0.9 for i in all_equip if i.name == item]
    item_cost = item_cost[0] if item_cost != [] else drop_cost[item]
    item_cost = round(item_cost)
    inv.pop(index)
    print(inv)
    money += item_cost
    await Database().exec_and_commit(sql=f"UPDATE players_inventory SET money = ?, inventory = ?"
                                         f" WHERE telegram_id = ?",
                                     parameters=(money, '/'.join(inv), call.message.chat.id))
    for elem in available_slots:
        equipment = await Database().fetchone(
            f"SELECT {slots_name_to_column[elem]} FROM players_inventory WHERE telegram_id={call.message.chat.id}")
        if equipment[0] not in inv:
            await Database().exec_and_commit(sql=f"UPDATE players_inventory SET {slots_name_to_column[elem]} = ?"
                                                 f" WHERE telegram_id = ?",
                                             parameters=('Пусто', call.message.chat.id))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'Ассортимент',
                                            callback_data=f"shopb_0"))
    keyboard.add(types.InlineKeyboardButton(text=f'Продажа',
                                            callback_data=f"sell_0"))
    await call.message.edit_text(f"Вы продали {item} за {item_cost} медяков",
                                 reply_markup=keyboard) if call.message.text is not None else await call.message.edit_caption(
        f"Вы продали {item} за {item_cost} медяков", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith="buy")
async def buy(call: types.CallbackQuery):
    item = all_equip[0]
    await Database.create()
    level = await Database().fetchone(
        f"SELECT level FROM players_stat WHERE telegram_id={call.message.chat.id}")
    level = int(level[0])
    all_availabe_equip = [item if item.level <= level and item.cost > 0 else None for item in all_equip]
    all_availabe_equip = [item for item in all_availabe_equip if item is not None]
    item2 = all_availabe_equip[int(call.data.split("_")[1])].name
    await Database.create()
    inv = await Database().fetchone(
        f"SELECT money,inventory,inventory_size FROM players_inventory WHERE telegram_id={call.message.chat.id}")
    prof = await Database().fetchone(f"SELECT class FROM players_stat WHERE telegram_id={call.message.chat.id}")
    pl_class = classes_by_name[prof[0]]
    money = int(inv[0])
    invent = inv[1].split('/')
    size = len(invent)
    max_size = int(inv[2])
    for elem in all_equip:
        if elem.name == item2:
            item = elem
            print(item)
    needs_count = Counter(item.req)
    inv_count = Counter(invent)
    print(invent, item.req)
    if item.cost < money and (
            len([True for elem in needs_count.keys() if needs_count[elem] <= inv_count[elem]]) == len(needs_count)
            or item.req is None) and (item.level <= 10 if pl_class.type != 'warrior'
                                                          and pl_class.type != 'archer' else True) and size + 1 <= max_size:
        money -= item.cost
        if item.req is not None:
            for elem in item.req:
                print(elem, invent)
                invent.remove(elem)
        invent.append(item.name)
        await Database().exec_and_commit(sql=f"UPDATE players_inventory SET money = ?, inventory= ?"
                                             f" WHERE telegram_id = ?",
                                         parameters=(money, '/'.join(invent), call.message.chat.id))
        await call.message.reply(f"Куплен предмет {item.name}")
    elif item.cost > money:
        await call.message.reply(
            f"Недостаточно средств\nТребуется {item.cost} медяков, накопите еще {item.cost - money} медяков")
    if pl_class.type != 'warrior' and pl_class.type != 'archer' and item.level > 10:
        await call.message.reply(f"Вы не можете покупать профиссиональное снаряжение воинов и лучников")
    if size + 1 > max_size:
        await call.message.reply(f"Недостаточно места в инвентаре")
    if len([True for elem in needs_count.keys() if needs_count[elem] <= inv_count[elem]]) != len(
            needs_count) or item.req is not None:
        await call.message.reply(
            f"У вас нет необходимых материалов: {', '.join(item.req) if type(item.req) is list else item.req}")
    await call.answer()


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
    await call.answer("Вы успешно сменили свой класс на Инврисолога!")
    await call.message.edit_text(f"Вы выбрали класс Инврисолог")
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
    keyboard.add(types.InlineKeyboardButton(text="Инврисолог", callback_data="mage"))
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
            f"Чтобы снарядить какую-либо вещь пропишите команду /equip")


@dp.message_handler(commands=['ml', 'sl', 'magic_list', 'spells_list'])
async def magic_list(message: types.Message):
    await Database.create()
    res = await Database().fetchone(f"SELECT magic_spell1,magic_spell2,magic_spell3 FROM players_inventory "
                                    f"WHERE telegram_id={message.from_user.id}")
    await message.reply(f'Заклинания:\nПервый слот: {res[0]}\nВторой слот: {res[1]}\nТретий слот: {res[2]}')


@dp.message_handler(commands=['mc', 'magic', 'magic_change'])
async def magic_change(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    for elem in [1, 2, 3]:
        keyboard.add(types.InlineKeyboardButton(text=f'Магический слот {elem}',
                                                callback_data=f"mc1_{elem}"))
    await message.answer("Выберите слот", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith="mc1")
async def mc(call: types.CallbackQuery):
    await Database.create()
    level = await Database().fetchone(
        f"SELECT level FROM players_stat WHERE telegram_id={call.message.chat.id}")
    level = level[0]
    pl_class = await Database().fetchone(
        f"SELECT class FROM players_stat WHERE telegram_id={call.message.chat.id}")
    pl_class = pl_class[0]
    pl_class = classes_by_name[pl_class]
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(spell)):
        if (spell[i].level <= level and pl_class.type == 'mage') or (spell[i].level <= level and spell[i].level <= 15):
            keyboard.add(types.InlineKeyboardButton(text=f'{spell[i].name}',
                                                    callback_data=f"mc2_{call.data.split('_')[1]}_{i}"))
    await call.message.edit_text(f'Выбранный магический слот - {call.data.split("_")[1]}', reply_markup=keyboard)


@dp.callback_query_handler(text_startswith="mc2")
async def mc2(call: types.CallbackQuery):
    slot, magic_spell = call.data.split("_")[1], spell[int(call.data.split("_")[2])].name
    await Database.create()
    await Database().exec_and_commit(sql=f"UPDATE players_inventory SET {'magic_spell' + slot}"
                                         f" = ? WHERE telegram_id = ?",
                                     parameters=(magic_spell, call.message.chat.id))
    await call.message.edit_text(f"Слот {slot} был изменен на {magic_spell}")


@dp.message_handler(commands=['e', 'equip', 'equipment'])
async def equip(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    for elem in available_slots:
        keyboard.add(types.InlineKeyboardButton(text=f'{" ".join(elem.split("_"))}',
                                                callback_data=f"eq1-{elem}"))
    await message.answer("Выберите слот", reply_markup=keyboard)


@dp.callback_query_handler(text_startswith="eq1")
async def eq(call: types.CallbackQuery):
    print(call.data)
    name = ''
    await Database.create()
    inv = await Database().fetchone(
        f"SELECT inventory FROM players_inventory WHERE telegram_id={call.message.chat.id}")
    inv = inv[0].split("/")
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(inv)):
        if inv[i] in slots_to_massive[slots_name_to_column[call.data.split("-")[1]]]:
            keyboard.add(types.InlineKeyboardButton(text=f'{inv[i]}',
                                                    callback_data=f"eq2-{call.data.split('-')[1]}-{i}"))
    await call.message.edit_text(f'Выбранный слот - {" ".join(call.data.split("-")[1].split("_"))}',
                                 reply_markup=keyboard)


@dp.callback_query_handler(text_startswith="eq2")
async def equiped(call: types.CallbackQuery):
    print(call.data)
    armor = None
    await Database.create()
    slot = slots_name_to_column[call.data.split('-')[1]]
    equipment = ''
    inv = await Database().fetchone(
        f"SELECT inventory FROM players_inventory WHERE telegram_id={call.message.chat.id}")
    inv = inv[0].split("/")
    for i in range(len(inv)):
        if i == int(call.data.split('-')[2]):
            equipment = inv[i]
    if equipment in slots_to_massive[slot] or equipment == "Пусто":
        await Database().exec_and_commit(sql=f"UPDATE players_inventory SET {slot}"
                                             f" = ? WHERE telegram_id = ?",
                                         parameters=(equipment, call.message.chat.id))
        if slot == "equip_armor":
            for elem in armors:
                if elem.name == equipment:
                    armor = elem
            res = await Database().fetchone(
                f"SELECT hp, max_hp, body FROM players_stat WHERE telegram_id={call.message.chat.id}")
            hp = res[0]
            max_hp = res[1]
            body = res[2]
            dif = 5 * body + armor.defence - max_hp
            hp += dif
            await Database().exec_and_commit(sql=f"UPDATE players_stat SET hp = ?, max_hp = ?"
                                                 f" WHERE telegram_id = ?",
                                             parameters=(hp, 5 * body + armor.defence, call.message.chat.id))
        await call.message.edit_text(f"Слот {' '.join(call.data.split('-')[1].split('_'))} был изменен на {equipment}")


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
            f"Приключенченское имя: {res[2]}\nКласс: {classes_by_name[res[4]].name}\nОчки здоровья:  {res[5]}/{res[6]}\n"
            f"Уровень: {res[7]} ({res[8]}/{(int(res[7]) + 1) * 100} единиц)\n<b>Характеристики</b>:\n"
            f"Телосложение: <b>{res[9]}</b> Ловкость: <b>{res[10]}</b>\n"
            f"Интеллект: <b>{res[11]}</b> Мудрость/харизма: <b>{res[12]}</b>\n<b>Родство с магией</b>:\n"
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


@dp.message_handler(commands=['town'])
async def go_to(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Да", callback_data="town"))
    await message.answer('Пойти в город', reply_markup=keyboard)


@dp.callback_query_handler(text="town")
async def go_town(call: types.CallbackQuery):
    await Database.create()
    money = await Database().fetchone(f"SELECT money FROM players_inventory WHERE telegram_id={call.from_user.id}")
    if money[0] >= 75:
        await Database().exec_and_commit(sql="UPDATE players_stat SET location = ? WHERE telegram_id = ?",
                                         parameters=('town', call.from_user.id))
        await Database().exec_and_commit(sql="UPDATE players_inventory SET money = ? WHERE telegram_id = ?",
                                         parameters=(money[0] - 75, call.from_user.id))
        await call.answer("Таинственные силы изменеили ваше положение в пространстве!")
        await call.message.edit_text(f"Вы ушли в город")
        await change_loc(call.message)
    else:
        await call.message.edit_text(f"Недостаточно средств")


@dp.message_handler(commands=['delete'])
async def delete_player(message: types.Message):
    telegram_id = message.text.split(' ')[1]
    print(message.from_user.id)
    await Database.create()
    if message.from_user.id in config.admins:
        nick = await Database().fetchone(f"SELECT nick FROM players_stat WHERE telegram_id={telegram_id}")
        nick = nick[0]
        await Database().exec_and_commit(sql=f"DELETE FROM players_stat WHERE telegram_id = ?",
                                         parameters=(telegram_id,))
        await Database().exec_and_commit(sql=f"DELETE FROM players_inventory WHERE telegram_id = ?",
                                         parameters=(telegram_id,))
        await message.answer(f"Приключенец {'@' + nick} испепелен")
    else:
        await message.answer("Ваш статус бога не подтвержден, чтобы распоряжется жизнями людей")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
