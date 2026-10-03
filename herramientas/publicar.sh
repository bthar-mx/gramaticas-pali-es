#!/usr/bin/env bash
# Publica el trabajo preparado por Claude al final de cada tarea.
#
# Lee dos archivos que Claude escribe (y que no viajan con el repositorio):
#   herramientas/.publicar/archivos.txt  — una ruta por línea, relativa a la
#       raíz del repositorio. «rm <ruta>» = archivo que se elimina (git rm).
#       Se ignoran las líneas vacías y las que empiezan por «#».
#   herramientas/.publicar/mensaje.txt   — el mensaje del commit.
#
# Hace exactamente: git add / git rm de esas rutas, git status --short,
# git commit (el hook pre-commit muestra sus avisos completos) y git push.
# Si algo falla, se detiene y muestra el error. Nunca usa --force.
#
# Uso: ./herramientas/publicar.sh

RAIZ="$(cd "$(dirname "$0")/.." && pwd)" || { echo "ERROR: no encuentro la raíz del repositorio."; exit 1; }
cd "$RAIZ" || { echo "ERROR: no puedo entrar en $RAIZ."; exit 1; }

DIR="herramientas/.publicar"
ARCHIVOS="$DIR/archivos.txt"
MENSAJE="$DIR/mensaje.txt"

fallo() {
  echo
  echo "ERROR: $1"
  echo "Publicación detenida; no se ha hecho nada más."
  exit 1
}

[ -s "$ARCHIVOS" ] || fallo "falta $ARCHIVOS o está vacío."
[ -s "$MENSAJE" ]  || fallo "falta $MENSAJE o está vacío."

AGREGAR=()
QUITAR=()
while IFS= read -r LINEA || [ -n "$LINEA" ]; do
  LINEA="${LINEA%$'\r'}"
  # quitar espacios al principio y al final
  LINEA="${LINEA#"${LINEA%%[![:space:]]*}"}"
  LINEA="${LINEA%"${LINEA##*[![:space:]]}"}"
  [ -z "$LINEA" ] && continue
  case "$LINEA" in
    \#*) continue ;;
    "rm "*)
      RUTA="${LINEA#rm }"
      RUTA="${RUTA#"${RUTA%%[![:space:]]*}"}"
      QUITAR+=("$RUTA") ;;
    *) AGREGAR+=("$LINEA") ;;
  esac
done < "$ARCHIVOS"

[ ${#AGREGAR[@]} -gt 0 ] || [ ${#QUITAR[@]} -gt 0 ] || fallo "$ARCHIVOS no contiene ninguna ruta."

if [ ${#AGREGAR[@]} -gt 0 ]; then
  echo "== git add (${#AGREGAR[@]})"
  git add -- "${AGREGAR[@]}" || fallo "git add ha fallado."
fi

if [ ${#QUITAR[@]} -gt 0 ]; then
  echo "== git rm (${#QUITAR[@]})"
  git rm -- "${QUITAR[@]}" || fallo "git rm ha fallado."
fi

echo
echo "== git status --short"
git status --short || fallo "git status ha fallado."

echo
echo "== git commit"
git commit -F "$MENSAJE" || fallo "el commit no se ha hecho (revisa los mensajes del hook de arriba)."

echo
echo "== git push"
git push || fallo "el commit está hecho en local, pero git push ha fallado."

echo
echo "Publicado: $(git rev-parse --short HEAD)"
