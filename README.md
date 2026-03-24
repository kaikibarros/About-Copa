# 🚀 Busca Semântica com FastAPI

API de busca semântica que utiliza **embeddings** para encontrar textos com base no significado, não apenas por palavras-chave.

---

## ⚙️ Como Funciona

1. Coleta textos da Wikipedia  
2. Divide em **chunks**  
3. Gera embeddings com `SentenceTransformers`  
4. Calcula similaridade com **cosine similarity**  

---

## 🔌 Endpoints

### `GET /`
Retorna status da API

```json
{
  "message": "Sistema de busca semântica rodando 🚀"
}

GET /buscar?query=...

Realiza busca semântica

Exemplo:

/buscar?query=Brasil ganhou copa

Resposta:

{
  "query": "Brasil ganhou copa",
  "embedding_query": [0.12, -0.34, ...],
  "resultados": [
    {
      "texto": "O Brasil venceu a Copa do Mundo de 1958...",
      "score": 0.89
    }
  ]
}
``` 
# ▶️ Como Rodar
pip install fastapi uvicorn requests beautifulsoup4 numpy scikit-learn sentence-transformers
uvicorn main:app --reload

Acesse:

http://127.0.0.1:8000
http://127.0.0.1:8000/docs
```
```
# 🧠 Tecnologias

FastAPI
Sentence Transformers
Scikit-learn
BeautifulSoup
NumPy

``` 
```
# 🎯 Objetivo

   Demonstrar busca semântica com embeddings e API REST
