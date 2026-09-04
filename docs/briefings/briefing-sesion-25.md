# Kaccāyana Pāḷi-Español: Briefing de la Sesión 25

*Complementa a los briefings 05–24. Tema único: **el capítulo 5, Taddhita,
traducido entero en borrador** (§344–§405, tres tandas). No se tocó el
emparejador de negritas; la decisión aprobada sobre él está en §4.*

> **Lo primero que tiene que saber el chat nuevo:** el Taddhita está
> traducido en borrador completo y espera la revisión del IEBH. El
> capítulo 6 (Ākhyāta) **no tiene fuente en el repositorio ni en el
> proyecto**: lo primero es pedírsela al IEBH. La revisión del capítulo 5
> continuará en el chat de la sesión 25, que queda abierto.

---

## 1. ESTADO AL CIERRE

HEAD: **`2dbb2526`** («convenciones: §0, registro del español»), publicado
en `origin/main`. Comprobado sin ejecutar git, leyendo
`.git/refs/heads/main` y `.git/logs/HEAD` como texto. **Ese commit no
figura en el §1 del briefing 24** (se hizo tras cerrarlo); queda
registrado aquí.

**Cinco archivos nuevos sin confirmar**, todos de esta sesión:

| Archivo | Qué es |
| --- | --- |
| `docs/5 - Taddhita-Kaccāyana.md` | Fuente Nandisena, cap. 5. Copiada de la subida del IEBH al chat; **md5 idéntico** al original |
| `docs/5. Taddhita-Rūpasiddhi.md` | Rūpasiddhi cap. 5, para cotejo. Ídem |
| `docs/borradores/sesion-25-suttas-344-363.md` | Primera tanda |
| `docs/borradores/sesion-25-suttas-364-383.md` | Segunda tanda |
| `docs/borradores/sesion-25-suttas-384-405.md` | Tercera tanda, con fórmulas de cierre provisionales |

Confirmarlos y publicarlos corresponde al IEBH.

## 2. EL TADDHITA, TRADUCIDO EN BORRADOR

62 suttas (§344–§405), un solo kaṇḍa (el octavo del Nāma). Tandas de
20/20/22 decididas por IEBH. Formato idéntico a los borradores del
Samāsa (sesiones 11 y 13): desgloses según Thitzana, pāḷi cotejado con
Pind (desfase +2: Nandisena §344–§405 = Pind 346–407, comprobado en todo
el capítulo), referencias canónicas retiradas del cuerpo y tabuladas al
final, erratas literales en el cuerpo con propuesta en las NOTAS DE
TRABAJO, notas al pie 1–44 de Nandisena más la 45 del traductor.

**Método de copia y verificación, que es lo reutilizable:**

- Las fuentes llegaron por subida al chat (la caché del proyecto no es
  visible para el shell; una subida sí, y permite `cp` byte a byte con
  md5). **No copiar fuentes a mano a través del contexto.**
- Cada párrafo pāḷi de los borradores se verificó mecánicamente contra la
  fuente (normalizando espacios, comillas y negritas, y descontando las
  referencias retiradas): 79 + 46 + 82 párrafos, todos reproducidos.
- La verificación cazó un error real de transcripción: «saṅkyānaṃ» por
  «saṅk**h**yānaṃ» en la vutti de §395. Es la clase de error de un solo
  carácter que las VARIANTES del emparejador documentan. **Ningún
  borrador de fuente se da por bueno sin esta comprobación.**

**Decisiones que esperan al IEBH** (el §8 de cada borrador las lista; lo
gordo): erratas literales (Vesamitttī §344, evamādisto/honti §368,
nava §390, pacccaye §400, vuddhī §405…); la DUDA del verso de §352 («na
vade»); samūha «conjunto» frente a samuccaya «colección»; el Rūpasiddhi
«0» de §377 (cómo lo registra la numeración triple); la grafía vacilante
saṅkyā/saṅkhyā; los superíndices restaurados de §394–§395 (la capa de
texto imprime «1014» por 10¹⁴; **cotejar con el PDF**); el título de
§401, que Nandisena deja «[Sutta has not been translated]» y cuya
traducción es nuestra (nota 45). El montaje del capítulo (entrada en
`CAPITULOS`, `concordancia.json`, tarjeta del índice) queda para después
de la revisión.

**Siglas nuevas para el repertorio del emparejador** cuando se restituya
la negrita del cap. 5: DAA, Mhvs, Sārattha-Ṭīkā, Abh (≠Abhi), PvA, SnA,
VvA, AbhA (≠AbhiA), «Vin.A.» (con punto interior), «Vin ii» (sin punto),
y las referencias con texto incrustado («-Sad. sutta 850», «-piṭṭhesu pi
passitabbaṃ»). `RE_SALTABLE` no reconoce ninguna.

## 3. GLOSARIO: PROPUESTAS ACUMULADAS

