# Guia de Desenvolvimento Frontend (Vanilla JS)

Nossa filosofia: **Simplicidade**. Usamos HTML padrão e JavaScript moderno (ES Modules).

## 1. Onde colocar os arquivos?

* `src/templates/pages/`: Onde fica o HTML.
* `src/static/css/`: Onde fica o estilo.
* `src/static/js/`: Onde fica a lógica.

---

## 2. Organização do JavaScript

Para não virar espaguete, dividimos o JS em **Services** e **Controllers**.

### A. Services (`src/static/js/services/`)

Aqui ficam APENAS as chamadas para a API (fetch). Este código não sabe que o HTML existe.

**Exemplo (`bebidas.service.js`):**

```javascript
const API_URL = '/api/v1/bebidas/';

export async function getBebidas() {
    const response = await fetch(API_URL);
    return await response.json();
}
```

### B. Pages/Controllers (src/static/js/pages/)

Aqui fica o codigo que manipula o DOM (tela). Ele importa o service e atualiza o HTML.

**Exemplo (cardapio.js):**

```javascript
import { getBebidas } from '../services/bebidas.service.js';

document.addEventListener('DOMContentLoaded', async () => {
    const lista = document.getElementById('lista-bebidas');
    
    try {
        const dados = await getBebidas();
        dados.forEach(bebida => {
            const item = document.createElement('li');
            item.textContent = `${bebida.nome} - R$ ${bebida.preco}`;
            lista.appendChild(item);
        });
    } catch (error) {
        console.error(error);
    }
});
```

---

## 3. Como conectar no HTML

No seu arquivo HTML, importe o script como modulo:

```html
<script type="module" src="/static/js/pages/cardapio.js"></script>
```
