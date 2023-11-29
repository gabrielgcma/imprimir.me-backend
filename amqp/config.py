import os

config = {
    "host": os.getenv("RABBITMQ_HOST"),
    "port": os.getenv("RABBITMQ_PORT"),
    "exchange": "empresa1",
    "queue": "documentos_a_imprimir",
}
