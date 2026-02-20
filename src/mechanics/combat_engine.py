"""
Módulo de Resolução de Combate e Dano (Combat Engine)
=====================================================

Este módulo compõe a camada de regras bélicas do motor Abraxas.
Ele é responsável por agregar modificadores de atributos (Bônus de Dano),
resgatar o dano base das armas equipadas e calcular a mitigação física 
proporcionada pelas armaduras, atualizando o estado (HP) das entidades no banco.

Dependências:
    - sqlite3: Para consulta do equipamento ativo e tabelas de regras de combate.

Padrões aplicados:
    - Data-Driven Design (Delegação de regras condicionais para o SQL).
    - Separação de Preocupações (SoC - Não realiza rolagens, apenas fornece as fórmulas).
"""

import sqlite3

class CombatEngine:
    """
    Motor Lógico para resolução de Dano e Mitigação do BRP.
    
    Gerencia a leitura do equipamento ativo (loadout) do personagem, constrói 
    as strings de rolagem de dano (ex: '1D8+1+1D4') e aplica a subtração de 
    Pontos de Vida considerando a absorção de armaduras.

    Attributes:
        connection (sqlite3.Connection): Conexão ativa com o banco de dados SQLite.
    """
    
    def __init__(self, db_path: str = "abraxas.db") -> None:
        """
        Inicializa o motor de combate conectando-se ao banco de dados.

        Args:
            db_path (str): O caminho para o arquivo do banco de dados SQLite. 
                           Padrão é "abraxas.db".
        """
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

    def get_damage_bonus(self, char_id: str) -> str:
        """
        Calcula a soma de STR + SIZ e consulta a tabela de regras abstratas 
        (Lookup Table) para retornar a string do dado de bônus do personagem.

        Args:
            char_id (str): O identificador único do personagem.

        Returns:
            str: O modificador em formato de dado (ex: '-1D6', '+0', '+1D4').

        Raises:
            ValueError: Se o personagem não possuir atributos base cadastrados.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT str, siz FROM characteristics WHERE char_id = ?", (char_id,))
        stats = cursor.fetchone()
        
        if not stats:
            raise ValueError(f"Características não encontradas para o personagem '{char_id}'.")
            
        stat_sum = stats["str"] + stats["siz"]
        
        # O banco de dados resolve a condicional via operador BETWEEN
        cursor.execute(
            """
            SELECT dice_modifier FROM damage_bonus_rules 
            WHERE ? BETWEEN min_stat AND max_stat
            """, (stat_sum,)
        )
        rule = cursor.fetchone()
        
        return rule["dice_modifier"] if rule else "+0"

    def calculate_raw_damage(self, attacker_id: str) -> str:
        """
        Agrega o dano base da arma equipada com o Bônus de Dano do atacante.

        Caso o personagem não tenha uma arma equipada, a função assume o 
        comportamento padrão do BRP para ataques desarmados (Brawl = 1D3).

        Args:
            attacker_id (str): O identificador único do personagem atacante.

        Returns:
            str: A expressão concatenada pronta para o parser de dados (ex: '1D8+1+1D4').
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT w.base_damage, w.applies_damage_bonus
            FROM character_loadout cl
            JOIN weapons w ON cl.equipped_weapon_id = w.id
            WHERE cl.char_id = ?
            """, (attacker_id,)
        )
        weapon = cursor.fetchone()
        
        if not weapon:
            # Dano base de combate desarmado no BRP Quick-Start
            return "1D3"
            
        damage_expr = weapon["base_damage"]
        
        # Armas de fogo e certos projéteis não recebem o bônus de força
        if weapon["applies_damage_bonus"]:
            db_expr = self.get_damage_bonus(attacker_id)
            if db_expr != "+0":
                damage_expr += f"{db_expr}"
                
        return damage_expr

    def apply_damage(self, target_id: str, rolled_damage: int) -> int:
        """
        Aplica a mitigação da armadura (Armor Points) sobre o dano rolado 
        e persiste o novo valor de HP (Hit Points) do alvo no banco de dados.

        A função garante que a mitigação da armadura não recupere a vida do alvo 
        caso seja maior que o dano recebido (dano mínimo é 0).

        Args:
            target_id (str): O identificador único do personagem recebendo o ataque.
            rolled_damage (int): O valor numérico final gerado pelos dados de dano.

        Returns:
            int: O dano real sofrido após a absorção da armadura.
        """
        cursor = self.connection.cursor()
        
        # 1. Busca os Armor Points (AP) do alvo. COALESCE previne falhas se não houver armadura.
        cursor.execute(
            """
            SELECT COALESCE(a.armor_points, 0) as ap
            FROM character_loadout cl
            LEFT JOIN armors a ON cl.equipped_armor_id = a.id
            WHERE cl.char_id = ?
            """, (target_id,)
        )
        armor_row = cursor.fetchone()
        armor_points = armor_row["ap"] if armor_row else 0
        
        # 2. Subtrai a mitigação. A função max(0, X) impede dano negativo.
        actual_damage = max(0, rolled_damage - armor_points)
        
        if actual_damage > 0:
            # 3. Atualiza o estado persistente (Hit Points) no SQLite via transação segura
            with self.connection:
                self.connection.execute(
                    """
                    UPDATE character_state 
                    SET current_hp = current_hp - ? 
                    WHERE char_id = ?
                    """, (actual_damage, target_id)
                )
                
        return actual_damage

# Exemplo de fluxo arquitetural (View -> Engine -> Parser -> Engine -> View):
# engine = CombatEngine()
# dmg_expr = engine.calculate_raw_damage("001") 
# rolled_dmg = DiceRoller.parse_and_roll(dmg_expr) # Avalia '1D8+1+1D4', resulta em ex: 8
# dano_sofrido = engine.apply_damage("TARGET_02", rolled_dmg)