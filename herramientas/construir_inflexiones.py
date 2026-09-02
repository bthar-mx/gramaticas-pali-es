#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Escribe recursos/verbo/inflexiones.json: las ocho tablas de terminaciones.

    python3 herramientas/construir_inflexiones.py

POR QUÉ EXISTE ESTE ARCHIVO
---------------------------

Las tablas de inflexión que la página publicó hasta la v1.2 salían del
documento «Verbo» (`docs/fuentes/verbo.docx`, tablas 2-9), que es una versión
**reducida**: da una sola terminación por casilla. La buena está en otro
sitio, y estuvo disponible desde el primer día en DOS fuentes independientes:

1. **Ocho documentos de Google**, uno por inflexión, enlazados desde el índice
   «ÍNDICE DE PARADIGMAS DE INFLEXIONES VERBALES». Traen las formas
   alternativas —«ī - i», «uṃ - iṃsu»— y, sobre todo, las **referencias a
   Kaccāyana, Rūpasiddhi y Saddanīti** que justifican cada nota.
2. **Las presentaciones**: `GP-T - Verbo-V.pdf` imprime la misma tabla del
   aoristo con «Ī-I, UṂ - IṂSU, Ā-TTHA, O-I, MHĀ - MHA, A - AṂ».

Se perdieron por dos fallos encadenados: el índice se leyó en texto plano, que
descarta los hipervínculos, de modo que pareció una simple lista de códigos; y
el extractor de las diapositivas sólo buscaba escaleras —páginas con cabecera
PASO/AUTORIDAD/EXPLICACIÓN— y nunca miró las tablas de terminaciones. La
auditoría cotejaba las escaleras y no estas tablas, así que nada avisó.

`auditar_verbo.py` compara ahora estas ocho tablas con las del documento y con
las de las diapositivas, y enumera toda diferencia.

CÓMO SE VUELVE A TRAER
----------------------

Los ocho documentos son públicos. El índice está en

    https://docs.google.com/document/d/1_UA2LcOlS2ixLCoXfUMDouZBiel2kB8wjcBh2f9sWG0/

y **hay que exportarlo como HTML, no como texto**: en texto los enlaces
desaparecen. Cada documento se lee con

    https://docs.google.com/document/d/<ID>/export?format=txt

