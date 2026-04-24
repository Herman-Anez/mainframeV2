01-que-es-bash.md
Bash: el intérprete de comandos que se convirtió en lenguaje

Bash (Bourne Again SHell) es un intérprete de comandos y lenguaje de scripting creado por Brian Fox para el proyecto GNU en 1989. Es el shell por defecto en la mayoría de las distribuciones Linux y macOS (hasta Catalina; de ahí en adelante usa zsh como shell interactivo, pero bash sigue presente en /bin/bash y se puede usar para scripts).

    No solo un shell interactivo: Bash puede ejecutar comandos uno a uno, pero su verdadero poder reside en los scripts. Un script de Bash es un archivo de texto con una secuencia de comandos que el intérprete ejecuta en orden.

    Familia de shells:

        sh (shell Bourne original): ancestro mínimo. /bin/sh puede ser un enlace a bash (que se ejecuta en modo de compatibilidad POSIX) o a dash (más ligero).

        bash: añade características como arrays, expansión de llaves, [[, etc.

        ksh, zsh, fish: otros shells con sintaxis similares pero diferencias importantes.

    ¿Por qué aprender Bash?

        Automatización de tareas del sistema (backups, despliegues, monitorización).

        Administración de servidores y tuberías CI/CD.

        Es ubicuo: cualquier máquina Unix/Linux lo tiene.

        Es la “navaja suiza” para pegar comandos.

Distinciones clave:

    Shell interactivo vs no interactivo: cuando ejecutas un script (bash script.sh) estás en modo no interactivo. El comportamiento de algunos comandos y la carga de archivos de configuración cambian.

    Shell de login vs no login: un shell de login lee /etc/profile, ~/.bash_profile, etc.; el no login lee ~/.bashrc. Veremos esto en detalle en 06-entorno-y-configuracion.md.

Modos de operación:

    Interactivo: lee entrada del usuario, muestra prompt, manejo de señales por defecto, historial activo.

    Non-interactivo: ejecuta un script o comando pasado con -c. No carga todos los archivos de inicialización.

    Modo POSIX: si se invoca como sh o con --posix, Bash se comporta de manera más estricta y compatible.

Entender estas diferencias es fundamental para evitar comportamientos inesperados al ejecutar scripts desde cron, systemd o SSH.
02-shebang-y-ejecucion.md
El shebang y las distintas formas de ejecutar un script
El shebang (#!)

La primera línea de un script debe ser el shebang (contracción de “sharp” y “bang”). Indica al sistema qué intérprete usar.
bash

#!/bin/bash

O la forma portátil (recomendada para scripts que deben correr en sistemas sin /bin/bash en esa ruta exacta):
bash

#!/usr/bin/env bash

/usr/bin/env busca bash en el PATH y lo ejecuta. Ventaja: no depende de una ruta fija. Desventaja: el entorno puede no ser controlable (el PATH puede ser distinto).

Opciones en el shebang: puedes pasar una sola opción, por ejemplo:
bash

#!/bin/bash -u

Pero no se pueden pasar múltiples opciones de manera fiable. Lo mejor es usar set dentro del script (ver depuración).
Ejecución de un script

    Convertirlo en ejecutable y lanzarlo:
    bash

    chmod +x script.sh
    ./script.sh

    Esto ejecuta un proceso nuevo con el intérprete indicado en el shebang. El script debe tener permiso de ejecución.

    Invocar explícitamente el intérprete:
    bash

    bash script.sh

    No necesita ser ejecutable. Puedes pasar opciones extra: bash -x script.sh.

    Ejecutar en el shell actual con source o .:
    bash

    source script.sh
    . script.sh

    Esto ejecuta los comandos en el entorno actual, sin lanzar un proceso hijo. Los cambios de variables, funciones y directorio actual persisten en la sesión interactiva. Importante: si el script tiene exit, finalizará la sesión interactiva.

Diferencias prácticas:

    ./script.sh vs bash script.sh: el shebang se respeta o se ignora respectivamente.

    source es muy usado para cargar bibliotecas de funciones o archivos de configuración en el mismo shell.

Argumentos del script: al ejecutar un script, puedes pasar argumentos posicionales. Estos estarán disponibles dentro como $1, $2, etc. (ver variables).
Comportamiento de los shells no interactivos

Cuando se invoca un script con bash script.sh, Bash arranca en modo no interactivo, no lee ~/.bashrc a menos que se fuerce con BASH_ENV. Es común tener funciones que dependen de ~/.bashrc y no estarán disponibles en el script. Solución: cargar explícitamente la librería necesaria.
03-variables.md
Variables: cajones con nombre para tus datos
Definición y asignación

En Bash, la asignación no puede tener espacios alrededor del =:
bash

nombre="Juan"
numero=42

Acceso: $nombre o ${nombre}. Las llaves son obligatorias en ciertos contextos (concatenación con texto, o expansiones especiales):
bash

echo "Hola ${nombre}, tu número es ${numero}"

Variables sin declarar: si accedes a una variable no definida, Bash devuelve una cadena vacía. Con set -u (modo estricto) causará un error.
Tipos de variables

Bash no tiene tipado fuerte. Todo se almacena como cadena. Con declare se pueden establecer atributos:

    declare -i var → variable entera (las asignaciones evalúan aritmética automáticamente).

    declare -r var=valor → solo lectura (constante).

    declare -a arr → array indexado.

    declare -A map → array asociativo (diccionario).

    declare -x var → exportar al entorno.

También existe local dentro de funciones (restringe el ámbito).
Variables de entorno

Las variables de entorno son heredadas por los procesos hijos. Para verlas: env o printenv.
Para hacer que una variable de shell pase al entorno: export VAR=valor.
Para eliminarla del entorno (pero no del shell actual): export -n VAR.
Para eliminar la variable por completo: unset VAR.
Variables especiales (parámetros posicionales y otros)
Variable	Significado
$0	Nombre del script o shell
$1 … $9	Argumentos posicionales del 1º al 9º
${10}	A partir del décimo es obligatorio usar llaves
$#	Número de argumentos
$@	Todos los argumentos como lista de palabras separadas (cada uno entrecomillado si se usa "$@")
$*	Todos los argumentos como una sola palabra (separados por el primer carácter de IFS)
$?	Código de salida del último comando (0 = éxito, otro = error)
$$	PID del shell actual
$!	PID del último proceso lanzado en segundo plano
$_	Último argumento del último comando ejecutado (en algunos contextos)

Nota sobre $@ vs $*: casi siempre quieres "$@". Conserva los argumentos que contienen espacios. Ejemplo:
bash

set -- "a b" c
for arg in "$@"; do echo "$arg"; done   # "a b", "c" (correcto)
for arg in $*;   do echo "$arg"; done   # "a", "b", "c"   (separó por espacio)

Variables predefinidas útiles

    HOME: directorio home del usuario.

    PATH: lista de directorios donde buscar ejecutables.

    USER: nombre del usuario actual.

    PWD: directorio de trabajo actual (mantenido por el shell).

    OLDPWD: directorio anterior.

    RANDOM: genera un entero aleatorio entre 0 y 32767 (se puede reinicializar asignándole un valor).

    SECONDS: segundos transcurridos desde que arrancó el shell.

    UID: UID numérico del usuario.

    LINENO: número de línea actual (útil para depuración).

    FUNCNAME: array con la pila de funciones en ejecución.

Ámbito (scope)

Por defecto las variables son globales. Dentro de una función puedes usar local para que no afecten al exterior:
bash

mi_func() {
    local var_interna="solo aquí"
}

Expansión de parámetros (solo una muestra)

    ${var:-valor_por_defecto}: devuelve valor_por_defecto si var no está definida o es nula.

    ${var:=valor}: asigna y devuelve si no está definida.

    ${var:?mensaje}: muestra error si no está definida/nula y aborta (si no es interactivo).

    ${var:+alternativo}: si var existe y no es nula, devuelve alternativo.

    ${#var}: longitud de la cadena.

    ${var#patrón}: elimina la coincidencia más corta del prefijo.

    ${var##patrón}: elimina la más larga del prefijo.

    ${var%patrón}: sufijo más corto.

    ${var%%patrón}: sufijo más largo.

    ${var/buscar/reemplazar}: reemplaza la primera ocurrencia.

    ${var//buscar/reemplazar}: reemplazo global.

    Mayúsculas/minúsculas: ${var^^} (todo mayúsculas), ${var,,} (minúsculas), ${var^} (primera mayúscula), ${var,} (primera minúscula).

04-sustituciones-y-expansiones.md
Expansiones: cómo Bash transforma las líneas antes de ejecutarlas

Bash realiza varios pasos de expansión tras leer una línea. Conocerlos evita dolores de cabeza con comillas y caracteres especiales.
1. Expansión de llaves (brace expansion)

Genera combinaciones o secuencias sin necesidad de que existan los archivos.
bash

echo archivo-{a,b,c}.txt   # archivo-a.txt archivo-b.txt archivo-c.txt
echo {1..10}               # 1 2 3 ... 10
echo {01..10}              # 01 02 ... 10
echo {a..z}                # a b c ... z
echo prefijo-{a,b,c}-sufijo  # combinaciones

No puede haber espacios dentro de las llaves. Se expande antes de cualquier otra cosa.
2. Sustitución de comandos

Ejecuta un comando y captura su salida estándar.
Sintaxis moderna (anidable sin escapes):
bash

fecha=$(date)

Sintaxis clásica (menos recomendada por problemas con anidamiento):
bash

fecha=`date`

Se puede almacenar en variables, pasar como argumento, etc. La salida sustituida recorta el salto de línea final.
3. Sustitución de procesos (process substitution)

Permite tratar la salida (o entrada) de un comando como un archivo.
bash

diff <(ls dir1) <(ls dir2)

Aquí <(...) crea un descriptor de archivo temporal que contiene la salida del comando. También existe >(...) para escribir a un comando como si fuera un archivo, útil para comandos que esperan un archivo de salida.
4. Expansión aritmética

Evalúa una expresión matemática entera y la sustituye por el resultado.
bash

resultado=$(( 3 + 4 * 2 ))   # 11
let "a = 5 * 2"              # alternativa, afecta variable "a"

Soporta los operadores básicos, incrementos (++), asignaciones (+=), operadores bit a bit y comparaciones (que retornan 1 o 0). No admite punto flotante; usa bc para eso.
5. Expansión de tilde

    ~ → $HOME

    ~usuario → home de ese usuario

    ~+ → $PWD

    ~- → $OLDPWD

6. Expansión de variables y comodines

Después de las expansiones anteriores, se realiza la expansión de variables (sustitución de parámetros) y el globbing (expansión de nombres de archivo): *, ?, [...]. Esto ocurre solo si no está entrecomillado.
Orden de evaluación (resumen)

    Dividir en palabras (word splitting) basado en IFS

    Expansión de llaves

    Sustitución de tilde

    Sustitución de parámetros y variables

    Sustitución de comandos

    Expansión aritmética

    División de palabras (de nuevo)

    Expansión de nombres de archivo (globbing)

Comillas: las comillas dobles ("...") protegen contra división de palabras y globbing, pero permiten variables y sustituciones. Las simples ('...') suprimen toda expansión.
05-comentarios-y-sintaxis.md
Comentarios y la gramática básica de las líneas
Comentarios

Cualquier línea que comience con # (excepto el shebang) es un comentario.
bash

# Esto es un comentario
echo "Hola"   # comentario después de un comando (el # debe estar seguido de espacio o sin ambigüedad)

No existen comentarios multilínea nativos. Se suelen usar here-docs no leídos:
bash

: <<'COMENTARIO_LARGO'
Todo esto es ignorado.
Puede tener comillas sin problemas.
COMENTARIO_LARGO

El comando : (dos puntos) es un no-op que no hace nada y siempre retorna éxito.
Separadores de comandos

    ; : ejecuta un comando tras otro secuencialmente, independientemente del éxito.

    && : ejecuta el siguiente solo si el anterior tuvo éxito (código de salida 0).

    || : ejecuta el siguiente solo si el anterior falló (código de salida distinto de 0).

Continuación de línea

Si una línea termina con \, Bash interpreta que el comando continúa en la siguiente línea:
bash

echo "esto es un comando muy largo" \
     "y sigue aquí"

La barra invertida debe ser el último carácter, sin espacios después.
Listas de comandos y agrupación

    (comandos) : ejecuta en un subshell (entorno heredado pero aislado; cambios de variables, directorio, etc., no afectan al padre).

    { comandos; } : agrupa comandos en el entorno actual. La sintaxis requiere punto y coma después del último comando y espacios alrededor de las llaves.

Comillas y escapes

    \ : quita el significado especial del siguiente carácter.

    '...' : literal absoluto, ni $ ni \ funcionan.

    "..." : permiten expansiones de variables ($), sustitución de comandos y caracteres de escape como \$, \", \\.

Ejemplo de diferencias:
bash

nombre=Juan
echo '$nombre'   # muestra literal $nombre
echo "$nombre"   # muestra Juan

El comando test y sus alias

El if evalúa comandos, no expresiones. Pero es común usar:
bash

if [ "$a" -eq 5 ]; then ...

[ es un comando (alias de test) que exige coincidencia sintáctica: espacios alrededor, y el último argumento ]. [[ ]] es una palabra reservada de Bash más moderna y segura, que permite &&, ||, =~ (regex) y no hace división de palabras. Recomendación: en scripts para bash, usar siempre [[ ]] en condicionales.
06-entorno-y-configuracion.md
Cómo se configura Bash según sea login, interactivo, etc.

Bash lee distintos archivos según el tipo de sesión. Este es uno de los aspectos más confusos y causantes de errores.
Tipos de shell y archivos de inicio
Tipo de shell	Archivos leídos
Login shell interactivo	/etc/profile, luego el primero que exista de: ~/.bash_profile, ~/.bash_login, ~/.profile
Login shell no interactivo	/etc/profile, luego el primero de: ~/.bash_profile, ~/.bash_login, ~/.profile (pero no lee .bashrc a menos que se invoque explícitamente con source)
Shell interactivo no login	/etc/bash.bashrc (si existe), ~/.bashrc
Shell no interactivo no login	Variable BASH_ENV: si está definida, se expande y se interpreta como un archivo de inicio. No lee ni .bashrc ni .profile automáticamente.
Invocado como sh (POSIX)	Solo archivos especificados por ENV, o comp. POSIX
Propósito de cada archivo

    ~/.bash_profile: ideal para configuraciones de sesión de login (variables globales, arranque de agentes, etc.). Normalmente debería sourciar ~/.bashrc para que los shells interactivos no login también tengan esas configuraciones:
    bash

    if [ -f ~/.bashrc ]; then
        source ~/.bashrc
    fi

    ~/.bashrc: para configuraciones de shells interactivos (alias, prompt, funciones, atajos, etc.). Se carga cada vez que abres una terminal.

    ~/.profile: se usa en shells de login que no son bash (como sh), o por retrocompatibilidad. A menudo contiene solo lo necesario para cargar .bashrc y establecer el PATH.

Variables de entorno importantes para la configuración

    BASH_ENV: si se define, los scripts no interactivos la expandirán y tratarán de cargar ese archivo. Útil para dotar de funciones a scripts sin tener que hacer source explícito.

    ENV: similar pero para shells POSIX.

    PATH: $HOME/.local/bin:/usr/local/bin:...

    PS1, PS2, PS4: prompts (interactivo, continuación y traza de depuración).

Comportamiento típico en scripts ejecutados por cron, systemd o SSH remoto

    Cron y systemd ejecutan shells no interactivos y no login. No cargan .bashrc.

    SSH ejecuta un login shell interactivo si se invoca con ssh usuario@host, pero si pasas un comando: ssh host script.sh, se ejecuta un shell no interactivo, no login, sin .bash_profile y sin .bashrc.

    Para scripts que necesiten el entorno completo, se puede forzar: bash -l script.sh (simula login) o incluir source ~/.bashrc al principio.

Cómo gestionar el entorno correctamente

    Mantén las variables de entorno en ~/.bash_profile o ~/.profile y las funciones/alias en ~/.bashrc.

    Nunca definas variables de entorno necesarias para scripts en .bashrc sin cargarlo explícitamente.

    Para automatización, es mejor definir todo en el propio script o en un archivo de configuración aparte.

Scripts de ejemplo

A continuación los dos scripts sugeridos, con comentarios explicativos integrados.
scripts/hola-mundo.sh
bash

#!/usr/bin/env bash
# --------------------------------------------------------------------
# hola-mundo.sh
# Script mínimo que demuestra shebang, variables, entrada y salida.
# --------------------------------------------------------------------

# Anunciamos el modo estricto (detiene el script ante errores y variables no definidas)
set -euo pipefail

# 1. Uso de variable simple
saludo="Hola, mundo"
echo "$saludo"

# 2. Capturar argumentos de línea de comandos
if [ "$#" -gt 0 ]; then
    echo "Recibiste $# argumento(s):"
    # Iteramos sobre todos los argumentos respetando espacios
    for arg in "$@"; do
        echo "  -> $arg"
    done
else
    echo "No pasaste argumentos. Intenta: $0 Juan María"
fi

# 3. Leer entrada del usuario
read -r -p "¿Cómo te llamas? " nombre
echo "Encantado, ${nombre:-invitado}."
# ${nombre:-invitado} imprime "invitado" si el usuario no escribió nada.

# 4. Mostrar algunas variables especiales
echo "PID de este script: $$"
echo "Directorio actual: $PWD"
echo "Último código de salida: $? (debería ser 0)"

exit 0

scripts/ejemplo-variables.sh
bash

#!/usr/bin/env bash
set -euo pipefail

# --------------------------------------------------------------------
# ejemplo-variables.sh
# Ilustra diferentes tipos de variables, expansiones y ámbito.
# --------------------------------------------------------------------

# --- Variables globales y de entorno ---
export MENSAJE_GLOBAL="Hola desde el entorno"
no_exportado="Solo en este script"

echo "MENSAJE_GLOBAL = $MENSAJE_GLOBAL"
echo "no_exportado  = $no_exportado"

# --- Variables numéricas y de solo lectura ---
declare -i entero=10
entero+=5                      # Ahora vale 15 (gracias a -i)
echo "Entero tras suma: $entero"

declare -r CONSTANTE=3.1416
echo "Constante PI aproximado: $CONSTANTE"
# Descomentar la siguiente línea causaría error:
# CONSTANTE=4

# --- Arrays ---
# Array indexado
frutas=(manzana naranja pera)
frutas+=("uva")                # Añade un elemento
echo "Primera fruta: ${frutas[0]}"
echo "Todas las frutas: ${frutas[@]}"
echo "Número de frutas: ${#frutas[@]}"

# Array asociativo (requiere declare -A)
declare -A capitales
capitales=([Francia]="París" [Japón]="Tokio" [Brasil]="Brasilia")
capitales["Alemania"]="Berlín"
echo "Capital de Japón: ${capitales[Japón]}"
echo "Todas las capitales: ${capitales[@]}"

# --- Expansiones de parámetros ---
nombre="Juan Carlos"
# Longitud
echo "Longitud de nombre: ${#nombre}"
# Subcadena: del carácter 0, longitud 4
echo "Primer nombre: ${nombre:0:4}"
# Reemplazo
echo "Con guiones: ${nombre// /_}"
# Default
echo "Apellido (si no existe): ${apellido:-Desconocido}"

# --- Ámbito con funciones ---
mi_funcion() {
    local local_var="soy local"
    echo "Dentro de la función: local_var = $local_var"
    # Esta variable global se modifica fuera
    global_modificada="modificada dentro de función"
}
mi_funcion
echo "Fuera de la función: global_modificada = $global_modificada"
# Esto estaría vacío si intentáramos imprimir local_var (es local)

# --- Exit code y captura de salida de comandos ---
comando_inexistente 2>/dev/null || echo "Código de salida tras fallo: $?"

output=$(date "+%Y-%m-%d")
echo "Fecha formateada: $output"

exit 0

We'll produce detailed content for the 02-control-de-flujo/ folder, covering all the specified .md files and both scripts, as requested. The user wants a deep dive similar to the previous fundamentals section. We'll structure the response as if writing the documentation for each file, with thorough explanations, examples, and best practices. We'll also include the scripts with explanatory comments. The language must be Spanish, consistent with the previous answer. Let's outline each file:

    01-condicionales-if.md: Explain if, then, elif, else, fi, the command evaluation model, how if works with the exit status of commands (0=true, non-zero=false). Include common pitfalls (missing spaces, using [ vs [[). Show simple examples, nested if, and how to combine with &&, || to avoid deep nesting.

    02-test-y-operadores.md: Deep dive into the test command, [ and [[. Cover string operators (=, !=, -z, -n), integer comparisons (-eq, -ne, -lt, -le, -gt, -ge), file tests (-f, -d, -e, -r, -w, -x, -s, etc.), and logical operators (-a, -o, ! for [, &&, ||, ! for [[). Emphasize that [[ is a Bash keyword with enhanced features (regex =~, pattern matching, no word splitting). Also mention (( )) for arithmetic tests.

    03-case.md: Pattern matching with case, syntax (case expresión in patron1) comandos;; patron2) comandos;; *) default;; esac), glob patterns, multiple patterns with |, ending with ;;, ;&, ;;&. Provide examples like parsing options, categorizing input.

    04-bucles-for-while-until.md: Cover for in two forms: for var in lista and for (( expr1; expr2; expr3 )). while loop, until loop. Explain break and continue. Show iteration over arguments, files (with globbing), arrays, and reading lines from a file or command with while read. Mention IFS issues.

    05-select-menus.md: The select construct for simple menus. Syntax, how it works with PS3 prompt, REPLY variable, and case inside. Show example.

    scripts/condiciones.sh: A script demonstrating file tests, string and numeric comparisons, the use of if/elif/else, [[ ]], (()), maybe case.

    scripts/adivina-numero.sh: A number guessing game using loops, random number generation ($RANDOM), input validation with while, conditions. Shows while, if, user input, arithmetic.

We'll write all this as a continuation of the previous answer. The user expects the same depth and style: informative, with code snippets, warnings, and tips. The response will be structured with headings and content for each file. We'll avoid repeating the entire folder structure but just deliver the content. We'll provide it in a single message, as requested "profundicemos estos temas ahora", similar to the previous long answer.

We'll ensure all code examples are well-commented and clear. Since this is a knowledge base, we'll use a pedagogical tone.

A continuación profundizamos en los temas de 02-control-de-flujo/, incluyendo el contenido de cada archivo .md y los scripts de ejemplo con explicaciones.
01-condicionales-if.md
La estructura if en Bash: evaluar comandos, no expresiones

En Bash, la sentencia if evalúa el código de salida de un comando (o lista de comandos). No evalúa directamente una expresión booleana como en otros lenguajes. La regla es:

    Código de salida 0 → verdadero (éxito)

    Código de salida distinto de 0 → falso (fallo)

Esto permite usar cualquier comando o pipeline como condición.
Sintaxis básica
bash

if comando1; then
    # se ejecuta si comando1 retorna 0
elif comando2; then
    # se ejecuta si comando1 falla y comando2 retorna 0
else
    # si todos los anteriores fallaron
fi

then debe estar en una nueva línea o precedido por ;. El elif (opcional) puede repetirse y también va acompañado de then. El cierre es siempre fi (al revés).
Cómo funciona en la práctica

El comando puede ser cualquiera: una tubería, una llamada a grep, test, [[ ]], (( )), etc.
bash

# Verificar si un archivo existe
if ls archivo.txt >/dev/null 2>&1; then
    echo "Existe"
fi

# Usando test/[
if [ "$nombre" = "admin" ]; then
    echo "Acceso concedido"
fi

# Usando [[ ]]
if [[ $numero -gt 10 ]]; then
    echo "Mayor que 10"
fi

# Evaluación aritmética (( ))
if (( x > 10 )); then
    echo "x mayor que 10"
fi

# Comprobar el éxito de varios comandos
if comando1 && comando2; then
    echo "Ambos exitosos"
fi

Uso de && y || como condicionales en línea

Se pueden encadenar comandos sin necesidad de un if completo:
bash

[ -f config.cfg ] && echo "Existe" || echo "No existe"

Equivale a un if then else simple, pero con cuidado: si el primer echo fallara (raro), el || se ejecutaría también. Para lógica segura usa if.
Anidamiento y buenas prácticas

    Evita escaleras muy profundas de if/elif; considera usar case cuando evalúes múltiples valores discretos.

    Siempre usa comillas dobles alrededor de variables en [ ] para evitar división de palabras y errores de sintaxis. Con [[ ]] no es necesario (pero no hace daño).

    Usa [[ ]] para todo excepto cuando necesites compatibilidad POSIX estricta (sh).

    Aprovecha elif para evitar anidar varios else if.

Ejemplo de anidamiento y uso de elif:
bash

if [[ $1 == "iniciar" ]]; then
    systemctl start mi-servicio
elif [[ $1 == "detener" ]]; then
    systemctl stop mi-servicio
elif [[ $1 == "reiniciar" ]]; then
    systemctl restart mi-servicio
else
    echo "Uso: $0 {iniciar|detener|reiniciar}"
    exit 1
fi

Trucos avanzados

    Negación con !: if ! comando; then ... → se ejecuta si el comando falla.

    Comprobación de comandos builtin vs externos: if type -P tmux >/dev/null; then ... para ver si un programa está instalado.

    Redirigir la salida de if: El if no captura la salida estándar, pero puedes almacenarla previamente o usar grep -q.

02-test-y-operadores.md
El comando test, [ ], y la palabra reservada [[ ]]
test y su alias [

El comando test evalúa condiciones y retorna 0 (verdadero) o 1 (falso). [ es un enlace simbólico a test que exige que el último argumento sea ]. Por eso los espacios son cruciales:
bash

if [ "$a" = "$b" ]; then ...   # correcto
if [$a=$b]; then               # error de sintaxis

Los operadores dentro de [ ] se clasifican en:

    Cadenas: = (igual), != (distinto), -z (cadena vacía), -n (cadena no vacía).

    Números: -eq, -ne, -lt, -le, -gt, -ge. Solo enteros.

    Archivos: -e (existe), -f (archivo regular), -d (directorio), -r (legible), -w (escribible), -x (ejecutable), -s (no vacío), -L (enlace simbólico), -O (propietario), etc.

    Lógicos: ! (NOT), -a (AND), -o (OR). Deben ser operadores dentro del mismo [ ], con todos los espacios.

Limitaciones de [:

    No maneja bien cadenas vacías sin comillas.

    Los operadores && y || de shell no funcionan dentro de [ ]; hay que hacerlos fuera o usar -a/-o.

    Con variables no entrecomilladas, el word splitting rompe la sintaxis.

Ejemplo:
bash

# Peligroso: si $archivo está vacío, se convierte en [ = ".txt" ] y da error
[ $archivo = ".txt" ]

# Seguro
[ "$archivo" = ".txt" ]

[[ ]]: la mejora nativa de Bash

[[ ]] es una palabra reservada de Bash (no un comando) que soluciona muchos problemas:

    No realiza word splitting ni expansión de nombres de archivo sobre las variables dentro.

    Permite && y || lógicos dentro sin confundir con redirecciones.

    Soporta el operador =~ para expresiones regulares.

    Permite patrones de globbing con == (sin entrecomillar el patrón).

    Soporta el operador -v para verificar si una variable está definida.

Operadores adicionales en [[ ]]:

    =~ : compara con expresión regular.

    == : igual que =, pero además permite patrones glob (*, ?, [...]) si la parte derecha no está entrecomillada. Ej: [[ $name == admin* ]].

    <, > : comparación lexicográfica (según locale). No confundir con redirecciones; deben escaparse (\<) o usarse dentro de [[ ]] sin problemas.

Ejemplos con [[ ]]:
bash

# Regex
if [[ "$ip" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "IP válida"
fi

# Globbing
if [[ "$archivo" == *.log ]]; then
    echo "Es un archivo de log"
fi

# Verificar si variable definida
if [[ -v usuario ]]; then
    echo "Variable usuario existe"
fi

Evaluación aritmética (( ))

Para comparaciones numéricas, Bash ofrece (( )) que devuelve 0 si la expresión aritmética es verdadera (distinta de 0) y 1 si es 0 (falsa). Es más natural para números:
bash

if (( contador > 10 && contador <= 20 )); then
    echo "En rango"
fi

Dentro de (( )) no se necesita $ para las variables, y se pueden usar operadores de C: >, <, >=, <=, ==, !=, &&, ||, !.
03-case.md
case: cuando tienes muchas ramas sobre un mismo valor

La sentencia case compara una expresión con una serie de patrones glob. Es mucho más limpia que concatenar if/elif para comparaciones de igualdad.
Sintaxis
bash

case $variable in
    patrón1)
        comandos;;
    patrón2|patrón3)
        comandos;;
    *)
        comandos por defecto;;
esac

Cada rama termina con ;; (equivalente a un break). Existen otros finalizadores:

    ;& → ejecuta la siguiente rama sin evaluar su patrón (fall-through al estilo C).

    ;;& → ejecuta la siguiente rama evaluando su patrón (útil para múltiples coincidencias).

Patrones

Los patrones son los mismos que usa el globbing: *, ?, [...], y se puede usar | para alternativas. No son expresiones regulares.

Ejemplos de patrones:

    [0-9]* : empieza con dígito.

    *.txt : termina en .txt.

    si|s|yes|y : cualquiera de esas palabras.

    ?*.log : al menos un carácter seguido de .log.

Ejemplo típico: menú de opciones
bash

read -p "Elige [iniciar|detener|estado]: " opcion
case $opcion in
    iniciar|start)
        systemctl start mi-servicio
        ;;
    detener|stop)
        systemctl stop mi-servicio
        ;;
    estado|status)
        systemctl status mi-servicio
        ;;
    *)
        echo "Opción no válida"
        ;;
esac

Uso de ;;& para múltiples tests
bash

case $var in
    a*)
        echo "Empieza con a"
        ;;&
    *b*)
        echo "Contiene b"
        ;;&
    *)
        echo "Rama por defecto"
        ;;
esac

Si var="abc", imprimirá las tres líneas.
Capturar patrones con shopt -s extglob

Con la opción extglob activada, case puede usar patrones extendidos como @(pat1|pat2), *(pat), +(pat), ?(pat), !(pat). Esto potencia mucho las posibilidades.
04-bucles-for-while-until.md
Bucles en Bash: iteraciones controladas
for estilo lista
bash

for variable in lista; do
    comandos
done

La lista puede ser literal (1 2 3), expansión de llaves ({1..10}), globbing (*.txt), salida de un comando ($(seq 1 5)), o un array (${arr[@]}).

Iterar sobre argumentos: por defecto in "$@":
bash

for arg; do
    echo "Argumento: $arg"
done

for estilo C
bash

for (( inicialización; condición; incremento )); do
    comandos
done

Ejemplo:
bash

for (( i=0; i<10; i++ )); do
    echo "i=$i"
done

Este estilo es exclusivo de Bash/Ksh/Zsh, no POSIX.
while

Ejecuta el cuerpo mientras el comando de prueba retorne 0.
bash

while [ condición ]; do
    comandos
done

También se puede usar [[ ]] o (( )). Se puede combinar con read para leer líneas de un archivo o entrada estándar.
bash

while IFS= read -r linea; do
    echo "Línea: $linea"
done < archivo.txt

Cuidado con la variable dentro de tuberías: si usas cmd | while ..., el while se ejecuta en un subshell y las variables modificadas dentro no sobreviven. Soluciones: usar <<< here-string, redirección, o shopt -s lastpipe (en Bash 4.2+).
until

Es el opuesto de while: se ejecuta hasta que el comando retorne 0 (éxito).
bash

until ping -c1 -W1 servidor &>/dev/null; do
    echo "Esperando servidor..."
    sleep 2
done

Control de bucles: break y continue

    break [n] : sale del bucle (o de n niveles anidados).

    continue [n] : salta a la siguiente iteración.

Iterar sobre archivos con espacios en nombres

El globbing maneja correctamente los espacios si se usa "$var". Ejemplo:
bash

for archivo in *.txt; do
    [ -e "$archivo" ] || continue   # por si no hay archivos
    echo "Procesando $archivo"
done

05-select-menus.md
Creando menús interactivos sencillos con select

Bash incorpora select para construir menús numéricos automáticos, ideales para scripts interactivos.
Sintaxis
bash

select variable in lista; do
    case $variable in
        opcion1) ... ;;
        opcion2) ... ;;
        *) ... ;;
    esac
    break  # normalmente se sale con break, o no si se quiere repetir el menú
done

El sistema muestra un menú numerado (usando PS3 como prompt) y asigna el texto seleccionado a variable, además de guardar el número en REPLY. Si el usuario ingresa un número inválido, variable queda vacía.
Ejemplo completo
bash

#!/bin/bash
PS3="Elige una opción (1-4): "
select opcion in "Listar" "Crear archivo" "Ver fecha" "Salir"; do
    case $opcion in
        "Listar")
            ls -l
            ;;
        "Crear archivo")
            touch nuevo.txt && echo "Creado"
            ;;
        "Ver fecha")
            date
            ;;
        "Salir")
            echo "Adiós"
            break
            ;;
        *)
            echo "Opción no válida: $REPLY"
            ;;
    esac
done

El break en la rama "Salir" termina el bucle select. Las demás ramas no llevan break, por lo que el menú se repetirá.
Personalización

    PS3: prompt que se muestra antes de leer la entrada.

    COLUMNS: ancho del terminal; si se define un valor pequeño, el formato puede cambiar.

    select es ideal para prototipos rápidos. Para diálogos más complejos, existen herramientas como dialog o whiptail.

Scripts de ejemplo
scripts/condiciones.sh
bash

#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------
# condiciones.sh - Demostración de estructuras condicionales
# ---------------------------------------------------------------

# --- Recibir argumento ---
archivo="${1:-}"

# 1. Verificar si se proporcionó el argumento
if [[ -z "$archivo" ]]; then
    echo "Uso: $0 <archivo>"
    exit 1
fi

# 2. Pruebas de archivo con if/elif/else
if [[ ! -e "$archivo" ]]; then
    echo "El archivo '$archivo' no existe."
    exit 2
elif [[ -d "$archivo" ]]; then
    echo "'$archivo' es un directorio."
elif [[ -f "$archivo" ]]; then
    echo "'$archivo' es un archivo regular."
    # Pruebas adicionales
    [[ -r "$archivo" ]] && echo "  -> Tiene permiso de lectura." || echo "  -> No se puede leer."
    [[ -s "$archivo" ]] && echo "  -> No está vacío." || echo "  -> Está vacío."
else
    echo "'$archivo' es otro tipo de archivo."
fi

# 3. Comparaciones numéricas y de cadena
contador=15
umbral=10
if (( contador > umbral )); then
    echo "El contador ($contador) supera el umbral ($umbral)."
fi

# Usando [[ ]] para cadenas con patrón
if [[ "$archivo" == *.log ]]; then
    echo "Advertencia: Estás trabajando con un archivo de log."
fi

# 4. Uso de case para clasificar extensión
extension="${archivo##*.}"
case "$extension" in
    txt|md)
        echo "Parece un archivo de texto."
        ;;
    sh|bash)
        echo "Es un script de shell."
        ;;
    jpg|png|gif)
        echo "Imagen detectada."
        ;;
    *)
        echo "Extensión desconocida: .$extension"
        ;;
