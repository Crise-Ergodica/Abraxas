import sqlite3
import math
from typing import Dict, Any

class BRPEngine:
    """Motor Lógico para o sistema BRP acoplado estritamente ao SQLite."""
    
    def __init__(self, db_path: str = "abraxas.db") -> None:
        self.connection = sqlite3.connect(db_path)
        # Permite acessar colunas por nome
        self.connection.row_factory = sqlite3.Row 

    def _get_characteristics(self, char_id: str) -> Dict[str, int]:
        """Consulta as características base do personagem."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM characteristics WHERE char_id = ?", (char_id,))
        row = cursor.fetchone()
        
        if not row:
            raise ValueError(f"Personagem {char_id} não encontrado nas características base.")
            
        # Converte a Row do SQLite para um dicionário, transformando as chaves em MAIÚSCULAS
        # Isso facilita o mapeamento (eval) com as fórmulas do banco (ex: 'CON', 'SIZ')
        return {key.upper(): value for key, value in dict(row).items() if key != "char_id"}

    def _get_formula(self, stat_name: str) -> str:
        """Consulta uma fórmula matemática das regras do jogo injetadas no banco."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT formula FROM brp_formulas WHERE stat_name = ?", (stat_name,))
        row = cursor.fetchone()
        
        if not row:
            raise ValueError(f"Fórmula para {stat_name} não definida no banco.")
        return row["formula"]

    def calculate_derived_stats(self, char_id: str) -> Dict[str, int]:
        """
        Processador de Regras: Injeta os valores das características nas fórmulas
        abstraídas pelo banco de dados. Utiliza o método de avaliação determinística.
        """
        chars = self._get_characteristics(char_id)
        
        hp_formula = self._get_formula("MAX_HP")
        mp_formula = self._get_formula("MAX_MP")
        
        # O eval é seguro aqui pois as fórmulas são geradas pelo próprio sistema (banco embarcado)
        # e o dicionário `chars` contém apenas numéricos limpos mapeados.
        max_hp_raw = eval(hp_formula, {}, chars)
        max_mp_raw = eval(mp_formula, {}, chars)
        
        # BRP dita que frações no HP são arredondadas para cima
        return {
            "max_hp": math.ceil(max_hp_raw),
            "max_mp": int(max_mp_raw)
        }

    def initialize_character_state(self, char_id: str) -> None:
        """Calcula os atributos derivados e inicializa a tabela de estado do personagem."""
        derived = self.calculate_derived_stats(char_id)
        
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO character_state (char_id, current_hp, current_mp)
                VALUES (?, ?, ?)
                ON CONFLICT(char_id) DO UPDATE SET 
                    current_hp = excluded.current_hp,
                    current_mp = excluded.current_mp
                """,
                (char_id, derived["max_hp"], derived["max_mp"])
            )

# Uso pelo sistema (desacoplado da TUI):
# engine = BRPEngine()
# engine.initialize_character_state("001")
