let internacoesMap = {};

function nomeAluno(p) {
  return p.usuario?.nome || "—";
}

function dadosInternacao(p) {
  const prontuarioParecer = p.numero_prontuario;
  const i = p.internacao;
  if (i) {
    return {
      prontuario: prontuarioParecer || i.numero_prontuario,
      setor: i.setor_internacao,
      paciente: i.nome_paciente,
    };
  }
  const legado = internacoesMap[p.internacao_id];
  if (legado) {
    return {
      prontuario: legado.numero_prontuario,
      setor: legado.setor_internacao,
      paciente: legado.nome_paciente,
    };
  }
  return { prontuario: "—", setor: "—", paciente: "—" };
}

async function carregarInternacoesMap() {
  const lista = await App.api("/api/internacao");
  internacoesMap = Object.fromEntries(lista.map((i) => [i.id, i]));
  return lista;
}

async function listarPareceres() {
  const pareceres = await App.api("/api/parecer");
  const tbody = document.querySelector("#tabela-pareceres tbody");

  if (!pareceres.length) {
    tbody.innerHTML =
      '<tr><td colspan="8" class="text-muted">Nenhum parecer registrado.</td></tr>';
    return;
  }

  tbody.innerHTML = pareceres
    .map((p) => {
      const { prontuario, setor, paciente } = dadosInternacao(p);
      return `
    <tr>
      <td>${p.id}</td>
      <td>${prontuario}</td>
      <td>${paciente}</td>
      <td>${setor}</td>
      <td>${nomeAluno(p)}</td>
      <td>${App.formatDateTime(p.data_solicitacao_parecer)}</td>
      <td>${App.formatDateTime(p.data_parecer)}</td>
      <td class="table-actions">
        <button type="button" class="btn btn-ghost btn-sm" data-id="${p.id}">Detalhes</button>
      </td>
    </tr>`;
    })
    .join("");

  tbody.querySelectorAll("button[data-id]").forEach((btn) => {
    btn.addEventListener("click", () => abrirModal(btn.dataset.id));
  });
}

function preencherSelectInternacoes(selectId) {
  const sel = document.getElementById(selectId);
  sel.innerHTML = Object.values(internacoesMap)
    .map(
      (i) =>
        `<option value="${i.id}">#${i.id} — ${i.numero_prontuario} — ${i.nome_paciente} (${i.setor_internacao})</option>`
    )
    .join("");
}

async function abrirModal(id) {
  const p = await App.api(`/api/parecer/${id}`);
  document.getElementById("par-id").value = p.id;
  document.getElementById("par-internacao").value = p.internacao_id;
  const sol = App.splitDateTime(p.data_solicitacao_parecer);
  const res = App.splitDateTime(p.data_parecer);
  document.getElementById("par-solicitacao-data").value = sol.date;
  document.getElementById("par-solicitacao-hora").value = sol.time;
  document.getElementById("par-resposta-data").value = res.date;
  document.getElementById("par-resposta-hora").value = res.time;
  document.getElementById("par-texto").value = p.texto_parecer || "";
  document.getElementById("modal-parecer").classList.remove("hidden");
  App.initCharCounters(document.getElementById("form-editar-parecer"));
}

function fecharModal() {
  document.getElementById("modal-parecer").classList.add("hidden");
}

document.addEventListener("DOMContentLoaded", async () => {
  try {
    await carregarInternacoesMap();
    preencherSelectInternacoes("par-internacao");
    await listarPareceres();

    document.getElementById("form-editar-parecer").addEventListener("submit", async (e) => {
      e.preventDefault();
      const id = document.getElementById("par-id").value;
      try {
        await App.api(`/api/parecer/${id}`, {
          method: "PUT",
          body: {
            internacao_id: parseInt(document.getElementById("par-internacao").value, 10),
            data_solicitacao_parecer: App.combineDateTime(
              document.getElementById("par-solicitacao-data").value,
              document.getElementById("par-solicitacao-hora").value
            ),
            data_parecer: (() => {
              const d = document.getElementById("par-resposta-data").value;
              if (!d) return null;
              return App.combineDateTime(d, document.getElementById("par-resposta-hora").value);
            })(),
            texto_parecer: document.getElementById("par-texto").value,
          },
        });
        App.showModal("success", "Sucesso", "Parecer atualizado.");
        fecharModal();
        await listarPareceres();
      } catch (err) {
        App.showModal("error", "Erro", err.message);
      }
    });

    document.getElementById("btn-excluir-parecer").addEventListener("click", async () => {
      const id = document.getElementById("par-id").value;
      if (!confirm("Remover este parecer?")) return;
      try {
        await App.api(`/api/parecer/${id}`, { method: "DELETE" });
        App.showModal("success", "Sucesso", "Parecer removido.");
        fecharModal();
        await listarPareceres();
      } catch (err) {
        App.showModal("error", "Erro", err.message);
      }
    });

    document.getElementById("btn-fechar-parecer").addEventListener("click", fecharModal);
  } catch (err) {
    App.showModal("error", "Erro", err.message);
  }
});
