/* Lógica compartida — Gramáticas Pāḷi en español
   Extraído de 1-Sandhi-Kappa v1.1.
   Cada página define window.PALI_CAPITULO antes de cargar este archivo:
     id, doneKey, obra, obraSubtitulo, capituloPali, capituloEs, epubNombre */

// ─── Feature 1: IntersectionObserver for TOC scroll sync ─────────────
(function() {
  if (!window.IntersectionObserver) return;
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        var id = entry.target.id;
        document.querySelectorAll('.toc-item').forEach(function(el) {
          el.classList.remove('scroll-active');
        });
        var tocItem = document.getElementById('toc-' + id);
        if (tocItem) {
          tocItem.classList.add('scroll-active');
          if (typeof openTocGroupOf === 'function') openTocGroupOf(tocItem);
          try { tocItem.scrollIntoView({block:'nearest', behavior:'smooth'}); } catch(e) {}
        }
      }
    });
  }, { threshold: 0.2, rootMargin: '-10% 0px -70% 0px' });

  document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.sutta-card[id]').forEach(function(card) {
      observer.observe(card);
    });
  });
})();

// ─── Feature 2: Share sutta link ─────────────────────────────────────
function shareSutta(id) {
  var url = window.location.href.split('#')[0] + '#' + id;
  navigator.clipboard.writeText(url).then(function() {
    var btn = document.querySelector('#' + id + ' .share-btn');
    if (btn) {
      var orig = btn.innerHTML;
      btn.innerHTML = '✓ ¡Copiado!';
      btn.classList.add('shared');
      setTimeout(function() { btn.innerHTML = orig; btn.classList.remove('shared'); }, 2000);
    }
  });
}

// Handle deep links on load
document.addEventListener('DOMContentLoaded', function() {
  var hash = window.location.hash;
  if (hash && hash.length > 1) {
    var id = hash.slice(1);
    setTimeout(function() { jump(id); }, 100);
  }
});

// ─── Feature 3: Completion checkboxes with localStorage ──────────────
var CAP = window.PALI_CAPITULO || {};
// Cadenas de la interfaz: las da el generador (IDIOMAS en generar_capitulo.py)
// según el idioma de la página; sin ellas, español.
var T = CAP.textos || {
  estudiados: 'estudiados', abiertos: 'abiertos',
  ocultar_notas: 'Ocultar notas', ver_notas: 'Ver notas',
  ocultar: 'Ocultar', mostrar_mas: 'Mostrar más (formación, etc.)',
  encontrados: 'sutta(s) encontrado(s)', copiado: '✓ Copiado', copiar: 'Copiar §'
};
var DONE_KEY = CAP.doneKey || 'pali_done';

function loadDone() {
  try {
    return JSON.parse(localStorage.getItem(DONE_KEY) || '[]');
  } catch(e) { return []; }
}
function saveDone(arr) {
  try { localStorage.setItem(DONE_KEY, JSON.stringify(arr)); } catch(e) {}
}
function toggleDone(id) {
  var done = loadDone();
  var idx = done.indexOf(id);
  if (idx >= 0) {
    done.splice(idx, 1);
  } else {
    done.push(id);
  }
  saveDone(done);
  renderDone();
}
function renderDone() {
  var done = loadDone();
  var total = document.querySelectorAll('.sutta-card[id^="s"]').length;
  // Update checkboxes
  document.querySelectorAll('[id^="cb-"]').forEach(function(cb) {
    var sid = cb.id.replace('cb-', '');
    if (done.indexOf(sid) >= 0) {
      cb.classList.add('checked');
    } else {
      cb.classList.remove('checked');
    }
  });
  // Update counter
  var counter = document.getElementById('done-count');
  if (counter) counter.textContent = done.length + ' / ' + total + ' ' + T.estudiados;
  // Update progress badge to show completion
  var badge = document.getElementById('pbadge');
  if (badge && done.length > 0) {
    var pct = Math.round(done.length / total * 100);
    badge.title = pct + '% completado';
  }
}
document.addEventListener('DOMContentLoaded', renderDone);

