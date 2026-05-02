const $ = (selector) => document.querySelector(selector);

const state = {
  path: "",
  detected: null,
  lastState: null,
  profiles: [],
  defaultProfile: "rtx5080m",
};

function toast(message, isError = false) {
  const node = $("#toast");
  node.textContent = message;
  node.style.borderColor = isError ? "var(--danger)" : "var(--line)";
  node.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => node.classList.remove("show"), 4200);
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok || data.ok === false) {
    throw new Error(data.error || `HTTP ${response.status}`);
  }
  return data;
}

function setBusy(button, busy, text) {
  if (!button) return;
  if (busy) {
    button.dataset.oldText = button.textContent;
    button.textContent = text || "Procesando...";
    button.disabled = true;
  } else {
    button.textContent = button.dataset.oldText || button.textContent;
    button.disabled = false;
  }
}

function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  localStorage.setItem("nte-rt-theme", theme);
  $("#themeToggle").textContent = theme === "dark" ? "Oscuro" : "Claro";
}

function currentMode() {
  return document.querySelector("input[name='mode']:checked")?.value || "dxgi";
}

function currentProfile() {
  return document.querySelector("input[name='profile']:checked")?.value || state.defaultProfile || "rtx5080m";
}

function processText(processes) {
  if (!processes || processes.length === 0) return "Ninguno activo";
  const names = [...new Set(processes.map((item) => item.ProcessName || item.processName).filter(Boolean))];
  return names.join(", ");
}

function findProfileByInstall(install) {
  const ini = install?.optScalerIni || {};
  const deviceId = (ini.SpoofedDeviceId || "").toLowerCase();
  const gpuName = (ini.SpoofedGPUName || "").toLowerCase();
  return state.profiles.find((profile) => (
    (profile.deviceId || "").toLowerCase() === deviceId ||
    (profile.gpuName || "").toLowerCase() === gpuName
  ));
}

function setProfileSelection(profileId) {
  const input = document.querySelector(`input[name='profile'][value='${profileId}']`);
  if (input) input.checked = true;
  const selected = state.profiles.find((profile) => profile.id === currentProfile());
  $("#profileBadge").textContent = selected ? selected.label : "GPU objetivo";
}

function renderProfiles(profiles, defaultProfile) {
  if (!Array.isArray(profiles) || profiles.length === 0) return;
  const selectedBefore = currentProfile();
  state.profiles = profiles;
  state.defaultProfile = defaultProfile || state.defaultProfile;
  const selectedId = profiles.some((profile) => profile.id === selectedBefore) ? selectedBefore : state.defaultProfile;
  const grid = $("#profileGrid");
  grid.innerHTML = "";
  profiles.forEach((profile) => {
    const label = document.createElement("label");
    label.className = "profile-option";
    const checked = profile.id === selectedId ? "checked" : "";
    label.innerHTML = `
      <input type="radio" name="profile" value="${profile.id}" ${checked} />
      <span>
        <strong>${profile.label}</strong>
        <small>${profile.gpuName} / ${profile.deviceId}</small>
      </span>
    `;
    label.querySelector("input").addEventListener("change", () => setProfileSelection(profile.id));
    grid.appendChild(label);
  });
  setProfileSelection(document.querySelector("input[name='profile']:checked")?.value || selectedId);
}

function updateHero(install) {
  const installed = install?.installed;
  $("#statusGlyph").textContent = installed ? "Activo" : "Pendiente";
  $("#statusLine").textContent = installed
    ? "Desbloqueo de ray tracing instalado"
    : "Desbloqueo de ray tracing no instalado";
  $("#installBadge").textContent = installed ? "Instalado" : "No instalado";
}

function updateDetected(detected) {
  state.detected = detected;
  if (!detected) return;
  state.path = detected.win64;
  $("#gamePath").value = detected.win64;
  $("#pathHint").textContent = `HTGame.exe: ${detected.exe}`;
  updateHero(detected.install);
  renderInstallState(detected.install);
  const installedProfile = findProfileByInstall(detected.install);
  if (installedProfile) setProfileSelection(installedProfile.id);
  renderBackups(detected.backups || []);
}

