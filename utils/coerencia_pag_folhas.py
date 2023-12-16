from fastapi import HTTPException, status
import logging

logging.basicConfig(level=logging.INFO)

class Validaçao_pag_folhas:

    @staticmethod
    def validar_coerencia_paginas_copias(paginas_por_folha, numero_copias):
        try: 
            limite_maximo = numero_copias * 2  

            resultado = paginas_por_folha * numero_copias

            if resultado > limite_maximo:
                raise ValueError("Coerência entre PAGINAS_POR_FOLHA e NUMERO_COPIAS inválida. Excede o limite máximo permitido.")
        except Exception as e:
            logging.error("Erro ao validar coerência entre PAGINAS_POR_FOLHA e NUMERO_COPIAS: " + str(e))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coerência entre PAGINAS_POR_FOLHA e NUMERO_COPIAS inválida. Excede o limite máximo permitido.",
            )
