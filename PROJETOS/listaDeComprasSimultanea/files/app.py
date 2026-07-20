"""
Cliente da Lista de Mercado em Tempo Real (Flet)
=================================================
Esse é o aplicativo que você e sua esposa realmente abrem no celular.
Ele é escrito 100% em Python usando o Flet, um framework que transforma
código Python em um app de verdade — instalável no Android, iOS, ou até
como programa de computador — sem precisar aprender outra linguagem
(tipo Java, Swift ou JavaScript).

Como ele conversa com o servidor (backend):
- Usa requisições HTTP normais (biblioteca "requests") para ações como
  adicionar, marcar ou remover item.
- Mantém uma conexão WebSocket aberta em paralelo só para "escutar"
  quando a lista muda em outro celular — é isso que dá o efeito de
  tempo real.
"""

import json
import threading

import flet as ft
import requests
import websocket  # biblioteca "websocket-client" (nome de import é "websocket")

# ⚠️ IMPORTANTE: troque pelo endereço real do seu servidor depois que ele
# estiver hospedado na internet (veja o README.md do projeto para o passo
# a passo de hospedagem gratuita).
SERVIDOR_HTTP = "https://python-1-cliz.onrender.com"
SERVIDOR_WS = "wss://python-1-cliz.onrender.com/ws"


def main(page: ft.Page):
    page.title = "Lista de Mercado"
    page.window.width = 400
    page.window.height = 700
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # -----------------------------------------------------------------
    # Controles da tela (campos, botões, etc)
    # -----------------------------------------------------------------
    campo_nome_usuario = ft.TextField(label="Seu nome", value="Eu")
    campo_novo_item = ft.TextField(label="Novo item", expand=True)
    campo_quantidade = ft.TextField(label="Qtd", width=70, value="1")
    lista_view = ft.Column(spacing=8)
    texto_status = ft.Text("Conectando...", size=12, color=ft.Colors.GREY)

    # -----------------------------------------------------------------
    # Funções que falam com a API REST (ações do usuário)
    # -----------------------------------------------------------------
    def adicionar_item(e):
        if not campo_novo_item.value:
            return
        try:
            requests.post(
                f"{SERVIDOR_HTTP}/itens",
                json={
                    "nome": campo_novo_item.value,
                    "quantidade": campo_quantidade.value or "1",
                    "adicionado_por": campo_nome_usuario.value or "Alguém",
                },
                timeout=5,
            )
            # limpa os campos depois de adicionar; a lista na tela é atualizada
            # sozinha quando a mensagem chegar pelo WebSocket
            campo_novo_item.value = ""
            campo_quantidade.value = "1"
            page.update()
        except Exception as ex:
            mostrar_erro(f"Não consegui adicionar: {ex}")

    def alternar_comprado(item_id: int, valor_atual: bool):
        try:
            requests.put(
                f"{SERVIDOR_HTTP}/itens/{item_id}",
                json={"comprado": not valor_atual},
                timeout=5,
            )
        except Exception as ex:
            mostrar_erro(f"Não consegui atualizar: {ex}")

    def remover_item(item_id: int):
        try:
            requests.delete(f"{SERVIDOR_HTTP}/itens/{item_id}", timeout=5)
        except Exception as ex:
            mostrar_erro(f"Não consegui remover: {ex}")

    def mostrar_erro(msg: str):
        page.open(ft.SnackBar(ft.Text(msg)))
        page.update()

    # -----------------------------------------------------------------
    # Desenha a lista na tela a partir dos dados recebidos do servidor
    # -----------------------------------------------------------------
    def redesenhar_lista(itens: list):
        lista_view.controls.clear()
        for item in itens:
            checkbox = ft.Checkbox(
                value=item["comprado"],
                on_change=lambda e, i=item: alternar_comprado(i["id"], i["comprado"]),
            )
            texto = ft.Text(
                f'{item["nome"]} (x{item["quantidade"]})',
                color=ft.Colors.GREY if item["comprado"] else None,
            )
            subtitulo = ft.Text(
                f'adicionado por {item["adicionado_por"]}' if item["adicionado_por"] else "",
                size=10,
                color=ft.Colors.GREY,
            )
            botao_remover = ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                on_click=lambda e, i=item["id"]: remover_item(i),
            )
            linha = ft.Row(
                [checkbox, ft.Column([texto, subtitulo], spacing=0, expand=True), botao_remover]
            )
            lista_view.controls.append(linha)
        page.update()

    # -----------------------------------------------------------------
    # Conexão WebSocket rodando em uma thread separada, para não travar
    # a interface enquanto fica "escutando" o servidor
    # -----------------------------------------------------------------
    def escutar_websocket():
        def ao_receber_mensagem(ws, mensagem):
            dados = json.loads(mensagem)
            if dados.get("tipo") == "lista_atualizada":
                redesenhar_lista(dados["itens"])

        def ao_abrir(ws):
            texto_status.value = "Conectado (tempo real ativo)"
            texto_status.color = ft.Colors.GREEN
            page.update()

        def ao_fechar(ws, *args):
            texto_status.value = "Desconectado — tentando reconectar..."
            texto_status.color = ft.Colors.RED
            page.update()

        ws_app = websocket.WebSocketApp(
            SERVIDOR_WS,
            on_message=ao_receber_mensagem,
            on_open=ao_abrir,
            on_close=ao_fechar,
        )
        ws_app.run_forever(reconnect=5)  # tenta reconectar sozinho a cada 5s se cair

    # Busca a lista inicial via HTTP normal (antes do WebSocket conectar)
    try:
        resposta = requests.get(f"{SERVIDOR_HTTP}/itens", timeout=5)
        redesenhar_lista(resposta.json())
    except Exception:
        texto_status.value = "Não consegui conectar ao servidor"
        texto_status.color = ft.Colors.RED

    # Inicia o WebSocket em segundo plano
    # (thread "daemon" = fecha automaticamente junto com o app)
    threading.Thread(target=escutar_websocket, daemon=True).start()

    # -----------------------------------------------------------------
    # Layout da tela
    # -----------------------------------------------------------------
    page.add(
        campo_nome_usuario,
        ft.Row([campo_novo_item, campo_quantidade,
                ft.IconButton(icon=ft.Icons.ADD, on_click=adicionar_item)]),
        texto_status,
        ft.Divider(),
        lista_view,
    )


ft.app(target=main)
