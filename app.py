import gradio as gr
import random

# Simulação do estado do jogo (em um cenário real, viria de um banco de dados ou classe)
status_jogador = {
    "nome": "EcoRanger",
    "classe": "Biomeomante",
    "densidade_natureza": 50,  # Escala de 0 a 100
    "pontuacao": 0,
    "turno": 1
}

# Banco de dados temporário de histórias (simulando o que a IA/Equipe geraria)
historias = [
    {
        "texto": "Turno 1: Você chega às bordas do Distrito de Vidro. As raízes de uma Sumaúma secular estão quebrando o asfalto e bloqueando os painéis solares públicos. Os guardas urbanos querem cortar as raízes.",
        "opcoes": [
            ("Usar fitorremediação e manejo para guiar as raízes sem cortá-las.", "natureza"),
            ("Hackear os painéis solares para mudá-los de lugar, ignorando a árvore.", "urbano"),
            ("Deixar que os guardas cortem a árvore para evitar apagões no bairro.", "destrutivo")
        ]
    },
    {
        "texto": "Turno 2: Um enxame de polinizadores cibernéticos está atacando os jardins verticais do centro tecnológico por causa de uma frequência de rádio errada.",
        "opcoes": [
            ("Reprogramar a frequência usando conhecimento biológico dos insetos.", "natureza"),
            ("Desligar os jardins verticais para os insetos irem embora.", "urbano"),
            ("Usar um pulso eletromagnético (EMP) para fritar o enxame.", "destrutivo")
        ]
    }
]

def processar_escolha(opcao_selecionada):
    if not opcao_selecionada:
        return atualizar_interface("Escolha uma opção para continuar.")
        
    # Lógica de pontuação baseada na densidade de conhecimento ecológico
    if opcao_selecionada == "natureza":
        status_jogador["densidade_natureza"] = min(100, status_jogador["densidade_natureza"] + 15)
        status_jogador["pontuacao"] += 20
        feedback = "🌱 Ótima escolha! Você aplicou conceitos ecológicos profundos."
    elif opcao_selecionada == "urbano":
        status_jogador["pontuacao"] += 10
        feedback = "🏢 Escolha funcional urbana, mas neutra para o meio ambiente."
    else:
        status_jogador["densidade_natureza"] = max(0, status_jogador["densidade_natureza"] - 20)
        feedback = "⚠️ Essa ação degradou a harmonia natural da região."

    status_jogador["turno"] += 1
    
    # Verifica fim do jogo (fim das rodadas)
    if status_jogador["turno"] > len(historias):
        resumo_final = (
            f"### 🎉 Fim da Rodada!\n\n"
            f"**Resultado do seu Desempenho:**\n"
            f"- Pontuação Final: {status_jogador['pontuacao']}\n"
            f"- Densidade de Uso de Conhecimento da Natureza: {status_jogador['densidade_natureza']}%\n\n"
            f"Obrigado por jogar! Suas decisões foram armazenadas para avaliar o impacto ambiental."
        )
        return gr.update(visible=False), gr.update(value=resumo_final), gr.update(visible=False), obter_painel_status()

    return carregar_turno(feedback)

def carregar_turno(feedback_anterior=""):
    turno_atual = status_jogador["turno"] - 1
    dados_turno = historias[turno_atual]
    
    texto_exibicao = f"{feedback_anterior}\n\n{dados_turno['texto']}" if feedback_anterior else dados_turno['texto']
    
    # Atualiza os botões de rádio com as novas opções
    novas_opcoes = [op[0] for op in dados_turnos_opcoes(dados_turno)]
    
    return (
        gr.update(choices=novas_opcoes, value=None), 
        gr.update(value=texto_exibicao),
        gr.update(visible=True),
        obter_painel_status()
    )

def dados_turnos_opcoes(dados_turno):
    # Retorna as opções mapeadas para o componente
    return dados_turno["opcoes"]

def obter_painel_status():
    return (
        f"**Protagonista:** {status_jogador['nome']} | **Classe:** {status_jogador['classe']}\n"
        f"**Densidade Ecológica:** {status_jogador['densidade_natureza']}% | **Pontuação:** {status_jogador['pontuacao']}"
    )

# --- CONSTRUÇÃO DA INTERFACE COM GRADIO ---
with gr.Blocks() as demo:
    gr.Markdown("# 🌿 Solarpunk RPG Chronicles")
    gr.Markdown(
        "### Um RPG estilo Novel onde a natureza e a vida urbana andam lado a lado."
    )

    with gr.Row():
        # Painel de Status (Evolução do personagem e métricas)
        painel_status = gr.Markdown(obter_painel_status())

    gr.Markdown("---")

    # Corpo da história (onde a IA insere o texto)
    caixa_historia = gr.Markdown(historias[0]["texto"])

    # Input do jogador (Tomadas de decisão)
    opcoes_radio = gr.Radio(
        choices=[op[0] for op in historias[0]["opcoes"]],
        label="O que você decide fazer?",
    )

    botao_enviar = gr.Button("Confirmar Decisão", variant="primary")

    # Lógica de clique
    def intermediario_escolha(escolha_texto):
        turno_atual = status_jogador["turno"] - 1
        if turno_atual < len(historias):
            for texto, tipo in historias[turno_atual]["opcoes"]:
                if texto == escolha_texto:
                    return processar_escolha(tipo)
        return processar_escolha(None)

    botao_enviar.click(
        fn=intermediario_escolha,
        inputs=opcoes_radio,
        outputs=[opcoes_radio, caixa_historia, botao_enviar, painel_status],
    )

# Rodar a aplicação
if __name__ == "__main__":
    # CORREÇÃO: O tema foi movido para o método launch()
    demo.launch(theme=gr.themes.Soft())