let tiposAlta = [];
let internacaoDetalheId = null;

async function carregarTiposAlta() {
  tiposAlta = await App.api("/api/tipo-alta");
  const sel = document.getElementById("edit-tipo-alta");
  sel.innerHTML =
    '<option value="">—</option>' +
    tiposAlta.map((t) => `<option value="${t.id}">${t.alta}</option>`).join("");
}

function agruparPorNome(lista) {
  const map = new Map();

  for (const i of lista) {
    const nome = (i.nome_paciente || "Não informado").trim();
    const chave = nome.toLowerCase();

    if (!map.has(chave)) {
      map.set(chave, {
        nome,
        nascimento: null,
        internacoes: [],
      });
    }

    const grupo = map.get(chave);
    grupo.internacoes.push(i);

    if (i.data_nascimento_paciente && !grupo.nascimento) {
      grupo.nascimento = i.data_nascimento_paciente;
    }
  }

  for (const grupo of map.values()) {
    grupo.internacoes.sort((a, b) => {
      const da = a.data_internacao || "";
      const db = b.data_internacao || "";
      return db.localeCompare(da);
    });
  }

  return [...map.values()].sort((a, b) =>
    a.nome.localeCompare(b.nome, "pt-BR", { sensitivity: "base" })
  );
}

function renderListaPacientes(pacientes) {
  const container = document.getElementById("lista-pacientes");

  if (!pacientes.length) {
    container.innerHTML = '<p class="text-muted">Nenhum paciente cadastrado.</p>';
    return;
  }

  container.innerHTML = pacientes
    .map((pac, idx) => {
      const nasc = pac.nascimento ? App.formatDate(pac.nascimento) : "—";
      const totalPareceres = pac.internacoes.reduce(
        (s, i) => s + (i.pareceres?.length || 0),
        0
      );

      const linhas = pac.internacoes
        .map((i) => {
          const qtd = i.pareceres?.length || 0;
          return `
        <tr>
          <td>#${i.id}</td>
          <td>${App.formatDate(i.data_internacao)}</td>
          <td>${i.setor_internacao}</td>
          <td>${qtd}</td>
          <td class="table-actions">
            <button type="button" class="btn btn-ghost btn-sm" data-ver-internacao="${i.id}">Ver internação</button>
          </td>
        </tr>`;
        })
        .join("");

      return `
      <article class="paciente-grupo">
        <button type="button" class="paciente-grupo-header" data-toggle="pac-${idx}" aria-expanded="false">
          <span class="paciente-grupo-titulo">${pac.nome}</span>
          <span class="paciente-grupo-meta">${pac.internacoes.length} internação(ões) · ${totalPareceres} parecer(es)</span>
        </button>
        <div id="pac-${idx}" class="paciente-grupo-body hidden">
          <p class="text-muted paciente-grupo-detalhe">Nascimento: ${nasc}</p>
          <div class="table-wrap">
            <table class="table table-compact">
              <thead>
                <tr>
                  <th>ID internação</th>
                  <th>Data internação</th>
                  <th>Setor</th>
                  <th>Pareceres</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>${linhas}</tbody>
            </table>
          </div>
        </div>
      </article>`;
    })
    .join("");

  container.querySelectorAll("[data-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const panel = document.getElementById(btn.dataset.toggle);
      const aberto = !panel.classList.contains("hidden");
      panel.classList.toggle("hidden", aberto);
      btn.setAttribute("aria-expanded", String(!aberto));
    });
  });

  container.querySelectorAll("[data-ver-internacao]").forEach((btn) => {
    btn.addEventListener("click", () => abrirModalInternacao(btn.dataset.verInternacao));
  });
}

function prontuarioParecer(p) {
  return p.numero_prontuario || p.internacao?.numero_prontuario || "—";
}

function renderDetalheInternacao(i) {
  const pareceres = [...(i.pareceres || [])].sort((a, b) => b.id - a.id);
  const tipoAlta = i.tipo_alta?.alta || "—";

  const tabelaPareceres =
    pareceres.length === 0
      ? '<p class="text-muted">Nenhum parecer nesta internação.</p>'
      : `<div class="table-wrap">
          <table class="table table-compact">
            <thead>
              <tr>
                <th>ID parecer</th>
                <th>Prontuário</th>
                <th>Aluno</th>
                <th>Solicitação</th>
                <th>Resposta</th>
                <th>Observações</th>
              </tr>
            </thead>
            <tbody>
              ${pareceres
                .map(
                  (p) => `
              <tr>
                <td>#${p.id}</td>
                <td><strong>${prontuarioParecer(p)}</strong></td>
                <td>${p.usuario?.nome || "—"}</td>
                <td>${App.formatDateTime(p.data_solicitacao_parecer)}</td>
                <td>${App.formatDateTime(p.data_parecer)}</td>
                <td class="cell-texto">${(p.texto_parecer || "—").slice(0, 200)}${(p.texto_parecer || "").length > 200 ? "…" : ""}</td>
              </tr>`
                )
                .join("")}
            </tbody>
          </table>
        </div>`;

  return `
    <dl class="detalhe-dl">
      <dt>Paciente</dt><dd>${i.nome_paciente}</dd>
      <dt>Internação</dt><dd>#${i.id}</dd>
      <dt>Data de internação</dt><dd>${App.formatDate(i.data_internacao)}</dd>
      <dt>Setor</dt><dd>${i.setor_internacao}</dd>
      <dt>Alta</dt><dd>${i.data_alta ? App.formatDate(i.data_alta) : "—"} (${tipoAlta})</dd>
    </dl>
    <h3 class="form-subtitle">Pareceres desta internação</h3>
    <p class="text-muted form-section-hint">Cada parecer mantém o número de prontuário informado no registro.</p>
    ${tabelaPareceres}`;
}

