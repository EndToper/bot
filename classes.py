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
