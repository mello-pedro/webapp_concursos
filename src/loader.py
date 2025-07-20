import pandas as pd

def load_reference(path: str) -> pd.DataFrame:
    """
    Carrega a planilha de referência que deve conter colunas: 'disciplina', 'topico'.
    """
    df = pd.read_excel(path)
    # Espera colunas: disciplina, topico
    return df