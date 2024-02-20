import asyncio
import os
import sqlite3
from contextlib import closing

from crawler import Crawler
from database import Database


def main(groups: list[str]):
    with closing(sqlite3.connect("db.db")) as conn:
        database = Database.initialize(conn)
        crawler = Crawler(os.getenv("API_ID", "API_HASH"), database)
        crawler.run(groups)
        conn.commit()


main([
    "ru2chnews",
    "comentlentach",
    "poputka_kg",
    "nevzorovtvchat",
    "Ateo_Chat",
])
