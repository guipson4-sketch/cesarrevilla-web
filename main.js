/* César Revilla · interacciones (sin dependencias) */
(function () {
  var d = document, root = d.documentElement;
  root.classList.add("js");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Cabecera compacta al bajar + barra de lectura + línea de tiempo
  var head = d.querySelector(".site-head");
  var bar = d.querySelector(".progress");
  var feeds = d.querySelectorAll(".feed");
  function onScroll() {
    var y = window.scrollY || 0;
    if (head) head.classList.toggle("scrolled", y > 12);
    if (bar) {
      var h = d.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    }
    feeds.forEach(function (f) {
      var r = f.getBoundingClientRect();
      var p = (window.innerHeight * 0.7 - r.top) / r.height;
      f.style.setProperty("--fill", Math.max(0, Math.min(1, p)) * 100 + "%");
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Aparición al entrar en pantalla
  var targets = d.querySelectorAll(".card, .feed li, .prov li, details.faq, .facts, .gallery figure, section.block h2, .stat, table");
  targets.forEach(function (el) { el.classList.add("reveal"); });
  function countUp(el) {
    var end = parseFloat(el.getAttribute("data-count"));
    if (isNaN(end)) return;
    if (reduce) { el.textContent = end.toLocaleString("en-US"); return; }
    var t0 = null, dur = 1600;
    function step(t) {
      if (!t0) t0 = t;
      var k = Math.min(1, (t - t0) / dur);
      var e = 1 - Math.pow(1 - k, 3);
      el.textContent = Math.round(end * e).toLocaleString("en-US");
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if (!("IntersectionObserver" in window)) {
    targets.forEach(function (el) { el.classList.add("is-in"); });
    d.querySelectorAll("[data-count]").forEach(countUp);
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add("is-in");
      var c = en.target.querySelector("[data-count]");
      if (c) countUp(c);
      io.unobserve(en.target);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
  targets.forEach(function (el) { io.observe(el); });
})();
