# Guia de Desenvolvimento Backend (Django & DRF)

## 1. Arquitetura das Pastas (`src/apps`)

Nós separamos a lógica em duas grandes áreas para manter a organização:

### `src/apps/core/`
Aqui vivem as **Regras de Negócio e Dados**.
* `models.py`: Definição das tabelas do banco.
* `admin.py`: Configuração do painel administrativo.
* `services.py`: (Opcional) Lógica complexa que não cabe no Model.

### `src/apps/api/`
Aqui vive a **Camada de Exposição (HTTP)**.
* `serializers.py`: Transforma Models em JSON.
* `views.py`: Recebe a requisição, chama o `core`, e devolve a resposta.
* `urls.py`: Rotas da API (ex: `/api/v1/alunos/`).

---

## 2. Passo a Passo: Criando uma Nova Feature

Se você precisa criar um cadastro de "Bebidas", siga esta ordem:

1.  **Model (`core/models.py`):**
    Crie a classe `Bebida`. Rode `makemigrations` e `migrate`.

2.  **Serializer (`api/serializers.py`):**
    Crie o `BebidaSerializer`. Defina quais campos serão visíveis no JSON.

3.  **View (`api/views.py`):**
    Use `ModelViewSet` para ganhar o CRUD completo (Listar, Criar, Editar, Deletar) de graça.

4.  **Rota (`api/urls.py`):**
    Registre a View no router.

---

## 3. Padrões de Código Python

* Use **Type Hints** sempre que possível.
    ```python
    def calcular_preco(valor: float, taxa: float) -> float:
        return valor * taxa
    ```
* Mantenha as Views magras. Se tem muito `if/else`, mova para um `services.py` ou para o Model.