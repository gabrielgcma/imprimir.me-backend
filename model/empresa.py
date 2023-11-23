from pydantic import BaseModel

class Empresa(BaseModel):
    username: str
    email: str
    password: str
    cnpj: str
    is_company: bool = True
    razao_social: str
    nome_fantasia: str
    chave_pix: str
    pais: str
    estado: str
    cidade: str
    bairro: str
    rua: str
    numero: int
    complemento: str
    cep: str
    longitude: float
    latitude: float
    color_print: bool = False
    black_print: bool = False
    color_value: float
    black_value: float

class EmpresaCreate(BaseModel):
    username: str
    password: str
    email: str
    cnpj: str
    is_company: bool = True
    razao_social: str
    nome_fantasia: str
    chave_pix: str
    pais: str
    estado: str
    cidade: str
    bairro: str
    rua: str
    numero: int
    complemento: str
    cep: str
    longitude: float
    latitude: float
    color_print: bool = False
    black_print: bool = False
    color_value: float
    black_value: float