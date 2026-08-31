# La automatización de los veredictos — grado medio

![El camino de un veredicto, del navegador del revisor a la página pública](flujo-veredictos.svg)

*Decisión del IEBH (2026-08-28): los veredictos del modo revisión viajan
solos hasta una cola del proyecto; la incorporación, los arneses y la firma
siguen siendo la puerta. El grado completo (que un veredicto se convierta en
caso publicado sin pasar por la Mac) queda para después, si el uso lo pide.*

## Cómo funciona

1. El revisor, en `/recursos/solucionador/?revision`, marca veredictos y
   pulsa **«Enviar N veredictos al proyecto»**. El navegador hace `POST`
   a `/api/veredictos` y el worker guarda el `.md` en la cola (KV, 90 días).
   **Desde el 2026-08-31 enviar exige identidad** (Access; v. más abajo), y el
   correo verificado queda con la entrada. Leer la cola sigue pidiendo la
   clave, en `/api/cola`, y nada de lo enviado toca el proyecto por sí solo.
   «Exportar .md» sigue existiendo como camino manual, **sin login ninguno**
   (y es el repuesto si la cola no responde).
2. En la Mac, quien firma corre el ciclo COMPLETO con **una orden**
   (2026-08-29 — la independencia de quien firma):

       VEREDICTOS_CLAVE=… python3 herramientas/ciclo_veredictos.py

   Recoge e incorpora, re-vierte las referencias que los casos nuevos
   toquen, regenera la página, corre los cinco arneses y, sólo con todo
   en verde, hace el commit y el push (que despliega). Ante el primer
   fallo se detiene sin publicar nada. `--sin-push` deja el commit hecho
   sin empujarlo. El paso a paso sigue disponible:

       VEREDICTOS_CLAVE=… python3 herramientas/traer_veredictos.py

   Eso guarda cada entrada en `docs/solucionador/veredictos-recibidos/`
   (registro permanente), la pasa por `incorporar_adjudicaciones.py` (que
   avisa de veredictos ilegibles y no toca formas ya adjudicadas) y retira
   de la cola sólo lo incorporado sin error. `--solo-mirar` lista sin tocar.
3. Después, lo de siempre: `generar_solucionador.py`, `arnes_casos.js`
   (y referencias/arneses/medición si la señal cambió), commit y push.
   **Nada se adjudica sin ese paso.**

Los datos POR VOZ ya no se pierden (2026-08-30, briefing 35 §6 quater: el
IEBH daba escaleras en el cuadro de observaciones y se tiraban): la **nota**
de cada veredicto y la **escalera** de su campo nuevo (un paso por línea)
se incorporan verbatim al caso — `nota` y `escalera_iebh`, rotuladas como
del revisor; el motor no las deriva ni las verifica. A un caso ya
adjudicado se le añaden si le faltan y el veredicto coincide; el veredicto
mismo nunca se toca. Las **Observaciones del revisor** (el cuadro libre)
siguen siendo prosa y no se vuelven casos, pero el incorporador las imprime
enteras con un aviso: quien corre el ciclo las lee en el acto, y si dan
reglas generales, quien firma decide — como salió la de los absolutivos en
-tvā/-tvāna.

## Cómo se activa (una sola vez, en la Mac)

    npx wrangler kv namespace create VEREDICTOS
    #  → imprime un "id"; descomentar el bloque kv_namespaces de
    #    wrangler.jsonc y poner ese id
    npx wrangler secret put CLAVE_VEREDICTOS
    #  → la clave que sólo conoce quien recoge la cola
    git add -A && git commit && git push

Hasta entonces el sitio funciona igual: `/api/veredictos` responde 503 y el
botón «Enviar» lo dice y remite a «Exportar .md».

## QUIÉN ENVÍA: el login del modo revisión (2026-08-31)

*Pedido de Angel. Antes de esto la cola era un buzón **anónimo**, y el
problema no era que entrara basura —eso se ve y se descarta— sino que el
`.md` exportado trae escrita la orden de incorporación con
`--fuente "IEBH, …"`. Lo de un desconocido entraba al proyecto **rotulado
como del IEBH**: el principio 4 roto en silencio, que es la peor manera.*

Ahora enviar exige **identidad verificada por Cloudflare Access**, y el correo
verificado se guarda con la entrada. La lista de quién puede entrar vive en la
política de Access —se edita en el panel, sin tocar código ni desplegar—, que
es la diferencia con una contraseña compartida: **se revoca a uno solo**.

### Los dos papeles, y por qué sólo uno necesita entrar

| papel | qué hace | ¿login? |
| --- | --- | --- |
| **estudiante** | marca veredictos y **exporta el .md** | **no**: exportar no toca el servidor, pasa entero en el navegador |
| **revisor** | además **envía** a la cola | **sí**: enviar es lo único que llega al worker |

