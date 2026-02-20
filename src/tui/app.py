"""
Módulo de Interface Gráfica de Terminal (TUI)
=============================================

Este módulo compõe a camada de Apresentação (View) do sistema Abraxas,
construído sobre o framework assíncrono Textual.

A interface opera em um Event Loop contínuo, reagindo a interações do usuário
de forma não-bloqueante. A TUI é completamente burra em relação às regras de
negócio: ela apenas delega comandos para os motores lógicos (Engine Layer),
aguarda a resolução estocástica e o recálculo matemático, e então consome
a "verdade absoluta" gravada no banco de dados SQLite para se redesenhar.

Dependências:
    - asyncio: Para controle do Event Loop e pausas não-bloqueantes.
    - textual: Framework de renderização da interface no terminal.

Padrões aplicados:
    - Programação Orientada a Eventos (Event-Driven)
    - Reatividade de Estado (Data Binding)
    - Separação de Preocupações (SoC)
"""

import asyncio
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Button, Static, Label
from textual.reactive import reactive

# Importações dos motores lógicos (Assumindo que estão acessíveis no escopo)
# from src.mechanics.engine import BRPEngine
# from src.mechanics.dice_engine import SkillEngine
# from src.mechanics.combat_engine import CombatEngine


class CharacterStatsWidget(Static):
    """
    Widget reativo responsável por exibir o estado vital do personagem.

    Qualquer alteração nas variáveis `hp` ou `mp` disparará automaticamente
    um evento de re-renderização nativo do Textual, garantindo que a tela
    sempre reflita o estado atual da memória.

    Attributes:
        hp (int): Pontos de vida atuais do personagem (Hit Points).
        mp (int): Pontos de magia atuais do personagem (Magic Points).
    """

    hp = reactive(0)
    mp = reactive(0)

    def render(self) -> str:
        """
        Gera a string formatada que será desenhada no terminal.

        Returns:
            str: O texto contendo os status vitais formatados.
        """
        return f"Hit Points (HP): {self.hp} | Magic Points (MP): {self.mp}"


class AbraxasTUI(App):
    """
    Aplicação principal e orquestradora da Interface de Terminal.

    Gerencia o ciclo de vida da tela, a injeção de dependências dos motores
    do BRP e captura os eventos de teclado e mouse do jogador.

    Attributes:
        char_id (str): O identificador único do personagem ativo no banco de dados.
        CSS (str): Regras de estilização (TCSS) embutidas para o layout.
        BINDINGS (list): Mapeamento de atalhos de teclado globais da aplicação.
    """

    CSS = """
    Screen { align: center middle; }
    CharacterStatsWidget { padding: 1; background: $boost; text-align: center; }
    #log_panel { height: 1fr; border: solid green; padding: 1; margin-top: 1; }
    """

    BINDINGS = [("q", "quit", "Sair do Abraxas")]

    def __init__(self, char_id: str):
        """
        Inicializa a TUI e as instâncias dos motores acoplados ao SQLite.

        Args:
            char_id (str): O UUID ou identificador do personagem sendo jogado.
        """
        super().__init__()
        self.char_id = char_id
        # self.brp_engine = BRPEngine("abraxas.db")
        # self.skill_engine = SkillEngine("abraxas.db")
        # self.combat_engine = CombatEngine("abraxas.db")

    def compose(self) -> ComposeResult:
        """
        Monta a árvore de componentes (DOM estrutural) da interface.

        Yields:
            ComposeResult: Componentes Textual hierarquizados para renderização.
        """
        yield Header(show_clock=True)
        with Vertical():
            yield CharacterStatsWidget(id="stats")
            with Horizontal():
                yield Button("Rolar Dodge", id="roll_dodge", variant="primary")
                yield Button("Receber Dano", id="take_damage", variant="error")
            yield Label("Aguardando ação...", id="log_panel")
        yield Footer()

    def on_mount(self) -> None:
        """
        Hook de ciclo de vida engatilhado quando a tela é inserida no terminal.
        Garante que a UI carregue com o estado real persistido no banco de dados.
        """
        self.update_stats_from_db()

    def update_stats_from_db(self) -> None:
        """
        Sincroniza a View com a camada de persistência.
        Consulta o banco de dados via Motor Lógico e injeta os valores reais
        nos widgets reativos, forçando a atualização visual.
        """
        # Exemplo da chamada arquitetural real:
        # state = self.brp_engine.get_current_state(self.char_id)

        # Mock simulando o retorno do SQLite:
        mock_state = {"current_hp": 13, "current_mp": 14}

        stats_widget = self.query_one("#stats", CharacterStatsWidget)
        stats_widget.hp = mock_state["current_hp"]
        stats_widget.mp = mock_state["current_mp"]

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Manipulador de eventos assíncrono para interações de clique.

        Libera a Main Thread durante pausas estéticas (await asyncio.sleep)
        para construir suspense mecânico antes de delegar as rolagens e
        gravações ao Motor de Regras.

        Args:
            event (Button.Pressed): O evento de clique capturado pelo Textual.
        """
        log = self.query_one("#log_panel", Label)

        if event.button.id == "roll_dodge":
            # 1. Feedback visual imediato antes da rolagem
            log.update("> [Aguarde] Calculando chance e rolando D100...")

            # 2. Pausa dramática assíncrona (mantém a UI responsiva)
            await asyncio.sleep(0.8)

            # 3. Execução matemática via Engine
            # result_level, roll = self.skill_engine.roll_skill(self.char_id, "SKL_DODGE")

            # 4. Auditoria de Dados: Persiste o resultado da rolagem no log do SQLite
            # self.skill_engine.log_roll_audit(self.char_id, "SKL_DODGE", roll, result_level.name)

            # Mock temporário:
            roll = 42
            result_level = "SUCCESS"
            log.update(
                f"> Rolagem de Dodge: {roll} [{result_level}]\n> [Log de Auditoria gravado com sucesso]"
            )

        elif event.button.id == "take_damage":
            log.update("> [Alerta] O inimigo desferiu um golpe...")
            await asyncio.sleep(1.0)

            # Delegação do dano após a mitigação da armadura (Engine de Combate)
            damage_taken = 3
            # self.combat_engine.apply_damage(self.char_id, damage_taken)
            log.update(
                f"> O personagem sofreu {damage_taken} de dano físico após mitigação."
            )

            # Sincroniza a UI com a nova verdade absoluta do banco
            self.update_stats_from_db()


# if __name__ == "__main__":
#     app = AbraxasTUI(char_id="001")
#     app.run()
