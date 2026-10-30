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