// ─── Feature 4: EPUB export ───────────────────────────────────────────
function exportEPUB() {
  if (typeof JSZip === 'undefined') {
    alert('Cargando biblioteca EPUB… Por favor inténtalo de nuevo en unos segundos.');
    return;
  }
  var zip = new JSZip();

  // mimetype (must be first, uncompressed)
  zip.file('mimetype', 'application/epub+zip', {compression: 'STORE'});

  // META-INF/container.xml
  zip.folder('META-INF').file('container.xml',
    '<?xml version="1.0"?>\n' +
    '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n' +
    '  <rootfiles>\n' +
    '    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n' +
    '  </rootfiles>\n' +
    '</container>'
  );

  // Build chapter HTML
  var suttas = document.querySelectorAll('.sutta-card');
  var chapters = [];
  suttas.forEach(function(card) {
    var id = card.id;
    var title = (card.querySelector('.sutta-ref') ? card.querySelector('.sutta-ref').innerText : '') + ' ' +
                (card.querySelector('.sutta-pali-title') ? card.querySelector('.sutta-pali-title').innerText : '');
    var pali = card.querySelector('.pali-block') ? card.querySelector('.pali-block').innerText : '';
    var gloss = card.querySelector('.gloss') ? card.querySelector('.gloss').innerText : '';
    var vuttis = card.querySelectorAll('.vutti');
    var vutti_text = '';
    vuttis.forEach(function(v) { vutti_text += '<p>' + v.innerText.replace(/\n/g, ' ') + '</p>\n'; });
    var breakdown = card.querySelector('.sutta-breakdown') ? card.querySelector('.sutta-breakdown').innerText : '';

    chapters.push({
      id: id,
      title: title.trim(),
      content:
        '<h2>' + title.trim() + '</h2>\n' +
        (breakdown ? '<p class="breakdown">' + breakdown + '</p>\n' : '') +
        '<div class="pali"><p>' + pali.replace(/\n/g, '<br/>') + '</p></div>\n' +
        '<p class="gloss"><em>' + gloss + '</em></p>\n' +
        vutti_text
    });
  });

  // CSS for EPUB
  var epub_css =
    'body { font-family: serif; font-size: 1em; line-height: 1.7; margin: 1.5em; }\n' +
    'h1 { font-size: 1.4em; text-align: center; margin: 1em 0; }\n' +
    'h2 { font-size: 1.1em; margin: 1.5em 0 .5em; color: #333; }\n' +
    '.breakdown { font-family: monospace; font-size: .85em; color: #666; margin-bottom: .5em; }\n' +
    '.pali { background: #f5f5f3; padding: .5em .75em; border-left: 3px solid #aaa; margin: .75em 0; font-style: italic; }\n' +
    '.gloss { border-left: 3px solid #7F77DD; padding: .4em .75em; background: #f0f0fa; margin: .5em 0; }\n' +
    'p { margin: .4em 0; }\n';
  zip.folder('OEBPS').file('style.css', epub_css);

  // Spine items
  var manifest_items = ['<item id="css" href="style.css" media-type="text/css"/>\n'];
  var spine_items = [];
  var toc_items = [];

  // Title page
  var title_html =
    '<?xml version="1.0" encoding="utf-8"?>\n' +
    '<!DOCTYPE html>\n' +
    '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es">\n' +
    '<head><meta charset="utf-8"/><title>' + CAP.obra + ' — ' + CAP.capituloPali + '</title>' +
    '<link rel="stylesheet" href="style.css"/></head>\n' +
    '<body>\n<h1>' + CAP.obra + '</h1>\n' +
    '<p style="text-align:center">' + CAP.obraSubtitulo + '</p>\n' +
    '<p style="text-align:center"><strong>' + CAP.capituloPali + '</strong></p>\n' +
    '<p style="text-align:center">' + CAP.capituloEs + '</p>\n' +
    '<p style="text-align:center;margin-top:2em;color:#666;font-size:.9em">' +
    'Edición bilingüe Pāḷi–Español · ' +
    document.querySelectorAll('.sutta-card[id^="s"]').length + ' suttas · ' +
    document.querySelectorAll('.kanda-section').length + ' secciones<br/>' +
    'Traducción al español por Bhikkhu Nandisena</p>\n' +
    '</body></html>';
  zip.folder('OEBPS').file('title.xhtml', title_html);
  manifest_items.push('<item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>\n');
  spine_items.push('<itemref idref="title"/>\n');

  // Chapter files
  chapters.forEach(function(ch, i) {
    var fname = ch.id + '.xhtml';
    var chapter_html =
      '<?xml version="1.0" encoding="utf-8"?>\n' +
      '<!DOCTYPE html>\n' +
      '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es">\n' +
      '<head><meta charset="utf-8"/><title>' + ch.title + '</title>' +
      '<link rel="stylesheet" href="style.css"/></head>\n' +
      '<body>\n' + ch.content + '\n</body></html>';
    zip.folder('OEBPS').file(fname, chapter_html);
    manifest_items.push('<item id="' + ch.id + '" href="' + fname + '" media-type="application/xhtml+xml"/>\n');
    spine_items.push('<itemref idref="' + ch.id + '"/>\n');
    toc_items.push('<li><a href="' + fname + '">' + ch.title + '</a></li>\n');
  });

  // content.opf
  var now = new Date().toISOString().slice(0, 10);
  var opf =
    '<?xml version="1.0" encoding="utf-8"?>\n' +
    '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">\n' +
    '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n' +
    '  <dc:identifier id="uid">' + CAP.id + '</dc:identifier>\n' +
    '  <dc:title>' + CAP.obra + ' — ' + CAP.capituloPali + '</dc:title>\n' +
    '  <dc:creator>Bhikkhu Nandisena (trad.)</dc:creator>\n' +
    '  <dc:language>es</dc:language>\n' +
    '  <dc:date>' + now + '</dc:date>\n' +
    '  <meta property="dcterms:modified">' + now + 'T00:00:00Z</meta>\n' +
    '</metadata>\n' +
    '<manifest>\n  ' + manifest_items.join('  ') +
    '</manifest>\n' +
    '<spine>\n  ' + spine_items.join('  ') +
    '</spine>\n' +
    '</package>';
  zip.folder('OEBPS').file('content.opf', opf);

  // nav.xhtml (EPUB3 navigation)
  var nav_html =
    '<?xml version="1.0" encoding="utf-8"?>\n' +
    '<!DOCTYPE html>\n' +
    '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">\n' +
    '<head><meta charset="utf-8"/><title>Índice</title></head>\n' +
    '<body>\n<nav epub:type="toc">\n<ol>\n' +
    toc_items.join('') +
    '</ol>\n</nav>\n</body>\n</html>';
  zip.folder('OEBPS').file('nav.xhtml', nav_html);

  // Generate and download
  zip.generateAsync({type: 'blob', mimeType: 'application/epub+zip'}).then(function(blob) {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = CAP.epubNombre;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function() { URL.revokeObjectURL(a.href); }, 1000);
  });
}