async function abrirModalInternacao(id) {
  const i = await App.api(`/api/internacao/${id}`);
  internacaoDetalheId = i.id;
  document.getElementById(
    "modal-internacao-titulo"
  ).textContent = `Internação #${i.id} — ${i.nome_paciente}`;
  document.getElementById("modal-internacao-conteudo").innerHTML = renderDetalheInternacao(i);
  document.getElementById("modal-internacao").classList.remove("hidden");
}

function fecharModalInternacao() {
  document.getElementById("modal-internacao").classList.add("hidden");
  internacaoDetalheId = null;
}

async function listarPacientes() {
  const lista = await App.api("/api/internacao");
  renderListaPacientes(agruparPorNome(lista));
}

async function abrirModalEditar(id) {
  const i = await App.api(`/api/internacao/${id}`);
  document.getElementById("edit-pac-id").value = i.id;
  document.getElementById("edit-prontuario").value = i.numero_prontuario;
  document.getElementById("edit-setor").value = i.setor_internacao;
  document.getElementById("edit-nome-pac").value = i.nome_paciente;
  document.getElementById("edit-data-int").value = i.data_internacao || "";
  document.getElementById("edit-sexo").value = i.sexo_paciente || "F";
  document.getElementById("edit-data-alta").value = i.data_alta || "";
  document.getElementById("edit-tipo-alta").value = i.tipo_alta_id || "";
  document.getElementById("edit-obs-alta").value = i.obs_alta || "";
  document.getElementById("modal-paciente").classList.remove("hidden");
  App.initCharCounters(document.getElementById("form-editar-paciente"));
}

function fecharModalEditar() {
  document.getElementById("modal-paciente").classList.add("hidden");
}

document.addEventListener("DOMContentLoaded", async () => {
  try {
    await carregarTiposAlta();
    await listarPacientes();

    document.getElementById("btn-fechar-internacao").addEventListener("click", fecharModalInternacao);
    document.getElementById("btn-editar-internacao").addEventListener("click", () => {
      if (!internacaoDetalheId) return;
      const id = internacaoDetalheId;
      fecharModalInternacao();
      abrirModalEditar(id);
    });

    document.getElementById("form-editar-paciente").addEventListener("submit", async (e) => {
      e.preventDefault();
      const id = document.getElementById("edit-pac-id").value;
      try {
        const i = await App.api(`/api/internacao/${id}`);
        await App.api(`/api/internacao/${id}`, {
          method: "PUT",
          body: {
            data_internacao: document.getElementById("edit-data-int").value,
            numero_prontuario: document.getElementById("edit-prontuario").value,
            setor_internacao: document.getElementById("edit-setor").value,
            nome_paciente: document.getElementById("edit-nome-pac").value,
            sexo_paciente: document.getElementById("edit-sexo").value,
            data_nascimento_paciente: i.data_nascimento_paciente,
            grau_instrucao_paciente: i.grau_instrucao_paciente,
            moradia_paciente: i.moradia_paciente,
            familiares_atendidos: i.familiares_atendidos,
            criado_por: i.criado_por,
            data_alta: document.getElementById("edit-data-alta").value || null,
            tipo_alta_id: document.getElementById("edit-tipo-alta").value
              ? parseInt(document.getElementById("edit-tipo-alta").value, 10)
              : null,
            obs_alta: document.getElementById("edit-obs-alta").value || null,
          },
        });
        const tipoId = document.getElementById("edit-tipo-alta").value;
        if (document.getElementById("edit-data-alta").value || tipoId) {
          await App.api(`/api/internacao/${id}/alta`, {
            method: "PUT",
            body: {
              data_alta: document.getElementById("edit-data-alta").value || null,
              tipo_alta_id: tipoId ? parseInt(tipoId, 10) : null,
              obs_alta: document.getElementById("edit-obs-alta").value || null,
            },
          });
        }
        App.showModal("success", "Sucesso", "Internação atualizada.");
        fecharModalEditar();
        await listarPacientes();
      } catch (err) {
        App.showModal("error", "Erro", err.message);
      }
    });

    document.getElementById("btn-excluir-paciente").addEventListener("click", async () => {
      const id = document.getElementById("edit-pac-id").value;
      if (!confirm("Remover esta internação?")) return;
      try {
        await App.api(`/api/internacao/${id}`, { method: "DELETE" });
        App.showModal("success", "Sucesso", "Internação removida.");
        fecharModalEditar();
        await listarPacientes();
      } catch (err) {
        App.showModal("error", "Erro", err.message);
      }
    });

    document.getElementById("btn-fechar-paciente").addEventListener("click", fecharModalEditar);
  } catch (err) {
    App.showModal("error", "Erro", err.message);
  }
});
