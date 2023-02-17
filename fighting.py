from sql import Database
from aiogram import types
from classes import basic_enemies, Enemy
from magic import spell
import random as r
from auxiliary import monsters, monsters_from_loc, number_by_name, classes_by_name, name_damage,perfor_enhanc,change_loc
from equip import weapons




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
    monster_title = ''
    for key in basic_enemies.keys():
        if monster.name == basic_enemies[key].name:
            monster_title = key
    await message.answer_photo(protect_content=True,photo=types.InputFile(f"./assets/{monster_title}.png"),caption=f"Ваш противник - {monster.name}\nХиты здоровья: {monster.hp}\nВаши хиты: {res[0]}/{res[1]}")
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
                                                callback_data=f"att_{result[i]}_{number_by_name[monster.name]}_{monster.hp}"))
    await message.answer(text='Выберите способ атаки', reply_markup=keyboard)


async def attack(call: types.CallbackQuery):
    await Database.create()
    attack = call.data.split("_")[1]
    m_name = monsters[int(call.data.split("_")[2])]
    m_hp = call.data.split("_")[3]
    await call.message.edit_text(f'Вы атакавали, используя {attack}')
    monster = None
    for elem in basic_enemies.values():
        if m_name == elem.name:
            monster = Enemy(elem.name, int(m_hp), elem.dex, elem.dam, elem.dam_type, elem.res, elem.drop, elem.xp,
                            elem.boss)
    weapon = None
    for elem2 in weapons:
        if attack == elem2.name:
            weapon = elem2
    for elem3 in spell:
        if attack == elem3.name:
            weapon = elem3
    chars = await Database().fetchone(
        f"SELECT body, dexterity, intellect, wisdom FROM players_stat WHERE telegram_id={call.message.chat.id}")
    print(chars)
    chars = [int(chars[0]), int(chars[1]), int(chars[2]), int(chars[3])]
    magic_affinity = await Database().fetchone(
        f"SELECT fire, water, electro, element, space FROM players_stat WHERE telegram_id={call.message.chat.id}")
    level = await Database().fetchone(
        f"SELECT level FROM players_stat WHERE telegram_id={call.message.chat.id}")
    level = int(level[0])
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
    if 'bod' in weapon.type_char or 'dex' in weapon.type_char:
        weapon_damage = 0
        for i in range(2 * weapon.count if r.randint(1, 10) == 1 and pl_class.type == 'archer' else weapon.count):
            weapon_damage += r.randint(1, weapon.dice)
        damage = weapon_damage
        damage += chars[0] / 1.5 if 'bod' in weapon.type_char and pl_class.type == 'warrior' else chars[0] / 2 if 'bod' in weapon.type_char else chars[1]/ 1.5 if 'dex' in weapon.type_char and pl_class.type == 'archer' else chars[1] / 2
        rw = r.randint(1, 1000)
        damage = damage * 2 if rw <= 125 and pl_class.type == 'warrior' else damage
    elif 'int' in weapon.type_char:
        magic_damage = 0
        for i in range(weapon.count):
            intel = round((chars[2]*0.5) if chars[2] > 40 else (round(chars[2]*0.7) if chars[2] > 20 else chars[2])) * (0.5 if chars[2] > 40 else (0.7 if chars[2] > 20 else 1))
            intel = int(intel) if weapon.damage_type == ['space'] or weapon.damage_type == ['space','melee'] else int(chars[2])
            print(intel)
            magic_damage += r.randint(1, intel)
            print(magic_damage)
        for elem in weapon.damage_type:
            magic_damage = magic_damage * (bonus[elem]
                                           + (element if elem in ['fire', 'electro', 'water', 'ice'] else 0)
                                           + (0.1 if pl_class.type == 'mage' else 0)
                                           + (0.4 if weapon.damage_type == ['space'] or weapon.damage_type == ['space','melee'] else 0)
                                           - (0.1 if elem == 'space' and weapon.damage_type != ['space'] or weapon.damage_type != ['space','melee'] else 0))
        damage = magic_damage if 'heal' not in weapon.damage_type else 0
    print(damage)
    damage = damage * (0.5+level/(10+level)) if weapon.damage_type == ['space'] or weapon.damage_type == ['space','melee'] else damage
    print(damage)
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
    dex = chars[1] / weapon.nerf_dex if weapon.type_char != 'int' else chars[1]
    if dex > monster.dex and 'melee' not in weapon.damage_type:
        if rand < 85:
            monster_damage = 0
    elif round(dex / monster.dex * 100 if dex / monster.dex * 100 <= 80 else 80) > rand and 'melee' not in weapon.damage_type:
        monster_damage = 0
    elif round(dex / monster.dex * 100) > rand and 'melee' in weapon.damage_type and round(
            chars[1] / monster.dex * 100) < 50:
        monster_damage = 0
    elif 50 > rand and round(dex / monster.dex * 100) > 50 and 'melee' in weapon.damage_type:
        monster_damage = 0
    hp -= monster_damage
    await call.message.answer(
        f'Вы нанесли монстру {damage + (chars[3] if "poison" in weapon.damage_type else 0) + curse_dam}'
        f' урона {", ".join(damages)}\nВам нанесено {monster_damage} урона {", ".join(mon_damages)}')
    if 'heal' in weapon.damage_type:
        hp = hp + 3*round(magic_damage) + 1 if hp + 3*round(magic_damage) + 1 < max_hp else max_hp
        await call.message.answer(f'Вы восстановили {3*round(magic_damage) + 1} хитов')
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
        exp = await Database().fetchone(
            f"SELECT  exp FROM players_stat WHERE telegram_id={call.message.chat.id}")
        await Database().exec_and_commit(sql=f"UPDATE players_stat SET hp = ?"
                                             f" WHERE telegram_id = ?",
                                         parameters=(round(max_hp / 2) if hp < round(max_hp / 2) else hp, call.message.chat.id))
        exp = int(exp[0])
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