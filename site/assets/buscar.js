/* Búsqueda en todo el sitio — Gramáticas Pāḷi en español
   FUENTE, no salida, como pali.js y cabecera.js: ningún generador escribe
   este archivo. La página (/buscar/, /en/buscar/) y el índice
   (assets/busqueda-es.json, busqueda-en.json) los escribe
   herramientas/generar_busqueda.py. Rediseño de la navegación, etapa 4a
   (2026-10-08).

   · El índice se pide sólo cuando alguien busca: al llegar con ?q=, o al
     escribir o enviar la caja. Nunca al cargar una página sin búsqueda.
   · Sin dependencias ni CDN.
   · norm() es la normalización de los buscadores de las páginas (plegar()
     de pali.js, fold() de raíces): minúsculas, sin diacríticos (ā = a,
     ṃ = m, ñ = n…), sin puntuación. generar_busqueda.norm() hace lo mismo
     con las claves del índice; si se cambia una, hay que cambiar la otra.
   · La búsqueda queda en la dirección (?q=) para poder compartirla.
   · Los grupos salen por su mejor coincidencia, no en un orden fijo; en
     Suttas, lo que se ve (título, traducción) antes que lo que sólo está en
     las palabras de los ejemplos (véase buscar()).
   · Los borradores no traen texto al índice: sólo su título, y la
     clasificación y el análisis, los § que cubren (véase porNumero()). */
