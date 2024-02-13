from datetime import datetime
from sqlalchemy import desc

from sqlalchemy.orm import Session

from api.database import get_db
from api.exceptions import LimiteInsuficiente
from api.models.cliente_model import ClienteModel
from api.models.transacao_model import TransacaoModel
from api.schemas.transacao_schema import TransacaoRequestSchema


class TransacaoDAO:

    def __init__(self):
        self._db_session: Session = next(get_db())

    def get_ultimas_transacoes(self, cliente_id: int, quantidade: int) -> list[TransacaoModel]:
        """
        Recuperar as últimas X transações.
        
        Returns:
            `[TransacaoModel,...]`: lista das transações.
        """
        transacoes = self._db_session.query(TransacaoModel) \
            .filter(TransacaoModel.cliente_id == cliente_id) \
            .order_by(desc(TransacaoModel.realizada_em)) \
            .limit(quantidade).all()

        return transacoes
    
    def create_transacao(self, cliente_id: int, transacao: TransacaoRequestSchema) -> tuple[int, int]:
        """
        Registra uma nova transação.

        Returns:
            `(int, int)`: saldo atualizado e limite do cliente.

        Raises:
            `api.exceptions.LimiteInsuficiente` se o débito estourar o limite do cliente.
        """
        nova_transacao = TransacaoModel(
            cliente_id=cliente_id,
            realizada_em=datetime.now(),
            **transacao.model_dump()
        )
        cliente: ClienteModel = self._db_session.query(ClienteModel).with_for_update().get(cliente_id)

        if nova_transacao.tipo == 'c':
            cliente.saldo += nova_transacao.valor
        elif nova_transacao.tipo == 'd':
            if (cliente.saldo - nova_transacao.valor) < -cliente.limite:
                self._db_session.rollback()
                raise LimiteInsuficiente(f"Limite excedido por {abs(cliente.saldo - nova_transacao.valor + cliente.limite)}")
            
            cliente.saldo -= nova_transacao.valor

        novo_saldo = cliente.saldo
        limite = cliente.limite
        cliente.updated_at = datetime.now()
        self._db_session.commit()

        self._db_session.add(nova_transacao)
        self._db_session.commit()

        return novo_saldo, limite
