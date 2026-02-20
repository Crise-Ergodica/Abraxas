<div align="center">
  <img src="docs/img/logo-readme.svg" alt="Abraxas Logo" width="100%">
</div>
<br>

<div align="center">

![Status](https://img.shields.io/badge/Status-Development-yellow)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Textual](https://img.shields.io/badge/TUI-Textual-17B890?logo=terminal&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Poetry](https://img.shields.io/badge/Manager-Poetry-60A5FA?logo=poetry&logoColor=white)

</div>

**Abraxas** é uma obra ergódica e um motor de RPG de mesa desenhado inteiramente para o terminal. Subvertendo as interfaces tradicionais de navegador, o sistema utiliza uma arquitetura TUI (*Terminal User Interface*) para entregar uma imersão mecânica e tátil.

Apoiado em um design *Data-Driven*, o núcleo do jogo processa regras, cálculos de atributos e rolagens através de um motor independente em Python, enquanto a persistência de estado é garantida por um banco de dados SQLite embarcado. O objetivo final é a compilação do projeto em um executável autossuficiente (via PyInstaller), dispensando qualquer configuração por parte do jogador final.

---

## Como Inicializar o Ambiente de Desenvolvimento

O gerenciamento de dependências e do ambiente virtual é feito inteiramente pelo **Poetry**.

1. **Instale as dependências:**
   O comando abaixo lerá o `pyproject.toml`, criará a pasta `.venv` na raiz do projeto e instalará o Textual e demais ferramentas isoladamente.
   ```bash
   poetry install
   ```

2. **Inicie a Interface:**
   Use o próprio Poetry para acionar o ponto de entrada da TUI, sem precisar ativar o ambiente virtual manualmente.
   ```bash
   poetry run python run.py
   ```

---

## Documentação Completa

Para manter este repositório limpo, todas as especificações técnicas, diagramas de arquitetura, guias do motor lógico (Engine) e manuais de contribuição foram movidos.

Mais informações detalhadas se encontram na **[Wiki do Abraxas](https://github.com/Crise-Ergodica/Abraxas/wiki/Wiki-Abraxas)**.
