
const API_URL = "https://about-copa.onrender.com/docs#";

async function buscar() {
  const query = document.getElementById("query").value;
  const resultsDiv = document.getElementById("results");

  if (!query) {
    alert("Digite uma busca!");
    return;
  }

  resultsDiv.innerHTML = "<p>Carregando...</p>";

  try {
    const response = await fetch(
      `${API_URL}?query=${encodeURIComponent(query)}`,
    );
    const data = await response.json();

    let html = "";

    // Embedding da query
    html += `
      <div class="card">
        <strong>Embedding da Query (primeiros 10 valores):</strong>
        <div class="embedding">${data.embedding_query.join(", ")}</div>
      </div>
    `;
    // Resultados
    data.resultados.forEach((item, index) => {
      html += `
        <div class="card">
          <strong>Resultado ${index + 1}</strong>
          <p>${item.texto}</p>
          <div class="score">Score: ${item.score.toFixed(4)}</div>
        </div>
      `;
    });

    resultsDiv.innerHTML = html;

    // Scroll automático
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: "smooth",
    });
  } catch (error) {
    resultsDiv.innerHTML = "<p>Erro ao buscar dados.</p>";
    console.error(error);
  }
}

