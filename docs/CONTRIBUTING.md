# Guia de Contribuicao e Workflow

> "Codigo limpo e codigo que foi revisado."

## 1. Termo de Responsabilidade e Escopo de Atuação

Para que o projeto flua sem gargalos, cada membro deve focar em dominar sua area de atuacao. Este termo garante que nao havera sobreposicao de tarefas nao planejadas e que cada integrante sabe exatamente o que precisa estudar e entregar.

### Infraestrutura e DBA (Gustavo, Gabriel e Rafael)
* **O que fazem:** Sao os guardioes dos dados. Responsaveis pela modelagem do banco relacional, orquestracao com Docker e criacao das classes no `models.py` do Django. 
* **O que devem dominar:** SQL, relacionamento de tabelas (PK/FK), funcionamento das migracoes do Django (`makemigrations` e `migrate`) e comandos basicos de Docker Compose.

### Backend Logic e API (Aurora)
* **O que faz:** E a ponte entre os dados e a interface. Responsavel pela logica de negocio, seguranca e por expor os dados criados pela Infra atraves de JSON (`views.py`, `serializers.py` e `urls.py`).
* **O que deve dominar:** Django REST Framework (DRF), verbos HTTP (GET, POST, PUT, DELETE), status codes e autenticacao de API.

### QA e Documentacao (Aurora e Kayke)
* **O que faz:** Garante que o software funcione como o esperado e que as decisoes da equipe estejam registradas. Cuida da documentacao automatica da API e da redacao tecnica.
* **O que deve dominar:** Testes automatizados (Pytest), padroes de documentacao (Swagger/Redoc) e formatacao de manuais (Markdown/LaTeX).

### Frontend: UI/UX e Integracao (Ana Clara e Gabriel)
* **O que fazem:** Constroem a interface visual e dao vida ao sistema conectando o HTML com a API do Backend.
* **O que devem dominar:** Estruturacao semantica (HTML5), estilizacao (CSS puro ou framework), manipulacao do DOM via JavaScript e assincronismo (`fetch`, `async/await`, `Promises`).

### Regra de Alteracao de Stack Tecnologica
A autonomia das frentes de trabalho e encorajada. Porem, se qualquer subgrupo decidir alterar a tecnologia de sua responsabilidade em comum acordo (exemplo: trocar Vanilla JS por Alpine.js, ou alterar o banco de dados), a seguinte regra se aplica:
1. A equipe de **QA e Documentacao** deve ser notificada imediatamente para que testes e documentacoes academicas sejam realinhados.
2. O restante do grupo deve ser avisado sobre o impacto.
3. Este documento (`CONTRIBUTING.md`) e o `README.md` principal **devem obrigatoriamente** ser atualizados refletindo a nova Stack no mesmo Pull Request que introduzir a mudanca.

---

## 2. O Git Flow do Grupo

Nao invente moda. Siga estritamente este fluxo para evitar conflitos de merge.

### As Branches Sagradas

* `main`: **INTOCAVEL**. E o codigo que funciona. So recebe merge via Pull Request aprovado.
* `develop`: A branch onde integramos as funcionalidades. Todos os PRs devem apontar para ca.

### Nomenclatura de Branches

Sempre crie branches a partir da `develop`. Use o padrao:
`tipo/nome-da-tarefa`

* `feat/login-usuario` (Nova funcionalidade)
* `fix/botao-quebrado` (Correcao de erro)
* `docs/atualiza-readme` (Documentacao)
* `refactor/limpeza-css` (Melhoria de codigo sem mudar funcionalidade)

---

## 3. Mensagens de Commit (Conventional Commits)

Escreva commits que contem uma historia. O padrao e:
`tipo: descricao curta no imperativo`

**Exemplos Aceitos:**

* `feat: adiciona model de Produto`
* `fix: corrige erro de CORS na API`
* `style: ajusta indentacao no navbar`

**Exemplos PROIBIDOS:**

* `consertando`
* `finalizando`
* `testando`

---

## 4. O Ritual do Pull Request (PR)

Antes de abrir um PR no GitHub:

1. Garanta que seu codigo esta rodando localmente sem erros.
2. Atualize sua branch com a `develop` (`git pull origin develop`) para resolver conflitos na sua maquina, nao no GitHub.
3. Preencha a descricao do PR explicando **O QUE** foi feito e **COMO** testar.

**Regra de Ouro:** Nenhum PR e aprovado sem pelo menos 1 Review de outro colega do grupo.