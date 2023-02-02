import asyncio
import random as r
from aiogram import Bot, Dispatcher, executor, types
from sql import Database
import os
import config
from classes import GameClass

classless = GameClass('Бесклассовый', 0, 0, 0, 0, 0, 0, 0, 0, [0])
mage = GameClass('Маг', 1, 1, 1.05, 1.05, 1.05, 1.1, 1, 1.05, [3])
warrior = GameClass('Воин', 1.1, 1, 1, 1, 1, 1, 1, 1, [1])
archer = GameClass('Лучник', 1.1, 1.1, 1, 1, 1, 1, 1, 1, [2])
warlock = GameClass('Колдун', 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 1.15, 0.85, [4])

classes_by_name = {'classless': classless, 'mage': mage, 'warrior': warrior, 'archer': archer, 'warlock': warlock}

import texts

bot = Bot(token=os.environ.get("TOKEN"))
dp = Dispatcher(bot)

@dp.callback_query_handler(text="warrior")
async def become_warrior(call: types.CallbackQuery):
    await Database.create()
    await Database().exec_and_commit(sql="UPDATE players_stat SET class = ? WHERE telegram_id = ?",
                                     parameters=('warrior',call.from_user.id))
    await call.answer("Вы успешно сменили свой класс на Воина! Удачи вам в ваших странствиях по мире Инврис!")

@dp.callback_query_handler(text="archer")
async def become_archer(call: types.CallbackQuery):
    await Database.create()
    await Database().exec_and_commit(sql="UPDATE players_stat SET class = ? WHERE telegram_id = ?",
                                     parameters=('archer',call.from_user.id))
    await call.answer("Вы успешно сменили свой класс на Лучника! Удачи вам в ваших странствиях по мире Инврис!")

@dp.callback_query_handler(text="mage")
async def become_archer(call: types.CallbackQuery):
    await Database.create()
    await Database().exec_and_commit(sql="UPDATE players_stat SET class = ? WHERE telegram_id = ?",
                                     parameters=('mage',call.from_user.id))
    await call.answer("Вы успешно сменили свой класс на Мага! Удачи вам в ваших странствиях по мире Инврис!")

@dp.callback_query_handler(text="warlock")
async def become_archer(call: types.CallbackQuery):
    await Database.create()
    await Database().exec_and_commit(sql="UPDATE players_stat SET class = ? WHERE telegram_id = ?",
                                     parameters=('warlock',call.from_user.id))
    await call.answer("Вы успешно сменили свой класс на Колдуна! Удачи вам в ваших странствиях по мире Инврис!")


async def change_class(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Воин", callback_data="warrior"))
    keyboard.add(types.InlineKeyboardButton(text="Лучник", callback_data="archer"))
    keyboard.add(types.InlineKeyboardButton(text="Маг", callback_data="mage"))
    keyboard.add(types.InlineKeyboardButton(text="Колдун", callback_data="warlock"))
    await message.answer(texts.change_class,reply_markup=keyboard)


@dp.message_handler(commands=['p', 'profile', 'stat', 's', 'statistic'])
async def profile(message: types.Message):
    await Database.create()
    res = await Database().fetchone(f"SELECT * FROM players_stat WHERE telegram_id={message.from_user.id}")
    print(res)
    if res is None:
        await message.reply("Профиль доступен только приключенцам. "
                            "Вам нужно прибыть на континент Инврис для просмотра профиля."
                            "(напишите /start или /go)")
    else:
        await message.reply(
            f"Приключенченское имя: {res[2]}\nКласс: {classes_by_name[res[3]].name}\nОпыт: {res[4]} единиц\n<b>Характеристики</b>:\n"
            f"Телосложение: <b>{res[5]}</b> Ловкость: <b>{res[6]}</b>\nИнтеллект: <b>{res[7]}</b> Мудрость\харизма: <b>{res[8]}</b>\n"
            f"<b>Родство с магией</b>:\nОгонь: <b>{res[9]}</b> Вода(лед): <b>{res[10]}</b>\nМолния: <b>{res[11]}</b> Пространство: <b>{res[13]}</b>\n"
            f"<b><i>Бонус элементарной магии:</i></b> <b>+{res[12]}</b>\n", parse_mode="html")


@dp.message_handler(commands=['start', 'go'])
async def create_player(message: types.Message):
    await Database.create()
    chars = []
    for i in range(4):
        chars.append(r.randint(1, 8))
    for i in range(3):
        chars.append(round(r.random() * 1.5, 2))
    print(message.from_user)
    param = (message.from_user.id, message.from_user.username, 'classless', 0, chars[0], chars[1], chars[2],
             chars[3], chars[4], chars[5], chars[6], round(r.random() * 0.2, 2),
             round(r.random() * 0.75, 2))
    print(param)
    res = await Database().fetchone(f"SELECT * FROM players_stat WHERE telegram_id={message.from_user.id}")
    if res is None:
        await message.answer(texts.start)
        await Database().exec_and_commit(
            sql="INSERT INTO players_stat VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", parameters=param)
        await profile(message)
        await change_class(message)
    else:
        await message.answer("Вы уже отправились в приключение!")
    print(await Database().fetchone(f"SELECT * FROM players_stat WHERE telegram_id={message.from_user.id}"))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)