function renderBackups(backups) {
  const select = $("#backupSelect");
  select.innerHTML = "";
  $("#backupCount").textContent = `${backups.length} respaldo(s)`;
  $("#openBackupBtn").disabled = backups.length === 0;
  if (backups.length === 0) {
    const option = document.createElement("option");
    option.textContent = "Sin respaldos";
    option.value = "";
    select.appendChild(option);
    return;
  }
  backups.forEach((backup) => {
    const option = document.createElement("option");
    option.value = backup.id;
    option.textContent = `${backup.id} / ${backup.mode || "unknown"} / ${backup.profile || "perfil"}`;
    option.dataset.path = backup.path;
    select.appendChild(option);
  });
}

function renderInstallState(install) {
  if (!install) {
    $("#installState").textContent = "No detectado.";
    return;
  }
  const lines = [
    `installed: ${install.installed}`,
    `winmm: ${install.winmm ? `${install.winmm.size} bytes, optiscaler=${install.winmm.looksLikeOptiScaler}` : "no encontrado"}`,
    `OptiScaler dir: ${install.optScalerDirExists}`,
    `DLSSTweaks (legacy): ${install.legacyDlsstweaksIni}`,
    "",
    "[OptiScaler.ini]",
  ];
  const ini = install.optScalerIni || {};
  Object.keys(ini).sort().forEach((key) => lines.push(`${key}=${ini[key]}`));
  const matched = findProfileByInstall(install);
  if (matched) {
    lines.splice(4, 0, `perfil detectado: ${matched.label}`);
  }
  $("#installState").textContent = lines.join("\n");
}

function updateStateView(data) {
  state.lastState = data;
  renderProfiles(data.profiles || [], data.defaultProfile);
  $("#versionText").textContent = data.version || "0.1.0";
  if (data.name) document.title = `${data.name} / ${data.englishName || "NTE Ray Tracing Panel"}`;
  const gpu = data.nvidia?.[0];
  $("#gpuName").textContent = gpu
    ? `${gpu.Name} (${gpu.DeviceIdHex || "unknown"})`
    : "NVIDIA no detectada";
  $("#procmonState").textContent = data.procmon?.present ? "Residuo detectado" : "Limpio";
  $("#processState").textContent = processText(data.processes || []);
  $("#optiBadge").textContent = data.optiscaler ? `Preparado ${data.optiscaler.tag}` : "No preparado";
  if (data.selectedDetected && !data.selectedDetected.error) {
    updateDetected(data.selectedDetected);
  } else if (data.commonDetected) {
    updateDetected(data.commonDetected);
  } else {
    updateHero(null);
  }
}

async function refreshState() {
  const path = $("#gamePath").value.trim();
  const url = path ? `/api/state?path=${encodeURIComponent(path)}` : "/api/state";
  const data = await api(url);
  updateStateView(data);
}

async function detectGame() {
  const button = $("#detectBtn");
  setBusy(button, true, "Detectando...");
  try {
    const data = await api("/api/detect", {
      method: "POST",
      body: JSON.stringify({ path: $("#gamePath").value.trim() }),
    });
    updateDetected(data.detected);
    toast("Directorio Win64 del juego detectado.");
  } catch (error) {
    toast(error.message, true);
  } finally {
    setBusy(button, false);
  }
}

async function browseGame() {
  const button = $("#browseBtn");
  setBusy(button, true, "Abriendo...");
  try {
    const data = await api("/api/browse", { method: "POST", body: "{}" });
    if (data.path) {
      $("#gamePath").value = data.path;
      await detectGame();
    }
  } catch (error) {
    toast(error.message, true);
  } finally {
    setBusy(button, false);
  }
}

