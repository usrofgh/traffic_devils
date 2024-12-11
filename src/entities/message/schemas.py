from pydantic import BaseModel


class MessageCreateSchema(BaseModel):
    bot_token: str
    chat_id: str
    message: str


class MessageCreateDBSchema(MessageCreateSchema):
    author_id: int
    tg_response: dict


class MessageReadSchema(BaseModel):
    id: int
    bot_token: str
    chat_id: str
    author_id: int
    message: str
    tg_response: dict | None


class MessageFilterSchema(BaseModel):
    author_id: int | None = None
    bot_token: str | None = None
    chat_id: str | None = None
    offset: int | None = None
    limit: int | None = None