De modo que no hay que cerrar la página: se cierra **el POST**, que es el
único sitio por donde se entra.

### Dos rutas, porque Access no distingue métodos

**Se aprendió sobre la marcha el mismo 2026-08-31.** Access protege una RUTA,
y la protege para todos los métodos. Puesto delante de `/api/veredictos`
pensando en el POST del navegador, dejó fuera también el GET — es decir,
`traer_veredictos.py`, que corre en la Mac sin sesión y recibía el HTML del
login en vez del JSON. Con una sola ruta no hay arreglo posible.

De modo que cada puerta lleva la cerradura que le toca:

| ruta | quién pasa | con qué |
| --- | --- | --- |
| `POST /api/veredictos` | el navegador del revisor | **identidad** (Access) |
| `GET/DELETE /api/cola?clave=…` | quien recoge, desde la Mac | **la clave** de siempre |
| `GET /api/entrar` | el revisor, para iniciar sesión | identidad (Access) |

No es un apaño: al buzón se echa una carta diciendo quién eres, y el buzón se
abre con llave. Nunca fueron la misma cosa.

`/api/entrar` existe porque la sesión de Access se obtiene visitando una ruta
protegida, y la página del solucionador **no** lo está ni debe estarlo —el
estudiante entra sin cuenta—. Sin ella el revisor tendría que visitar a mano
el endpoint del POST para que le pidieran la contraseña.

**Tiene que ir como SEGUNDO «destination» de la MISMA aplicación de Access.**
La galleta vale por aplicación: en otra aplicación, iniciar sesión ahí no
abriría el POST.

### En el panel de Cloudflare (una sola vez, lo hace Angel)

1. **Zero Trust → Access → Applications → Add an application → Self-hosted.**
   Gratis hasta 50 usuarios.
2. Destinations → dos hostnames públicos **en esta misma aplicación**:
   `gramaticas.buddha-dhamma.net/api/veredictos` y
   `gramaticas.buddha-dhamma.net/api/entrar`.
   **No** se protege `/recursos/solucionador/`: la página tiene que seguir
   abierta para el estudiante, que no necesita cuenta.
3. **Policy → Allow**, con `Emails` y la lista de quien esté aprobado. Ése es
   el repertorio, y se cambia aquí sin volver a desplegar.
4. Copiar el **Application Audience (AUD) tag** de la pestaña *Overview*.
5. En la Mac:

        npx wrangler secret put ACCESO_EQUIPO
        #  → mi-equipo.cloudflareaccess.com   (Settings → Custom Pages, o la
        #    URL de login; es el dominio del EQUIPO, no el del sitio)
        npx wrangler secret put ACCESO_AUD
        #  → el AUD tag del paso 4
        git add -A && git commit && git push

**Mientras esas dos variables no estén puestas, todo sigue exactamente como
hoy** y la cola acepta envíos anónimos. Es deliberado: desplegar el worker no
debe cerrar la puerta antes de que exista la llave. Lo único que cambia desde
ya es que esas entradas quedan marcadas `correo: null` y **`traer_veredictos.py`
deja de atribuirlas al IEBH**.

### Qué se ve después

    python3 herramientas/traer_veredictos.py --solo-mirar
      · 2026-09-02T…-a1b2c3d4 — 3 veredictos — revisor@ejemplo.org

y el `--fuente` de cada entrada sale de ahí. Cuando no hay identidad lo dice
—«SIN IDENTIDAD VERIFICADA»— en vez de suponer. Para rotular a mano, que es
acto deliberado de quien firma, está `--fuente`.

### El arnés

    node worker/arnes_identidad.mjs

Dieciocho comprobaciones, sin red — nueve de identidad y seis del reparto
de rutas, que es lo que impide volver a dejar fuera a quien recoge: token bueno, sin token, firma de otra clave,
**aud de otra aplicación del mismo equipo** (el descuido clásico), caducado,
cuerpo manipulado con firma legítima, `alg: none`, la galleta
`CF_Authorization` —que es como llega de un navegador— y el caso de Access sin
configurar. Es código de autenticación: el que no se prueba parece bien hasta
el día que importa.

## Qué guardar en secreto

La clave (`CLAVE_VEREDICTOS`) sólo la conoce quien recoge. Si se filtrara,
lo peor posible es que alguien LEA o VACÍE la cola — no puede publicar ni
adjudicar nada: eso sigue pidiendo la Mac, los arneses y la firma.

**El envío ya no es abierto** desde que Access está configurado (arriba). Y aun
así la puerta del proyecto es la de siempre: una entrada basura se descarta al
mirarla, y el incorporador la rechaza sola si no trae `VEREDICTO:` legibles.
El login dice **quién** dejó algo en el buzón; **nada se adjudica sin la
firma**, que es lo que no delega ningún candado.
