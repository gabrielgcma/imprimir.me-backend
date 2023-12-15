from pydantic import BaseModel, Field, validator

class PedidoCreate(BaseModel):
    id_usuario: int
    id_empresa: int
    valor_pedido: float
    valor_repassado: float
    numero_copias: int
    arquivos: str
    tamanho_papel: str
    paginas_por_folha: int
    margens: str
    paginas: str
    disposicao: str
    is_color: bool

class PedidoConsultaUser(BaseModel):
    id_empresa: int
    valor_pedido: float
    numero_copias: int
    tamanho_papel: str
    is_color: bool