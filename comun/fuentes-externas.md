# Fuentes externas: qué hay, qué autoridad tiene y qué se puede hacer con ella

Este archivo registra las fuentes que **no** están en el repositorio y que el
proyecto consulta. Para la autoridad doctrinal manda `CLAUDE.md`; esto es el
inventario práctico: dónde está cada cosa, en qué estado, y qué permiso trae.

Registrado el 2026-08-30 (sesión 39), al encontrarse en el Saddanīti la
autoridad de «tveva» que faltaba. Véase `docs/solucionador/tveva-dos-lecturas.md`.

---

## 1. bhaddacak.github.io — las gramáticas tradicionales en línea

<https://bhaddacak.github.io/grammarbooks>

Lo encontró IEBH el 2026-08-30. Es la fuente que resolvió la pregunta de
«tveva», y trae obras que el proyecto no tenía de ninguna otra manera.

### Qué contiene

| Obra | Dirección | Comprobado |
| --- | --- | --- |
| Kaccāyana + Rūpasiddhi | `/kaccrupa` | 190.368 caracteres |
| Kaccāyana solo / Rūpasiddhi sola | `/kacc` · `/rupa` | |
| Moggallāna + Payogasiddhi (+Pañcikāṭīkā) | `/moggpayo` | |
| Niruttidīpanī (Leḍī Sayāḍo, 1903) | `/nirutti` | |
| **Saddanīti · Suttamālā** | `/saddsut` | **1.347 suttas**, caps. 1-7 (388.254 car.) + caps. 8-9 (69.009 car.) |
| **Saddanīti · Dhātumālā** | `/sadddha` | 466.560 caracteres |
| **Saddanīti · Padamālā** | `/saddpad` | 541.140 caracteres |
| Abhidhānappadīpikā (+Ṭīkā) | `/abhidha` | |
| Subodhālaṅkāra, Vuttodaya | `/subho` · `/vutt` | |
| **Buscador de suttas entre obras** | `/gramsut` | relaciona Kacc, Mogg, Sadd, Nirutti |

El Suttamālā está **completo**: el selector de suttas tiene 1.347 entradas y la
numeración corre sin saltos de 1 a 1347 en los siete primeros capítulos; los
capítulos 8 y 9 (Catupadavibhāga, Pāḷinayādisaṅgaha) van en un segundo archivo
y no llevan numeración de sutta, que es como es el texto.

### Cómo se lee por programa

Las páginas son aplicaciones de JavaScript: `web_fetch` devuelve el armazón y
un «Loading…», no el texto. Hay que abrirlas en el navegador y leer
`document.getElementById('textdisplay').innerText`. Los datos crudos están
comprimidos en `/assets/palitext/gram/*.gz` y la página los descomprime con
pako.

### Advertencias, y no son menores

- **El propio editor avisa de erratas.** El texto romanizado viene del tailandés
  de Palipage; dice haber «corregido algunos puntos sin querer» al limpiarlo y
  que quedan más fallos que ésos. Su instrucción es expresa: **para cita seria,
  cotejar antes contra la edición de Helmer Smith.**
- **Y la advertencia se comprobó cierta el mismo día.** En el sutta 49 del
  Suttamālā este texto trae **un** ejemplo («itveva coro asimāvudhañ ca»);
  Smith trae **cuatro**. No es una errata de letra: faltan tres ejemplos, y dos
  de ellos son los que deciden la cuestión. De modo que sirve para ENCONTRAR y
  no para CITAR.
- **Licencia CC BY-NC-ND 4.0.** Consultarlo es libre; redistribuirlo o meter el
  texto en este repositorio, no. Si alguna vez hace falta una copia local para
  el solucionador, hay que pedir permiso o buscar otra procedencia.

---

## 2. Saddanīti de Helmer Smith en PDF — la edición para citar

En poder del IEBH. Comprobado el 2026-08-30 sobre
«Saddaníti - Aggavamsa's Pali Grammar Suttamālā.pdf», 340 páginas, 23 MB.

### Estado del archivo: imagen pura, y no importa tanto como parece

    Producer: Adobe Acrobat 9.0 Image Conversion Plug-in
    pdffonts  → NINGUNA fuente
    pdftotext → NADA

No hay capa de texto: es un escaneo. Pero **el escaneo es excelente y se lee
sin dificultad** a 150 dpi con `pdftoppm`, incluidos los diacríticos, la
cursiva y el aparato en cuerpo menor.

### Para qué sirve, que es la pregunta que importa

**Sirve, y mucho, para COTEJAR pasajes concretos.** Es exactamente lo que el
editor del sitio manda hacer, y no hace falta extraer nada: se localiza la
página, se convierte a imagen y se lee. Así se verificó el sutta 49 el
2026-08-30, y el cotejo dio tres ejemplos que el otro texto no traía.

**Trae además el aparato, que es media edición.** Smith imprime para cada sutta
la concordancia con Kaccāyana (`Kc`), Rūpasiddhi (`Rūp`), el Nyāsa (`Mmd`) y el
Kātantra, más la referencia canónica de cada ejemplo. Eso responde por sí solo
preguntas que de otro modo cuestan una sesión: en el sutta 49 el aparato da
`§ 50 Kc 20` y `§ 51 Kc 21` y **no da ningún `Kc` para el 49**, que es el
testimonio del propio Smith de que Kaccāyana no tiene sutta correspondiente.

### Para qué NO conviene: el texto entero por OCR

Es la tentación y es la trampa que este proyecto ya conoce. `CLAUDE.md` lo
dice del PDF de U Sīlānanda y vale igual aquí: el OCR sobre pāḷi romanizado
con diacríticos completos es justamente el trabajo del que hay que
desconfiar. Y esta página es peor que aquélla: mezcla redonda y cursiva con
valor distintivo, lleva números de nota voladitos, numeración de línea al
margen, y un aparato en cuerpo menor con sus propias abreviaturas. Un OCR que
confunda `ṭ` con `t`, o que se coma una cursiva, produce texto que **parece**
bueno y no lo es —y no tenemos contra qué cotejarlo, que es la definición del
problema—.

**Norma, entonces:** el Smith se usa **por página y a la vista**, para cotejar
y para leer el aparato. Si alguna vez se quisiera el texto entero, se
diagnostica primero, se pilota un capítulo, y se mide contra el texto de
Bhaddacak antes de creerle nada a la máquina.

### Cómo se hace, en concreto

    pdftoppm -png -r 150 -f <pág> -l <pág> "<archivo>.pdf" <salida>

La página impresa **no** coincide con la del PDF: en este volumen la impresa
617 es la 24 del PDF (la numeración de Smith es continua a través de las tres
partes del Saddanīti, y el Suttamālā empieza pasada la 600).

**Los PDF no viajan con el repositorio**: `*.pdf` está en `.gitignore`, como los
del Saddanīti y el Abhidhāna. Se quedan en la carpeta del IEBH.

---

## 3. Lo que sigue faltando

- **La Rūpasiddhi** en texto: sólo la tenemos a través de `/kaccrupa`, con la
  misma advertencia de erratas.
- **El aparato de variantes del OSBCT** (Sī, Syā, Kaṃ, I, Ka). `corpus-formas.json`
  se construyó con el «aparato quitado», de modo que desde este repositorio no se
  puede saber qué lee otra edición en un pasaje dado. Lo tiene el proyecto OSBCT.
- **El texto corrido del canon.** Aquí hay formas con cuentas —681.927 formas,
  8.062.163 fichas— y eso permite CONTAR pero no LEER el contexto. También es
  del OSBCT.
