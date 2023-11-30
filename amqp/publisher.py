import pika
import logging
import os
from .config import config

logger = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False
FORMAT = (
    "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.ERROR)


class Publisher(object):
    def publish(self, message):
        try:
            connection = self.create_connection()
            channel = connection.channel()

            channel.exchange_declare(exchange=config["exchange"])
            channel.queue_declare(queue=config["queue"])
            channel.queue_bind(
                exchange=config["exchange"],
                queue=config["queue"],
                routing_key="routing-key",
            )

            channel.basic_publish(
                exchange=config["exchange"], routing_key="routing-key", body=message
            )

            connection.close()

            logger.info("Documento do pedido enviado com sucesso!")

        except Exception as e:
            logger.error(f"Erro na conexão do RabbitMQ: {e}")

    def create_connection(self):
        credentials = pika.PlainCredentials(
            username=os.getenv("RABBITMQ_USER"), password=os.getenv("RABBITMQ_PASS")
        )
        param = pika.ConnectionParameters(
            host=config["host"], port=config["port"], credentials=credentials
        )
        return pika.BlockingConnection(param)
