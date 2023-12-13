from pydantic import BaseModel

class UsuarioEmpresa_Relacionamento(BaseModel):
    id_usuario: int
    id_empresa: int
