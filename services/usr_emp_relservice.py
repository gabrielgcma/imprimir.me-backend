from fastapi import HTTPException, status
from model.usuario_empresa_relacionamento import UsuarioEmpresa_Relacionamento as RelacionamentoModel
from services.empresaservice import EmpresaCrud
from services.usuarioservice import UsuarioCrud
from data.database import UsuarioEmpresa_Relacionamento
import logging

logging.basicConfig(level=logging.INFO)

class RelacionamentoCrud:
    def __init__(self, db_session):
        self.db_session = db_session

    def relacionar_empresa_usuario(self, relacionamento: RelacionamentoModel):
        relacionamento_decode = relacionamento.dict()
        
        if (EmpresaCrud.get_empresa(self, relacionamento_decode['id_empresa']) == None):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa não encontrada",
            )
        
        if (UsuarioCrud.get_usuario(self, relacionamento_decode['id_usuario']) == None):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )

        relacionamento_banco = UsuarioEmpresa_Relacionamento(**relacionamento_decode)

        try:
            self.db_session.add(relacionamento_banco)
            self.db_session.commit()
        except Exception as e:
            logging.error(
                "Erro ao registrar relacionamento - services/usr_emp_relservice.py - relacionar_empresa_usuario() " + "Empresa: " + str(relacionamento_decode.id_empresa) + "Usuario: " + str(relacionamento_decode.id_usuario) + str(e)
            )
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao cadastrar relacionamento no banco",
            )

        return RelacionamentoModel(**relacionamento_decode)