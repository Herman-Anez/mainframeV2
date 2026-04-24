# as

```bash
#!/bin/bash
# =============================================================================
# Script:  git-shift-files.sh
# Descripción:
#   En un directorio con archivos numerados (ej: 01-intro.md, 02-setup.md, ...)
#   este script incrementa en 1 los números de todos los archivos a partir de
#   un número dado, usando 'git mv' para conservar el historial.
#
# Uso:
#   ./git-shift-files.sh <número_inicio> [formato_padding]
#
# Argumentos:
#   número_inicio   : primer número que será incrementado (ej. 5 para subir 5->6)
#   formato_padding : (opcional) formato printf para el número, por defecto "%02d"
#                     Útil si tus archivos usan 001, 01, etc.
#
# Ejemplo (insertar un archivo después del 03):
#   # Copia el nuevo archivo con un nombre temporal:
#   cp nuevo.md temp_nuevo.md
#   # Incrementa todo a partir del 04 (porque después del 03 hay que liberar el 04)
#   ./git-shift-files.sh 4
#   # Ahora renombra el temporal a 04-nuevo.md (o el nombre que corresponda)
#   git mv temp_nuevo.md 04-nuevo.md
#   git add 04-nuevo.md
#   git commit -m "Inserta nuevo capítulo como 04-nuevo.md"
#
# Notas:
#   - Debe ejecutarse dentro de un repositorio Git.
#   - Los archivos deben seguir el patrón <número>-* (ej. 01-*.md, 02-*.txt).
#   - El patrón puede ajustarse en la variable PATRON.
#   - Se renombran en orden descendente para evitar conflictos.
#   - Se recomienda hacer un commit antes para poder volver atrás si algo falla.
#
# Autor: TuNombre
# Licencia: MIT
# =============================================================================

set -euo pipefail   # Detener en error, variables sin definir, fallo en pipes

# ---------- Configuración ----------
PATRON="*"                      # Extensión o parte fija del nombre, p.ej. "*.md"
PADDING_POR_DEFECTO="%02d"      # Formato por defecto (dos dígitos con cero a la izquierda)

# ---------- Funciones de apoyo ----------

# Mensaje de log con timestamp
log() {
    echo "[$(date '+%H:%M:%S')] $*"
}

# Salida con error
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Verifica que estamos dentro de un repositorio git
check_git_repo() {
    git rev-parse --git-dir >/dev/null 2>&1 || error_exit "No se detectó un repositorio Git. Ejecuta el script dentro de uno."
}

# ---------- Lectura de parámetros ----------
if [ $# -lt 1 ]; then
    echo "Uso: $0 <número_inicio> [formato_padding]"
    echo "Ejemplo: $0 5"
    echo "         $0 5 \"%03d\"  (para números como 005)"
    exit 1
fi

START_NUM=$1
# Validar que START_NUM es un entero positivo
if ! [[ "$START_NUM" =~ ^[0-9]+$ ]]; then
    error_exit "El número de inicio debe ser un entero positivo: '$START_NUM'"
fi

PADDING="${2:-$PADDING_POR_DEFECTO}"

# ---------- Pre-vuelo ----------
check_git_repo
log "Inicio del proceso de desplazamiento de archivos."
log "Comenzando desde el número $START_NUM (se incrementará en +1)."
log "Formato de número: $PADDING"

# Generar una lista de archivos que coincidan con el patrón <número>-*
# Se buscan archivos cuyo nombre empiece con un número (con padding variable) seguido de un guion.
# En este script asumimos que el nombre tiene dígitos al principio, luego un guion y el resto.
# Ajustar PATRON si es necesario (por ejemplo "*.md" para filtrar solo markdown).
mapfile -t FILES < <(ls | grep -E "^[0-9]+-.*${PATRON}$" | sort -t '-' -k1,1n)

if [ ${#FILES[@]} -eq 0 ]; then
    log "No se encontraron archivos que coincidan con el patrón."
    exit 0
fi

# Solo procesamos archivos cuyo número actual sea >= START_NUM
# Además, recorremos en orden descendente para que el renombrado no pise otros.
FILES_TO_SHIFT=()
for file in "${FILES[@]}"; do
    # Extraer el número del nombre: todo lo que está antes del primer '-'.
    # Ej: "02-intro.md" -> numero="02"
    numero=$(echo "$file" | cut -d'-' -f1)
    # Eliminar ceros a la izquierda para comparar numéricamente (evita que 08 se interprete como octal)
    num_val=$((10#$numero))
    if [ "$num_val" -ge "$START_NUM" ]; then
        FILES_TO_SHIFT+=("$file")
    fi
done

if [ ${#FILES_TO_SHIFT[@]} -eq 0 ]; then
    log "No hay archivos con número >= $START_NUM, nada que desplazar."
    exit 0
fi

# Ordenar descendentemente según el valor numérico
# Leemos el array y lo reordenamos
sorted_desc=()
while IFS= read -r line; do
    sorted_desc+=("$line")
done < <(for f in "${FILES_TO_SHIFT[@]}"; do
             num=$(echo "$f" | cut -d'-' -f1)
             printf "%s\t%s\n" $((10#$num)) "$f"
         done | sort -rn | cut -f2)

log "Se desplazarán ${#sorted_desc[@]} archivos (del mayor al menor) para evitar conflictos."

# ---------- Ejecutar git mv ----------
renombrados=0
for old_name in "${sorted_desc[@]}"; do
    # Extraer el número actual (con padding original)
    old_num_padded=$(echo "$old_name" | cut -d'-' -f1)
    old_num_val=$((10#$old_num_padded))
    # Calcular nuevo número (old_num_val + 1)
    new_num_val=$((old_num_val + 1))
    # Formatear el nuevo número con el padding deseado
    new_num_padded=$(printf "$PADDING" "$new_num_val")

    # Construir el nuevo nombre: reemplazar el número anterior por el nuevo
    # Conservamos la parte del nombre después del primer '-'
    rest_of_name=$(echo "$old_name" | cut -d'-' -f2-)
    new_name="${new_num_padded}-${rest_of_name}"

    # Verificar que el nuevo nombre no exista ya (no debería, pero por seguridad)
    if [ -e "$new_name" ]; then
        error_exit "Conflicto: el archivo destino '$new_name' ya existe. Abortando."
    fi

    # Realizar el renombrado con git mv
    log "git mv \"$old_name\" \"$new_name\""
    if git mv "$old_name" "$new_name"; then
        renombrados=$((renombrados + 1))
    else
        error_exit "Fallo al renombrar '$old_name' a '$new_name'."
    fi
done

log "Desplazamiento completado. $renombrados archivos renombrados con git mv."
log "Recuerda hacer commit de los cambios si todo es correcto."
```

