from fastapi import HTTPException, status
from validate_cnpj import is_valid
import logging

logging.basicConfig(level=logging.INFO)

class CNPJFormatter:

    @staticmethod
    def formatar_cnpj(cnpj):
        cnpj = ''.join(filter(str.isdigit, cnpj))

        if is_valid(cnpj):
            return True
        else:
            logging.error(
                "CNPJ inválido - utils/cnpjformatter.py - formatar_cnpj() " + str(cnpj)
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNPJ inválido",
            )