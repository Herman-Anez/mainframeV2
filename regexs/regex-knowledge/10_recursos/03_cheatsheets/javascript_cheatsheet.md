
# Cheat Sheet: JavaScript Regex

Referencia rápida para el uso de expresiones regulares en JavaScript (Motores V8, SpiderMonkey, etc.), incluyendo las características modernas de **ES2018+**.

## Creación de expresiones regulares

*   **Literal:** `/patrón/flags` (Recomendado para patrones estáticos).
*   **Constructor:** `new RegExp('patrón', 'flags')` (Necesario para patrones dinámicos; requiere escapar barras invertidas: `\\`).

## Métodos principales

| Método | Contexto | Descripción |
| :--- | :---: | :--- |
| `regex.exec(str)` | `RegExp` | Ejecuta una búsqueda. Devuelve un array de resultados o `null`. Actualiza `lastIndex`. |
| `regex.test(str)` | `RegExp` | Devuelve `true` si hay coincidencia, `false` en caso contrario. |
| `str.match(regex)` | `String` | Devuelve un array con las coincidencias. Si no tiene flag `g`, incluye grupos. |
| `str.matchAll(regex)` | `String` | Devuelve un iterador con todas las coincidencias y sus grupos (requiere flag `g`). |
| `str.search(regex)` | `String` | Devuelve el índice de la primera coincidencia o `-1`. |
| `str.replace(re, sub)` | `String` | Reemplaza las coincidencias con una cadena o el resultado de una función. |
| `str.split(regex)` | `String` | Divide la cadena en un array usando la regex como separador. |

## Flags de JavaScript

| Flag | Nombre | Descripción |
| :---: | :--- | :--- |
| `g` | Global | No se detiene en la primera coincidencia. |
| `i` | Case-insensitive | Ignora mayúsculas y minúsculas. |
| `m` | Multiline | `^` y `$` coinciden con inicios y finales de línea. |
| `s` | Dotall | El punto `.` coincide también con saltos de línea (ES2018). |
| `u` | Unicode | Habilita el soporte para puntos de código Unicode (ES2015). |
| `y` | Sticky | Busca solo desde la posición `lastIndex` del motor. |
| `d` | Indices | Genera índices de inicio y fin para grupos de captura (ES2022). |

## Características modernas

*   **Propiedades Unicode (con flag `u`):** `\p{L}`, `\p{Emoji_Presentation}`, `\p{Script=Greek}`.
*   **Grupos con nombre (ES2018):** `(?<name>...)`. Se accede mediante `match.groups.name`.
*   **Lookbehind (ES2018):** Soporta tanto positivo `(?<=...)` como negativo `(?<!...)`.

> [!CAUTION]
> **Limitaciones de JavaScript:**
> No soporta grupos atómicos, cuantificadores posesivos, recursión, condicionales, la marca `\K` ni flags inline dentro del patrón.

> [!TIP]
> **Simulación de Grupo Atómico:** Puedes simular un grupo atómico usando un lookahead capturador seguido de una retroreferencia: `(?=(patrón))\1`.
> **Cadenas Literales:** Usa `String.raw` al definir regex en el constructor para evitar el doble escape de barras invertidas: `new RegExp(String.raw`\d+\.\d+`)`.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Cheat Sheet PCRE](pcre_cheatsheet.md) | [🏠 Inicio](../../README.md) | [Cheat Sheet Python ▶](python_cheatsheet.md) |

