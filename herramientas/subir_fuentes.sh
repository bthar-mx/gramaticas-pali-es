#!/bin/sh
# Sube los paquetes de fondo de «Preguntar» al KV privado FUENTES.
#
#     sh herramientas/subir_fuentes.sh [carpeta]
#
# Lee ~/Documents/preguntar-fuentes/ (o la carpeta que se le dé), con una
# subcarpeta por obra y un Markdown por § de Kaccāyana:
#
#     silananda-rup/2.md   rupasiddhi/2.md   nyasappadipika/2.md   nyasa/2.md
#
# y sube cada archivo con la clave «<obra>/<§>» («silananda-rup/2»). El JSON
# intermedio se escribe en un directorio temporal FUERA del repositorio y se
# borra al terminar: el repositorio es público y los textos no deben entrar en
# él. Este guion no contiene ningún texto; sólo los traslada.
#
# Hace falta: Node (para npx), haber iniciado sesión con «npx wrangler login»
# (el enlace FUENTES ya está en wrangler.jsonc).
#
# Subir otra vez sobrescribe las claves que ya estén; no borra las que falten
# en la carpeta. Para quitar una:
#     npx wrangler kv key delete --binding FUENTES --remote "nyasa/2"
set -eu

ORIGEN=${1:-"$HOME/Documents/preguntar-fuentes"}
RAIZ=$(cd "$(dirname "$0")/.." && pwd)

if [ ! -d "$ORIGEN" ]; then
  echo "No existe la carpeta de fuentes: $ORIGEN" >&2
  exit 1
fi

TMP=$(mktemp -d "${TMPDIR:-/tmp}/subir-fuentes.XXXXXX")
trap 'rm -rf "$TMP"' EXIT INT TERM
BULTO="$TMP/fuentes.json"

# El JSON lo arma Node, que ya hace falta para npx y escapa bien el UTF-8.
ORIGEN="$ORIGEN" BULTO="$BULTO" node --input-type=module -e '
import { readdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";
const OBRAS = ["silananda-rup", "rupasiddhi", "nyasappadipika", "nyasa"];
const origen = process.env.ORIGEN;
const pares = [], avisos = [];
for (const obra of OBRAS) {
  const dir = join(origen, obra);
  if (!existsSync(dir)) { avisos.push("falta la carpeta " + obra + "/"); continue; }
  let n = 0;
  for (const f of readdirSync(dir).sort()) {
    if (!f.endsWith(".md")) continue;
    const s = f.slice(0, -3);
    if (!/^[0-9]+$/.test(s)) { avisos.push(obra + "/" + f + ": el nombre no es un § (se salta)"); continue; }
    const texto = readFileSync(join(dir, f), "utf-8").normalize("NFC");
    if (!texto.trim()) { avisos.push(obra + "/" + f + ": vacío (se salta)"); continue; }
    const cab = texto.split("\n", 1)[0];
    if (cab.split(";").length < 5) {
      avisos.push(obra + "/" + f + ": la primera línea no parece la cabecera «fuente; edición/origen; ubicación; aviso; derechos»");
    }
    pares.push({ key: obra + "/" + Number(s), value: texto });
    n += 1;
  }
  console.log("  " + obra.padEnd(15) + n + " archivos");
}
for (const a of avisos) console.log("  AVISO: " + a);
writeFileSync(process.env.BULTO, JSON.stringify(pares));
writeFileSync(process.env.BULTO + ".n", String(pares.length));
'

N=$(cat "$BULTO.n")
if [ "$N" -eq 0 ]; then
  echo "No hay nada que subir." >&2
  exit 1
fi

cd "$RAIZ"
npx wrangler kv bulk put "$BULTO" --binding FUENTES --remote
echo "Subidas $N claves al KV FUENTES."
