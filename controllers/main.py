from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from controllers.jwt import create_access_token, verify_token
from model.usuario import Usuario as UsuarioModel, UsuarioCreate, UsuarioList, UsuarioConsulta
from data.database import session, Usuario
from datetime import timedelta, datetime
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TokenData(BaseModel):
    username: str
    password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_data = verify_token(token, credentials_exception)

    if not user_data or "id_usuario" not in user_data or "username" not in user_data:
        raise credentials_exception

    usuario_model = UsuarioModel(
        id_usuario=user_data["id_usuario"],
        username=user_data["username"],
    )

    return usuario_model

@app.post("/token")
async def login_for_access_token(form_data: TokenData):
    user = session.query(Usuario).filter(Usuario.username == form_data.username).first()
    if user is None or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou password estão incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/usuario/cadastro", response_model=UsuarioModel)
async def cadastrar_usuario(usuario: UsuarioCreate):
    usuario_decode = usuario.dict()
    usuario_decode["password"] = pwd_context.hash(usuario_decode["password"])
    usuario_decode["data_nascimento"] = datetime.strptime(usuario_decode["data_nascimento"], "%d%m%Y")
    usuario_banco = Usuario(**usuario_decode)
    try:
        session.add(usuario_banco)
        session.commit()
    except Exception as e:
        logging.error(
            "Erro ao registrar novo usuário no banco - controllers/main.py - cadastrar_usuario() " + str(usuario_decode) + str(e)
        )
        session.rollback()

    return UsuarioModel(**usuario_decode)

@app.get("/usuario/listar", response_model=list[UsuarioList])
async def listar_usuarios():
    usuarios = session.query(Usuario).all()
    usuarios_decode = []
    for usuario in usuarios:
        usuario_decode = usuario.__dict__
        usuario_decode["data_nascimento"] = usuario_decode["data_nascimento"].strftime("%d/%m/%Y")
        usuarios_decode.append(usuario_decode)

    return usuarios_decode

@app.get("/usuario/{id_usuario}", response_model=UsuarioConsulta)
async def get_usuario(id_usuario: int):
    usuario = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    usuario_decode = usuario.__dict__
    usuario_decode["data_nascimento"] = usuario_decode["data_nascimento"].strftime("%d/%m/%Y")
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )
    
    return usuario_decode

@app.put("/usuario/{id_usuario}", response_model=UsuarioModel)
async def update_usuario(id_usuario: int, usuario_update: UsuarioCreate):
    try:
        usuario_banco = session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if not usuario_banco:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado",
            )

        usuario_banco.username = usuario_update.username
        usuario_banco.email = usuario_update.email
        usuario_banco.password = pwd_context.hash(usuario_update.password)
        usuario_banco.cpf = usuario_update.cpf
        usuario_banco.is_company = usuario_update.is_company
        usuario_banco.data_nascimento = datetime.strptime(usuario_update.data_nascimento, "%d%m%Y")

        session.commit()

        return usuario_banco
    
    except Exception as e:
        logging.error(
            "Erro ao atualizar usuário no banco - controllers/main.py - update_usuario() " + str(usuario_update) + str(e)
        )
        session.rollback()