// El botón del EPUB llama a exportEpub(); alias del nombre real.
function exportEpub() { exportEPUB(); }

// ─── Visited tracking ────────────────────────────────────────────
var visited = new Set();

// ─── Toggle sutta card ───────────────────────────────────────────
function toggleCard(id) {
  var card = document.getElementById(id);
  if (!card) return;
  card.classList.toggle('open');
  if (id !== 'intro') visited.add(id);
  refreshProgress();
  setTocActive(id);
}

// ─── Saltar: suave de cerca, de golpe de lejos ──────────────────
// Un capítulo mide muchos miles de píxeles, y más con las tarjetas
// abiertas. Animar el recorrido entero tarda segundos, porque el navegador
// lo recorre todo. A menos de dos pantallas la animación sí ayuda a ver de
// dónde a dónde se va; más allá, sólo hace esperar.
function saltarA(el, block) {
  var lejos = Math.abs(el.getBoundingClientRect().top) >= window.innerHeight * 2;
  var quieto = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  try {
    el.scrollIntoView({block: block || 'start',
                       behavior: (lejos || quieto) ? 'instant' : 'smooth'});
  } catch (e) {                       // navegadores sin «instant»
    el.scrollIntoView(true);
  }
}

// Volver al inicio, con el mismo criterio: desde el final de un capítulo
// la animación tardaría lo mismo que cualquier otro salto largo.
function volverArriba() {
  var quieto = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var lejos = window.scrollY >= window.innerHeight * 2;
  try {
    window.scrollTo({top: 0, behavior: (lejos || quieto) ? 'instant' : 'smooth'});
  } catch (e) {
    window.scrollTo(0, 0);
  }
}

