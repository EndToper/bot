from sql import Database
from aiogram import types
from classes import  GameClass
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
                     "Темный инврисовый лес":['raven-mockingbird','distortion-envrisent','used-distortion-envrisent'],
                     "Портал":['raven-mockingbird','distortion-envrisent','fused-distortion-envrisent']}

monsters = ['Гоблин','Волк','Леший','Травяной паразит','Ядовитая слизь','Дух цветов',
            'Накки','Морге́на','Русалка','Мандрагора','Король духов цветов',
            'Длинношеий морской змей','Гигантский осьминог','Медуза Горгона',
            'Воин наги','Тень','Ворон-пересмешник','Камнелем',
            'Саламандра','Анчимайен, мальчик-шаровая-молния',
            'Инврисовая дриада','Инврисэнт',
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
            'Инврисовая дриада':20,'Инврисэнт':21,
            'Древний инврисэнт':22,'Искаженный инврисэнт':23,
            'Сросшиеся искаженные инврисэнты':24}


name_damage = {'fire': 'огнем', 'phys': 'физической силой', 'water': 'водой', 'ice': 'льдом', 'electro': 'молнией',
               'space': 'пространством', 'curse': 'проклятьем', 'poison': 'ядом', 'heal': '', 'melee': ''}

async def get_money(money):
    gold = money // 1000
    silver = (money - gold * 1000) // 10
    bronze = money - gold * 1000 - silver * 10
    return f'{gold} золотых, {silver} серебряных, {bronze} медяков'


async def perfor_enhanc(chars, rint, count, call, hp, max_hp):
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
    await Database().exec_and_commit(sql=f"UPDATE players_stat SET hp = ?, max_hp = ?"
                                         f" WHERE telegram_id = ?",
                                     parameters=(hp + (chars[0] - last_body) * 5,
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
    if "path" not in loc_obj.title:
        await message.answer_photo(protect_content=True,photo=types.InputFile(f"./assets/locations/{loc_obj.title}.png"),caption=text_loc, reply_markup=keyboard)
    else:
        await message.answer(text_loc, reply_markup=keyboard)





