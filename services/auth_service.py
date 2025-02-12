import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})

        secret_key = os.getenv("SECRET_KEY")
        algorithm = os.getenv("ALGORITHM")
        if not secret_key or not algorithm:
            logger.error("SECRET_KEY ou ALGORITHM não configurados corretamente.")
            raise ValueError("Configuração de segurança não encontrada.")

        logger.info("Iniciando a geração do token de acesso.")
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        logger.info("Token gerado com sucesso.")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Erro ao gerar o token: {e}")
        raise


def verify_user(username: str, password: str) -> Optional[dict]:
    logger.info(f"Verificando credenciais para o usuário: {username}")
    if username == "admin" and password == "admin":
        logger.info(f"Usuário {username} autenticado com sucesso.")
        return {"id": "123", "username": username}

    logger.warning(f"Tentativa de autenticação falhou para o usuário: {username}")
    return None
