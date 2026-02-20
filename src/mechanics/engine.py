"""
Módulo Central do Motor Abraxas (BRP Engine)
============================================

Este módulo atua como a camada de negócio (Engine Layer) da arquitetura
Orientada a Dados do sistema. Ele é responsável por processar as regras, 
fórmulas matemáticas e rolagens abstratas definidas no banco de dados relacional (SQLite),
garantindo que nenhuma regra de jogo seja 'hardcoded' no código fonte.

A classe `BRPEngine` consome o schema de dados e injeta dinamicamente o estado
atual do personagem nas expressões matemáticas extraídas da tabela `brp_formulas`,
calculando atributos derivados e atualizando o estado do jogador na persistência.

Dependências:
    - sqlite3: Para comunicação nativa com o banco de dados embarcado.
    - math: Para os arredondamentos mecânicos exigidos pelo sistema BRP.

Padrões aplicados:
    - Data-Driven Design
    - Single Responsibility Principle (SRP)
"""

import sqlite3
import math
from typing import Dict

class BRPEngine:
    """
    Motor Lógico para o sistema BRP acoplado estritamente ao SQLite.
    
    Gerencia a leitura de atributos, recuperação de fórmulas e o processamento 
    matemático do estado do personagem.

    Attributes:
        connection (sqlite3.Connection): Conexão ativa com o banco de dados SQLite.
    """
    
    def __init__(self, db_path: str = "abraxas.db") -> None:
        """
        Inicializa o motor conectando-se ao banco de dados.

        Args:
            db_path (str): O caminho para o arquivo do banco de dados SQLite. 
                           Padrão é "abraxas.db".
        """
        self.connection = sqlite3.connect(db_path)
        # Permite acessar colunas por nome ao invés de apenas por índice numérico
        self.connection.row_factory = sqlite3.Row 

    def _get_characteristics(self, char_id: str) -> Dict[str, int]:
        """
        Consulta as características base de um personagem específico no banco de dados.

        Args:
            char_id (str): O identificador único do personagem.

        Returns:
            Dict[str, int]: Dicionário com as siglas dos atributos em maiúsculas e seus valores.
                            Exemplo: {'STR': 13, 'CON': 14, 'SIZ': 12, 'INT': 17, ...}

        Raises:
            ValueError: Se o `char_id` não for encontrado na tabela `characteristics`.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM characteristics WHERE char_id = ?", (char_id,))
        row = cursor.fetchone()
        
        if not row:
            raise ValueError(f"Personagem {char_id} não encontrado nas características base.")
            
        # Converte a Row do SQLite para um dicionário, transformando as chaves em MAIÚSCULAS
        # Isso facilita o mapeamento (eval) com as fórmulas do banco (ex: 'CON', 'SIZ')
        return {key.upper(): value for key, value in dict(row).items() if key != "char_id"}

    def _get_formula(self, stat_name: str) -> str:
        """
        Consulta uma fórmula matemática abstrata armazenada no banco de dados.

        Args:
            stat_name (str): O nome da estatística derivada a ser consultada (ex: 'MAX_HP').

        Returns:
            str: A string contendo a fórmula matemática (ex: '(CON + SIZ) / 2').

        Raises:
            ValueError: Se a fórmula solicitada não existir na tabela `brp_formulas`.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT formula FROM brp_formulas WHERE stat_name = ?", (stat_name,))
        row = cursor.fetchone()
        
        if not row:
            raise ValueError(f"Fórmula para '{stat_name}' não definida no banco.")
        
        return row["formula"]

    def calculate_derived_stats(self, char_id: str) -> Dict[str, int]:
        """
        Processador de Regras: Injeta os valores das características nas fórmulas
        abstraídas pelo banco de dados para calcular os status derivados do personagem.

        Utiliza avaliação determinística via `eval` de forma segura, pois o contexto 
        está confinado às fórmulas do próprio sistema e aos atributos limpos do personagem.

        Args:
            char_id (str): O identificador único do personagem.

        Returns:
            Dict[str, int]: Um dicionário com os atributos derivados calculados e 
                            arredondados. Contém as chaves 'max_hp' e 'max_mp'.
        """
        chars = self._get_characteristics(char_id)
        
        hp_formula = self._get_formula("MAX_HP")
        mp_formula = self._get_formula("MAX_MP")
        
        # Avaliação das fórmulas com os atributos do personagem
        max_hp_raw = eval(hp_formula, {}, chars)
        max_mp_raw = eval(mp_formula, {}, chars)
        
        # O sistema BRP dita que frações no HP devem ser arredondadas para cima (math.ceil),
        # enquanto o MP baseia-se diretamente no valor inteiro da fórmula.
        return {
            "max_hp": math.ceil(max_hp_raw),
            "max_mp": int(max_mp_raw)
        }

    def initialize_character_state(self, char_id: str) -> None:
        """
        Calcula os atributos derivados e inicializa (ou atualiza) a tabela 
        dinâmica de estado (save) do personagem no banco de dados.

        A operação é idempotente: se o personagem já existir, a tabela sofrerá 
        apenas uma atualização (UPSERT) baseada nos valores de HP e MP calculados.

        Args:
            char_id (str): O identificador único do personagem.
        """
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
