from pydantic import BaseModel

class Usuario(BaseModel):
    id_usuario: int
    username: str
    email: str
    hashed_password: str
    cpf: str
    is_company: bool = False
    data_nascimento: str

class UsuarioCreate(BaseModel):
    username: str
    password: str
    email: str
    cpf: str
    is_company: bool = False
    data_nascimento: str