from fastapi import HTTPException, status
from validate_docbr import CPF
import logging

logging.basicConfig(level=logging.INFO)

class CPFFormatter:

    @staticmethod
    def formatar_cpf(cpf):
        cpf = ''.join(filter(str.isdigit, cpf))

        if CPF().validate(cpf):
            return True
        else:
            logging.error(
                "CPF inválido - utils/cpfformatter.py - formatar_cpf() " + str(cpf)
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF inválido",
            )