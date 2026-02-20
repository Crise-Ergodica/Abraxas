-- Identidade base da Entidade
CREATE TABLE IF NOT EXISTS character (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

-- Características Base do BRP
CREATE TABLE IF NOT EXISTS characteristics (
    char_id TEXT PRIMARY KEY,
    str INTEGER NOT NULL,
    con INTEGER NOT NULL,
    siz INTEGER NOT NULL,
    int INTEGER NOT NULL,
    pow INTEGER NOT NULL,
    dex INTEGER NOT NULL,
    app INTEGER NOT NULL,
    FOREIGN KEY(char_id) REFERENCES character(id) ON DELETE CASCADE
);

-- Tabela Data-Driven para Fórmulas do Sistema
CREATE TABLE IF NOT EXISTS brp_formulas (
    stat_name TEXT PRIMARY KEY,
    formula TEXT NOT NULL,
    description TEXT
);

-- Estado Mutável (O "Save" Dinâmico)
CREATE TABLE IF NOT EXISTS character_state (
    char_id TEXT PRIMARY KEY,
    current_hp INTEGER NOT NULL,
    current_mp INTEGER NOT NULL,
    FOREIGN KEY(char_id) REFERENCES character(id) ON DELETE CASCADE
);

-- INSERTS INICIAIS (A semente do BRP)
INSERT INTO brp_formulas (stat_name, formula, description) 
VALUES ('MAX_HP', '(CON + SIZ) / 2', 'BRP Quick-Start HP formula');

INSERT INTO brp_formulas (stat_name, formula, description) 
VALUES ('MAX_MP', 'POW', 'Power points equals POW');

-- Personagem de Exemplo (Taras)
INSERT INTO character (id, name) VALUES ('001', 'Taras');
INSERT INTO characteristics (char_id, str, con, siz, int, pow, dex, app) 
VALUES ('001', 13, 14, 12, 17, 14, 14, 15);
