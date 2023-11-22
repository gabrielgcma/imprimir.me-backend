from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from model.usuario import Usuario as UsuarioModel, UsuarioCreate, UsuarioList, UsuarioConsulta
from data.database import session
from services.usuarioservice import UsuarioCrud
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
