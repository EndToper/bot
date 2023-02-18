class MagicType:
    def __init__(self,damage_type, count,title,name,level,cast_cost,type_char):
        self.damage_type = damage_type
        self.count = count
        self.title = title
        self.name = name
        self.level = level
        self.cast_cost = cast_cost
        self.type_char = type_char
        self.cost = 0

spell = [MagicType(['fire'],1,'fireball','Огненный шар',0, 0,'int'),
         MagicType(['water'],1,"watershot",'Водный выстрел',0, 0,'int'),
         MagicType(['electro'],1,'small_lightning','Быстрая молния',0, 0,'int'),
         MagicType(['space'],2,'earthshot','Земляная дробь',0, 0,'int'),
         MagicType(['space','heal'],1,'heal','Низшее исцеление',0, 0,'int'),
         MagicType(['fire'],2,'big_fireball','Большой огненный шар',5,6,'int'),
         MagicType(['fire'],3,'fire_arrow','Огненная стрела',10,9,'int'),
         MagicType(['fire','curse'],4,'curse_fire','Проклятое пламя',15, 16,'int'),
         MagicType(['fire','melee'],2,'fire_star','Звезда из огня',17,4,'int'),
         MagicType(['fire'],4,'fireball_rain','Дождь огненных шаров',20,12,'int'),
         MagicType(['fire','electro'],5,'fire_lightning','Огненная молния',25,25,'int'),
         MagicType(['fire','melee'],3,'fire_spikes','Огненные пики',30,7,'int'),
         MagicType(['fire'],5,'meteor_rain','Метеоритный дождь',40,21,'int'),
         MagicType(['fire'],6,'hellfire','Адское сожжение',50,36,'int'),
         MagicType(['water'],2,'waterfall','Водопад',3,5,'int'),
         MagicType(['water','poison'],1,'poisonshot','Ядовитый выстрел',6,0,'int'),
         MagicType(['water','poison'],3,'poison','Отравление',15,8,'int'),
         MagicType(['ice'],4,'ice_dagger','Ледяной кинжал',25,11,'int'),
         MagicType(['ice','poison'],5,'poisoned_ice_arrow','Отравленная ледяная стрела',30,25,'int'),
         MagicType(['electro','melee'],3,'electro_lasso','Электролассо',20,8,'int'),
         MagicType(['electro'],4,'lightning_bolt','Молния',35,19,'int'),
         MagicType(['electro'],5,'storm','Шторм',50,25,'int'),
         MagicType(['space','fire','electro'],3,'fire_electro_arrow','Огненная электрострела',10,20,'int'),
         MagicType(['space','curse','poison','melee'],4,'poison_cursed_sword','Проклятый ядовитый меч',20,25,'int'),
         MagicType(['space','ice','electro'],5,'space_attack','Пространственный удар',30,36,'int'),
         MagicType(['space','melee'],9,'space_slice','Разруб пространства',40,32,'int'),
         MagicType(['space'],11,'space_boom','Взрыв пространства',50,36,'int'),
         MagicType(['space'],14,'space_deformation','Искажение пространства',60,40,'int'),
         MagicType(['space'],16,'space_collapse','Коллапс пространства',70,44,'int'),
         MagicType(['space','heal'],2,'small_heal','Малое исцеление',15,2,'int'),
         MagicType(['space','heal'],3,'middle_heal','Среднее исцеление',35,3,'int'),
         MagicType(['space','heal'],4,'high_heal','Высшее исцеление',55,4,'int'),
         MagicType(['space','heal'],5,'absolute_heal','Абсолютное исцеление',70,5,'int')]