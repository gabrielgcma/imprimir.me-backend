from fastapi import HTTPException, status
import logging

logging.basicConfig(level=logging.INFO)

class DecimalFormatter:

    @staticmethod
    def formatar_valor_decimal(valor):
        try:
            if '.' not in str(valor):
                valor = '{:.2f}'.format(float(valor))
            else:
                valor = str(valor)
            return valor
        except (ValueError, TypeError):
            logging.error(
                "Valor decimal inválido - utils/decimalformatter.py - formatar_valor_decimal() " + str(valor)
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Campo inválido: {valor}",
            )