esac

scripts/adivina-numero.sh
bash

#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------
# adivina-numero.sh - Juego de adivinanza con bucles y condiciones
# ---------------------------------------------------------------

# Generar número aleatorio entre 1 y 100
numero_secreto=$(( RANDOM % 100 + 1 ))
intentos=0
max_intentos=7

echo "Adivina el número entre 1 y 100. Tienes $max_intentos intentos."

# Bucle principal while
while (( intentos < max_intentos )); do
    # Incrementar contador de intentos
    (( intentos++ ))
    
    # Leer entrada del usuario de manera robusta
    read -r -p "Intento $intentos/$max_intentos: " entrada

    # Validar que sea un número entero positivo (usando [[ ]] y regex)
    if [[ ! "$entrada" =~ ^[0-9]+$ ]]; then
        echo "Por favor, ingresa un número válido."
        (( intentos-- ))  # no cuenta como intento
        continue
    fi

    # Convertir a entero (aunque ya es cadena numérica)
    suposicion=$entrada

    # Evaluar con condicionales
    if (( suposicion == numero_secreto )); then
        echo "¡Correcto! Adivinaste en $intentos intentos."
        exit 0
    elif (( suposicion < numero_secreto )); then
        echo "Demasiado bajo."
    else
        echo "Demasiado alto."
    fi
