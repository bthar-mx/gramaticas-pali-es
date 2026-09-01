#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Escribe el borrador inglés de la página del verbo.

    python3 herramientas/construir_ingles_verbo.py

Produce `recursos/verbo/ingles.json`. La INTERFAZ se publica siempre; la PROSA
—palabras del IEBH— sólo llega a la página cuando `"adjudicado"` es `true`,
igual que en `recursos/paradigmas/ingles.json`. **Está en `true` desde el
1-sep-2026, por encargo de Angel.** Volver a `false` basta para que la página
en inglés muestre otra vez el español con su aviso: no hay que tocar nada más.

La terminología no se inventa: sale de la propia traducción inglesa que
Bhikkhu Nandisena hizo del Ākhyāta-kappa, en `docs/6 - Ākhyāta-Kaccāyana.md`.
De ahí vienen tres criterios:

1. **Los nombres de las vibhatti no se traducen.** Él escribe «vattamānā»,
   «hiyyattanī», «sattamī», «pañcamī», «bhavissantī» entre comillas, y lo
   mismo «parassapada», «attanopada», «sabbadhātuka», «kārita». Se conserva
   el nombre pāḷi y se añade el equivalente inglés donde el español lo añade.
2. **El aparato estructural sí se traduce, y con sus palabras**: «root»,
   «person», «third / middle / first person», «conjugational sign»,
   «reduplication», «is elided», «substituted by».
3. **sattamī es «potential»**, no «optative»: es lo que él escribe, y lo que
   dice el español («potencial»).

Las formas pāḷi no se traducen nunca —son el objeto de la página— y las
referencias §N tampoco: son la cita, y es la misma en los dos idiomas.

