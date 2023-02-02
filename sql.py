
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
            "(id int primary key, telegram_id int, nick text, class text, level int, body int, intellect int, dexterity int, wisdom int,"
            " fire int, water int, electro int, element int, space int)"
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