done

# Si sale del bucle, se acabaron los intentos
echo "Lo siento, has agotado tus intentos. El número era: $numero_secreto"
exit 1

01-definicion-y-parametros.md
Definiendo funciones: la base de la modularidad en Bash

En Bash existen dos sintaxis equivalentes para definir funciones. Ambas hacen exactamente lo mismo:
bash

# Sintaxis clásica (POSIX)
nombre_de_funcion() {
    comandos
}

# Sintaxis con palabra reservada
function nombre_de_funcion {
    comandos
}

Puedes mezclar estilos (aunque no es recomendable): function nombre() { ... } también funciona. Las llaves { } delimitan el cuerpo y deben ir separadas por espacios o saltos de línea del contenido.
Parámetros posicionales dentro de la función

Las funciones reciben sus propios argumentos, igual que un script. Los parámetros $1, $2, ..., $@, $# se refieren a los argumentos pasados a la función, no a los del script principal.
bash

saludar() {
    echo "Hola, $1!"
}
saludar "María"   # Imprime: Hola, María!

Dentro de una función, $0 sigue siendo el nombre del script (o del shell). Para obtener el nombre de la función actual se usa FUNCNAME[0].

Acceso a todos los argumentos:

    $@ se expande a la lista de argumentos, cada uno entrecomillado si usas "$@".

    $* los expande como una sola palabra unida por el primer carácter de IFS.

    $# indica el número de argumentos.

Ejemplo de función robusta que itera argumentos:
bash

listar_argumentos() {
    echo "Recibí $# argumentos:"
    local i=1
    for arg in "$@"; do
        echo "  Arg $i: $arg"
        ((i++))
    done
}
listar_argumentos "a b" c d   # los espacios en "a b" se respetan

Desplazamiento de parámetros con shift

Dentro de la función también se puede usar shift para descartar los primeros argumentos, muy útil para procesar opciones.
bash

parsear_opciones() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -v|--verbose) verbose=1 ;;
            -o|--output)  shift; output="$1" ;;
            --) shift; break ;;
            -*) echo "Opción desconocida: $1"; return 1 ;;
            *) break ;;
        esac
        shift
    done
    echo "Resto de argumentos: $@"
}

Parámetros con valores por defecto y validación

Puedes usar las expansiones de parámetros para asignar valores por defecto:
bash

conectar() {
    local host="${1:-localhost}"
    local puerto="${2:-22}"
    echo "Conectando a $host en puerto $puerto..."
}
conectar            # localhost:22
conectar "server"   # server:22

Para validar que un argumento sea obligatorio:
bash

procesar_archivo() {
    local archivo="${1:?Error: falta el nombre del archivo}"
    [[ -f "$archivo" ]] || { echo "No existe $archivo"; return 1; }
    # ...
}

Pasar argumentos desde arrays o variables

Si necesitas pasar argumentos almacenados en un array, la expansión correcta es "${array[@]}":
bash

args=("--verbose" "--output=salida.txt")
mi_funcion "${args[@]}"

02-retorno-y-variables-locales.md
Sacar datos de una función: códigos de salida y captura de salida

Las funciones en Bash no pueden devolver objetos complejos; tienen dos mecanismos principales de retorno:
1. Códigos de salida con return

La instrucción return [n] finaliza la función y establece $? con el valor n (entre 0 y 255). Por convención, 0 indica éxito y otro valor error.
bash

es_par() {
    (( $1 % 2 == 0 )) && return 0
    return 1
}

if es_par 4; then
    echo "Es par"
else
    echo "Es impar"
fi

No uses return para devolver datos (como cadenas), solo para indicar estado. Si necesitas devolver un valor numérico mayor a 255, tienes que capturarlo por otro medio (ver abajo).
2. Captura de la salida estándar (stdout)

La forma más versátil de devolver información es emitirla con echo o printf y capturarla mediante sustitución de comandos:
bash

obtener_fecha() {
    date "+%Y-%m-%d"
}

hoy=$(obtener_fecha)
echo "Hoy es $hoy"

Ten cuidado con echo: si tu función produce salida de depuración o logs, también será capturada. Usa stderr para mensajes informativos:
bash

buscar_usuario() {
    local login="$1"
    echo "Buscando en base de datos..." >&2   # no interfiere con el resultado
    grep "^$login:" /etc/passwd | cut -d: -f5
}

Devolver múltiples valores: puedes emitirlos separados por espacios (o cualquier delimitador) y luego leerlos con read:
bash

calcular_min_max() {
    local a=$1 b=$2
    if (( a < b )); then
        echo "$a $b"
    else
        echo "$b $a"
    fi
}

read min max < <(calcular_min_max 10 5)
echo "min=$min, max=$max"   # min=5, max=10

3. Variables globales y locales

Por defecto, las variables definidas dentro de una función son globales (visibles en todo el script). Para limitar su alcance a la función (y a las funciones que ésta llame, debido al scoping dinámico), debes declararlas con local.
bash

mi_script() {
    global=10
    local local_var=20

    otra_funcion
    echo "global=$global, local_var=$local_var"  # 10, 20
}

otra_funcion() {
    echo "Dentro de otra_funcion: global=$global, local_var=$local_var"
    global=30            # modifica la global del ámbito superior
    local_var=40         # ¡modifica la local de mi_script! (scoping dinámico)
}

mi_script

El comportamiento es que local crea una variable ligada al ámbito de la función que la declaró, y cualquier función anidada puede leerla y escribirla (como si fuera global en ese árbol de llamadas). Para evitar colisiones, es buena práctica usar local siempre en funciones.
FUNCNAME, BASH_SOURCE y LINENO para depuración

    FUNCNAME es un array con la pila de llamadas: ${FUNCNAME[0]} es la función actual, ${FUNCNAME[1]} la que la llamó, etc.

    BASH_SOURCE contiene los nombres de los archivos de cada nivel.

    LINENO es el número de línea actual (en el script o función).

bash

depurar() {
    echo "Función: ${FUNCNAME[1]} en ${BASH_SOURCE[1]}, línea ${BASH_LINENO[0]}"
}

03-librerias-y-source.md
Creando bibliotecas de funciones reutilizables

Puedes agrupar funciones en archivos separados y cargarlos en tu script con source (o su alias .). Esto evita duplicar código y facilita el mantenimiento.
Sintaxis
bash

# Desde un script o línea de comandos
source ./ruta/archivo_funciones.sh
# o bien
. ./ruta/archivo_funciones.sh

La diferencia entre source y la ejecución directa (bash archivo.sh) es que source no inicia un proceso hijo; las definiciones de funciones, variables y cambios de entorno ocurren en el shell actual.
Rutas relativas y absolutas

Si usas rutas relativas en un script, recuerda que se resolverán respecto al directorio de trabajo actual ($PWD), que puede no ser el directorio donde está el script. Para cargar una biblioteca que siempre acompaña al script, determina el directorio del script con:
bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/utils.sh"

BASH_SOURCE[0] es el camino al archivo actual (incluso si fue sourceado), mientras que $0 es el script principal.
Protección contra ejecución doble

Una función común es incluir una biblioteca que sólo debe ser sourceada, no ejecutada directamente. Para detectar si el script está siendo ejecutado (no sourceado), comparamos $0 con BASH_SOURCE[0]:
bash

# Al final de utils.sh
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Este archivo debe ser sourceado, no ejecutado."
    echo "Uso: source $(basename "$0")"
    exit 1
fi

Alternativamente, si el script debe comportarse diferente al ser ejecutado directamente, podemos usar esta detección para mostrar tests o ejemplos.
Técnicas avanzadas de bibliotecas

    Evitar recarga innecesaria: usa una variable de guarda para no cargar la biblioteca dos veces.

bash

if [[ -n "${_UTILS_SH_LOADED:-}" ]]; then
    return 0
fi
_UTILS_SH_LOADED=1

# ... definiciones de funciones ...

    Bibliotecas con funciones y constantes: exporta variables solo si es necesario, y usa readonly para constantes.

    Organización: guarda las bibliotecas en $HOME/lib/bash o en /usr/local/lib/bash y añádelas al path, o utiliza un directorio relativo al script.

04-recursividad.md
Funciones que se llaman a sí mismas

Bash soporta recursividad sin límite explícito fijado por el lenguaje, pero la pila de llamadas consume recursos del sistema y puede llegar a saturarse con unos miles de niveles (depende del sistema). No hay optimización de recursión de cola.
Ejemplo clásico: factorial
bash

factorial() {
    local n=$1
    if (( n <= 1 )); then
        echo 1
    else
        local prev
        prev=$(factorial $((n - 1)))
        echo $(( n * prev ))
    fi
}

resultado=$(factorial 5)
echo "5! = $resultado"   # 120

Nota: al usar $() se invoca un subshell, lo que puede impactar el rendimiento. En este ejemplo el resultado se emite con echo y se captura, lo cual es correcto pero no muy eficiente. Una alternativa es usar variables globales para acumular (con cuidado de no interferir con llamadas concurrentes).
Ejemplo: recorrido recursivo de directorios
bash

listar_recursivo() {
    local dir="$1"
    for entrada in "$dir"/* "$dir"/.[!.]* "$dir"/..?*; do
        [ -e "$entrada" ] || continue
        if [[ -d "$entrada" && ! -L "$entrada" ]]; then
            echo "[DIR] $entrada"
            listar_recursivo "$entrada"
        else
            echo "[FILE] $entrada"
        fi
    done
}
listar_recursivo "/ruta/a/directorio"

Ten cuidado con los enlaces simbólicos a directorios: podrías generar un bucle infinito. En el ejemplo excluimos los enlaces con ! -L.
Control de la profundidad

Para evitar sobrepasar un límite de recursión, puedes pasar un contador:
bash

explorar() {
    local profundidad=$1 max=$2 dir=$3
    if (( profundidad > max )); then
        return
    fi
    echo "Procesando $dir (nivel $profundidad)"
    for sub in "$dir"/*/; do
        [ -d "$sub" ] && explorar $(( profundidad + 1 )) "$max" "$sub"
    done
}

Consideraciones de rendimiento y depuración

    La recursividad con echo y $() crea muchos procesos hijos; para tareas masivas considera un enfoque iterativo.

    La variable FUNCNAME te permite inspeccionar la pila de llamadas; útil para depurar.

    set -x muestra todas las llamadas, pero puede generar una salida enorme.

Scripts de ejemplo
scripts/calculadora.sh

Una calculadora interactiva que utiliza funciones para cada operación, con menú select y validación de entrada. Demuestra parámetros, retorno por echo y manejo de errores.
bash

#!/usr/bin/env bash
set -euo pipefail

# Función: sumar
sumar() {
    echo "$(( $1 + $2 ))"
}

# Función: restar
restar() {
    echo "$(( $1 - $2 ))"
}

# Función: multiplicar
multiplicar() {
    echo "$(( $1 * $2 ))"
}

# Función: dividir (con validación)
dividir() {
    local a=$1 b=$2
    if (( b == 0 )); then
        echo "Error: división por cero" >&2
        return 1
    fi
    # Bash no hace división flotante; usamos bc para decimales
    echo "scale=4; $a / $b" | bc
}

# --- Menú interactivo ---
PS3="Elige operación (1-5): "
opciones=("Sumar" "Restar" "Multiplicar" "Dividir" "Salir")

select opcion in "${opciones[@]}"; do
    if [[ "$opcion" == "Salir" ]]; then
        echo "Adiós"
        break
    fi

    # Pedir operandos
    read -r -p "Primer número: " num1
    read -r -p "Segundo número: " num2

    # Validar que sean números (enteros o decimales simples)
    if [[ ! "$num1" =~ ^-?[0-9]+(\.[0-9]+)?$ ]] || [[ ! "$num2" =~ ^-?[0-9]+(\.[0-9]+)?$ ]]; then
        echo "Ambos operandos deben ser números" >&2
        continue
    fi

    case "$opcion" in
        "Sumar")
            resultado=$(sumar "$num1" "$num2")
            ;;
        "Restar")
            resultado=$(restar "$num1" "$num2")
            ;;
        "Multiplicar")
            resultado=$(multiplicar "$num1" "$num2")
            ;;
        "Dividir")
            if ! resultado=$(dividir "$num1" "$num2"); then
                # La función devolvió error (>2 ya mostró mensaje)
                continue
            fi
            ;;
        *)
            echo "Opción no válida: $REPLY"
            continue
            ;;
    esac

    echo "Resultado: $resultado"
done

scripts/utils.sh

Librería de funciones útiles para cualquier script. Incluye funciones para logging, manejo de errores y comprobación de permisos. Está preparada para ser sourceada.
bash

#!/usr/bin/env bash
# utils.sh - Funciones de utilidad reutilizables
# Debe ser cargado con: source utils.sh

# Evitar carga múltiple
if [[ -n "${_UTILS_SH_LOADED:-}" ]]; then
    return 0
fi
readonly _UTILS_SH_LOADED=1

# ------------------------------------------------------------
# Configuración
# ------------------------------------------------------------

# Colores para mensajes (opcional)
readonly COLOR_RESET='\e[0m'
readonly COLOR_RED='\e[31m'
readonly COLOR_GREEN='\e[32m'
readonly COLOR_YELLOW='\e[33m'

# Activar colores solo si la salida es una terminal
if [[ -t 1 ]]; then
    _USE_COLOR=1
else
    _USE_COLOR=0
fi

# ------------------------------------------------------------
# Funciones de logging
# ------------------------------------------------------------

info() {
    if (( _USE_COLOR )); then
        echo -e "${COLOR_GREEN}[INFO]${COLOR_RESET} $(date '+%Y-%m-%d %H:%M:%S') - $*"
    else
        echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $*"
    fi
}

warn() {
    if (( _USE_COLOR )); then
        echo -e "${COLOR_YELLOW}[WARN]${COLOR_RESET} $(date '+%Y-%m-%d %H:%M:%S') - $*" >&2
    else
        echo "[WARN] $(date '+%Y-%m-%d %H:%M:%S') - $*" >&2
    fi
}

error() {
    if (( _USE_COLOR )); then
        echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $(date '+%Y-%m-%d %H:%M:%S') - $*" >&2
    else
        echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $*" >&2
    fi
}

# ------------------------------------------------------------
# Manejor de errores críticos (finaliza el script)
# ------------------------------------------------------------

die() {
    error "$*"
    exit 1
}

# ------------------------------------------------------------
# Verificar si se ejecuta como root
# ------------------------------------------------------------

require_root() {
    if [[ $EUID -ne 0 ]]; then
        die "Este script debe ejecutarse como root"
    fi
}

# ------------------------------------------------------------
# Verificar comandos necesarios
# ------------------------------------------------------------

require_cmd() {
    local cmd
    for cmd in "$@"; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            die "Comando '$cmd' no encontrado. Instálalo e inténtalo de nuevo."
        fi
    done
}

# ------------------------------------------------------------
# Función de ayuda (genérica)
# ------------------------------------------------------------

show_help() {
    cat <<EOF
Uso: $(basename "$0") [opciones]

Opciones:
  -h, --help    Muestra esta ayuda
  -v, --verbose Modo detallado

EOF
}

# ------------------------------------------------------------
# Protección: si se ejecuta directamente, mostrar advertencia
# ------------------------------------------------------------

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Este archivo es una biblioteca de funciones. Debe ser cargado con:"
    echo "   source $(basename "$0")"
    exit 1
fi

01-redirecciones-y-pipes.md
El arte de redirigir entradas y salidas

Bash maneja tres flujos estándar para cada proceso: stdin (entrada, descriptor 0), stdout (salida normal, descriptor 1) y stderr (errores, descriptor 2). Las redirecciones permiten conectar estos flujos a archivos, otros comandos o dispositivos.
Redirección de salida estándar (stdout)
Operador	Acción
comando > archivo	Redirige stdout a archivo, sobrescribiéndolo si existe. Crea el archivo si no existe.
comando >> archivo	Redirige stdout a archivo, añadiendo al final.

Ejemplo:
bash

echo "Línea 1" > salida.txt   # Crea/sobrescribe
echo "Línea 2" >> salida.txt  # Añade

Redirección de errores estándar (stderr)
Operador	Acción
comando 2> archivo	Redirige stderr a archivo (sobrescribir).
comando 2>> archivo	Añade stderr.

Ejemplo:
bash

ls /ruta_inexistente 2> errores.log

Redirigir ambos (stdout y stderr) al mismo destino

Existen dos sintaxis comunes:
Operador	Acción
comando > archivo 2>&1	Redirige stdout a archivo, y luego stderr al mismo lugar que stdout. El orden importa: primero > archivo y luego 2>&1.
comando &> archivo	Redirige ambos a archivo (equivalente a > archivo 2>&1). Sintaxis preferida en Bash moderno.
comando &>> archivo	Añade ambos.

Ejemplo:
bash

complejo.sh &> todo.log

Redirigir a /dev/null

Para descartar salida:
bash

comando > /dev/null 2>&1   # Silencia todo

Redirigir entrada estándar (stdin)
Operador	Acción
comando < archivo	Lee stdin desde archivo.
comando << EOF	Here-document (ver tema 03).
comando <<< "cadena"	Here-string (ver tema 03).
Duplicar y mover descriptores

