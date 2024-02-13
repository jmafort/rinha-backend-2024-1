from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP

from api.database import Base


class ClienteModel(Base):
    __tablename__ = "clientes"
    __table_args__ = {"schema": "banco"}

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    limite = Column(Integer, nullable=False)
    saldo = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
