-- -----------------------------------------------------------------------------
-- 5. PERÍCIAS (SKILLS) - O "LIVRO DE REGRAS"
-- Catálogo universal e estático do sistema BRP. Define a base matemática 
-- de cada perícia antes de qualquer intervenção do jogador.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS skills (
    id TEXT PRIMARY KEY,          -- Identificador da perícia (ex: SKL_DODGE)
    name TEXT UNIQUE NOT NULL,    -- Nome de exibição na interface (ex: 'Dodge')
    
    -- A base_formula é interpretada pelo Python (eval). 
    -- Pode ser um número inteiro fixo ('25') ou uma expressão ('DEX * 2').
    base_formula TEXT NOT NULL 
);

-- -----------------------------------------------------------------------------
-- 6. PERÍCIAS DO PERSONAGEM - ESTADO MUTÁVEL
-- Tabela associativa (N:N) que mapeia o "Save" das perícias de um jogador.
-- A chance final de sucesso = (base_formula calculada) + allocated_points.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS character_skills (
    char_id TEXT NOT NULL,
    skill_id TEXT NOT NULL,
    
    -- Pontos percentuais investidos pelo jogador (criação ou evolução)
    allocated_points INTEGER DEFAULT 0, 
    
    -- Mecânica clássica do BRP: Marca se a perícia foi usada com sucesso 
    -- na sessão atual, garantindo uma rolagem de evolução no final do jogo.
    experience_check BOOLEAN DEFAULT 0, 
    
    PRIMARY KEY (char_id, skill_id),
    FOREIGN KEY(char_id) REFERENCES character(id) ON DELETE CASCADE,
    FOREIGN KEY(skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

/*******************************************************************************
 * INSERTS DE INICIALIZAÇÃO (CATÁLOGO DE PERÍCIAS)
 *******************************************************************************/

-- Injeção do catálogo base do BRP
INSERT INTO skills (id, name, base_formula) VALUES ('SKL_BRAWL', 'Brawl', '25');
INSERT INTO skills (id, name, base_formula) VALUES ('SKL_DODGE', 'Dodge', 'DEX * 2');
INSERT INTO skills (id, name, base_formula) VALUES ('SKL_APPRAISE', 'Appraise', '15');
INSERT INTO skills (id, name, base_formula) VALUES ('SKL_OWN_LANG', 'Language (Own)', 'INT * 5');

-- Injetando o estado inicial das perícias no personagem de exemplo (Taras - id '001')
INSERT INTO character_skills (char_id, skill_id, allocated_points) VALUES ('001', 'SKL_DODGE', 20);
INSERT INTO character_skills (char_id, skill_id, allocated_points) VALUES ('001', 'SKL_BRAWL', 10);
