from fastapi import APIRouter, HTTPException, status
from api.exceptions import LimiteInsuficiente, NotFound

from api.schemas.transacao_schema import TransacaoRequestSchema, TransacaoResponseSchema
from api.schemas.cliente_schema import ClienteRequestSchema, ClienteResponseSchema
from api.services.cliente_service import ClienteService


router = APIRouter(prefix="/clientes")

@router.get("/{cliente_id}/extrato")
def get_extrato(cliente_id: int) -> dict:
    service = ClienteService()
    try:
        extrato = service.get_extrato(cliente_id)
        return extrato
    
    except NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    
@router.post("/{cliente_id}/transacoes")
def post_transacao(cliente_id: int, transacao: TransacaoRequestSchema) -> dict:
    service = ClienteService()
    try:
        response = service.create_transacao(cliente_id, transacao)
        return response
    
    except NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    except LimiteInsuficiente as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(e))

# @router.get("", status_code=status.HTTP_200_OK)
# def get_clientes(offset: int = 0, limit: int = 20) -> list[ClienteResponseSchema]:
#     clientes_repository = ClientesRepository()
#     clientes = clientes_repository.list_clientes(offset=offset, limit=limit)
#     return clientes

# @router.post("", status_code=status.HTTP_201_CREATED)
# def create_cliente(cliente: ClienteRequestSchema) -> dict[str, int]:
#     cliente_repository = ClientesRepository()
#     id = cliente_repository.create_cliente(cliente)
#     return {"id": id}

# @router.get("/{id}")
# def get_cliente(id: int) -> ClienteResponseSchema:
#     clientes_repository = ClientesRepository()
#     cliente = clientes_repository.get_cliente(id)
    
#     if not cliente:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
#     return cliente

# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_cliente(id: int) -> None:
#     cliente_repository = ClientesRepository()
#     cliente_existe = cliente_repository.delete_cliente(id)
#     if not cliente_existe:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# @router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def update_cliente(id: int, updated_info: ClienteRequestSchema) -> None:
#     cliente_repository = ClientesRepository()
#     cliente_existe = cliente_repository.update_cliente(id, updated_info)

#     if not cliente_existe:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

