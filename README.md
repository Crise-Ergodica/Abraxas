<div align="center">
  <img src="docs/img/logo-readme.svg" alt="Abraxas Logo" width="100%">
</div>
<br>

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)
![JavaScript](https://img.shields.io/badge/Frontend-Vanilla_JS-F7DF1E?logo=javascript&logoColor=black)
![Poetry](https://img.shields.io/badge/Gerenciador-Poetry-60A5FA?logo=poetry&logoColor=white)

> **Descrição:** Localizada na Praça Guilhermino de Oliveira, N 224 Santa Margarida MG, e tendo seu horário de funcionamento de Segunda a Sábado das 8:00 às 21:00 horas, oferece atendimento e entrega de uma ampla variedade de bebidas de alta qualidade, que abrange desde refrigerantes e sucos, até uma seleção de vinhos, cervejas artesanais, destilados e coquetéis prontos para desfrutar. O atendimento On-line funciona a partir do momento em que o cliente entra em contato pelos canais digitais da loja (Instagram ou WhatsApp) ou por chamada telefônica, e rapidamente a atendente irá separar seu pedido, caso não tenha algum item ela vai sugerir algo semelhante, pegar o endereço de entrega e em caso de pagamento por meio de Pix já receber o pagamento. Assim que o pedido for fechado o motoboy irá levar até a casa do cliente e em caso de pagamentos por meio de dinheiro ou cartão receber o pagamento. Já o atendimento presencial funciona de maneira simples o cliente escolhe entre receber a ajuda da atendente ou ele mesmo pegar o que deseja e se dirigir até o caixa para efetuar o pagamento. 

---

## Documentacao do Projeto

Para manter a padronizacao, leia os guias antes de iniciar o desenvolvimento:

- [Contribuição e Git](docs/CONTRIBUTING.md)
- [Backend (Django)](docs/BACKEND_GUIDE.md)
- [Frontend (JS)](docs/FRONTEND_GUIDE.md)

*Conforme o desenvolvimento avança, independente de sermos responsaveis ou não pela documentação final, é dever de cada integrante gerar documentos e comits organizados para o entendimento de todos do código em sua frente*

---

## 1. Composição do Time e Responsabilidades

A divisão do grupo segue uma arquitetura **Backend (API Provider)** e **Frontend (API Consumer)**.

| Integrante | Função Principal | Responsabilidades Chave | Stack Focada |
| :--- | :--- | :--- | :--- |
| **Gustavo**, **Gabriel**, **Rafael** | Infra e DBA | Configuração do Docker, CI/CD, Modelagem do Banco (SQL), Migrations. | Docker, PostgreSQL, SQL |
| **Aurora**, **Kayke** | QA e Docs | Testes Automatizados, Swagger/Redoc, Documentação Acadêmica (LaTeX/ABNT). | Pytest, Swagger, Markdown |
| **Aurora** | Backend Logic | Desenvolvimento das Views, Regras de Negócio e Segurança. | Django REST Framework (DRF) |
| **Aurora** | API Integration | Serializers, Endpoints, Autenticação (JWT/Session). | Python, DRF, JSON |
| **Ana Clara**, **Gabriel** | UI/UX Designer | Estrutura HTML Semântica, CSS (Tailwind/Bootstrap), Acessibilidade. | HTML5, CSS3, Figma |
| **Ana Clara** | Frontend Dev | Consumo de API (Fetch/Axios), Manipulação de DOM, Lógica JS. | JavaScript (ES6+), AJAX |

---

## 2. Arquitetura do Projeto

O projeto é um **Monorepo Modular**. O Backend serve apenas JSON; o Frontend consome esses dados e renderiza o HTML.

```text
Abraxas/
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

1. **Instale as dependências:**
    Isso criará automaticamente a pasta `.venv` na raiz.

    ```bash
    poetry install
    ```

2. **Ative o Ambiente Virtual:**

    **Windows:**

    ```bash
    .venv\Scripts\activate
    ```

     **Linux / Mac:**

    ```bash
    source .venv/bin/activate
    ```

3. **Variáveis de Ambiente:**

    ```bash
    cp .env.example .env
    ```

4. **Suba o Banco de Dados (Docker):**

    ```bash
    docker-compose up -d
    ```

5. **Execute o Projeto:**

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

1. **Crie sua branch:**

    ```bash
    git checkout develop
    git pull origin develop
    git checkout -b feature/minha-nova-funcionalidade
    ```

2. **Trabalhe e Commite:**

    - Use [Conventional Commits](https://www.conventionalcommits.org/):
        - `feat: adiciona model de alunos`
        - `fix: corrige erro no login`
        - `docs: atualiza diagrama de classes`

    - **Abra um Pull Request (PR):**
        - No GitHub, solicite o merge da sua `feature` para a `develop`.
        - Solicite revisão de pelo menos 1 colega.

---

## 5. Documentação da API

A documentação dos endpoints é gerada automaticamente pelo Swagger.
Após rodar o servidor, acesse:

- **Swagger UI:** `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc:** `http://localhost:8000/api/schema/redoc/`
# Abraxas
# Abraxas
