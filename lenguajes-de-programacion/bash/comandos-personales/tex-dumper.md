find . -type f -print0 | while IFS= read -r -d '' file; do \
  echo "===== INICIO: $file ====="; \
  cat "$file"; \
  echo; \
  echo "===== FIN: $file ====="; \
  echo; \
done > salida.txt

find . -type f \
  ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  -print0 | while IFS= read -r -d '' file; do
    echo "===== INICIO: $file ====="
    cat "$file"
    echo
    echo "===== FIN: $file ====="
    echo
  done > salida.txt

  Explicación:

    find . -type f -print0 → lista todos los archivos (solo archivos regulares) desde el directorio actual, separando los nombres con \0 (nulo), lo que soporta espacios, saltos de línea y caracteres especiales.

    while IFS= read -r -d '' file → lee cada nombre de archivo de forma segura.

    echo "===== INICIO: ... ===== → marca el inicio.

    cat "$file" → muestra el contenido.

    echo (vacío) y echo "===== FIN ... ===== → separadores.

    Todo el bloque se redirige a salida.txt.