// ─── Jump to sutta (from nav or TOC) ────────────────────────────
function jump(id) {
  var card = document.getElementById(id);
  if (!card) return;
  card.classList.add('open');
  if (id !== 'intro') visited.add(id);
  setTimeout(function() {
    saltarA(card, 'start');           // se mide ya abierta la tarjeta
  }, 40);
  refreshProgress();
  setTocActive(id);
}

function jumpOpen(id) { jump(id); }
function jumpTo(id) { jump(id); }

// ─── Expand / Collapse all ───────────────────────────────────────
function expandAll() {
  document.querySelectorAll('.sutta-card').forEach(function(c) {
    c.classList.add('open');
  });
  refreshProgress();
}
function collapseAll() {
  document.querySelectorAll('.sutta-card').forEach(function(c) {
    c.classList.remove('open');
  });
  refreshProgress();
}

// ─── Progress ────────────────────────────────────────────────────
function refreshProgress() {
  var all = document.querySelectorAll('.sutta-card[id^="s"]');
  var total = all.length;
  var open = document.querySelectorAll('.sutta-card[id^="s"].open').length;
  var pct = total > 0 ? (visited.size / total) * 100 : 0;
  document.getElementById('pbar').style.width = pct + '%';
  document.getElementById('pbadge').textContent = visited.size + ' / ' + total + ' §';
  var lbl = document.getElementById('open-count');
  if (lbl) lbl.textContent = open > 0 ? open + ' / ' + total + ' ' + T.abiertos : '';
}

// ─── TOC active ──────────────────────────────────────────────────
function setTocActive(id) {
  document.querySelectorAll('.toc-item').forEach(function(el) {
    el.classList.remove('active');
  });
  var a = document.getElementById('toc-' + id);
  if (a) {
    a.classList.add('active');
    openTocGroupOf(a);
    try { a.scrollIntoView({block:'nearest', behavior:'smooth'}); } catch(e) {}
  }
}

// ─── Diseño de una página (sesión 08): TOC plegable, «ir a §…»,
//     mini-navegación de kaṇḍas ─────────────────────────────────────
function toggleTocGroup(k) {
  var g = document.getElementById('tocg-' + k);
  if (g) g.classList.toggle('open');
}

// Abre el grupo del kaṇḍa activo y cierra los demás.
function openTocGroupOf(el) {
  var g = el && el.closest ? el.closest('.toc-group') : null;
  if (!g || g.classList.contains('open')) return;
  document.querySelectorAll('.toc-group.open').forEach(function(x) {
    x.classList.remove('open');
  });
  g.classList.add('open');
}

function jumpKanda(k) {
  var h = document.getElementById('kanda-' + k);
  if (h) saltarA(h, 'start');
}

// Caja «ir a §…» / filtro por título pāḷi.
// ─── Plegado de diacríticos para buscar ──────────────────────────
// Las dos cajas de esta página —el buscador de suttas y el filtro del
// índice— comparaban el texto tal cual, de modo que «pali» no encontraba
// «pāḷi», ni «byanjane» a «byañjane», ni «elision» a «elisión». Y los
// diacríticos pāḷi no se teclean en un teclado corriente, que es
// justamente cuando hace falta buscar. El resto del sitio ya los ignora.
var PLIEGA = {'ā':'a','ī':'i','ū':'u','ṃ':'m','ṁ':'m','ñ':'n','ṭ':'t','ḍ':'d',
              'ṇ':'n','ḷ':'l','ṅ':'n','ṣ':'s','ś':'s','ṛ':'r','ṝ':'r','ḥ':'h',
              'á':'a','é':'e','í':'i','ó':'o','ú':'u','ü':'u','ô':'o','ý':'y'};
