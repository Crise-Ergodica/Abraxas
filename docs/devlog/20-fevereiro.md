# Dia 20/02 - 01º Dev Log de Abraxas

## O que fizemos

Estabelecemos a fundação arquitetural do Motor Lógico e da Base de Dados do projeto "Abraxas", garantindo um design estritamente *Data-Driven*. O sistema foi segregado em responsabilidades claras: regras e estado vivem no SQLite, processamento matemático ocorre no Python puro, e a interface visual é delegada ao Textual.

Entregas técnicas concluídas em código e schemas relacionais:

* **Fase 1: Fundação Genética (Atributos):** Modelagem das tabelas `characteristics` e `character_state`. Implementação da tabela `brp_formulas` que armazena a lógica matemática do BRP (ex: `(CON + SIZ) / 2` para HP) isolando a regra de negócio do código Python.
* **Fase 2: Motor de Perícias e Rolagens (d100):** Criação das tabelas `skills` e `character_skills`. Desenvolvimento do `SkillEngine` em Python para calcular totais dinâmicos e determinar os Níveis de Sucesso (Normal, Especial de 1/5 e Falha) do BRP.
* **Fase 3: Motor de Combate:** Estruturação das tabelas `weapons`, `armors` e `damage_bonus_rules`. O código foi desenhado para calcular o Bônus de Dano (STR+SIZ) via queries SQL simples sem lógicas condicionais hardcoded. Implementação do cálculo de mitigação de armadura no update de HP.
* **Fase 4: Integração TUI e Assincronismo:** Construção do esqueleto da Interface de Terminal usando o framework Textual. Aplicação de variáveis reativas (`reactive`) e uso do `asyncio` no Event Loop para permitir renderização de suspense mecânico tátil nas rolagens sem travar a Main Thread.
* **Auditoria de Sistema:** Implementação da tabela `roll_history` utilizando o padrão *Facade* no `SkillEngine` para persistir deterministicamente todos os resultados de ações processadas, garantindo a fonte da verdade no banco.

## O que está nos planos pra fazer (em ordem)

Seguindo os princípios de game design de motores de RPG e as regras do BRP, os próximos passos lógicos focarão em resolução de conflitos dinâmicos e progressão:

1. **Motor de Turnos e Ordem de Ação (Combat Round):** Traduzir as 4 fases do round de combate do BRP para tabelas de estado no banco (Declaração, Movimento, Ações e Resolução). Criar o *scheduler* em Python que ordena as ações estritamente com base na característica DEX e gerencia a alocação de "Ataque" e "Defesa (Parry/Dodge)" por rodada.
2. **Tabela de Resistência (Resistance Table) e Rolagens Opostas:** Expandir a Engine para processar conflitos diretos entre entidades (Ex: Esconder vs. Escutar) calculando níveis de sucesso cancelados (Special > Success > Failure). Implementar a fórmula matricial em Python `50 + (Ativo - Passivo) * 5` para resolver a Tabela de Resistência do BRP.
3. **Sistema de Experiência e Evolução:** Criar a rotina para atualizar a coluna `experience_check` no banco quando um jogador acertar uma perícia. Escrever o script de "Fim de Sessão" que realiza a rolagem de falha para tentar evoluir perícias marcadas em `1D6` pontos.

## O que falta fazer

Para que a fundação evolua para o produto de software final "Abraxas", os seguintes épicos arquiteturais ainda precisam ser iniciados:

* **Camada de Literatura Ergódica:** Estruturar as tabelas relacionais responsáveis por armazenar a "Árvore Narrativa" (Nós de texto, condições de atributos/itens para liberar opções de diálogo ou caminhos).
* **Sistema de Inventário e Carga:** Modelagem de itens consumíveis genéricos, controle de munição para armas de fogo, e cálculo ativo de limite de peso baseado na STR.
* **Matriz de Ferimentos Críticos:** Lógica matemática e UI para monitorar quando o personagem sofre um dano único igual ou maior que a metade (1/2) do seu HP, aplicando penalidades e mec mecânicas curativas (`First Aid` curando `1D3`).
* **Seed de Dados Inicial:** Povoamento completo das tabelas de SQLite com a lista massiva de perícias base (Listen 25%, Spot 25%, Brawl 25%, etc.) e equipamentos.
* **Motor de Extensibilidade e Homebrew:** Criação de sistemas e interfaces que facilitem a manipulação das regras. Inicialmente, ferramentas voltadas para quem contribui com o código-fonte; posteriormente, a criação de uma interface dedicada dentro do próprio executável para o jogador adicionar, editar ou subtrair regras (como alterar o número de atributos base, criar novas fórmulas, etc.), consolidando a flexibilidade absoluta do motor.
* **Pipeline de Build:** Configurar o *PyInstaller* via script no *Poetry* para compilar o banco SQLite embarcado, motor Python e dependências Textual em um binário único autossuficiente.