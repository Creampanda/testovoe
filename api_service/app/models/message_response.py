from pydantic import BaseModel


class MessageResponse(BaseModel):
    """
    MessageResponse представляет собой модель данных для сообщения ответа.

    Attributes:
        message (str): Сообщение.
    """

    message: str
