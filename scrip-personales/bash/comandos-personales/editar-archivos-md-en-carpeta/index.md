
# index

Edita todos loas archivos .md de una carpeta, revisa si tiene un string insertado al final del archivo, si no lo tiene lo agrega.

```bash
for f in *.md; do
  grep -qxF "[back](../index.md)" "$f" || echo "[back](../index.md)" >> "$f"
done
```

for f in *.md; do

- `for`: inicia un bucle.
- `f`: es una variable que irá tomando distintos valores.
- `in *.md`: significa “para cada archivo que termine en .md en esta carpeta”.
- `*.md`: es un glob, un patrón que coincide con todos los archivos Markdown.
- `do`: indica el inicio del bloque de instrucciones que se ejecutará en cada iteración.

👉 En resumen: “para cada archivo .md, haz lo siguiente…”

echo `"[back](../index.md)"`

echo: imprime texto en la salida estándar.
`"[back](../index.md)"`: es el string que quieres añadir.

`>> "$f"`

- `>>`: redirección que añade (append) al final del archivo.
- `"$f"`: es el archivo actual del bucle.

Las comillas "" evitan problemas si el nombre del archivo tiene espacios.

👉 Esto significa: “añade ese texto al final del archivo”.

grep -qxF `"[back](../index.md)"` "$f"

grep: busca texto dentro de un archivo.
-q: modo silencioso (no imprime nada, solo devuelve éxito o fallo).
-x: exige coincidencia de línea completa.
-F: busca texto literal (no regex).
Si encuentra la línea exacta, devuelve éxito.

||

Es un operador lógico: “OR”.
Significa: “si lo de la izquierda falla, ejecuta lo de la derecha”.

👉 Entonces:

Si no encuentra la línea → se ejecuta echo >> "$f"
Si ya existe → no hace nada