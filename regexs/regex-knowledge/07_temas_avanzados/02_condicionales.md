# Condicionales

Las construcciones condicionales permiten elegir entre dos (o más) patrones basándose en una condición específica dentro de la expresión regular.

**Sintaxis general:**
```regex
(?(condición)patrón-si|patrón-no)
```

La **condición** puede ser:
*   **Un número de grupo captura:** ej. `(?(1)…)`. Se cumple si el grupo 1 participó en la coincidencia.
*   **Un nombre de grupo:** `(?(<nombre>)…)` o `(?(nombre)…)`.
*   **Una aserción (lookahead o lookbehind):** `(?(?=…)patrón-si|patrón-no)`.

## Condición basada en grupo existente

```regex
(\+34)?(\d{9})(?(1)|(?:ERROR))
```
1.  Captura opcional de `+34` en grupo 1.
2.  Luego dígitos (`\d{9}`).
3.  **Condicional:** si el grupo 1 existe (se capturó el prefijo), no hace nada extra (vacío después de `|`). Si no, intenta casar `"ERROR"`.

> [!TIP]
> Una forma más práctica es permitir formato con o sin prefijo, pero aplicar lógica según la presencia del grupo.

### Ejemplo real: fecha con formato flexible
Ejemplo donde el separador debe ser consistente (simplificado):
```regex
(\d{4})([-/])(\d{2})\2(\d{4} | (?(1)\d{4}|\d{2}))
```

### Patrón clásico: número de teléfono con prefijo opcional
```regex
^(?:(\+34)\s?)?\d{9}(?(1)|(?=.))
```
Si el grupo 1 capturó `+34`, entonces continúa; si no, el condicional falla a menos que pongamos un patrón alternativo.

## Condición con aserción

```regex
(?(?=[A-Z])[A-Z]\w*|[a-z]\w*)
```
Si la posición actual empieza con mayúscula, usa el patrón de mayúscula; si no, el de minúscula. Es equivalente a una alternancia con lookahead, pero más elegante.

## Condicionales y grupos nombrados

Soportado en PCRE, Perl, .NET y el módulo `regex` de Python:
```regex
(?<quote>['"])?(?(<quote>).*?\k<quote>|\S+)
```
Si se captura una comilla (simple o doble) en el grupo `quote`, busca contenido hasta encontrar la misma comilla. Si no se captura, busca una palabra sin espacios (`\S+`).

## Soporte por motor

> [!IMPORTANT]
> *   **PCRE / PHP:** Condicionales completos (grupos y aserciones).
> *   **Perl:** Soporte completo.
> *   **Python regex:** Soporta grupos y aserciones; el módulo estándar `re` **no** los soporta.
> *   **.NET:** Soporte completo.
> *   **Java, JavaScript:** **No soportan** condicionales nativamente.

## Sintaxis detallada

*   **`(?(n)si|no)`**: `n` es el número de grupo de captura (sin escape).
*   **`(?(<name>)si|no)`** o **`(?(name)si|no)`**.
*   **`(?(?=...)si|no)`**: Aserción positiva.
*   **`(?(?!...)si|no)`**: Aserción negativa.
*   **Omitir rama `no`**: Se puede dejar vacía: `(?(1)si)`.

## Casos de uso prácticos

1.  **Formato de moneda condicional:** Si hay decimales, forzar dos dígitos; si no, número entero.
    ```regex
    \$(?:(\.\d{2})|(\d+))(?(1)(?=.\d{2})|\b)
    ```
2.  **Comillas tipográficas:** Asegurar que las citas empiecen y terminen con el mismo tipo de comilla (`« »` vs `" "`).
3.  **Paréntesis opcionales balanceados:** `(\(?\d+\)?)?` con condicional para cerrar correctamente.

## Alternativas cuando no hay soporte

En motores sin condicionales, se puede simular con una alternancia que repita partes del patrón:
```regex
(\+34)?\d{9}  ->  (?:\+34\d{9}|\d{9})
```
Sin embargo, se pierde la capacidad de referir dinámicamente a la captura. Para lógicas complejas en motores limitados, es necesario usar lógica en el código del lenguaje (dos regex separadas o un `if`).

## Precauciones

> [!WARNING]
> *   **Legibilidad:** Las condiciones pueden complicar el patrón; usa el modo verboso (`/x`) para documentar.
> *   **Backtracking:** Al igual que otras construcciones avanzadas, pueden aumentar el backtracking si no se acotan correctamente.

---

### 📖 Temas relacionados
| Archivo | Descripción |
| :--- | :--- |
| [01_recursion_y_subrutinas.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/07_temas_avanzados/01_recursion_y_subrutinas.md) | Patrones recursivos y subrutinas |
| [04_backtracking_catastrofico.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/07_temas_avanzados/04_backtracking_catastrofico.md) | Riesgos de rendimiento |
| [06_motores_y_dialectos](../06_motores_y_dialectos/01_comparativa_general.md) | Comparativa de soporte |
