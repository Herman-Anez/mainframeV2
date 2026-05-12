# Optimización de Rendimiento

Escribir una regex que funcione es solo el primer paso. La eficiencia es crucial cuando se procesan grandes volúmenes de texto o en aplicaciones interactivas. La optimización busca reducir el número de pasos de backtracking, evitar reevaluaciones innecesarias y aprovechar las características específicas de cada motor.

## Técnicas de optimización

### 1. Evitar el punto (`.`) cuando sea posible
El punto coincide con casi cualquier carácter, y los cuantificadores con punto (`.*`, `.+)`) a menudo obligan a realizar backtracking excesivo. Prefiere el uso de **clases negadas**:

```regex
"([^"]*)"      # Eficiente: en lugar de ".*?"
<([^>]*)>      # Eficiente: en lugar de <.*?>
```
Las clases negadas son más rápidas porque el motor no necesita expandirse paso a paso; consumen de una vez todo el texto hasta encontrar el delimitador.

### 2. Usar cuantificadores posesivos o grupos atómicos
Cuando se sabe que un cuantificador no debe ceder caracteres para que el resto del patrón coincida, aplica un **posesivo** (`*+`, `++`) o envuélvelo en un **grupo atómico** (`(?>…)`). Esto elimina los estados de retroceso innecesarios.

```regex
\w++@\w++\.\w++   # Partes de email imposibles de anidar
(?>".*?")?        # Grupo atómico para contenido opcional
```

### 3. Anclar siempre que sea posible
Usar `^` al inicio y `$` al final ancla el patrón a los bordes de la cadena, evitando que el motor intente buscar coincidencias en todas las posiciones intermedias.

```regex
^\d{5}(?:-\d{4})?$       # Código postal (EE.UU.)
```
> [!TIP]
> Si la regex se usa dentro de `split()` o `findall()`, considera si puedes restringir las posiciones con límites de palabra (`\b`) u otras aserciones.

### 4. Orden de alternancia: Lo más probable primero
Coloca primero la opción más frecuente o la más específica dentro de una alternancia para que el motor termine antes en el caso de éxito.
```regex
# En lugar de a(bc|bcd), usa:
a(bcd|bc)   # O mejor: abcd?
```

### 5. Factorizar patrones comunes
Agrupar prefijos comunes reduce la repetición de comprobaciones por parte del motor:
```regex
(abc|abd|abe)  →  ab(c|d|e)
```

### 6. Usar `\K` en lugar de lookbehind largo
En PCRE y el módulo `regex` de Python, `\K` descarta lo coincidido a la izquierda de su posición. Es más eficiente que un lookbehind de longitud variable.
```regex
€\K\d+\.\d+    # Más rápido que (?<=€)\d+\.\d+
```

### 7. Limitar los cuantificadores
Si conoces el máximo razonable de caracteres, úsalo en lugar de cuantificadores infinitos: `.{0,200}` es preferible a `.*` si sabes que la línea no excederá los 200 caracteres.

### 8. Evitar el flag `m` (multilínea) si no es necesario
El modo multilínea añade más posiciones posibles para `^` y `$`, lo que puede aumentar el número de intentos de búsqueda.

### 9. Compilar y reutilizar el patrón
En lenguajes como Java, C# o Python, compilar la expresión con `Pattern.compile` o `re.compile` evita el coste de parsear el patrón en cada ejecución, especialmente dentro de bucles.

### 10. Elegir las funciones adecuadas
*   Si solo necesitas saber si hay coincidencia: usa `test()` (JS) o `re.search()` (Python) en lugar de extraer el contenido.
*   Si solo buscas la primera coincidencia: evita `findall()` o flags globales innecesarios.

### 11. Usar grupos de no captura `(?:…)`
Cada grupo de captura consume memoria y tiempo de CPU para almacenar la referencia. Emplea `(?:…)` para agrupar sin capturar cuando no necesites extraer esa parte.

### 12. Aprovechar capacidades específicas del motor
*   **.NET:** `RegexOptions.Compiled` genera código IL y acelera la ejecución.
*   **Java:** `Pattern.compile` cachea internamente; no suele ser necesario implementar un cache propio.
*   **Python:** El módulo `re` también cachea internamente las últimas regex utilizadas.

### 13. Usar `\b` y límites inteligentes
Los límites de palabra fallan rápidamente si la posición no es la adecuada, ahorrando muchos pasos de procesamiento.

## Evaluación de rendimiento

> [!IMPORTANT]
> **Herramientas de medición:**
> *   **Mide con datos reales:** No confíes solo en la teoría; usa volúmenes de datos representativos.
> *   **JavaScript:** Usa `console.time()` y `console.timeEnd()`.
> *   **Python:** Usa el módulo `timeit`.
> *   **regex101:** Observa el contador de **"steps"** en el debugger.

## Cuándo no usar regex

> [!CAUTION]
> No intentes resolverlo todo con expresiones regulares:
> *   **Formatos anidados:** Para HTML, JSON o XML completos, usa un parser específico.
> *   **Tareas triviales:** `startsWith()`, `endsWith()` o `indexOf()` son siempre más rápidas que una regex para comprobaciones literales.
> *   **Lógica de negocio compleja:** Si la regex supera las 100 líneas, la lógica imperativa en código suele ser más mantenible y eficiente.

## Ejemplo de optimización real

### Caso: Extraer palabras ignorando puntuación
```regex
// No óptimo
\b\w+\b

// Mejor
\w+

// Soporte para contracciones (ej. "don't")
[a-zA-Z]+(?:'[a-zA-Z]+)?
```
*Nota: Usar `[a-zA-Z]` es más rápido que `\w` si solo esperas caracteres ASCII.*

### Caso: Validar número decimal con separadores
*   **Ineficiente:** `^\d{1,3}(?:\.\d{3})*,\d{2}$` (puede causar backtracking en fallos).
*   **Eficiente:** `^\d{1,3}(?:\.\d{3})*+,\d{2}$` (posesivo) o `^\d{1,3}(?>(?:\.\d{3})*),\d{2}$` (grupo atómico).

## Resumen de buenas prácticas

> [!TIP]
> 1.  **Dile NO al punto perezoso** cuando puedas usar una clase negada.
> 2.  **Usa posesivos/atómicos** en patrones anidados o con alternancia.
> 3.  **Compila y reutiliza** tus patrones.
> 4.  **Ancla tus expresiones** para fallar rápido ante entradas incorrectas.
> 5.  **Mide y prueba** con casos extremos (inputs muy largos o mal formados).
> 6.  **Divide y vencerás:** Divide problemas complejos en varias etapas de procesamiento si es necesario.

---

### 📖 Temas relacionados
| Archivo | Descripción |
| :--- | :--- |
| [04_backtracking_catastrofico.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/07_temas_avanzados/04_backtracking_catastrofico.md) | Riesgos de rendimiento crítico |
| [06_motores_y_dialectos](../06_motores_y_dialectos/01_comparativa_general.md) | Diferencias de rendimiento por motor |
| [01_fundamentos](../01_fundamentos/01_caracteres_literales.md) | Conceptos base de optimización |

