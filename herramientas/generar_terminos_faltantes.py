#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arma docs/glosario/terminos-faltantes.html —el formulario de adjudicación de
los términos gramaticales que NO están en el glosario— a partir de
docs/glosario/terminos-faltantes.json (la cosecha de la sesión 57:
Kaccāyana, Rūpasiddhi, Nyāsa y Thitzana).

    python3 herramientas/generar_terminos_faltantes.py

Es un documento de TRABAJO, no del sitio: se abre en local, el IEBH marca lo
que acepta, corrige el español y el inglés donde quiera, y pulsa «Exportar»,
que descarga veredictos-terminos-faltantes.json. Ese archivo se deja en
docs/glosario/ y lo aplica

    python3 herramientas/incorporar_terminos_faltantes.py

El formulario guarda el trabajo a medias en localStorage del navegador, de
modo que se puede cerrar y seguir otro día.
"""
import json, os, html

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "docs", "glosario", "terminos-faltantes.json")
DESTINO = os.path.join(RAIZ, "docs", "glosario", "terminos-faltantes.html")

PLANTILLA = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Términos que faltan en el glosario — adjudicación</title>
<style>
:root{--ink:#1d1a15;--soot:#6b665c;--paper:#f7f4ee;--line:#d9d3c6;--gold:#a8791e;--ok:#2e7d4f;--warn:#b45309}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 Georgia,"Times New Roman",serif}
header{position:sticky;top:0;background:var(--paper);border-bottom:1px solid var(--line);padding:10px 18px;z-index:2;display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center}
h1{font-size:18px;margin:0 8px 0 0}
main{padding:12px 18px 60px}
p.intro{max-width:70em;color:var(--soot);margin:8px 0 14px}
table{border-collapse:collapse;width:100%}
th,td{border-bottom:1px solid var(--line);padding:7px 6px;vertical-align:top;text-align:left}
th{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--soot);position:sticky;top:52px;background:var(--paper)}
td.pali{font-style:italic;font-size:16px;white-space:nowrap}
td.num{white-space:nowrap;color:var(--soot);font-size:12px}
td.fuentes{font-size:12px;color:var(--soot);white-space:nowrap}
td .com{font-size:13px;color:var(--soot)}
td .ref{font-size:12px;color:var(--soot);margin-top:3px}
input[type=text],textarea{width:100%;box-sizing:border-box;font:inherit;font-size:14px;padding:4px 6px;border:1px solid var(--line);border-radius:4px;background:#fff}
textarea{min-height:34px;resize:vertical}
tr.ok{background:#eef6f0}
tr.no{opacity:.55}
.sug{font-size:14px}
.btn{font:inherit;font-size:13px;padding:5px 10px;border:1px solid var(--line);border-radius:5px;background:#fff;cursor:pointer}
.btn:hover{border-color:var(--gold)}
.badge{font-size:12px;color:var(--soot)}
select{font:inherit;font-size:13px}
.tipo{font-size:11px;color:var(--soot);letter-spacing:.04em}
label.ck{display:inline-flex;align-items:center;gap:4px;font-size:12px;white-space:nowrap}
#aviso{font-size:13px;color:var(--ok)}
</style></head><body>
<header>
  <h1>Términos que faltan en el glosario</h1>
  <span class="badge" id="cuenta"></span>
  <label class="badge">ver <select id="filtro"><option value="">todo</option><option value="término">términos</option><option value="sufijo">sufijos</option><option value="designación">designaciones</option><option value="pendiente">sin decidir</option><option value="acepta">aceptados</option><option value="rechaza">rechazados</option></select></label>
  <button class="btn" id="todos">Aceptar todos los visibles</button>
  <button class="btn" id="exportar">Exportar veredictos ⬇</button>
  <button class="btn" id="copiar">Copiar al portapapeles</button>
  <label class="btn">Cargar veredictos <input type="file" id="cargar" accept=".json" hidden></label>
  <span id="aviso"></span>
</header>
<main>
<p class="intro">Cosecha de la sesión 57 sobre Kaccāyana (los ocho capítulos), Rūpasiddhi, Nyāsa y el vol. 2 de Ven. A. Thitzana: lo que ninguna de las tres fuentes del glosario tiene como lema. Las cifras de la columna «fuentes» son apariciones del tema en cada obra. El español y el inglés son <b>propuestas</b>; en cada fila hay sitio para la suya. Marque <b>acepta</b> para que entre (con su corrección si la escribió) o <b>rechaza</b> para que no; lo que quede sin marcar no se toca. El trabajo se guarda solo en este navegador; al terminar, <b>Exportar</b> descarga <code>veredictos-terminos-faltantes.json</code>: déjelo en <code>docs/glosario/</code> y avise, o pegue el texto copiado en el chat. Lo aceptado entra en la lista normativa (<code>comun/glosario.md</code>) y en su propuesta inglesa.</p>
<table><thead><tr>
<th>#</th><th>término</th><th>fuentes</th><th>español propuesto</th><th>inglés propuesto</th><th>comentario</th><th>veredicto</th><th>su español</th><th>su inglés</th><th>su nota</th>
</tr></thead><tbody id="cuerpo"></tbody></table>
</main>
<script>
const DATOS = __DATOS__;
const CLAVE = 'veredictos-terminos-faltantes';
let V = {}; try { V = JSON.parse(localStorage.getItem(CLAVE) || '{}'); } catch(e) { V = {}; }
const esc = s => String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const guarda = () => { try { localStorage.setItem(CLAVE, JSON.stringify(V)); } catch(e) {} cuenta(); };
function fila(d, i){
  const v = V[d.id] || {};
  const f = Object.entries(d.fuentes || {}).map(([k,n]) => k + ' ' + n).join(' · ');
  return '<tr data-id="' + esc(d.id) + '" class="' + (v.veredicto || '') + '">' +
    '<td class="num">' + (i+1) + '<div class="tipo">' + esc(d.tipo) + '</div></td>' +
    '<td class="pali">' + esc(d.termino) + '</td>' +
    '<td class="fuentes">' + esc(f) + '</td>' +
    '<td class="sug">' + esc(d.es) + '</td>' +
    '<td class="sug">' + esc(d.en) + '</td>' +
    '<td><div class="com">' + esc(d.comentario) + '</div>' + (d.ref ? '<div class="ref">' + esc(d.ref) + '</div>' : '') + '</td>' +
    '<td><label class="ck"><input type="radio" name="v-' + esc(d.id) + '" value="acepta"' + (v.veredicto === 'acepta' ? ' checked' : '') + '> acepta</label><br>' +
        '<label class="ck"><input type="radio" name="v-' + esc(d.id) + '" value="rechaza"' + (v.veredicto === 'rechaza' ? ' checked' : '') + '> rechaza</label></td>' +
    '<td><input type="text" data-campo="es" value="' + esc(v.es || '') + '" placeholder="(si no, vale el propuesto)"></td>' +
    '<td><input type="text" data-campo="en" value="' + esc(v.en || '') + '" placeholder="(si no, vale el propuesto)"></td>' +
    '<td><textarea data-campo="nota" placeholder="">' + esc(v.nota || '') + '</textarea></td></tr>';
}
function pinta(){
  const filtro = document.getElementById('filtro').value;
  const filas = DATOS.filter(d => {
    const v = V[d.id] || {};
    if (!filtro) return true;
    if (filtro === 'pendiente') return !v.veredicto;
    if (filtro === 'acepta' || filtro === 'rechaza') return v.veredicto === filtro;
    return d.tipo === filtro;
  });
  document.getElementById('cuerpo').innerHTML = filas.map((d) => fila(d, DATOS.indexOf(d))).join('');
  cuenta();
}
function cuenta(){
  const a = DATOS.filter(d => (V[d.id]||{}).veredicto === 'acepta').length;
  const r = DATOS.filter(d => (V[d.id]||{}).veredicto === 'rechaza').length;
  document.getElementById('cuenta').textContent = DATOS.length + ' filas · ' + a + ' aceptadas · ' + r + ' rechazadas · ' + (DATOS.length - a - r) + ' sin decidir';
}
document.getElementById('cuerpo').addEventListener('change', ev => {
  const tr = ev.target.closest('tr'); if (!tr) return;
  const id = tr.dataset.id; V[id] = V[id] || {};
  if (ev.target.type === 'radio') { V[id].veredicto = ev.target.value; tr.className = ev.target.value; }
  else if (ev.target.dataset.campo) V[id][ev.target.dataset.campo] = ev.target.value;
  guarda();
});
document.getElementById('cuerpo').addEventListener('input', ev => {
  const tr = ev.target.closest('tr'); if (!tr || !ev.target.dataset.campo) return;
  V[tr.dataset.id] = V[tr.dataset.id] || {}; V[tr.dataset.id][ev.target.dataset.campo] = ev.target.value; guarda();
});
document.getElementById('filtro').onchange = pinta;
document.getElementById('todos').onclick = () => {
  for (const tr of document.querySelectorAll('#cuerpo tr')) { const id = tr.dataset.id; V[id] = V[id] || {}; V[id].veredicto = 'acepta'; }
  guarda(); pinta();
};
function exportable(){
  const out = { fecha: new Date().toISOString().slice(0,10), adjudicado_por: 'IEBH', veredictos: {} };
  for (const d of DATOS) { const v = V[d.id]; if (v && v.veredicto) out.veredictos[d.id] = { veredicto: v.veredicto, es: v.es || '', en: v.en || '', nota: v.nota || '' }; }
  return JSON.stringify(out, null, 1);
}
document.getElementById('exportar').onclick = () => {
  const blob = new Blob([exportable()], {type: 'application/json'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'veredictos-terminos-faltantes.json'; a.click();
  document.getElementById('aviso').textContent = 'Descargado veredictos-terminos-faltantes.json';
};
document.getElementById('copiar').onclick = async () => {
  try { await navigator.clipboard.writeText(exportable()); document.getElementById('aviso').textContent = 'Copiado al portapapeles'; }
  catch(e) { document.getElementById('aviso').textContent = 'No se pudo copiar; use Exportar'; }
};
document.getElementById('cargar').onchange = ev => {
  const f = ev.target.files[0]; if (!f) return;
  f.text().then(t => { const j = JSON.parse(t); const vs = j.veredictos || j; for (const k in vs) V[k] = Object.assign(V[k] || {}, vs[k]); guarda(); pinta(); document.getElementById('aviso').textContent = 'Cargado ' + f.name; });
};
pinta();
</script>
</body></html>
"""

def main():
    datos = json.load(open(DATOS, encoding="utf-8"))
    pagina = PLANTILLA.replace("__DATOS__", json.dumps(datos, ensure_ascii=False))
    with open(DESTINO, "w", encoding="utf-8") as fh:
        fh.write(pagina)
    print("{0} filas → {1}".format(len(datos), os.path.relpath(DESTINO, RAIZ)))

if __name__ == "__main__":
    main()
