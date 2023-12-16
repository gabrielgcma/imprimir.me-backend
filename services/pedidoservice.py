from fastapi import HTTPException, status
from model.pedido import PedidoCreate
from services.empresaservice import EmpresaCrud
from services.usuarioservice import UsuarioCrud
from data.database import Pedido
from utils.coerencia_pag_folhas import Validaçao_pag_folhas
from utils.decimalformatter import DecimalFormatter
from sqlalchemy.orm import Session
import logging

from amqp.publisher import Publisher

logging.basicConfig(level=logging.INFO)


class PedidoCrud:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def cadastrar_pedido(self, pedido: PedidoCreate):
        pedido_decode = pedido.dict()

        if (UsuarioCrud.get_usuario(self, pedido_decode['id_usuario']) == None):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )

        if (EmpresaCrud.get_empresa(self, pedido_decode['id_empresa']) == None):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa não encontrada",
            )
        
        Validaçao_pag_folhas.validar_coerencia_paginas_copias(pedido_decode.get("paginas_por_folha"), pedido_decode.get("numero_copias"))
        pedido_decode["valor_repassado"] = pedido.valor_pedido * 0.9
        DecimalFormatter.formatar_valor_decimal(pedido_decode["valor_repassado"])
        DecimalFormatter.formatar_valor_decimal(pedido_decode["valor_repassado"])

        pedido_banco = Pedido(**pedido_decode)

        try: 
            self.db_session.add(pedido_banco)
            self.db_session.commit()
        except Exception as e:
            logging.error(
                "Erro ao registrar novo Pedido no banco - controllers/main.py - cadastrar_pedido() " + str(pedido_decode) + str(e)
            )
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao cadastrar Pedido no banco",
            )
        
        return PedidoCreate(**pedido_decode)

    def listar_pedidos(self):
        pedidos = self.db_session.query(Pedido).all()
        pedidos_decode = []
        for pedido in pedidos:
            pedido_decode = pedido.__dict__
            pedidos_decode.append(pedido_decode)

        return pedidos_decode

    def get_pedido(self, id_pedido: int):
        pedido = (
            self.db_session.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
        )
        if pedido is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado",
            )

        pedido_decode = pedido.__dict__
        return pedido_decode

    def get_pedidos_empresa(self, id_empresa: int):
        pedidos = (
            self.db_session.query(Pedido).filter(Pedido.id_empresa == id_empresa).all()
        )
        if pedidos is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não há pedidos dessa empresa",
            )

        pedidos_decode = pedidos.__dict__
        return pedidos_decode

    def get_pedidos_usuario(self, id_usuario: int):
        pedidos = (
            self.db_session.query(Pedido).filter(Pedido.id_usuario == id_usuario).all()
        )
        if pedidos is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não há pedidos desse usuário",
            )

        pedidos_decode = pedidos.__dict__
        return pedidos_decode
