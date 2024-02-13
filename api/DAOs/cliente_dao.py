from datetime import datetime
from sqlalchemy.orm import Session

from api.database import get_db
from api.exceptions import NotFound
from api.schemas.cliente_schema import ClienteRequestSchema
from api.models.cliente_model import ClienteModel


class ClienteDAO:

    def __init__(self):
        self._db_session: Session = next(get_db())

    def list_clientes(self, offset: int, limit: int) -> list[ClienteModel]:
        clientes = self._db_session.query(ClienteModel).offset(offset).limit(limit).all()
        return clientes
    
    def get_cliente(self, id: int) -> ClienteModel | None:
        return self._db_session.query(ClienteModel).get(id)
    
    def create_cliente(self, cliente: ClienteRequestSchema) -> int:
        novo_cliente = ClienteModel(created_at=datetime.now(), **cliente.model_dump())
        self._db_session.add(novo_cliente)
        self._db_session.commit()
        self._db_session.refresh(novo_cliente)
        
        return novo_cliente.id
    
    def delete_cliente(self, id: int) -> None:
        cliente = self.get_cliente(id)
        if not cliente:
            raise NotFound
        
        self._db_session.delete(cliente)
        self._db_session.commit()

    def update_cliente(self, id: int, updated_info: ClienteRequestSchema) -> dict[str, str | int]:
        cliente = self.get_cliente(id)
        if not cliente:
            raise NotFound

        self._db_session.query(ClienteModel).filter(
            ClienteModel.id == id).with_for_update().update(updated_info.model_dump())
        self._db_session.commit()

        return updated_info.model_dump()