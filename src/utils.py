# src/utils.py

import uuid
from datetime import datetime

def generate_uuid() -> str:
    """
    Gera um UUID4 em formato de string.
    """
    return str(uuid.uuid4())

def current_date(fmt: str = "%Y-%m-%d") -> str:
    """
    Retorna a data atual no formato especificado (padrão ISO YYYY-MM-DD).
    """
    return datetime.now().strftime(fmt)

def seconds_to_hms(seconds: int) -> str:
    """
    Converte um tempo em segundos para uma string HH:MM:SS.
    """
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def validate_selection(value: str, options: list[str], field_name: str) -> None:
    """
    Valida se `value` está dentro de `options`, senão lança ValueError.
    """
    if value not in options:
        raise ValueError(f"Valor inválido em '{field_name}': '{value}' não está nas opções válidas.")
