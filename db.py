import datetime
import sqlite3


class Database:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    @classmethod
    def initialize(cls, conn):
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT
            );
            
            CREATE TABLE IF NOT EXISTS media_from_user (
                media_file_id TEXT PRIMARY KEY REFERENCES comments(media_file_id),
                content TEXT
            );
            
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                post_id INTEGER REFERENCES post(id),
                author_id INTEGER REFERENCES users(id),
                media_file_id TEXT,
                message TEXT,
                data DATETIME
            );
            
            CREATE TABLE IF NOT EXISTS media_from_post (
                media_file_id TEXT PRIMARY KEY REFERENCES post(media_file_id),
                content TEXT
            );
            
            CREATE TABLE IF NOT EXISTS post (
                id INTEGER PRIMARY KEY,
                group_id INTEGER REFERENCES groups(id),
                message TEXT,
                media_file_id TEXT
            );
            
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
            
            CREATE TABLE IF NOT EXISTS message (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER REFERENCES chat(id),
                author_id INTEGER REFERENCES users(id),
                media_file_id TEXT,
                message TEXT,
                data DATETIME
            );
            
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
            
            """
        )
        return cls(conn)

    def add_user(self, id: int, username: str, first_name: str, last_name: str):
        self.conn.execute(
            "INSERT INTO users(id, username, first_name, last_name) VALUES(?, ?, ?, ?)",
            (id, username, first_name, last_name),
        )

    def add_media_from_user(self, media_file_id: str, content: str):
        self.conn.execute(
            "INSERT INTO media_from_user (media_file_id, content) VALUES(?, ?)",
            (media_file_id, content),
        )

    def add_comment(
        self,
        id: int,
        post_id: int,
        author_id: int,
        message: str,
        media_file_id: str,
        data: datetime.datetime,
    ):
        self.conn.execute(
            "INSERT INTO comments (id, post_id, author_id, message, media_file_id, data) VALUES(?, ?, ?, ?, ?, ?)",
            (id, post_id, author_id, message, media_file_id, data),
        )

    def add_media_from_post(self, media_file_id: str, content: str):
        self.conn.execute(
            "INSERT INTO media_from_post (media_file_id, content) VALUES(?, ?)",
            (media_file_id, content),
        )

    def add_post(
        self, id: int, group_id: int, message: str, media_file_id: str
    ):
        self.conn.execute(
            "INSERT INTO post (id, group_id, message, media_file_id) VALUES(?, ?, ?, ?)",
            (id, group_id, message, media_file_id),
        )

    def add_group(self, id: int, name: str):
        self.conn.execute(
            "INSERT INTO groups(id, name) VALUES(?, ?)", (id, name)
        )

    def add_message(
        self,
        id: int,
        chat_id: int,
        author_id: int,
        message: str,
        media_file_id: str,
        data: datetime.datetime,
    ):
        self.conn.execute(
            "INSERT INTO message (id, chat_id, author_id, message, media_file_id, data) VALUES(?, ?, ?, ?, ?, ?)",
            (id, chat_id, author_id, message, media_file_id, data),
        )

    def add_chat(self, id: int, name: str):
        self.conn.execute(
            "INSERT INTO chats (id, name) VALUES(?, ?)", (id, name)
        )

    def commit(self):
        self.conn.commit()
