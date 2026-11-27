/* Reporte El Niño 2026–2027 · datos en vivo (Senamhi + modelo Open-Meteo) · sin dependencias */
(function () {
  var SEN = "https://www.senamhi.gob.pe/";
  var d = document;
  var $ = function (id) { return d.getElementById(id); };
  var MES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","setiembre","octubre","noviembre","diciembre"];
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function fecha(iso) { var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || ""); return m ? (+m[3]) + " de " + MES[+m[2] - 1] : iso; }
  function ahora() { try { return new Date().toLocaleString("es-PE", { dateStyle: "long", timeStyle: "short" }); } catch (e) { return new Date().toString(); } }
  function get(id, html) { var el = $(id); if (el) el.innerHTML = html; }
  function cache(key, ttl, fn) {
    try { var c = JSON.parse(sessionStorage.getItem(key) || "null"); if (c && Date.now() - c.t < ttl) return Promise.resolve(c.v); } catch (e) {}
    return fn().then(function (v) { try { sessionStorage.setItem(key, JSON.stringify({ t: Date.now(), v: v })); } catch (e) {} return v; });
  }
  function norm(t) { return t.replace(/\s+/g, " ").trim(); }

  /* ---- Avisos meteorológicos de Senamhi ---- */
  function avisos() {
    return cache("ni_av2", 600000, function () {
      return fetch(SEN + "?p=aviso-meteorologico").then(function (r) { if (!r.ok) throw 0; return r.text(); }).then(function (h) {
        var doc = new DOMParser().parseFromString(h, "text/html");
        var rows = [].slice.call(doc.querySelectorAll("table tbody tr")).map(function (tr) {
          var td = tr.querySelectorAll("td"), a = tr.querySelector("a");
          if (td.length < 7) return null;
          return { t: norm(td[0].textContent), n: norm(td[1].textContent), em: norm(td[2].textContent), ini: norm(td[3].textContent),
                   fin: norm(td[4].textContent), dur: norm(td[5].textContent), niv: norm(td[6].textContent).toUpperCase(),
                   href: a ? new URL(a.getAttribute("href"), SEN).href : SEN + "?p=aviso-meteorologico" };
        }).filter(Boolean);
        var act = rows.filter(function (r) { return /vigente|emitido/i.test(r.n); });
        if (!act.length) throw 0;
        var lluvia = act.filter(function (r) { return /PRECIP|LLUVIA/i.test(r.t); });
        var norte = lluvia.filter(function (r) { return /NORTE|TUMBES|PIURA/i.test(r.t); })[0];
        if (!norte) return { act: act, det: "" };
        return fetch(norte.href).then(function (r) { return r.text(); }).then(function (h2) {
          var tx = norm(new DOMParser().parseFromString(h2, "text/html").body.textContent);
          var m = /El SENAMHI informa.{20,1600}/.exec(tx), det = m ? m[0] : "";
          det = det.replace(/(\s\d{1,2} de [A-Za-zéÉ]+){1,6}\s*$/, "");
          var cut = det.lastIndexOf("."); if (cut > 200) det = det.slice(0, cut + 1);
          return { act: act, det: det, ref: norte.href };
        }).catch(function () { return { act: act, det: "" }; });
      });
    });
  }
  function pintaAvisos(x) {
    var C = { ROJO: "rojo", NARANJA: "naranja", AMARILLO: "amarillo" };
    var prio = function (r) { return /PRECIP|LLUVIA/i.test(r.t) && /NORTE|TUMBES|PIURA/i.test(r.t) ? 0 : /PRECIP|LLUVIA/i.test(r.t) ? 1 : 2; };
    var lista = x.act.slice().sort(function (a, b) { return prio(a) - prio(b); });
    var h = lista.slice(0, 6).map(function (r, i) {
      return '<li class="ni-av ni-' + (C[r.niv] || "otro") + (prio(r) === 0 ? " ni-main" : "") + '"><span class="ni-pill">' + esc(r.niv) + '</span>' +
        '<div><strong>' + esc(r.t) + '</strong><br><span class="ni-meta">Aviso N.° ' + esc(r.n) + ' · del ' + esc(fecha(r.ini)) + ' al ' + esc(fecha(r.fin)) + ' · ' + esc(r.dur) +
        ' · <a href="' + esc(r.href) + '" rel="noopener" target="_blank">Ver aviso en Senamhi</a></span></div></li>';
    }).join("");
    var det = x.det ? '<blockquote class="ni-det">' + esc(x.det) + '<footer>Senamhi, aviso de precipitaciones en la costa norte y sierra · <a href="' + esc(x.ref) + '" rel="noopener" target="_blank">texto completo</a></footer></blockquote>' : "";
    get("ni-avisos", '<ul class="ni-lista">' + h + '</ul>' + det + '<p class="ni-hora">Leído desde Senamhi el ' + esc(ahora()).replace(/\.$/, '') + '.</p>');
  }

  /* ---- Estado de El Niño costero (ENFEN, vía Senamhi) ---- */
  function estado() {
    return cache("ni_es2", 1800000, function () {
      return fetch(SEN + "?p=fenomeno-el-nino").then(function (r) { if (!r.ok) throw 0; return r.text(); }).then(function (h) {
        var tx = norm(new DOMParser().parseFromString(h, "text/html").body.textContent);
        var m = /Condiciones actuales de El Niño\/La Niña:\s*(.+?)\s*\(Actualizado al ([^)]+)\)\s*(.+?)\s*(?:Ver más|Monitoreo)/i.exec(tx);
        if (!m || /\{\{|\}\}/.test(m[1] + m[2] + m[3])) throw 0;
        var c = /Comunicado ENFEN[^0-9]{0,20}(\d+-\d{4})/i.exec(tx) || /Comunicado N°\s*(\d+-\d{4})/i.exec(tx);
        return { est: m[1], fec: m[2], msg: m[3] };
      });
    });
  }
  function pintaEstado(x) {
    if (/\{\{|\}\}/.test(x.est + x.fec + x.msg)) return;
    get("ni-estado", '<p class="ni-big"><strong>' + esc(x.est) + '</strong></p><p>' + esc(x.msg.charAt(0) + x.msg.slice(1).toLowerCase()).replace(/niño/g, 'Niño') + '</p><p class="ni-hora">Actualizado por Senamhi/ENFEN al ' + esc(x.fec) + '. Leído el ' + esc(ahora()).replace(/\.$/, '') + '.</p>');
  }

  /* ---- Lluvia estimada por modelo (Open-Meteo): referencial, no oficial ---- */
  var LUG = [["Piura", -5.1945, -80.6328], ["Sullana", -4.9039, -80.6853], ["Chulucanas", -5.0968, -80.1619], ["Paita", -5.0892, -81.1144], ["Talara", -4.5772, -81.2719], ["Tumbes", -3.5669, -80.4515]];
  function modelo() {
    return cache("ni_om2", 900000, function () {
      var u = "https://api.open-meteo.com/v1/forecast?latitude=" + LUG.map(function (l) { return l[1]; }).join(",") + "&longitude=" + LUG.map(function (l) { return l[2]; }).join(",") +
        "&hourly=precipitation&past_hours=24&forecast_hours=24&timezone=America%2FLima";
      return fetch(u).then(function (r) { if (!r.ok) throw 0; return r.json(); });
    });
  }
  function pintaModelo(j) {
    var arr = Array.isArray(j) ? j : [j];
    var sum = function (a) { return a.reduce(function (s, v) { return s + (v || 0); }, 0); };
    var f = function (n) { return n.toFixed(1).replace(".", ","); };
    var filas = arr.map(function (o, i) {
      var p = (o.hourly && o.hourly.precipitation) || [], pas = p.slice(0, 24), fut = p.slice(24, 48);
      return "<tr><th scope=\"row\">" + esc(LUG[i][0]) + "</th><td>" + f(sum(pas)) + " mm</td><td>" + f(sum(fut)) + " mm</td><td>" + f(Math.max.apply(null, fut.concat([0]))) + " mm/h</td></tr>";
    }).join("");
    get("ni-modelo", '<div class="table-wrap"><table class="ni-tabla"><thead><tr><th>Ciudad</th><th>Últimas 24 h</th><th>Próximas 24 h</th><th>Máximo por hora (próx. 24 h)</th></tr></thead><tbody>' + filas + '</tbody></table></div><p class="ni-hora">Estimación de un modelo meteorológico (Open-Meteo), leída el ' + esc(ahora()).replace(/\.$/, '') + '. No es un dato oficial de Senamhi: los puntos pueden recibir mucho más o mucho menos que lo estimado.</p>');
  }

  function falla(id) { get(id, '<p class="ni-fallo">No pudimos leer el dato en vivo ahora. Ábrelo directamente en <a href="' + SEN + '?p=aviso-meteorologico" rel="noopener" target="_blank">Senamhi</a>.</p>'); }
  function carga() {
    avisos().then(pintaAvisos).catch(function () {});
    estado().then(pintaEstado).catch(function () {});
    modelo().then(pintaModelo).catch(function () { falla("ni-modelo"); });
  }
  function init() {
    var box = $("ni-avisos");
    if (!box) return;
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { io.disconnect(); carga(); } }, { rootMargin: "400px" });
      io.observe(box);
    } else { carga(); }
    var b = $("ni-refresh");
    if (b) b.addEventListener("click", function () { try { ["ni_av2", "ni_es2", "ni_om2"].forEach(function (k) { sessionStorage.removeItem(k); }); } catch (e) {} carga(); });
  }
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", init); else init();
})();
