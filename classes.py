class GameClass:
    def __init__(self,
                 name: str,
                 physical_damage_bonus: float,
                 damage_by_arrows_bonus: float,
                 fire_damage_bonus: float,
                 water_damage_bonus: float,
                 electro_damage_bonus: float,
                 space_damage_bonus: float,
                 curses_damage_bonus: float,
                 heal_bonus: float,
                 ability_number):
        self.pdb = physical_damage_bonus
        self.dab = damage_by_arrows_bonus
        self.fdb = fire_damage_bonus
        self.wdb = water_damage_bonus
        self.edb = electro_damage_bonus
        self.sdb = space_damage_bonus
        self.cdb = curses_damage_bonus
        self.heal = heal_bonus
        self.name = name
        self.ability_number = ability_number


class Enemy:
    def __init__(self,name, hp, dex, physical_damage, fire_damage, water_damage, electro_damage):
        self.name = name
        self.hp = hp
        self.dex = dex
        self.phys_dam = physical_damage
        self.fire_dam = fire_damage
        self.wat_dam = water_damage
        self.el_dam = electro_damage