async function downloadOpti(force = false) {
  const button = force ? $("#forceDownloadBtn") : $("#downloadBtn");
  setBusy(button, true, force ? "Redescargando..." : "Descargando...");
  try {
    const data = await api("/api/download", {
      method: "POST",
      body: JSON.stringify({ force }),
    });
    $("#optiBadge").textContent = `Preparado ${data.optiscaler.tag}`;
    toast(data.optiscaler.downloaded ? "OptiScaler descargado y extraído." : "OptiScaler ya estaba preparado.");
    await refreshState();
  } catch (error) {
    toast(error.message, true);
  } finally {
    setBusy(button, false);
  }
}

async function installSpoof() {
  const button = $("#installBtn");
  setBusy(button, true, "Instalando...");
  try {
    const data = await api("/api/install", {
      method: "POST",
      body: JSON.stringify({
        path: $("#gamePath").value.trim(),
        mode: currentMode(),
        profile: currentProfile(),
        closeGame: $("#closeGame").checked,
      }),
    });
    updateDetected(data.detected);
    toast(`Instalación completada. Respaldo creado: ${data.backup}`);
  } catch (error) {
    toast(error.message, true);
  } finally {
    setBusy(button, false);
  }
}

async function restoreBackup() {
  const button = $("#restoreBtn");
  const backup = $("#backupSelect").value;
  if (!backup) {
    toast("No hay respaldos disponibles.", true);
    return;
  }
  setBusy(button, true, "Restaurando...");
  try {
    const data = await api("/api/restore", {
      method: "POST",
      body: JSON.stringify({
        path: $("#gamePath").value.trim(),
        backup,
        closeGame: $("#closeGame").checked,
      }),
    });
    updateDetected(data.detected);
    toast(data.message);
  } catch (error) {
    toast(error.message, true);
  } finally {
    setBusy(button, false);
  }
}

async function refreshLog() {
  const button = $("#logBtn");
  setBusy(button, true, "Leyendo...");
  try {
    const path = encodeURIComponent($("#gamePath").value.trim());
    const data = await api(`/api/log?path=${path}`);
    $("#logView").textContent = data.log.exists
      ? data.log.tail || "El registro está vacío."
      : "Aún no se ha generado OptiScaler.log.";
  } catch (error) {
    toast(error.message, true);
  } finally {
    setBusy(button, false);
  }
}

async function shutdown() {
  try {
    await api("/api/shutdown", { method: "POST", body: "{}" });
    toast("El servicio backend se está cerrando.");
  } catch (error) {
    toast(error.message, true);
  }
}

function bindNav() {
  const links = [...document.querySelectorAll(".nav a")];
  links.forEach((link) => {
    link.addEventListener("click", () => {
      links.forEach((item) => item.classList.remove("active"));
      link.classList.add("active");
    });
  });
}

function bindEvents() {
  $("#themeToggle").addEventListener("click", () => {
    setTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
  });
  $("#browseBtn").addEventListener("click", browseGame);
  $("#detectBtn").addEventListener("click", detectGame);
  $("#refreshBtn").addEventListener("click", () => refreshState().catch((error) => toast(error.message, true)));
  $("#downloadBtn").addEventListener("click", () => downloadOpti(false));
  $("#forceDownloadBtn").addEventListener("click", () => downloadOpti(true));
  $("#installBtn").addEventListener("click", installSpoof);
  $("#restoreBtn").addEventListener("click", restoreBackup);
  $("#logBtn").addEventListener("click", refreshLog);
  $("#shutdownBtn").addEventListener("click", shutdown);
  $("#shutdownBtnTop").addEventListener("click", shutdown);
  $("#openBackupBtn").addEventListener("click", () => {
    const selected = $("#backupSelect").selectedOptions[0];
    toast(selected?.dataset.path || "Sin ruta de respaldo.");
  });
}

function init() {
  setTheme(localStorage.getItem("nte-rt-theme") || "light");
  bindNav();
  bindEvents();
  refreshState().catch((error) => toast(error.message, true));
}

init();
