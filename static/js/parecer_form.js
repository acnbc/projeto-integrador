const SETORES = [
  "CIRURGIA CARDÍACA",
  "CARDIOLOGIA",
  "CIRURGIA PLÁSTICA",
  "CIRURGIA GERA",
  "UI CIRÚRGICA",
  "CIRURGIA TORÁCICA",
  "CUCC (CENTRO UNIVERSITÁRIO DE CONTROLE DO CÂNCER)",
  "CIRURGIA VASCULAR",
  "CUIDADOS PALIATIVOS",
  "CLINICA DA DOR",
  "CLINICA MÉDICA",
  "CTI GERAL",
  "NAI (Núcleo de Atenção ao Idoso)",
  "DERMATOLOGIA",
  "NESA (Núcleo de Estudos de Saúde do Adolescente)",
  "DIP",
  "NEUROCIRURGIA",
  "ENDOCRINOLOGIA |",
  "OFTALMOLOGIA",
  "ORTOPEDIA",
  "GINECOLOGIA",
  "OTORRINOLARINGOLOGIA",
  "HEMATOLOGIA",
  "PEDIATRIA",
  "PSIQUIATRIA",
  "PNEUMOLOGIA",
  "UCI - Unidade Cardio Intensiva",
  "REUMATOLOGIA",
  "UROLOGIA",
];

let pacienteCarregado = null;
let preenchimentoAutomatico = false;

function preencherSetores(valorSelecionado = "") {
  const sel = document.getElementById("p-setor");
  sel.innerHTML =
    '<option value="">Selecione o setor</option>' +
    SETORES.map(
      (s) =>
        `<option value="${s}"${s === valorSelecionado ? " selected" : ""}>${s}</option>`
    ).join("");
}

async function carregarTiposAlta() {
  const tipos = await App.api("/api/tipo-alta");
  const sel = document.getElementById("p-tipo-alta");
  sel.innerHTML =
    '<option value="">— Não informado —</option>' +
    tipos.map((t) => `<option value="${t.id}">${t.alta}</option>`).join("");
}

function calcularIdade() {
  const nasc = document.getElementById("p-nascimento").value;
  const out = document.getElementById("p-idade");
  if (!nasc) {
    out.value = "";
    return;
  }
  const hoje = new Date();
  const dn = new Date(nasc + "T12:00:00");
  let idade = hoje.getFullYear() - dn.getFullYear();
  const m = hoje.getMonth() - dn.getMonth();
  if (m < 0 || (m === 0 && hoje.getDate() < dn.getDate())) idade--;
  out.value = idade >= 0 ? `${idade} ano(s)` : "";
}

function toggleNomePaciente() {
  const ocultar = document.getElementById("p-ocultar-nome").checked;
  const wrap = document.getElementById("wrap-nome-paciente");
  const input = document.getElementById("p-nome");
  wrap.classList.toggle("hidden", ocultar);
  input.required = !ocultar;
  if (ocultar) input.value = "";
}

function combineDateTime(dateStr, timeStr) {
  if (!dateStr) return null;
  const time = timeStr || "00:00";
  return `${dateStr}T${time}:00`;
}

function formatarDataInternacao(isoDate) {
  if (!isoDate) return "sem data";
  return App.formatDate(isoDate);
}

function resetSelectInternacoes() {
  const sel = document.getElementById("p-internacao-select");
  sel.innerHTML =
    '<option value="nova">Nova internação (informe data e setor abaixo)</option>';
  document.getElementById("p-internacao-id").value = "";
  atualizarModoInternacao();
}

function labelInternacaoOpcao(i) {
  const qtd = i.total_pareceres ?? 0;
  const pareceres =
    qtd === 0
      ? "nenhum parecer ainda"
      : `${qtd} parecer${qtd !== 1 ? "es" : ""} já registrado${qtd !== 1 ? "s" : ""}`;
  return `Internação #${i.id} — ${formatarDataInternacao(i.data_internacao)} — ${i.setor_internacao} (${pareceres})`;
}

function preencherSelectInternacoes(internacoes) {
  const sel = document.getElementById("p-internacao-select");
  const opts = internacoes.map((i) => `<option value="${i.id}">${labelInternacaoOpcao(i)}</option>`);
  sel.innerHTML =
    '<option value="nova">Nova internação (informe data e setor abaixo)</option>' + opts.join("");
}

