# Lista de Mercado em Tempo Real 🛒

App colaborativo: um adiciona itens em casa, o outro vê e risca a lista
em tempo real dentro do mercado. Feito 100% em Python.

## Como o projeto é dividido

```
lista-mercado/
├── backend/     -> servidor (roda 24h na internet, guarda a lista)
│   ├── main.py
│   └── requirements.txt
└── client/      -> o app que vocês instalam no celular
    ├── app.py
    └── requirements.txt
```

Como vocês vão usar o app estando em redes diferentes (você no mercado,
sua esposa em casa), o **backend precisa ficar hospedado na internet**
— rodando só no seu computador não funciona, porque o celular de fora
não conseguiria alcançá-lo.

---

## Passo 1 — Testar o backend no seu computador

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Acesse `http://localhost:8000/itens` no navegador — se aparecer `[]`,
está funcionando (lista vazia).

---

## Passo 2 — Hospedar o backend na internet (grátis)

Recomendo o **Render.com** (tem plano gratuito, bom pra projetos assim):

1. Crie uma conta em https://render.com
2. Suba a pasta `backend/` para um repositório no GitHub
3. No Render: **New > Web Service**, conecte o repositório
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Após o deploy, o Render te dá uma URL tipo:
   `https://lista-mercado-xxxx.onrender.com`

⚠️ Observação: no plano gratuito, o servidor "dorme" depois de um tempo
sem uso e demora uns segundos pra acordar na próxima requisição — normal
para uso doméstico, mas fique ciente.

Alternativas parecidas: **Railway.app** e **Fly.io**.

---

## Passo 3 — Conectar o app cliente ao servidor

Abra `client/app.py` e troque estas duas linhas pela URL que o Render
te deu:

```python
SERVIDOR_HTTP = "https://lista-mercado-xxxx.onrender.com"
SERVIDOR_WS = "wss://lista-mercado-xxxx.onrender.com/ws"
```

Repare que `http` vira `https` e `ws` vira `wss` (versões seguras, que o
Render exige).

---

## Passo 4 — Rodar o app cliente

Para testar no computador antes de instalar no celular:

```bash
cd client
pip install -r requirements.txt
python app.py
```

Isso abre uma janela de desktop já funcional. Peça pra sua esposa rodar
o mesmo `app.py` no computador dela (com o mesmo servidor configurado) e
testem adicionando itens dos dois lados.

---

## Passo 5 — Transformar em app instalável (Android/iOS/desktop)

O Flet usa o `flet build` para empacotar seu código Python em um app de
verdade:

```bash
# Android (gera um .apk que dá pra instalar direto no celular)
flet build apk

# iOS (precisa de um Mac com Xcode)
flet build ipa

# Windows / macOS / Linux (programa de computador)
flet build windows   # ou macos / linux
```

O `.apk` gerado fica em `client/build/apk/` — basta transferir esse
arquivo pro celular Android (por WhatsApp, e-mail, cabo, etc) e instalar
manualmente (o Android vai pedir pra liberar "instalar de fontes
desconhecidas" na primeira vez).

> 💡 Se o `flet build` pedir o Flutter SDK e você não quiser instalar
> tudo isso localmente, o Flet oferece um serviço de build na nuvem
> (`flet build apk --cloud` na versão mais recente) que compila sem
> precisar de nada instalado — confira a documentação oficial do Flet
> para o comando exato da versão que você instalou.

---

## Resumo do fluxo

1. Backend fica sempre ligado na internet (Render).
2. Você e sua esposa instalam o mesmo app (gerado pelo `flet build`) nos
   celulares, ambos apontando pro mesmo endereço do backend.
3. Qualquer item adicionado por um aparece instantaneamente no outro,
   graças ao WebSocket.

## Próximos passos possíveis (se quiser evoluir depois)
- Autenticação simples (senha compartilhada) pra ninguém de fora mexer na lista
- Categorias de produtos (hortifruti, limpeza, etc)
- Histórico de listas anteriores