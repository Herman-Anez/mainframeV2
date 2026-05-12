# PCRE.md
## ¿Qué es PCRE?

PCRE (Perl Compatible Regular Expressions) es una biblioteca de código abierto que implementa expresiones regulares inspiradas en las de Perl, añadiendo alguna extensión adicional. Es el motor usado por PHP (las funciones `preg_*`), Apache (`mod_rewrite`, `mod_security`), Postfix, y muchos otros. Existen dos versiones principales: PCRE (la original, ya obsoleta) y PCRE2 (reescrita, con soporte mejorado y nueva API).

### Características destacadas

*   Todas las funcionalidades comunes: lookahead, lookbehind, grupos atómicos, cuantificadores posesivos, retroreferencias, grupos con nombre, condicionales.
*   Recursión y subrutinas.
*   Verbos de control: `(*SKIP)`, `(*FAIL)`, `(*COMMIT)`, etc.
*   `\K`: reinicia el inicio de la coincidencia.
*   Unicode completo (propiedades, scripts) con flag `u` o `(*UTF)(*UCP)`.
*   Compatibilidad con Perl muy alta, aunque con algunas diferencias (ej. manejo de `\z` y `\Z` es idéntico).

### Versiones PCRE vs PCRE2

*   **PCRE (8.xx)**: última versión, congelada. Limitada a lookbehind de longitud fija.
*   **PCRE2 (10.xx)**: reescritura completa. Soporta lookbehind variable (con ciertas restricciones, debe poder determinarse una longitud máxima). Mejor rendimiento, nueva API.

> [!NOTE]
> PHP en sus versiones recientes (7.3+) ya usa PCRE2.

### Sintaxis y activación de flags

En PHP (PCRE), las flags se añaden al final del delimitador: `/patrón/ixu`. Dentro del patrón se pueden modificar con `(?i)`, `(?-i)`, `(?i:…)`.

**Ejemplo de lookbehind variable en PCRE2:**
```php
preg_match('/(?<=abc|defg)X/', 'defgX'); // válido en PCRE2, error en PCRE antiguo
```

### Recursión y subrutinas

Permite emparejar estructuras anidadas sin fin de grupos. Ejemplo: paréntesis balanceados.
```regex
\( (?: [^()]++ | (?R) )* \)
```
*   `[^()]++` consume caracteres que no son paréntesis (posesivo).
*   `| (?R)` permite volver a aplicar el patrón completo recursivamente.
*   El asterisco `*` repite todo el grupo.

Subrutinas con `(?&nombre)` reutilizan un grupo nombrado, pero re-evaluando su patrón, no su captura.
```regex
(?<word>\w+)\ (?&word)   // palabra repetida: "hola hola"
```

### Verbos de control avanzados

Son metacomandos en la sintaxis `(*... )`. Algunos:

*   **`(*SKIP)(*FAIL)`**: Descarta todo el texto hasta la posición actual y fuerza que el motor continúe desde después de esa posición. Ideal para ignorar contenido.
    ```regex
    <.*?(*SKIP)(*FAIL)|(?<=>)\w+
    ```
    *Encuentra palabras que están fuera de etiquetas HTML: primero salta las etiquetas, luego busca palabras.*

*   **`(*COMMIT)`**: Una vez que se ha pasado ese punto, no se permite backtracking que retroceda más atrás del commit. Similar a grupo atómico global.

*   **`(*MARK:nombre)`** y **`(*THEN)`**: para control en alternancia.

### `\K` (Keep Out)

Descarta todo lo coincidido a su izquierda. Equivale a un lookbehind positivo variable, pero más eficiente.
```regex
€\K\d+\.\d{2}   // captura solo la cantidad, descartando el símbolo €
```

### Soporte Unicode

PCRE2 con las opciones `PCRE2_UTF` y `PCRE2_UCP` activa el modo Unicode. En PHP se usa el flag `u`. Permite `\p{...}`, `\P{...}`, y ajusta `\w`, `\d`, `\b`.
```php
preg_match('/\p{Greek}/u', 'αβγ'); // true
```

### Limitaciones

*   No soporta grupos balanceados como .NET.
*   La recursión puede causar stack overflow en profundidades extremas.
*   El lookbehind variable en PCRE2 está restringido: no permite cuantificadores sin límite superior dentro del lookbehind si no se puede calcular una longitud máxima (ej. `(?<=\d+)\w` está bien porque la longitud máxima es ilimitada pero el motor lo maneja, aunque hay límites de recursos). En realidad, PCRE2 permite cualquier patrón, pero intenta averiguar la longitud máxima; si no puede, lo trata como no fijo internamente, y puede recurrir a probar desde el inicio de la cadena, lo cual es ineficiente. Se recomienda acotar cuantificadores.

### Ejemplos prácticos en PHP

**Extraer números de teléfono con formato español (+34 XXX XXX XXX) sin capturar prefijo:**
```php
$patron = '/\+34\K\s?\d{3}\s?\d{3}\s?\d{3}/';
preg_match_all($patron, '+34 612 345 678 y +34 987654321', $matches);
// $matches[0] contiene "612 345 678" y "987654321"
```

**Validar código postal español (5 dígitos, opcionalmente seguido de "-" + 4 dígitos):**
```php
$cp = '/^(\d{5})(?:-(\d{4}))?$/';
```

---

### 📖 Temas relacionados
| Archivo | Descripción |
| :--- | :--- |
| [01_comparativa_general.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/01_comparativa_general.md) | Comparativa entre motores |
| [03_JavaScript.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/03_JavaScript.md) | Regex en el ecosistema ECMAScript |
| [04_Python.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/04_Python.md) | El módulo re y regex de Python |


---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Comparativa General](01_comparativa_general.md) | [🏠 Inicio](../../README.md) | [Javascript ▶](03_JavaScript.md) |
