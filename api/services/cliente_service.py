from datetime import datetime
from api.DAOs.cliente_dao import ClienteDAO
from api.DAOs.transacao_dao import TransacaoDAO
from api.exceptions import NotFound
from api.schemas.transacao_schema import TransacaoRequestSchema, TransacaoResponseSchema


class ClienteService:

    def __init__(self):
        self._cliente_dao = ClienteDAO()
        self._transacao_dao = TransacaoDAO()

    def get_extrato(self, cliente_id: int) -> dict[str, list | dict]:
        """
        Monta o extrato de um cliente.

        Returns:
            {
                "data": "2024-01-17T02:34:41",
                "conta": {
                    "saldo": -9098,
                    "limite": 100000
                },
                "ultimas_transacoes": [
                    {
                        "valor": 10,
                        "tipo": "c",
                        "descricao": "descricao",
                        "realizada_em": "2024-01-17T02:34:38.543030Z"
                    },
                    {
                        "valor": 90000,
                        "tipo": "d",
                        "descricao": "descricao",
                        "realizada_em": "2024-01-17T02:34:38.543030Z"
                    }
                ]
            }
        
        Raises:
            `api.exceptions.NotFound` se o cliente não existir.
        """
        cliente = self._cliente_dao.get_cliente(cliente_id)
        if not cliente:
            raise NotFound
        
        extrato = {}
        extrato["saldo"] = {
            "valor": cliente.saldo,
            "data_extrato": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "limite": cliente.limite
        }

        transacoes = self._transacao_dao.get_ultimas_transacoes(cliente_id, 10)
        transacoes = [TransacaoResponseSchema.model_validate(transacao).model_dump() for transacao in transacoes]
        extrato["ultimas_transacoes"] = transacoes

        return extrato
    
    def create_transacao(self, cliente_id: int, transacao: TransacaoRequestSchema) -> dict[str, int]:
        """
        Cria uma nova transação para um cliente.

        Returns:
            {
                "saldo": -9000,
                "limite": 10000
            }

        Raises:
            `api.exceptions.NotFound` se o cliente não existir.
            `api.exceptions.LimiteInsuficiente` se o débito estourar o limite do cliente.
        """
        cliente = self._cliente_dao.get_cliente(cliente_id)
        if not cliente:
            raise NotFound
        
        saldo, limite = self._transacao_dao.create_transacao(cliente_id, transacao)

        return {"saldo": saldo, "limite": limite}
