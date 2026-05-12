# POSIX.md
## Expresiones regulares POSIX

El estándar POSIX define dos tipos de expresiones regulares para herramientas de línea de comandos Unix/Linux: BRE (Basic Regular Expressions) y ERE (Extended Regular Expressions). Son mucho más simples que los motores modernos y no incluyen la mayoría de las funcionalidades avanzadas.

### BRE (Basic Regular Expressions)

Utilizadas por defecto en `grep`, `sed` y `ed`. Características:

*   La mayoría de metacaracteres requieren escape: `{ }`, `( )`, `?`, `+`, `|` no son metacaracteres a menos que se escapen con `\`.
*   `*` sí actúa como cuantificador (cero o más).
*   `.` y `[ ]` funcionan como siempre.
*   `^` y `$` representan inicio/fin de línea.
*   **Retroreferencias**: `\( ... \)` captura un grupo y `\1` hace referencia a él. Esto es exclusivo de BRE; ERE no tiene backreferences.
*   No hay `+` nativo (hay que escribir `\+`), ni `?` (`\?`), ni `|` (`\|`).

**Ejemplo de BRE:**
```bash
grep '^\(hello\).*\1$' file.txt   # línea que empieza y termina con "hello" (usando captura)
```

### ERE (Extended Regular Expressions)

Activan con `grep -E` (o `egrep`) y `sed -E`. Añaden metacaracteres sin necesidad de escape:

*   `+`, `?`, `{ }`, `|`, `( )` son reconocidos directamente como especiales.
*   **Sin retroreferencias**: `\1` es tratado como carácter literal (error o escape no válido, depende de la implementación). No hay memoria de capturas (aunque `( )` se usan para agrupar, no capturan en el sentido de backreference).
*   No tienen `\b` ni `\B`, ni `\w/\d/\s` (aunque algunas versiones de grep con la opción `-w` buscan palabras completas externamente).
*   No hay lookahead, lookbehind, grupos atómicos, etc.
*   **Clases POSIX**: `[[:alnum:]]`, `[[:digit:]]`, `[[:space:]]`, etc., son soportadas.

**Ejemplo de ERE:**
```bash
grep -E 'colou?r' file.txt   # "color" o "colour"
grep -E '[0-9]{3}-[0-9]{2}' file.txt  # número de seguro social formato USA
```

### Herramientas y uso

| Herramienta | Modo por defecto | Activación ERE |
| :--- | :--- | :--- |
| **grep** | BRE | `grep -E` o `egrep` |
| **sed** | BRE | `sed -E` (o `-r` en GNU) |
| **awk** | ERE (en la mayoría de implementaciones actuales) | Por defecto (en mawk, gawk) |
| **vi/vim** | BRE (en búsquedas con `/`) | `\v` (very magic) para ERE |

### Limitaciones generales

*   No admiten cuantificadores no greedy (perezosos). `*?` no existe.
*   No hay anclas de palabra `\b`; se puede simular con `[[:<:]]` y `[[:>:]]` en algunas implementaciones (GNU) pero no es estándar.
*   No hay metacaracteres predefinidos como `\d`, `\w`; se usan clases POSIX `[[:digit:]]`, `[[:alnum:]]` o rangos.
*   No hay grupos atómicos ni posesivos.
*   Son motores DFA (o híbridos en GNU) que evitan el backtracking, por lo que son rápidos y no sufren backtracking catastrófico. Sin embargo, sacrifican funcionalidad.

### Escapado en BRE

Para usar `(`, `)`, `{`, `}`, `?`, `+`, `|` como metacaracteres, se requiere `\`. De lo contrario, coinciden literalmente.

*   **Sin escape**: `a{3}` busca "a{3}" literal.
*   **Con escape**: `a\{3\}` busca exactamente 3 'a's.

> [!IMPORTANT]
> Esto hace que los patrones BRE sean confusos y propensos a errores. Muchos usuarios prefieren siempre el modo ERE para scripts.

### POSIX en la práctica moderna

Hoy en día, las herramientas del sistema siguen usando POSIX. Por ejemplo, para validar un email simple en un script de shell con `grep -E`:
```bash
echo "user@domain.com" | grep -E '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
```
*Aunque no es una validación robusta, cubre casos sencillos.*

### Consejos

*   En scripts portables, limítate a POSIX ERE o BRE según la necesidad.
*   Para tareas complejas, delega a un lenguaje moderno (Perl, Python, etc.) en vez de luchar con `sed/grep`.
*   Las clases POSIX son la forma más clara de expresar conjuntos en estos entornos.

---

### Ejemplo práctico en `sed`

**Reemplazar múltiples espacios por uno solo:**
```bash
sed -E 's/[[:space:]]+/ /g' archivo.txt
```

---

### 📖 Temas relacionados
| Archivo | Descripción |
| :--- | :--- |
| [01_comparativa_general.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/01_comparativa_general.md) | Comparativa entre motores |
| [02_PCRE.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/02_PCRE.md) | Detalles de PCRE |


---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Net](06_NET.md) | [🏠 Inicio](../../README.md) | ➖ |
