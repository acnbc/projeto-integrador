/** Utilitários globais: auth, API, modal, contadores de caracteres */
const App = {
  PERFIL_COORDENADOR: 1,
  PERFIL_ALUNO: 2,

  getToken() {
    return localStorage.getItem("access_token");
  },

  getUser() {
    const raw = localStorage.getItem("user");
    return raw ? JSON.parse(raw) : null;
  },

  setSession(token, user) {
    localStorage.setItem("access_token", token);
    localStorage.setItem("user", JSON.stringify(user));
  },

  clearSession() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
  },

  isCoordenador() {
    const u = this.getUser();
    return u && u.perfil_id === this.PERFIL_COORDENADOR;
  },

  isAluno() {
    const u = this.getUser();
    return u && u.perfil_id === this.PERFIL_ALUNO;
  },

  async api(path, options = {}) {
    const headers = { ...(options.headers || {}) };
    const token = this.getToken();
    if (token) headers.Authorization = `Bearer ${token}`;

    if (options.body && typeof options.body === "object" && !(options.body instanceof FormData)) {
      headers["Content-Type"] = "application/json";
      options.body = JSON.stringify(options.body);
    }

    const res = await fetch(path, { ...options, headers });

    if (res.status === 204) return null;

    let data = null;
    const text = await res.text();
    if (text) {
      try {
        data = JSON.parse(text);
      } catch {
        data = { detail: text };
      }
    }

    if (!res.ok) {
      const msg = data?.detail
        ? typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail)
        : `Erro ${res.status}`;
      throw new Error(msg);
    }
    return data;
  },

  showModal(type, title, message) {
    const overlay = document.getElementById("modal-overlay");
    const icon = document.getElementById("modal-icon");
    const titleEl = document.getElementById("modal-title");
    const msgEl = document.getElementById("modal-message");
    if (!overlay) return;

    icon.className = "modal-icon " + (type === "success" ? "success" : "error");
    icon.textContent = type === "success" ? "✓" : "!";
    titleEl.textContent = title;
    msgEl.textContent = message;
    overlay.classList.remove("hidden");
    overlay.setAttribute("aria-hidden", "false");
  },

  hideModal() {
    const overlay = document.getElementById("modal-overlay");
    if (overlay) {
      overlay.classList.add("hidden");
      overlay.setAttribute("aria-hidden", "true");
    }
  },

  bindModal() {
    document.getElementById("modal-close")?.addEventListener("click", () => this.hideModal());
    document.getElementById("modal-overlay")?.addEventListener("click", (e) => {
      if (e.target.id === "modal-overlay") this.hideModal();
    });
  },

  initCharCounters(root = document) {
    root.querySelectorAll("[data-char-counter][data-maxlength]").forEach((el) => {
      const max = parseInt(el.dataset.maxlength, 10);
      const counter = root.querySelector(`.char-counter[data-for="${el.id}"]`);
      if (!counter) return;

      const update = () => {
        const len = el.value.length;
        const rest = max - len;
        counter.textContent =
          rest > 0
            ? `${rest} caractere${rest !== 1 ? "s" : ""} restante${rest !== 1 ? "s" : ""}`
            : "Limite atingido";
        counter.classList.toggle("warn", rest <= Math.ceil(max * 0.15) && rest > 0);
        counter.classList.toggle("danger", rest <= 0);
      };
      el.addEventListener("input", update);
      update();
    });
  },

  setupNav() {
    const user = this.getUser();
    const label = document.getElementById("user-label");
    if (label && user) label.textContent = user.nome || user.email;

    if (user) document.body.dataset.perfil = String(user.perfil_id);

    document.getElementById("btn-logout")?.addEventListener("click", () => {
      this.clearSession();
      window.location.href = "/login";
    });
  },

  guardPage() {
    const page = document.body.dataset.page;

    this.bindModal();

    if (page === "login") return;

    if (!this.getToken()) {
      window.location.href = "/login";
      return;
    }

    if (page === "pareceres" && this.isAluno()) {
      window.location.href = "/pareceres/novo";
      return;
    }

    const required = document.body.dataset.perfilRequerido;
    if (required === "coordenador" && !this.isCoordenador()) {
      window.location.href = "/pareceres/novo";
      return;
    }

    this.setupNav();
  },

  formatDate(iso) {
    if (!iso) return "—";
    const parte = String(iso).split("T")[0];
    return parte.split("-").reverse().join("/");
  },

  formatDateTime(iso) {
    if (!iso) return "—";
    const match = String(iso).match(/^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2})/);
    if (match) {
      const [, data, hora] = match;
      return `${data.split("-").reverse().join("/")} ${hora}`;
    }
    return this.formatDate(iso);
  },

  splitDateTime(iso) {
    if (!iso) return { date: "", time: "" };
    const match = String(iso).match(/^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2})/);
    if (match) return { date: match[1], time: match[2] };
    return { date: String(iso).split("T")[0], time: "" };
  },

  combineDateTime(dateStr, timeStr) {
    if (!dateStr) return null;
    return `${dateStr}T${timeStr || "00:00"}:00`;
  },
};

document.addEventListener("DOMContentLoaded", () => App.guardPage());
