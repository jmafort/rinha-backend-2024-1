from datetime import datetime
from enum import Enum

from pydantic import Field

from api.schemas import BaseSchema


class DescricaoEnum(str, Enum):
    c = 'c'
    d = 'd'


class TransacaoRequestSchema(BaseSchema):
    valor: int
    tipo: DescricaoEnum
    descricao: str | None = Field(default=None, max_length=10)


class TransacaoResponseSchema(TransacaoRequestSchema):
    realizada_em: datetime
