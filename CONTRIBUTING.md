<div align="center">
  
  <img src="docs/img/logo-contributing.svg" alt="Contributing Abraxas Logo" width="100%">

</div>

---

Agradecemos o seu interesse em contribuir com o **Abraxas**. Este documento estabelece os padrões arquiteturais, as diretrizes legais para a modificação do motor e como você pode ajudar a expandir o universo e as regras do sistema.

---

## 1. Licenciamento e Criação de Homebrew

O código-fonte do motor Abraxas é distribuído sob a **Licença MIT**. Isso garante liberdade máxima para a comunidade. 

Você tem permissão total para utilizar, copiar, modificar, distribuir e até comercializar suas próprias campanhas usando o nosso motor, sob a única condição de que o aviso de copyright original da Licença MIT seja incluído.

### Modificações Data-Driven (Conteúdo Customizado)

Devido à natureza *Data-Driven* do Abraxas, **não é necessário alterar o código Python para criar regras customizadas ou *Homebrews***. 

* Novas fórmulas de dano, custos de sanidade, itens, perícias e cálculos de atributos derivados devem ser adicionados ou modificados exclusivamente através dos arquivos **JSON** na camada de Dados (`src/database/` ou diretório correspondente).
* Modificações nas engrenagens matemáticas (como alterar a forma como os dados explodem ou como a rolagem base funciona) devem ser direcionadas ao núcleo do motor (`src/mechanics/engine.py`).

---

## 2. Padrões de Arquitetura e Escopo

Se você deseja contribuir diretamente com o código base do projeto, respeite os seguintes domínios de responsabilidade:

* **Infraestrutura:** Gerenciamento do banco de dados SQLite embarcado e orquestração do ambiente de compilação (Poetry e PyInstaller).
* **Motor Lógico (Engine):** Lógica matemática de processamento de regras, gerenciamento de estado e carregamento dos arquivos JSON.
* **TUI (Interface de Terminal):** Componentização visual utilizando o framework Textual. Toda a renderização interativa e estilização TCSS pertencem a esta camada.

---

## 3. Ajude na Documentação (A Wiki do Abraxas)

Como o Abraxas também é uma obra de literatura ergódica, a documentação é tão importante quanto o código. Nós encorajamos fortemente que a comunidade nos ajude a expandir, corrigir e traduzir os guias do sistema.

Se você gosta de escrever, revisar regras de RPG ou documentar arquitetura de software, sua contribuição é essencial na nossa Wiki oficial:

**[Acesse e contribua com a Wiki do Abraxas](https://github.com/Crise-Ergodica/Abraxas/wiki/Wiki-Abraxas)**

Você pode contribuir documentando:

* Tutoriais de como escrever um arquivo JSON válido para criar uma nova arma.
* Guias de uso da interface TUI.
* Explicações detalhadas sobre as fórmulas matemáticas do motor.

---

## 4. Padrões de Commits e Pull Requests

Quando for enviar código ou alterações nos arquivos JSON base, adotamos um processo simplificado, focado em clareza:

1. Faça um *Fork* deste repositório e crie uma *branch* para a sua alteração.
2. Certifique-se de que o projeto executa perfeitamente em ambiente local utilizando `poetry run python run.py`.
3. Utilize o padrão **Conventional Commits** para o seu histórico. O formato obrigatório é `tipo: descrição objetiva`.
   * **Exemplos permitidos:** `feat: adiciona barra de vida na TUI`, `fix: corrige falha no cálculo de armadura pesada`, `docs: atualiza guia de criação de itens na wiki`.
4. Abra um *Pull Request* (PR) contendo uma descrição clara do que foi resolvido e como a equipe deve testar a sua nova implementação.
