from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

# Connection string no WSL:

# url = URL.create(
#     drivername='postgresql+psycopg2',
#     username='postgres',
#     password='postgres',
#     host='172.18.246.203',
#     database='imprimirme',
#     port=5434
# )

# Connection string Linux (Amado)
url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="postgres",
    host="db",
    database="imprimirme",
    port=5432,
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    is_company = Column(Boolean, default=False)
    data_nascimento = Column(String, nullable=False)


Base.metadata.create_all(engine)
