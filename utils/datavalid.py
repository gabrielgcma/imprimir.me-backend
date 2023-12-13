from fastapi import HTTPException, status
from datetime import timedelta, datetime
import logging

logging.basicConfig(level=logging.INFO)

class DataValid:

    @staticmethod
    def validate(data):
        try:
            data_nascimento = datetime.strptime(data, "%d%m%Y")
            hoje = datetime.now()
            idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

            if idade < 18:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="O usuário deve ter mais de 18 anos.",
                )

        except ValueError:
            logging.error(
                "Data inválida - utils/datavalid.py - validate() " + str(data)
            )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Data de nascimento inválida. Utilize o formato DDMMYYYY.",
            )