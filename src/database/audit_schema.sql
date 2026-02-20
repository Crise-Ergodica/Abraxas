-- -----------------------------------------------------------------------------
-- 11. AUDITORIA E HISTÓRICO (ROLL HISTORY) - ESTADO MUTÁVEL
-- Tabela de log apendável (append-only) para registrar todas as rolagens do BRP.
-- Garante a persistência do histórico do jogador, fundamental para narrativas
-- ramificadas e para a prevenção de adulteração de estado (save scumming).
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS roll_history (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    char_id TEXT NOT NULL,
    action_name TEXT NOT NULL,       -- Nome da perícia ou ação rolada (ex: 'SKL_DODGE')
    die_result INTEGER NOT NULL,     -- Resultado bruto gerado pelo d100 (1 a 100)
    
    -- Nível de sucesso alcançado, armazenado como String para facilitar a leitura 
    -- direta no banco de dados (ex: 'SUCCESS', 'SPECIAL_SUCCESS', 'FAILURE')
    success_level TEXT NOT NULL,     
    
    -- Carimbo de tempo inserido automaticamente pelo motor do SQLite
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
    
    FOREIGN KEY(char_id) REFERENCES character(id) ON DELETE CASCADE
);