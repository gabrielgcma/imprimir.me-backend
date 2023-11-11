# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from controllers.jwt import create_access_token, verify_token
from model.usuario import Usuario as UsuarioModel, UsuarioCreate
from data.database import session, Usuario
from datetime import timedelta
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

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

@app.get("/users/me", response_model=UsuarioModel)
async def read_users_me(current_user: UsuarioModel = Depends(get_current_user)):
    return current_user

@app.post("/usuario/cadastro", response_model=UsuarioModel)
async def cadastrar_usuario(usuario: UsuarioCreate):
    usuario_decode = usuario.dict()
    usuario_banco = Usuario(**usuario_decode)
    session.add(usuario_banco)
    session.commit()
    
    usuario_decode["id_usuario"] = usuario_banco.id_usuario
    usuario_decode["hashed_password"] = "senha_fake"  
    
    return UsuarioModel(**usuario_decode)

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
