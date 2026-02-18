"""
Módulo de Inicialização do Motor de Regras (Game Engine).

Este módulo é responsável por localizar, carregar e validar os arquivos de dados
(JSON) que contêm as regras do sistema e as definições de perícias. Ele atua
como um ponto de entrada único (Singleton) para a instância do motor de jogo,
garantindo que os arquivos sejam lidos apenas uma vez durante o ciclo de vida
da aplicação Django.

Arquivos esperados no diretório 'data/':
    - core_rules.json: Regras fundamentais (cálculos de dano, HP, etc).
    - skills.json: Lista base de perícias e suas fórmulas.

Este módulo segue as diretrizes da PEP 8 (Estilo) e PEP 257 (Docstrings).
"""

import json
import os
import sys
from typing import List, Dict, Any, Optional

# Tenta importar a classe do motor. O uso de import relativo (.) assume
# que este arquivo está no mesmo diretório que rpg_engine.py.
try:
    from .rpg_engine import BRPGameEngine
except ImportError:
    # Fallback para execução isolada fora do contexto do Django/Pacote
    from rpg_engine import BRPGameEngine


def _get_data_directory() -> str:
    """
    Determina o caminho absoluto para o diretório de dados json.

    Utiliza o caminho deste arquivo (__file__) como referência para evitar
    dependências de configurações globais do Django (settings.py), tornando
    o módulo mais portável e testável isoladamente.

    Returns:
        str: O caminho absoluto para a pasta 'data'.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'data')


def load_game_engine() -> Optional[BRPGameEngine]:
    """
    Carrega os arquivos de regras e instancia o motor de jogo.

    Esta função percorre a lista de arquivos JSON pré-definidos, realiza a
    leitura segura e funde (merge) todos os objetos em uma única lista de
    regras. Em seguida, inicializa a classe BRPGameEngine com esses dados.

    O processo inclui tratamento de erros para arquivos inexistentes ou
    JSONs mal formatados, garantindo que a aplicação não trave fatalmente
    durante a importação, embora registre os erros no console.

    Returns:
        Optional[BRPGameEngine]: Uma instância configurada do motor de regras
        ou None caso ocorra um erro crítico que impeça a criação.
    """
    data_dir = _get_data_directory()
    all_rules: List[Dict[str, Any]] = []
    
    # Lista de arquivos obrigatórios para o funcionamento do sistema
    files_to_load = ['core_rules.json', 'skills.json']
    
    print(f"[INFO] Iniciando carregamento do BRP Engine em: {data_dir}")

    for filename in files_to_load:
        filepath = os.path.join(data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"[ALERTA] Arquivo nao encontrado: {filepath}")
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as file_handle:
                data = json.load(file_handle)
                
                # Lógica para suportar diferentes estruturas de JSON
                # Caso 1: O arquivo é uma lista direta de objetos
                if isinstance(data, list):
                    all_rules.extend(data)
                    print(f"[SUCESSO] {filename}: Carregado com {len(data)} regras.")
                
                # Caso 2: O arquivo é um dicionário com uma chave 'skills'
                # (Compatibilidade com formatos antigos ou exportações externas)
                elif isinstance(data, dict) and 'skills' in data:
                    skills_list = data['skills']
                    if isinstance(skills_list, list):
                        all_rules.extend(skills_list)
                        print(f"[SUCESSO] {filename}: Carregado com {len(skills_list)} pericias.")
                    else:
                        print(f"[ERRO] {filename}: A chave 'skills' nao contem uma lista.")
                
                else:
                    print(f"[ERRO] {filename}: Formato JSON desconhecido ou invalido.")

        except json.JSONDecodeError as error:
            print(f"[ERRO CRITICO] Falha de sintaxe no JSON {filename}: {error}")
        except Exception as error:
            print(f"[ERRO CRITICO] Erro inesperado ao ler {filename}: {error}")

    if not all_rules:
        print("[ERRO FATAL] Nenhuma regra foi carregada. O motor nao pode ser iniciado.")
        return None

    return BRPGameEngine(all_rules)


# Instância Global do Motor (Singleton)
# Outros módulos do Django (views.py, models.py) devem importar esta variável.
# Exemplo de uso: from apps.core.game_instance import GAME_ENGINE
GAME_ENGINE = load_game_engine()