Los IDs están en DOCUMENTOS, más abajo. Lo transcrito aquí es verbatim.
"""

import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "recursos", "verbo", "inflexiones.json")

INDICE = "1_UA2LcOlS2ixLCoXfUMDouZBiel2kB8wjcBh2f9sWG0"

DOCUMENTOS = {
    "presente indicativo": "10HTRsYs9p1yxfxUEDWJjjNm0LdbXexPMKPdRxsdhyvw",
    "imperativo": "1VL6ERDctsuKDbAUV-d83JF8URgZPkpSKFXGwLrrs0oc",
    "potencial": "1KW3bMgwsTDUil5yW0puhN3_0x1mn9kFwY4Te4BxEMuI",
    "imperfecto": "1P7Hhq9ezUskRUbrfhl2Rhk5t5KiIGSx71CoAjFuCfBg",
    "perfecto": "1EC4TJfze-SwvRAVjbAIv0FI96vNrLLyKmFPQZNFR8rM",
    "aoristo": "1cMYgtcrbhT5jnS_oKYzjgDoSeij-6KNA6QN4qvMaZqg",
    "futuro": "10qIRmZZ9d1Qcee40AyBi5OTZw3AZINqFJfh0gIlQuys",
    "condicional": "1aj0xwhbEvvI-p79DeqmoQhgk86MKQ7YuFJM4ygi8Yug",
}

# Las referencias de las notas al pie. Se guardan desmenuzadas para que el
# §N de Kaccāyana pueda enlazarse como el de las escaleras, con la misma
# maquinaria: hoy sale en texto plano porque el Ākhyāta-kappa no está
# publicado, y se enlazará solo el día que entre.
REFS = {
    "aumento": {"kacc": 519, "ru": 457, "sad": 1032},
    "i_opcional": {"kacc": 516, "ru": 466, "sad": 1030},
    "alarga_a": {"kacc": 478, "ru": 438, "sad": 959},
    "e_potencial": {"ru": 454, "sad": 1088},
    "umsu": {"kacc": 504, "ru": 470, "sad": 1016},
    "resto_aor": {"ru": 469},
    "re_presente": {"ru": 442, "nir": 570},
}

# Cada inflexión: el título, su nombre pāḷi, las tres filas de la tabla —en el
# orden 3ª, 2ª, 1ª persona y, dentro de cada una, parassapada singular y
# plural, attanopada singular y plural—, y las notas con sus referencias.
INFLEXIONES = [
    {
        "titulo": "presente indicativo", "pali": "vattamānā", "codigo": "PRES",
        "filas": [
            ["3a (paṭhama)", "ti", "(a)nti", "te", "(a)nte"],
            ["2a (majjhima)", "si", "tha", "se", "vhe"],
            ["1a (uttama)", "mi", "ma", "e", "mhe"],
        ],
        "notas": [
            {"texto": "La ‘a’ se alarga antes de ‘mi’, ‘ma’ y ‘mhe’. Ej., "
                      "gacchāmi, voy; gacchāma, vamos; gacchāmhe, vamos.",
             "ref": "alarga_a"},
            {"texto": "A veces hay sustitución de ‘(a)nti’ y ‘(a)nte’ por "
                      "‘re’.",
             "ref": "re_presente"},
        ],
    },
    {
        "titulo": "imperativo", "pali": "pañcamī", "codigo": "IMP",
        "filas": [
            ["3a (paṭhama)", "tu", "antu", "taṃ", "antaṃ"],
            ["2a (majjhima)", "hi", "tha", "ssu", "vho"],
            ["1a (uttama)", "mi", "ma", "e", "āmase"],
        ],
        "notas": [
            {"texto": "La ‘a’ se alarga antes de ‘mi’, ‘ma’ y ‘hi’ — a veces "
                      "se elide ‘hi’. Ej., gacchāmi, vaya; gacchāma, vayamos; "
                      "gacchāhi, ve; gaccha, ve.",
             "ref": "alarga_a"},
        ],
    },
    {
        "titulo": "potencial", "pali": "sattamī", "codigo": "POT",
        "filas": [
            ["3a (paṭhama)", "eyya - e", "eyyuṃ", "etha", "eraṃ"],
            ["2a (majjhima)", "eyyāsi - e", "eyyātha", "etho", "eyyāvho"],
            ["1a (uttama)", "eyyāmi - e", "eyyāma", "eyyaṃ - e", "eyyāmhe"],
        ],
        "notas": [
            {"texto": "En la primera, segunda y tercera persona singular de "
                      "la voz activa, a veces hay sustitución por ‘e’. "
                      "También en la primera persona singular de la voz "
                      "media/reflexiva, a veces hay sustitución por ‘e’.",
             "ref": "e_potencial"},
        ],
    },
    {
        "titulo": "imperfecto", "pali": "hiyyattanī", "codigo": "IMPERF",
        "filas": [
            ["3a (paṭhama)", "ā", "ū", "ttha", "tthuṃ"],
            ["2a (majjhima)", "o", "ttha", "se", "vhaṃ"],
            ["1a (uttama)", "aṃ", "mhā", "iṃ", "mhase"],
        ],
        "notas": [
            {"texto": "La inserción del aumento ‘a’ antes de la raíz es "
                      "opcional.",
             "ref": "aumento"},
        ],
    },
    {
        "titulo": "perfecto", "pali": "parokkhā", "codigo": "PERF",
        "filas": [
            ["3a (paṭhama)", "a", "u", "ttha", "re"],
            ["2a (majjhima)", "e", "ttha", "tho", "vho"],
            ["1a (uttama)", "aṃ", "mha", "iṃ", "mhe"],
        ],
        "notas": [
            {"texto": "La inserción de ‘i’ antes de la inflexión verbal es "
                      "opcional.",
             "ref": "i_opcional"},
        ],
    },
    {
        "titulo": "aoristo", "pali": "ajjatanī", "codigo": "AOR",
        "filas": [
            ["3a (paṭhama)", "ī - i", "uṃ - iṃsu", "ā - ttha", "ū"],
            ["2a (majjhima)", "o - i", "ttha", "se", "vhaṃ"],
            ["1a (uttama)", "iṃ", "mhā - mha", "a - aṃ", "mhe"],
        ],
        "notas": [
            {"texto": "La inserción de ‘a’ al comienzo de la raíz es "
                      "opcional.",
             "ref": "aumento"},
            {"texto": "La inserción de ‘i’ antes de la inflexión verbal es "
                      "opcional.",
             "ref": "i_opcional"},
            {"texto": "También a veces en la tercera persona del singular hay "
                      "‘i’, en la primera del plural ‘mha’, y hay sustitución "
                      "de ‘o’ por ‘i’, ‘ā’ por ‘ttha’ y ‘a’ por ‘aṃ’.",
             "ref": "resto_aor"},
            {"texto": "Y ‘uṃ’ por ‘iṃsu’.", "ref": "umsu"},
        ],
    },
    {
        "titulo": "futuro", "pali": "bhavissantī", "codigo": "FUT",
        "filas": [
            ["3a (paṭhama)", "ssati", "ssanti", "ssate", "ssante"],
            ["2a (majjhima)", "ssasi", "ssatha", "ssase", "ssavhe"],
            ["1a (uttama)", "ssāmi", "ssāma", "ssaṃ", "ssāmhe"],
        ],
        "notas": [
            {"texto": "La inserción de ‘i’ antes de la inflexión verbal es "
                      "opcional.",
             "ref": "i_opcional"},
        ],
    },
    {
        "titulo": "condicional", "pali": "kālātipatti", "codigo": "COND",
        "filas": [
            ["3a (paṭhama)", "ssā - ssa", "ssaṃsu", "ssatha", "ssisu"],
            ["2a (majjhima)", "sse - ssa", "ssatha", "ssase", "ssavhe"],
            ["1a (uttama)", "ssaṃ", "ssāmhā - ssāmha", "ssiṃ", "ssāmhase"],
        ],
        "notas": [
            {"texto": "La inserción de ‘a’ al comienzo de la raíz es "
                      "opcional.",
             "ref": "aumento"},
            {"texto": "La inserción de ‘i’ antes de la inflexión verbal es "
                      "opcional.",
             "ref": "i_opcional"},
            {"texto": "También, a veces, hay acortamiento de la ‘ā’ de ‘ssā’ "
                      "y ‘ssāmhā’ y sustitución de ‘sse’ por ‘ssa’.",
             "ref": None},
        ],
    },
]


# Los casos en que se usa cada inflexión, tal como los lista su
# documento. El documento «Verbo» los da también, en su tabla de
# usos, con algunas diferencias de redacción que auditar_verbo.py
# enumera.
USOS = {
    "presente indicativo": [
        "Acción en el presente (paccuppanna)",
        "Pasado (atīta); cercanía del presente (paccuppanna-samīpe)",
        "Verdades universales."
    ],
    "imperativo": [
        "Orden (āṇatti)",
        "Bendición, deseo (āsiṭṭha)",
        "Indicación de lo que se debería hacer (vidhi)",
        "Invitación (nimantana)",
        "Solicitud (ajjhesanā)",
        "Consentimiento, permiso (anumati)",
        "Aspiración (patthanā)",
        "Tiempo oportuno o adecuado (pattakāla)"
    ],
    "potencial": [
        "Consentimiento (anumati)",
        "Suposición (parikappa)",
        "Indicación de lo que se debería hacer (vidhi)",
        "Invitación (nimantana)",
        "Solicitud, permiso (ajjhesanā)",
        "Aspiración (patthanā)",
        "Tiempo oportuno o adecuado (pattakāla)"
    ],
    "imperfecto": [
        "El pasado directamente experimentado (paccakkha)",
        "El pasado no directamente experimentado (appaccakkha). El pasado expresado por este tiempo verbal es partir de ayer hacia atrás, por esto el nombre hiyyattanī."
    ],
    "perfecto": [
        "Éste es el pasado indefinido y se utiliza para referirse a una acción que no ha sido experimentada por medio de los sentidos (appaccakkha)."
    ],
    "aoristo": [
        "El pasado directamente experimentado (paccakkha)",
        "El pasado que no ha sido experimentado directamente (appaccakkha). El pasado expresado por este tiempo verbal es a partir de hoy día hacia atrás; de aquí el nombre ajjatanī."
    ],
    "futuro": [
        "Futuro (anāgata)",
        "Pasado (atīta)"
    ],
    "condicional": [
        "La no ocurrencia de una acción debido a deficiencia de causas (kāraṇavekalla)",
        "La no ocurrencia de una acción debido a la existencia de condiciones que impiden su realización"
    ]
}

CABECERA = [
    ["", "voz activa o transitiva (parassapada)",
     "voz activa o transitiva (parassapada)",
     "voz media o reflexiva (attanopada)",
     "voz media o reflexiva (attanopada)"],
    ["persona (purisa)", "singular (ekavacana)", "plural (bahuvacana)",
     "singular (ekavacana)", "plural (bahuvacana)"],
]


def main():
    if len(INFLEXIONES) != 8:
        raise SystemExit(f"{len(INFLEXIONES)} inflexiones; deberían ser 8")
    for inf in INFLEXIONES:
        if len(inf["filas"]) != 3:
            raise SystemExit(f"{inf['titulo']}: {len(inf['filas'])} personas")
        for fila in inf["filas"]:
            if len(fila) != 5:
                raise SystemExit(f"{inf['titulo']}: fila de {len(fila)}")
        for nota in inf["notas"]:
            if nota["ref"] and nota["ref"] not in REFS:
                raise SystemExit(f"{inf['titulo']}: ref «{nota['ref']}» "
                                 "desconocida")
        inf["doc"] = DOCUMENTOS[inf["titulo"]]
        inf["usos"] = USOS[inf["titulo"]]

    datos = {
        "_nota": ("Las ocho tablas de terminaciones, de los ocho documentos "
                  "de Google enlazados desde el índice de paradigmas de "
                  "inflexiones verbales. Transcritas verbatim por "
                  "herramientas/construir_inflexiones.py, que explica en su "
                  "docstring por qué existen y cómo volver a traerlas."),
        "fuente": {
            "autor": "Bhikkhu Nandisena",
            "obra": "Índice de paradigmas de inflexiones verbales (IEBH)",
            "indice": INDICE,
        },
        "cabecera": CABECERA,
        "refs": REFS,
        "inflexiones": INFLEXIONES,
    }
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    alternas = sum(1 for inf in INFLEXIONES for fila in inf["filas"]
                   for c in fila[1:] if " - " in c)
    notas = sum(len(inf["notas"]) for inf in INFLEXIONES)
    print(os.path.relpath(DESTINO, RAIZ))
    print(f"  inflexiones          {len(INFLEXIONES)}")
    print(f"  casillas con forma alternativa  {alternas}")
    print(f"  notas                {notas}  ·  referencias {len(REFS)}")
    print(f"  casos de uso         "
          f"{sum(len(u) for u in USOS.values())}")


if __name__ == "__main__":
    main()
