import os

import mysql.connector
from mysql.connector import Error

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
ENV_FILE = os.path.join(ROOT_DIR, ".env")

if load_dotenv is not None:
    load_dotenv(dotenv_path=ENV_FILE)


def _get_env_value(key: str, default: str) -> str:
    value = os.getenv(key, "").strip()
    return value or default


def get_db_connection():
    try:
        return mysql.connector.connect(
            host=_get_env_value("MYSQL_HOST", "localhost"),
            port=int(_get_env_value("MYSQL_PORT", "3306")),
            user=_get_env_value("MYSQL_USER", "biblioteca_user"),
            password=_get_env_value("MYSQL_PASSWORD", "secreto12345"),
            database=_get_env_value("MYSQL_DATABASE", "biblioteca"),
            consume_results=True,
        )
    except Error as exc:
        raise RuntimeError(f"No se pudo conectar a MySQL: {exc}") from exc
    except ValueError as exc:
        raise RuntimeError(f"El valor de MYSQL_PORT no es válido: {exc}") from exc
