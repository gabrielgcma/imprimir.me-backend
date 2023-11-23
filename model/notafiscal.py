from pydantic import BaseModel

class NotaFiscal(BaseModel):
    id_usuario: int
    id_empresa: int
    id_pedido: int
    # id_pagamento: int
    # data_emissao: str
    # data_vencimento: str
    # valor: float
    # status: str

class NotaFiscalCreate(BaseModel):
    id_usuario: int
    id_empresa: int
    id_pedido: int