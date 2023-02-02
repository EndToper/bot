import asyncio
import logging
import random as r
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from sql import Database





import texts


API_TOKEN = '6184666539:AAHBWOSpJs9bv41qw-1dL9EBXjQ4In-E8FE'



bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


'''@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["С пюрешкой", "Без пюрешки"]
    keyboard.add(*buttons)
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)

@dp.message_handler(Text(equals="С пюрешкой"))
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор!",reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == "Без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!",reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands="random")
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
    await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10", reply_markup=keyboard)

@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(str(r.randint(1, 10)))
    await call.answer()

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)'''

@dp.message_handler(commands=['start','s','go'])
async def create_player(message: types.Message):
    await Database.create()
    chars =[]
    for i in range(4):
        chars.append(r.randint(1,8))
    for i in range(3):
        chars.append(round(r.random()*1.5,2))
    print(message.from_user)
    param = (message.from_user.id,message.from_user.username, None,0, chars[0], chars[1],chars[2],
                                    chars[3],chars[4],chars[5],chars[6],round(r.random()*0.2,2),
                                   round(r.random()*0.75,2))
    print(param)
    res = await Database().fetchone(f"SELECT * FROM players_stat WHERE telegram_id={message.from_user.id}")
    if res is None:
        await message.answer(texts.start)
        await Database().exec_and_commit(
            sql="INSERT INTO players_stat VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", parameters=param)
    else:
        await message.answer("Вы уже отправились в приключение!")
    print(await Database().fetchone(f"SELECT * FROM players_stat WHERE telegram_id={message.from_user.id}"))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)