Lo que queda por decidir, y por eso va sin adjudicar, está en
`docs/verbo/ingles-por-adjudicar.md`.
"""

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

DESTINO = os.path.join(RAIZ, "recursos", "verbo", "ingles.json")

# --------------------------------------------------------------- interfaz
# Esta capa SÍ se publica: son rótulos de la página, no palabras del IEBH.

INTERFAZ = {
    # El pāḷi del título va en su propio <span class="pali">: Fraunces no
    # lleva las combinadas y compone «ākhyāta» con el macron descolocado.
    "titulo": 'The <em>verb</em> · <span class="pali">ākhyāta</span>',
    "titulo_llano": "The verb · ākhyāta",
    "eyebrow": "Kaccāyana · chapter vi",
    "volver": "← Resources · Pāḷi Grammars",
    "sb_titulo": "The verb",
    "sb_sub": "ākhyāta · Kaccāyana vi",
    "indice": "Index",
    "arriba": "Back to top",
    "version": "Version",
    "version_nota": ("First version of the page. It brings together Bhikkhu "
                     "Nandisena's «Verbo» document and his thirteen class "
                     "presentations: 21 derivations with one operation per "
                     "row, the authority given as the Kaccāyana/Rūpasiddhi "
                     "pair —which the document did not give— and 105 "
                     "conjugation paradigms. Rows showing a form the source "
                     "does not print are marked, and the single corrected "
                     "erratum says what it was. The Ākhyāta-kappa is not yet "
                     "published as a chapter, so its §N appear as plain "
                     "text; they will link themselves once it is."),
    "entradilla": ("The eight verbal inflections of Pāḷi, the eight groups of "
                   "roots, <b>{escaleras} derivations</b> step by step with "
                   "the aphorism that authorises each operation, and "
                   "<b>{paradigmas} conjugation paradigms</b>."),
    "pestanas": {
        "introduccion": "Introduction",
        "inflexiones": "Inflections",
        "formacion": "Formation",
        "paradigmas": "Paradigms",
    },
    "cabeceras": {
        "paso": "step",
        "operaciones": "grammatical operations",
        "autoridad": "authority",
        "explicacion": "explanation",
    },
    "titulos": {
        "usos": "Uses of the verbal inflections",
        "voces": "The three voices",
        "ganas": "The eight groups of roots",
    },
    "marcas": {
        "propuesta": "proposed",
        "segun_documento": "according to the «Verbo» document",
        "segun_diapositiva": "according to {0}",
    },
    "leyendas": {
        "inflexiones": ("The eight series of endings. Each in its two groups "
                        "—<b>parassapada</b>, the word for another, and "
                        "<b>attanopada</b>, the word for oneself— and its "
                        "three persons."),
        "formacion": ("Each row shows the form <b>resulting</b> from the rule "
                      "beside it, so that the derivation can be checked line "
                      "by line. The authority is given as the pair "
                      "<b>Kaccāyana / Rūpasiddhi</b>: the document cites the "
                      "second number, and the first is that of the "
                      "corresponding chapter of Kaccāyana. Rows marked "
                      "<span class=\"marca-propuesta\">proposed</span> show an "
                      "intermediate form the source does not print, deduced "
                      "from the rule cited; the sign ✱ marks a corrected "
                      "authority, and says how."),
        "paradigmas": ("One hundred and five conjugation tables. Those of "
                       "<b>bhū</b> and <b>paca</b> are from the «Verbo» "
                       "document; those gathered under <b>other paradigms</b> "
                       "come from <i>The Higher Pali Course for Advanced "
                       "Students</i>, by the Venerable Buddhadatta Thera "
                       "(Colombo, 1951), as the document itself states."),
    },
    "tema": {"oscuro": "Dark mode", "claro": "Light mode"},
    "pie_aviso": ("The English of this page is the interface only. The prose "
                  "of the IEBH is shown in Spanish until the translation is "
                  "signed off."),
}

# ------------------------------------------------------------------ prosa
# Esta capa NO se publica mientras «adjudicado» sea false.

OPERACIONES = {
    "colocar la raíz": "place the root",
    "elidir la vocal final": "elide the final vowel",
    "elidir vocal final": "elide the final vowel",
    "elidir vocal final de ‘bhava’": "elide the final vowel of ‘bhava’",
    "colocar inflexión verbal": "place the verbal inflection",
    "colocar inflexión verbal presente indicativo":
        "place the verbal inflection, present indicative",
    "colocar inflexión verbal, presente indicativo":
        "place the verbal inflection, present indicative",
    "colocar signo de conjugación": "place the conjugational sign",
    "fortalecer vocal ‘ū’": "strengthen the vowel ‘ū’",
    "fortalecer la vocal": "strengthen the vowel",
    "fortalecer la vocal de la raíz": "strengthen the vowel of the root",
    "sustituir ‘o’ por ‘ava’": "replace ‘o’ with ‘ava’",
    "sustituir ‘o’ por ‘āva’": "replace ‘o’ with ‘āva’",
    "sustituir ‘v’ por ‘b’": "replace ‘v’ with ‘b’",
    "sustituir ‘ṃ’ por ’n’": "replace ‘ṃ’ with ‘n’",
    "se sustituye ’n’ por ‘ṇ’": "‘n’ is replaced by ‘ṇ’",
    "se acorta la vocal de la raíz": "the vowel of the root is shortened",
    "se elide ‘ha’ de la raíz": "‘ha’ of the root is elided",
    "elidir ‘y’": "elide ‘y’",
    "elidir ‘ṇ’": "elide ‘ṇ’",
    "duplicar ‘v’": "double ‘v’",
    "insertar ‘i’": "insert ‘i’",
    "colocar el sufijo ‘ya’": "place the suffix ‘ya’",
    "colocar sufijo ‘ya’": "place the suffix ‘ya’",
    "colocar sufijos causativos y asignar nombre “kārita”":
        "place the causative suffixes and assign the name “kārita”",
    "asimilación de ‘ya’ con ‘c’ - cya = cca":
        "assimilation of ‘ya’ with ‘c’ — cya = cca",
    "formar el verbo": "form the verb",
    "formar el verbo causativo": "form the causative verb",
}

GLOSAS = {
    "ser/estar": "to be",
    "existiendo/estando": "existing, being",
    "cocinar": "to cook",
    "cocinando": "cooking",
    "ir": "to go",
    "oprimir": "to press",
    "sacrificar": "to sacrifice",
    "obstruir": "to obstruct",
    "jugar": "to play",
    "oir/escuchar": "to hear, to listen",
    "vender": "to sell",
    "intercambio/comerciando": "exchange, trading",
    "extender": "to extend",
    "robar": "to steal",
    "agarrando": "grasping",
    "experimentando": "experiencing",
}

TIEMPOS = {
    "presente": "present",
    "imperativo": "imperative",
    "potencial": "potential",
    "imperfecto": "imperfect",
    "perfecto": "perfect",
    "aoristo": "aorist",
    "futuro": "future",
    "condicional": "conditional",
    "presente indicativo": "present indicative",
}

# Las notas que el documento pone bajo el título de algunas inflexiones.
NOTAS = {
    "inserción de ‘a’ es opcional": "insertion of ‘a’ is optional",
}

VOCES = {
    "voz activa": "active voice",
    "voz pasiva": "passive voice",
    "voz impersonal": "impersonal voice",
}

# Los rótulos de entrada de los paradigmas. La forma pāḷi no se toca; sólo se
# traduce la glosa que va entre paréntesis.
ENTRADAS = {
    "1a-bhū (ser/estar)": "1a-bhū (to be)",
    "1b-anu-bhū (experimentar)": "1b-anu-bhū (to experience)",
    "1c-bhū (ser/estar)": "1c-bhū (to be)",
    "2a-paca (cocinar)": "2a-paca (to cook)",
    "3-kara (hacer)": "3-kara (to do)",
    "4-hū (ser/estar)": "4-hū (to be)",
    "5-asa (ser/estar)": "5-asa (to be)",
    "6-vada (decir)": "6-vada (to say)",
    "7-vaca (decir/hablar)": "7-vaca (to say, to speak)",
    "8-dā (dar)": "8-dā (to give)",
    "9-disa (ver)": "9-disa (to see)",
    "10-ñā (comprender)": "10-ñā (to understand)",
    "11-brū (decir)": "11-brū (to say)",
    "12-ṭhā (estar parado)": "12-ṭhā (to stand)",
    "13-su (oír/escuchar)": "13-su (to hear, to listen)",
    "14-gaha (tomar/agarrar)": "14-gaha (to take, to grasp)",
    "15-e (venir)": "15-e (to come)",
    "16-hana (matar)": "16-hana (to kill)",
    "17-hara (llevar)": "17-hara (to carry)",
    "18-labha (obtener)": "18-labha (to obtain)",
    "19-upa-pada (nacer, reconectar)": "19-upa-pada (to be born, to reconnect)",
    "20-vi-hara (morar/vivir)": "20-vi-hara (to dwell, to live)",
}

# La línea de procedencia de cada grupo de paradigmas. Los títulos de obra y
# los nombres propios no se traducen; el de Buddhadatta ya viene en inglés.
OBRAS = {
    "Nandisena, «Verbo»": "Nandisena, «Verbo»",
    "Buddhadatta, The Higher Pali Course for Advanced Students, Colombo, 1951":
        "Buddhadatta, The Higher Pali Course for Advanced Students, "
        "Colombo, 1951",
}

PERSONAS = {
    "3a": "3rd", "2a": "2nd", "1a": "1st",
    "persona (purisa)": "person (purisa)",
}

# «Plural» con mayúscula sale de una sola tabla de inflexión del documento;
# las demás la escriben en minúscula. Se traduce tal como está.
NUMEROS = {
    "singular (ekavacana)": "singular (ekavacana)",
    "plural (bahuvacana)": "plural (bahuvacana)",
    "singular": "singular",
    "plural": "plural",
    "Plural": "Plural",
}

FORMACION = {
    "Formación: presente indicativo, tercera persona singular":
        "Formation: present indicative, third person singular",
    "Formación: voz pasiva, presente indicativo, tercera persona singular":
        "Formation: passive voice, present indicative, third person singular",
    "Formación: voz pasiva presente indicativo, tercera persona singular":
        "Formation: passive voice, present indicative, third person singular",
    "Formación: causativo, voz activa, presente indicativo, tercera persona "
    "singular":
        "Formation: causative, active voice, present indicative, third person "
        "singular",
    "Formación: causativo, voz pasiva, presente indicativo, tercera persona "
    "singular":
        "Formation: causative, passive voice, present indicative, third "
        "person singular",
    "Formación: causativo, presente indicativo, tercera persona singular":
        "Formation: causative, present indicative, third person singular",
}

# Cabeceras y celdas de las tres tablas de referencia. Las voces pāḷi entre
# paréntesis se conservan tal cual: son la cita, no la traducción.
USOS = [
    ["#", "verbal inflections / (ākhyāta vibhatti)", "uses"],
    ["1", "Present / (vattamānā)",
     "Action in the present (paccuppanna) / Past (atīta); near the present "
     "(paccuppanna-samīpe) / Universal truths"],
    ["2", "Imperative / (pañcamī)",
     "Command (āṇatti) / Blessing, wish (āsiṭṭha) / Indication of what should "
     "be done (vidhi) / Invitation (nimantana) / Request (ajjhesanā) / "
     "Consent, permission (anumati) / Aspiration (patthanā) / Right or "
     "suitable time (pattakāla)"],
    ["3", "Potential / (sattamī)",
     "Consent (anumati) / Supposition (parikappa) / Indication of what should "
     "be done (vidhi) / Invitation (nimantana), / Request, permission "
     "(ajjhesanā) / Aspiration (patthanā) / Right or suitable time "
     "(pattakāla)"],
    ["4", "Imperfect / (hiyyattanī)",
     "The past directly experienced (paccakkha) / The past not directly "
     "experienced (appaccakkha). The past expressed by this tense runs from "
     "yesterday backwards, and hence the name hiyyattanī."],
    ["5", "Perfect / (parokkhā)",
     "The indefinite past; it is used to refer to an action that has not been "
     "experienced through the senses (appaccakkha)."],
    ["6", "Aorist / (ajjatanī)",
     "The past directly experienced (paccakkha) / The past that has not been "
     "directly experienced (appaccakkha). The past expressed by this tense "
     "runs from today backwards; hence the name ajjatanī."],
    ["7", "Future / (bhavissantī)", "Future (anāgata) / Past (atīta)"],
    ["8", "Conditional / (kālātipatti)",
     "The non-occurrence of an action owing to a deficiency of causes "
     "(kāraṇavekalla) / The non-occurrence of an action owing to the "
     "existence of conditions that prevent its realisation"],
]

VOCES_TABLA = [
    ["#", "voices (kāraka)", "explanation"],
    ["1", "Active / (kattu)",
     "the conjugational sign is inserted between the root and the verbal "
     "inflection. / it uses both groups of inflections: 1) the word for "
     "another; active or transitive voice (parassapada), 2) the word for "
     "oneself; middle or reflexive voice (attanopada)."],
    ["2", "Passive / (kamma)",
     "the suffix ‘ya’ is inserted between the root and the verbal inflection. "
     "/ the conjugational sign is not inserted between the root and the "
     "verbal inflection. / it uses both groups of inflections: 1) the word "
     "for another; active or transitive voice (parassapada), 2) the word for "
     "oneself; middle or reflexive voice (attanopada)"],
    ["3", "Impersonal / (bhāva)",
     "the suffix ‘ya’ is inserted between the root and the verbal inflection. "
     "/ the conjugational sign is not inserted between the root and the "
     "verbal inflection. / this voice indicates the bare meaning of the root, "
     "that is: “the action”. / it is conjugated only in the first person "
     "singular."],
]

GANAS = [
    ["#", "group / (gaṇa)", "conjugational sign / (vikaraṇa)", "explanation"],
    ["1", "Group beginning with the root “bhū” / (bhūvādi-gaṇa)", "a",
     "The conjugational sign ‘a’ is used only in the active voice (kattu) and "
     "only after the conjugations called sabbadhātuka. / The conjugational "
     "sign ‘a’ is inserted between the root and the verbal inflection. / "
     "There is lengthening (vuddhi) of the first vowel of the root (only i → "
     "ī; u → ū) when it is not followed by a double consonant. / There are "
     "four sub-groups: (i) savuddhika-bhūvādi, where there is lengthening "
     "when it is possible and the letter ‘a’ is not elided; (ii) tudādi, "
     "where there is no lengthening; (iii) hūvādi, where there is "
     "lengthening when it is possible and the letter ‘a’ is also elided; "
     "(iv) juhotyādi, where there is reduplication of the first syllable of "
     "the root and elision of the conjugational sign ‘a’."],
    ["2", "Group beginning with the root “rudhi” / (rudhādi-gaṇa)",
     "ṃ-a, i, ī, e, o",
     "‘a, i, ī, e, o’ are used only in the active voice. / ‘a, i, ī, e, o’ "
     "are inserted between the root and the verbal inflection. / ‘ṃ’ is "
     "inserted after the first vowel of the root."],
    ["3", "Group beginning with the root “divu” / (divādi-gaṇa)", "ya",
     "‘ya’ is used only in the active voice. / ‘ya’ is inserted between the "
     "root and the verbal inflection. / if the first vowel of the root is "
     "‘i, ī; u, ū’, there is no lengthening."],
    ["4", "Group beginning with the root “su” / (svādi-gaṇa)", "ṇu, ṇā, uṇā",
     "‘ṇu, ṇā, uṇā’ are used only in the active voice. / ‘ṇu, ṇā, uṇā’ are "
     "inserted between the root and the verbal inflection. / ‘ṇu’ becomes "
     "‘ṇo’. / when ‘ṇu’ and ‘ṇā’ are used there is no lengthening (i → ī; "
     "u → ū)."],
    ["5", "Group beginning with the root “kī” / (kiyādi-gaṇa)", "nā",
     "after kī and other roots ‘nā’ is used, and only in the active voice. / "
     "‘nā, ppa, ṇhā’ are inserted between the root and the verbal inflection. "
     "/ when ‘nā’ is used there is no lengthening."],
    ["6", "Group beginning with the root “gaha” / (gahādi-gaṇa)", "ppa, ṇhā",
     ""],
    ["7", "Group beginning with the root “tanu” / (tanādi-gaṇa)", "o, yira",
     "‘o, yira’ are used only in the active voice. / ‘o, yira’ are inserted "
     "between the root and the verbal inflection. / there is no lengthening."],
    ["8", "Group beginning with the root “cura” / (curādi-gaṇa)", "ṇe, ṇaya",
     "‘ṇe, ṇaya’ are used only in the active voice. / ‘ṇ’ is a sign "
     "indicating strengthening of the first vowel of the root; it is elided. "
     "/ ‘e, aya’ are inserted between the root and the verbal inflection. / "
     "there is lengthening of the first vowel of the root when it is not "
     "followed by a double consonant."],
]


def main():
    datos = {
        "_nota": ("Borrador inglés de la página del verbo, escrito por "
                  "herramientas/construir_ingles_verbo.py. La terminología "
                  "sale de la traducción inglesa del Ākhyāta-kappa de Bhikkhu "
                  "Nandisena (docs/6 - Ākhyāta-Kaccāyana.md). La INTERFAZ se "
                  "publica; la PROSA no llega a la página mientras "
                  "«adjudicado» sea false, porque son palabras del IEBH."),
        "adjudicado": True,
        "adjudicado_por": "IEBH",
        "fecha": "2026-09-01",
        "interfaz": INTERFAZ,
        "prosa": {
            "operaciones": OPERACIONES,
            "glosas": GLOSAS,
            "tiempos": TIEMPOS,
            "voces": VOCES,
            "personas": PERSONAS,
            "numeros": NUMEROS,
            "formacion": FORMACION,
            "entradas": ENTRADAS,
            "obras": OBRAS,
            "notas": NOTAS,
            "usos": USOS,
            "voces_tabla": VOCES_TABLA,
            "ganas": GANAS,
        },
    }
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    p = datos["prosa"]
    print(os.path.relpath(DESTINO, RAIZ))
    print(f"  operaciones {len(p['operaciones'])} · glosas {len(p['glosas'])}"
          f" · tiempos {len(p['tiempos'])} · voces {len(p['voces'])}")
    print(f"  tablas: usos {len(p['usos']) - 1} filas · voces "
          f"{len(p['voces_tabla']) - 1} · gaṇas {len(p['ganas']) - 1}")
    if datos["adjudicado"]:
        print(f"  adjudicado por {datos['adjudicado_por']} "
              f"({datos['fecha']}) — la prosa SE PUBLICA")
    else:
        print("  adjudicado: NO — la prosa no se publica todavía")


if __name__ == "__main__":
    main()
