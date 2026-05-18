document.addEventListener("DOMContentLoaded", async () => {
  try {
    const stats = await App.api("/api/dashboard/stats");

    document.getElementById("stat-tempo").textContent =
      stats.tempo_medio_resposta_dias > 0
        ? `${stats.tempo_medio_resposta_dias} dias`
        : "—";

    document.getElementById("stat-total").textContent = stats.total_pareceres_com_resposta;

    const chart = document.getElementById("chart-setores");
    const empty = document.getElementById("chart-empty");
    const dados = stats.distribuicao_por_setor || [];

    if (!dados.length) {
      chart.innerHTML = "";
      empty.classList.remove("hidden");
      return;
    }

    empty.classList.add("hidden");
    const maxPct = Math.max(...dados.map((d) => d.percentual), 1);

    chart.innerHTML = dados
      .map(
        (d) => `
      <div class="bar-row">
        <span class="bar-label" title="${d.setor}">${d.setor}</span>
        <div class="bar-track">
          <div class="bar-fill" style="width: ${(d.percentual / maxPct) * 100}%"></div>
        </div>
        <span class="bar-pct">${d.percentual}%</span>
      </div>`
      )
      .join("");
  } catch (err) {
    App.showModal("error", "Erro", err.message);
  }
});