Cada borrador trae su §5/§6 de términos propuestos (apacca, gottagaṇa,
samūha, sippa, bhāva, visesa, tad ass’ atthi, saṅkhyāpūraṇa, ekasesa,
gaṇana, nipātana, pakāravacana, sabbanāma, asaṃyoganta, y el juego
cerrado vuddhi/lopa/āgama/vikāra/viparīta/ādesa, entre otros). **Ninguno
está aún en `comun/glosario.md`**: entran cuando IEBH los apruebe.

## 4. EL EMPAREJADOR: APROBADO Y NO IMPLEMENTADO

El IEBH aprobó §4.2 del briefing 24 (longest-first) **con puerta de
superconjunto**: el conjunto de líneas colocadas tras el cambio debe
contener al de ahora —no basta que suba la cuenta—; si alguna línea hoy
colocada deserta, parar y mirarla antes de seguir. Corre contra los dos
capítulos, reconstrucción OK en ambos, y las nueve ganancias se cotejan a
ojo antes de aplicar. **Sin implementar: no se tocó código.**

Dos observaciones de esta sesión que el implementador debe saber:

1. **Las cuentas del prototipo del 24 no cuadran**: 443+18+32=493 frente
   a 452+11+38=501. El emparejador actual tiene un cuarto desenlace
   silencioso: en `restituir_negritas.py`, cuando una línea repetida
   tiene más apariciones en el PDF que en el maestro, el
   `if orden < len(hits)` la deja caer sin contarla en colocadas,
   ambiguas ni ausentes. Resolver esa contabilidad antes de leer la tabla
   del prototipo como coste.
2. **La vía de §70 propuesta en el briefing 24 no puede funcionar tal
   cual**: dice «descartar la puntuación sólo del lado del PDF», pero la
   coma sobrante está en el maestro. Alternativa con la misma forma que
   la puerta de arriba: una segunda pasada **sólo sobre las ausentes**,
   ciega a la puntuación, que acepta un hit sólo si es único — una línea
   que hoy no encuentra nada no tiene colocación correcta que perder.
   Sin medir.

## 5. LO QUE SIGUE ABIERTO (herencia de la 24, sin cambios)

Todo el §7 del briefing 24 sigue vigente: §70 y §92 de la negrita, las
32 ausentes y 18 ambiguas del Nāma, las tres citas canónicas (§315
cerrable sin más), las 2379 desinencias de paradigmas, el Nyāsa sin
constar en `CLAUDE.md`, pañcamī/sattamī sin llegar al glosario, las
referencias bibliográficas del Nāma nunca restituidas (§10.1), el permiso
de la marca, la descripción de Zenodo, `docs/1. Sandhi-Kappa.md`. La
pregunta «¿qué capítulo sigue?» quedó contestada: **el 6, Ākhyāta, en un
chat nuevo**.

## 6. CAPÍTULO 6 (ĀKHYĀTA): QUÉ NECESITA EL CHAT NUEVO

1. **La fuente no existe** ni en `docs/` ni en el proyecto de claude.ai
   (sólo está `docs/fuentes/nyasa/Nyasa-06-akhyata.md`, que es el
   comentario, no la base). Pedir al IEBH el capítulo 6 de Nandisena — y
   el de la Rūpasiddhi si quiere cotejo — **subidos al chat**, que es el
   canal byte a byte; copiarlos a `docs/` con md5, como en §2.
2. Leer primero este briefing; `comun/convenciones.md` §0 es normativo.
3. Formato y flujo: los tres borradores de la sesión 25 son la plantilla
   —tandas acordadas con IEBH, desgloses de Thitzana, cotejo con Pind
   (localizar el desfase de numeración para el Ākhyāta), referencias a
   tabla, erratas literales, verificación mecánica de cada párrafo pāḷi.
4. En Thitzana (vol. 2) y Pind los capítulos de Ākhyāta se localizan con
   `Grep` sobre los archivos de la caché del proyecto, como se hizo aquí.
5. La revisión del capítulo 5 **no** es asunto del chat nuevo: sigue en
   el chat de la sesión 25.

## 7. RECORDATORIOS QUE NO CAMBIAN

Los del §8 del briefing 24, íntegros: nada de git desde el sandbox (ni
`status`); con IEBH en inglés, **la respuesta entera, también los
bloques para copiar**; el producto en español; nada de calcos
(«commitear», «empujado») — `comun/convenciones.md` §0; los PDF no viven
en el repositorio; todo cambio del emparejador corre contra los dos
capítulos; `reconstrucción: OK` no dice que la negrita esté bien puesta;
nada se edita en `site/` salvo `pali.css`, `pali.js` y los SVG; lo de
Thitzana se señala como suyo y su flecha va al revés; ante duda,
`<!-- DUDA -->`; **proponer y verificar, nunca afirmar**; el briefing se
escribe cuando ya no se va a tocar nada más.
