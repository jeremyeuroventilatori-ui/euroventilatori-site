/* JS commun à toutes les pages : le souffle (canvas d'air ambiant), thème,
   menu mobile, parallaxe légère, révélation au défilement.
   index.html embarque en plus ses scripts propres (hero centrifuge, pupitre). */
(function () {
"use strict";
var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
var root = document.documentElement;
function tok(n){ return getComputedStyle(root).getPropertyValue(n).trim(); }

/* ---------- thème ---------- */
var themeBtn = document.getElementById("themeBtn");
if (themeBtn) themeBtn.addEventListener("click", function () {
  var dark = root.getAttribute("data-theme") === "dark" ||
    (!root.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
  root.setAttribute("data-theme", dark ? "light" : "dark");
});

/* ---------- menu mobile ---------- */
var burger = document.getElementById("burger"), nav = document.getElementById("mainNav");
if (burger && nav) {
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });
  nav.addEventListener("click", function (e) {
    if (e.target.tagName === "A") { nav.classList.remove("open"); burger.setAttribute("aria-expanded", "false"); }
  });
}

/* ============================================================
   LE SOUFFLE — nappe d'air qui traverse toutes les pages.
   Filets laminaires ondulants ; le défilement crée une rafale
   (l'air accélère, s'étire, puis retrouve son régime de croisière).
   ============================================================ */
var air = document.getElementById("airCanvas");
if (air) {
  var ax = air.getContext("2d"), DPR = Math.min(devicePixelRatio || 1, 2);
  var W = 0, H = 0, lines = [], gust = 0, lastY = scrollY, t = 0;

  function seedLines() {
    W = air.clientWidth; H = air.clientHeight;
    air.width = W * DPR; air.height = H * DPR; ax.setTransform(DPR, 0, 0, DPR, 0, 0);
    lines = [];
    /* densité proportionnelle à la hauteur : ni vide sur grand écran, ni chargé sur mobile */
    var n = Math.max(9, Math.min(22, Math.round(H / 46)));
    for (var i = 0; i < n; i++) {
      lines.push({
        y: (i + 0.5) * (H / n) + (Math.random() - 0.5) * 12,
        x: Math.random() * W,                    /* position de tête */
        len: 40 + Math.random() * 130,           /* longueur du filet */
        v: 0.25 + Math.random() * 0.55,          /* vitesse de croisière */
        amp: 4 + Math.random() * 13,             /* amplitude d'ondulation */
        k: 0.004 + Math.random() * 0.008,        /* fréquence spatiale */
        ph: Math.random() * Math.PI * 2,
        fast: Math.random() < 0.16                /* quelques filets marqués */
      });
    }
  }

  function airFrame() {
    ax.clearRect(0, 0, W, H);
    var brand = tok("--brand"), accent = tok("--accent");
    t += 0.01;
    /* la rafale retombe doucement — inertie de l'air */
    gust *= 0.94;
    var boost = 1 + Math.min(gust, 26) * 0.55;

    for (var i = 0; i < lines.length; i++) {
      var L = lines[i];
      L.x += L.v * boost;
      if (L.x - L.len > W) { L.x = -L.len - Math.random() * 60; L.y += (Math.random() - 0.5) * 8; }

      /* le filet s'étire sous la rafale, comme un fluide accéléré */
      var len = L.len * (1 + Math.min(gust, 26) * 0.05);
      ax.beginPath();
      for (var s = 0; s <= len; s += 7) {
        var px = L.x - s;
        if (px < -20 || px > W + 20) continue;
        var py = L.y + Math.sin(px * L.k + L.ph + t) * L.amp;
        s === 0 ? ax.moveTo(px, py) : ax.lineTo(px, py);
      }
      ax.strokeStyle = L.fast ? accent : brand;
      ax.globalAlpha = (L.fast ? 0.20 : 0.13) + Math.min(gust, 26) * 0.007;
      ax.lineWidth = L.fast ? 1.5 : 1;
      ax.lineCap = "round";
      ax.stroke();
    }
    ax.globalAlpha = 1;
    if (!reduced) requestAnimationFrame(airFrame);
  }

  seedLines();
  addEventListener("resize", seedLines);
  if (reduced) { airFrame(); }
  else {
    addEventListener("scroll", function () {
      gust += Math.min(Math.abs(scrollY - lastY) * 0.16, 5);
      lastY = scrollY;
    }, { passive: true });
    requestAnimationFrame(airFrame);
  }
  new MutationObserver(function () { if (reduced) airFrame(); })
    .observe(root, { attributes: true, attributeFilter: ["data-theme"] });
}

/* ---------- parallaxe (mots fantômes) ---------- */
var plxEls = [];
document.querySelectorAll("[data-plx]").forEach(function (el) {
  plxEls.push({ el: el, d: parseFloat(el.getAttribute("data-plx")) || 0, sec: null });
});
function plxFrame() {
  var vc = innerHeight / 2;
  for (var i = 0; i < plxEls.length; i++) {
    var o = plxEls[i];
    if (!o.sec) o.sec = o.el.closest("section, footer") || o.el.parentElement;
    var r = o.sec.getBoundingClientRect();
    if (r.bottom < -200 || r.top > innerHeight + 200) continue;
    var y = (r.top + r.height / 2 - vc) * o.d;
    o.el.style.transform = "translate3d(0," + y.toFixed(1) + "px,0)";
  }
}
if (!reduced && plxEls.length) {
  var tick = false;
  addEventListener("scroll", function () {
    if (tick) return; tick = true;
    requestAnimationFrame(function () { plxFrame(); tick = false; });
  }, { passive: true });
  plxFrame();
}

/* ---------- révélation au défilement (opacité seule) ---------- */
var rv = document.querySelectorAll(".rv");
if (rv.length) {
  if (reduced) { rv.forEach(function (e) { e.classList.add("on"); }); }
  else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("on"); io.unobserve(e.target); } });
    }, { threshold: .14 });
    rv.forEach(function (e) { io.observe(e); });
  }
}

/* ---------- compteurs des bandeaux de preuve ---------- */
var fmt = new Intl.NumberFormat("fr-FR");
var counters = document.querySelectorAll("[data-count]");
if (counters.length) {
  var cio = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      cio.unobserve(e.target);
      var end = +e.target.getAttribute("data-count");
      if (reduced) { e.target.textContent = fmt.format(end); return; }
      var t0 = performance.now();
      (function step(now) {
        var k = Math.min(1, (now - t0) / 1100); k = 1 - Math.pow(1 - k, 3);
        e.target.textContent = fmt.format(Math.round(end * k));
        if (k < 1) requestAnimationFrame(step);
      })(t0);
    });
  }, { threshold: .5 });
  counters.forEach(function (c) { cio.observe(c); });
}
})();