function plegar(s) {
  return (s || '').toLowerCase()
    .replace(/[āīūṃṁñṭḍṇḷṅṣśṛṝḥáéíóúüôý]/g, function(c) { return PLIEGA[c]; })
    .replace(/[’'‘"“”\u00ab\u00bb.,;:()\[\]§+=¿?—–-]/g, '')
    .replace(/\s+/g, ' ').trim();
}
// El texto plegado de un elemento se calcula una vez y se guarda: en el
// Nāma son 219 suttas largos y rehacerlo en cada tecla se nota.
function textoBuscable(el) {
  if (el._plegado === undefined || el._plegadoDe !== el.textContent.length) {
    el._plegado = plegar(el.textContent);
    el._plegadoDe = el.textContent.length;
  }
  return el._plegado;
}
// Varias palabras: han de estar todas, en cualquier orden.
function casan(texto, q) {
  var t = plegar(q).split(' ').filter(Boolean);
  if (!t.length) return true;
  for (var i = 0; i < t.length; i++) {
    if (texto.indexOf(t[i]) < 0) return false;
  }
  return true;
}

function filterToc(q) {
  q = q.trim().toLowerCase();
  var esNum = /^§?\s*\d+$/.test(q);
  var grupos = document.querySelectorAll('.toc-group');
  if (!q || esNum) {
    document.querySelectorAll('.toc-item.toc-hidden').forEach(function(el) {
      el.classList.remove('toc-hidden');
    });
    grupos.forEach(function(g) {
      g.classList.remove('toc-filtered', 'toc-empty');
    });
    return;
  }
  grupos.forEach(function(g) {
    var hay = false;
    g.querySelectorAll('.toc-item').forEach(function(el) {
      var ok = casan(textoBuscable(el), q);
      el.classList.toggle('toc-hidden', !ok);
      if (ok) hay = true;
    });
    g.classList.toggle('toc-filtered', hay);
    g.classList.toggle('toc-empty', !hay);
  });
}

// Caja «§…» de la barra fija de kaṇḍas.
function kandaJumpKey(e) {
  if (e.key !== 'Enter') return;
  var m = e.target.value.trim().match(/^§?\s*(\d+)$/);
  if (m && document.getElementById('s' + m[1])) {
    jump('s' + m[1]);
    e.target.value = '';
    e.target.blur();
  }
}

// Botón flotante «volver al inicio»: aparece al bajar.
window.addEventListener('scroll', function() {
  var b = document.getElementById('top-btn');
  if (b) b.classList.toggle('show', window.scrollY > 600);
}, {passive: true});

function tocJumpKey(e) {
  if (e.key !== 'Enter') return;
  var v = e.target.value.trim();
  var m = v.match(/^§?\s*(\d+)$/);
  if (m) {
    if (document.getElementById('s' + m[1])) jump('s' + m[1]);
    return;
  }
  var vis = document.querySelectorAll('.toc-item:not(.toc-hidden)');
  if (v && vis.length === 1) vis[0].click();
}

// Resalta en la mini-navegación el kaṇḍa por el que se pasa.
(function() {
  if (!window.IntersectionObserver) return;
  var obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(en) {
      if (!en.isIntersecting) return;
      var k = en.target.id.replace('kanda-', '');
      document.querySelectorAll('.kanda-nav-btn').forEach(function(b) {
        b.classList.remove('active');
      });
      var btn = document.getElementById('knav-' + k);
      if (btn) btn.classList.add('active');
    });
  }, {rootMargin: '-5% 0px -75% 0px'});
  document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.kanda-heading[id]').forEach(function(h) {
      obs.observe(h);
    });
    // al cargar, solo el primer grupo del TOC abierto
    var g1 = document.querySelector('.toc-group');
    if (g1 && !document.querySelector('.toc-group.open')) {
      g1.classList.add('open');
    }
  });
})();

