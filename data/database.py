from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, Float, LargeBinary
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Connection string no WSL:
url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="postgres",
    host="172.18.246.203",
    database="imprimirme",
    port=5434,
)

# Connection string Linux (Amado)
# url = URL.create(
#     drivername='postgresql+psycopg2',
#     username=os.getenv('POSTGRES_USER'),
#     password=os.getenv('POSTGRES_PASS'),
#     host=os.getenv('POSTGRES_HOST'),
#     database=os.getenv('POSTGRES_DATABASE'),
#     port=os.getenv('POSTGRES_PORT'),
# )

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    is_company = Column(Boolean, default=False)
    data_nascimento = Column(Date, nullable=False)


class Empresa(Base):
    __tablename__ = "empresa"

    id_empresa = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    cnpj = Column(String, nullable=False, unique=True)
    is_company = Column(Boolean, default=True)
    razao_social = Column(String, nullable=False)
    nome_fantasia = Column(String, nullable=False)
    chave_pix = Column(String, nullable=True, unique=True)
    pais = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    rua = Column(String, nullable=True)
    numero = Column(Integer, nullable=True)
    complemento = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    color_print = Column(Boolean, nullable=True)
    black_print = Column(Boolean, nullable=True)
    color_value = Column(Float, nullable=True)
    black_value = Column(Float, nullable=True)


class NotaFiscal(Base):
    __tablename__ = "nota_fiscal"

    id_nota = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_usuario = Column(Integer, nullable=False)
    id_empresa = Column(Integer, nullable=False)
    id_pedido = Column(Integer, nullable=False)


class Pedido(Base):
    __tablename__ = "pedido"

    id_pedido = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_usuario = Column(Integer, nullable=False)
    id_empresa = Column(Integer, nullable=False)
    valor_pedido = Column(Float, nullable=False)
    valor_repassado = Column(Float, nullable=False)
    numero_copias = Column(Integer, nullable=False)
    arquivos = Column(LargeBinary, nullable=False)
    tamanho_papel = Column(String, nullable=False)
    paginas_por_folha = Column(Boolean, nullable=False)
    margens = Column(String, nullable=False)
    paginas = Column(String, nullable=False)
    disposicao = Column(String, nullable=False)
    is_color = Column(Boolean, nullable=False)


Base.metadata.create_all(engine)
