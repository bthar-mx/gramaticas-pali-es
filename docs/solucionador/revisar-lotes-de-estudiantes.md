# Revisar un lote de veredictos de un estudiante

Procedimiento completo, de lo que llega por correo a lo que queda publicado.
Escrito el 2026-09-03, después del lote de la Therīgāthā-aṭṭhakathā.

Todas las órdenes se corren desde la raíz del repositorio:

    cd ~/Documents/gramaticas-pali-es

---

## 0. Guardar lo que llegó

Un estudiante suele mandar **varios archivos del mismo rato** —el lote
guardado tres veces según iba avanzando—, con las formas repetidas. Se
guardan todos, sin elegir: cuál es el bueno lo dice el guion.

    mkdir -p docs/solucionador/lotes-estudiante/AAAA-MM-DD
    # copiar ahí los .md tal como llegaron, sin renombrarlos

Los nombres traen paréntesis y espacios («veredictos-2026-09-02 (3).md»).
No hace falta arreglarlos: el comodín `*.md` los toma igual.

---

## 1. Leer el informe

    python3 herramientas/revisar_lote.py \
        docs/solucionador/lotes-estudiante/AAAA-MM-DD/*.md

Deduplica los archivos y, por cada forma, imprime:

- la frase de contexto, sacada de las observaciones del lote;
- **todas** las lecturas del motor con su escalera —la página le enseña al
  estudiante una sola, y por eso conviene ver las otras—;
- el veredicto del estudiante, y **si recompone**;
- los precedentes del banco con la misma segunda voz, que es donde salen
  las contradicciones;
- si la forma ya estaba adjudicada, y si dice otra cosa.

**El guion avisa, no rechaza.** Que el motor no recomponga unos componentes
no los desmiente: el Tipiṭaka es la fuente y Kaccāyana la autoridad que lo
explica, no la que lo autoriza. Lo que el aviso dice es que, de entrar así,
la ficha quedará sin escalera.

No escribe nada mientras no se le dé `--salida`.

---

## 2. Escribir el lote unificado

    python3 herramientas/revisar_lote.py \
        docs/solucionador/lotes-estudiante/AAAA-MM-DD/*.md \
        --salida docs/solucionador/lote-estudiante-AAAA-MM-DD.md

Sale un solo lote, sin repeticiones, con la evidencia en comentarios HTML
—que el incorporador no lee— y una línea `VEREDICTO:` por forma.

---

## 3. Adjudicar

Se edita ese archivo a mano. Por cada forma:

    VEREDICTO: sugatīsu + eva

Y, si el motor no deriva la lectura firmada, la escalera; va **verbatim**,
rotulada como del revisor, y las líneas de los pasos van **sangradas**:

    VEREDICTO: guttā + iti + assā
    ESCALERA:
        guttā iti assā
        gutt ā iti assā (§10)
        gutt ā ti assā (§13)
        gutt ā t i assā (§10)
        gutt ā t i ssā (§13)
        guttātissā (§11)

También se admite `NOTA DEL REVISOR: …` en una línea, para lo que valga la
pena conservar.

Un veredicto puede ser `no` (no es sandhi) o `compuesto` (fuera del
encargo). Lo que se deje en blanco se salta.

---

## 4. Ensayo del incorporador

    python3 herramientas/incorporar_adjudicaciones.py \
        docs/solucionador/lote-estudiante-AAAA-MM-DD.md \
        --fuente "IEBH, AAAA-MM-DD · revisión del lote de un estudiante" \
        --sin-tocar

`--sin-tocar` no escribe nada: dice qué pasaría. Léase el resumen del final,
que nombra forma por forma qué se incorpora, qué se enriquece y qué se
declina.

Una forma **ya adjudicada no se toca**. Si el veredicto nuevo difiere del
guardado, el incorporador declina y lo dice: eso se decide a mano, en
`recursos/solucionador/casos-reportados.json`.

---

## 5. Incorporar de verdad

La misma orden sin `--sin-tocar`:

    python3 herramientas/incorporar_adjudicaciones.py \
        docs/solucionador/lote-estudiante-AAAA-MM-DD.md \
        --fuente "IEBH, AAAA-MM-DD · revisión del lote de un estudiante"

---

## 6. Las referencias — el paso que se olvida

**Esto es lo que hace fallar el arnés de detección.** Un caso nuevo puede
tocar cualquiera de las cuatro referencias contra las que se mide el JS, y
la que quede rancia cierra la puerta.

Qué referencias tocan las formas nuevas:

    python3 - <<'FIN'
    import json, os, sys
    sys.path.insert(0, 'nuestro')
    from normalizar import cotejo
    NUEVAS = {cotejo('forma1'), cotejo('forma2')}      # ← poner las formas
    for nombre, campo in [
            ("referencia-senal-solo-canon.json", "forma"),
            ("referencia-corpus-versos-solo-canon.json", "forma"),
            ("referencia-corpus-comentario-solo-canon.json", "forma"),
            ("referencia-pagina-solo-canon.json", "f")]:
        d = json.load(open(os.path.join('nuestro/js', nombre), encoding='utf-8'))
        s = {cotejo(x.get(campo, "")) for x in d.get("filas", [])}
        print(nombre, '→ toca:', sorted(NUEVAS & s))
    FIN

Y se re-vierte **sólo** la que salga tocada:

    # señal (la primera corrida es lenta; después usa caché)
    SENAL_CACHE=$HOME/.cache/gramaticas-pali-senal.json \
        python3 nuestro/volcar_referencia_senal.py --dpd-filtro

    # corpus en verso
    python3 nuestro/volcar_referencia_corpus.py --solo-canon --dpd-filtro

    # corpus en prosa (comentario)
    python3 nuestro/volcar_referencia_corpus.py --solo-canon --dpd-filtro --comentario

    # la página
    python3 nuestro/volcar_referencia_pagina.py --dpd-filtro

---

## 7. Regenerar y comprobar

    python3 herramientas/generar_solucionador.py

    node nuestro/js/arnes.js
    node nuestro/js/arnes_corpus.js
    node nuestro/js/arnes_deteccion.js
    node nuestro/js/arnes_pagina.js
    node nuestro/js/arnes_casos.js

Los cinco tienen que pasar. Si uno falla, **no hay commit**: el árbol queda
tal cual para diagnosticar y no se publica nada.

---

## 8. Publicar

    git add -A
    git commit -m "Casos del lote de un estudiante del AAAA-MM-DD: forma1, forma2"
    git push

El hook de pre-commit regenera el HTML de `site/` y lo añade solo. El push
a `main` despliega en <https://gramaticas.buddha-dhamma.net>.

---

## El camino corto, cuando los veredictos vienen por la cola

Lo de arriba es para lotes que llegan **por fuera** —un archivo por correo—.
Los que entran por el modo revisión de la página van por la cola, y entonces
todo el ciclo es una sola orden, que además firma:

    VEREDICTOS_CLAVE=… python3 herramientas/ciclo_veredictos.py

Hace la cola, las referencias, la página, los cinco arneses, el commit y el
push, y **se detiene ante el primer fallo**. Pide el árbol limpio antes de
empezar.

---

## Lo que conviene no olvidar

- **Las observaciones del revisor no se vuelven datos.** El cuadro libre es
  prosa: queda en el archivo, para leerse. Si trae una escalera o corrige
  unos componentes, eso hay que ponerlo en los campos de la ficha a mano.
- **La página le enseña al estudiante una sola lectura del motor.** Por eso
  un veredicto suyo puede estar eligiendo contra un abanico que no vio.
- **Recomponer es necesario y no suficiente.** Que una cadena de aforismos
  recomponga la forma demuestra que la gramática PODRÍA producirla; no
  demuestra que el Tipiṭaka la diga.
