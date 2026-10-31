/* César Revilla · interacciones (sin dependencias) · v2.1 */
(function () {
  var d = document, root = d.documentElement, w = window;
  root.classList.add("js");
  var reduce = w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var head = d.querySelector(".site-head");
  var bar = d.querySelector(".progress");
  var feeds = d.querySelectorAll(".feed");
  var targets = Array.prototype.slice.call(
    d.querySelectorAll(".card, .feed li, .prov li, details.faq, .facts, .gallery figure, section.block h2, .stat, .table-wrap, .chart-fig, .imp, .tile, .press, .channel"));

  function countUp(el) {
    var end = parseFloat(el.getAttribute("data-count"));
    if (isNaN(end) || el.dataset.done) return;
    el.dataset.done = "1";
    if (reduce) { el.textContent = end.toLocaleString("en-US"); return; }
    var t0 = null, dur = 1600;
    function step(t) {
      if (!t0) t0 = t;
      var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      el.textContent = Math.round(end * e).toLocaleString("en-US");
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  function show(el) {
    if (el.classList.contains("is-in")) return;
    el.classList.add("is-in");
    var c = el.querySelector("[data-count]");
    if (c) countUp(c);
  }

  targets.forEach(function (el) { el.classList.add("reveal"); });

  // Lo que ya está en pantalla o por encima se muestra al instante (nunca queda oculto)
  function sweep() {
    var vh = w.innerHeight;
    for (var i = 0; i < targets.length; i++) {
      var el = targets[i];
      if (el.classList.contains("is-in")) continue;
      if (el.getBoundingClientRect().top < vh * 0.95) show(el);
    }
  }

  var ticking = false;
  function frame() {
    ticking = false;
    var y = w.scrollY || 0;
    if (head) head.classList.toggle("scrolled", y > 12);
    if (bar) {
      var h = root.scrollHeight - w.innerHeight;
      bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    }
    for (var i = 0; i < feeds.length; i++) {
      var r = feeds[i].getBoundingClientRect();
      var p = (w.innerHeight * 0.7 - r.top) / r.height;
      feeds[i].style.setProperty("--fill", Math.max(0, Math.min(1, p)) * 100 + "%");
    }
    sweep();
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  w.addEventListener("scroll", onScroll, { passive: true });
  w.addEventListener("resize", onScroll, { passive: true });

  if ("IntersectionObserver" in w && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { show(en.target); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -5% 0px", threshold: 0 });
    targets.forEach(function (el) { io.observe(el); });
  } else {
    targets.forEach(show);
  }
  requestAnimationFrame(frame);
  // Red de seguridad: si algo quedara sin mostrarse, aparece igual
  w.addEventListener("load", function () { setTimeout(sweep, 300); });
})();

// Sellos de ley publicada (por si la página se generó antes del sello)
(function (d) {
  var L = {"universidad-nacional-de-huancabamba-ley-32162": "Ley 32162", "retiro-afp-2024-ley-32002": "Ley 32002",
    "retiro-cts-2024-comision-economia": "Ley 32027", "mypes-detracciones-ley-por-insistencia-2023": "Ley publicada",
    "represa-tapa-de-cuy-sechura": "Ley 31413"};
  function mk(t) { var s = d.createElement("span"); s.className = "stamp"; s.textContent = "\u2713 " + t; return s; }
  d.querySelectorAll(".card").forEach(function (c) {
    if (c.querySelector(".stamp")) return;
    var a = c.querySelector("h3 a"); if (!a) return;
    var k = (a.getAttribute("href") || "").split("/").pop().replace(".html", "");
    if (L[k]) c.insertBefore(mk(L[k]), c.firstChild);
  });
  var k = location.pathname.split("/").pop().replace(".html", ""), meta = d.querySelector("p.meta");
  if (L[k] && meta && !meta.querySelector(".stamp")) meta.insertBefore(mk(L[k]), meta.firstChild);
  var tc = d.querySelector('meta[name="theme-color"]'); if (tc) tc.setAttribute("content", "#0F2A44");
})(document);