aplicacion rapida 

```bash
( start=$1; pad=${2:-%02d}; pat=${3:-.*}; git rev-parse --git-dir >/dev/null 2>&1 || { echo "Not in a git repo"; exit 1; }; mapfile -t files < <(ls | grep -E "^[0-9]+-${pat}$" | sort -t '-' -k1,1n); to_shift=(); for f in "${files[@]}"; do n=$((10#$(echo "$f" | cut -d'-' -f1))); [[ $n -ge $start ]] && to_shift+=("$f"); done; [ ${#to_shift[@]} -eq 0 ] && { echo "No files to shift"; exit 0; }; readarray -t sorted < <(for f in "${to_shift[@]}"; do printf "%s\t%s\n" $((10#$(echo "$f" | cut -d'-' -f1))) "$f"; done | sort -rn | cut -f2); for old in "${sorted[@]}"; do old_num=$(echo "$old" | cut -d'-' -f1); old_val=$((10#$old_num)); new_val=$((old_val+1)); new_num=$(printf "$pad" "$new_val"); rest=$(echo "$old" | cut -d'-' -f2-); new="${new_num}-${rest}"; [ -e "$new" ] && { echo "Conflict: $new exists"; exit 2; }; git mv "$old" "$new"; done; echo "Shifted ${#sorted[@]} files." )
```
