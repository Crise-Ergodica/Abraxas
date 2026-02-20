-- -----------------------------------------------------------------------------
-- 7. ARMADURAS - O "LIVRO DE REGRAS"
-- Catálogo estático de armaduras disponíveis no jogo.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS armors (
    id TEXT PRIMARY KEY,          -- Identificador da armadura (ex: ARM_HARD_LEATHER)
    name TEXT UNIQUE NOT NULL,    -- Nome de exibição na interface (TUI)
    armor_points INTEGER NOT NULL -- Pontos de armadura (Mitigação direta de dano físico)
);

-- -----------------------------------------------------------------------------
-- 8. ARMAS - O "LIVRO DE REGRAS"
-- Catálogo estático de armamento físico e à distância.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS weapons (
    id TEXT PRIMARY KEY,          -- Identificador da arma (ex: WPN_BROADSWORD)
    name TEXT UNIQUE NOT NULL,    -- Nome de exibição
    
    -- String no formato clássico de RPG (ex: '1D8', '1D6+1'). 
    -- Será parseada pelo motor Python durante o combate.
    base_damage TEXT NOT NULL,    
    
    -- Armas de fogo ou certos projéteis não somam a Força do usuário.
    applies_damage_bonus BOOLEAN NOT NULL DEFAULT 1 
);

-- -----------------------------------------------------------------------------
-- 9. REGRAS DE BÔNUS DE DANO (DAMAGE BONUS) - DATA-DRIVEN
-- Tabela de consulta (Lookup Table) para o modificador de dano corpo-a-corpo.
-- A regra BRP dita que o bônus é baseado na soma de STR (Força) + SIZ (Tamanho).
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS damage_bonus_rules (
    min_stat INTEGER NOT NULL,    -- Limite inferior da soma (STR + SIZ)
    max_stat INTEGER NOT NULL,    -- Limite superior da soma (STR + SIZ)
    
    -- Modificador em formato de dado que será concatenado ao dano da arma
    -- Exemplo: '-1D6', '+0', '+1D4'
    dice_modifier TEXT NOT NULL,  
    PRIMARY KEY (min_stat, max_stat)
);

-- -----------------------------------------------------------------------------
-- 10. EQUIPAMENTO ATIVO (LOADOUT) - ESTADO MUTÁVEL
-- O "Save" do que o personagem está empunhando e vestindo no momento.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS character_loadout (
    char_id TEXT PRIMARY KEY,
    equipped_weapon_id TEXT,      -- Pode ser NULL se estiver desarmado (Brawl)
    equipped_armor_id TEXT,       -- Pode ser NULL se estiver sem armadura
    
    FOREIGN KEY(char_id) REFERENCES character(id) ON DELETE CASCADE,
    FOREIGN KEY(equipped_weapon_id) REFERENCES weapons(id),
    FOREIGN KEY(equipped_armor_id) REFERENCES armors(id)
);

/*******************************************************************************
 * INSERTS DE INICIALIZAÇÃO (REGRAS E EQUIPAMENTOS)
 *******************************************************************************/

-- Tabela oficial de Bônus de Dano do BRP (STR + SIZ)
INSERT INTO damage_bonus_rules (min_stat, max_stat, dice_modifier) VALUES (2, 12, '-1D6');
INSERT INTO damage_bonus_rules (min_stat, max_stat, dice_modifier) VALUES (13, 16, '-1D4');
INSERT INTO damage_bonus_rules (min_stat, max_stat, dice_modifier) VALUES (17, 24, '+0');
INSERT INTO damage_bonus_rules (min_stat, max_stat, dice_modifier) VALUES (25, 32, '+1D4');
INSERT INTO damage_bonus_rules (min_stat, max_stat, dice_modifier) VALUES (33, 40, '+1D6');

-- Equipamentos Base (Catálogo Quick-Start)
INSERT INTO weapons (id, name, base_damage, applies_damage_bonus) VALUES ('WPN_BROADSWORD', 'Broadsword', '1D8+1', 1);
INSERT INTO armors (id, name, armor_points) VALUES ('ARM_HARD_LEATHER', 'Hard Leather', 2);

-- Equipando o personagem de teste (Taras - id '001')
INSERT INTO character_loadout (char_id, equipped_weapon_id, equipped_armor_id) 
VALUES ('001', 'WPN_BROADSWORD', 'ARM_HARD_LEATHER');