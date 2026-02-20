/*******************************************************************************
 * SCHEMA DE BANCO DE DADOS - ABRAXAS (MOTOR BRP)
 * =============================================================================
 * Arquitetura: Data-Driven Relacional (SQLite)
 * Descrição: Define as entidades centrais do sistema de RPG, separando 
 * estritamente as Regras Universais (Fórmulas) do Estado (Saves).
 *******************************************************************************/

-- -----------------------------------------------------------------------------
-- 1. IDENTIDADE BASE
-- Tabela raiz de onde todas as outras informações do jogador derivam.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS character (
    id TEXT PRIMARY KEY,       -- Identificador único (Recomendado: UUID)
    name TEXT NOT NULL         -- Nome de exibição na interface (TUI)
);

-- -----------------------------------------------------------------------------
-- 2. CARACTERÍSTICAS (Basic Role-Playing)
-- As colunas utilizam as siglas oficiais do BRP em minúsculo para mapeamento
-- direto via eval() no motor Python.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS characteristics (
    char_id TEXT PRIMARY KEY,
    str INTEGER NOT NULL, -- Strength (Força Física)
    con INTEGER NOT NULL, -- Constitution (Saúde e Resistência)
    siz INTEGER NOT NULL, -- Size (Tamanho e Massa Corporal)
    int INTEGER NOT NULL, -- Intelligence (Capacidade de Raciocínio)
    pow INTEGER NOT NULL, -- Power (Força de Vontade e Magia)
    dex INTEGER NOT NULL, -- Dexterity (Agilidade e Reflexos)
    app INTEGER NOT NULL, -- Appearance (Aparência Física)
    
    -- Se o personagem for apagado, seus atributos são destruídos em cascata
    FOREIGN KEY(char_id) REFERENCES character(id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 3. O "LIVRO DE REGRAS" (Data-Driven)
-- Tabela estática. Nenhuma coluna aqui depende de um jogador específico.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS brp_formulas (
    stat_name TEXT PRIMARY KEY, -- Nome do atributo derivado (ex: MAX_HP)
    formula TEXT NOT NULL,      -- Expressão matemática em texto puro
    description TEXT            -- Explicação legível da regra para contribuintes
);

-- -----------------------------------------------------------------------------
-- 4. ESTADO MUTÁVEL (O "Save" do Jogador)
-- Tabela dinâmica atualizada constantemente pela TUI e rolagens de dano.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS character_state (
    char_id TEXT PRIMARY KEY,
    current_hp INTEGER NOT NULL, -- Pontos de Vida (Hit Points) atuais
    current_mp INTEGER NOT NULL, -- Pontos de Magia (Magic Points) atuais
    FOREIGN KEY(char_id) REFERENCES character(id) ON DELETE CASCADE
);

/*******************************************************************************
 * INSERTS DE INICIALIZAÇÃO (SEMENTES DO BRP)
 * Popula o banco com as regras fundamentais e dados de teste.
 *******************************************************************************/

-- Fórmulas do Quick-Start do BRP
INSERT INTO brp_formulas (stat_name, formula, description) 
VALUES ('MAX_HP', '(CON + SIZ) / 2', 'Hit Points máximos: Média de CON e SIZ');

INSERT INTO brp_formulas (stat_name, formula, description) 
VALUES ('MAX_MP', 'POW', 'Magic Points máximos: Igual ao valor de POW');

-- Personagem de Exemplo para Testes na Engine
INSERT INTO character (id, name) VALUES ('001', 'Taras');
INSERT INTO characteristics (char_id, str, con, siz, int, pow, dex, app) 
VALUES ('001', 13, 14, 12, 17, 14, 14, 15);
