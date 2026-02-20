<div align=center>
  
````text
   ░███    ░████████   ░█████████     ░███    ░██    ░██    ░███      ░██████   
  ░██░██   ░██    ░██  ░██     ░██   ░██░██    ░██  ░██    ░██░██    ░██   ░██  
 ░██  ░██  ░██    ░██  ░██     ░██  ░██  ░██    ░██░██    ░██  ░██  ░██         
░█████████ ░████████   ░█████████  ░█████████    ░███    ░█████████  ░████████  
░██    ░██ ░██     ░██ ░██   ░██   ░██    ░██   ░██░██   ░██    ░██         ░██ 
░██    ░██ ░██     ░██ ░██    ░██  ░██    ░██  ░██  ░██  ░██    ░██  ░██   ░██  
░██    ░██ ░█████████  ░██     ░██ ░██    ░██ ░██    ░██ ░██    ░██   ░██████   
````                                                                        
<br>

![Status](https://img.shields.io/badge/Status-Development-yellow)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)
![BRP](https://img.shields.io/badge/System-Basic_Roleplaying-red)
![JSON](https://img.shields.io/badge/Architecture-Data_Driven-orange)
![Poetry](https://img.shields.io/badge/Manager-Poetry-60A5FA?logo=poetry&logoColor=white)

</div>

**Description:** Abraxas é uma plataforma de gerenciamento de jogos de interpretação de papéis (RPG) baseada no sistema Basic Roleplaying (BRP). Distinguindo-se por uma arquitetura Orientada a Dados (*Data-Driven*), o sistema desacopla as regras de negócio do código-fonte. Regras, fórmulas de dano, custos de perícia e especificações de itens são definidos em arquivos JSON externos. Esta arquitetura permite que o sistema calcule atributos derivados, como Pontos de Vida e Bônus de Dano, dinamicamente em tempo de execução. Esta abordagem facilita a implementação de regras customizadas ou a adaptação para cenários distintos (Fantasia, Ficção Científica, Horror) sem a necessidade de refatoração da lógica do Backend.

---

## Project Documentation

Para garantir a padronização e a compreensão da arquitetura do motor, consulte os seguintes guias:

- [Engine Guide](docs/ENGINE_GUIDE.md)
- [JSON Rules Schema](docs/JSON_SCHEMA.md)
- [Frontend and API Consumption](docs/FRONTEND_GUIDE.md)

---

## 1. System Architecture

O projeto segue o padrão *Interpreter*. Um componente central, designado como "Motor" (`rpg_engine.py`), interpreta definições ("Regras JSON") e aplica um contexto ("Personagem do Banco de Dados") para gerar resultados.



### Data Flow

1.  **Data Layer (`data/*.json`):** Define a mecânica operacional (ex: fórmulas de cálculo de HP).
2.  **Engine Layer (`rpg_engine.py`):** Processa fórmulas matemáticas e rolagens de dados.
3.  **Instance Layer (`game_instance.py`):** Singleton responsável por carregar os arquivos JSON na memória durante a inicialização da aplicação.
4.  **Model Layer (`models.py`):** O modelo de Personagem persiste apenas atributos base. Atributos derivados são computados via propriedades calculadas instantaneamente pelo Motor.

---

## 2. Directory Structure

O projeto é modular, separando a lógica do framework (Django) da lógica do jogo (Engine).

```text
abraxas/
├── abraxas.spec             # Configurações de compilação do PyInstaller
├── requirements.txt         # Bibliotecas necessárias (textual, etc.)
├── README.md                # A vitrine do portfólio (explicação da obra e do código)
├── run.py                   # O ponto de ignição do executável
└── src/
    ├── __init__.py
    ├── database/
    │   ├── __init__.py
    │   ├── connection.py    # Gerencia a conexão com o SQLite
    │   └── queries.py       # Funções que buscam e salvam o estado do leitor/jogador
    ├── mechanics/           # O motor invisível do sistema
    │   ├── __init__.py
    │   ├── engine.py        # Lógica oculta, testes, cálculos e caminhos do labirinto
    │   └── state.py         # Gerencia em qual ponto da travessia o usuário está
    ├── tui/                 # A casca interativa (Textual)
    │   ├── __init__.py
    │   ├── app.py           # Classe principal (herda de textual.app.App)
    │   ├── screens/         # Telas distintas (Ex: Menu, Ficha, Narrativa)
    │   ├── widgets/         # Seus componentes customizados
    │   └── styles/
    │       └── abraxas.tcss # O arquivo de design CSS do Textual
    └── assets/              # Arquivos estáticos empacotados pelo PyInstaller
        ├── init_db.sqlite   # Banco de dados inicial embutido (se necessário)
        └── ascii_art.txt    # Elementos visuais em texto
```

---

## 3. Setup and Execution

### Prerequisites
- Python 3.11 ou superior
- Poetry

### Step-by-Step

1.  **Instalar dependências:**
    ```bash
    poetry install
    ```

2.  **Ativar Ambiente Virtual:**
    ```bash
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Verificar Arquivos de Regra:**
    Certifique-se de que o diretório `src/apps/core/data/` contém os arquivos `core_rules.json` e `skills.json`. O sistema não inicializará sem estes arquivos.

4.  **Executar Servidor:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```
    O carregador do Motor exibirá logs no terminal indicando a quantidade de regras e perícias carregadas.

---

## 4. Development Workflow

O fluxo de trabalho foca na integridade das regras:

1.  **Rule Modification:** Para modificar o dano de armas ou cálculos de HP, edite os arquivos **JSON** em `apps/core/data/`. A modificação do código Python não é necessária para alterações de regras.
2.  **Logic Modification:** Para implementar novas funções matemáticas ou novas mecânicas centrais, edite o `rpg_engine.py`.

### Git Flow
- **main:** Versão de produção estável.
- **develop:** Branch de integração.
- **feature/mechanic-name:** Branches de trabalho.

---

## 5. API Documentation (Swagger)

A API REST expõe os dados calculados dos personagens.
Após iniciar o servidor, acesse:

- **Swagger UI:** `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc:** `http://localhost:8000/api/schema/redoc/`

---

### Usage Example (Django Shell)

```python
from apps.core.models import Character

# O sistema calcula atributos derivados automaticamente:
conan = Character.objects.create(name="Conan", strength=18, size=16)

print(f"Max HP: {conan.hit_points_max}")  # Calculado via JSON
print(f"Damage Bonus: {conan.damage_bonus}") # Calculado via JSON

conan.equip_weapon('weapon_battle_axe')
print(f"Attack Damage: {conan.get_attack_damage_formula()}") # Exemplo de saída: "1d8+1+1d6"
```
