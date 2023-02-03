import asyncio
import random as r
from aiogram import Bot, Dispatcher, executor, types
from sql import Database
import os
import config
from classes import GameClass, Enemy

classless = GameClass('Бесклассовый', 0, 0, 0, 0, 0, 0, 0, 0, [0])
mage = GameClass('Маг', 1, 1, 1.05, 1.05, 1.05, 1.1, 1, 1.05, [3])
warrior = GameClass('Воин', 1.1, 1, 1, 1, 1, 1, 1, 1, [1])
archer = GameClass('Лучник', 1.1, 1.1, 1, 1, 1, 1, 1, 1, [2])
warlock = GameClass('Колдун', 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 1.15, 0.85, [4])

classes_by_name = {'classless': classless, 'mage': mage, 'warrior': warrior, 'archer': archer, 'warlock': warlock}
available_slots = ['Броня','Главное_оружие','Второе_оружие','Украшение']
slots_name_to_column = {"Броня":"equip_armor","Главное_оружие":"equip_weapon","Второе_оружие":"equip_weapon2","Украшение":"equip_jewellery"}

import texts

bot = Bot(token=os.environ.get("TOKEN"))
dp = Dispatcher(bot)

@dp.callback_query_handler(text="warrior")
async def become_warrior(call: types.CallbackQuery):
    await Database.create()
    await Database().exec_and_commit(sql="UPDATE players_stat SET class = ? WHERE telegram_id = ?",
                                     parameters=('warrior',call.from_user.id))
    await Database().exec_and_commit(sql="UPDATE players_inventory SET inventory = ? WHERE telegram_id = ?",
                                     parameters=('Кольчуга/Ржавый меч', call.from_user.id))
    await call.answer("Вы успешно сменили свой класс на Воина!")

@dp.callback_query_handler(text="archer")
async def become_archer(call: types.CallbackQuery):
    await Database.create()
    await Database().exec_and_commit(sql="UPDATE players_stat SET class = ? WHERE telegram_id = ?",
                                     parameters=('archer',call.from_user.id))
    await Database().exec_and_commit(sql="UPDATE players_inventory SET inventory = ? WHERE telegram_id = ?",
                                     parameters=('Старый лук/Проклеенный кожей доспех', call.from_user.id))
    await call.answer("Вы успешно сменили свой класс на Лучника!")

@dp.callback_query_handler(text="mage")
async def become_archer(call: types.CallbackQuery):
    await Database.create()
    await Database().exec_and_commit(sql="UPDATE players_stat SET class = ? WHERE telegram_id = ?",
                                     parameters=('mage',call.from_user.id))
    await Database().exec_and_commit(sql="UPDATE players_inventory SET inventory = ? WHERE telegram_id = ?",
                                     parameters=('Кинжал/Кожаный доспех', call.from_user.id))
    await call.answer("Вы успешно сменили свой класс на Мага!")

@dp.callback_query_handler(text="warlock")
async def become_archer(call: types.CallbackQuery):
    await Database.create()
    await Database().exec_and_commit(sql="UPDATE players_stat SET class = ? WHERE telegram_id = ?",
                                     parameters=('warlock',call.from_user.id))
    await Database().exec_and_commit(sql="UPDATE players_inventory SET inventory = ? WHERE telegram_id = ?",
                                     parameters=('Железный меч с проклятьем/Проклеенный кожей доспех', call.from_user.id))
    await call.answer("Вы успешно сменили свой класс на Колдуна!")


