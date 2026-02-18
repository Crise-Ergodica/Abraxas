import math
import random
import re
from typing import Any, Dict, List, Union, Optional

"""
rpg_engine.py

Motor de Regras (Rule Engine) para o sistema BRP (Basic Roleplaying).
Versão compatível com JSON v2.0 (Python Syntax).

Responsabilidades:
1. Carregar regras do JSON.
2. Interpretar rolagens de dados (ex: "1d6+2").
3. Executar fórmulas dinâmicas (ex: "math.ceil(hp / 2)").
4. Injetar contexto (Atributos + Tabelas) nas fórmulas.
"""

def roll_dice(dice_expression: Union[str, int, float]) -> int:
    """
    Processa uma expressão de dados (String) ou retorna o valor se já for número.
    
    Args:
        dice_expression: Pode ser "1d6", "2d10+5", "10" (str) ou 10 (int).
    
    Returns:
        int: O resultado da soma dos dados + modificadores.
    """
    # 1. Se já for número (ex: dano fixo ou resultado de cálculo anterior), retorna.
    if isinstance(dice_expression, (int, float)):
        return int(dice_expression)
        
    # 2. Se não for string válida, retorna 0 para não quebrar o cálculo.
    if not isinstance(dice_expression, str):
        return 0

    # 3. Limpeza: " 1D6 + 2 " -> "1d6+2"
    expr = dice_expression.lower().replace(" ", "")
    
    # 4. Regex para parsear "XdY+Z"
    # Grupos: (Qtd)d(Lados)(Sinal)(Modificador)
    match = re.match(r'(\d+)d(\d+)(?:([+-])(\d+))?', expr)
    
    if not match:
        # Tenta converter direto se for apenas string numérica "5"
        try:
            return int(expr)
        except ValueError:
            return 0 # Falha silenciosa (ex: string vazia)

    count = int(match.group(1))
    sides = int(match.group(2))
    mod_sign = match.group(3)
    mod_val = int(match.group(4)) if match.group(4) else 0

    # 5. Rola os dados
    total = sum(random.randint(1, sides) for _ in range(count))
    
    # 6. Aplica modificador
    if mod_sign == '-':
        total -= mod_val
    elif mod_sign == '+':
        total += mod_val
        
    return total


class BRPGameEngine:
    """
    Classe principal que orquestra a leitura e execução das regras.
    """

    def __init__(self, rules_json: List[Dict[str, Any]]):
        """
        Inicializa o motor mapeando IDs para objetos de regra.
        """
        self.rules_registry = {rule['id']: rule for rule in rules_json}

    def resolve(self, rule_id: str, context: Dict[str, Any]) -> Any:
        """
        Calcula uma regra baseada no ID e no Contexto fornecido.

        Args:
            rule_id (str): O ID da regra no JSON (ex: 'damage_bonus_calculation').
            context (dict): Dicionário com TODAS as variáveis necessárias.
                            Ex: {'strength': 18, 'size': 16, 'meters': 10, 'source': 'lava'}

        Returns:
            Any: Resultado do cálculo (int, float, str ou list).
        """
        rule = self.rules_registry.get(rule_id)
        if not rule:
            # Em produção, use logging.error
            print(f"ERRO: Regra '{rule_id}' não encontrada.")
            return None

        # Acesso direto à lógica
        logic = rule.get('logic')
        data_table = rule.get('data_table')

        # CASO 1: Regra sem fórmula (Apenas Lista ou Texto)
        # Ex: 'combat_actions' (lista de definições)
        if not logic or not logic.get('formula'):
            return data_table or rule.get('description')

        # CASO 2: Regra com Fórmula
        # Preparando o Sandbox (Ambiente Seguro)
        local_scope = {
            'math': math,            # Permite math.ceil, math.floor
            'roll': roll_dice,       # Permite roll('1d6')
            'data_table': data_table or {}, # Permite data_table.get()
            'max': max,              # Permite max(0, x)
            'min': min,
            'round': round
        }

        # Injeção de Variáveis (Dependency Injection)
        # Pega do context apenas o que a regra pede em input_variables
        missing_vars = []
        for var_name in logic.get('input_variables', []):
            val = context.get(var_name)
            
            if val is None:
                missing_vars.append(var_name)
                val = 0 # Valor default para evitar crash (NameError)
            
            local_scope[var_name] = val

        if missing_vars:
            print(f"Aviso: Variáveis {missing_vars} faltando para calcular '{rule_id}'. Usando 0.")

        # Execução da Fórmula (Eval Seguro)
        try:
            # __builtins__: None impede acesso a sistema de arquivos/rede
            result = eval(logic['formula'], {"__builtins__": None}, local_scope)
            return result
        except Exception as e:
            return f"Erro de Cálculo em '{rule_id}': {str(e)}"