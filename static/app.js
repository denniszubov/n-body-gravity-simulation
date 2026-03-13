/* ── N-Body Gravity Simulation ─────────────────────────── */

const canvas = document.getElementById("sim-canvas");
const ctx = canvas.getContext("2d");

// ── State ──────────────────────────────────────────────

let presets = [];
let activePreset = null;
let positions = [];
let masses = [];
let viewRange = 8.0;
let running = false;
let pollTimer = null;
let simTime = 0;
let pendingRequest = false;

// ── DOM refs ───────────────────────────────────────────

const els = {
  preset: document.getElementById("preset-select"),
  nBodies: document.getElementById("n-bodies"),
  nBodiesGroup: document.getElementById("n-bodies-group"),
  seed: document.getElementById("seed"),
  dt: document.getElementById("dt"),
  stepsPerFrame: document.getElementById("steps-per-frame"),
  btnStart: document.getElementById("btn-start"),
  btnPause: document.getElementById("btn-pause"),
  btnReset: document.getElementById("btn-reset"),
  indicator: document.getElementById("status-indicator"),
  statTime: document.getElementById("stat-time"),
  statBodies: document.getElementById("stat-bodies"),
  statSps: document.getElementById("stat-sps"),
  statStepTime: document.getElementById("stat-step-time"),
  statKe: document.getElementById("stat-ke"),
  statPe: document.getElementById("stat-pe"),
  statTotalE: document.getElementById("stat-total-e"),
  statInitialE: document.getElementById("stat-initial-e"),
  energyDrift: document.getElementById("energy-drift"),
};

// ── API helpers ────────────────────────────────────────

async function api(method, path, body) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (body !== undefined) opts.body = JSON.stringify(body);
  const res = await fetch(path, opts);
  if (!res.ok) throw new Error(`API ${path}: ${res.status}`);
  return res.json();
}

// ── Canvas sizing ──────────────────────────────────────

