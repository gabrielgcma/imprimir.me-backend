from pydantic import BaseModel
from datetime import datetime

class Usuario(BaseModel):
    username: str
    email: str
    password: str
    cpf: str
    is_company: bool = False
    data_nascimento: datetime

class UsuarioCreate(BaseModel):
    username: str
    password: str
    email: str
    cpf: str
    is_company: bool = False
    data_nascimento: str

class UsuarioConsulta(BaseModel):
    id_usuario: int
    username: str
    email: str
    cpf: str
    is_company: bool
    data_nascimento: str

class UsuarioList(BaseModel):
    id_usuario: int
    username: str
    email: str
    cpf: str
    is_company: bool
    data_nascimento: str