<div align="center">
  <img src="docs/img/logo-readme.svg" alt="Barão das Bebidas Logo" width="100%">
</div>
<br>

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)
![JavaScript](https://img.shields.io/badge/Frontend-Vanilla_JS-F7DF1E?logo=javascript&logoColor=black)
![Poetry](https://img.shields.io/badge/Gerenciador-Poetry-60A5FA?logo=poetry&logoColor=white)

> **Descrição:** Breve resumo do propósito do TCC/Projeto de Extensão. Qual problema ele resolve? Quem é o público-alvo? (Ex: Sistema de gestão acadêmica focado em acessibilidade...).

---

## 1. Composição do Time e Responsabilidades

A divisão do grupo segue uma arquitetura **Backend (API Provider)** e **Frontend (API Consumer)**.

| Integrante | Função Principal | Responsabilidades Chave | Stack Focada |
| :--- | :--- | :--- | :--- |
| **...** | Infra e DBA | Configuração do Docker, CI/CD, Modelagem do Banco (SQL), Migrations. | Docker, PostgreSQL, SQL |
| **Aurora** | QA e Docs | Testes Automatizados, Swagger/Redoc, Documentação Acadêmica (LaTeX/ABNT). | Pytest, Swagger, Markdown |
| **Aurora** | Backend Logic | Desenvolvimento das Views, Regras de Negócio e Segurança. | Django REST Framework (DRF) |
| **Aurora** | API Integration | Serializers, Endpoints, Autenticação (JWT/Session). | Python, DRF, JSON |
| **Ana Clara** | UI/UX Designer | Estrutura HTML Semântica, CSS (Tailwind/Bootstrap), Acessibilidade. | HTML5, CSS3, Figma |
| **Ana Clara** | Frontend Dev | Consumo de API (Fetch/Axios), Manipulação de DOM, Lógica JS. | JavaScript (ES6+), AJAX |

---

## 2. Arquitetura do Projeto

O projeto é um **Monorepo Modular**. O Backend serve apenas JSON; o Frontend consome esses dados e renderiza o HTML.

```text
nome-do-projeto/
├── .github/workflows/    # Automação (CI/CD)
├── docs/                 # Documentação do TCC (Diagramas, PDFs)
├── src/                  # CÓDIGO FONTE
│   ├── config/           # Configurações do Django (settings, urls base)
│   ├── apps/             # Aplicações Django (Onde vive a API)
│   │   ├── core/         # Models e Utils
│   │   └── api/          # Serializers e Views (DRF)
│   ├── static/           # ASSETS FRONTEND
│   │   ├── css/          # Estilos
│   │   └── js/           # Lógica do Cliente
│   │       ├── services/ # Abstração das chamadas API (fetch)
│   │       └── pages/    # Scripts específicos de cada tela
│   └── templates/        # HTML Puro (Esqueleto da página)
├── tests/                # Testes Automatizados
├── docker-compose.yml    # Orquestração de Containers (Banco + App)
├── pyproject.toml        # Dependências (Poetry)
└── README.md             # Você está aqui
```

---

## 3. Como Rodar o Projeto (Setup)

### Passo a Passo

1.  **Instale as dependências:**
    Isso criará automaticamente a pasta `.venv` na raiz.
    ```bash
    poetry install
    ```

2.  **Ative o Ambiente Virtual:**
    **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
     **Linux / Mac:**
        ```bash
        source .venv/bin/activate
        ```

3.  **Variáveis de Ambiente:**
    ```bash
    cp .env.example .env
    ```

4.  **Suba o Banco de Dados (Docker):**
    ```bash
    docker-compose up -d
    ```

5.  **Execute o Projeto:**
    Com a venv ativa, use os comandos normais do Django:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```
    > O servidor estará rodando em: `http://127.0.0.1:8000/`

---

## 4. Workflow de Desenvolvimento (Git Flow)

Para evitar conflitos, seguimos estritamente este fluxo. **NUNCA faça commit direto na main ou develop.**

### As Branches
- **main**: Código de produção (estável). Apenas Tech Lead aprova o merge.
- **develop**: Branch de integração. Todo PR deve apontar para cá.
- **feature/nome-da-feature**: Branch de trabalho individual.

### Ciclo de Vida de uma Tarefa

1.  **Crie sua branch:**
    ```bash
    git checkout develop
    git pull origin develop
    git checkout -b feature/minha-nova-funcionalidade
    ```

2.  **Trabalhe e Commite:**
* Use [Conventional Commits](https://www.conventionalcommits.org/):
    - `feat: adiciona model de alunos`
    - `fix: corrige erro no login`
    - `docs: atualiza diagrama de classes`

3.  **Abra um Pull Request (PR):**
    - No GitHub, solicite o merge da sua `feature` para a `develop`.
    - Solicite revisão de pelo menos 1 colega.

---

## 5. Documentação da API

A documentação dos endpoints é gerada automaticamente pelo Swagger.
Após rodar o servidor, acesse:

* **Swagger UI:** `http://localhost:8000/api/schema/swagger-ui/`
* **ReDoc:** `http://localhost:8000/api/schema/redoc/`
