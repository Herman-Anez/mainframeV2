# JavaScript.md
## Motor regex en JavaScript

JavaScript utiliza un motor de regex integrado en los motores V8 (Chrome, Node.js), SpiderMonkey (Firefox), JavaScriptCore (Safari). Históricamente ha sido limitado, pero las versiones modernas (ES2015 en adelante) han añadido características significativas.

### Evolución y versiones

| Versión | Añadidos |
| :--- | :--- |
| **ES3 (1999)** | Base: literales `/.../`, grupos de captura, backreferences, cuantificadores greedy, lookahead, m, i, g. |
| **ES5 (2009)** | "use strict" sin cambios en regex. |
| **ES2015 (ES6)** | Flag **u** (Unicode), flag **y** (sticky). Nueva sintaxis de escape unicode `\u{...}`. |
| **ES2018** | Flag **s** (dotAll), lookbehind `(?<= )` / `(?<! )`, grupos con nombre `(?<name>...)`, propiedades Unicode `\p{...}`. |
| **ES2020** | `String.prototype.matchAll` (iterador). |
| **ES2021** | Sin cambios importantes. |
| **ES2022** | Flag **d** (hasIndices) para obtener posición de grupos. |

### Características actuales (ES2022+)

*   **Lookahead positivo y negativo**: soportados de siempre.
*   **Lookbehind (desde ES2018)**: soporta longitud variable sin restricciones.
*   **Grupos con nombre**: `(?<year>\d{4})` y acceso vía `match.groups.year`.
*   **Propiedades Unicode**: `/\p{Script=Greek}/u`.
*   **Flag s (dotAll)**: `.` incluye `\n`.
*   **Flag y (sticky)**: Búsqueda desde la posición exacta indicada por `lastIndex` sin ignorar caracteres previos.
*   **Flag d (indices)**: `match.indices` retorna arrays con inicio/fin de cada grupo.

### Lo que NO tiene JavaScript

*   Grupos atómicos `(?>...)`.
*   Cuantificadores posesivos `*+`, `++`.
*   Recursión y subrutinas.
*   Condicionales `(?(cond)si|no)`.
*   `\K` (keep out).
*   Verbos de control como `(*SKIP)`.
*   **Modo verboso**: no hay flag `x`. Los patrones se escriben como cadenas normales.

### Simulación de grupos atómicos en JS

Podemos emular un grupo atómico usando un lookahead y una backreference:
```javascript
// Simular (?>a+)b
let regex = /(?=(a+))\1b/;
// El lookahead captura todas las 'a', luego \1 las consume sin poder retroceder.
```
> [!TIP]
> Este truco funciona para patrones simples. Para casos más complejos con alternancia no es suficiente.

### Flag y (sticky)

La búsqueda solo tiene éxito si la coincidencia comienza exactamente en la posición `regex.lastIndex`.
```javascript
let regex = /\d+/y;
regex.lastIndex = 2;
"abc 123".match(regex); // null, porque en posición 2 está 'c '
regex.lastIndex = 4;
"abc 123".match(regex); // "123"
```
*Es útil en tokenizadores.*

### Flag d (hasIndices)

Devuelve las posiciones de inicio y fin de la coincidencia y de cada grupo.
```javascript
let regex = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/d;
let match = regex.exec('2024-12-25');
match.indices.groups.year; // [0, 4]
```

### Buenas prácticas en JS

*   Usar el constructor `RegExp` cuando el patrón es dinámico, escapando adecuadamente las barras.
*   Aprovechar plantillas de cadena para mayor legibilidad:
    ```javascript
    let pattern = new RegExp(String.raw`
      ^
      (?<area>\d{3})
      -
      (?<number>\d{7})
      $
    `.replace(/\s+/g, ''), ''); // eliminar espacios simulando modo verboso
    ```
*   Cuidado con el escape de barras invertidas en cadenas normales: `'\d'` se convierte en `d` a menos que sea `'\\d'`.

### Ejemplos prácticos en JS

**Extraer hashtags de un tweet, devolviendo solo palabras sin #:**
```javascript
let tweet = "Hola #gente #regex #JS2024";
let hashtags = [...tweet.matchAll(/(?<=#)\w+/gu)].map(m => m[0]);
// ["gente", "regex", "JS2024"]
```

**Validar email con Unicode:**
```javascript
let emailRegex = /^[\p{L}._%+\-]+@[\p{L}.\-]+\.[\p{L}]{2,}$/u;
emailRegex.test("jörn@müller.de"); // true
```

---

### 📖 Temas relacionados
| Archivo | Descripción |
| :--- | :--- |
| [01_comparativa_general.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/01_comparativa_general.md) | Comparativa entre motores |
| [02_PCRE.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/02_PCRE.md) | Detalles del motor PCRE |
| [04_Python.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/04_Python.md) | El módulo re y regex de Python |


---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Pcre](02_PCRE.md) | [🏠 Inicio](../../README.md) | [Python ▶](04_Python.md) |