Con exec puedes manipular descriptores personalizados (3-9) para tareas avanzadas como rotar salidas o mantener múltiples flujos simultáneos.
bash

# Abrir archivo como descriptor 3 para escritura
exec 3> log.txt
echo "Mensaje 1" >&3       # Escribe en log.txt vía descriptor 3
exec 3>&-                  # Cerrar descriptor

Tuberías (pipelines)

Las tuberías (|) conectan la salida estándar de un comando con la entrada estándar del siguiente:
bash

comando1 | comando2 | comando3

Características importantes:

    Cada comando en la tubería se ejecuta en un subshell (excepto builtins en ciertos casos con shopt -s lastpipe en Bash 4.2+).

    PIPESTATUS es un array con los códigos de salida de cada comando de la última tubería (útil para detectar fallos intermedios).

    La opción set -o pipefail hace que una tubería falle si cualquier comando falla (no solo el último).

Ejemplo con PIPESTATUS:
bash

curl -s http://ejemplo.com/inexistente | grep "algo"
echo "${PIPESTATUS[0]}"   # Código de curl
echo "${PIPESTATUS[1]}"   # Código de grep

Tuberías con stderr y tee

    |& es un atajo para 2>&1 |, redirige stderr y stdout a la tubería (Bash 4+).

    tee lee de stdin y escribe tanto a stdout como a uno o más archivos. Ideal para registrar salida y seguir viéndola.

bash

comando 2>&1 | tee -a registro.log

Sustitución de procesos avanzada

    <(comando) genera un archivo temporal (o pipe) con la salida del comando. Se comporta como un archivo de solo lectura.

    >(comando) proporciona un archivo donde escribir; la entrada se envía al comando.

bash

diff <(ls dir1) <(ls dir2)          # Compara listados sin archivos temporales
tar cf >(ssh destino "tar xf -") .  # Transfiere tar por ssh

02-lectura-y-escritura.md
Leer del usuario y escribir en pantalla o archivos con seguridad
read: capturar entrada del usuario o de un archivo
bash

read [-p prompt] [-s] [-t timeout] [-n nchars] [-a array] [-d delim] variable1 variable2 ...

    -p "texto": muestra un prompt sin necesidad de echo.

    -s: modo silencioso (no eco, ideal para contraseñas).

    -t segundos: tiempo máximo de espera.

    -n n: leer solo n caracteres (sin esperar Intro).

    -a arr: leer en un array, split según IFS.

    -d delim: cambiar delimitador (por defecto newline).

    -r: siempre usa -r para evitar que las barras invertidas se interpreten como escapes (trata la entrada de forma literal).

Ejemplo robusto:
bash

read -r -p "Nombre: " nombre
read -r -s -p "Contraseña: " pass; echo   # El echo extra para el salto de línea

Leer varias variables:
bash

read -r col1 col2 col3 <<< "uno dos tres"   # col3 recibe "tres"

IFS (Internal Field Separator)

IFS define los caracteres que separan palabras cuando read o la expansión de variables sin comillas dividen. Por defecto contiene espacio, tabulador y nueva línea. Puedes cambiarlo temporalmente para parsear líneas con campos delimitados:
bash

while IFS=: read -r usuario pass uid gid resto; do
    echo "Usuario: $usuario, UID: $uid"
done < /etc/passwd

Escribir en archivos de manera segura

Además de las redirecciones, puedes usar printf para formatear la salida y cat para combinar contenido.

    echo "algo" > archivo: simple pero echo puede interpretar escapes (\n) a menos que uses echo -E o el modo POSIX.

    printf "%s\n" "línea" > archivo: más predecible y seguro, especialmente con datos que pueden comenzar con -.

Crear un archivo vacío:
bash

> nuevo.txt      # Redirigir nada (crea/trunca)
: > nuevo.txt    # Alternativa con comando : (no-op)

Bloqueos de archivos (flock)

Para evitar condiciones de carrera al escribir en un mismo archivo desde múltiples procesos, puedes usar flock:
bash

exec 200>archivo.lock
flock -e 200  # bloqueo exclusivo
# ... operaciones ...
flock -u 200  # desbloquear

Leer línea por línea (sin problemas de subshell)

El clásico bucle while read con redirección al final del bucle es la forma correcta para que las variables sobrevivan:
bash

while IFS= read -r linea || [[ -n "$linea" ]]; do   # maneja última línea sin newline
    echo "Procesando: $linea"
done < archivo.txt

Si se usa tubería (cat archivo | while ...), el while se ejecuta en un subshell y cualquier variable modificada se pierde. Alternativas: redirección simple como arriba, o shopt -s lastpipe (en scripts, no interactivo).
03-here-docs-y-strings.md
Documentos incrustados y cadenas redirigidas
Here-document (<<)

Permiten introducir bloques multilínea directamente en el script:
bash

comando << DELIMITADOR
línea 1
línea 2
DELIMITADOR

La palabra delimitadora puede ser cualquier identificador; por convención se usa EOF, END, etc. Si el delimitador está entrecomillado (<< "EOF"), no se realiza expansión de variables ni comandos dentro del bloque (como comillas simples). Si no está entrecomillado, se expanden $var, $(comando), etc.

Ejemplo con expansión:
bash

cat << FIN
Hoy es $(date)
Tu home es $HOME
FIN

Ejemplo sin expansión:
bash

cat << 'FIN'
La variable $HOME no se expande aquí.
FIN

Here-document con supresión de tabuladores

Usando <<- (con guión), las tabulaciones iniciales de cada línea (solo tabuladores, no espacios) se eliminan, lo que permite indentar el bloque sin que aparezcan en el resultado.
bash

if [[ condicion ]]; then
    cat <<- EOF
        Mensaje indentado con tabs,
        pero al imprimir se eliminan los tabs.
    EOF
fi

Here-string (<<<)

Pasa una cadena como entrada estándar a un comando. Es más limpia que echo "cadena" | comando.
bash

tr 'a-z' 'A-Z' <<< "hola mundo"   # HOLA MUNDO
read -r var1 var2 <<< "uno dos"

Usos típicos

    Generar archivos de configuración temporales.

    Enviar múltiples líneas a un comando (como mail, cat, bc).

    Proporcionar respuestas automáticas a programas interactivos:

bash

./instalador << RESPUESTAS
yes
/ruta/de/instalacion
no
RESPUESTAS

Combinar con cat y redirecciones para crear archivos
bash

cat > archivo.conf << 'EOF'
server {
    listen 80;
    server_name ejemplo.com;
}
EOF

04-manipulacion-de-cadenas.md
El poder de las expansiones de parámetros sin herramientas externas

Bash ofrece un conjunto muy rico de operaciones sobre cadenas directamente con la sintaxis ${variable...}. Rara vez necesitarás sed o awk para tareas básicas de cadenas (aunque siguen siendo potentes complementos).
Obtener longitud
bash

cadena="Hola Mundo"
echo "${#cadena}"         # 10

Extraer subcadenas
bash

echo "${cadena:0:4}"      # Hola  (offset, longitud)
echo "${cadena:5}"        # Mundo (desde offset hasta el final)
echo "${cadena:(-5):5}"   # Mundo (índices negativos cuentan desde el final)

