import customtkinter as ctk
import datetime

# Configuração inicial do tema do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


# ==============================================================================
# MOTOR LÓGICO: CLASSE PERSONAGEM
# ==============================================================================
class Personagem:
    # CORRIGIDO: __init__ com dois underlines
    def __init__(self, nome):
        self.nome = nome
        self.classe_atual = "Iniciante"
        self.pontos_fauna = 0
        self.pontos_flora = 0
        self.conhecimento_total = 0  # Equivalente ao BioScore
        self.historico_decisoes = []

    def verificar_evolucao(self):
        """Avalia os pontos atuais e evolui a classe se atingir os requisitos."""
        classe_anterior = self.classe_atual

        # Lógica de Evolução (Árvore de Classes)
        if self.pontos_fauna >= 15 and self.pontos_flora >= 15:
            self.classe_atual = "Guardião Biocêntrico"
        elif self.pontos_fauna >= 10:
            self.classe_atual = "Ranger do Cerrado"
        elif self.pontos_flora >= 10:
            self.classe_atual = "Mestre Botânico"

        return self.classe_atual != classe_anterior  # Retorna True se evoluiu

    def processar_acao(self, ganho_fauna, ganho_flora, id_escolha):
        """Recebe os pontos da escolha, atualiza atributos e salva o log."""
        self.pontos_fauna += ganho_fauna
        self.pontos_flora += ganho_flora
        impacto_rodada = ganho_fauna + ganho_flora
        self.conhecimento_total += impacto_rodada

        # Log da decisão para relatórios educacionais
        log = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "id_escolha": id_escolha,
            "impacto_ambiental": impacto_rodada,
        }
        self.historico_decisoes.append(log)

        # Verifica se essa ação causou evolução
        evoluiu = self.verificar_evolucao()
        return evoluiu


# ==============================================================================
# INTERFACE GRÁFICA: JANELA DO JOGO
# ==============================================================================
class JanelaJogo(ctk.CTk):
    # CORRIGIDO: __init__ com dois underlines
    def __init__(self):
        # CORRIGIDO: super().__init__() com dois underlines para inicializar o CTk
        super().__init__()

