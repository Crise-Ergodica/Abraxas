# Guia de Contribuição e Workflow

> "Código limpo é código que foi revisado."

## 1. O Git Flow do Grupo

Não invente moda. Siga estritamente este fluxo para evitar conflitos de merge.

### As Branches Sagradas

- `main`: **INTOCÁVEL**. É o código que funciona. Só recebe merge via Pull Request aprovado.
- `develop`: A branch onde integramos as funcionalidades. Todos os PRs devem apontar para cá.

### Nomenclatura de Branches

Sempre crie branches a partir da `develop`. Use o padrão:
`tipo/nome-da-tarefa`

- `feat/login-usuario` (Nova funcionalidade)
- `fix/botao-quebrado` (Correção de erro)
- `docs/atualiza-readme` (Documentação)
- `refactor/limpeza-css` (Melhoria de código sem mudar funcionalidade)

---

## 2. Mensagens de Commit (Conventional Commits)

Escreva commits que contem uma história. O padrão é:
`tipo: descrição curta no imperativo`

**Exemplos Aceitos:**

- `feat: adiciona model de Produto`
- `fix: corrige erro de CORS na API`
- `style: ajusta indentação no navbar`

**Exemplos PROIBIDOS:**

- `consertando`
- `finalizando`
- `testando`

---

## 3. O Ritual do Pull Request (PR)

Antes de abrir um PR no GitHub:

1. Garanta que seu código está rodando localmente.
2. Atualize sua branch com a `develop` (`git pull origin develop`) para resolver conflitos na sua máquina, não no GitHub.
3. Preencha a descrição do PR explicando **O QUE** foi feito e **COMO** testar.

**Regra de Ouro:** Nenhum PR é aprovado sem pelo menos 1 Review de outro colega.
