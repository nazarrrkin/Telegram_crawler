from pyrogram import Client
from pyrogram.enums import ChatType

from db import Database


class Crawler:
    def __init__(self, api_id: int, api_hash: str, database: Database):
        app = Client("33748350451", api_id, api_hash)
        app.connect()
        self.app = app
        self.database = database
        self.fetched_users = set()

    def run(self, groups: list[str]):
        self.app.run(self.fetch_many(groups))

    async def fetch_many(self, groups: list[str]):
        for group_name in groups:
            group = await self.app.get_chat(group_name)
            if group.type == ChatType.CHANNEL:
                print(f"Scanning channel: {group}")
                await self.fetch_group(group)
            elif group.type == ChatType.SUPERGROUP:
                print(f"Scanning chat: {group}")
                await self.fetch_chat(group)

    async def fetch_group(self, group):
        await self.app.join_chat(group.id)
        self.database.add_group(group.id, group.username)
        async for post in self.app.get_chat_history(group.id):
            self.database.commit()
            post_id = post.id
            if post.photo or post.video or post.document:
                content = await self.app.download_media(post)
                if post.photo:
                    self.database.add_post(
                        post_id, group.id, post.caption, post.photo.file_unique_id
                    )
                    self.database.add_media_from_post(post.photo.file_unique_id, content)
                if post.video:
                    self.database.add_post(
                        post_id, group.id, post.caption, post.video.file_unique_id
                    )
                    self.database.add_media_from_post(post.video.file_unique_id, content)
                if post.document:
                    self.database.add_post(
                        post_id,
                        group.id,
                        post.caption,
                        post.document.file_unique_id,
                    )
                    self.database.add_media_from_post(
                        post.document.file_unique_id, content
                    )
            if post.text:
                self.database.add_post(post_id, group.id, post.text, None)

            try:
                async for message in self.app.get_discussion_replies(group.id, post_id):
                    try:
                        if message.media:
                            content = await self.app.download_media(message)
                            if message.photo:
                                self.database.add_comment(
                                    message.id,
                                    post_id,
                                    message.from_user.id,
                                    message.caption,
                                    message.photo.file_unique_id,
                                    message.date,
                                )
                                self.database.add_media_from_user(
                                    message.photo.file_unique_id, content
                                )
                            if message.video:
                                self.database.add_comment(
                                    message.id,
                                    post_id,
                                    message.from_user.id,
                                    message.caption,
                                    message.video.file_unique_id,
                                    message.date,
                                )
                                self.database.add_media_from_user(
                                    message.video.file_unique_id, content
                                )
                            if message.document:
                                self.database.add_comment(
                                    message.id,
                                    post_id,
                                    message.from_user.id,
                                    message.caption,
                                    message.document.file_unique_id,
                                    message.date,
                                )
                                self.database.add_media_from_user(
                                    message.document.file_unique_id, content
                                )
                        if message.text:
                            self.database.add_comment(
                                message.id,
                                post_id,
                                message.from_user.id,
                                message.text,
                                None,
                                message.date,
                            )

                        if message.from_user.id not in self.fetched_users:
                            self.database.add_user(
                                message.from_user.id,
                                message.from_user.username,
                                message.from_user.first_name,
                                message.from_user.last_name,
                            )
                            self.fetched_users.add(message.from_user.id)
                    except AttributeError:
                        pass
            except:
                continue

    async def fetch_chat(self, chat):
        count = 0
        await self.app.join_chat(chat.id)
        self.database.add_chat(chat.id, chat.username)
        async for message in self.app.get_chat_history(chat.id):
            self.database.commit()
            try:
                if message.text:
                    self.database.add_message(
                        message.id,
                        chat.id,
                        message.from_user.id,
                        message.text,
                        None,
                        message.date,
                    )
                    count += 1

                if message.from_user.id not in self.fetched_users:
                    self.database.add_user(
                        message.from_user.id,
                        message.from_user.username,
                        message.from_user.first_name,
                        message.from_user.last_name,
                    )
                    self.fetched_users.add(message.from_user.id)
                if count > 333333:
                    break
            except AttributeError:
                pass