function atualizarModoInternacao() {
  const val = document.getElementById("p-internacao-select").value;
  const wrap = document.getElementById("wrap-dados-internacao");
  const dataInt = document.getElementById("p-internacao");
  const setor = document.getElementById("p-setor");
  const hintInt = document.getElementById("p-internacao-hint");
  const nova = val === "nova";

  wrap.classList.toggle("field-readonly", !nova);
  dataInt.disabled = !nova;
  setor.disabled = !nova;
  dataInt.required = nova;
  setor.required = nova;

  if (nova) {
    hintInt.classList.add("hidden");
    hintInt.textContent = "";
    return;
  }

  const internacao = pacienteCarregado?.internacoes?.find((i) => String(i.id) === val);
  if (!internacao) {
    hintInt.classList.add("hidden");
    return;
  }

  if (internacao.data_internacao) dataInt.value = internacao.data_internacao;
  preencherSetores(internacao.setor_internacao);

  const qtd = internacao.total_pareceres ?? 0;
  hintInt.classList.remove("hidden");
  hintInt.textContent =
    qtd > 0
      ? `Será criado um novo parecer nesta internação (já existem ${qtd} parecer${qtd !== 1 ? "es" : ""}). Data e setor da internação não serão alterados.`
      : "Será criado o primeiro parecer desta internação. Data e setor da internação não serão alterados.";
}

function aplicarInternacaoSelecionada() {
  const val = document.getElementById("p-internacao-select").value;
  const hidden = document.getElementById("p-internacao-id");

  if (val === "nova" || !pacienteCarregado) {
    hidden.value = "";
    atualizarModoInternacao();
    return;
  }

  hidden.value = val;
  atualizarModoInternacao();
}

function preencherDemograficos(paciente) {
  if (paciente.data_nascimento_paciente) {
    document.getElementById("p-nascimento").value = paciente.data_nascimento_paciente;
  }
  if (paciente.sexo_paciente) {
    document.getElementById("p-sexo").value = paciente.sexo_paciente;
  }
  calcularIdade();
}

function preencherDadosPaciente(paciente, origem = "prontuario") {
  preenchimentoAutomatico = true;
  pacienteCarregado = paciente;

  const hintPront = document.getElementById("p-prontuario-hint");
  const hintNome = document.getElementById("p-nome-hint");
  hintNome.classList.add("hidden");
  hintNome.textContent = "";

  const totalPareceres = paciente.internacoes.reduce(
    (s, i) => s + (i.total_pareceres ?? 0),
    0
  );
  const msgBase = `Paciente encontrado — ${paciente.internacoes.length} internação(ões), ${totalPareceres} parecer(es). Dados demográficos preenchidos automaticamente.`;

  hintPront.classList.remove("hidden");
  if (origem === "nome") {
    hintPront.textContent = `${msgBase} Informe o número do prontuário deste parecer.`;
  } else {
    hintPront.textContent = `${msgBase} Confirme ou informe o prontuário deste parecer.`;
  }

  const ocultar = paciente.nome_oculto || paciente.nome_paciente === "Paciente oculto";
  document.getElementById("p-ocultar-nome").checked = ocultar;
  toggleNomePaciente();

  if (!ocultar && paciente.nome_paciente) {
    document.getElementById("p-nome").value = paciente.nome_paciente;
  }

  preencherDemograficos(paciente);

  preencherSelectInternacoes(paciente.internacoes);
  if (paciente.internacoes.length > 0) {
    document.getElementById("p-internacao-select").value = String(paciente.internacoes[0].id);
    aplicarInternacaoSelecionada();
  }

  preenchimentoAutomatico = false;
}

function limparDadosPaciente(limparProntuario = false) {
  pacienteCarregado = null;
  document.getElementById("p-prontuario-hint").classList.add("hidden");
  document.getElementById("p-prontuario-hint").textContent = "";
  document.getElementById("p-nome-hint").classList.add("hidden");
  document.getElementById("p-nome-hint").textContent = "";
  if (limparProntuario) document.getElementById("p-prontuario").value = "";
  resetSelectInternacoes();
  document.getElementById("p-internacao-id").value = "";
  atualizarModoInternacao();
}

async function buscarPacientePorProntuario() {
  const prontuario = document.getElementById("p-prontuario").value.trim();
  if (!prontuario) {
    limparDadosPaciente(false);
    return;
  }

  try {
    const paciente = await App.api(
      `/api/internacao/prontuario/${encodeURIComponent(prontuario)}`
    );
    preencherDadosPaciente(paciente, "prontuario");
  } catch (err) {
    if (pacienteCarregado?.numero_prontuario === prontuario) {
      limparDadosPaciente(false);
    }
    if (!err.message.includes("não encontrado")) {
      App.showModal("error", "Erro", err.message);
    }
  }
}

async function buscarPacientePorNome() {
  if (preenchimentoAutomatico) return;
  if (document.getElementById("p-ocultar-nome").checked) return;

  const nome = document.getElementById("p-nome").value.trim();
  const hintNome = document.getElementById("p-nome-hint");

  if (nome.length < 2) {
    hintNome.classList.add("hidden");
    return;
  }

  if (pacienteCarregado && pacienteCarregado.nome_paciente === nome) {
    return;
  }

  try {
    const paciente = await App.api(
      `/api/internacao/busca/nome?nome=${encodeURIComponent(nome)}`
    );
    preencherDadosPaciente(paciente, "nome");
  } catch (err) {
    hintNome.classList.remove("hidden");
    if (err.message.includes("vários pacientes")) {
      hintNome.textContent = err.message;
    } else if (err.message.includes("não encontrado")) {
      hintNome.classList.add("hidden");
    } else {
      hintNome.textContent = err.message;
    }
  }
}

