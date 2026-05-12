# 📁 Fundamentos: ¿Qué es una Regex?

## 📌 ¿Qué es una expresión regular?

Una expresión regular (**regex** o **regexp**) es una secuencia de caracteres que define un patrón de búsqueda. Se utiliza para encontrar, validar, extraer o modificar cadenas de texto. Con una única expresión podemos describir un conjunto potencialmente infinito de combinaciones que comparten una misma estructura.

## 📌 Fundamento teórico

Las expresiones regulares tienen su origen en la teoría de autómatas y los lenguajes formales. En ciencia de la computación, un **lenguaje regular** es aquel que puede ser reconocido por una máquina de estados finitos (determinista o no determinista, DFA/NFA). Toda expresión regular define un lenguaje regular.

Steven Kleene formalizó la notación en la década de 1950. Hoy en día, los motores de regex modernos extienden esta teoría con capacidades que van más allá de los lenguajes estrictamente regulares (por ejemplo, retroreferencias y recursión), lo que los hace más potentes pero también abre puertas a problemas de rendimiento.

> [!WARNING]
> El uso de extensiones modernas (como retroreferencias) puede llevar a problemas de rendimiento conocidos como **backtracking catastrófico**.

## 📌 Partes de una regex

- **Literales:** Caracteres que coinciden consigo mismos (ej. `a`, `1`, `@`).
- **Metacaracteres:** Símbolos con significado especial (`. ^ $ * + ? { } [ ] \ | ( )`).
- **Cuantificadores:** Indican cuántas veces debe aparecer un elemento.
- **Clases de caracteres:** Conjuntos o rangos entre corchetes `[...]`.
- **Anclas:** Posiciones sin consumo de caracteres (`^`, `$`, `\b`).
- **Grupos y captura:** Paréntesis para agrupar y recordar subcoincidencias.
- **Aserciones de ancho cero:** Lookahead y lookbehind.

## 📌 ¿Para qué se usan?

- Validación de formularios (email, teléfono, DNI).
- Extracción de datos de logs, scraping básico.
- Transformación de texto (reemplazar formatos, limpiar espacios).
- Resaltado de sintaxis en editores de código.
- Enrutamiento de URLs en frameworks web.
- Análisis léxico en compiladores e intérpretes.

## 📌 Motores y dialectos

No todas las regex son iguales. Existen varios dialectos según el motor que las procesa:

| Motor | Presente en | Características destacadas |
| :--- | :--- | :--- |
| **PCRE** | Perl, PHP, Apache, Python (módulo regex) | Recursión, grupos atómicos, lookbehind variable, subrutinas |
| **ECMAScript** | JavaScript moderno | Lookbehind (ES2018), propiedades Unicode `\p{}`, `\k` para grupos con nombre |
| **Python re** | Python estándar | Limitado: sin lookbehind variable, sin grupos atómicos |
| **.NET** | C#, PowerShell | Lookbehind variable, grupos balanceados para anidamiento |
| **Java** | `java.util.regex` | Grupos atómicos, lookbehind finito |
| **POSIX (ERE/BRE)** | `grep`, `sed`, `awk` | Muy básico, sin retroreferencias ni aserciones |

## 📌 Sintaxis genérica de una regex

Generalmente se escribe entre delimitadores `/patrón/flags` en JavaScript y Perl, o como cadena cruda `r'patrón'` en Python. Las banderas (`i`, `g`, `m`, `s`) modifican el comportamiento global.

### 🔹 Ejemplo conceptual

```text
/^([A-Z][a-z]+)\s(\d{2,4})$/gm
```

- `^`: inicio de línea
- `([A-Z][a-z]+)`: captura palabra que empieza con mayúscula
- `\s`: espacio
- `(\d{2,4})`: captura número de 2 a 4 dígitos
- `$`: fin de línea
- **Bandera** `m` (multilínea), `g` (global)

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| ➖ | [Índice](../README.md) | [Metacaracteres](02_metacaracteres.md) |
