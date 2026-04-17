const slides = Array.from(document.querySelectorAll(".slide"));
const slideIndicator = document.getElementById("slide-indicator");
const progressBar = document.getElementById("progress-bar");

let currentSlide = 0;
let currentLang = "lang-both";
let overviewOpen = false;

function updateDeck(index) {
  currentSlide = Math.max(0, Math.min(index, slides.length - 1));

  slides.forEach((slide, i) => {
    const isActive = i === currentSlide;
    slide.classList.toggle("active", isActive);
    slide.setAttribute("aria-hidden", !isActive);
  });

  slideIndicator.textContent =
    `${String(currentSlide + 1).padStart(2, "0")} / ${String(slides.length).padStart(2, "0")}`;
  progressBar.style.width = `${((currentSlide + 1) / slides.length) * 100}%`;
  syncCanvasAnimation();
}

function nextSlide() {
  updateDeck(currentSlide + 1);
}

function prevSlide() {
  updateDeck(currentSlide - 1);
}

document.addEventListener("keydown", (event) => {
  if (overviewOpen && event.key === "Escape") {
    toggleOverview(false);
    return;
  }

  if (overviewOpen) return;

  if (event.key === "ArrowRight" || event.key === "PageDown" || event.key === " ") {
    event.preventDefault();
    nextSlide();
  }

  if (event.key === "ArrowLeft" || event.key === "PageUp") {
    event.preventDefault();
    prevSlide();
  }

  if (event.key === "Home") {
    event.preventDefault();
    updateDeck(0);
  }

  if (event.key === "End") {
    event.preventDefault();
    updateDeck(slides.length - 1);
  }

  if (event.key.toLowerCase() === "f") {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  }

  if (event.key.toLowerCase() === "o") {
    toggleOverview();
  }
});

slides.forEach((slide, index) => {
  slide.addEventListener("click", () => {
    if (!overviewOpen && index === currentSlide) {
      nextSlide();
    }
  });
});

let touchStartX = 0;
let touchStartY = 0;

document.addEventListener("touchstart", (e) => {
  touchStartX = e.changedTouches[0].screenX;
  touchStartY = e.changedTouches[0].screenY;
}, { passive: true });

document.addEventListener("touchend", (e) => {
  if (overviewOpen) return;
  const dx = e.changedTouches[0].screenX - touchStartX;
  const dy = e.changedTouches[0].screenY - touchStartY;

  if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) {
    if (dx < 0) nextSlide();
    else prevSlide();
  }
}, { passive: true });

const overviewEl = document.getElementById("slide-overview");
const overviewGrid = document.getElementById("overview-grid");

function overviewTitle(slide) {
  const zh = slide.dataset.title || "";
  const en = slide.dataset.titleEn || "";

  if (currentLang === "lang-zh") return zh;
  if (currentLang === "lang-en") return en;
  return `${zh}<br><span style="opacity:.66;font-size:.88em;">${en}</span>`;
}

function buildOverview() {
  overviewGrid.innerHTML = "";
  slides.forEach((slide, i) => {
    const thumb = document.createElement("button");
    thumb.className = "overview-thumb" + (i === currentSlide ? " active" : "");
    thumb.innerHTML =
      `<span class="thumb-number">${String(i + 1).padStart(2, "0")}</span>` +
      `<span class="thumb-title">${overviewTitle(slide)}</span>`;
    thumb.addEventListener("click", () => {
      updateDeck(i);
      toggleOverview(false);
    });
    overviewGrid.appendChild(thumb);
  });
}

function toggleOverview(forceState) {
  overviewOpen = forceState !== undefined ? forceState : !overviewOpen;

  if (overviewOpen) {
    buildOverview();
    overviewEl.classList.remove("hidden");
    overviewEl.setAttribute("aria-hidden", "false");
  } else {
    overviewEl.classList.add("hidden");
    overviewEl.setAttribute("aria-hidden", "true");
  }
}

const langModes = ["lang-both", "lang-zh", "lang-en"];
const langLabels = { "lang-both": "双语", "lang-zh": "中文", "lang-en": "EN" };
const langBtn = document.getElementById("lang-toggle");

function setLang(mode) {
  document.body.classList.remove(...langModes);
  document.body.classList.add(mode);
  currentLang = mode;
  if (langBtn) langBtn.textContent = langLabels[mode];
  drawAllStaticCanvases();
  if (overviewOpen) buildOverview();
}

if (langBtn) {
  langBtn.addEventListener("click", () => {
    const idx = (langModes.indexOf(currentLang) + 1) % langModes.length;
    setLang(langModes[idx]);
  });
}