// ─── Collapsible sections ────────────────────────────────────────
function toggleSeq(seqId, btn) {
  var el = document.getElementById(seqId);
  if (!el) return;
  var open = el.classList.toggle('open');
  // Update button text
  for (var i = 0; i < btn.childNodes.length; i++) {
    if (btn.childNodes[i].nodeType === 3) {
      var type = btn.getAttribute('data-type');
      if (type === 'fn') {
        var n = btn.getAttribute('data-count') || '';
        btn.childNodes[i].nodeValue = open ? ' ' + T.ocultar_notas : (' ' + T.ver_notas + ' (' + n + ')');
      } else {
        btn.childNodes[i].nodeValue = open ? ' ' + T.ocultar : ' ' + T.mostrar_mas;
      }
    }
  }
}

// ─── Search ──────────────────────────────────────────────────────
function doSearch(q) {
  var cards = document.querySelectorAll('.sutta-card');
  var count = 0;
  q = q.trim().toLowerCase();
  cards.forEach(function(card) {
    if (!q || casan(textoBuscable(card), q)) {
      card.classList.remove('search-hidden');
      count++;
    } else {
      card.classList.add('search-hidden');
    }
  });
  var el = document.getElementById('search-count');
  if (el) el.textContent = q ? (count + ' ' + T.encontrados) : '';
}

// ─── Font size ───────────────────────────────────────────────────
var fontSize = 100;
function changeFont(dir) {
  fontSize = Math.max(80, Math.min(140, fontSize + dir * 10));
  document.getElementById('inner').style.fontSize = fontSize + '%';
  document.getElementById('font-lbl').textContent = fontSize + '%';
}

// ─── Copy sutta ──────────────────────────────────────────────────
function copySutta(id) {
  var card = document.getElementById(id);
  if (!card) return;
  var parts = [];
  var ref = card.querySelector('.sutta-ref');
  var title = card.querySelector('.sutta-pali-title');
  var bd = card.querySelector('.sutta-breakdown');
  if (ref && title) parts.push(ref.innerText.trim() + ' ' + title.innerText.trim());
  if (bd) parts.push(bd.innerText.trim());
  parts.push('');
  var pb = card.querySelector('.pali-block');
  if (pb) parts.push(pb.innerText.trim());
  parts.push('');
  card.querySelectorAll('.gloss, .vutti').forEach(function(el) {
    var t = el.innerText.trim();
    if (t) parts.push(t);
  });
  var text = parts.join('\n').replace(/\n{3,}/g, '\n\n').trim();
  navigator.clipboard.writeText(text).then(function() {
    var btn = card.querySelector('.copy-btn');
    if (!btn) return;
    btn.textContent = T.copiado;
    btn.classList.add('copied');
    setTimeout(function() { btn.textContent = T.copiar; btn.classList.remove('copied'); }, 2000);
  });
}

// ─── Dark mode ───────────────────────────────────────────────────
// La preferencia se guarda en la clave `pali_dark`, compartida con
// /recursos/sandhi/; la aplica un script inline al principio de <body>
// (antes de pintar), y aquí solo se conmuta y persiste.
function toggleDark() {
  var dark = document.body.classList.toggle('dark');
  try { localStorage.setItem('pali_dark', dark ? '1' : '0'); } catch (e) {}
}

// ─── Keyboard ────────────────────────────────────────────────────
document.addEventListener('keydown', function(e) {
  var sb = document.getElementById('search-box');
  if (e.key === '/' && document.activeElement !== sb) {
    e.preventDefault(); sb.focus();
  } else if (e.key === 'Escape' && document.activeElement === sb) {
    sb.value = ''; doSearch(''); sb.blur();
  }
});

// ─── Init ────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  refreshProgress();
  document.querySelectorAll('.sutta-header').forEach(function(h) {
    h.setAttribute('aria-expanded', 'false');
    h.setAttribute('role', 'button');
    h.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); h.click(); }
    });
  });
});

