# Cheat Sheet: PCRE (PHP, PCRE2, Apache)

Esta hoja de trucos cubre la sintaxis de **PCRE** (*Perl Compatible Regular Expressions*), que es el estándar más utilizado en servidores web, lenguajes como PHP y herramientas de línea de comandos.

## Metacaracteres básicos

| Símbolo | Significado |
| :--- | :--- |
| `.` | Cualquier carácter excepto nueva línea (incluye `\n` con flag `s`). |
| `^` | Inicio de cadena o de línea (con flag `m`). |
| `$` | Fin de cadena o de línea (con flag `m`). |
| `*` | Cuantificador: 0 o más veces. |
| `+` | Cuantificador: 1 o más veces. |
| `?` | Cuantificador: 0 o 1 vez / Hace que un cuantificador sea perezoso (*lazy*). |
| `{n}` | Exactamente `n` veces. |
| `{n,}` | Al menos `n` veces. |
| `{n,m}` | Entre `n` y `m` veces. |
| `*+`, `++`, etc. | Cuantificadores posesivos (no retroceden). |
| `( ... )` | Grupo de captura. |
| `(?: ... )` | Grupo sin captura. |
| `(?<name>...)` | Grupo de captura con nombre. |
| `(?> ... )` | Grupo atómico. |
| `\|` | Alternancia (OR lógico). |
| `\` | Carácter de escape. |

## Clases de caracteres

| Símbolo | Equivalente / Significado |
| :--- | :--- |
| `\d` | Dígito `[0-9]` (soporta Unicode con flag `u`). |
| `\D` | Cualquier carácter que NO sea un dígito. |
| `\w` | Carácter de palabra `[a-zA-Z0-9_]` (soporta Unicode con flag `u`). |
| `\W` | Cualquier carácter que NO sea de palabra. |
| `\s` | Espacio en blanco (espacio, tabulador, nueva línea). |
| `\S` | Cualquier carácter que NO sea un espacio en blanco. |
| `\h` | Espacio horizontal. |
| `\v` | Espacio vertical. |
| `\R` | Salto de línea universal (cualquier secuencia de fin de línea). |

## Anclas y límites

| Símbolo | Significado |
| :--- | :--- |
| `\b` | Límite de palabra (*boundary*). |
| `\B` | Posición que NO es un límite de palabra. |
| `\A` | Inicio absoluto de la cadena (ignora flag `m`). |
| `\z` | Final absoluto de la cadena (ignora flag `m`). |
| `\Z` | Final de la cadena o justo antes de un salto de línea final. |

## Lookahead / Lookbehind

| Constructo | Significado |
| :--- | :--- |
| `(?=...)` | **Lookahead positivo:** Asegura que lo que sigue coincide con el patrón. |
| `(?!...)` | **Lookahead negativo:** Asegura que lo que sigue NO coincide con el patrón. |
| `(?<=...)` | **Lookbehind positivo:** Asegura que lo que precede coincide (longitud fija/variable en PCRE2). |
| `(?<!...)` | **Lookbehind negativo:** Asegura que lo que precede NO coincide con el patrón. |

## Flags comunes

| Flag | Descripción |
| :---: | :--- |
| `i` | Case-insensitive: ignora mayúsculas y minúsculas. |
| `m` | Multiline: `^` y `$` coinciden con inicios y fines de línea. |
| `s` | Dotall: el punto `.` coincide también con saltos de línea `\n`. |
| `x` | Verbose: permite espacios y comentarios dentro de la regex. |
| `u` | Unicode: habilita el soporte completo para caracteres internacionales. |
| `U` | Ungreedy: invierte la codicia de los cuantificadores por defecto. |

## Avanzado PCRE

| Constructo | Descripción |
| :--- | :--- |
| `(?R)`, `(?0)` | Recursión: intenta casar el patrón completo de nuevo. |
| `(?1)`, `(?2)` | Recursión a un grupo de captura específico por su número. |
| `(?&name)` | Subrutina: llama a un grupo de captura con nombre. |
| `\k<name>` | Retroreferencia a un grupo capturado con nombre. |
| `\g{n}` | Retroreferencia para números de grupo grandes. |
| `(?(cond)si\|no)` | Expresión condicional. |
| `\K` | Descarta todo lo coincidido a la izquierda de esta marca. |
| `(*SKIP)(*FAIL)` | Control de backtracking para saltar y fallar tramos. |
| `(*COMMIT)` | Confirma el avance actual; si falla después, no hay retroceso. |
| `\p{L}`, `\p{S}` | Coincide con propiedades Unicode (Letras, Símbolos, etc.). |

## Secuencias de escape

| Secuencia | Significado |
| :--- | :--- |
| `\n` | Nueva línea. |
| `\r` | Retorno de carro. |
| `\t` | Tabulador. |
| `\x{2020}` | Carácter Unicode especificado por su código hexadecimal. |
| `\Q...\E` | Trata todo el texto entre las marcas como literales (ignora metacaracteres). |

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Cheat Sheets Index](index.md) | [🏠 Inicio](../../README.md) | [Cheat Sheet JavaScript ▶](javascript_cheatsheet.md) |