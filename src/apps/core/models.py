"""
Módulo de Definição de Modelos do Núcleo do RPG.

Este módulo define a estrutura de dados persistente para os personagens e
outras entidades do jogo. Ele integra-se diretamente com o motor de regras
(Game Engine) para calcular atributos derivados dinamicamente, garantindo
consistência entre os dados brutos (banco de dados) e as regras de negócio
(arquivos JSON).
"""

from django.db import models
from django.core.validators import MinValueValidator
from .game_instance import GAME_ENGINE


class Character(models.Model):
    """
    Representa um personagem jogável ou NPC dentro do sistema.

    Armazena apenas os atributos primários (base stats) e dados de identificação.
    Todos os atributos derivados (como Pontos de Vida, Bônus de Dano, etc.)
    são calculados em tempo de execução através de propriedades (@property)
    que consultam o motor de regras.

    Atributos:
        name (str): O nome do personagem.
        player_name (str): Nome do jogador dono do personagem (opcional).
        
        Atributos Primários (Characteristics):
        strength (int): Força física bruta.
        constitution (int): Saúde e resistência física.
        size (int): Massa corporal e altura.
        intelligence (int): Capacidade cognitiva e memória.
        power (int): Força de vontade e aptidão mágica.
        dexterity (int): Agilidade, coordenação e reflexos.
        appearance (int): Atratividade e carisma.
        education (int): Conhecimento formal acumulado.

        skills_experience (dict): Um campo JSON armazenando o progresso
            individual nas perícias. A chave é o ID da perícia (ex: 'skill_dodge')
            e o valor é a porcentagem ADICIONADA à base.
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Nome do Personagem",
        help_text="Nome pelo qual o personagem é conhecido."
    )

    player_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Nome do Jogador"
    )

    # --- Atributos Primários (Characteristics) ---
    # Valores padrão definidos como 10 (média humana no sistema BRP)
    
    strength = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        verbose_name="Força (STR)"
    )

    constitution = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        verbose_name="Constituição (CON)"
    )

    size = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        verbose_name="Tamanho (SIZ)"
    )

    intelligence = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        verbose_name="Inteligência (INT)"
    )

    power = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        verbose_name="Poder (POW)"
    )

    dexterity = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        verbose_name="Destreza (DEX)"
    )

    appearance = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        verbose_name="Aparência (APP)"
    )

    education = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        verbose_name="Educação (EDU)"
    )

    current_weapon_id = models.CharField(
        max_length=50,
        default="weapon_fist", # O padrão é estar desarmado (Soco)
        blank=True,
        verbose_name="ID da Arma Equipada",
        help_text="ID de referência do arquivo weapons.json (ex: weapon_sword)"
    )
    
    # --- Dados Flexíveis ---

    skills_experience = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Experiência em Perícias",
        help_text="Dicionário mapeando ID da perícia para pontos de bônus adquiridos."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Personagem"
        verbose_name_plural = "Personagens"
        ordering = ['name']

    def __str__(self) -> str:
        """Retorna a representação textual do personagem."""
        return self.name

    def get_context(self) -> dict:
        """
        Gera o dicionário de contexto necessário para o Motor de Regras.

        Este método empacota todos os atributos do modelo em um formato que
        o BRPGameEngine consegue ler (chaves em minúsculo, nomes completos).

        Returns:
            dict: Dicionário contendo strength, constitution, size, etc.
        """
        return {
            'strength': self.strength,
            'constitution': self.constitution,
            'size': self.size,
            'intelligence': self.intelligence,
            'power': self.power,
            'dexterity': self.dexterity,
            'appearance': self.appearance,
            'education': self.education,
            # Atributos derivados podem ser injetados aqui se necessário para
            # cálculos de segunda ordem, mas o básico é isso.
        }

    # --- Propriedades Derivadas (Calculadas pela Engine) ---

    @property
    def hit_points_max(self) -> int:
        """
        Calcula os Pontos de Vida (HP) totais usando a regra 'hp_total'.

        Returns:
            int: O valor máximo de HP (geralmente média de CON e SIZ).
        """
        return GAME_ENGINE.resolve('hp_total', self.get_context())

    @property
    def magic_points_max(self) -> int:
        """
        Calcula os Pontos de Magia (MP). No BRP padrão, é igual ao Poder.

        Returns:
            int: O valor máximo de MP.
        """
        # Se houver regra complexa no JSON, use ENGINE.resolve.
        # Caso contrário, retorno direto é mais performático.
        return self.power

    @property
    def damage_bonus(self) -> str:
        """
        Calcula o Bônus de Dano corpo a corpo usando a regra 'damage_bonus_calculation'.

        Returns:
            str: Uma string representando o dado extra (ex: '+1d4', '-1d6').
        """
        return GAME_ENGINE.resolve('damage_bonus_calculation', self.get_context())

    @property
    def movement_rate(self) -> int:
        """
        Calcula a taxa de movimento por rodada usando a regra 'movement_rate'.

        Returns:
            int: Metros por rodada (ex: 10 ou 12).
        """
        return GAME_ENGINE.resolve('movement_rate', self.get_context())

    @property
    def action_points(self) -> int:
        """
        Calcula o número de ações por turno usando a regra 'action_points'.

        Returns:
            int: Número de ações (geralmente 1 ou 2).
        """
        return GAME_ENGINE.resolve('action_points', self.get_context())

    @property
    def initiative_rank(self) -> int:
        """
        Calcula o Rank de Iniciativa (DEX Rank) usando a regra 'initiative_rating'.
        
        Returns:
            int: O valor usado para determinar a ordem de turno.
        """
        return GAME_ENGINE.resolve('initiative_rating', self.get_context())

    # --- Métodos de Perícia ---

    def get_skill_total(self, skill_id: str) -> int:
        """
        Calcula o valor final de uma perícia (Base + Experiência).

        O método consulta o Engine para obter a chance base (ex: Esquiva = DEX*2)
        e soma com os pontos de experiência armazenados no JSONField do modelo.

        Args:
            skill_id (str): O ID da perícia (ex: 'skill_dodge', 'skill_stealth').

        Returns:
            int: O valor percentual total da perícia.
        """
        # 1. Obter a base da Engine (fórmula do JSON)
        # O engine resolve a fórmula usando os atributos deste personagem
        base_value = GAME_ENGINE.resolve(skill_id, self.get_context())

        # Se a perícia não existir no JSON, base_value pode ser None ou string de erro
        if not isinstance(base_value, (int, float)):
            # Fallback seguro: se a regra não existe, assume base 0
            base_value = 0

        # 2. Obter o bônus comprado/evoluído (do banco de dados)
        bonus_value = self.skills_experience.get(skill_id, 0)

        return int(base_value + bonus_value)
    
    # --- Métodos de Equipamento e Combate ---
    
    def equip_weapon(self, weapon_id: str) -> bool:
        """
        Define a arma ativa do personagem após validar se ela existe no sistema.

        Args:
            weapon_id (str): O ID da arma conforme definido em weapons.json 
                             (ex: 'weapon_assault_rifle', 'weapon_dagger').

        Returns:
            bool: True se equipou com sucesso, False se o ID é inválido.
        """
        # 1. Validação de Segurança
        # Acessa o registro bruto da engine para ver se o item existe
        item_data = GAME_ENGINE.rules_registry.get(weapon_id)

        if not item_data:
            print(f"[ERRO] Tentativa de equipar item inexistente: {weapon_id}")
            return False
        
        # 2. Validação de Categoria (Opcional, mas recomendada)
        # Impede que o personagem equipe "skill_dodge" como arma
        valid_categories = ['melee', 'missile', 'firearm', 'energy']
        if item_data.get('category') not in valid_categories:
            print(f"[ERRO] ID '{weapon_id}' não é uma arma válida.")
            return False

        # 3. Persistência
        self.current_weapon_id = weapon_id
        self.save() # Salva no banco de dados imediatamente
        return True

    @property
    def current_weapon_data(self) -> dict:
        """
        Retorna o dicionário completo de dados da arma equipada (JSON).
        Útil para o Frontend exibir nome, dano e descrição.
        
        Returns:
            dict: Dados da arma ou dados do 'Soco' se nada for encontrado.
        """
        # Busca no Engine. Se não achar, fallback para Soco.
        weapon = GAME_ENGINE.rules_registry.get(self.current_weapon_id)
        
        if not weapon:
            # Fallback de segurança caso o ID no banco esteja corrompido
            return GAME_ENGINE.rules_registry.get('weapon_fist', {})
            
        return weapon

    def get_attack_damage_formula(self) -> str:
        """
        Gera a fórmula final de dano combinando a Arma + Bônus de Dano do Personagem.

        Returns:
            str: Fórmula matemática (ex: '1d6+1+1d4').
        """
        weapon = self.current_weapon_data
        base_damage = weapon.get('damage', '0')
        category = weapon.get('category', 'melee')

        # Regra BRP: Bônus de Dano (Força+Tam) só aplica em ataques Melee (Corpo a Corpo)
        # Armas de fogo e energia causam dano fixo.
        if category == 'melee':
            # self.damage_bonus vem da Property que criamos antes, calculada pela Engine
            bonus = self.damage_bonus 
            
            # Se o bônus não for "0", concatena.
            if bonus and bonus != "0" and bonus != 0:
                return f"{base_damage}{bonus}"
        
        return str(base_damage)