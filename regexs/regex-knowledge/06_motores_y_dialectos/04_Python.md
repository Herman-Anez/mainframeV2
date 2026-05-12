# Python.md
## Dos motores en Python

Python tiene dos opciones para trabajar con regex:

*   **Módulo re**: incluido en la biblioteca estándar. Limitado en funcionalidades avanzadas.
*   **Módulo regex (externo, PyPI)**: instalable con `pip install regex`. Superset compatible con `re` pero añade soporte de PCRE (recursión, lookbehind variable, grupos atómicos, etc.).

### Módulo re estándar

#### Características

*   Lookahead positivo/negativo.
*   Lookbehind positivo/negativo solo con patrones de ancho fijo (cada alternativa debe tener la misma longitud, sin cuantificadores variables).
*   Grupos con nombre `(?P<name>...)` (única sintaxis).
*   Flags: `re.I` (IGNORECASE), `re.M` (MULTILINE), `re.S` (DOTALL), `re.X` (VERBOSE), `re.A` (ASCII), `re.U` (UNICODE, por defecto en Python 3).
*   No posee: grupos atómicos, cuantificadores posesivos, `\K`, recursión, condicionales, `\p{Unicode}`.

#### Limitaciones del lookbehind
```python
import re
re.search(r'(?<=abc|def)x', 'abcx')   # OK, longitudes iguales (3)
re.search(r'(?<=a+)x', 'aax')        # Error: look-behind requires fixed-width pattern
```

> [!WARNING]
> El módulo `re` también es bastante estricto con los escapes; no admite escapes desconocidos (como `\q`), mostrando advertencias.

#### Flags como constante de función

Se pasan a `re.compile()` o directamente a las funciones:
```python
re.findall(r'patrón', texto, re.IGNORECASE | re.DOTALL)
```

#### Modo verboso

Muy útil para patrones complejos:
```python
pattern = re.compile(r"""
    ^
    (\d{4})   # año
    -
    (\d{2})   # mes
    -
    (\d{2})   # día
    $
""", re.VERBOSE)
```

### Módulo regex (externo)

#### Instalación y compatibilidad
```bash
pip install regex
```

```python
import regex
```

Su API es casi idéntica a `re`, pero añade más capacidades. Se maneja con las mismas funciones (`search`, `match`, `findall`, `sub`), y soporta las mismas flags más algunas nuevas (`regex.VERBOSE`, etc.).

#### Nuevas características

*   Lookbehind variable sin restricciones.
*   Grupos atómicos `(?>...)`.
*   Cuantificadores posesivos `*+`, `++`.
*   Recursión `(?R)`, `(?0)`, subrutinas `(?&nombre)`.
*   Condicionales `(?(cond)si|no)`.
*   Propiedades Unicode `\p{Lu}`, `\p{Script=Latin}`.
*   `\K` para descartar lo coincidido a la izquierda.
*   Coincidencia aproximada (módulo fuzzy).
*   Flags inline `(?i)`, `(?-i)`, `(?i:...)`.

**Ejemplo de lookbehind variable en regex:**
```python
import regex
m = regex.search(r'(?<=a+)b', 'aaab')
m.group()  # 'b'
```

**Ejemplo de grupo atómico:**
```python
regex.search(r'(?>a+)b', 'aab')   # match (con aab)
regex.search(r'(?>a+)b', 'aaaa')  # None, sin backtracking
```

**Recursión:**
```python
regex.search(r'\( ( [^()] | (?R) )* \)', '( (a) (b) )', regex.X)
```

#### Modo Unicode completo

El módulo `regex` maneja Unicode de forma excelente; `\w` reconoce caracteres de palabra de cualquier alfabeto como el módulo `re` en Python 3 (por defecto Unicode), pero además `\d` también puede ser dígito Unicode si se usa la flag `regex.U` (activada por defecto) mejorada. Además `\p{...}` funciona.

### Comparación rápida re vs regex

| Característica | re | regex |
| :--- | :---: | :---: |
| **Lookbehind fijo** | ✔ | ✔ |
| **Lookbehind variable** | ✘ | ✔ |
| **Grupos atómicos** | ✘ | ✔ |
| **Posesivos** | ✘ | ✔ |
| **Recursión** | ✘ | ✔ |
| **\K** | ✘ | ✔ |
| **\p{Unicode}** | ✘ | ✔ |
| **Coincidencia aproximada** | ✘ | ✔ (fuzzy) |
| **Rendimiento (general)** | Rápido (implementación en C) | Más lento en algunas operaciones |

### Buenas prácticas en Python

*   Usa raw strings `r''` para evitar dobles escapes.
*   Prefiere `re.compile()` cuando el patrón se reutiliza.
*   Si necesitas funcionalidades avanzadas, adopta `regex`; su interfaz es compatible.
*   Para textos con Unicode, el módulo `re` ya es adecuado; para propiedades o recursión, ve a `regex`.

---

### 📖 Temas relacionados
| Archivo | Descripción |
| :--- | :--- |
| [01_comparativa_general.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/01_comparativa_general.md) | Comparativa entre motores |
| [03_JavaScript.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/03_JavaScript.md) | Regex en JavaScript |
| [05_Java.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/05_Java.md) | Regex en Java |
