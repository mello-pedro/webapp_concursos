---- cria tabela de exrecicios

CREATE TABLE exercicio_sessoes (
    session_id TEXT PRIMARY KEY,
    date TEXT,
    discipline TEXT,
    topic TEXT,
    qtd_feitas INTEGER,
    qtd_certas INTEGER,
    qtd_erradas INTEGER,
    qtd_branco INTEGER
);

----