function renderMath() {
  if (typeof renderMathInElement !== "undefined") {
    renderMathInElement(document.body, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false }
      ],
      ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]
    });
  }

  document.querySelectorAll(".math").forEach((el) => {
    if (el.dataset.rendered) return;
    try {
      katex.render(el.textContent, el, { throwOnError: false, displayMode: false });
      el.dataset.rendered = "1";
    } catch (_) {}
  });
}

function setupCanvasDPI(canvas, ctx) {
  if (!canvas || !ctx) return;
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  if (!rect.width || !rect.height) return;
  canvas.width = Math.round(rect.width * dpr);
  canvas.height = Math.round(rect.height * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function canvasRect(canvas) {
  const rect = canvas.getBoundingClientRect();
  return {
    w: rect.width || 980,
    h: rect.height || 460
  };
}

const waveCanvas = document.getElementById("wave-canvas");
const waveCtx = waveCanvas ? waveCanvas.getContext("2d") : null;
const beatCanvas = document.getElementById("beat-canvas");
const beatCtx = beatCanvas ? beatCanvas.getContext("2d") : null;

const waveSlideIndex = waveCanvas ? slides.indexOf(waveCanvas.closest(".slide")) : -1;
const beatSlideIndex = beatCanvas ? slides.indexOf(beatCanvas.closest(".slide")) : -1;

let waveFrameId = null;
let beatFrameId = null;
let waveTime = 0;
let beatTime = 0;

function drawWaveCanvasFrame() {
  if (!waveCanvas || !waveCtx) return;
  const { w, h } = canvasRect(waveCanvas);
  const ctx = waveCtx;

  ctx.clearRect(0, 0, w, h);

  const bg = ctx.createLinearGradient(0, 0, w, h);
  bg.addColorStop(0, "#0b1622");
  bg.addColorStop(1, "#09121d");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, w, h);

  ctx.strokeStyle = "rgba(255,255,255,0.05)";
  ctx.lineWidth = 1;
  for (let x = 0; x < w; x += 70) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, h);
    ctx.stroke();
  }

  const axisY = h * 0.52;
  ctx.strokeStyle = "rgba(242,226,198,0.22)";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(42, axisY);
  ctx.lineTo(w - 36, axisY);
  ctx.stroke();

  /* Im[ψ] = sin(kx - ωt) — gold/warm color */
  ctx.strokeStyle = "rgba(239,171,86,0.55)";
  ctx.lineWidth = 3;
  ctx.setLineDash([8, 6]);
  ctx.beginPath();
  for (let x = 40; x <= w - 40; x += 2) {
    const phase = (x / 72) - waveTime;
    const y = axisY - Math.sin(phase) * (h * 0.18);
    if (x === 40) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();
  ctx.setLineDash([]);

  /* Re[ψ] = cos(kx - ωt) — cyan */
  ctx.strokeStyle = "#7dc0ce";
  ctx.lineWidth = 4;
  ctx.beginPath();
  for (let x = 40; x <= w - 40; x += 2) {
    const phase = (x / 72) - waveTime;
    const y = axisY - Math.cos(phase) * (h * 0.18);
    if (x === 40) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();

  ctx.fillStyle = "rgba(239,171,86,0.95)";
  for (let i = 0; i < 6; i += 1) {
    const x = 92 + i * ((w - 180) / 5);
    const y = axisY - Math.cos((x / 72) - waveTime) * (h * 0.18);
    ctx.beginPath();
    ctx.arc(x, y, 4.5, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.font = "18px 'IBM Plex Sans', sans-serif";

  /* Legend: Re (solid cyan), Im (dashed gold) */
  ctx.fillStyle = "#7dc0ce";
  ctx.fillText("── Re[ψ]", 42, 30);
  ctx.fillStyle = "rgba(239,171,86,0.75)";
  ctx.fillText("╌╌ Im[ψ]", 42, 54);

  ctx.fillStyle = "rgba(192,201,211,0.92)";
  if (currentLang === "lang-en") {
    ctx.fillText("ψ(x,t) = A eⁱ⁽ᵏˣ⁻ωᵗ⁾", w - 260, 36);
    ctx.fillText("traveling wave", w - 176, axisY - h * 0.22);
  } else if (currentLang === "lang-zh") {
    ctx.fillText("ψ(x,t) = A eⁱ⁽ᵏˣ⁻ωᵗ⁾", w - 260, 36);
    ctx.fillText("行波", w - 86, axisY - h * 0.22);
  } else {
    ctx.fillText("ψ(x,t) = A eⁱ⁽ᵏˣ⁻ωᵗ⁾", w - 260, 36);
    ctx.fillText("行波 / traveling wave", w - 220, axisY - h * 0.22);
  }
}

function animateWaveCanvas() {
  if (currentSlide !== waveSlideIndex) {
    waveFrameId = null;
    return;
  }
  waveTime += 0.045;
  drawWaveCanvasFrame();
  waveFrameId = requestAnimationFrame(animateWaveCanvas);
}

function phi1(x, L) {
  return Math.sqrt(2 / L) * Math.sin(Math.PI * x / L);
}

function phi2(x, L) {
  return Math.sqrt(2 / L) * Math.sin(2 * Math.PI * x / L);
}

function drawBeatCanvasFrame() {
  if (!beatCanvas || !beatCtx) return;
  const { w, h } = canvasRect(beatCanvas);
  const ctx = beatCtx;
  const L = 1;
  /* Beat frequency δ = (E₂ - E₁)/ℏ in animation units.
     Coefficients are c₁ = c₂ = 1/√2, so:
     |ψ|² = (φ₁² + φ₂²)/2 + φ₁φ₂ cos(δt) */
  const delta = 1.75;

  ctx.clearRect(0, 0, w, h);

  const bg = ctx.createLinearGradient(0, 0, w, h);
  bg.addColorStop(0, "#0b1622");
  bg.addColorStop(1, "#09121d");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, w, h);

  const left = 90;
  const right = w - 90;
  const bottom = h - 80;
  const top = 72;
  const axisY = bottom;

  ctx.strokeStyle = "rgba(242,226,198,0.22)";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(left, axisY);
  ctx.lineTo(right, axisY);
  ctx.stroke();

  ctx.strokeStyle = "#efab56";
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(left, top);
  ctx.lineTo(left, bottom);
  ctx.lineTo(right, bottom);
  ctx.lineTo(right, top);
  ctx.stroke();

  ctx.strokeStyle = "#7dc0ce";
  ctx.lineWidth = 4;
  ctx.beginPath();
  for (let i = 0; i <= 420; i += 1) {
    const xNorm = i / 420;
    const x = xNorm * L;
    const amp = (phi1(x, L) ** 2 + phi2(x, L) ** 2) / 2 + phi1(x, L) * phi2(x, L) * Math.cos(beatTime * delta);
    const px = left + xNorm * (right - left);
    const py = bottom - amp * 120;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();

  ctx.fillStyle = "rgba(192,201,211,0.92)";
  ctx.font = "18px 'IBM Plex Sans', sans-serif";
  if (currentLang === "lang-en") {
    ctx.fillText("|ψ(x,t)|² for c₁φ₁ + c₂φ₂", 36, 40);
    ctx.fillText("phase difference drives oscillation", w - 280, 40);
  } else if (currentLang === "lang-zh") {
    ctx.fillText("|ψ(x,t)|²：两个定态叠加后的概率密度", 36, 40);
    ctx.fillText("相位差驱动振荡", w - 160, 40);
  } else {
    ctx.fillText("|ψ(x,t)|²：叠加态概率密度 / superposed probability density", 36, 40);
  }
}

function animateBeatCanvas() {
  if (currentSlide !== beatSlideIndex) {
    beatFrameId = null;
    return;
  }
  beatTime += 0.035;
  drawBeatCanvasFrame();
  beatFrameId = requestAnimationFrame(animateBeatCanvas);
}

function drawAllStaticCanvases() {
  if (waveCanvas) {
    setupCanvasDPI(waveCanvas, waveCtx);
    drawWaveCanvasFrame();
  }
  if (beatCanvas) {
    setupCanvasDPI(beatCanvas, beatCtx);
    drawBeatCanvasFrame();
  }
}

function syncCanvasAnimation() {
  if (waveCanvas) {
    if (currentSlide === waveSlideIndex) {
      setupCanvasDPI(waveCanvas, waveCtx);
      if (waveFrameId === null) animateWaveCanvas();
    } else if (waveFrameId !== null) {
      cancelAnimationFrame(waveFrameId);
      waveFrameId = null;
      drawWaveCanvasFrame();
    }
  }

  if (beatCanvas) {
    if (currentSlide === beatSlideIndex) {
      setupCanvasDPI(beatCanvas, beatCtx);
      if (beatFrameId === null) animateBeatCanvas();
    } else if (beatFrameId !== null) {
      cancelAnimationFrame(beatFrameId);
      beatFrameId = null;
      drawBeatCanvasFrame();
    }
  }
}

/* Debounce resize to avoid excessive redraws during window dragging */
let resizeTimer;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    drawAllStaticCanvases();
    syncCanvasAnimation();
  }, 100);
});

updateDeck(0);
drawAllStaticCanvases();

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", renderMath);
} else {
  setTimeout(renderMath, 100);
}
