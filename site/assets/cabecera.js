/* Cabecera común del sitio — Gramáticas Pāḷi en español
   FUENTE, no salida, como pali.css y pali.js. El marcado sale de
   herramientas/cabecera.py; los datos de «Ir a §», de assets/secciones.json,
   que escribe herramientas/generar_secciones.py.

   La barra no tiene mecanismo propio de idioma ni de tema: pulsa los mandos
   que cada página ya tenía (siguen en el DOM, ocultos). Qué mando es el de
   cada página lo dicen los data-* de <header class="cab">. Así se conservan
   las dos URL de los capítulos y su redirección, los conmutadores de las
   páginas de una sola URL y las claves pali_lang y pali_dark. */
(function () {
  'use strict';
  var cab = document.getElementById('cab');
  if (!cab) return;
  var html = document.documentElement;
  var D = cab.dataset;
  var TEXTOS = {};
  try { TEXTOS = JSON.parse(D.textos || '{}'); } catch (e) {}

  /* La raíz del sitio, sacada de la dirección de este mismo guion: vale en
     el dominio, en /index.html y en una copia local. */
  var BASE = (function () {
    var s = document.currentScript && document.currentScript.src;
    if (s) return s.replace(/assets\/cabecera\.js(\?.*)?$/, '');
    var a = document.createElement('a'); a.href = D.raiz || './';
    return a.href;
  })();

  function $(sel) { try { return sel ? document.querySelector(sel) : null; } catch (e) { return null; } }

  /* ── Idioma ─────────────────────────────────────────────────────── */
  function idioma() {
    var m = D.modoIdioma;
    if (m === 'enlace') return D.idioma === 'en' ? 'en' : 'es';
    if (m === 'solo-es') return 'es';
    if (document.body && document.body.classList.contains('en')) return 'en';
    return /^en\b/i.test(html.getAttribute('lang') || '') ? 'en' : 'es';
  }
  function t(clave) {
    var l = idioma();
    return (TEXTOS[l] && TEXTOS[l][clave]) || (TEXTOS.es && TEXTOS.es[clave]) || '';
  }

  function cambiarIdioma(destino, ev) {
    var m = D.modoIdioma, ctl = (D.ctlIdioma || '').split('|');
    if (m === 'solo-es' || destino === idioma()) { if (ev) ev.preventDefault(); return; }
    var boton = null;
    if (m === 'par') boton = $(destino === 'en' ? ctl[1] : ctl[0]);
    else boton = $(ctl[0]);
    if (boton) {
      if (ev) ev.preventDefault();
      boton.click();          /* el de la página: guarda pali_lang y, en los
                                 capítulos, lleva a la otra URL con el #ancla */
    }
    /* sin mando en la página, el enlace del segmento hace su trabajo */
  }

  /* ── Tema ───────────────────────────────────────────────────────── */
  function oscuro() {
    var modo = D.tema, a = html.getAttribute('data-theme');
    if (modo === 'clase') return !!(document.body && document.body.classList.contains('dark'));
    if (a === 'dark') return true;
    if (modo === 'medio' && a === null) {
      return !!(window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches);
    }
    return false;
  }

  /* ── Pintar lo que depende del estado de la página ──────────────── */
  var botonTema = cab.querySelector('.cab-tema');
  var ultimo = '';
  function pintar() {
    var l = idioma(), o = oscuro();
    var firma = l + (o ? '1' : '0');
    if (firma === ultimo) return;
    ultimo = firma;
    cab.setAttribute('data-idioma-actual', l);
    cab.querySelectorAll('[data-cab-t]').forEach(function (el) { el.textContent = t(el.getAttribute('data-cab-t')); });
    cab.querySelectorAll('[data-cab-aria]').forEach(function (el) { el.setAttribute('aria-label', t(el.getAttribute('data-cab-aria'))); });
    cab.querySelectorAll('[data-cab-ph]').forEach(function (el) { el.setAttribute('placeholder', t(el.getAttribute('data-cab-ph'))); });
    if (D.modoIdioma === 'alterna' || D.modoIdioma === 'par') {
      cab.querySelectorAll('.cab-seg').forEach(function (b) {
        var cur = b.getAttribute('data-l') === l;
        b.classList.toggle('cab-cur', cur);
        b.setAttribute('aria-pressed', cur ? 'true' : 'false');
      });
    }
    if (botonTema) botonTema.setAttribute('aria-pressed', o ? 'true' : 'false');
    document.querySelectorAll('form[data-ir-sutta] .ir-aviso, .cab-aviso').forEach(function (a) { a.hidden = true; });
  }

  cab.querySelectorAll('.cab-seg').forEach(function (s) {
    s.addEventListener('click', function (ev) { cambiarIdioma(s.getAttribute('data-l'), ev); });
  });
  if (botonTema) botonTema.addEventListener('click', function () {
    var ctl = $(D.ctlTema);
    if (ctl) ctl.click();
    pintar();
  });

  /* Las páginas cambian de lengua o de tema por su cuenta (y al cargar):
     la barra las sigue. */
  if (window.MutationObserver) {
    var mo = new MutationObserver(pintar);
    mo.observe(html, { attributes: true, attributeFilter: ['lang', 'data-theme', 'class'] });
    if (document.body) mo.observe(document.body, { attributes: true, attributeFilter: ['class'] });
  }
  if (window.matchMedia) {
    var mq = matchMedia('(prefers-color-scheme: dark)');
    if (mq.addEventListener) mq.addEventListener('change', pintar);
  }

  /* ── Menú del teléfono ──────────────────────────────────────────── */
  var menu = cab.querySelector('.cab-menu');
  function abrir(si) {
    cab.classList.toggle('cab-abierta', si);
    if (menu) menu.setAttribute('aria-expanded', si ? 'true' : 'false');
  }
  if (menu) menu.addEventListener('click', function () { abrir(!cab.classList.contains('cab-abierta')); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && cab.classList.contains('cab-abierta')) { abrir(false); if (menu) menu.focus(); }
  });
  document.addEventListener('click', function (e) {
    if (cab.classList.contains('cab-abierta') && !cab.contains(e.target)) abrir(false);
  });

  /* ── Ir a § ─────────────────────────────────────────────────────── */
  var SECCIONES = null, cargando = null;
  function cargar() {
    if (SECCIONES) return Promise.resolve(SECCIONES);
    if (cargando) return cargando;
    cargando = fetch(BASE + 'assets/secciones.json', { credentials: 'same-origin' })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) { SECCIONES = d; return d; })
      .catch(function (e) { cargando = null; throw e; });
    return cargando;
  }

  /* El destino de un §, en UNA función. Desde la etapa 2 (2026-10-08) es la
     página del sutta, /s/N/ o /en/s/N/, que generar_hub.py escribe para
     cada § de secciones.json (y en inglés si el capítulo tiene edición
     inglesa). Un § que no está en el mapa no tiene destino. */
  function destinoSutta(n, l, datos) {
    var cap = datos && datos.secciones && datos.secciones[String(n)];
    if (!cap) return null;
    var info = datos.capitulos && datos.capitulos[cap];
    var en = l === 'en' && info && info.en;
    return BASE + (en ? 'en/' : '') + 's/' + n + '/';
  }

  function avisar(form, texto, enlace) {
    var a = form.querySelector('.cab-aviso, .ir-aviso');
    if (!a) return;
    a.textContent = texto;
    if (enlace) {
      a.appendChild(document.createTextNode(' '));
      var e = document.createElement('a');
      e.href = BASE + 'recursos/' + (idioma() === 'en' ? '?lang=en' : '');
      e.textContent = t('ver_recursos');
      a.appendChild(e);
    }
    a.hidden = false;
  }

  function ir(form) {
    var input = form.querySelector('input');
    var v = (input && input.value || '').replace(/[§\s.]/g, '');
    if (!v) { input && input.focus(); return; }
    if (!/^\d+$/.test(v)) {
      if (form.hasAttribute('data-palabras')) avisar(form, t('palabras'), true);
      else avisar(form, t('no_numero'));
      return;
    }
    var n = parseInt(v, 10);
    cargar().then(function (datos) {
      var url = destinoSutta(n, idioma(), datos);
      if (!url) { avisar(form, t('no_publicado').replace('{n}', n)); return; }
      var aqui = location.href.split('#')[0].split('?')[0].replace(/index\.html$/, '');
      abrir(false);
      if (aqui === url) {
        /* ya está en la página de ese sutta: arriba */
        window.scrollTo(0, 0);
        form.querySelector('input').value = '';
      } else {
        location.href = url;
      }
    }, function () { avisar(form, t('sin_indice')); });
  }

  document.querySelectorAll('form[data-ir-sutta]').forEach(function (form) {
    form.addEventListener('submit', function (e) { e.preventDefault(); ir(form); });
    var input = form.querySelector('input');
    if (input) {
      input.addEventListener('focus', function () { cargar().catch(function () {}); }, { once: true });
      input.addEventListener('input', function () {
        var a = form.querySelector('.cab-aviso, .ir-aviso'); if (a) a.hidden = true;
      });
    }
  });

  pintar();
  /* Las páginas que ponen su lengua o su tema en su propio guion final
     (después de éste) quedan recogidas por el observador; por si alguna lo
     hace sin tocar atributos, una pasada más al terminar de cargar. */
  window.addEventListener('load', pintar);
})();