async def change_class(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Воин", callback_data="warrior"))
    keyboard.add(types.InlineKeyboardButton(text="Лучник", callback_data="archer"))
    keyboard.add(types.InlineKeyboardButton(text="Маг", callback_data="mage"))
    keyboard.add(types.InlineKeyboardButton(text="Колдун", callback_data="warlock"))
    await message.answer(texts.change_class,reply_markup=keyboard)

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
        await message.reply(f"Ваш инвентарь имеет вместимость {res[1]}. Заполнено {len(inv) if res[2] != 'Пусто' else 0}/{res[1]}\n"
                            f"Инвентарь: {inv2}\n"
                            f"Экипировка:\n"
                            f"Броня: {res[4]}\n"
                            f"Главное оружие: {res[5]}\n"
                            f"Второе оружие: {res[6]}\n"
                            f"Украшения: {res[7]}\n"
                            f"Чтобы снарядить какую-либо вещь пропишите команду /equip <slot> <name>\n"
                            f"Например /equip Броня Кольчуга\n"
                            f"Чтоб снять предмет пропишите /equip <slot> Пусто")


@dp.message_handler(commands=['e', 'equip', 'equipment'])
async def equip(message: types.Message):
    await Database.create()
    text = message.text.split(" ")
    print(text,len(text))
    if len(text) < 3:
        await message.reply("Неправильно введенная команда.\n Чтобы снарядить какую-либо вещь пропишите команду"
                            " /equip <slot> <name>\nНапример /equip Броня Кольчуга\n")
    else:
        slot = text[1]
        if slot not in available_slots:
            await message.reply(f"Выбран несуществующий слот. Выберите один из следующих слотов: {', '.join(available_slots)}")
        else:
            inv = await Database().fetchone(f"SELECT inventory FROM players_inventory WHERE telegram_id={message.from_user.id}")
            inv = inv[0].split("/")
            equipment = ''
            for i in range(2,len(text)):
                equipment += text[i] + " "
            equipment = equipment[0:len(equipment)-1]
            print(equipment)
            print(inv)
            if equipment in inv or equipment == "Пусто":
                await Database().exec_and_commit(sql=f"UPDATE players_inventory SET {slots_name_to_column[slot]}"
                                                     f" = ? WHERE telegram_id = ?",
                                                 parameters=(equipment,message.from_user.id))
                await message.reply(f"Слот {slot} был изменен на {equipment}")
            else:
                await message.reply(f"У вас нет предмета {equipment} в инвентаре")


@dp.message_handler(commands=['p', 'profile', 'stat', 's', 'statistic'])
async def profile(message: types.Message):
    await Database.create()
    res = await Database().fetchone(f"SELECT * FROM players_stat WHERE telegram_id={message.from_user.id}")
    armor = await Database().fetchone(f"SELECT equip_armor FROM players_inventory WHERE telegram_id={message.from_user.id}")
    print(res)
    if res is None:
        await message.reply("Профиль доступен только приключенцам. \n"
                            "Вам нужно прибыть на континент Инврис для просмотра профиля.\n"
                            "(напишите /start или /go)")
    else:
        await message.reply(
            f"Приключенченское имя: {res[2]}\nКласс: {classes_by_name[res[3]].name}\nХиты здоровья:{res[4]}\n"
            f"Опыт: {res[5]} единиц\n<b>Характеристики</b>:\nТелосложение: <b>{res[6]}</b> Ловкость: <b>{res[7]}</b>\n"
            f"Интеллект: <b>{res[8]}</b> Мудрость\харизма: <b>{res[9]}</b>\n<b>Родство с магией</b>:\n"
            f"Огонь: <b>{res[10]}</b> Вода(лед): <b>{res[11]}</b>\nМолния: <b>{res[12]}</b> Пространство: <b>{res[14]}</b>\n"
            f"<b><i>Бонус элементарной магии:</i></b> <b>+{res[13]}</b>\nДля просмотра инвентаря - /inventory", parse_mode="html")


@dp.message_handler(commands=['start', 'go'])
async def create_player(message: types.Message):
    await Database.create()
    chars = []
    for i in range(4):
        chars.append(r.randint(1, 8))
    for i in range(3):
        chars.append(round(r.random() * 1.5, 2))
    param = (message.from_user.id, message.from_user.username, 'classless', chars[0]*10, 0, chars[0], chars[1], chars[2],
             chars[3], chars[4], chars[5], chars[6], round(r.random() * 0.2, 2),
             round(r.random() * 0.75, 2))
    param2 = (message.from_user.id,chars[0]+2,"Пусто",chars[0],"Пусто","Пусто","Пусто","Пусто")
    print(param)
    print(param2)
    res = await Database().fetchone(f"SELECT * FROM players_stat WHERE telegram_id={message.from_user.id}")
    if res is None:
        await message.answer(texts.start)
        await Database().exec_and_commit(
            sql="INSERT INTO players_stat VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", parameters=param)
        await Database().exec_and_commit(
            sql="INSERT INTO players_inventory VALUES(?, ?, ?, ?, ?, ?, ?, ?)", parameters=param2)
        await profile(message)
        await change_class(message)
    else:
        await message.answer("Вы уже отправились в приключение!")
    print(await Database().fetchone(f"SELECT * FROM players_stat WHERE telegram_id={message.from_user.id}"))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)