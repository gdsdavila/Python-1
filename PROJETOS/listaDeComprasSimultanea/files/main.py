"""
Backend da Lista de Mercado em Tempo Real
==========================================
Este servidor é o "cérebro" do aplicativo. Ele guarda a lista de compras
em um banco de dados e avisa TODOS os aparelhos conectados sempre que
algo muda (item adicionado, marcado como comprado, removido, etc).

Tecnologias usadas:
- FastAPI: framework web para criar a API (as "portas de entrada" que o app usa)
- WebSockets: canal de comunicação que fica aberto, permitindo que o servidor
  "empurre" atualizações para os celulares sem que eles precisem ficar perguntando
  "tem novidade?" a cada segundo (isso é o que dá a sensação de "tempo real")
- SQLite: banco de dados simples, guardado em um único arquivo (mercado.db)
"""

import json
import sqlite3
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_PATH = "mercado.db"


# ---------------------------------------------------------------------------
# 1. BANCO DE DADOS
# ---------------------------------------------------------------------------
def get_db() -> sqlite3.Connection:
    """Abre uma conexão com o banco. Cada função abre a sua e fecha depois,
    isso evita problemas quando várias pessoas mexem no app ao mesmo tempo."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acessar colunas pelo nome (ex: row["nome"])
    return conn


def init_db():
    """Cria a tabela de itens se ela ainda não existir. Roda uma vez, quando
    o servidor liga."""
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade TEXT DEFAULT '1',
            comprado INTEGER DEFAULT 0,   -- 0 = falso, 1 = verdadeiro (SQLite não tem bool)
            adicionado_por TEXT DEFAULT ''
        )
        """
    )
    conn.commit()
    conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # "lifespan" é o jeito do FastAPI de rodar código no início e no fim do servidor
    init_db()
    yield  # o servidor fica rodando aqui até ser desligado
    # (nada especial a fazer quando desliga, nesse caso)


app = FastAPI(lifespan=lifespan)

# CORS: sem isso, o app do celular é bloqueado de "conversar" com o servidor
# quando eles estão em endereços diferentes. Em produção, troque "*" pelo
# endereço real do seu app por segurança.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# 2. FORMATO DOS DADOS (o que a API espera receber / devolver)
# ---------------------------------------------------------------------------
class NovoItem(BaseModel):
    nome: str
    quantidade: str = "1"
    adicionado_por: str = ""


class AtualizarItem(BaseModel):
    comprado: bool


def item_para_dict(row: sqlite3.Row) -> dict:
    """Transforma uma linha do banco em um dicionário simples (fácil de virar JSON)."""
    return {
        "id": row["id"],
        "nome": row["nome"],
        "quantidade": row["quantidade"],
        "comprado": bool(row["comprado"]),
        "adicionado_por": row["adicionado_por"],
    }


def listar_itens() -> List[dict]:
    conn = get_db()
    # ORDER BY comprado: os itens ainda não comprados aparecem primeiro
    rows = conn.execute("SELECT * FROM itens ORDER BY comprado, id").fetchall()
    conn.close()
    return [item_para_dict(r) for r in rows]


# ---------------------------------------------------------------------------
# 3. GERENCIADOR DE CONEXÕES EM TEMPO REAL (WebSocket)
# ---------------------------------------------------------------------------
class GerenciadorConexoes:
    """Guarda a lista de celulares conectados no momento e sabe como
    mandar mensagem pra todos eles de uma vez (broadcast)."""

    def __init__(self):
        self.conexoes_ativas: List[WebSocket] = []

    async def conectar(self, ws: WebSocket):
        await ws.accept()
        self.conexoes_ativas.append(ws)

    def desconectar(self, ws: WebSocket):
        if ws in self.conexoes_ativas:
            self.conexoes_ativas.remove(ws)

    async def transmitir_lista_atualizada(self):
        """Envia a lista atual de itens para TODOS os aparelhos conectados.
        É isso que faz a mágica do tempo real acontecer: assim que sua esposa
        adiciona um item em casa, seu celular no mercado recebe a atualização
        na hora, sem precisar recarregar nada."""
        dados = json.dumps({"tipo": "lista_atualizada", "itens": listar_itens()})
        conexoes_com_erro = []
        for conexao in self.conexoes_ativas:
            try:
                await conexao.send_text(dados)
            except Exception:
                conexoes_com_erro.append(conexao)
        for c in conexoes_com_erro:
            self.desconectar(c)


gerenciador = GerenciadorConexoes()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Ponto de conexão em tempo real. O app do celular conecta aqui e fica
    'escutando' por mudanças na lista."""
    await gerenciador.conectar(websocket)
    # assim que alguém conecta, já manda a lista atual pra ele
    await websocket.send_text(json.dumps({"tipo": "lista_atualizada", "itens": listar_itens()}))
    try:
        while True:
            # mantemos a conexão aberta esperando o cliente. Não fazemos nada
            # com o que ele manda aqui, porque as ações de verdade (adicionar,
            # marcar, remover) vêm pelas rotas HTTP normais lá embaixo.
            await websocket.receive_text()
    except WebSocketDisconnect:
        gerenciador.desconectar(websocket)


# ---------------------------------------------------------------------------
# 4. ROTAS DA API (ações que o app pode fazer)
# ---------------------------------------------------------------------------
@app.get("/itens")
def get_itens():
    """Devolve a lista de compras atual (usado quando o app abre)."""
    return listar_itens()


@app.post("/itens")
async def adicionar_item(item: NovoItem):
    """Adiciona um novo item à lista e avisa todo mundo em tempo real."""
    conn = get_db()
    conn.execute(
        "INSERT INTO itens (nome, quantidade, adicionado_por) VALUES (?, ?, ?)",
        (item.nome, item.quantidade, item.adicionado_por),
    )
    conn.commit()
    conn.close()
    await gerenciador.transmitir_lista_atualizada()
    return {"ok": True}


@app.put("/itens/{item_id}")
async def marcar_item(item_id: int, dados: AtualizarItem):
    """Marca/desmarca um item como comprado (usado quando alguém risca
    o item dentro do mercado)."""
    conn = get_db()
    resultado = conn.execute("SELECT id FROM itens WHERE id = ?", (item_id,)).fetchone()
    if resultado is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Item não encontrado")
    conn.execute("UPDATE itens SET comprado = ? WHERE id = ?", (int(dados.comprado), item_id))
    conn.commit()
    conn.close()
    await gerenciador.transmitir_lista_atualizada()
    return {"ok": True}


@app.delete("/itens/{item_id}")
async def remover_item(item_id: int):
    """Remove um item da lista (ex: adicionado por engano, ou não precisa mais)."""
    conn = get_db()
    conn.execute("DELETE FROM itens WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    await gerenciador.transmitir_lista_atualizada()
    return {"ok": True}


@app.delete("/itens")
async def limpar_comprados():
    """Remove de uma vez todos os itens já marcados como comprados
    (útil pra 'zerar' a lista depois que as compras terminam)."""
    conn = get_db()
    conn.execute("DELETE FROM itens WHERE comprado = 1")
    conn.commit()
    conn.close()
    await gerenciador.transmitir_lista_atualizada()
    return {"ok": True}
