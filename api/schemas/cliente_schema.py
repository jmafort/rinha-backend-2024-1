from datetime import datetime

from pydantic import Field, field_serializer

from api.schemas import BaseSchema


class ClienteBaseSchema(BaseSchema):
    limite: int
    saldo: int


class ClienteRequestSchema(ClienteBaseSchema):
    nome: str = Field(max_length=100)


class ClienteResponseSchema(ClienteRequestSchema):
    id: int
    created_at: datetime
    updated_at: datetime | None
