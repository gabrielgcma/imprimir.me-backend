import os

config = {
    "host": os.getenv("RABBITMQ_HOST"),
    "port": os.getenv("RABBITMQ_PORT"),
    "exchange": "documentos_a_imprimir",
    "queue": "empresa_0",
}
