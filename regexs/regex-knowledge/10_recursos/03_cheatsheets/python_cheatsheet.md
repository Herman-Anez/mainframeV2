# Cheat Sheet: Python Regex

Referencia para el uso de expresiones regulares en Python, cubriendo tanto el módulo estándar `re` como el módulo avanzado `regex`.

## Módulos disponibles

> [!NOTE]
> **Módulo `re` (Librería estándar):** Estable y rápido, pero con limitaciones (lookbehind de longitud fija, sin grupos atómicos ni recursión).
> **Módulo `regex` (PyPI):** Compatible con `re` pero incluye todas las características de PCRE (lookbehind variable, recursión, grupos atómicos y soporte completo de Unicode).

## Funciones principales (módulo `re`)

| Función | Propósito |
| :--- | :--- |
| `re.search(pat, text)` | Busca la primera coincidencia en cualquier posición de la cadena. |
| `re.match(pat, text)` | Intenta casar el patrón solo desde el **inicio** de la cadena. |
| `re.fullmatch(pat, text)` | Devuelve un Match solo si el patrón coincide con la **cadena completa**. |
| `re.findall(pat, text)` | Devuelve una lista con todas las coincidencias encontradas. |
| `re.finditer(pat, text)` | Devuelve un iterador que proporciona objetos Match para cada coincidencia. |
| `re.sub(pat, repl, text)` | Reemplaza las coincidencias encontradas con una cadena o función. |
| `re.split(pat, text)` | Divide la cadena utilizando el patrón como delimitador. |
| `re.compile(pat, flags)` | Compila un patrón para su reutilización (mejora el rendimiento). |

## Flags de Python

| Constante | Versión corta | Significado |
| :--- | :---: | :--- |
| `re.IGNORECASE` | `re.I` | Ignora mayúsculas y minúsculas. |
| `re.MULTILINE` | `re.M` | `^` y `$` coinciden con inicios y finales de línea. |
| `re.DOTALL` | `re.S` | El punto `.` coincide también con saltos de línea `\n`. |
| `re.VERBOSE` | `re.X` | Permite escribir la regex en varias líneas y añadir comentarios. |
| `re.ASCII` | `re.A` | Hace que `\w`, `\d`, `\s`, `\b` solo coincidan con caracteres ASCII. |
| `re.UNICODE` | `re.U` | Habilita soporte Unicode (comportamiento por defecto en Python 3). |

## Grupos con nombre

*   **Definición:** `(?P<nombre>...)`.
*   **Retroreferencia en el patrón:** `(?P=nombre)`.
*   **Acceso en el objeto Match:** `match.group('nombre')`.
*   **Uso en sustitución (`re.sub`):** `\g<nombre>`.

> [!IMPORTANT]
> **Diferencias críticas con PCRE (módulo `re`):**
> *   **Lookbehind:** Solo se permiten patrones de longitud fija (no se permite `+`, `*` o `{n,}`).
> *   **Funciones faltantes:** No soporta grupos atómicos, cuantificadores posesivos, recursión ni la marca `\K`.
> *   **Propiedades Unicode:** No soporta `\p{L}` de forma nativa (se requiere el módulo `regex`).

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Cheat Sheet JavaScript](javascript_cheatsheet.md) | [🏠 Inicio](../../README.md) | [Enlaces Útiles ▶](../04_enlaces_utiles.md) |