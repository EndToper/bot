
import aiosqlite

class Database:
    _instance = None
    _db: aiosqlite.Connection = None

    def __new__(cls, *args, **kwargs):

        return cls._instance

    @classmethod
    async def create(cls) -> None:
        """
        Creates a :class:`aiosqlite.Connection` to the database to make it accessible as a singleton.
        :return: None
        """

        db = await aiosqlite.connect("envris.db")

        await db.execute(
            "CREATE TABLE IF NOT EXISTS players_stat "
            "(id int primary key, telegram_id int, nick text, location text, class text, hp int, level int, exp level, body int, intellect int, dexterity int, wisdom int,"
            " fire int, water int, electro int, element int, space int)"
        )
        await db.commit()

        await db.execute(
            "CREATE TABLE IF NOT EXISTS players_inventory "
            "(telegram_id int, inventory_size int, inventory text, money int, last_body int, equip_armor text, equip_weapon text,"
            " equip_weapon2 text, equip_jewellery text, magic_spell1 text, magic_spell2 text, magic_spell3 text)"
        )
        await db.commit()

        cls._db = db
        cls._instance = super(Database, cls).__new__(cls)

    async def fetchone(
            self,
            sql: str):


        cursor = await self._db.execute(sql)
        res = await cursor.fetchone()
        await cursor.close()

        return res


    async def fetchall(
            self,
            sql: str):


        cursor = await self._db.execute(sql)
        res = await cursor.fetchall()
        await cursor.close()

        return res

    async def exec_and_commit(self, sql, parameters):

        await self._db.execute(sql, parameters)
        await self._db.commit()
