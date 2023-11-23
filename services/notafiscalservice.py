from fastapi import HTTPException, status
from model.notafiscal import NotaFiscal as NotaFiscalModel, NotaFiscalCreate
from data.database import NotaFiscal
import logging

logging.basicConfig(level=logging.INFO)


class NotaFiscalCrud:
    def __init__(self, db_session):
        self.db_session = db_session

    def cadastrar_nota_fiscal(self, notafiscal: NotaFiscalCreate):
        notafiscal_decode = notafiscal.dict()
        notafiscal_banco = NotaFiscal(**notafiscal_decode)
        
        try:
            self.db_session.add(notafiscal_banco)
            self.db_session.commit()
        except Exception as e:
            logging.error(
                "Erro ao registrar nova Nota Fiscal no banco - controllers/main.py - cadastrar_nota_fiscal() " + str(notafiscal_decode) + str(e)
            )
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao cadastrar Nota Fiscal no banco",
            )

        return NotaFiscalModel(**notafiscal_decode)

    def listar_notas(self):
        notas = self.db_session.query(NotaFiscal).all()
        notasfiscais_decode = []
        for notafiscal in notas:
            notafiscal_decode = notafiscal.__dict__
            notasfiscais_decode.append(notafiscal_decode)

        return notasfiscais_decode

    def get_notafiscal(self, id_nota: int):
        notafiscal = self.db_session.query(NotaFiscal).filter(NotaFiscal.id_nota == id_nota).first()
        if NotaFiscal is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota Fiscal não encontrada",
            )

        notafiscal_decode = notafiscal.__dict__
        return notafiscal_decode