let perfis = [];

async function carregarPerfis(selectIds) {
  perfis = await App.api("/api/perfil");
  selectIds.forEach((id) => {
    const sel = document.getElementById(id);
    if (!sel) return;
    sel.innerHTML = perfis
      .map((p) => `<option value="${p.id}">${p.nome}</option>`)
      .join("");
  });
}

async function listarUsuarios() {
  const usuarios = await App.api("/api/usuario");
  const tbody = document.querySelector("#tabela-usuarios tbody");
  tbody.innerHTML = usuarios
    .map(
      (u) => `
    <tr>
      <td>${u.nome}</td>
      <td>${u.email}</td>
      <td>${u.perfil?.nome || u.perfil_id}</td>
      <td class="table-actions">
        <button type="button" class="btn btn-ghost btn-sm" data-id="${u.id}">Ver / Editar</button>
      </td>
    </tr>`
    )
    .join("");

  tbody.querySelectorAll("button[data-id]").forEach((btn) => {
    btn.addEventListener("click", () => abrirModal(btn.dataset.id));
  });
}

async function abrirModal(id) {
  const u = await App.api(`/api/usuario/${id}`);
  document.getElementById("edit-id").value = u.id;
  document.getElementById("edit-nome").value = u.nome;
  document.getElementById("edit-email").value = u.email;
  document.getElementById("edit-senha").value = "";
  document.getElementById("edit-perfil").value = u.perfil_id;
  document.getElementById("modal-usuario").classList.remove("hidden");
}

function fecharModal() {
  document.getElementById("modal-usuario").classList.add("hidden");
}

document.addEventListener("DOMContentLoaded", async () => {
  try {
    await carregarPerfis(["u-perfil", "edit-perfil"]);
    await listarUsuarios();

    document.getElementById("form-usuario").addEventListener("submit", async (e) => {
      e.preventDefault();
      try {
        await App.api("/api/usuario", {
          method: "POST",
          body: {
            nome: document.getElementById("u-nome").value,
            email: document.getElementById("u-email").value,
            senha: document.getElementById("u-senha").value,
            perfil_id: parseInt(document.getElementById("u-perfil").value, 10),
          },
        });
        e.target.reset();
        App.showModal("success", "Sucesso", "Usuário criado.");
        await listarUsuarios();
      } catch (err) {
        App.showModal("error", "Erro", err.message);
      }
    });

    document.getElementById("form-editar-usuario").addEventListener("submit", async (e) => {
      e.preventDefault();
      const id = document.getElementById("edit-id").value;
      const body = {
        nome: document.getElementById("edit-nome").value,
        email: document.getElementById("edit-email").value,
        perfil_id: parseInt(document.getElementById("edit-perfil").value, 10),
      };
      const senha = document.getElementById("edit-senha").value;
      if (senha) body.senha = senha;
      try {
        await App.api(`/api/usuario/${id}`, { method: "PUT", body });
        App.showModal("success", "Sucesso", "Usuário atualizado.");
        fecharModal();
        await listarUsuarios();
      } catch (err) {
        App.showModal("error", "Erro", err.message);
      }
    });

    document.getElementById("btn-inativar-usuario").addEventListener("click", async () => {
      const id = document.getElementById("edit-id").value;
      if (!confirm("Inativar este usuário?")) return;
      try {
        await App.api(`/api/usuario/${id}/inativar`, { method: "POST" });
        App.showModal("success", "Sucesso", "Usuário inativado.");
        fecharModal();
        await listarUsuarios();
      } catch (err) {
        App.showModal("error", "Erro", err.message);
      }
    });

    document.getElementById("btn-fechar-usuario").addEventListener("click", fecharModal);
  } catch (err) {
    App.showModal("error", "Erro", err.message);
  }
});
