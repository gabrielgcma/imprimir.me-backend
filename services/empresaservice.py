from fastapi import HTTPException, status
from model.empresa import Empresa as EmpresaModel, EmpresaCreate
from data.database import Empresa
import logging

logging.basicConfig(level=logging.INFO)

class EmpresaCrud:
    def __init__(self, db_session):
        self.db_session = db_session

    def cadastrar_empresa(self, empresa: EmpresaCreate):
        empresa_decode = empresa.dict()
        empresa_banco = Empresa(**empresa_decode)
        
        try:
            self.db_session.add(empresa_banco)
            self.db_session.commit()
        except Exception as e:
            logging.error(
                "Erro ao registrar nova empersa no banco - controllers/main.py - cadastrar_empresa() " + str(empresa_decode) + str(e)
            )
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao cadastrar empresa no banco",
            )

        return EmpresaModel(**empresa_decode)

    def listar_empresas(self):
        empresas = self.db_session.query(Empresa).all()
        empresas_decode = []
        for empresa in empresas:
            empresa_decode = empresa.__dict__
            empresas_decode.append(empresa_decode)

        return empresas_decode

    def get_empresa(self, id_empresa: int):
        empresa = self.db_session.query(Empresa).filter(Empresa.id_empresa == id_empresa).first()
        if empresa is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa não encontrada",
            )

        empresa_decode = empresa.__dict__
        return empresa_decode

    def update_empresa(self, id_empresa: int, empresa_update: EmpresaCreate):
        try:
            empresa_banco = self.db_session.query(Empresa).filter(Empresa.id_empresa == id_empresa).first()
            if not empresa_banco:
                raise HTTPException(
                    status_code=404,
                    detail="Empresa não encontrada",
                )

            empresa_banco.username = empresa_update.username
            empresa_banco.password = empresa_update.password
            empresa_banco.email = empresa_update.email
            empresa_banco.cnpj = empresa_update.cnpj
            empresa_banco.is_company = empresa_update.is_company
            empresa_banco.razao_social = empresa_update.razao_social
            empresa_banco.nome_fantasia = empresa_update.nome_fantasia
            empresa_banco.chave_pix = empresa_update.chave_pix
            empresa_banco.pais = empresa_update.pais
            empresa_banco.estado = empresa_update.estado
            empresa_banco.cidade = empresa_update.cidade
            empresa_banco.bairro = empresa_update.bairro
            empresa_banco.rua = empresa_update.rua
            empresa_banco.numero = empresa_update.numero
            empresa_banco.complemento = empresa_update.complemento
            empresa_banco.cep = empresa_update.cep
            empresa_banco.longitude = empresa_update.longitude
            empresa_banco.latitude = empresa_update.latitude
            empresa_banco.color_print = empresa_update.color_print
            empresa_banco.black_print = empresa_update.black_print
            empresa_banco.color_value = empresa_update.color_value
            empresa_banco.black_value = empresa_update.black_value

            self.db_session.commit()

            return empresa_banco
    
        except Exception as e:
            logging.error(
                "Erro ao atualizar empresa no banco - controllers/main.py - update_empresa() " + str(empresa_update) + str(e)
            )
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar empresa no banco",
            )
