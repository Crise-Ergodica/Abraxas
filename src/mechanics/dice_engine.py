"""
Módulo de Resolução de Perícias e Rolagens (Dice Engine)
========================================================

Este módulo compõe a camada de regras dinâmicas do motor Abraxas.
Ele é responsável por calcular as chances de sucesso de perícias com base
nas fórmulas matemáticas abstraídas no banco de dados, além de gerenciar
as rolagens estocásticas (d100) características do sistema Basic Role-Playing (BRP).

Dependências:
    - sqlite3: Para consulta do catálogo de perícias e do save do jogador.
    - random: Para geração do número pseudoaleatório (o dado d100).
    - math: Para os arredondamentos mecânicos exigidos pelo sistema BRP.
    - enum: Para tipagem estrita dos níveis de sucesso.

Padrões aplicados:
    - Data-Driven Design
    - Separação de Preocupações (SoC - UI separada da lógica de dados)
"""

import sqlite3
import random
import math
from enum import Enum
from typing import Dict, Tuple


class SuccessLevel(Enum):
    """
    Enumeração que representa os níveis de sucesso do BRP Quick-Start.

    A interface de usuário (TUI) deve reagir a estes níveis para narrar
    o resultado da ação (ex: pintar de verde para SUCCESS, dourado para SPECIAL).
    """

    FAILURE = 0
    SUCCESS = 1
    SPECIAL_SUCCESS = 2


class SkillEngine:
    """
    Motor focado na resolução matemática de Perícias e Rolagens (d100) do BRP.

    Gerencia a leitura das fórmulas base (ex: 'DEX * 2'), a soma dos pontos
    alocados pelo jogador e a geração do resultado final perante o dado estocástico.

    Attributes:
        connection (sqlite3.Connection): Conexão ativa com o banco de dados SQLite.
    """

    def __init__(self, db_path: str = "abraxas.db") -> None:
        """
        Inicializa o motor de perícias conectando-se ao banco de dados.

        Args:
            db_path (str): O caminho para o arquivo do banco de dados SQLite.
                           Padrão é "abraxas.db".
        """
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

    def _get_characteristics(self, char_id: str) -> Dict[str, int]:
        """
        Consulta as características base do personagem para resolver fórmulas de perícias.

        Args:
            char_id (str): O identificador único do personagem.

        Returns:
            Dict[str, int]: Dicionário com as siglas dos atributos em maiúsculas e
                            seus valores (ex: {'DEX': 14, 'INT': 17}).

        Raises:
            ValueError: Se o `char_id` não for encontrado na tabela de características.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM characteristics WHERE char_id = ?", (char_id,))
        row = cursor.fetchone()

        if not row:
            raise ValueError(f"Personagem '{char_id}' não encontrado.")

        return {
            key.upper(): value for key, value in dict(row).items() if key != "char_id"
        }

    def get_skill_total(self, char_id: str, skill_id: str) -> int:
        """
        Calcula de forma determinística a chance percentual final de uma perícia.

        O cálculo obedece à regra BRP:
        Chance Final = (Fórmula Base Avaliada) + (Pontos Alocados pelo Jogador).

        Args:
            char_id (str): O identificador único do personagem.
            skill_id (str): O identificador único da perícia (ex: 'SKL_DODGE').

        Returns:
            int: O valor percentual final da perícia (o alvo para a rolagem de dados).

        Raises:
            ValueError: Se a perícia especificada não existir no catálogo do banco.
        """
        cursor = self.connection.cursor()
        # O LEFT JOIN garante que, mesmo que o jogador não tenha pontos alocados (NULL),
        # a perícia ainda possa ser rolada usando apenas sua base padrão (COALESCE para 0).
        cursor.execute(
            """
            SELECT s.base_formula, COALESCE(cs.allocated_points, 0) as allocated_points
            FROM skills s
            LEFT JOIN character_skills cs ON s.id = cs.skill_id AND cs.char_id = ?
            WHERE s.id = ?
            """,
            (char_id, skill_id),
        )
        row = cursor.fetchone()

        if not row:
            raise ValueError(f"Perícia '{skill_id}' não configurada no banco.")

        chars = self._get_characteristics(char_id)
        # Avalia se a base é fixa (ex: '25') ou dependente de status (ex: 'DEX * 2')
        base_val = int(eval(row["base_formula"], {}, chars))
        return base_val + row["allocated_points"]

    def _log_roll_audit(self, char_id: str, action_name: str, die_result: int, success_level: str) -> None:
        """
        Método privado. Persiste o resultado da rolagem no banco de dados.
        A TUI não faz ideia de que isso está acontecendo.
        """
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO roll_history (char_id, action_name, die_result, success_level)
                VALUES (?, ?, ?, ?)
                """,
                (char_id, action_name, die_result, success_level)
            )
    
    def roll_skill(self, char_id: str, skill_id: str) -> Tuple[SuccessLevel, int]:
        """
        Gera a rolagem estocástica (1d100) e a valida contra o rating total da perícia.

        A mecânica de Sucesso Especial do BRP Quick-Start define que resultados
        iguais ou inferiores a 20% (1/5) da chance total da perícia, arredondados
        para cima, geram um efeito ampliado.

        Args:
            char_id (str): O identificador único do personagem executando a ação.
            skill_id (str): O identificador único da perícia sendo rolada.

        Returns:
            Tuple[SuccessLevel, int]: Uma tupla contendo o grau de sucesso alcançado (Enum)
                                      e o resultado bruto gerado pelo dado (int, de 1 a 100).
        """
        total_skill = self.get_skill_total(char_id, skill_id)
        roll = random.randint(1, 100)
        
        special_chance = math.ceil(total_skill / 5.0)
        
        if roll <= special_chance:
            result = SuccessLevel.SPECIAL_SUCCESS
        elif roll <= total_skill:
            result = SuccessLevel.SUCCESS
        else:
            result = SuccessLevel.FAILURE
            
        # A MÁGICA AQUI: O motor grava no banco sozinho antes de devolver a resposta!
        self._log_roll_audit(char_id, skill_id, roll, result.name)
            
        return result, roll


# Exemplo de uso pelo sistema (desacoplado da TUI):
# engine = SkillEngine()
# level, die_result = engine.roll_skill("001", "SKL_DODGE")
# print(f"Resultado: {level.name} (Dado: {die_result})")
