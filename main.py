import requests
from bs4 import BeautifulSoup
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import numpy as np

# =========================
# CONFIG
# =========================
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# SCRAPING
# =========================

URLS = [
    "https://pt.wikipedia.org/wiki/Copa_do_Mundo_FIFA",
    "https://pt.wikipedia.org/wiki/Copa_do_Mundo_de_1930",
    "https://pt.wikipedia.org/wiki/Copa_do_Mundo_de_1958",
]

def coletar_texto(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        paragrafos = soup.find_all("p")

        texto = ""
        for p in paragrafos:
            txt = re.sub(r'\[\d+\]', '', p.get_text())
            if len(txt.strip()) > 50:
                texto += txt.strip() + "\n"

        return texto

    except Exception as e:
        print(f"Erro ao coletar {url}: {e}")
        return ""

def coletar_todos():
    textos = []
    for url in URLS:
        print(f"Coletando: {url}")
        textos.append(coletar_texto(url))
    return "\n".join(textos)

# =========================
# CHUNKS
# =========================

def gerar_chunks(texto, tamanho=100, overlap=25):
    palavras = texto.split()
    chunks = []

    for i in range(0, len(palavras), tamanho - overlap):
        chunk = " ".join(palavras[i:i+tamanho])
        chunks.append(chunk)

    return chunks

# =========================
# SISTEMA DE BUSCA
# =========================

class SistemaBusca:
    def __init__(self):
        self.chunks = []
        self.vetores = None

    def indexar(self, chunks):
        print(f"Gerando embeddings para {len(chunks)} chunks...")
        self.chunks = chunks
        self.vetores = model.encode(chunks)
        
    def gerar_embedding(self, texto):
        return model.encode([texto])[0]  # ✅ corrigido

    def buscar(self, query, top_n=5):
        emb = self.gerar_embedding(query)

        scores = np.dot(self.vetores, emb) / (
            np.linalg.norm(self.vetores, axis=1) * np.linalg.norm(emb)
        )

        indices = np.argsort(scores)[-top_n:][::-1]

        return [(self.chunks[i], float(scores[i])) for i in indices]
# =========================
# LAZY LOAD
# =========================

sistema = None

def get_sistema():
    global sistema

    if sistema is None:
        print("Inicializando sistema...")

        texto_scraping = coletar_todos()

        texto_manual = """
        A Alemanha venceu a Copa do Mundo de 2014 ao derrotar a Argentina.
        A França venceu a Copa do Mundo de 2018 ao derrotar a Croácia.
        O Uruguai venceu a Copa do Mundo de 1930.
        O Brasil venceu a Copa do Mundo de 1958 com Pelé como destaque.
        """

        texto = texto_scraping + "\n" + texto_manual
        chunks = gerar_chunks(texto)[:50]

        sistema = SistemaBusca()
        sistema.indexar(chunks)

    return sistema

# =========================
# ROTAS
# =========================

@app.get("/")
def read_root():
    return {"message": "Sistema rodando 🚀"}

@app.get("/buscar")
def buscar(query: str):
    sistema = get_sistema() 

    emb = sistema.gerar_embedding(query)
    resultados = sistema.buscar(query, top_n=5)

    return {
        "query": query,
        "embedding_query": emb[:10].tolist(),  
        "resultados": [
            {"texto": chunk[:200], "score": score}
            for chunk, score in resultados
        ]
    }