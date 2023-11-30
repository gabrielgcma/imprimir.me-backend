import sys
import os

sys.path.append("..")

import pika
import logging
import json
from model.pedido import PedidoCreate

# print("aaaa")
# from data.database import Pedido
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    Date,
    Float,
    LargeBinary,
)
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy.engine import URL

config = {
    "user": "user",
    "password": "user",
    "host": "localhost",
    "port": 5672,
    "exchange": "documentos_a_imprimir",
    "queue": "empresa_0",
}

Base = declarative_base()


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


logger = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False
FORMAT = (
    "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


class Subscriber(object):
    def receive_msgs(self, db_session: Session):
        try:
            self.connection = self.create_connection()
            logger.info("Conexão com RabbitMQ estabelecida...")
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=config["queue"])

            def callback(ch, method, properties, body):
                logger.debug(f"[x] Mensagem recebida: \n\n {body}")
                registrar_pedido_bd(body, db_session)

            self.channel.basic_consume(
                queue=config["queue"], on_message_callback=callback, auto_ack=True
            )

            logger.info("Subscriber ativo e aguardando mensagens...")

            self.channel.start_consuming()
        except KeyboardInterrupt:
            print()
            logger.debug("O subscriber está sendo terminado...")
            self.stop_consuming()
            logger.debug("O subscriber foi terminado com sucesso...")

    def create_connection(self):
        credentials = pika.PlainCredentials(
            username=config["user"], password=config["password"]
        )
        params = pika.ConnectionParameters(
            host=config["host"], port=config["port"], credentials=credentials
        )
        return pika.BlockingConnection(params)

    def stop_consuming(self):
        self.channel.stop_consuming()
        self.connection.close()
        logger.debug("A conexão do subscriber foi interrompida com sucesso...")


def registrar_pedido_bd(msg_pedido, db_session: Session):
    pedido_decoded = msg_pedido.decode("utf-8")
    pedido_json = json.loads(pedido_decoded)

    pedido_json["arquivos"] = pedido_json["arquivos"].encode("utf-8")

    pedido_objeto = Pedido(**pedido_json)

    try:
        db_session.add(pedido_objeto)
        db_session.commit()
        return logger.debug(
            f"\nPedido {pedido_objeto.id_pedido} criado com sucesso no banco de dados."
        )
    except Exception as e:
        logger.error(
            f"Erro ao criar o registro do pedido no banco de dados -- registro_pedido_bd() - subscriber.py"
        )
        print(e.with_traceback())
        db_session.rollback()


if __name__ == "__main__":
    url_banco = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password="postgres",
        host="localhost",
        database="imprimirme",
        port="5432",
    )
    engine = create_engine(url_banco)
    Session = sessionmaker(bind=engine)
    session = Session()

    sub = Subscriber()
    sub.receive_msgs(db_session=session)
