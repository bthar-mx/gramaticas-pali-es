#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Las operaciones de sandhi, hacia adelante. Una por aforismo.

Cada función recibe las dos voces y devuelve la lista de pasos, con la
convención del `CLAUDE.md` §3: el texto primero, los segmentos separados por
espacios, la cita entre paréntesis al final. Devuelve `None` si la operación no
puede aplicarse a ese par.

**Estas funciones no deciden.** Aplican. Quien decide es la recomposición: el
solucionador prueba todas y se queda con las que reproducen exactamente la
forma de entrada.

Cada una lleva arriba el enunciado que implementa, tal como está en el banco.
Ninguna operación se agrega sin enunciado: si un cambio no está enunciado, la
forma queda sin resolver y se dice por qué.

§10 y §11 son el andamiaje: §10 separa la consonante final sin vocal de la voz
**anterior** —nunca de la siguiente—, §11 vuelve a unir al final.
"""

import re
import unicodedata

VOCALES = "aāiīuūeo"
LARGA = {"a": "ā", "i": "ī", "u": "ū"}
CORTA = {v: k for k, v in LARGA.items()}

# Las cinco series y su nasal final, que es «la última consonante del grupo».
VAGGA = {
    "k": "ṅ", "kh": "ṅ", "g": "ṅ", "gh": "ṅ", "ṅ": "ṅ",
    "c": "ñ", "ch": "ñ", "j": "ñ", "jh": "ñ", "ñ": "ñ",
    "ṭ": "ṇ", "ṭh": "ṇ", "ḍ": "ṇ", "ḍh": "ṇ", "ṇ": "ṇ",
    "t": "n", "th": "n", "d": "n", "dh": "n", "n": "n",
    "p": "m", "ph": "m", "b": "m", "bh": "m", "m": "m",
}
# La segunda y cuarta de cada serie, y la primera y tercera con que se duplican
# (§29). La segunda va sobre la primera, la cuarta sobre la tercera.
SEGUNDA_CUARTA = {"kh": "k", "gh": "g", "ch": "c", "jh": "j",
                  "ṭh": "ṭ", "ḍh": "ḍ", "th": "t", "dh": "d",
                  "ph": "p", "bh": "b"}
DIGRAFOS = tuple(SEGUNDA_CUARTA)

# §269, con la ampliación que el propio documento enuncia debajo de la regla.
CONJUNTAS = {"ty": "c", "ly": "l", "ny": "ñ", "dy": "j", "sy": "s",
             "thy": "ch", "dhy": "jh", "ṇy": "ñ"}

# La lista de la Rūpasiddhi Nāma que fija el grupo de «mana» (§183).
GRUPO_MANA = {"vaca", "vaya", "teja", "tapa", "ceta", "tama", "yasa",
              "aya", "paya", "sira", "chanda", "sara", "ura", "raha",
              "aha", "mana"}


def nfc(t):
    return unicodedata.normalize("NFC", t)


def cot(t):
    t = nfc(t).replace("’", "").replace("'", "").replace("-", "")
    return re.sub(r"\s+", "", t).lower().replace("ṁ", "ṃ")


def primera_letra(t):
    return t[:2] if t[:2] in DIGRAFOS or t[:2] in VAGGA else t[:1]


def cierre(pasos, unido, atestiguada):
    """Añade §11 y, si procede, el paso de la edición moderna.

    `atestiguada=None` es el **modo enumeración**: no se compara contra nada y
    se devuelven los pasos tal como salen. Sirve para preguntar «¿qué formas
    pueden dar estas dos voces?» —el paso que falta cuando la edición separó el
    sandhi y hay que reconstruir la forma unida—.

    **Ese modo no publica nada por sí solo.** Lo que enumera vuelve a entrar por
    la puerta de siempre: cada forma candidata se le da al solucionador y sólo
    sobrevive si se descompone exactamente en las dos voces de partida. La
    verificación por recomposición sigue siendo la única que autoriza un paso;
    lo único que cambia es de qué lado se entra.
    """
    pasos = list(pasos) + ["{0} (§11)".format(unido)]
    if atestiguada is None:
        return pasos
    if cot(unido) != cot(atestiguada):
        return None
    if nfc(atestiguada).strip() != nfc(unido).strip():
        pasos.append("{0} (EM)".format(atestiguada))
    return pasos


def sep10(a, b):
    """§10 sobre la voz anterior: raíz · vocal final · voz siguiente."""
    if not a or a[-1] not in VOCALES or len(a) < 2:
        return None
    return a[:-1], a[-1]


# ── Vocal + vocal ───────────────────────────────────────────────────────

def op_14(a, b, F):
    """§14 — «A veces las vocales "i", "ī" y "u", "ū", cuando siguen a una
    vocal disímil que ha sido elidida, se convierten en "e" y "o"
    respectivamente». La disímil es sólo «a» y «ā» (nota 3)."""
    s = sep10(a, b)
    if not s or not b or b[0] not in "iīuū" or s[1] not in "aā":
        return None
    raiz, v = s
    nuevo = ("e" if b[0] in "iī" else "o") + b[1:]
    return cierre(["{0} {1}".format(a, b),
                   "{0} {1} {2} (§10)".format(raiz, v, b),
                   "{0} {1} (§12)".format(raiz, b),
                   "{0} {1} (§14)".format(raiz, nuevo)], raiz + nuevo, F)


def op_19(a, b, F):
    """§19 — «la sílaba "ti" de "ati", "pati" y "iti" se convierte en "c" y
    ésta se duplica». La duplicación la hace §28."""
    if a[-2:] != "ti" or a[:-2] not in ("a", "pa", "i") or not b or b[0] not in VOCALES:
        return None
    raiz = a[:-2]
    return cierre(["{0} {1}".format(a, b),
                   "{0}c {1} (§19)".format(raiz, b),
                   "{0}cc {1} (§28)".format(raiz, b)], raiz + "cc" + b, F)


def op_20(a, b, F):
    """§20 — «la sílaba "dha" de "idha", se convierte en "da"»."""
    if a != "idha" or not b or b[0] not in VOCALES:
        return None
    return cierre(["{0} {1}".format(a, b),
                   "ida {0} (§20)".format(b)], "ida" + b, F)


def op_22(a, b, F):
    """§22 — «después de "yathā" y "tathā", la "e" de "eva" se convierte en
    "ri"»."""
    if a not in ("yathā", "tathā") or b != "eva":
        return None
    corto = a[:-1] + "a"
    return cierre(["{0} {1}".format(a, b),
                   "{0} riva (§22)".format(a),
                   "{0} riva (§22)".format(corto)], corto + "riva", F)


# ── Vocal + consonante ──────────────────────────────────────────────────

def op_25(a, b, F):
    """§25 — «una vocal, cuando va seguida por una consonante, se alarga»."""
    if not a or a[-1] not in LARGA or not b or b[0] in VOCALES:
        return None
    largo = a[:-1] + LARGA[a[-1]]
    pasos = ["{0} {1}".format(a, b),
             "{0} {1} (§25)".format(largo, b)]
    return cierre(pasos, largo + b, F) or cierre(pasos, largo + " " + b, F)


def op_26(a, b, F):
    """§26 — «una vocal, cuando va seguida por una consonante, se acorta»."""
    if not a or a[-1] not in CORTA or not b or b[0] in VOCALES:
        return None
    corto = a[:-1] + CORTA[a[-1]]
    pasos = ["{0} {1}".format(a, b),
             "{0} {1} (§26)".format(corto, b)]
    return cierre(pasos, corto + b, F) or cierre(pasos, corto + " " + b, F)


def op_27(a, b, F):
    """§27 — «la "o" de "eta" y "ta", cuando va seguida por una consonante, se
    elide». El propio banco muestra el paso doble: se elide y queda "a"."""
    # El enunciado nombra **«eta» y «ta»**, no «cualquier voz terminada en o».
    # Sin esta restricción salían 308 lecturas falsas en 1.200 formas del
    # corpus, con primeras voces `ko`, `vippo`, `ano`… bajo un aforismo que no
    # las licencia. Las cuatro formas del banco que usan §27 son `eso dhammo`,
    # `so sīlavā`, `eso attho` y `eso ābhogo`: las dos voces son `eso` y `so`.
    if a not in ("eso", "so") or not b or b[0] in VOCALES:
        return None
    raiz = a[:-1]
    return cierre(["{0} {1}".format(a, b),
                   "{0} o {1} (§10)".format(raiz, b),
                   "{0} {1}, {0} a {1} (§27)".format(raiz, b)], raiz + "a " + b, F)


def op_29(a, b, F):
    """§29 — «la segunda y cuarta consonante de las agrupadas se duplican en la
    primera y tercera de las agrupadas respectivamente»."""
    if not a or a[-1] not in VOCALES:
        return None
    ini = primera_letra(b)
    if ini not in SEGUNDA_CUARTA:
        return None
    doble = SEGUNDA_CUARTA[ini] + b
    return cierre(["{0} {1}".format(a, b),
                   "{0} {1} (§29)".format(a, doble)], a + doble, F)


def op_36(a, b, F):
    """§36 — «cuando una consonante sigue, hay insersión de la letra "o"»."""
    s = sep10(a, b)
    if not s or not b or b[0] in VOCALES:
        return None
    raiz, v = s
    return cierre(["{0} {1}".format(a, b),
                   "{0} {1} {2} (§10)".format(raiz, v, b),
                   "{0} {1} (§12)".format(raiz, b),
                   "{0} o {1} (§36)".format(raiz, b)], raiz + "o" + b, F)


def op_44(a, b, F):
    """§44 — «el prefijo "abhi" cuando va seguido por una vocal se substituye
    por "abbh"»."""
    if a != "abhi" or not b or b[0] not in VOCALES:
        return None
    return cierre(["{0} {1}".format(a, b),
                   "abbh {0} (§44)".format(b)], "abbh" + b, F)


def op_45(a, b, F):
    """§45 — «el prefijo "adhi" cuando va seguido por una vocal se substituye
    por "ajjh"»."""
    if a != "adhi" or not b or b[0] not in VOCALES:
        return None
    return cierre(["{0} {1}".format(a, b),
                   "ajjh {0} (§45)".format(b)], "ajjh" + b, F)


def op_48(a, b, F):
    """§48 — «el prefijo "pati" cuando va seguido por una vocal o una
    consonante, se convierte en "paṭi"»."""
    if a != "pati":
        return None
    return cierre(["{0} {1}".format(a, b),
                   "paṭi {0} (§48)".format(b)], "paṭi" + b, F)


def op_49(a, b, F):
    """§49 — «cuando va seguida por una consonante, la vocal final de "putha"
    se convierte en "u"». El paso de duplicación lo hace §28."""
    if a != "putha" or not b or b[0] in VOCALES:
        return None
    ini = primera_letra(b)
    salidas = ["puthu" + b]
    pasos = ["{0} {1}".format(a, b),
             "puth a {0} (§10)".format(b),
             "puth u {0} (§49)".format(b)]
    r = cierre(pasos, "puthu" + b, F)
    if r:
        return r
    return cierre(pasos + ["puth u {0}{1} (§28)".format(ini, b)],
                  "puthu" + ini + b, F)


def op_50(a, b, F):
    """§50 — «cuando va seguido por una consonante, el prefijo "ava" se
    convierte en "o"»."""
    if a != "ava" or not b or b[0] in VOCALES:
        return None
    return cierre(["{0} {1}".format(a, b),
                   "o {0} (§50)".format(b)], "o" + b, F)


def op_79(a, b, F):
    """§79 — «la letra "o", la substitución del prefijo "ava", se convierte en
    "u"». Va después de §50, y §28 duplica."""
    if a != "ava" or not b or b[0] in VOCALES:
        return None
    ini = primera_letra(b)
    pasos = ["{0} {1}".format(a, b),
             "o {0} (§50)".format(b),
             "u {0} (§79)".format(b)]
    r = cierre(pasos, "u" + b, F)
    if r:
        return r
    return cierre(pasos + ["u {0}{1} (§28)".format(ini, b)], "u" + ini + b, F)


def op_183(a, b, F):
    """§183 — «cuando hay elisión de la inflexión nominal, la vocal final del
    grupo de "mana" se convierte en "o"». El grupo lo fija la lista de la
    Rūpasiddhi Nāma."""
    if a not in GRUPO_MANA:
        return None
    return cierre(["{0} {1}".format(a, b),
                   "{0} {1} {2} (§10)".format(a[:-1], a[-1], b),
                   "{0} o {1} (§183)".format(a[:-1], b)], a[:-1] + "o" + b, F)


def op_269(a, b, F):
    """§269 — «las consonantes conjuntas "ty", "ly", "ny", "dy" se convierten
    en "c", "l", "ñ", "j" respectivamente y después éstas se duplican». El
    documento amplía debajo a "sy", "thy", "dhy", "ṇy" y a los vaggas con "y".
    Va después de §21, que produce la conjunta."""
    s = sep10(a, b)
    if not s or not b or b[0] not in VOCALES:
        return None
    raiz, v = s
    if v not in "iī":
        return None
    conj = primera_letra(raiz[-1:]) + "y"
    if conj not in CONJUNTAS:
        return None
    nueva = CONJUNTAS[conj]
    base = raiz[:-1]
    pasos = ["{0} {1}".format(a, b),
             "{0} {1} {2} (§10)".format(raiz, v, b),
             "{0} y {1} (§21)".format(raiz, b),
             "{0} {1} (§269)".format(base + nueva, b),
             "{0} {1} (§28)".format(base + nueva + nueva, b)]
    return cierre(pasos, base + nueva + nueva + b, F)


# ── Niggahīta ───────────────────────────────────────────────────────────

def op_31(a, b, F):
    """§31 — «cuando va seguida por una consonante agrupada, la "niggahīta" se
    convierte en la última consonante del grupo». La nota 14 da la tabla:
    k→ṅ, c→ñ, ṭ→ṇ, t→n, p→m."""
    if not a.endswith("ṃ"):
        return None
    ini = primera_letra(b)
    if ini not in VAGGA:
        return None
    nuevo = a[:-1] + VAGGA[ini]
    pasos = ["{0} {1}".format(a, b), "{0} {1} (§31)".format(nuevo, b)]
    return cierre(pasos, nuevo + b, F) or cierre(pasos, nuevo + " " + b, F)


def op_31_l(a, b, F):
    """El «vā» de §31: la niggahīta se vuelve «l» ante «l».

    Su regla niggahita 2 lo enuncia y §31 no: «A veces, cuando la consonante
    "l" sigue, la "niggahīta" del prefijo "saṃ" y del final de "puma" se
    convierte en "l".» Por eso va restringida a esas dos voces y no a cualquier
    palabra terminada en niggahīta: `saṃ + lakkhaṇā`, `saṃ + lekho`,
    `puṃ + liṅgaṃ`. Las tres están en sus 261 formas.
    """
    if a not in ("saṃ", "puṃ") or not b.startswith("l"):
        return None
    nuevo = a[:-1] + "l"
    pasos = ["{0} {1}".format(a, b),
             '{0} {1} (por "vā" en §31)'.format(nuevo, b)]
    return cierre(pasos, nuevo + b, F) or cierre(pasos, nuevo + " " + b, F)


def op_S49(a, b, F):
    """Saddanīti Suttamālā 49 — la 'i' se vuelve 'v' ante la 'e' de «eva».

    **Es la primera operación del motor que NO es de Kaccāyana**, y por eso
    se cita con su obra entera y no con un «§N» a secas, que en esta página
    significa Kaccāyana.

        49. Evass' ekāre itiss' aññassa c' issa vo.
        Evasaddassa ekāre pare itisaddassa aññassa ca saddassa issa vakāro
        hoti kvaci: «itv eva coro asim āvudhañ ca; vilapatv eva so dijo;
        Isigili tv eva; Samantapāsādikā tv eva». Kvacī ti kiṃ: icc eva.

    Cotejado contra Helmer Smith, Saddanīti III (Suttamālā), p. 617. Los
    cuatro ejemplos son suyos; el texto romanizado de Bhaddacak sólo trae el
    primero. Véase `docs/solucionador/tveva-dos-lecturas.md`.

    Kaccāyana no tiene sutta correspondiente, y no es conjetura: el aparato
    de Smith da «Kc» para los suttas 50 y 51 y NINGUNO para el 49; y en el
    texto entero de Kaccāyana y la Rūpasiddhi no aparece «itveva» ni
    «tveva» ni «tyeva» una sola vez.

    DOS RESTRICCIONES, y las dos son del texto, no prudencia nuestra:

    1. **Sólo ante «eva»**, porque el sutta dice «evassa ekāre» — ante la
       'e' de la palabra «eva»—. Es lo que impide que esta regla se dispare
       en cualquier juntura con 'i' final: no es una sustitución general.
    2. **Sólo 'i', no 'ī'.** El sutta dice «issa», la letra 'i'. Es la misma
       lectura estricta que el proyecto ya hace con §18, que dice
       «okāra-ukāra» y por eso no cubre «ū», frente a §21, que dice
       «ivaṇṇo» —la clase— y por eso sí cubre «ī».

    Y no es sólo de «iti»: el sutta dice «itisaddassa aññassa ca saddassa»
    —la 'i' de «iti» Y la de otra palabra—, y su propio ejemplo «vilapatv
    eva» viene de «vilapati», que es verbo, no partícula.
    """
    # ALCANCE, y esto es una restricción NUESTRA, no del sutta: se exige que
    # la primera voz acabe en «-ti». El sutta dice «issa» —la 'i'— y añade
    # «aññassa ca saddassa» —y la de otra palabra—, de modo que su enunciado
    # es más ancho. Pero sus CUATRO ejemplos son unánimemente «-ti»: «itv
    # eva» (iti), «vilapatv eva» (vilapati), y «Isigili tv eva» y
    # «Samantapāsādikā tv eva», donde la 'i' es la del «ti» citativo.
    #
    # Medido sobre las 681.927 formas de la edición: sin la restricción el
    # sutta gana 248 formas (masa 1.821); con ella, 234 (masa 1.276). Las 14
    # que quedan fuera son todas falsas —«sveva» leído «si + eva» cuando es
    # «so + eva» (§18), «dveva» leído «di + eva» cuando es «dve + eva», y
    # «dvevassasahassāyukā», que es «dve vassasahassāyukā»—, y se apoyan en
    # voces que la edición trae una o dos veces. Sin la restricción, «sv
    # eva» del banco salía con una octava lectura falsa y arnes.js lo
    # detenía; con ella, los cinco arneses pasan.
    #
    # <!-- DUDA: estrechar el enunciado es decisión del IEBH, no del motor.
    #      Si se prefiere el sutta tal como está escrito, quítese la
    #      condición de «-ti» y acéptese la lectura falsa de «sveva». -->
    if not a or not a.endswith("ti") or not b.startswith("eva"):
        return None
    nuevo = a[:-1] + "v"
    pasos = ["{0} {1}".format(a, b),
             "{0} {1} {2} (§10)".format(a[:-1], "i", b),
             "{0} {1} {2} (Saddanīti Suttamālā §49)".format(a[:-1], "v", b)]
    return cierre(pasos, nuevo + b, F)


def op_35_l(a, b, F):
    """La «ḷ» que se inserta después de «cha».

    §35 enumera ocho consonantes —«Ya-va-ma-da-na-ta-ra-lā»— y la «ḷ» no está
    entre ellas. Pero **la nota 9 de su documento sí la enuncia**: «Se inserta
    "ḷ" después de "cha" y numerales.» De ahí sale `cha-ḷ-abhiññā`, que está en
    sus 261 formas. Se implementa por la nota y se cita por la nota, no
    estirando la lista del aforismo, que dice lo que dice.
    """
    if a != "cha" or not b or b[0] not in VOCALES:
        return None
    pasos = ["{0} {1}".format(a, b),
             "{0} ḷ {1} (§35, nota 9)".format(a, b)]
    return cierre(pasos, a + "ḷ" + b, F) or cierre(pasos, a + "ḷ " + b, F)


def op_32(a, b, F):
    """§32 — «cuando "eva" y "hi" siguen, la "niggahīta" se convierte en "ñ"; y
    ésta se duplica cuando va seguida por "eva"»."""
    if not a.endswith("ṃ") or b not in ("eva", "hi"):
        return None
    base = a[:-1] + "ñ"
    if b == "hi":
        # **La forma unida primero.** Probando antes la separada, §11 «unía»
        # sin unir: de «taṃ hi» salía «tañ hi (§32) · tañ hi (§11)», dos pasos
        # con el mismo texto, y §11 dice trasladar la consonante a la letra
        # siguiente. La secuencia del banco lo hace al revés y bien: «tañhi
        # (§11)» y después «tañ hi (EM)», que es la edición moderna.
        pasos = ["{0} {1}".format(a, b), "{0} hi (§32)".format(base)]
        return cierre(pasos, base + "hi", F) or cierre(pasos, base + " hi", F)
    pasos = ["{0} {1}".format(a, b),
             "{0} eva (§32)".format(base),
             "{0} ñeva (§28)".format(base)]
    return cierre(pasos, base + "ñeva", F) or cierre(pasos, base + " ñeva", F)


def op_33(a, b, F):
    """§33 — «cuando "y" sigue, la "niggahīta" junto con "y" se convierte en
    "ñ"; y ésta se duplica». Sólo para el prefijo "saṃ" y ante el pronombre
    "ya" (nota 15)."""
    if not a.endswith("ṃ") or not b.startswith("y"):
        return None
    base = a[:-1] + "ñ"
    resto = b[1:]
    pasos = ["{0} {1}".format(a, b),
             "{0} ñ{1} (§33)".format(base, resto)]
    return cierre(pasos, base + "ñ" + resto, F) or \
        cierre(pasos, base + " ñ" + resto, F)


def op_34(a, b, F):
    """§34 — «cuando una vocal sigue, la "niggahīta" se convierte en "m" y
    "d"». En "d" sólo después de "ya", "ta" y "eta" (nota 16)."""
    if not a.endswith("ṃ") or not b or b[0] not in VOCALES:
        return None
    for letra in ("m", "d"):
        if letra == "d" and a[:-1] not in ("ya", "ta", "eta"):
            continue
        nuevo = a[:-1] + letra
        r = cierre(["{0} {1}".format(a, b),
                    "{0} {1} (§34)".format(nuevo, b)], nuevo + b, F) or \
            cierre(["{0} {1}".format(a, b),
                    "{0} {1} (§34)".format(nuevo, b)], nuevo + " " + b, F)
        if r:
            return r
    return None


def op_37(a, b, F):
    """§37 — «cuando una vocal o una consonante sigue, se inserta la
    "niggahīta"»."""
    return cierre(["{0} {1}".format(a, b),
                   "{0} ṃ {1} (§37)".format(a, b)], a + "ṃ" + b, F) or \
        cierre(["{0} {1}".format(a, b),
                "{0} ṃ {1} (§37)".format(a, b)], a + "ṃ " + b, F)


def op_38(a, b, F):
    """§38 — «cuando una vocal sigue, la "niggahīta" se elide». La nota 17
    añade: elidida la niggahīta, se elide la vocal anterior y se alarga la
    siguiente."""
    if not a.endswith("ṃ") or not b or b[0] not in VOCALES:
        return None
    sin = a[:-1]
    pasos = ["{0} {1}".format(a, b), "{0} {1} (§38)".format(sin, b)]
    r = cierre(pasos, sin + b, F) or cierre(pasos, sin + " " + b, F)
    if r:
        return r
    s = sep10(sin, b)
    if not s or b[0] not in LARGA:
        return None
    raiz, v = s
    largo = LARGA[b[0]] + b[1:]
    return cierre(pasos + ["{0} {1} {2} (§10)".format(raiz, v, b),
                           "{0} {1} (§12)".format(raiz, b),
                           "{0} {1} (§15)".format(raiz, largo)], raiz + largo, F)


def op_39(a, b, F):
    """§39 — «cuando una consonante sigue, la "niggahīta" se elide»."""
    if not a.endswith("ṃ") or not b or b[0] in VOCALES:
        return None
    sin = a[:-1]
    pasos = ["{0} {1}".format(a, b), "{0} {1} (§39)".format(sin, b)]
    return cierre(pasos, sin + b, F) or cierre(pasos, sin + " " + b, F)


def op_40(a, b, F):
    """§40 — «la vocal después de la "niggahīta" se elide y la "niggahīta" se
    convierte en la consonante final del grupo correspondiente»."""
    if not a.endswith("ṃ") or not b or b[0] not in VOCALES or len(b) < 2:
        return None
    sinv = b[1:]
    ini = primera_letra(sinv)
    pasos = ["{0} {1}".format(a, b), "{0} {1} (§40)".format(a, sinv)]
    if ini in VAGGA:
        nuevo = a[:-1] + VAGGA[ini]
        pasos = pasos + ["{0} {1} (§31)".format(nuevo, sinv)]
        return (cierre(pasos, nuevo + sinv, F)
                or cierre(pasos, nuevo + " " + sinv, F))
    return cierre(pasos, a + sinv, F) or cierre(pasos, a + " " + sinv, F)


def op_41(a, b, F):
    """§41 — «cuando la vocal siguiente a la "niggahīta" se elide, si la
    consonante siguiente es conjunta, ésta se convierte en no-conjunta»."""
    if not a.endswith("ṃ") or not b or b[0] not in VOCALES or len(b) < 3:
        return None
    sinv = b[1:]
    if len(sinv) < 2 or sinv[0] != sinv[1]:
        return None
    simple = sinv[1:]
    pasos = ["{0} {1}".format(a, b),
             "{0} {1} (§40)".format(a, sinv),
             "{0} {1} (§41)".format(a, simple)]
    return cierre(pasos, a + simple, F) or cierre(pasos, a + " " + simple, F)


def op_51(a, b, F):
    """§51 — «a veces hay transposición de las letras "r", "h", "n"».

    Se aplica **sobre la voz anterior**, y después §11 une. Las tres formas del
    banco que dependen de este aforismo dicen exactamente qué clase de
    transposición es, y son tres clases distintas:

      · `bahvābādho` → `bavhābādho`  — «hv» pasa a «vh»: las dos letras son
        contiguas y se intercambian.
      · `na abhineyya` → `an abhineyya` → `anabhineyya` — «na» pasa a «an»: la
        «n» y la vocal se intercambian. **Ésta es la privativa**, y es el propio
        banco del Venerable el que la explica con §51.
      · `pariyudāhāsi` → `payirudāhāsi` — «r» e «y» se intercambian **con una
        letra en medio**: `r i y` pasa a `y i r`.

    Por eso se prueban los dos saltos, el contiguo y el de una letra en medio, y
    no más: los tres ejemplos del banco no dan pie a más. Quien decide sigue
    siendo la recomposición.
    """
    if not a:
        return None
    salidas = []
    for i in range(len(a)):
        if a[i] not in "rhn":
            continue
        for salto in (1, 2):
            for j in (i - salto, i + salto):
                if not (0 <= j < len(a)):
                    continue
                letras = list(a)
                letras[i], letras[j] = letras[j], letras[i]
                salidas.append("".join(letras))
    for trans in salidas:
        pasos = ["{0} {1}".format(a, b).strip(),
                 "{0} {1} (§51)".format(trans, b).strip()]
        r = (cierre(pasos, trans + b, F) or cierre(pasos, trans + " " + b, F)
             if b else cierre(pasos, trans, F))
        if r:
            return r
    return None


TODAS = {
    14: op_14, 19: op_19, 20: op_20, 22: op_22, 25: op_25, 26: op_26,
    27: op_27, 29: op_29, 31: op_31, 32: op_32, 33: op_33, 34: op_34,
    36: op_36, 37: op_37, 38: op_38, 39: op_39, 40: op_40, 41: op_41,
    44: op_44, 45: op_45, 48: op_48, 49: op_49, 50: op_50, 51: op_51,
    79: op_79, 183: op_183, 269: op_269,
}


# ── Cadenas de dos operaciones ──────────────────────────────────────────
# El banco encadena reglas, y una operación sola no llega a la forma. Estas
# dos cadenas están en sus propias secuencias, paso por paso; no se inventan.

# Cada uno de los tres aforismos de sustitución nombra **su** vocal, y hasta
# hoy el motor no lo comprobaba: citaba §17, §18 y §21 para el mismo par y
# dejaba que la recomposición eligiera. Como §17 y §21 producen la misma «y»,
# toda forma con «e» final salía además bajo §21, y toda forma con «i» final
# además bajo §17: dos referencias falsas por cada acierto. Los enunciados,
# del Sandhi-kappa:
#
#   §17 · «Yam edantass' ādeso» (Kac. 19) — «‘Y’ [es] la sustitución de la
#         ‘e’ final».                                     → sólo «e»
#   §18 · «Vam od-udantānaṃ» (Kac. 20) — «‘V’, de los que terminan en ‘o’ y
#         ‘u’»; la glosa: «Okār'-ukārānaṃ».               → sólo «o», «u»
#   §21 · «Ivaṇṇo yaṃ navā» (Kac. 21) — «la letra anterior ‘i’ (o ‘ī’),
#         ocasionalmente, se vuelve ‘y’».                 → sólo «i», «ī»
#
# §21 se llama «ivaṇṇa» —la *clase* de la i— y por eso el texto añade «ī» de
# forma expresa. §18 no dice «uvaṇṇa» sino «okāra-ukāra», las *letras* «o» y
# «u», y no nombra «ū». Se sigue el texto tal como está. Si aparece una forma
# que exija «ū», es una pregunta para el Venerable, no una licencia que
# tomarse aquí.
VOCAL_SUST = {17: "e", 18: "ou", 21: "iī"}
LETRA_SUST = {17: "y", 18: "v", 21: "y"}


def _sustitucion(a, b, n):
    """§10 y la sustitución de la vocal final por «y» o «v», si la vocal
    final es la que el aforismo `n` nombra. Devuelve (raíz, vocal, letra)."""
    s = sep10(a, b)
    if not s or not b or b[0] not in VOCALES:
        return None
    raiz, v = s
    if v not in VOCAL_SUST[n]:
        return None
    return raiz, v, LETRA_SUST[n]


CLASE_VOCAL = {"a": "a", "ā": "a", "i": "i", "ī": "i", "u": "u", "ū": "u",
               "e": "e", "o": "o"}


def licencia_elision_siguiente(a, b, n=None):
    """¿Licencia §13 (o su cadena con §16 o §38) la elisión de la vocal
    siguiente en este par?

    §13 es «Vā paro asarūpā» — la vocal siguiente se elide tras una vocal
    DISÍMIL (asarūpa)—. Adjudicación del IEBH (2026-08-29, observación
    sobre assasāmīti): cuando la vocal final y la inicial son de la misma
    clase (a/ā, i/ī, u/ū, e, o), la que se elide es la PRIMERA —§12, y la
    superviviente se alarga por §15—; §13 no cubre el par. La propia
    edición concuerda: tadāhaṃ, migīva y vadhūdaraṃ están bajo «una vocal
    que precede a otra se elide» (sara-sandhi, regla 1), y la secuencia
    derivada que los citaba por §13 era nuestra, no suya. Como con §17,
    §18 y §21: el derivador del Venerable no se toca — se deja de
    preguntarle por un aforismo cuyo enunciado no cubre el par.
    """
    prev = a[:-1] if a and a.endswith("ṃ") else a    # «38+13»: cae la niggahīta
    if not prev or not b:
        return True
    u, v = prev[-1], b[0]
    if (u in CLASE_VOCAL and v in CLASE_VOCAL
            and CLASE_VOCAL[u] == CLASE_VOCAL[v]):
        return False
    return True


def licencia_sustitucion(a, b, n):
    """¿Licencia el aforismo `n` esta sustitución?

    §17, §18 y §21 no son intercambiables: cada uno nombra su vocal final.
    Esta pregunta se hace **antes** de llamar al derivador del Venerable, que
    aplica los tres sin mirar la vocal —de «kho assa» sacaba «khv assa» bajo
    §17, bajo §18 y bajo §21, tres referencias donde el texto da una—. El
    archivo del Venerable no se toca; lo que cambia es que no se le pregunta
    por un aforismo cuyo enunciado no cubre el par.
    """
    return _sustitucion(a, b, n) is not None


def _cadena_sust_alarga(a, b, F, n, destino):
    """§17/§18/§21 y después §25.

    Del banco: «me ayaṃ · m e ayaṃ (§10) · m y ayaṃ (§17) · m y āyaṃ (§25)
    · myāyaṃ (§11)». La sustitución deja la conjunta y §25 alarga la vocal
    siguiente porque queda ante consonante.
    """
    s = _sustitucion(a, b, n)
    if not s or b[0] not in LARGA:
        return None
    raiz, v, letra = s
    largo = LARGA[b[0]] + b[1:]
    return cierre(["{0} {1}".format(a, b),
                   "{0} {1} {2} (§10)".format(raiz, v, b),
                   "{0} {1} {2} (§{3})".format(raiz, letra, b, n),
                   "{0} {1} {2} (§25)".format(raiz, letra, largo)],
                  raiz + letra + largo, F)


def op_17_25(a, b, F):
    return _cadena_sust_alarga(a, b, F, 17, "y")


def op_18_25(a, b, F):
    return _cadena_sust_alarga(a, b, F, 18, "v")


def op_21_25(a, b, F):
    return _cadena_sust_alarga(a, b, F, 21, "y")


def op_35_26(a, b, F):
    """§35 y después §26.

    Del banco, byañjana 2.2: «cuando se inserta una consonante» la vocal se
    acorta. «yathā idaṃ» da «yatha-y-idaṃ»: §35 inserta la «y» y §26 acorta
    la «ā» de «yathā».
    """
    if not a or a[-1] not in CORTA:
        return None
    corto = a[:-1] + CORTA[a[-1]]
    for letra in "yvmdntrlhg":
        r = cierre(["{0} {1}".format(a, b),
                    "{0} {1} {2} (§35)".format(a, letra, b),
                    "{0} {1} {2} (§26)".format(corto, letra, b)],
                   corto + letra + b, F)
        if r:
            return r
    return None


def _cadena_38(a, b, F, segunda):
    """§38 y después §12 o §13.

    §38 — «cuando una vocal sigue, la "niggahīta" se elide». Elidida la
    niggahīta, las dos voces quedan **vocal contra vocal**, y ahí §12 —«la
    vocal anterior se elide»— y §13 —«la vocal siguiente se elide»— se aplican
    por su propio enunciado, sin nada añadido. La nota 17 documenta una de las
    dos continuaciones —la que además alarga, §15, y que `op_38` ya cubre—;
    éstas son las otras dos, sin alargamiento.

    De «paripucchiṃ ahaṃ»: §38 deja «paripucchi ahaṃ», §12 elide la «i» y da
    «paripucchahaṃ», que es la forma atestiguada. De «cāriṃ ahaṃ»: §38 deja
    «cāri ahaṃ», §13 elide la «a» y da «cārihaṃ».
    """
    if not a.endswith("ṃ") or not b or b[0] not in VOCALES:
        return None
    sin = a[:-1]
    s = sep10(sin, b)
    if not s:
        return None
    raiz, v = s
    pasos = ["{0} {1}".format(a, b),
             "{0} {1} (§38)".format(sin, b),
             "{0} {1} {2} (§10)".format(raiz, v, b)]
    if segunda == 12:
        return cierre(pasos + ["{0} {1} (§12)".format(raiz, b)], raiz + b, F)
    if len(b) < 2:
        return None
    return cierre(pasos + ["{0} {1} {2} (§13)".format(raiz, v, b[1:])],
                  raiz + v + b[1:], F)


def op_38_12(a, b, F):
    return _cadena_38(a, b, F, 12)


def op_38_13(a, b, F):
    return _cadena_38(a, b, F, 13)


TODAS.update({"17+25": op_17_25, "18+25": op_18_25, "21+25": op_21_25,
              "35+26": op_35_26})
TODAS.update({"38+12": op_38_12, "38+13": op_38_13})
TODAS.update({"31vā": op_31_l, "35nota9": op_35_l})
# «S49» y no 49: el 49 de este motor es el de KACCĀYANA y está tomado.
TODAS.update({"S49": op_S49})