// Mobile: close tooltips on outside tap
document.addEventListener('click', function(e) {
  if (!e.target.closest('.fn-tip, .tip-wrap, .ref-tip, .nav-tip-wrap')) {
    document.querySelectorAll('.fn-tip-box, .tip-box, .ref-tip-box').forEach(function(el) {
      el.style.display = '';
    });
  }
});
// ─── Cajón TOC móvil (☰, sesión 10) ─────────────────────────────
// En pantallas sin sidebar (<1100 px) el mismo #toc se abre como cajón
// deslizante. El botón ☰ se inserta al frente de la barra de kaṇḍas.
function toggleTocDrawer(force) {
  var open = (typeof force === 'boolean') ? force
           : !document.body.classList.contains('toc-open');
  document.body.classList.toggle('toc-open', open);
  var b = document.getElementById('toc-burger');
  if (b) b.setAttribute('aria-expanded', open ? 'true' : 'false');
}
document.addEventListener('DOMContentLoaded', function() {
  var toc = document.getElementById('toc');
  var nav = document.querySelector('.kanda-nav');
  if (!toc || !nav) return;
  toc.classList.add('toc-drawer');
  var b = document.createElement('button');
  b.id = 'toc-burger'; b.className = 'toc-burger';
  b.setAttribute('aria-label', 'Abrir el índice de suttas');
  b.setAttribute('aria-expanded', 'false');
  b.textContent = '☰';
  b.addEventListener('click', function() { toggleTocDrawer(); });
  nav.insertBefore(b, nav.firstChild);
  var ovl = document.createElement('div');
  ovl.id = 'toc-ovl';
  ovl.addEventListener('click', function() { toggleTocDrawer(false); });
  document.body.appendChild(ovl);
  // Elegir un sutta cierra el cajón.
  toc.addEventListener('click', function(e) {
    if (e.target.closest && e.target.closest('.toc-item')) toggleTocDrawer(false);
  });

  // ─── Plegar el índice en pantalla ancha (sesión 29) ───────────
  // El ☰ de la barra de kaṇḍas es para el cajón de pantalla estrecha.
  // En ancha el índice va fijo al lado del texto, y se pliega con el ☰
  // de su esquina superior izquierda; el mismo ☰, fijo en ese punto,
  // lo devuelve: parece un solo botón aunque sean dos. No se guarda:
  // se abre siempre al entrar.
  function verToc(oculto) {
    document.documentElement.classList.toggle('sin-toc', oculto);
    var v = document.getElementById('toc-volver');
    if (v) v.setAttribute('aria-expanded', oculto ? 'false' : 'true');
  }
  var cerrar = document.createElement('button');
  cerrar.className = 'toc-ocultar';
  cerrar.type = 'button';
  /* El mismo ☰ que en las barras de los recursos: un solo símbolo para
     plegar el índice en todo el sitio. */
  cerrar.textContent = '☰';
  cerrar.setAttribute('aria-label', 'Ocultar el índice');
  cerrar.setAttribute('data-tip', 'Aparta el índice para leer a todo lo ancho. El ☰ se queda en su sitio para devolverlo.');
  cerrar.addEventListener('click', function() { verToc(true); });
  toc.style.position = toc.style.position || '';
  toc.insertBefore(cerrar, toc.firstChild);

  var volver = document.createElement('button');
  volver.id = 'toc-volver';
  volver.type = 'button';
  volver.textContent = '☰';
  volver.setAttribute('aria-label', 'Mostrar el índice');
  volver.setAttribute('data-tip', 'Mostrar otra vez el índice de suttas.');
  volver.addEventListener('click', function() { verToc(false); });
  document.body.appendChild(volver);

  // Al estrecharse la ventana el índice pasa a cajón: que no se quede
  // plegado y sin pestaña que lo devuelva.
  addEventListener('resize', function() {
    if (innerWidth < 1100) document.documentElement.classList.remove('sin-toc');
  });
});
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape' && document.body.classList.contains('toc-open')) {
    toggleTocDrawer(false);
  }
});

// Mobile: tap fn-sup to toggle tooltip
document.addEventListener('click', function(e) {
  var sup = e.target.closest('.fn-sup');
  if (sup) {
    e.stopPropagation();
    var box = sup.parentElement.querySelector('.fn-tip-box');
    if (box) {
      var cur = box.style.display;
      // Close all others first
      document.querySelectorAll('.fn-tip-box').forEach(function(b) { b.style.display = ''; });
      box.style.display = (cur === 'block') ? '' : 'block';
    }
  }
});
