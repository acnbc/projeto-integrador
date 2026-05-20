document.addEventListener("DOMContentLoaded", () => {
  App.bindModal();

  if (App.getToken()) {
    window.location.href = App.isCoordenador() ? "/dashboard" : "/pareceres/novo";
    return;
  }

  document.getElementById("form-login").addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const btn = document.getElementById("btn-login");
    btn.disabled = true;

    try {
      const body = new URLSearchParams();
      body.append("username", email);
      body.append("password", password);

      const tokenRes = await fetch("/api/usuario/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body,
      });

      const raw = await tokenRes.text();
      let tokenData = null;
      if (raw) {
        try {
          tokenData = JSON.parse(raw);
        } catch {
          throw new Error(
            tokenRes.status >= 500
              ? "Servidor indisponível. Verifique se o MySQL está em execução."
              : "Resposta inválida do servidor."
          );
        }
      }
      if (!tokenRes.ok) {
        throw new Error(
          typeof tokenData?.detail === "string"
            ? tokenData.detail
            : "E-mail ou senha incorretos"
        );
      }

      App.setSession(tokenData.access_token, { email });

      const user = await App.api("/api/usuario/me");
      App.setSession(tokenData.access_token, user);

      App.showModal("success", "Login realizado", `Bem-vindo(a), ${user.nome}!`);
      setTimeout(() => {
        window.location.href =
          user.perfil_id === App.PERFIL_COORDENADOR ? "/dashboard" : "/pareceres/novo";
      }, 800);
    } catch (err) {
      App.showModal("error", "Falha no login", err.message);
    } finally {
      btn.disabled = false;
    }
  });
});