function definirDataHoraPadrao() {
  const agora = new Date();
  const data = agora.toISOString().slice(0, 10);
  const hora = agora.toTimeString().slice(0, 5);
  document.getElementById("p-solicitacao-data").value = data;
  document.getElementById("p-solicitacao-hora").value = hora;
}

function resetarFormularioCompleto(user) {
  const form = document.getElementById("form-parecer");
  form.reset();

  pacienteCarregado = null;
  preenchimentoAutomatico = false;

  document.getElementById("p-internacao-id").value = "";
  document.getElementById("p-ocultar-nome").checked = false;
  document.getElementById("p-prontuario").value = "";
  document.getElementById("p-nome").value = "";
  document.getElementById("p-nascimento").value = "";
  document.getElementById("p-sexo").value = "F";
  document.getElementById("p-idade").value = "";
  document.getElementById("p-internacao").value = "";
  document.getElementById("p-resposta-data").value = "";
  document.getElementById("p-resposta-hora").value = "";
  document.getElementById("p-alta").value = "";
  document.getElementById("p-obs").value = "";

  ["p-prontuario-hint", "p-nome-hint", "p-internacao-hint"].forEach((id) => {
    const el = document.getElementById(id);
    el.classList.add("hidden");
    el.textContent = "";
  });

  resetSelectInternacoes();
  preencherSetores();
  document.getElementById("p-tipo-alta").value = "";
  definirDataHoraPadrao();
  toggleNomePaciente();
  atualizarModoInternacao();

  if (user) {
    document.getElementById("p-aluno").value = user.nome || user.email;
  }

  App.initCharCounters(form);
}

document.addEventListener("DOMContentLoaded", async () => {
  const form = document.getElementById("form-parecer");
  App.initCharCounters(form);

  const user = App.getUser();
  if (user) document.getElementById("p-aluno").value = user.nome || user.email;

  preencherSetores();
  definirDataHoraPadrao();
  atualizarModoInternacao();

  document.getElementById("p-ocultar-nome").addEventListener("change", toggleNomePaciente);
  document.getElementById("p-nascimento").addEventListener("change", calcularIdade);
  document.getElementById("p-nascimento").addEventListener("input", calcularIdade);
  document.getElementById("p-prontuario").addEventListener("blur", buscarPacientePorProntuario);
  document.getElementById("p-nome").addEventListener("blur", buscarPacientePorNome);
  document
    .getElementById("p-internacao-select")
    .addEventListener("change", aplicarInternacaoSelecionada);

  try {
    await carregarTiposAlta();
  } catch {
    /* tipos de alta opcionais */
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const ocultar = document.getElementById("p-ocultar-nome").checked;
    const tipoAlta = document.getElementById("p-tipo-alta").value;
    const selectVal = document.getElementById("p-internacao-select").value;
    const respostaData = document.getElementById("p-resposta-data").value;
    const respostaHora = document.getElementById("p-resposta-hora").value;

    let internacaoId = null;
    if (selectVal !== "nova") {
      const parsed = parseInt(selectVal, 10);
      if (!Number.isNaN(parsed)) internacaoId = parsed;
    }

    const body = {
      numero_prontuario: document.getElementById("p-prontuario").value.trim(),
      internacao_id: internacaoId,
      nome_paciente: ocultar ? null : document.getElementById("p-nome").value.trim(),
      ocultar_nome_paciente: ocultar,
      data_nascimento_paciente: document.getElementById("p-nascimento").value,
      sexo_paciente: document.getElementById("p-sexo").value,
      data_internacao: document.getElementById("p-internacao").value,
      setor_internacao: document.getElementById("p-setor").value,
      data_solicitacao_parecer: combineDateTime(
        document.getElementById("p-solicitacao-data").value,
        document.getElementById("p-solicitacao-hora").value
      ),
      data_parecer:
        respostaData && respostaHora
          ? combineDateTime(respostaData, respostaHora)
          : respostaData
            ? combineDateTime(respostaData, "00:00")
            : null,
      data_alta: document.getElementById("p-alta").value || null,
      tipo_alta_id: tipoAlta ? parseInt(tipoAlta, 10) : null,
      observacoes_gerais: document.getElementById("p-obs").value.trim() || null,
    };

    try {
      await App.api("/api/parecer/completo", { method: "POST", body });
      resetarFormularioCompleto(user);
      App.showModal("success", "Sucesso", "Parecer enviado e salvo com sucesso.");
    } catch (err) {
      App.showModal("error", "Erro", err.message);
    }
  });
});