Eliminar prefijo o sufijo (más corto y más largo)
Expresión	Significado
${var#patrón}	Elimina la coincidencia más corta del prefijo.
${var##patrón}	Elimina la coincidencia más larga del prefijo.
${var%patrón}	Elimina la coincidencia más corta del sufijo.
${var%%patrón}	Elimina la coincidencia más larga del sufijo.

Los patrones son globs, no regex.

Ejemplos:
bash

ruta="/home/usuario/documento.txt"
echo "${ruta##*/}"    # documento.txt  (todo antes del último /)
echo "${ruta%/*}"     # /home/usuario  (todo después del último /)
echo "${ruta%.txt}"   # /home/usuario/documento
echo "${ruta%%.*}"    # /home/usuario/documento (si no hay otro punto)

Reemplazo de subcadenas

    ${var/patrón/reemplazo}: reemplaza la primera ocurrencia.

    ${var//patrón/reemplazo}: reemplaza todas las ocurrencias.

    ${var/#patrón/reemplazo}: reemplaza solo si está al inicio.

    ${var/%patrón/reemplazo}: reemplaza solo si está al final.

bash

texto="gato. perro. gato."
echo "${texto/gato/ratón}"    # ratón. perro. gato.
echo "${texto//gato/ratón}"   # ratón. perro. ratón.
echo "${texto/#gato/ratón}"   # ratón. perro. gato.
echo "${texto/%gato./ratón}"  # gato. perro. ratón

Cambiar mayúsculas/minúsculas

    ${var^^}: todo a mayúsculas.

    ${var,,}: todo a minúsculas.

    ${var^}: primera letra a mayúscula.

    ${var,}: primera letra a minúscula.

bash

nombre="juan carlos"
echo "${nombre^}"     # Juan carlos
echo "${nombre^^}"    # JUAN CARLOS

Uso de @ o * en arrays

Las expansiones sobre arrays usando @ o * aplican la transformación a cada elemento:
bash

ciudades=("buenos aires" "la paz")
echo "${ciudades[@]^}"   # Buenos Aires La Paz

Combinar con patrones extendidos (extglob)

Las expansiones admiten patrones de extglob si se activa shopt -s extglob. Ejemplo: quitar extensión múltiple:
bash

shopt -s extglob
archivo="script.tar.gz"
echo "${archivo%.*}"    # script.tar
echo "${archivo%%.*}"   # script
echo "${archivo##*.}"   # gz

Truco: comprobar si una cadena contiene un patrón

Con [[ ]] y * como comodín:
bash

if [[ "$cadena" == *"subcadena"* ]]; then ...

Cuando necesitas sed o awk

Para tareas más complejas (expresiones regulares con grupos, reemplazos condicionales, cálculos numéricos), puedes incrustar sed o awk en el script, pero primero intenta con las expansiones nativas.
05-globbing-y-comodines.md
Selección de archivos mediante patrones

El globbing (expansión de nombres de archivo) es el mecanismo que convierte *.txt en la lista de archivos que coinciden. No usa expresiones regulares, sino patrones propios.
Caracteres comodín básicos
Patrón	Coincidencia
*	Cualquier cadena (incluso vacía).
?	Un carácter cualquiera (exactamente uno).
[abc]	Un carácter de la lista.
[a-z]	Rango de caracteres (según locale).
[!abc] o [^abc]	Un carácter que NO esté en la lista.

Ejemplos:
bash

ls -l *.txt       # Archivos .txt
ls -l foto?.jpg   # foto1.jpg, fotoA.jpg, pero no foto10.jpg
rm -i Archivo[1-5].log

shopt y opciones de globbing

    shopt -s nullglob: si no hay coincidencias, el patrón se expande a nada (en lugar de devolverse literal).

    shopt -s failglob: si no hay coincidencias, se produce un error.

    shopt -s nocaseglob: hace que el globbing sea insensible a mayúsculas/minúsculas.

    shopt -s globstar: habilita ** para coincidencia recursiva de directorios (Bash 4.0+).

    shopt -s dotglob: incluye archivos cuyo nombre comienza con punto (ocultos).

Ejemplo crucial con nullglob:
bash

shopt -s nullglob
for archivo in *.log; do
    # Si no hay .log, el bucle no se ejecuta ni una sola vez
    echo "Procesando $archivo"
done

Sin nullglob, el bucle ejecutaría un iteración con archivo='*.log' literal.
Expresiones de clase POSIX

Dentro de [...] se pueden usar clases:

    [:alpha:], [:digit:], [:alnum:], [:lower:], [:upper:], [:space:], etc.

Ejemplo: archivo[[:digit:]].txt coincide con archivos con un carácter dígito.
Recorrido recursivo con ** (globstar)

Con shopt -s globstar, ** coincide con cualquier número de subdirectorios:
bash

shopt -s globstar
for archivo in **/*.py; do
    echo "Script Python: $archivo"
done

Cuidado: puede ser costoso en árboles grandes.
Extended globbing (shopt -s extglob)

Habilita patrones compuestos avanzados:
Patrón	Coincidencia
?(patrón)	Cero o una ocurrencia del patrón.
*(patrón)	Cero o más ocurrencias del patrón.
+(patrón)	Una o más ocurrencias del patrón.
@(pat1|pat2)	Exactamente uno de los patrones (como OR).
!(patrón)	Cualquier cosa que no coincida con el patrón.

Ejemplos:
bash

shopt -s extglob
ls -d ?(*.txt|*.md)        # archivos con cero o una ocurrencia: .txt o .md
rm !(*.bak|*.tmp)          # borrar todo excepto .bak y .tmp (¡peligroso!)
cp @(uno|dos|tres).txt dir # copia solo esos tres archivos

Precauciones con globbing y espacios

El globbing maneja correctamente archivos con espacios siempre que las variables se entrecomillen. Nunca hagas for f in $(ls *.txt); prefiere:
bash

for f in *.txt; do
    echo "$f"
done

Scripts de ejemplo
scripts/backup-logs.sh

Un script que demuestra redirecciones, lectura de directorios, compresión, logging y comprobación de errores.
bash

#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------
# backup-logs.sh – Comprime logs y registra toda la actividad
# ---------------------------------------------------------------

# Configuración
LOG_DIR="${1:-/var/log}"
BACKUP_DIR="${2:-./backups}"
MAX_LOG_AGE=7   # días

# Archivo de log del propio script
SCRIPT_LOG="./backup.log"

# Función para escribir en log y mostrar por pantalla
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$SCRIPT_LOG"
}

# --- Inicio ---
log "Iniciando backup de $LOG_DIR hacia $BACKUP_DIR"

# Crear directorio de destino si no existe
mkdir -p "$BACKUP_DIR"

# Buscar archivos .log con más de MAX_LOG_AGE días y empaquetarlos
# Usamos find con -mtime y redirigimos errores a stderr (por defecto ya)
# La salida de find la procesamos con while read para manejar nombres con espacios

# Enfoque seguro: read con -print0 y null delimitador
find "$LOG_DIR" -type f -name "*.log" -mtime +$MAX_LOG_AGE -print0 2>> "$SCRIPT_LOG" | 
    while IFS= read -r -d '' archivo; do
        # Comprimir cada archivo en el directorio de backup, preservando estructura
        rel_path="${archivo#$LOG_DIR/}"
        dest="$BACKUP_DIR/${rel_path}.gz"

        # Crear subdirectorios necesarios
        mkdir -p "$(dirname "$dest")"
        
        if gzip -c "$archivo" > "$dest" 2>> "$SCRIPT_LOG"; then
            log "Comprimido: $archivo -> $dest"
            # Opcional: eliminar original si la compresión fue exitosa
            # rm "$archivo"
        else
            log "ERROR al comprimir: $archivo" >&2
        fi
    done

# Comprobar el código de salida del pipeline (si usamos pipefail, detecta fallos)
if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
    log "find reportó errores. Revisar $SCRIPT_LOG"
fi

# Crear un tarball general con todos los backups (con fecha)
fecha=$(date +%Y%m%d)
tarball="$BACKUP_DIR/backup-logs-$fecha.tar.gz"
log "Creando tarball general: $tarball"
if tar czf "$tarball" -C "$BACKUP_DIR" . --exclude='*.tar.gz' 2>> "$SCRIPT_LOG"; then
    log "Tarball creado exitosamente"
else
    log "Fallo al crear tarball"
    exit 1
fi

log "Backup finalizado."

scripts/renombrar-archivos.sh

Demuestra manipulación de cadenas, globbing, cambio de extensiones y prefijo/sufijo.
bash

#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------
# renombrar-archivos.sh – Cambia nombres de archivos en masa
# ---------------------------------------------------------------

mostrar_ayuda() {
    cat << EOF
Uso: $0 [opciones] <directorio>

Opciones:
  -p PREFIJO  Añadir prefijo a todos los archivos.
  -s SUFIJO   Añadir sufijo (antes de la extensión).
  -e EXT      Cambiar extensión (ej: -e .txt).
  --lower     Convertir nombres a minúsculas.
  --upper     Convertir nombres a mayúsculas.
  -n          Modo simulación (no renombra, solo muestra).
  -h          Esta ayuda.

Ejemplo:
  $0 -p "old_" -e .bak ./directorio
EOF
}

# --- Parseo de opciones ---
prefijo=""
sufijo=""
nueva_ext=""
lower=0
upper=0
simular=0

while getopts "p:s:e:hlnu" opt; do
    case $opt in
        p) prefijo="$OPTARG" ;;
        s) sufijo="$OPTARG" ;;
        e) nueva_ext="$OPTARG" ;;
        l) lower=1 ;;
        u) upper=1 ;;
        n) simular=1 ;;
        h) mostrar_ayuda; exit 0 ;;
        *) mostrar_ayuda >&2; exit 1 ;;
    esac
done
shift $((OPTIND -1))

directorio="${1:-.}"
if [[ ! -d "$directorio" ]]; then
    echo "Error: '$directorio' no es un directorio válido." >&2
    exit 1
fi

# Activar nullglob para que los bucles no ejecuten si no hay archivos
shopt -s nullglob

# Procesar todos los archivos (no recursivo por defecto)
for archivo in "$directorio"/*; do
    # Saltamos si no es un archivo regular
    [[ -f "$archivo" ]] || continue

    dir=$(dirname "$archivo")
    nombre_base=$(basename "$archivo")
    nombre="${nombre_base%.*}"       # nombre sin extensión
    extension="${nombre_base##*.}"   # extensión (todo tras el último punto)

    # Si no hay extensión (nombre_base no tiene punto), 'nombre' y 'nombre_base' coinciden
    if [[ "$nombre_base" = "$extension" ]]; then
        # Caso sin extensión
        extension=""
        nombre="$nombre_base"
    else
        extension=".$extension"
    fi

    nuevo_nombre="$nombre"

    # Aplicar minúsculas/mayúsculas
    if (( lower )); then
        nuevo_nombre="${nuevo_nombre,,}"
    elif (( upper )); then
        nuevo_nombre="${nuevo_nombre^^}"
    fi

    # Añadir prefijo y sufijo
    nuevo_nombre="${prefijo}${nuevo_nombre}${sufijo}"

    # Cambiar extensión si se especifica
    if [[ -n "$nueva_ext" ]]; then
        # Asegurar que la nueva extensión comience con punto
        [[ "$nueva_ext" == .* ]] || nueva_ext=".$nueva_ext"
        extension="$nueva_ext"
    fi

    nuevo_archivo="$dir/$nuevo_nombre$extension"

    # Si el nombre no cambió, seguir
    if [[ "$archivo" == "$nuevo_archivo" ]]; then
        continue
    fi

    # Evitar sobrescribir archivos existentes
    if [[ -e "$nuevo_archivo" ]]; then
        echo "Error: ya existe '$nuevo_archivo', no se renombrará '$archivo'" >&2
        continue
    fi

    if (( simular )); then
        echo "[SIMULACIÓN] '$archivo' -> '$nuevo_archivo'"
    else
        mv -- "$archivo" "$nuevo_archivo"
        echo "Renombrado: '$archivo' -> '$nuevo_archivo'"
    fi
done

05 – ARRAYS
01-arrays-indexados.md
Listas ordenadas con índice numérico

Los arrays indexados en Bash son colecciones de elementos accesibles mediante un índice entero, comenzando en 0. No tienen un tamaño fijo; pueden crecer y reducirse dinámicamente.
Creación y asignación

Forma compacta (elementos separados por espacios):
bash

frutas=("manzana" "naranja" "pera")

Asignación por índice:
bash

colores[0]="rojo"
colores[1]="verde"
colores[2]="azul"

Usando declare -a (opcional pero explícito):
bash

declare -a numeros=(1 2 3 4)

Añadir elementos al final:
bash

frutas+=("uva" "sandía")   # el operador += con paréntesis

Desde la salida de un comando (usando mapfile o readarray):
bash

mapfile -t lineas < archivo.txt   # cada línea es un elemento
# o readarray -t lineas < archivo.txt (sinónimo)

Acceso a elementos
Expresión	Significado
${array[i]}	Elemento en índice i.
${array[0]}	Primer elemento.
${array[@]}	Todos los elementos como palabras separadas (cada uno entrecomillado con "${array[@]}").
${#array[@]}	Número de elementos.
${#array[i]}	Longitud del elemento en índice i.
"${!array[@]}"	Lista de índices (útil si hay huecos).

Iterar sobre todos los elementos (forma segura):
bash

for elem in "${frutas[@]}"; do
    echo "$elem"
done

Iterar sobre índices:
bash

for i in "${!frutas[@]}"; do
    echo "Índice $i: ${frutas[$i]}"
done

Operaciones con arrays

Eliminar un elemento:
bash

unset frutas[1]            # quita el índice 1, deja un hueco
unset frutas               # elimina todo el array

Extraer sub-array (slicing):
bash

"${frutas[@]:inicio:longitud}"   # desde inicio, longitud opcional

Ejemplo: "${frutas[@]:1:2}" devuelve los índices 1 y 2.

Concatenar arrays:
bash

todos=("${array1[@]}" "${array2[@]}")

Copiar un array:
bash

copia=("${original[@]}")

Rellenar desde un comando (evitando ls):
bash

archivos=( *.txt )                # expande globbing con nullglob si es necesario

Huecos y comportamiento

Los arrays pueden tener índices no contiguos. ${#array[@]} cuenta los elementos definidos, no el índice máximo.
Trucos adicionales

    Comprobar si un array está vacío: [[ ${#miarray[@]} -eq 0 ]]

    Unir elementos en una cadena: usar IFS temporalmente:

bash

IFS=:
echo "${frutas[*]}"   # manzana:naranja:pera

El * los une con el primer carácter de IFS.

    Convertir cadena a array: usando read -a o mapfile con delimitador.

02-arrays-asociativos.md
Diccionarios: claves alfanuméricas

Los arrays asociativos (diccionarios) permiten usar cadenas como índices en lugar de números. Requieren Bash ≥ 4.0 y deben declararse explícitamente con declare -A.
Declaración y asignación
bash

declare -A capitales
capitales["Francia"]="París"
capitales=([Japón]="Tokio" [Brasil]="Brasilia")

# Añadir más
capitales+=(["Alemania"]="Berlín")

No se pueden crear asociativos sin declare -A.
Acceso a elementos

    ${capitales["clave"]} devuelve el valor.

    "${!capitales[@]}" devuelve todas las claves.

    "${capitales[@]}" devuelve todos los valores (sin las claves).

    ${#capitales[@]} es el número de elementos.

Iterar sobre el array
bash

for pais in "${!capitales[@]}"; do
    echo "$pais -> ${capitales[$pais]}"
done

El orden de las claves no está garantizado (no preserva el orden de inserción).
Comprobar si una clave existe
bash

if [[ -v capitales["$clave"] ]]; then
    echo "Existe"
fi

O usando -n con una expansión:
bash

if [[ -n "${capitales[$clave]+presente}" ]]; then ...

Eliminar claves
bash

unset capitales["Brasil"]
unset capitales   # borrar todo

Usos típicos

    Mapeos de configuración (ej.: puertos por servicio).

    Caché de resultados.

    Contadores por categoría.

Precauciones

    No confundir arrays indexados con asociativos: declare -a vs declare -A.

    No asignar con paréntesis sin declare -A.

    Si usas local -A dentro de una función, también funciona (Bash 4.3+).

scripts/gestion-contactos.sh

Script interactivo que demuestra arrays asociativos con un menú completo.
bash

#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------
# gestion-contactos.sh – Agenda de contactos con array asociativo
# ---------------------------------------------------------------

declare -A contactos    # nombre -> teléfono

# Cargar algunos de ejemplo
contactos=(
    ["Ana García"]="555-1234"
    ["Luis Pérez"]="555-5678"
    ["Marta Ruiz"]="555-9012"
)

# Guardar agenda en archivo (opcional)
ARCHIVO_AGENDA="./agenda.txt"

cargar_agenda() {
    if [[ -f "$ARCHIVO_AGENDA" ]]; then
        while IFS=: read -r nombre telefono; do
            [[ -z "$nombre" ]] && continue
            contactos["$nombre"]="$telefono"
        done < "$ARCHIVO_AGENDA"
    fi
}

guardar_agenda() {
    : > "$ARCHIVO_AGENDA"   # truncar
    for nombre in "${!contactos[@]}"; do
        echo "$nombre:${contactos[$nombre]}" >> "$ARCHIVO_AGENDA"
    done
}

listar() {
    if [[ ${#contactos[@]} -eq 0 ]]; then
        echo "Agenda vacía."
    else
        echo "--- Contactos ---"
        for nombre in "${!contactos[@]}"; do
            echo "  $nombre: ${contactos[$nombre]}"
        done | sort
    fi
}

buscar() {
    read -r -p "Nombre a buscar: " patron
    local encontrados=0
    for nombre in "${!contactos[@]}"; do
        if [[ "$nombre" == *"$patron"* ]]; then
            echo "$nombre: ${contactos[$nombre]}"
            ((encontrados++))
        fi
    done
    (( encontrados == 0 )) && echo "No se encontraron coincidencias."
}

añadir() {
    read -r -p "Nombre: " nombre
    if [[ -v contactos["$nombre"] ]]; then
        echo "Ya existe '$nombre'. Usa modificar para cambiarlo."
        return
    fi
    read -r -p "Teléfono: " telefono
    contactos["$nombre"]="$telefono"
    echo "Añadido."
}

modificar() {
    read -r -p "Nombre a modificar: " nombre
    if [[ ! -v contactos["$nombre"] ]]; then
        echo "No existe '$nombre'."
        return
    fi
    read -r -p "Nuevo teléfono: " telefono
    contactos["$nombre"]="$telefono"
    echo "Actualizado."
}

eliminar() {
    read -r -p "Nombre a eliminar: " nombre
    if [[ -v contactos["$nombre"] ]]; then
        unset contactos["$nombre"]
        echo "Eliminado."
    else
        echo "No existe '$nombre'."
    fi
}

# Menú principal
PS3="Elige opción (1-6): "
opciones=("Listar" "Buscar" "Añadir" "Modificar" "Eliminar" "Salir")

cargar_agenda   # Recuperar datos previos si existen

while true; do
    select opcion in "${opciones[@]}"; do
        case "$opcion" in
            "Listar")   listar ;;
            "Buscar")   buscar ;;
            "Añadir")   añadir ;;
            "Modificar") modificar ;;
            "Eliminar") eliminar ;;
            "Salir")
                guardar_agenda
                echo "¡Hasta luego!"
                exit 0
                ;;
            *) echo "Opción no válida" ;;
        esac
        break
    done
done

06 – PROCESOS Y SEÑALES
01-trabajos-en-segundo-plano.md
Ejecutar tareas sin bloquear la terminal
El operador &

Poner & al final de un comando lo envía al segundo plano inmediatamente:
bash

sleep 60 &
echo "PID de sleep: $!"   # $! es el PID del último proceso lanzado en bg

El proceso se ejecuta en background y el prompt retorna al instante. Bash muestra el número de trabajo ([1] 12345).
nohup: ignorar SIGHUP

Cuando cierras la terminal (señal SIGHUP), los procesos en segundo plano normalmente terminan. nohup los protege, generalmente redirigiendo la salida a nohup.out:
bash

nohup script_largo.sh &

disown: desvincular del shell

Permite que un trabajo siga corriendo incluso después de cerrar el shell, eliminándolo de la tabla de trabajos de Bash:
bash

proceso_largo &
disown          # desvincula el último trabajo en bg
disown %1       # desvincula trabajo con id 1
disown -h %1    # no envía SIGHUP pero lo mantiene en lista de trabajos

Salida estándar y errores

Los trabajos en bg siguen heredando la terminal como salida. Es buena práctica redirigir:
bash

comando > salida.log 2>&1 &

Listar trabajos (jobs)

jobs -l muestra los trabajos activos y sus PIDs.
Diferencia entre proceso y trabajo

Un proceso es una entidad del sistema con PID. Un trabajo es un concepto del shell: puede consistir en varios procesos (tuberías). El shell asigna números de trabajo (%1, %2, etc.).
02-control-de-trabajos.md
fg, bg y manejo interactivo

Cuando un trabajo está en segundo plano, puedes traerlo al primer plano o reactivarlo.
fg: traer al primer plano
bash

sleep 100 &
fg %1        # o fg 1, o simplemente fg (si solo hay un trabajo)

El trabajo recibe entrada de teclado y señales de terminal; el shell espera a que termine.
bg: reanudar en segundo plano

Si un trabajo está detenido (con Ctrl+Z), puedes reanudarlo en segundo plano:
bash

bg %1

Suspender con Ctrl+Z

Envía SIGTSTP, suspendiendo el proceso en primer plano. Aparece como detenido (Stopped) en jobs.
Matar trabajos con kill %n

kill %1 envía SIGTERM al grupo de procesos del trabajo. También puedes usar números de PID con kill $PID.
Estado de los trabajos
Estado mostrado por jobs	Significado
Running	Ejecutándose
Stopped	Detenido (suspendido)
Done	Terminado (esperando recolección)
Trabajos con tuberías
bash

cat archivo | grep algo | wc -l &

El trabajo %1 agrupa los tres procesos. jobs -l mostrará los PIDs individuales.
Limitaciones

El control de trabajos (job control) está habilitado por defecto en shells interactivos. En scripts no interactivos (set -m lo activa, pero rara vez se usa). En scripts es más común manejar procesos directamente con wait y PIDs.
03-seniales-y-trap.md
Manejar eventos asíncronos: señales

Las señales son interrupciones software que el sistema o el usuario envían a un proceso. Bash permite capturar varias de ellas con trap.
Señales comunes relevantes para scripts
Señal	Número típico	Disparador
SIGHUP	1	Terminal cerrada / recargar configuración
SIGINT	2	Ctrl+C
SIGQUIT	3	Ctrl+\ (abandona y genera core)
SIGTERM	15	kill por defecto
SIGKILL	9	Imposible de capturar
SIGUSR1	10	Definido por el usuario
SIGUSR2	12	Definido por el usuario
SIGSTOP	19	Imposible de capturar
SIGTSTP	20	Ctrl+Z
EXIT	0 (pseudo)	El script termina (normal o por señal)
ERR	—	Atrapa cualquier comando que falle (solo en algunos contextos)
RETURN	—	Al volver de una función o script sourceado
DEBUG	—	Antes de cada comando simple (para depuración)
Sintaxis de trap
bash

trap 'comandos' SEÑAL1 SEÑAL2 ...

    comandos se ejecutan cuando se recibe alguna de las señales.

    trap '' SEÑAL ignora la señal.

    trap - SEÑAL restaura el comportamiento por defecto.

    trap sin argumentos lista los traps activos.

Ejemplo típico: limpiar archivos temporales al salir
bash

#!/bin/bash
tempfile=$(mktemp)
trap 'rm -f "$tempfile"; echo "Limpieza hecha"' EXIT

Si el script termina normalmente o por SIGINT, se ejecuta la limpieza.
Capturar Ctrl+C pero confirmar
bash

trap 'echo "¿Seguro que quieres salir? Pulsa Ctrl+\ para forzar."' SIGINT SIGTERM

trap con funciones
bash

cleanup() {
    echo "Limpiando..."
    rm -f /tmp/mitemp
}
trap cleanup EXIT SIGINT SIGTERM

Señal ERR y depuración

trap 'echo "Error en línea $LINENO"' ERR muestra un mensaje cada vez que un comando falle (si set -e no está activo). Cuidado: con set -e, al capturar ERR el script no termina a menos que explícitamente llames a exit.
Señales definibles por usuario: SIGUSR1, SIGUSR2

Pueden usarse para comunicación simple: un script atrapa SIGUSR1 y vuelca estadísticas, por ejemplo.
bash

trap 'echo "Estado: $(date)";' SIGUSR1

Luego desde otra terminal: kill -SIGUSR1 $PID.
Limitaciones

    No se pueden capturar SIGKILL ni SIGSTOP.

    Las funciones de trap se ejecutan en el entorno global; pueden interferir si no se diseñan con cuidado.

    Si el script recibe una señal mientras ejecuta la acción de trap, puede interrumpirse a medias (no es atómico).

04-espera-y-concurrencia.md
Controlar múltiples procesos simultáneos
wait: esperar procesos hijos

wait sin argumentos espera a que todos los procesos hijos terminen y devuelve el código de salida del último.

wait $PID espera a un PID concreto y retorna su código de salida.

Ejemplo de lanzamiento paralelo y espera:
bash

#!/bin/bash
for i in 1 2 3; do
    (sleep $i; echo "Tarea $i completada") &
done
wait
echo "Todas las tareas han terminado."

Recoger resultados de procesos hijos

No se puede capturar stdout directo de hijos en bg con $() porque son asíncronos. Opciones:

    Guardar en archivos temporales y luego leerlos.

    Usar coproc para comunicación bidireccional.

    Con Bash ≥ 4.3, wait $! y luego ...& con redirección a un archivo; después leer el archivo.

Técnica con archivos temporales:
bash

for i in 1 2 3; do
    (    # subshell para tarea
        resultado=$(echo "Tarea $i: $(date)")
        echo "$resultado" > "/tmp/resultado$i"
    ) &
done
wait
for i in 1 2 3; do
    cat "/tmp/resultado$i"
    rm "/tmp/resultado$i"
done

Pool de procesos (concurrencia limitada)

Lanzar demasiados procesos a la vez puede sobrecargar el sistema. Se puede implementar un pool sencillo contando hijos activos:
bash

MAX_PROCS=4
contador=0
for item in "${items[@]}"; do
    procesar "$item" &
    ((contador++))
    if (( contador >= MAX_PROCS )); then
        wait -n   # espera al menos uno (Bash 4.3+)
        ((contador--))
    fi
done
wait   # esperar los últimos

wait -n espera el siguiente trabajo hijo que termine y devuelve su código.
Uso de xargs -P o parallel

Para tareas masivas, a veces es más sencillo:
bash

xargs -I{} -P 4 comando {} < lista.txt

O parallel de GNU:
bash

parallel -j 4 procesar ::: "${items[@]}"

Coprocesos (coproc)

Permiten comunicación bidireccional con un proceso en segundo plano sin necesidad de archivos temporales:
bash

coproc NOMBRE { comando; }
echo "entrada" >&"${NOMBRE[1]}"    # stdin del coproceso
read salida <&"${NOMBRE[0]}"       # stdout

Útil para interactuar con procesos persistentes.
Scripts de ejemplo
scripts/paralelo.sh

Un script que descarga URLs en paralelo con un pool limitado, usando arrays para almacenar los resultados.
bash

#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------
# paralelo.sh – Descarga URLs concurrentemente con un máximo de hilos
# ---------------------------------------------------------------

urls=(
    "https://www.example.com"
    "https://www.example.org"
    "https://httpbin.org/get"
    "https://httpbin.org/delay/2"
)
MAX_HILOS=2
declare -a resultados        # almacenamos mensajes

# Función que descarga y guarda en archivo temporal
descargar() {
    local url="$1"
    local tmpfile
    tmpfile=$(mktemp)
    # Intentar descargar con curl; timeout de 5 seg
    if curl -s -o "$tmpfile" --connect-timeout 3 --max-time 5 "$url"; then
        size=$(stat -c %s "$tmpfile" 2>/dev/null || echo 0)
        echo "EXITO:$url:$size:$tmpfile"
    else
        echo "FALLO:$url:0:$tmpfile"
    fi
}

# Lanzar descargas en paralelo controlado
contador=0
for url in "${urls[@]}"; do
    descargar "$url" &
    ((contador++))
    # Alcanzado el máximo, esperar a que uno termine
    if (( contador >= MAX_HILOS )); then
        wait -n
        ((contador--))
    fi
done
wait   # esperar los últimos

# Recoger resultados (los procesos escribieron en stdout)
# Pero capturamos la salida de descargar desde aquí? No directamente.
# En lugar de eso, hagamos que descargar escriba en un archivo de resultados.
# Modifiquemos: cada trabajo escribe en un fifo o mejor en un archivo con su PID.
# Vamos a rehacer con almacenamiento en array asociativo usando archivos.

# Para simplificar, aquí mostraremos cómo usar wait y archivos temporales:
declare -A resultados_asoc  # url -> "EXITO:size" o "FALLO"

# Limpiar función anterior; redefinimos descargar para que escriba en un directorio compartido
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

descargar_v2() {
    local url="$1" out="$2"
    if curl -s -o "$out" --connect-timeout 3 --max-time 5 "$url"; then
        echo "EXITO:$(stat -c %s "$out")" > "$tmpdir/$BASHPID"
    else
        echo "FALLO:0" > "$tmpdir/$BASHPID"
    fi
}

for url in "${urls[@]}"; do
    # Archivo de salida único por descarga
    outfile="$tmpdir/$(echo "$url" | md5sum | cut -d' ' -f1).dat"
    descargar_v2 "$url" "$outfile" &
    echo "$url -> $outfile" >> "$tmpdir/mapeo"   # guardamos url -> archivo
done
wait

# Leer resultados
echo "==== Resultados ===="
while read -r linea; do
    url=$(echo "$linea" | awk -F' -> ' '{print $1}')
    f=$(echo "$linea" | awk -F' -> ' '{print $2}')
    if [[ -f "$f" ]]; then
        estado=$(cat "$f")
        echo "$url: $estado"
    else
        echo "$url: resultado perdido"
    fi
done < "$tmpdir/mapeo"

scripts/demonio-simple.sh

Un script que se ejecuta como demonio, atrapa señales y ejecuta tareas periódicas.
bash

#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------
# demonio-simple.sh – Script residente que ejecuta tareas periódicas
# ---------------------------------------------------------------

PIDFILE="./demonio.pid"
LOGFILE="./demonio.log"
INTERVALO=5    # segundos entre ejecuciones de la tarea

# Función de limpieza al salir
cleanup() {
    echo "$(date) - Recibida señal, finalizando demonio..." >> "$LOGFILE"
    rm -f "$PIDFILE"
    exit 0
}

# Atrapar señales
trap cleanup SIGINT SIGTERM EXIT
trap 'echo "$(date) - SIGHUP recibido, ignorando..." >> "$LOGFILE"' SIGHUP
trap 'echo "$(date) - SIGUSR1: estado $(date)" >> "$LOGFILE"' SIGUSR1

# Asegurar que solo una instancia corre
if [[ -f "$PIDFILE" ]]; then
    oldpid=$(cat "$PIDFILE")
    if kill -0 "$oldpid" 2>/dev/null; then
        echo "El demonio ya está corriendo (PID $oldpid)." >&2
        exit 1
    else
        echo "Eliminando PID huérfano." >&2
        rm -f "$PIDFILE"
    fi
fi

# Guardar el PID actual
echo "$$" > "$PIDFILE"
echo "Demonio iniciado con PID $$." | tee -a "$LOGFILE"
echo "Envía SIGUSR1 (kill -SIGUSR1 $$) para estado, SIGINT para terminar." | tee -a "$LOGFILE"

# Bucle principal
while true; do
    # --- Tarea del demonio ---
    echo "$(date) - Realizando tarea programada..." >> "$LOGFILE"
    # Ejemplo: comprobar espacio en disco
    df -h / | tail -1 >> "$LOGFILE"
    # -------------------------

    sleep "$INTERVALO"
done

Instrucciones para probar:
bash

chmod +x demonio-simple.sh
./demonio-simple.sh &        # lanzar en bg o en otra terminal
# En otra terminal:
kill -SIGUSR1 $(cat demonio.pid)   # ver estado
kill $(cat demonio.pid)            # terminar (SIGTERM)

01-regex-en-bash.md
Expresiones regulares dentro de Bash: [[ =~ ]]

Bash incorpora soporte nativo de expresiones regulares (regex) mediante el operador =~ dentro de la construcción [[ ]]. Esto permite hacer comprobaciones complejas de cadenas sin necesidad de invocar grep o sed.
Sintaxis básica
bash

if [[ "$cadena" =~ expresión_regular ]]; then
    echo "Coincidencia"
fi

La expresión regular va sin comillas (o al menos los metacaracteres deben estar sin entrecomillar). Si se usan comillas, Bash los trata como literales. Para usar una variable que contiene la regex, no se debe entrecomillar:
bash

patron="^[0-9]+$"
if [[ "$num" =~ $patron ]]; then ...

¡Correcto! En ese caso $patron se expande sin comillas y Bash interpreta su contenido como regex.
El array BASH_REMATCH

Después de una coincidencia exitosa, Bash almacena la parte que coincidió completamente en ${BASH_REMATCH[0]} y los grupos capturados (entre paréntesis) en ${BASH_REMATCH[1]}, ${BASH_REMATCH[2]}, etc.
bash

if [[ "Nombre: Juan" =~ Nombre:[[:space:]]+([a-zA-Z]+) ]]; then
    echo "Nombre encontrado: ${BASH_REMATCH[1]}"
fi

Metacaracteres y sintaxis (ERE)

Bash utiliza Expresiones Regulares Extendidas (ERE), similares a grep -E. Estos son los elementos principales:

    Anclas: ^ (inicio de cadena), $ (fin de cadena).

    Cuasificadores: * (cero o más), + (uno o más), ? (cero o uno).

    Cuantificador de rango: {n}, {n,m}, {n,}. Ojo: en algunas versiones antiguas de Bash hay que escapar las llaves \{3\}; desde Bash 3.2+ con expresión sin comillas funciona sin escapar.

    Clases de caracteres POSIX: [[:alnum:]], [[:alpha:]], [[:digit:]], [[:lower:]], [[:upper:]], [[:space:]], etc. Dentro de [] tradicionales también se pueden usar.

    Grupos y alternación: ( ) para agrupar y capturar, | para alternación.

    Punto: . coincide con cualquier carácter salvo nueva línea.

    Listas negadas: [^abc] cualquier carácter que no sea a,b,c.

    Secuencias de escape: \t (tabulador), \n (nueva línea) — ten en cuenta que en $'...' se interpretan, pero en la regex suelen funcionar.

Ejemplo de regex para una hora HH:MM:
bash

patron_hora='^([01][0-9]|2[0-3]):[0-5][0-9]$'
if [[ "$hora" =~ $patron_hora ]]; then
    echo "Formato de hora válido"
fi

Consideraciones importantes

    Sin comillas en la regex: si quieres que ^, $, * etc. se interpreten como metacaracteres, no encierres la expresión en comillas dentro del [[ ]]. Pero si toda la regex está en una variable y la expandes sin comillas ($var), funciona.

    Locales y clases: Los rangos como [a-z] dependen del locale (LC_COLLATE). Para mayor consistencia usa clases [[:lower:]].

    Escapando espacios: Los espacios en la regex deben tal cual; si la regex se guarda en variable, hay que protegerla con comillas al definirla pero no al usarla en =~.

    Compatibilidad: [[ ]] y =~ existen en Bash, ksh y zsh (con algunos matices). Si buscas máxima portabilidad POSIX, usa grep.

    Detección del fin de línea: El metacarácter $ coincide con el final de la cadena sin salto de línea. Si la variable tiene un salto de línea al final (común al leer archivos sin -r), puede fallar. Usa printf en vez de echo para evitar añadidos.

Ejemplo práctico: validar email sencillo
bash

is_valid_email() {
    local email="$1"
    local patron='^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    [[ "$email" =~ $patron ]]
}

Errores comunes

    Intentar usar =~ en [ ]; solo funciona en [[ ]].

    Escapar incorrectamente: [\w] no es válido; usa [[:word:]] en algunos Perl-like no, resort a [A-Za-z0-9_].

    Olvidar que * en regex no es igual que en glob: .* es cualquier cadena; * ya es cuantificador, necesita un prefijo.

02-extglob.md
Patrones extendidos: el poder del globbing avanzado

El extended globbing (extglob) es una extensión de Bash (activada con shopt -s extglob) que añade cuantificadores y alternación a los patrones de nombres de archivo. No son expresiones regulares; se rigen por las reglas del globbing (coincidencia sobre nombres de archivo existentes, salvo en contextos de case y [[ == ]]).
Habilitar
bash

shopt -s extglob   # activar
shopt -u extglob   # desactivar

Patrones disponibles
Patrón	Equivalente lógico	Descripción
?(pat)	pat es opcional	Cero o una ocurrencia de pat.
*(pat)	pat repetido	Cero o más ocurrencias.
+(pat)	pat al menos una vez	Una o más ocurrencias.
@(pat1|pat2|...)	uno de los patrones	Coincide con exactamente uno de la lista (OR).
!(pat)	cualquier cosa excepto pat	Todo lo que no coincida (puede ser una lista: !(pat1|pat2)).

Los patrones pueden contener los comodines clásicos (*, ?, [...]).
Uso en case

El case ya usa patrones glob, así que extglob se integra naturalmente:
bash

shopt -s extglob
case $archivo in
    +(*.txt|*.log))
        echo "Es un montón de texto/logs" ;;
    !(*.bak|*.tmp))
        echo "No es backup ni temporal" ;;
esac

Aquí +(*.txt|*.log) significa "uno o más bloques de *.txt o *.log", útil para cadenas como "nota.txt.log.txt" (aunque con nombres de archivo es raro). Realmente en case se usa más a nivel de cadena: @(si|yes) para opciones.
Uso en [[ == ]]

Cuando usas == o != dentro de [[ ]] y la parte derecha no está entrecomillada, Bash la interpreta como un patrón glob (con extglob si está activo). Esto permite coincidencias de subcadenas sin regex:
bash

shopt -s extglob
if [[ "$respuesta" == @(sí|yes|SI|YES) ]]; then
    echo "Aceptaste"
fi

También se pueden hacer comprobaciones como [[ $var == +([[:digit:]]) ]] para ver si contiene solo dígitos y es no vacío (una o más ocurrencias).
Uso en expansiones de parámetros

Las expansiones ${var#patron}, ${var%patron}, etc., también respetan extglob si está activo. Ejemplo:
bash

shopt -s extglob
ruta="/home/user/docs/reporte.txt"
echo "${ruta##!(/)+(\/)}"     # reporte.txt (quita todo hasta el último /)

Explicación: !(/)+(\/) coincide con "cualquier secuencia que no sea barra, seguida de una o más barras", es decir, todo hasta la última barra inclusive. Truco avanzado.
Uso como parte de comandos (generación de archivos)

Con extglob, al generar nombres de archivo puedes hacer cosas como:
bash

ls -d !(backup|tmp)   # lista todos los archivos/dirs excepto 'backup' y 'tmp'

Cuidado: !(...) con una lista larga puede fallar con Argument list too long. Usa find en esos casos.
Comparación con regex

    Extglob no tiene anclas implícitas; un patrón +(a)c coincide con "aaac" pero también con "Xabc" porque puede aparecer en cualquier parte de la cadena (en [[ == ]] es igual que glob: implícitamente anclado al inicio y fin si la variable completa, no? En [[ $var == +(a)c ]] el patrón debe coincidir con la cadena completa, no parcialmente. En globbing de archivos, la coincidencia es sobre el nombre completo. En case, el patrón debe coincidir con todo el valor. Así que sí, está anclado). Para coincidencias parciales habría que usar *...*.

    Extglob no tiene cuantificadores numéricos rígidos {3}, ni grupos de captura, ni aserciones. Para eso se usa regex.

03-grep-sed-awk-basico.md
Herramientas externas esenciales para scripts

Aunque Bash ofrece potentes capacidades de manipulación de cadenas, hay situaciones donde grep, sed y awk brillan, especialmente cuando se trabaja con archivos grandes, tuberías complejas o cuando necesitas portabilidad fuera de Bash puro.
grep

Busca líneas que coinciden con un patrón. Soporta varios sabores de regex.
Opción	Significado
-E	Expresiones Regulares Extendidas (ERE, como en Bash).
-P	Expresiones Regulares Perl (PCRE), más potentes (si disponible).
-i	Ignorar mayúsculas/minúsculas.
-v	Invertir selección (líneas que no coinciden).
-c	Contar líneas coincidentes.
-n	Mostrar número de línea.
-o	Mostrar solo la parte de la línea que coincide.
-q	Silencioso; solo interesa el código de salida.
-R / -r	Búsqueda recursiva en directorios.
--color=auto	Resaltar coincidencias.

Ejemplos en scripts:
bash

# Verificar si una palabra está en un diccionario
if grep -iq "^$palabra$" /usr/share/dict/words; then
    echo "Palabra válida"
fi

# Extraer todas las direcciones IP de un registro
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' log.txt | sort -u

sed

Editor de flujo (stream editor). Lee línea por línea y aplica comandos de sustitución, borrado, inserción, etc.

Sustitución: s/patrón/remplazo/opciones

    g: reemplazar todas las ocurrencias en la línea.

    i: ignorar mayúsculas (solo GNU sed con I).

    p: imprimir si hubo sustitución (con -n).

    -n suprime la salida automática; solo imprime cuando se pide (p).

    -i edita el archivo en el lugar (haz copia antes con -i.bak).

    Se pueden usar diferentes delimitadores: s#ruta/antigua#ruta/nueva#.

Ejemplos:
bash

# Reemplazar la primera coma por tabulador
sed 's/,/\t/' archivo.csv

# Reemplazar todas las 'a' por 'A'
sed 's/a/A/g'

# Borrar líneas que empiezan con #
sed '/^#/d'

# Imprimir solo entre líneas que contienen START y END
sed -n '/START/,/END/p'

# Usar grupos capturados
echo "Nombre: Juan" | sed 's/^Nombre: \([a-zA-Z]*\)/\1/'

awk

Lenguaje de procesamiento de patrones y campos. Cada línea se divide en campos según FS (por defecto espacios/tab), accesibles como $1, $2, ..., $NF (último), $0 (línea completa).

Estructura típica: awk 'patrón { acción }' archivo

    Patrón puede ser una expresión regular, condición numérica, o BEGIN/END.

    Acción entre llaves con código estilo C.

Variables internas:

    FS: field separator (entrada)

    OFS: output field separator

    RS: record separator (por defecto nueva línea)

    NR: número de registro (línea) actual

    NF: número de campos en el registro actual

Ejemplos:
bash

# Sumar una columna (2da columna)
awk '{sum += $2} END {print sum}' datos.txt

# Filtrar líneas cuyo primer campo > 10 e imprimir con otro formato
awk '$1 > 10 { printf "%-10s %5d\n", $3, $1 }' archivo.txt

# Imprimir solo la primera y última columna
awk '{print $1, $NF}'

# Calcular promedio de la 3ra columna
awk '{ total += $3; count++ } END { if(count>0) print total/count }' numeros.tsv

awk va más allá: puede hacer contadores, arrays asociativos, e incluso escribir programas completos. En scripts de Bash se usa para tareas de formato rápido o para procesar datos tabulares.
¿Cuándo usar cada uno?

    grep cuando solo necesitas encontrar o filtrar líneas.

    sed para sustituciones simples o transformaciones línea a línea.

    awk cuando necesitas lógica sobre campos, cálculos o informes.

    Las capacidades nativas de Bash (expansiones de parámetros, [[ =~ ]]) cubren la mayoría de manipulaciones de cadenas simples sin lanzar subshells.

Buenas prácticas: no abuses de las herramientas externas por una operación que Bash puede hacer con parameter expansion; el rendimiento importa.
Script de ejemplo
scripts/validador-email.sh

Script que valida direcciones de correo electrónico usando regex de Bash y permite comprobar un archivo de correos además de argumentos.
bash

#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------
# validador-email.sh - Verifica si uno o más correos son válidos
# ---------------------------------------------------------------

# Patrón de email pragmático (no RFC completo, pero suficiente)
# Caracteres permitidos: letras, dígitos, . _ % + -
# Dominio: letras, dígitos, guiones y puntos
# TLD: mínimo 2 letras
readonly EMAIL_REGEX='^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

# Función que imprime en color si es válido o no
print_result() {
    local email="$1"
    if is_valid "$email"; then
        echo -e "\e[32m✓\e[0m $email"
    else
        echo -e "\e[31m✗\e[0m $email"
    fi
}

# Comprueba un email con la regex
is_valid() {
    [[ "$1" =~ $EMAIL_REGEX ]]
}

# Procesar un archivo línea por línea (una dirección por línea)
check_file() {
    local file="$1"
    [[ -f "$file" ]] || { echo "Error: archivo '$file' no existe." >&2; exit 1; }
    while IFS= read -r email; do
        # Ignorar líneas vacías o comentarios
        [[ -z "$email" || "$email" == \#* ]] && continue
        print_result "$email"
    done < "$file"
}

# Mostrar ayuda
help() {
    cat <<EOF
Uso: $0 [opciones] [correo1 correo2 ...]

Sin argumentos, lee de stdin.
Opciones:
  -f ARCHIVO    Leer correos del archivo especificado (uno por línea)
  -h            Mostrar esta ayuda

Ejemplos:
  $0 juan@example.com
  $0 test@correo,com otro@dominio.org
  cat lista.txt | $0
  $0 -f correos.txt
EOF
}

# Parseo de opciones simples
archivo=""
while getopts "hf:" opt; do
    case $opt in
        h) help; exit 0 ;;
        f) archivo="$OPTARG" ;;
        *) help >&2; exit 1 ;;
    esac
done
shift $((OPTIND-1))

# Ejecutar según origen
if [[ -n "$archivo" ]]; then
    check_file "$archivo"
elif [[ $# -gt 0 ]]; then
    for addr in "$@"; do
        print_result "$addr"
    done
else
    # Leer de stdin
    while IFS= read -r line; do
        [[ -z "$line" || "$line" == \#* ]] && continue
        print_result "$line"
    done
fi

Ejemplo de uso:
bash

$ ./validador-email.sh user@example.com otro@@invalido
✓ user@example.com
✗ otro@@invalido
$ echo "admin@site.co" | ./validador-email.sh
✓ admin@site.co

El script demuestra [[ =~ ]], manejo de argumentos, lectura de archivos y stdin, y buenas prácticas de programación en Bash.

01-opciones-de-depuracion-set.md
Opciones de depuración y cómo activarlas

Bash ofrece varias opciones que se pueden activar con set o desde la línea de comandos para facilitar la depuración. Las más importantes son:
Opción	set -	Efecto
xtrace	set -x	Muestra cada orden simple expandida en stderr, precedida por PS4.
verbose	set -v	Muestra cada línea del script tal cual se lee, antes de ser ejecutada.
nounset	set -u	Trata las variables no definidas como error y termina el script.
errexit	set -e	Termina inmediatamente si un comando retorna un estado distinto de 0 (con algunas excepciones).
pipefail	set -o pipefail	El código de salida de una tubería es el del último comando que falló (o 0 si todos exitosos).
functrace	set -T	Se heredan las trampas DEBUG y RETURN a funciones llamadas (útil para depurar).
errtrace	set -E	Las trampas ERR también se activan en funciones y subshells.
Modo xtrace (-x)

Activar set -x provoca que antes de cada orden (después de las expansiones), se imprima la línea precedida por PS4. El valor por defecto de PS4 es + .
bash

#!/bin/bash -x
# o
set -x
echo "Hola mundo"
set +x    # desactivar

Para personalizar la traza, define PS4 con información como número de línea y nombre de función:
bash

PS4='+ (${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
set -x

Esto mostrará algo como + (script.sh:5): main(): echo "Hola".
Modo verbose (-v)

Imprime la línea leída del script justo antes de ser interpretada (sin expandir). Útil para detectar problemas de expansiones inesperadas.
Modo nounset (-u)

Con set -u, cualquier intento de expandir una variable no definida causará un error y la finalización del script. Para proporcionar valores por defecto se usan expansiones como ${var:-default}.
Modo errexit (-e)

set -e hace que el script aborte si un comando devuelve un código distinto de 0. Excepciones: no se aplica en:

    Comandos que son parte de if, while, until.

    Comandos en tuberías (salvo con pipefail).

    Comandos que se ejecutan con || o &&.

Es habitual combinarlo con pipefail para que las tuberías sean seguras:
bash

set -eo pipefail

Combinación recomendada
bash

set -euo pipefail

    -e: para errores de comando.

    -u: para variables sin definir.

    -o pipefail: para que los fallos en tuberías no pasen desapercibidos.

Para depuración se añade -x temporalmente.
trap para depuración (adelanto)

Se puede usar trap 'comandos' DEBUG para ejecutar código antes de cada comando simple. Por ejemplo, mostrar la pila de llamadas:
bash

trap 'echo "[DEBUG] ${BASH_SOURCE[0]}:$LINENO ${FUNCNAME[0]}: $BASH_COMMAND"' DEBUG

02-trampas-de-depuracion.md
Usar trap para introspección en tiempo de ejecución

Además de las opciones anteriores, las trampas ofrecen una fina granularidad para depurar.
trap ... ERR

Se activa cuando cualquier comando falla (siempre que el error no sea enmascarado por una estructura condicional). Muy útil para mostrar la línea exacta del fallo:
bash

trap 'echo "Error en la línea $LINENO"; exit 1' ERR

Si usas set -e, la combinación con ERR puede ser poderosa para volcar el estado en el momento del error.
trap ... DEBUG

Se ejecuta antes de cada comando simple. La variable BASH_COMMAND contiene el comando que se va a ejecutar.
bash

trap 'echo "Ejecutando: $BASH_COMMAND"' DEBUG

Normalmente se usa con funciones como:
bash

debug_trap() {
    echo "DEBUG: ${BASH_SOURCE[1]}:${BASH_LINENO[0]} ${FUNCNAME[1]} -> $BASH_COMMAND"
}
trap debug_trap DEBUG

Ojo: el trap DEBUG se hereda a las funciones si se activa functrace (set -T).
trap ... RETURN

Se activa al volver de una función o de un script sourceado. Muestra la traza al salir.
bash

trap 'echo "Saliendo de ${FUNCNAME[0]} con código $?"' RETURN

Ejemplo de trampa de volcado de pila
bash

_stacktrace() {
    local i
    echo "=== Stacktrace ==="
    for (( i=0; i<${#FUNCNAME[@]}; i++ )); do
        echo "  #$i ${FUNCNAME[$i]} (${BASH_SOURCE[$i]}:${BASH_LINENO[$i-1]})"
    done
}
trap _stacktrace ERR

Si ocurre un error, se imprime la pila de llamadas completa hasta la función main.
Limpieza al salir

EXIT (pseudo-señal) se dispara al terminar el script, incluso si es por error o señal (aunque no por SIGKILL). Usa trap ... EXIT para limpiar temporales.
bash

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

Combinar con ERR no es redundante: EXIT siempre se ejecuta; ERR permite reaccionar a errores específicos.
03-shellcheck.md
ShellCheck: tu revisor de scripts

ShellCheck es una herramienta de análisis estático para shell scripts que detecta errores comunes, malas prácticas y advertencias de portabilidad.
Instalación

    Ubuntu/Debian: apt install shellcheck

    macOS: brew install shellcheck

    Online: pega el código en shellcheck.net

    Integraciones: plugins para VSCode, Vim, Sublime, etc.

Uso básico
bash

shellcheck mi_script.sh

ShellCheck dará avisos categorizados: Error (con código SC), Warning, Info, Style.
Códigos de aviso más comunes
Código	Descripción	Ejemplo
SC2086	Variables sin comillas	rm $file → rm "$file"
SC2164	cd sin comprobar error	cd dir && ... o cd dir || exit
SC2206	Citar arrays	arr=($var) → read -ra arr <<< "$var"
SC2046	Word splitting en sustitución de comandos	for f in $(ls) → usa globbing
SC2068	Elementos de array sin comillas	${array[@]} → "${array[@]}"
SC2155	Declarar y asignar locales en la misma línea	local var=$(cmd) → local var; var=$(cmd)
SC2120	Variable no asignada en función	Revisa parámetros
SC2015	Uso de A && B || C como if/else	No es equivalente, usar if
SC1090	Archivo sourceado no encontrado	Ruta no fija; usar verificación
SC1117	Escape de barra invertida innecesaria	\d no es un dígito, mejor [0-9]

Nota: Puedes desactivar avisos con comentarios especiales: # shellcheck disable=SC2086.
Ejemplo de corrección con ShellCheck
bash

# original (con problemas)
cat $archivo | while read line; do echo $line; done

# ShellCheck sugiere:
# SC2002: Useless cat. Consider 'cmd < file | ..' or 'cmd file | ..' instead.
# SC2086: Double quote to prevent globbing and word splitting.
# SC2162: read without -r will mangle backslashes.

# corregido
while IFS= read -r line; do
    echo "$line"
done < "$archivo"

Integrar en CI

Para asegurar la calidad de los scripts en un repositorio:
bash

shellcheck *.sh && echo "OK"

ShellCheck permite especificar la severidad mínima (-S error) y excluir checks (-e SC1090).
04-estilo-y-convenciones.md
Escribir Bash que otros (y tú en 6 meses) entiendan

Un estilo consistente mejora la legibilidad y reduce errores. Aquí algunas convenciones recomendadas:
Nombres

    Variables locales y globales no exportadas: snake_case, en minúsculas. Ej: contador, nombre_archivo.

    Constantes y variables de entorno: UPPER_CASE. Ej: readonly MAX_INTENTOS=5.

    Nombres de funciones: snake_case o camelCase, pero consistente. Prefiere verbos: calcular_total, enviar_correo.

    Evitar palabras reservadas: readonly está bien, local también.

Indentación

    Usa 4 espacios (o tabuladores, pero sé consistente).

    Las estructuras if, for, while alinean sus palabras clave:

bash

if [[ ... ]]; then
    comandos
fi

    Las funciones comienzan en la columna 0; el cuerpo indentado.

bash

mi_funcion() {
    local variable
    comandos
}

Comillas

    Siempre entrecomilla las expansiones de variables a menos que tengas una razón específica para no hacerlo (word splitting deseado).

    Usa "$var" no $var.

    Dentro de [[ ]], las variables pueden ir sin comillas, pero es más seguro comillarlas.

Uso de [[ ]] sobre [ ]

Dentro de scripts de Bash (no POSIX), prefiere [[ ]]:

    Más seguro: no hace word splitting ni pathname expansion.

    Soporta =~, &&, ||.

    Sintaxis más natural.

No uses [ ] a menos que necesites compatibilidad con /bin/sh.
Comprobaciones y retorno temprano

    Valida argumentos y condiciones al inicio y retorna o sale con error.

    Patrón guard clause:

bash

if (( $# < 2 )); then
    echo "Uso: ..."
    exit 1
fi

Uso de printf sobre echo

    printf es más portátil y predecible.

    echo puede interpretar escapes y tener comportamientos distintos según la shell.

    Usa printf "%s\n" "$mensaje".

Comentarios

    Cada script debe tener un encabezado con propósito y uso.

    Las funciones complejas deben describir parámetros y retorno.

    No comentes lo obvio; explica por qué, no qué.

Funciones: main y modularización

Encapsula la lógica principal en una función main y al final del script llámala:
bash

#!/bin/bash
set -euo pipefail

main() {
    # lógica
}

main "$@"

Esto permite sourciar el script sin ejecutarlo y facilita las pruebas.
Evitar eval

eval puede ser peligroso. Usa arrays para construir comandos con opciones dinámicas.
Variables de entorno y readonly
bash

readonly CONFIG_FILE="${XDG_CONFIG_HOME:-$HOME/.config}/mi_app.conf"

Crear subsecciones con comentarios

Usa separadores visuales:
bash

# -------------------------------------------------------------------
# Configuración
# -------------------------------------------------------------------

05-scripts-robustos.md
El checklist para un script a prueba de balas

Un script robusto debe contemplar gestión de errores, limpieza, argumentos y un comportamiento predecible.
1. Encabezado robusto
bash

#!/usr/bin/env bash
# script.sh - Descripción corta
# Uso: script.sh [opciones] arg1
set -euo pipefail
# Opcional: activar más banderas
shopt -s nullglob    # globs que no coinciden se expanden a nada
shopt -s extglob      # si se necesitan patrones extendidos

2. Función main y llamada
bash

main() {
    # lógica
}
main "$@"

3. Parseo de opciones con getopts
bash

usage() {
    cat <<EOF
Uso: $0 [-v] [-o archivo] entrada
...
EOF
}

verbose=0
output="salida.txt"
while getopts "hvo:" opt; do
    case "$opt" in
        h) usage; exit 0 ;;
        v) verbose=1 ;;
        o) output="$OPTARG" ;;
        *) usage >&2; exit 1 ;;
    esac
done
shift $((OPTIND-1))

if (( $# == 0 )); then
    usage >&2
    exit 1
fi
input="$1"

4. Logging con niveles
bash

log_info()  { echo "[INFO] $(date '+%F %T') $*"; }
log_warn()  { echo "[WARN] $(date '+%F %T') $*" >&2; }
log_error() { echo "[ERROR] $(date '+%F %T') $*" >&2; }

5. Manejo de archivos temporales con mktemp
bash

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

Si creas un archivo temporal para guardar resultados, configura la trampa.
6. Dependencias

Comprobar comandos necesarios al inicio:
bash

deps=( curl jq )
for cmd in "${deps[@]}"; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        log_error "Falta el comando: $cmd"
        exit 1
    fi
done

7. Variables con valores por defecto y validadas
bash

readonly MAX_RETRIES="${MAX_RETRIES:-3}"
if (( MAX_RETRIES < 1 )); then
    log_error "MAX_RETRIES debe ser positivo"
    exit 1
fi

8. Operaciones con archivos seguras

    Antes de sobrescribir, comprueba con -f y pregunta o usa -i.

    Usa -- para separar opciones de argumentos: rm -- "$archivo".

    Al crear archivos, establece permisos restrictivos (umask 077 o chmod).

9. Internacionalización y rutas

    Usa $HOME y $XDG_*, no rutas fijas.

    No asumas que /tmp es el único lugar para temporales, pero mktemp se encarga.

10. Salir correctamente

    exit 0 para éxito, otros valores según el tipo de error.

    La trampa EXIT ejecutará la limpieza.

11. Idempotencia

Si el script crea algo, verifica si ya existe antes de fallar o sobrescribir.
12. Evitar fugas de información sensible

    No pongas contraseñas en argumentos visibles con ps. Usa variables de entorno o archivos de configuración con permisos restringidos.

    Siempre redirige a /dev/null o logs la salida que pueda contener secretos.

Script de ejemplo
scripts/plantilla-robusta.sh
bash

#!/usr/bin/env bash
# -------------------------------------------------------------------
# plantilla-robusta.sh – Plantilla para scripts Bash robustos
# Incorpora: parseo de opciones, logging, trampas, validación y limpieza.
# -------------------------------------------------------------------
set -euo pipefail
IFS=$'\n\t'

# --- Configuración ---
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Variables globales (seteadas por opciones) ---
VERBOSE=0
OUTPUT_FILE=""
INPUT_FILE=""

# --- Logging ---
log_info()  { echo "[INFO]  $(date '+%F %T') $*"; }
log_warn()  { echo "[WARN]  $(date '+%F %T') $*" >&2; }
log_error() { echo "[ERROR] $(date '+%F %T') $*" >&2; }

# --- Uso ---
usage() {
    cat <<EOF
Uso: $SCRIPT_NAME [opciones] <archivo>

Opciones:
  -o ARCHIVO   Ruta del archivo de salida (por defecto: stdout)
  -v           Modo detallado
  -h           Muestra esta ayuda

Descripción del script (reemplazar).
EOF
}

# --- Función de limpieza ---
cleanup() {
    local exit_code=$?
    # Eliminar archivos temporales si existen
    if [[ -n "${tmp_file:-}" && -f "$tmp_file" ]]; then
        rm -f "$tmp_file"
    fi
    if (( exit_code != 0 )); then
        log_error "Script finalizó con error (código $exit_code)."
    fi
    exit $exit_code
}
trap cleanup EXIT INT TERM
# Opcional: si quieres depuración de errores, añade:
# trap 'log_error "Comando fallido: $BASH_COMMAND"' ERR

# --- Comprobaciones de dependencias ---
check_deps() {
    local deps=( curl jq )   # ajusta según necesidades
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            log_error "Dependencia faltante: '$dep'. Instálala para continuar."
            exit 1
        fi
    done
}

# --- Función principal ---
main() {
    # Parsear opciones
    while getopts "hvo:" opt; do
        case "$opt" in
            h) usage; exit 0 ;;
            v) VERBOSE=1 ;;
            o) OUTPUT_FILE="$OPTARG" ;;
            *) usage >&2; exit 1 ;;
        esac
    done
    shift $((OPTIND-1))

    # Validar argumento obligatorio
    if (( $# == 0 )); then
        log_error "Se requiere un archivo de entrada."
        usage >&2
        exit 1
    fi
    INPUT_FILE="$1"

    # Verificar dependencias
    check_deps

    # Verificar que el archivo de entrada existe
    if [[ ! -f "$INPUT_FILE" ]]; then
        log_error "El archivo '$INPUT_FILE' no existe o no es regular."
        exit 1
    fi

    # Crear archivo temporal si es necesario
    tmp_file=$(mktemp) || exit 1

    # --- Lógica del script (ejemplo) ---
    log_info "Procesando '$INPUT_FILE'..."

    # Simulación de procesamiento
    if (( VERBOSE )); then
        log_info "Modo detallado activado."
    fi

    # Leer entrada y escribir salida
    while IFS= read -r line; do
        # Procesar cada línea...
        echo "$line" >> "$tmp_file"
    done < "$INPUT_FILE"

    # Resultado final
    if [[ -n "$OUTPUT_FILE" ]]; then
        cp "$tmp_file" "$OUTPUT_FILE"
        log_info "Salida guardada en '$OUTPUT_FILE'."
    else
        cat "$tmp_file"
    fi

    log_info "Procesamiento completado exitosamente."
}

# Llamada a main con los argumentos
main "$@"

Explicación de las características incluidas:

    IFS=$'\n\t' optimiza el word splitting.

    BASH_SOURCE[0] y dirname resuelven la ruta del script.

    readonly para constantes.

    cleanup registrada con EXIT, INT, TERM asegura limpieza incluso en cancelación.

    check_deps verifica que las herramientas necesarias estén en el PATH.

    Parseo con getopts, modo -v y opción -o.

    Uso de variable tmp_file creado con mktemp, se limpia en la trampa.

    Salida flexible (archivo o stdout).

    Uso de [[ ]], comillas consistentes, printf no se necesita tanto aquí porque echo es simple, pero se podría mejorar.

Esta plantilla puede ser el esqueleto de cualquier script serio.

Vamos a profundizar en los temas avanzados de la carpeta 09-avanzado/, donde Bash deja de ser un simple pegamento de comandos y se convierte en una herramienta de integración y desarrollo profesional.
01-getopts-y-argumentos.md
Parseo de opciones de línea de comandos

Un script serio debe aceptar opciones y argumentos de forma estándar. Bash ofrece dos mecanismos: el builtin getopts (para opciones cortas) y la utilidad externa getopt (que también soporta opciones largas y permite reordenar argumentos).
getopts

getopts es un builtin de Bash y cumple POSIX. Procesa las opciones una a una, actualizando las variables OPTARG (argumento de la opción, si procede), OPTIND (índice del siguiente argumento a procesar) y la variable que elijas para el flag.

Sintaxis básica:
bash

while getopts ":ho:v" opt; do
    case "$opt" in
        h) uso; exit 0 ;;
        o) output="$OPTARG" ;;
        v) verbose=1 ;;
        \?) echo "Opción inválida: -$OPTARG" >&2; exit 1 ;;
        :) echo "Opción -$OPTARG requiere un argumento." >&2; exit 1 ;;
    esac
done
shift $((OPTIND - 1))

    La cadena de opciones (ej: :ho:v) indica las letras válidas. Si una letra va seguida de : significa que espera un argumento.

    Si la cadena comienza con :, getopts funciona en modo silencioso (no imprime errores automáticamente); se debe manejar el caso \? y : manualmente. Así damos mensajes personalizados.

    $OPTARG contiene el argumento para la opción actual.

    $OPTIND es el índice (basado en 1) desde donde empiezan los argumentos no procesados; después del bucle, shift los deja disponibles como $1, $2…

Ejemplo: script que acepta -f archivo, -v (verbose) y -- para separar.
bash

while getopts "f:v-:" opt; do
    case "$opt" in
        f) file="$OPTARG" ;;
        v) verbose=1 ;;
        -) case "$OPTARG" in
               help) usage; exit 0 ;;
               *) echo "Opción larga no soportada: --$OPTARG" >&2; exit 1 ;;
           esac ;;
        ?) usage >&2; exit 1 ;;
    esac
done

Truco: si se usa - como opción en la cadena (f:v-:), getopts permite leer después de -- con $OPTARG. Así podemos implementar long options de forma manual (aunque es engorroso).
getopt (utilidad externa)

getopt (del paquete util-linux) soporta opciones largas (--verbose, --output=file), reordenamiento de argumentos y detección de errores. Su salida debe reasignarse a los argumentos posicionales con eval o con set --.

Ejemplo:
bash

OPTS=$(getopt -o ho:v --long help,output:,verbose -n "$0" -- "$@")
if [[ $? -ne 0 ]]; then
    echo "Error en opciones." >&2
    exit 1
fi
eval set -- "$OPTS"

while true; do
    case "$1" in
        -h|--help) usage; exit 0 ;;
        -o|--output) output="$2"; shift 2 ;;
        -v|--verbose) verbose=1; shift ;;
        --) shift; break ;;
        *) echo "Error interno"; exit 1 ;;
    esac
done

El eval set -- "$OPTS" es necesario porque getopt genera una cadena con los parámetros ya procesados. Es seguro si getopt es moderno y usamos --. La opción -n define el nombre para los mensajes de error.

Ventajas: admite opciones largas, agrupación de cortas (-vo archivo), y separación con --. Desventaja: dependencia externa (aunque util-linux es ubicuo en Linux).
Mejores prácticas para el parseo

    Proporciona siempre -h o --help.

    Usa -- para marcar fin de opciones y evitar conflictos con argumentos que empiezan con -.

    Valida argumentos obligatorios después del shift.

    Construye una función usage y muéstrala en caso de error.

    Si el script tiene muchas opciones, considera usar getopt o una librería de parseo.

Constantes y valores por defecto
bash

readonly VERSION="1.2.3"
OUTPUT_DIR="${OUTPUT_DIR:-./output}"   # valor por defecto desde entorno o fijo

02-coprocesos-y-pipes-con-nombre.md
Comunicación interprocesos avanzada

Bash permite dos técnicas poderosas para comunicación bidireccional: coprocesos (coproc) y tuberías con nombre (FIFOs).
Coprocesos (coproc)

Un coproceso es un comando que se ejecuta en segundo plano con dos tuberías conectadas a sus stdin y stdout. El shell proporciona descriptores de archivo para leer/escribir.

Sintaxis:
bash

coproc NOMBRE { comando; }
# o simplemente
coproc { comando; }   # el array se llama COPROC por defecto

Después, $NOMBRE_PID contiene el PID del coproceso y los descriptores están en un array:

    ${NOMBRE[0]} → descriptor de lectura (salida del comando).

    ${NOMBRE[1]} → descriptor de escritura (entrada del comando).

Ejemplo: calculadora bc persistente:
bash

coproc BC { bc -l; }
echo "scale=2; 10/3" >&${BC[1]}
read -u ${BC[0]} resultado
echo "Resultado: $resultado"

Podemos incluso encapsularlo en funciones:
bash

bc_send() { echo "$1" >&${BC[1]}; }
bc_recv() { local r; read -u ${BC[0]} r; echo "$r"; }
bc_send "sqrt(2)"
resp=$(bc_recv)

Cuidados:

    El coproceso no termina automáticamente; hay que cerrar sus descriptores y posiblemente enviarle quit.

    Para cerrar entrada: exec {BC[1]}>&-. Luego se puede leer hasta EOF y hacer wait $BC_PID.

    Si el coproceso produce mucha salida, se puede bloquear al no haber quien lea; hay que leer constantemente.

Tuberías con nombre (FIFOs)

Un FIFO es un archivo especial creado con mkfifo. Un proceso escribe en él y otro lee; es bloqueante hasta que ambas puntas estén conectadas.

Creación:
bash

mkfifo /tmp/mi_pipe

Lector (se bloquea hasta que haya escritor):
bash

cat < /tmp/mi_pipe

Escritor (se bloquea hasta que haya lector):
bash

echo "Hola" > /tmp/mi_pipe

En scripts, abrimos descriptores para evitar bloqueos:
bash

mkfifo pipeio
exec 3<>pipeio   # abrir lectura/escritura, evita bloqueo
echo "datos" >&3
read -u 3 linea
exec 3>&-        # cerrar
rm pipeio

El truco <> abre el FIFO para lectura/escritura simultánea, lo que evita el bloqueo por falta de lector/escritor.

Ejemplo de comunicación entre dos scripts:

    script_a abre un FIFO y espera órdenes.

    script_b envía comandos al FIFO y puede leer respuesta de otro FIFO.

Ventaja de los FIFOs: no están ligados al shell; procesos independientes pueden comunicarse fácilmente.

Comparación con coprocesos:

    Coproceso: comunicación con un único proceso controlado por el shell, conveniente para diálogos persistentes.

    FIFO: múltiples procesos pueden escribir/leer; más flexible pero más gestión manual.

03-dialogos-interactivos.md
Interfaces de usuario en la terminal

Más allá del simple read y select, existen herramientas para crear menús, barras de progreso y diálogos: dialog y whiptail.
dialog

dialog muestra widgets gráficos de texto. La mayoría de las distribuciones lo incluyen (apt install dialog).

Widgets comunes:
Widget	Uso
--yesno	Pregunta sí/no; código de salida 0 para sí.
--msgbox	Muestra un mensaje con botón OK.
--inputbox	Solicita una línea de texto.
--passwordbox	Como inputbox pero oculta entrada.
--menu	Menú de selección simple.
--checklist	Lista con casillas de verificación.
--radiolist	Lista con botones de radio.
--gauge	Barra de progreso (lee de stdin).
--infobox	Muestra mensaje y continúa.

Ejemplo: pregunta sí/no:
bash

if dialog --title "Confirmación" --yesno "¿Continuar?" 8 40; then
    echo "Usuario dijo Sí"
else
    echo "Usuario dijo No"
fi

Ejemplo: menú:
bash

opcion=$(dialog --title "Menú principal" \
    --menu "Elige una opción:" 15 50 4 \
    1 "Instalar" \
    2 "Configurar" \
    3 "Salir" 2>&1 >/dev/tty)
echo "Seleccionaste: $opcion"

La salida del widget va a stderr; por eso redirigimos 2>&1 >/dev/tty para capturarla en variable (y mostramos por pantalla la interfaz).

Barra de progreso con --gauge:
bash

(
    for i in $(seq 1 10); do
        echo $(( i*10 ))
        sleep 0.2
    done
) | dialog --title "Instalando" --gauge "Copiando archivos..." 8 50 0

whiptail

whiptail es una alternativa ligera (basada en newt) que usa una sintaxis similar pero con algunas diferencias. Suele estar presente en sistemas Debian/Ubuntu por defecto (apt install whiptail).

Ejemplo de menú con whiptail:
bash

opcion=$(whiptail --title "Menú" --menu "Elige" 15 50 4 \
    "1" "Opción 1" "2" "Opción 2" 3>&1 1>&2 2>&3)

La redirección es diferente: whiptail escribe la salida en stderr, y comúnmente se hace 3>&1 1>&2 2>&3 para capturarla.
Combinar con Bash

    Siempre verifica si la herramienta está instalada: command -v dialog >/dev/null || { echo "Instala dialog"; exit 1; }.

    El código de salida indica: 0 (éxito), 1 (Cancelar), 255 (error o ESC).

    Para diálogos de múltiples pasos, se puede encadenar en funciones.

Uso de select vs dialog

select es bueno para menús simples y rápida implementación, pero dialog da una experiencia mucho más profesional para scripts interactivos.
04-pruebas-unitarias.md
Testing de scripts con Bats y shunit2

Probar scripts de Bash es imprescindible cuando la complejidad crece. Dos frameworks destacan: Bats y shunit2.
Bats (Bash Automated Testing System)

Bats permite escribir pruebas con una sintaxis muy legible. Se instala en /usr/local/bin/bats o mediante gestor de paquetes (aunque la versión del sistema puede ser antigua; se recomienda instalar desde su repositorio).

Estructura de un archivo .bats:
bash

#!/usr/bin/env bats

@test "comprobar suma sencilla" {
    resultado="$(( 2 + 3 ))"
    [ "$resultado" -eq 5 ]
}

@test "funcion saludar devuelve nombre" {
    source ./mis_funciones.sh
    run saludar "Luis"
    [ "$status" -eq 0 ]
    [ "$output" = "Hola, Luis" ]
}

Características:

    run ejecuta un comando y captura $status, $output, $lines (array de líneas).

    Las pruebas se agrupan en archivos; se ejecutan con bats archivo.bats.

    También se puede cargar funciones auxiliares.

    Soporte para setup() y teardown() dentro del archivo.

Ejemplo más completo:
bash

setup() {
    # Crear un directorio temporal
    TESTDIR=$(mktemp -d)
}
teardown() {
    rm -rf "$TESTDIR"
}

@test "listar archivos" {
    touch "$TESTDIR/file1.txt"
    touch "$TESTDIR/file2.txt"
    run ls "$TESTDIR"
    [ "$status" -eq 0 ]
    [ "${#lines[@]}" -eq 2 ]
}

shunit2

shunit2 es otra librería (un script .sh que se descarga) que imita JUnit. Las funciones de prueba comienzan con test.
bash

#!/bin/bash
source ./shunit2

testSuma() {
    assertEquals 5 "$(( 2 + 3 ))"
}
testCadena() {
    str="hola"
    assertContains "$str" "ol"
}
setUp() { ... }
tearDown() { ... }
. shunit2

Elección: Bats tiene una sintaxis más moderna y es muy usado en entornos de CI. shunit2 es más veterano y ligero.
Pruebas con aislamiento

    Crea directorios temporales con mktemp -d.

    Al final de cada prueba, limpia en teardown.

    Si el script depende de comandos del sistema, puede ser necesario "mockearlos" redefiniendo funciones o usando PATH modificado.

    Para probar funciones sin llamar a otros scripts, estructura tu código en bibliotecas sourceables (ver 03-funciones/librerias).

Integración continua

Ejecuta bats tests/*.bats en tu pipeline de CI; falla si alguna prueba no pasa. Acompaña con shellcheck para calidad total.
Scripts de ejemplo
scripts/instalador-ejemplo.sh

Un instalador interactivo con whiptail (si disponible) o dialog, que usa getopts para opciones no interactivas, demuestra trampas, logging y preguntas de configuración.
bash

#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# -------------------------------------------------------------------
# instalador-ejemplo.sh - Instalador interactivo con diálogos
# -------------------------------------------------------------------

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

# --- Configuración por defecto ---
INSTALL_DIR="$HOME/.miapp"
AUTO_MODE=0
VERBOSE=0

# --- Funciones de utilidad y logging ---
info()  { echo "[INFO]  $*"; }
warn()  { echo "[WARN]  $*" >&2; }
error() { echo "[ERROR] $*" >&2; }

usage() {
    cat <<EOF
Instalador de MiApp.
Uso: $SCRIPT_NAME [opciones]

Opciones:
  -d DIR    Directorio de instalación (por defecto: $INSTALL_DIR)
  -y        Modo automático (sin preguntas)
  -v        Verbose
  -h        Ayuda
EOF
}

# --- Limpieza ---
cleanup() {
    local exit_code=$?
    [[ -n "${tmpfile:-}" && -f "$tmpfile" ]] && rm -f "$tmpfile"
    if (( exit_code != 0 )); then
        error "Instalación fallida."
    fi
    exit "$exit_code"
}
trap cleanup EXIT INT TERM

# --- Parseo de opciones ---
while getopts "d:yvh" opt; do
    case "$opt" in
        d) INSTALL_DIR="$OPTARG" ;;
        y) AUTO_MODE=1 ;;
        v) VERBOSE=1 ;;
        h) usage; exit 0 ;;
        *) usage >&2; exit 1 ;;
    esac
done
shift $((OPTIND-1))

# --- Seleccionar herramienta de diálogo ---
DIALOG=""
if command -v dialog >/dev/null; then
    DIALOG="dialog"
elif command -v whiptail >/dev/null; then
    DIALOG="whiptail"
fi

# --- Funciones de interfaz ---
ask_confirm() {
    local msg="$1"
    if [[ "$AUTO_MODE" -eq 1 ]]; then
        return 0    # sí por defecto
    fi
    if [[ -n "$DIALOG" ]]; then
        "$DIALOG" --title "Confirmación" --yesno "$msg" 8 50 2>/dev/null
    else
        read -r -p "$msg [S/n]: " resp
        [[ "$resp" == "" || "$resp" == "s" || "$resp" == "S" || "$resp" == "y" || "$resp" == "Y" ]]
    fi
}

ask_directory() {
    local prompt="$1" default="$2"
    if [[ "$AUTO_MODE" -eq 1 ]]; then
        echo "$default"
        return
    fi
    if [[ -n "$DIALOG" ]]; then
        "$DIALOG" --title "Directorio" --inputbox "$prompt" 8 60 "$default" 2>&1 >/dev/tty
    else
        read -r -p "$prompt [$default]: " entrada
        echo "${entrada:-$default}"
    fi
}

simulate_progress() {
    if [[ -n "$DIALOG" ]]; then
        for p in $(seq 0 10 100); do
            echo "$p"
            sleep 0.1
        done | "$DIALOG" --gauge "Instalando..." 6 50 0
    else
        info "Instalando..."
        sleep 1
    fi
}

# --- Proceso de instalación ---
main() {
    info "Iniciando instalación de MiApp (versión 1.0)"

    # Preguntar directorio de instalación
    INSTALL_DIR=$(ask_directory "Directorio de instalación:" "$INSTALL_DIR")

    # Confirmar
    if ! ask_confirm "Instalar en $INSTALL_DIR?"; then
        warn "Instalación cancelada por el usuario."
        exit 1
    fi

    # Simular instalación
    mkdir -p "$INSTALL_DIR"
    simulate_progress

    # Crear archivo de configuración de ejemplo
    cat > "$INSTALL_DIR/config.ini" <<EOF
# Configuración de MiApp
install_date=$(date)
version=1.0
EOF
    info "Archivo de configuración creado en $INSTALL_DIR/config.ini"

    info "¡Instalación completada exitosamente!"
}

main "$@"

scripts/pipe-comunicacion.sh

Demuestra la comunicación entre dos procesos (padre e hijo) mediante una tubería con nombre (FIFO). El script padre lanza un "servidor" que calcula factoriales y el "cliente" envía números y recibe resultados.
bash

#!/usr/bin/env bash
set -euo pipefail

# -------------------------------------------------------------------
# pipe-comunicacion.sh - Comunicación vía FIFO (servidor factorial)
# -------------------------------------------------------------------

FIFO_SRV="/tmp/fifo_servidor_$$"
FIFO_CLI="/tmp/fifo_cliente_$$"

cleanup() {
    rm -f "$FIFO_SRV" "$FIFO_CLI"
    exit 0
}
trap cleanup EXIT INT TERM

mkfifo "$FIFO_SRV"
mkfifo "$FIFO_CLI"

# Función factorial
factorial() {
    local n=$1 f=1
    for ((i=2; i<=n; i++)); do f=$((f*i)); done
    echo "$f"
}

# Proceso servidor
servidor() {
    exec 3<> "$FIFO_SRV"   # lectura de peticiones
    exec 4> "$FIFO_CLI"    # escritura de respuestas

    echo "Servidor: esperando peticiones..." >&2
    while true; do
        if read -r num <&3; then
            if [[ "$num" == "quit" ]]; then
                echo "Servidor: terminando." >&2
                exec 3>&-; exec 4>&-
                break
            fi
            if [[ "$num" =~ ^[0-9]+$ ]]; then
                resultado=$(factorial "$num")
                echo "$resultado" >&4
                echo "Servidor: factorial($num) = $resultado" >&2
            else
                echo "ERROR" >&4
            fi
        else
            # EOF en pipe (cliente cerró)
            break
        fi
    done
}

# Proceso cliente
cliente() {
    exec 3> "$FIFO_SRV"    # escritura de peticiones
    exec 4<> "$FIFO_CLI"   # lectura de respuestas

    # Enviar números
    for num in 5 7 3 10; do
        echo "$num" >&3
        read -r respuesta <&4
        echo "Cliente: factorial($num) = $respuesta"
    done
    echo "quit" >&3
    exec 3>&-; exec 4>&-
}

# Ejecutar servidor en segundo plano
servidor &
server_pid=$!

sleep 0.1   # dar tiempo a que el servidor abra los pipes

# Ejecutar cliente
cliente

wait "$server_pid"
echo "Comunicación finalizada."

¿Cómo funciona?

    Se crean dos FIFOs: uno para enviar peticiones al servidor (FIFO_SRV), otro para recibir respuestas (FIFO_CLI).

    El servidor abre descriptores y entra en bucle leyendo números, calcula factoriales y responde.

    El cliente abre los descriptores, envía números, lee respuestas y finalmente envía "quit".

    Ambos cierran descriptores y se limpian los FIFOs.

Este esquema puede extenderse a múltiples clientes, pero hay que gestionar el acceso concurrente.