# --- CONFIGURAÇÃO DE FONTES GLOBAIS ---
        # Altere os números abaixo para o tamanho que achar melhor!
        self.fonte_titulo = ("Arial", 18, "bold")  # Aumentado de 14 para 18
        self.fonte_subtitulo = ("Arial", 13)  # Aumentado de 11 para 13
        self.fonte_narrativa = ("Arial", 16)  # Aumentado de 13 para 16
        self.fonte_botoes = ("Arial", 14, "bold")  # Adicionado para os botões
        
        # Instanciando nosso personagem real no jogo
        self.heroi = Personagem("Guardião Aprendiz")

        # Configurações da janela principal
        self.title("EcoNarrative - Guardiões de Cerrardente")
        self.geometry("600x750")
        self.resizable(False, False)

        # --- 1. PAINEL DE STATUS (CABEÇALHO) ---
        self.frame_status = ctk.CTkFrame(self, corner_radius=10)
        self.frame_status.pack(padx=20, pady=10, fill="x")

        # Nome do Jogador e Classe (Dinâmico)
        self.lbl_nome_classe = ctk.CTkLabel(
            self.frame_status,
            text=f"Jogador: {self.heroi.nome} | Classe: {self.heroi.classe_atual}",
            font=self.fonte_subtitulo,
        )
        self.lbl_nome_classe.grid(row=0, column=0, padx=15, pady=5, sticky="w")

        # Nível (Status Fixo por enquanto)
        self.lbl_nivel = ctk.CTkLabel(
            self.frame_status, text="Nível: 1", 
            font=self.fonte_subtitulo,
        )
        self.lbl_nivel.grid(row=0, column=1, padx=15, pady=5, sticky="e")

        # Texto da barra de BioScore
        self.lbl_bioscore = ctk.CTkLabel(
            self.frame_status,
            text=f"Conhecimento Ecológico (BioScore): {self.heroi.conhecimento_total}",
            font=self.fonte_subtitulo,
        )
        self.lbl_bioscore.grid(
            row=1, column=0, columnspan=2, padx=15, pady=(5, 0), sticky="w"
        )

        # Barra de progresso visual
        self.barra_progresso = ctk.CTkProgressBar(self.frame_status)
        self.barra_progresso.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=15,
            pady=(0, 10),
            sticky="we",  # Mantemos o sticky para esticar nas laterais
        )
        self.barra_progresso.set(0.0)  # Inicia vazia

        self.frame_status.grid_columnconfigure(0, weight=1)
        self.frame_status.grid_columnconfigure(1, weight=1)

        # --- 2. TELA DE NARRATIVA CENTRAL ---
        self.txt_narrativa = ctk.CTkTextbox(
            self, corner_radius=10, font=("Arial", 13), wrap="word"
        )
        self.txt_narrativa.pack(padx=20, pady=10, fill="both", expand=True)

        texto_inicial = (
            "Você acorda na transição entre a fumaça da cidade grande e a poeira vermelha do Cerrado. "
            "À sua frente, uma antiga praça urbana encontra uma clareira de árvores com troncos tortuosos e "
            "cascas grossas. Um morador local corre até você gritando que os frutos de um pequizeiro centenário "
            "estão sumindo misteriosamente durante a noite.\n\nO que você decide fazer?"
        )
        self.txt_narrativa.insert("0.0", texto_inicial)
        self.txt_narrativa.configure(state="disabled")

        # --- 3. CAIXA DE AÇÕES / ESCOLHAS ---
        self.frame_escolhas = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_escolhas.pack(padx=20, pady=15, fill="x")

        # Criando botões com dicionários de dados para facilitar a modularidade
        self.btn_escolha1 = ctk.CTkButton(
            self.frame_escolhas,
            text="Opção A: Investigar pegadas de animais ao redor do pequizeiro.",
            command=lambda: self.processar_escolha(
                id_esc="ESC_A",
                fauna=10,
                flora=0,
                texto="Você analisa o chão e encontra pegadas alongadas. Seu conhecimento "
                "indica que pertencem a um Lobo-Guará!\n\n[+10 Pontos de Fauna]",
            ),
        )
        self.btn_escolha1.pack(pady=5, fill="x")

        self.btn_escolha2 = ctk.CTkButton(
            self.frame_escolhas,
            text="Opção B: Coletar amostras do solo e folhas para análise botânica.",
            command=lambda: self.processar_escolha(
                id_esc="ESC_B",
                fauna=0,
                flora=10,
                texto="Você nota que o solo urbano compactado está sufocando as raízes do "
                "Pequizeiro. Você ensina a comunidade a descompactar a terra.\n\n[+10 Pontos de Flora]",
            ),
        )
        self.btn_escolha2.pack(pady=5, fill="x")

        self.btn_escolha3 = ctk.CTkButton(
            self.frame_escolhas,
            text="Opção C: Ignorar a natureza e procurar câmeras de segurança na rua.",
            command=lambda: self.processar_escolha(
                id_esc="ESC_C",
                fauna=0,
                flora=0,
                texto="Você foca nas câmeras e descobre moradores pegando pequis, mas "
                "perde a chance de interagir com o ecossistema.\n\n[Sem ganho de Conhecimento]",
            ),
        )
        self.btn_escolha3.pack(pady=5, fill="x")

    # --- FUNÇÃO DE LÓGICA E ATUALIZAÇÃO ---
    def processar_escolha(self, id_esc, fauna, flora, texto):
        """Processa a escolha no motor lógico e atualiza os elementos visuais na tela."""
        # 1. Envia os dados para a classe Personagem atualizar os atributos
        evoluiu = self.heroi.processar_acao(
            ganho_fauna=fauna, ganho_flora=flora, id_escolha=id_esc
        )

        # 2. Atualiza a Narrativa
        self.txt_narrativa.configure(state="normal")
        self.txt_narrativa.delete("0.0", "end")

        texto_final = texto
        if evoluiu:
            texto_final += f"\n\n🌟 EVOLUÇÃO! Sua classe mudou para {self.heroi.classe_atual}! 🌟"

        self.txt_narrativa.insert("0.0", texto_final)
        self.txt_narrativa.configure(state="disabled")

        # 3. Atualiza os Textos do Painel de Status
        self.lbl_nome_classe.configure(
            text=f"Jogador: {self.heroi.nome} | Classe: {self.heroi.classe_atual}"
        )
        self.lbl_bioscore.configure(
            text=f"Conhecimento Ecológico (BioScore): {self.heroi.conhecimento_total} | Fauna: {self.heroi.pontos_fauna} | Flora: {self.heroi.pontos_flora}"
        )

        # 4. Atualiza a Barra de Progresso (Simulando que 30 pontos = barra 100% cheia)
        progresso = min(self.heroi.conhecimento_total / 30.0, 1.0)
        self.barra_progresso.set(progresso)

        # 5. Desabilita os botões após a escolha para simular o fim da rodada
        self.btn_escolha1.configure(state="disabled")
        self.btn_escolha2.configure(state="disabled")
        self.btn_escolha3.configure(state="disabled")



# Execução do script
if __name__ == "__main__":
    app = JanelaJogo()
    app.mainloop()