function resizeCanvas() {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = window.innerWidth * dpr;
  canvas.height = window.innerHeight * dpr;
  canvas.style.width = window.innerWidth + "px";
  canvas.style.height = window.innerHeight + "px";
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();

// ── World → Screen transform ───────────────────────────

function worldToScreen(wx, wy) {
  const cw = window.innerWidth;
  const ch = window.innerHeight;
  const panelOffset = window.innerWidth > 640 ? 280 : 0;
  const drawW = cw - panelOffset;
  const drawH = ch;
  const cx = panelOffset + drawW / 2;
  const cy = drawH / 2;
  const scale = Math.min(drawW, drawH) / (2 * viewRange);
  return [cx + wx * scale, cy - wy * scale];
}

// ── Particle rendering ─────────────────────────────────

function particleRadius(mass) {
  // Log scale: heavy bodies bigger, light bodies still visible
  return Math.max(1.5, Math.min(12, 1.5 + Math.log10(mass + 1) * 3.5));
}

function particleColor(mass, maxMass) {
  // Heavy bodies glow warm white, light bodies cool blue
  const t = Math.log10(mass + 1) / Math.log10(maxMass + 1);
  const r = Math.round(140 + t * 115);
  const g = Math.round(180 + t * 75);
  const b = Math.round(230 + t * 25);
  return `rgb(${r},${g},${b})`;
}

function drawParticles() {
  const cw = window.innerWidth;
  const ch = window.innerHeight;

  // Clear with deep black
  ctx.fillStyle = "#000000";
  ctx.fillRect(0, 0, cw, ch);

  if (positions.length === 0) return;

  const maxMass = Math.max(...masses);

  // Draw glow layer first (back to front: heaviest last)
  for (let i = 0; i < positions.length; i++) {
    const [wx, wy] = positions[i];
    const [sx, sy] = worldToScreen(wx, wy);
    const m = masses[i];
    const r = particleRadius(m);
    const glowR = r * 4;
    const color = particleColor(m, maxMass);

    // Outer glow
    const glow = ctx.createRadialGradient(sx, sy, 0, sx, sy, glowR);
    glow.addColorStop(0, color.replace("rgb", "rgba").replace(")", ",0.25)"));
    glow.addColorStop(0.4, color.replace("rgb", "rgba").replace(")", ",0.06)"));
    glow.addColorStop(1, "rgba(0,0,0,0)");

    ctx.beginPath();
    ctx.arc(sx, sy, glowR, 0, Math.PI * 2);
    ctx.fillStyle = glow;
    ctx.fill();
  }

  // Draw solid cores
  for (let i = 0; i < positions.length; i++) {
    const [wx, wy] = positions[i];
    const [sx, sy] = worldToScreen(wx, wy);
    const m = masses[i];
    const r = particleRadius(m);
    const color = particleColor(m, maxMass);

    // Bright core
    const core = ctx.createRadialGradient(sx, sy, 0, sx, sy, r);
    core.addColorStop(0, "#ffffff");
    core.addColorStop(0.3, color);
    core.addColorStop(1, color.replace("rgb", "rgba").replace(")", ",0.4)"));

    ctx.beginPath();
    ctx.arc(sx, sy, r, 0, Math.PI * 2);
    ctx.fillStyle = core;
    ctx.fill();
  }
}

// ── Animation loop ─────────────────────────────────────

function renderLoop() {
  drawParticles();
  requestAnimationFrame(renderLoop);
}

requestAnimationFrame(renderLoop);

// ── State update ───────────────────────────────────────

function updateStats(state) {
  simTime = state.t;
  positions = state.positions;
  masses = state.masses;

  els.statTime.textContent = state.t.toFixed(4);
  els.statBodies.textContent = state.n;

  if (state.step_time_ms > 0) {
    const dt = parseFloat(els.dt.value) || 0.005;
    const spf = parseInt(els.stepsPerFrame.value) || 6;
    const sps = (spf / (state.step_time_ms / 1000)).toFixed(0);
    els.statSps.textContent = sps;
    els.statStepTime.textContent = state.step_time_ms.toFixed(2) + " ms";
  }

  els.statKe.textContent = state.energy.kinetic.toFixed(4);
  els.statPe.textContent = state.energy.potential.toFixed(4);
  els.statTotalE.textContent = state.energy.total.toFixed(4);
  els.statInitialE.textContent = state.initial_energy.toFixed(4);

  const driftStr = state.relative_drift.toExponential(2);
  els.energyDrift.textContent = "Δ " + driftStr;
  els.energyDrift.classList.toggle("warn", state.relative_drift > 1e-4);
}

// ── Polling ────────────────────────────────────────────

function startPolling() {
  if (pollTimer) return;
  pollTimer = setInterval(async () => {
    if (pendingRequest) return; // skip if previous request still in-flight
    pendingRequest = true;
    try {
      const dt = parseFloat(els.dt.value) || 0.005;
      const nSteps = parseInt(els.stepsPerFrame.value) || 6;
      const state = await api("POST", "/api/sim/step", { dt, n_steps: nSteps });
      updateStats(state);
    } catch (e) {
      console.error("Step failed:", e);
      stopPolling();
    } finally {
      pendingRequest = false;
    }
  }, 50);
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
}

// ── UI state ───────────────────────────────────────────

function setRunning(val) {
  running = val;
  els.btnStart.disabled = val;
  els.btnPause.disabled = !val;
  els.indicator.className = "panel-indicator" + (val ? " running" : simTime > 0 ? " paused" : "");
  els.indicator.querySelector(".indicator-label").textContent = val ? "RUNNING" : simTime > 0 ? "PAUSED" : "IDLE";
}

// ── Create simulation ──────────────────────────────────

async function createSim() {
  stopPolling();
  setRunning(false);

  const presetName = els.preset.value;
  activePreset = presets.find((p) => p.name === presetName);
  viewRange = activePreset ? activePreset.view_range : 8.0;

  const body = {
    preset: presetName,
    n_bodies: parseInt(els.nBodies.value) || 200,
    seed: parseInt(els.seed.value) || 42,
  };

  try {
    const state = await api("POST", "/api/sim/create", body);
    updateStats(state);
  } catch (e) {
    console.error("Create failed:", e);
  }
}

// ── Preset UI toggle ───────────────────────────────────

function updatePresetUI() {
  const p = presets.find((p) => p.name === els.preset.value);
  els.nBodiesGroup.style.display = p && p.has_n_bodies ? "block" : "none";
}

// ── Init ───────────────────────────────────────────────

async function init() {
  try {
    presets = await api("GET", "/api/presets");
  } catch (e) {
    console.error("Failed to load presets:", e);
    return;
  }

  // Populate dropdown
  els.preset.innerHTML = "";
  for (const p of presets) {
    const opt = document.createElement("option");
    opt.value = p.name;
    opt.textContent = p.label;
    els.preset.appendChild(opt);
  }

  updatePresetUI();
  await createSim();
}

// ── Event listeners ────────────────────────────────────

els.preset.addEventListener("change", () => {
  updatePresetUI();
  createSim();
});

els.btnStart.addEventListener("click", () => {
  setRunning(true);
  startPolling();
});

els.btnPause.addEventListener("click", () => {
  setRunning(false);
  stopPolling();
});

els.btnReset.addEventListener("click", () => {
  createSim();
});

// ── Go ─────────────────────────────────────────────────

init();
