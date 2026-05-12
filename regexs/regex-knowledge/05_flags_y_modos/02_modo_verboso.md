# Modo Verboso (Extended)

## Definición

El **modo verboso** (flag `x` o `re.VERBOSE`) permite escribir expresiones regulares con espacios, tabulaciones, saltos de línea y comentarios, todo lo cual es ignorado por el motor. Así se pueden formatear patrones complejos de manera legible, como si fuera código con documentación embebida.

## Motores que lo soportan

*   **Python:** `re.VERBOSE` (o `re.X`)
*   **PCRE / PHP:** flag `x` después del delimitador o `(?x)` dentro del patrón.
*   **Perl:** `/x`
*   **.NET:** `RegexOptions.IgnorePatternWhitespace`
*   **Java:** `Pattern.COMMENTS`
*   **Ruby:** opción `x` en `Regexp.new`

> [!WARNING]
> **JavaScript:** NO lo soporta de manera nativa. Algunas bibliotecas como (XRegExp) lo implementan. La alternativa es construir el patrón con literales de plantilla multilínea y concatenación, aunque los comentarios no se ignoran de forma automática.

## Reglas de ignorado en modo verboso

1.  **Espacios:** Todos los espacios y tabuladores (excepto dentro de clases de caracteres `[...]`) son ignorados.
2.  **Saltos de línea:** Los saltos de línea son ignorados por completo.
3.  **Comentarios:** Comienzan con el carácter `#` y se extienden hasta el final de la línea. Ese texto no forma parte del patrón.

> [!TIP]
> Si se necesita un `#` literal, debe escaparse como `\#` o incluirse en una clase `[#]`.

## Ventajas

*   **Autodocumentación:** Patrones largos, como validación de contraseñas o direcciones, se vuelven comprensibles.
*   **Mantenimiento:** Facilita el mantenimiento y la colaboración en equipo.
*   **Estructura:** Permite desglosar patrones anidados en líneas separadas para mayor claridad.

## Ejemplo de patrón complejo tradicional vs. verboso

### Validación de email simplificada (Sin modo verboso)

```regex
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

### Versión verbosa en Python

```python
import re

pattern = re.compile(r"""
    ^                      # inicio de cadena
    [a-zA-Z0-9._%+-]+      # parte local (nombre de usuario)
    @                      # símbolo arroba
    [a-zA-Z0-9.-]+         # dominio
    \.                     # punto literal
    [a-zA-Z]{2,}           # extensión (al menos 2 letras)
    $                      # final de cadena
""", re.VERBOSE)
```

Mucho más claro, especialmente si el patrón sigue creciendo en complejidad.

## Cómo incluir espacios o # literales en modo verboso

Hay que escapar los espacios (con `\` o `[ ]`) y el símbolo `#` (con `\#`).

### Ejemplo

```python
re.compile(r"""
    \d+        # uno o más dígitos
    [ ]        # un espacio en blanco literal
    \#\d+      # almohadilla literal seguida de dígitos
""", re.VERBOSE)
```

> [!NOTE]
> También se puede usar `\s` cuando se quiere un espacio genérico, lo cual no se ve afectado por la supresión de espacios del modo verboso porque `\s` es una clase predefinida.

## Ámbito del flag `x`

Se puede activar para todo el patrón (mediante la bandera externa o `(?x)` al inicio) o solo para una porción:

*   `(?x)patrón` activa el modo.
*   `(?-x)patrón` lo desactiva.
*   `(?x:patrón)` aplica solo al grupo.

Esto es útil cuando solo una parte necesita comentarios o contiene muchos espacios que no deben ignorarse.

## Ejemplo de combinación con otras flags

### En Python

```python
re.compile(r"""
    ^
    (?=.*\d)    # al menos un dígito
    .{8,}
    $
""", re.VERBOSE | re.IGNORECASE)
```

### En PCRE/PHP

```php
preg_match('/
    ^
    (?=.*\d)    # dígito
    .{8,}
    $
/xi', $texto);
```

> [!IMPORTANT]
> En PCRE, los comentarios terminan con el final de la línea; no se puede poner nada tras `#` en esa línea, salvo que se usen delimitadores no usuales y todo vaya seguido.

## Alternativas en JavaScript

Como JavaScript carece de modo verboso, se puede usar una plantilla multilínea y unir las partes:

```javascript
let patrón = [
    '^',                    // inicio
    '[a-zA-Z0-9._%+-]+',    // usuario
    '@',
    '[a-zA-Z0-9.-]+',       // dominio
    '\\.',
    '[a-zA-Z]{2,}',
    '$'
].join('');

let regex = new RegExp(patrón);
```

No es tan limpio como los comentarios nativos, pero ayuda a estructurar patrones extensos.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Flags Comunes](01_flags_comunes.md) | [🏠 Inicio](../../README.md) | [Soporte Unicode ▶](03_unicode.md) |

