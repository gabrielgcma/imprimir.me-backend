from pydantic import BaseModel, ConfigDict

# BaseModel.model_config['arbitrary_types_allowed'] = True

class PedidoCreate(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)

    id_pedido: int
    id_usuario: int
    id_empresa: int
    valor_pedido: float
    valor_repassado: float
    numero_copias: int
    arquivos: bytes
    tamanho_papel: str
    paginas_por_folha: bool
    margens: str
    paginas: str
    disposicao: str
    is_color: bool

# Para consultas do usuário, como visualização do histórico de pedidos:
class PedidoConsultaUser(BaseModel):
    id_empresa: int
    valor_pedido: float
    numero_copias: int
    tamanho_papel: str
    is_color: bool