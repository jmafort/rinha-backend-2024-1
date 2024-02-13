from uuid import uuid4

from sqlalchemy import Column, UUID, ForeignKey, Integer, String, TIMESTAMP

from api.database import Base
from api.models.cliente_model import ClienteModel


class TransacaoModel(Base):
    __tablename__ = "transacoes"
    __table_args__ = {"schema": "banco"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    cliente_id = Column(Integer, ForeignKey(ClienteModel.id), nullable=False)
    valor = Column(Integer, nullable=False)
    tipo = Column(String(1), nullable=False)
    descricao = Column(String(10))
    realizada_em = Column(TIMESTAMP)
