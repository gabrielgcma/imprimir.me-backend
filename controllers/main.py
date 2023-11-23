from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from model.usuario import Usuario as UsuarioModel, UsuarioCreate, UsuarioList, UsuarioConsulta
from model.empresa import Empresa as EmpresaModel, EmpresaCreate
from model.notafiscal import NotaFiscal as NotaFiscalModel, NotaFiscalCreate
from data.database import session
from services.usuarioservice import UsuarioCrud
from services.empresaservice import EmpresaCrud
from services.notafiscalservice import NotaFiscalCrud
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData(BaseModel):
    username: str
    password: str

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
usuario_crud = UsuarioCrud(db_session=session)
empresa_crud = EmpresaCrud(db_session=session)
notafiscal_crud = NotaFiscalCrud(db_session=session)

@app.post("/token")
async def login_for_access_token(form_data: TokenData):
    return usuario_crud.login_for_access_token(form_data)

@app.post("/usuario/cadastro", response_model=UsuarioModel)
async def cadastrar_usuario(usuario: UsuarioCreate):
    return usuario_crud.cadastrar_usuario(usuario)

@app.get("/usuario/listar", response_model=list[UsuarioList])
async def listar_usuarios():
    return usuario_crud.listar_usuarios()

@app.get("/usuario/{id_usuario}", response_model=UsuarioConsulta)
async def get_usuario(id_usuario: int):
    return usuario_crud.get_usuario(id_usuario)

@app.put("/usuario/{id_usuario}", response_model=UsuarioModel)
async def update_usuario(id_usuario: int, usuario_update: UsuarioCreate):
    return usuario_crud.update_usuario(id_usuario, usuario_update)

@app.post("/empresa/cadastro", response_model=EmpresaModel)
async def cadastrar_empresa(empresa: EmpresaCreate):
    return empresa_crud.cadastrar_empresa(empresa)

@app.get("/empresa/listar", response_model=list[EmpresaModel])
async def listar_empresas():
    return empresa_crud.listar_empresas()

@app.get("/empresa/{id_empresa}", response_model=EmpresaModel)
async def get_empresa(id_empresa: int):
    return empresa_crud.get_empresa(id_empresa)

@app.put("/empresa/{id_empresa}", response_model=EmpresaModel)
async def update_empresa(id_empresa: int, empresa_update: EmpresaCreate):
    return empresa_crud.update_empresa(id_empresa, empresa_update)

@app.post("/notafiscal/cadastro", response_model=NotaFiscalModel)
async def cadastrar_nota_fiscal(notafiscal: NotaFiscalCreate):
    return notafiscal_crud.cadastrar_nota_fiscal(notafiscal)

@app.get("/notafiscal/listar", response_model=list[NotaFiscalModel])
async def listar_notas():
        return notafiscal_crud.listar_notas()

@app.get("/notafiscal/{id_nota}", response_model=NotaFiscalModel)
async def get_notafiscal(id_nota: int):
        return notafiscal_crud.get_notafiscal(id_nota)