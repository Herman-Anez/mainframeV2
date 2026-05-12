# comparativa_general.md
## El ecosistema de los motores de regex

No existe una única implementación de expresiones regulares. Cada lenguaje de programación o herramienta utiliza un motor de regex que interpreta los patrones y los ejecuta contra las cadenas. Estos motores difieren en sintaxis, características avanzadas y rendimiento. Conocer las diferencias es esencial para escribir patrones portables o aprovechar al máximo cada entorno.

### Principales familias de motores

| Motor | Ejemplos de uso | Tipo | Observaciones |
| :--- | :--- | :--- | :--- |
| **PCRE (Perl Compatible Regular Expressions)** | PHP, Apache, Python (módulo regex), diversos | Backtracking con muchas extensiones | Muy completo; posee recursión, subrutinas, verbos de control. |
| **ECMAScript** | JavaScript, navegadores, Node.js | Backtracking | Mejorado significativamente desde ES2018; aún carece de grupos atómicos, posesivos y recursión. |
| **Python re** | Biblioteca estándar de Python | Backtracking | Más limitado; lookbehind fijo, sin grupos atómicos, sin `\p{}`. |
| **Python regex** | Módulo externo PyPI | Backtracking avanzado | Similar a PCRE; soporta Unicode completo, recursión, etc. |
| **Java java.util.regex** | Java | Backtracking | Grupos atómicos, posesivos, lookbehind con límite máximo, propiedades Unicode. |
| **.NET** | C#, VB.NET, PowerShell | Backtracking | Extremadamente potente: lookbehind variable, grupos balanceados, ejecución derecha-izquierda. |
| **POSIX (BRE/ERE)** | grep, sed, awk | Autómata finito (sin retrocesos para referencias) | Muy básico; sin aserciones, sin cuantificadores perezosos; backreferences solo en BRE. |

### Tabla comparativa de características

| Característica | PCRE | JS (ES2024) | Python re | Python regex | Java | .NET | POSIX |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Lookahead (?= ) / (?! )** | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✘ |
| **Lookbehind (?<= ) / (?<! )** | ✔ (variable en PCRE2) | ✔ (variable) | ✔ (solo fijo) | ✔ (variable) | ✔ (longitud máxima finita) | ✔ (variable) | ✘ |
| **Grupos atómicos (?> )** | ✔ | ✘ | ✘ | ✔ | ✔ | ✔ | ✘ |
| **Cuantificadores posesivos *+, ++** | ✔ | ✘ | ✘ | ✔ | ✔ | ✔ | ✘ |
| **Grupos con nombre** | `(?<name>...)` / `(?'name'...)` | `(?<name>...)` | `(?P<name>...)` | `(?P<name>...)` / `(?<name>...)` | `(?<name>...)` | `(?<name>...)` / `(?'name'...)` | ✘ |
| **Recursión (?R) / (?0)** | ✔ | ✘ | ✘ | ✔ | ✘ | ✘ (se logra con balanceo) | ✘ |
| **Subrutinas (?&name)** | ✔ | ✘ | ✘ | ✔ | ✘ | ✘ | ✘ |
| **Condicionales (?(cond)si|no)** | ✔ | ✘ | ✘ | ✔ | ✘ | ✔ | ✘ |
| **Propiedades Unicode \p{...}** | ✔ (con flag u) | ✔ (ES2018+) | ✘ | ✔ | ✔ (desde Java 1.7) | ✔ | ✘ |
| **Modo verboso / comentarios** | ✔ | ✘ | ✔ | ✔ | ✔ | ✔ (opción IgnorePatternWhitespace) | ✘ |
| **Backreferences \1** | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Solo BRE |
| **\K (keep out)** | ✔ | ✘ | ✘ | ✔ | ✘ | ✘ | ✘ |
| **Verbos de control (*SKIP)(*F)** | ✔ | ✘ | ✘ | ✔ | ✘ | ✘ | ✘ |

### Factores que determinan la elección

*   **Portabilidad**: si el patrón debe funcionar en distintos lenguajes (ej. front y back), adhiérete al subconjunto común: lookahead, grupos, retroreferencias básicas, clases.
*   **Potencia**: para tareas complejas (balanceo de paréntesis, análisis léxico), elige PCRE, .NET o Python regex.
*   **Rendimiento**: los motores con backtracking pueden sufrir patrones catastróficos. Los motores DFA (POSIX) o híbridos optimizan, pero sacrifican funcionalidades.
*   **Disponibilidad**: en el navegador solo tienes JavaScript; en servidores PHP o Perl, PCRE es nativo; en Java y .NET, sus propias bibliotecas.

### Historia y evolución

*   **POSIX**: Primera estandarización (BRE/ERE). Muy limitado, aún presente en herramientas del sistema.
*   **Perl 5**: Revolucionó las regex añadiendo muchas extensiones; de ahí nació PCRE.
*   **PCRE**: Se convirtió en el estándar de facto para servidores, Apache, PHP.
*   **JavaScript**: Por mucho tiempo ignorado, pero desde ES2015/ES2018 ha incorporado lookbehind, unicode, grupos nombrados.
*   **Python**: La estándar re no ha evolucionado mucho; el módulo regex rellena los huecos.
*   **Java y .NET**: Cada uno con sus propias extensiones originales (balanceo en .NET, longitud finita en Java).

---

### 📖 Temas relacionados
| Archivo | Descripción |
| :--- | :--- |
| [02_PCRE.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/02_PCRE.md) | Detalles del motor PCRE |
| [03_JavaScript.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/03_JavaScript.md) | Regex en el ecosistema ECMAScript |
| [04_Python.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/04_Python.md) | El módulo re y regex de Python |
| [05_Java.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/05_Java.md) | Implementación de java.util.regex |
| [06_NET.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/06_NET.md) | Potencia de regex en .NET |
| [07_POSIX.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/07_POSIX.md) | Estándares BRE y ERE |


---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| ➖ | [🏠 Inicio](../../README.md) | [Pcre ▶](02_PCRE.md) |