(function () {
  'use strict';
  var raiz = document.getElementById('busca');
  if (!raiz) return;
  var TX = {};
  try { TX = JSON.parse(raiz.getAttribute('data-textos') || '{}'); } catch (e) {}
  var form = document.getElementById('busca-form');
  var input = document.getElementById('busca-q');
  var estado = document.getElementById('busca-estado');
  var res = document.getElementById('busca-res');

  /* La raíz del sitio, de la dirección de este guion (como cabecera.js). */
  var BASE = (function () {
    var s = document.currentScript && document.currentScript.src;
    if (s) return s.replace(/assets\/buscar\.js(\?.*)?$/, '');
    var a = document.createElement('a'); a.href = raiz.getAttribute('data-indice');
    return a.href.replace(/assets\/busqueda-[a-z]+\.json(\?.*)?$/, '');
  })();
  var URL_INDICE = (function () {
    var a = document.createElement('a'); a.href = raiz.getAttribute('data-indice');
    return a.href;
  })();

  var POR_GRUPO = 20;

  /* ── Normalización ─────────────────────────────────────────────── */
  var PUNT = /[’'‘"“”«».,;:()\[\]§+=¿?—–-]/g;
  var PUNT_1 = /^[’'‘"“”«».,;:()\[\]§+=¿?—–-]$/;
  function norm(s) {
    return String(s == null ? '' : s).normalize('NFC').normalize('NFD')
      .replace(/\p{M}/gu, '').replace(/[ŋŊ]/g, 'n').toLowerCase()
      .replace(PUNT, '').replace(/[^0-9a-z]+/g, ' ').trim();
  }
  /* Un carácter, plegado como norm() pero sin recortar: sirve para
     resaltar sobre el texto original. */
  function plegarCar(c) {
    var f = c.normalize('NFD').replace(/\p{M}/gu, '').replace(/[ŋŊ]/g, 'n').toLowerCase();
    if (PUNT_1.test(f)) return '';
    return f.replace(/[^0-9a-z]/g, ' ');
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function fmt(s, v) {
    return String(s || '').replace(/\{(\w+)\}/g, function (_, k) { return v[k] != null ? v[k] : ''; });
  }

  /* Resalta en `texto` cada aparición de las palabras buscadas. */
  function resaltar(texto, tokens) {
    if (!texto) return '';
    var plegado = '', idx = [];
    for (var i = 0; i < texto.length; i++) {
      var f = plegarCar(texto[i]);
      for (var k = 0; k < f.length; k++) idx.push(i);
      plegado += f;
    }
    idx.push(texto.length);
    var marcas = [];
    tokens.forEach(function (tk) {
      if (!tk) return;
      var desde = 0, at;
      while ((at = plegado.indexOf(tk, desde)) >= 0) {
        marcas.push([idx[at], idx[at + tk.length - 1] + 1]);
        desde = at + tk.length;
      }
    });
    if (!marcas.length) return esc(texto);
    marcas.sort(function (a, b) { return a[0] - b[0] || b[1] - a[1]; });
    var out = '', pos = 0;
    marcas.forEach(function (m) {
      if (m[0] < pos) { if (m[1] > pos) { out += '<mark>' + esc(texto.slice(pos, m[1])) + '</mark>'; pos = m[1]; } return; }
      out += esc(texto.slice(pos, m[0])) + '<mark>' + esc(texto.slice(m[0], m[1])) + '</mark>';
      pos = m[1];
    });
    return out + esc(texto.slice(pos));
  }

  /* ── El índice ─────────────────────────────────────────────────── */
  var INDICE = null, cargando = null;
  function cargar() {
    if (INDICE) return Promise.resolve(INDICE);
    if (cargando) return cargando;
    cargando = fetch(URL_INDICE, { credentials: 'same-origin' })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) { INDICE = preparar(d); return INDICE; })
      .catch(function (e) { cargando = null; throw e; });
    return cargando;
  }

  /* Lo que se compara, normalizado una sola vez. `nucleo`: el título sin
     su §N, su código de paradigma ni lo que va entre paréntesis, partido
     por « / » (raíces con dos formas): una coincidencia exacta con él pasa
     delante. */
  function preparar(d) {
    var tipos = d.tipos || [];
    var entradas = (d.e || []).map(function (e, i) {
      var t = e[1] || '', x = e[2] || '';
      var nt = norm(t), nx = norm(x);
      var base = t.replace(/^§\d+\s+/, '').replace(/^[^·]*·\s+/, '').replace(/\s*\([^)]*\)\s*$/, '');
      return {
        g: tipos[e[0]], t: t, x: x, u: e[3], b: !!e[5], l: e[6] || '', i: i,
        nt: nt, nx: nx, resto: nx + ' ' + (e[4] || ''),
        nucleo: base.split(' / ').map(norm),
        bruto: t.normalize('NFC').toLowerCase()
      };
    });
    return { tipos: tipos, e: entradas, borradores: d.borradores || [] };
  }

  function inicioDePalabra(s, at) { return at === 0 || s.charAt(at - 1) === ' '; }
  function finDePalabra(s, at) { return at === s.length || s.charAt(at) === ' '; }

  /* Devuelve {p, vis}: la puntuación (0 si falta alguna palabra) y si todas
     las palabras están a la vista —en el título o en el texto corto—, no
     sólo en las claves ocultas (las palabras de los ejemplos de un sutta). */
  function puntuar(e, tokens, qn, qbruto) {
    var p = 0, vis = true;
    for (var i = 0; i < tokens.length; i++) {
      var tk = tokens[i], at = e.nt.indexOf(tk);
      if (at >= 0) {
        /* la mejor aparición en el título: al principio de una palabra */
        var mejor = 0, desde = 0;
        while (at >= 0) {
          var v = inicioDePalabra(e.nt, at) ? (finDePalabra(e.nt, at + tk.length) ? 60 : 40) : 15;
          if (at === 0) v += 20;
          if (v > mejor) mejor = v;
          desde = at + 1;
          at = e.nt.indexOf(tk, desde);
        }
        p += mejor;
      } else {
        at = e.resto.indexOf(tk);
        if (at < 0) return null;         /* todas las palabras han de estar */
        if (e.nx.indexOf(tk) < 0) vis = false;
        p += inicioDePalabra(e.resto, at) ? (finDePalabra(e.resto, at + tk.length) ? 10 : 8) : 3;
      }
    }
    if (e.nt === qn || e.nucleo.indexOf(qn) >= 0) p += 500;
    if (qbruto && e.bruto.indexOf(qbruto) >= 0) p += 5;   /* con sus diacríticos */
    return { p: p - e.nt.length / 100, vis: vis };
  }

  /* Un número: el § publicado primero, y detrás los dos borradores que
     tienen fila para ese §, SÓLO con su título y su número. */
  function porNumero(n, idx) {
    var out = [];
    idx.borradores.forEach(function (b) {
      var dentro = (b.n || []).some(function (r) { return n >= r[0] && n <= r[1]; });
      if (dentro) out.push({ g: 'suttas', t: '§' + n + ' · ' + b.t, x: '', u: b.u.replace('{n}', n), b: true });
    });
    return out;
  }

  function buscar(q, idx) {
    var qn = norm(q);
    if (!qn) return null;
    var tokens = qn.split(' ');
    var qbruto = q.normalize('NFC').toLowerCase().trim();
    var grupos = {};
    idx.tipos.forEach(function (t) { grupos[t] = []; });
    idx.e.forEach(function (e) {
      var r = puntuar(e, tokens, qn, qbruto);
      if (r && r.p > 0) grupos[e.g].push({ e: e, p: r.p, vis: r.vis });
    });
    var num = /^\d+$/.test(qn) ? parseInt(qn, 10) : null;
    /* Dentro de cada grupo, la mejor primero. En Suttas, además, lo que
       coincide en el título o en la línea de traducción va antes que lo que
       sólo coincide en las palabras de los ejemplos, que no se ven. */
    var mejor = {};
    idx.tipos.forEach(function (t) {
      var l = grupos[t];
      if (num !== null && t === 'suttas') {
        l.forEach(function (r) { if (r.e.t.indexOf('§' + num + ' ') === 0) r.p += 10000; });
      }
      l.sort(function (a, b) {
        if (t === 'suttas' && a.vis !== b.vis) return a.vis ? -1 : 1;
        return b.p - a.p || a.e.i - b.e.i;
      });
      mejor[t] = l.reduce(function (m, r) { return Math.max(m, r.p); }, -Infinity);
      grupos[t] = l.map(function (r) { return r.e; });
    });
    /* Los grupos, por su mejor coincidencia: el que tiene el título exacto
       (bhū → Raíces, kāraka → Glosario) va primero. Un número pone Suttas
       delante (el § lleva +10000). A igualdad, el orden fijo de los tipos. */
    var orden = idx.tipos.slice().sort(function (a, b) {
      return (mejor[b] - mejor[a]) || (idx.tipos.indexOf(a) - idx.tipos.indexOf(b));
    });
    if (num !== null) {
      var extra = porNumero(num, idx);
      var l = grupos.suttas, k = (l.length && l[0].t.indexOf('§' + num + ' ') === 0) ? 1 : 0;
      grupos.suttas = l.slice(0, k).concat(extra, l.slice(k));
    }
    return { grupos: grupos, tokens: tokens, orden: orden };
  }

  /* ── Pintar ────────────────────────────────────────────────────── */
  /* El texto de una ficha que no tiene todavía inglés sale en español en
     /en/buscar/, como en la página del glosario, y con la misma etiqueta
     (.solo-es, base.css): «ES» a la vista y «No English text yet» para el
     lector de pantalla. */
  function soloEs() {
    var t = esc(TX.solo_es || 'No English text yet');
    return '<span class="solo-es" lang="en" title="' + t + '">' +
      '<span aria-hidden="true">ES</span><span class="vh">' + t + '</span></span>';
  }

  function filaHTML(e, tokens) {
    var pali = e.g === 'suttas' || e.g === 'glosario' || e.g === 'raices';
    return '<li><a class="busca-r" href="' + esc(BASE + e.u) + '">' +
      '<span class="busca-t"' + (pali && !e.b ? ' lang="pi"' : '') + '>' + resaltar(e.t, tokens) + '</span>' +
      (e.b ? ' <span class="borrador">' + esc(TX.borrador || 'borrador') + '</span>' : '') +
      (e.x ? '<span class="busca-x"' + (e.l ? ' lang="' + esc(e.l) + '"' : '') + '>' +
        (e.l === 'es' ? soloEs() : '') + resaltar(e.x, tokens) + '</span>' : '') +
      '</a></li>';
  }

  function pintarGrupo(sec, g, lista, tokens, mostrados) {
    var ul = sec.querySelector('ul');
    ul.insertAdjacentHTML('beforeend', lista.slice(mostrados, mostrados + POR_GRUPO)
      .map(function (e) { return filaHTML(e, tokens); }).join(''));
    var hechos = Math.min(lista.length, mostrados + POR_GRUPO);
    var mas = sec.querySelector('.busca-mas');
    if (hechos < lista.length) {
      var n = Math.min(POR_GRUPO, lista.length - hechos);
      mas.hidden = false;
      mas.textContent = fmt(TX.ver_mas, { n: n }) + ' (' + hechos + ' ' + fmt(TX.quedan, { n: lista.length }) + ')';
      mas.onclick = function () {
        var primero = ul.children.length;
        pintarGrupo(sec, g, lista, tokens, hechos);
        var a = ul.children[primero] && ul.children[primero].querySelector('a');
        if (a) a.focus();
      };
    } else {
      mas.hidden = true;
    }
  }

  function pintar(q, r) {
    res.innerHTML = '';
    if (!r) { estado.textContent = ''; return; }
    var total = 0;
    r.orden.forEach(function (t) { total += r.grupos[t].length; });
    if (!total) {
      estado.innerHTML = esc(fmt(TX.nada, { q: q })) + ' <span class="busca-sug">' + esc(TX.sugerencia) + '</span>';
      return;
    }
    estado.textContent = total === 1 ? fmt(TX.un_resultado, { q: q }) : fmt(TX.n_resultados, { n: total, q: q });
    r.orden.forEach(function (t) {
      var lista = r.grupos[t];
      if (!lista.length) return;
      var sec = document.createElement('section');
      sec.className = 'busca-grupo';
      sec.setAttribute('aria-labelledby', 'busca-g-' + t);
      sec.innerHTML = '<h2 id="busca-g-' + t + '">' + esc((TX.grupos && TX.grupos[t]) || t) +
        ' <span class="busca-n">' + lista.length + '</span></h2><ul class="busca-lista"></ul>' +
        '<button type="button" class="busca-mas" hidden></button>';
      res.appendChild(sec);
      pintarGrupo(sec, t, lista, r.tokens, 0);
    });
  }

  /* ── La dirección ──────────────────────────────────────────────── */
  function ponerEnURL(q) {
    try {
      var u = location.pathname + (q ? '?q=' + encodeURIComponent(q) : '') + location.hash;
      history.replaceState(null, '', u);
    } catch (e) {}
  }
  function deURL() {
    var m = /[?&]q=([^&#]*)/.exec(location.search);
    if (!m) return '';
    try { return decodeURIComponent(m[1].replace(/\+/g, ' ')); } catch (e) { return m[1]; }
  }

  /* ── Correr una búsqueda ───────────────────────────────────────── */
  var turno = 0;
  function correr(q, guardar) {
    q = String(q || '').replace(/\s+/g, ' ').trim();
    if (guardar) ponerEnURL(q);
    var mio = ++turno;
    if (!norm(q)) { res.innerHTML = ''; estado.textContent = ''; return; }
    if (!INDICE) estado.textContent = TX.cargando || '';
    cargar().then(function (idx) {
      if (mio !== turno) return;
      pintar(q, buscar(q, idx));
    }, function () {
      if (mio !== turno) return;
      estado.textContent = TX.error || '';
    });
  }

  var espera = null;
  input.addEventListener('input', function () {
    clearTimeout(espera);
    espera = setTimeout(function () { correr(input.value, true); }, 180);
  });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    clearTimeout(espera);
    correr(input.value, true);
  });

  /* ── Teclado: ↓ de la caja a los resultados, ↑ ↓ entre ellos, Esc a la
     caja. Los resultados son enlaces: Tab y Enter funcionan solos. ── */
  function enlaces() { return Array.prototype.slice.call(res.querySelectorAll('a.busca-r')); }
  input.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') {
      var l = enlaces();
      if (l.length) { e.preventDefault(); l[0].focus(); }
    }
  });
  res.addEventListener('keydown', function (e) {
    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp' && e.key !== 'Escape') return;
    var l = enlaces(), i = l.indexOf(document.activeElement);
    if (i < 0) return;
    e.preventDefault();
    if (e.key === 'Escape') { input.focus(); return; }
    if (e.key === 'ArrowDown' && i + 1 < l.length) l[i + 1].focus();
    else if (e.key === 'ArrowUp') (i > 0 ? l[i - 1] : input).focus();
  });

  /* ── Arranque: si la dirección trae ?q=, se busca; si no, nada (el
     índice no se pide hasta que alguien escriba). ── */
  var inicial = deURL();
  if (inicial) {
    input.value = inicial;
    correr(inicial, false);
  } else {
    input.focus({ preventScroll: true });
  }
})();
