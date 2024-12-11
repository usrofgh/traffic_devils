from src.entities.message.exceptions import MessageNotFound
from src.entities.message.model import MessageModel
from src.entities.message.repository import MessageRepository
from src.entities.message.schemas import MessageCreateDBSchema, MessageCreateSchema, MessageFilterSchema
from src.entities.user.model import UserModel
from src.tg import send_msg_to_tg


class MessageService:
    def __init__(self, repository: MessageRepository):
        self._repository = repository

    async def create_message(self, schema: MessageCreateSchema, author_id: int) -> MessageModel:
        tg_response = await send_msg_to_tg(**schema.model_dump())
        db_schema = MessageCreateDBSchema(**schema.model_dump(), author_id=author_id, tg_response=tg_response)
        return await self._repository.add_one(db_schema)

    async def get_messages(self, filter_schema: MessageFilterSchema, cur_user: UserModel) -> list[MessageModel]:
        author_ids = []
        if cur_user.role.name == "admin":
            pass
        if cur_user.role.name == "user":
            author_ids.append(cur_user.id)
        elif cur_user.role.name == "manager":
            author_ids.extend([client.id for client in cur_user.clients])
            author_ids.append(cur_user.id)

        return await self._repository.get_messages(
            author_ids=author_ids,
            **filter_schema.model_dump(exclude_none=True)
        )

    async def get_message_by_id(self, message_id: int, curr_user: UserModel) -> MessageModel:
        db_msg = await self._repository.find_one(id=message_id)
        if not db_msg:
            raise MessageNotFound

        if (
                curr_user.id != db_msg.author_id and  # not an author of a post
                db_msg.author_id not in [client.id for client in curr_user.clients] and  # not a manager of post author
                curr_user.role != "admin"  # curr_user is not an admin
        ):
            raise MessageNotFound  # Not found if the user doesn't have permissions for this post

        return db_msg

    async def delete_message(self, message_id: int, curr_user: UserModel) -> None:
        db_msg: MessageModel = await self._repository.find_one(id=message_id)
        if not db_msg:
            raise MessageNotFound

        if (
                curr_user.id != db_msg.author_id and  # not an author of a post
                db_msg.author_id not in [client.id for client in curr_user.clients] and # not a manager of a post author
                curr_user.role != "admin"  # curr_user is not an admin
        ):
            raise MessageNotFound  # Not found if the user doesn't have permissions for this post

        await self._repository.delete(db_msg)
