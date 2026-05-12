# optimizacion.md
Principios generales de rendimiento en regex

Escribir una regex que funcione es solo el primer paso. La eficiencia puede ser crucial cuando se procesan grandes volúmenes de texto o en aplicaciones interactivas. La optimización busca reducir el número de pasos de backtracking, evitar reevaluaciones innecesarias y aprovechar las características de cada motor.
Técnicas de optimización
1. Evitar el punto (.) cuando sea posible

El punto casa con casi cualquier cosa, y los cuantificadores con punto (.*, .+) a menudo obligan a retroceder. Prefiere clases negadas:
regex

"([^"]*)"      # en lugar de ".*?"
<([^>]*)>      # en lugar de <.*?>

Las clases negadas son más eficientes porque no necesitan expandirse paso a paso; consumen de una vez todo hasta el delimitador.
2. Usar cuantificadores posesivos o grupos atómicos

Cuando sabes que un cuantificador no debe ceder caracteres, aplica posesivo (*+, ++) o envuélvelo en un grupo atómico (?>…). Esto elimina los estados de retroceso internos.
regex

\w++@\w++\.\w++   # partes de email imposibles de anidar
(?>".*?")?        # grupo atómico para contenido opcional

3. Anclar siempre que se pueda

Usar ^ al inicio y $ al final ancla el patrón a los bordes, evitando que el motor pruebe en todas las posiciones intermedias si no es necesario.
regex

^\d{5}(?:-\d{4})?$       # código postal EEUU

Si la regex no necesita anclas porque va dentro de split o se usa con findall, considera si se puede restringir con \b u otras aserciones.
4. Orden de alternancia: pon primero lo más probable o lo más específico
regex

a(bc|bcd)   # probará "bc", si falla, "bcd". Si "bcd" es la común, pon primero "bcd" o mejor (bc|bcd) no, reescribe.

Mejor: b(cd|d)? o factorizar.
5. Factorizar patrones comunes
regex

(abc|abd|abe)  →  ab(c|d|e)

Agrupar prefijos comunes reduce repetición de comprobación.
6. Usar \K en lugar de lookbehind largo

En PCRE y Python regex, \K descarta lo coincidido a la izquierda. Puede ser más eficiente que lookbehind positivo de longitud variable, porque el motor no necesita simular hacia atrás desde cada posición.
regex

€\K\d+\.\d+    # más rápido que (?<=€)\d+\.\d+

7. Limitar los cuantificadores

Si sabes el máximo razonable, por ejemplo, una línea no excederá 200 caracteres: .{0,200} en lugar de .*. Reduce el universo de backtracking.
8. Evitar el flag m si no es necesario

El modo multilínea añade más posiciones de ^ y $, lo que puede aumentar el número de intentos. Si solo procesas una cadena simple, desactívalo.
9. Compilar el patrón una vez, reutilizarlo

En lenguajes como Java, C#, Python, compilar el regex con Pattern.compile / re.compile evita reparsear la expresión cada vez, especialmente si se usa en bucles.
10. Elegir las funciones adecuadas

    Si solo compruebas si existe, usa test() (JS), containsMatch (Java), re.search() (Python) en lugar de extraer todas las coincidencias.

    Si solo quieres la primera coincidencia, no uses findall.

11. Usar modo no captura (?:…) cuando no necesites referencias

Cada grupo de captura consume memoria y tiempo. Emplea (?:…) para agrupar sin capturar.
12. Aprovechar las capacidades del motor

    En .NET, RegexOptions.Compiled genera código IL y acelera la ejecución (a costa de tiempo de inicialización).

    En Java, Pattern.compile cachea si se llama repetidamente; no es necesario un Map estático en la mayoría de JVMs modernas.

    En Python, re.compile es útil, pero el módulo también cachea internamente las últimas regex usadas.

13. Usar \b y límites inteligentes

Los límites de palabra fallan rápido si la posición no es adecuada, ahorrando intentos.
Evaluación de rendimiento

    Mide con conjuntos de datos representativos.

    En JavaScript, console.time alrededor de las operaciones.

    En Python, timeit.

    En regex101, mira "steps" en el debugger.

    Si un patrón tarda demasiado, considera si una solución sin regex (split, indexOf, startsWith) es más apropiada para el caso simple. Muchas veces, código imperativo es más rápido y claro que una regex compleja.

Cuándo no usar regex

    Parseo de formatos anidados complejos (HTML, JSON, XML completos) → usa parsers específicos.

    Tareas muy simples como "hola".startsWith("ho") → funciones de cadena.

    Validaciones de reglas de negocio cambiantes → la lógica en código puede ser más mantenible que una macro regex de 100 líneas.

Ejemplo de optimización real

Caso: extraer todas las palabras de un texto en inglés, ignorando puntuación.
regex

// No óptimo
\b\w+\b

// Mejor (si \w es suficiente)
\w+

// Pero si queremos capturar contracciones (don't), necesitamos ajustes
[a-zA-Z]+(?:'[a-zA-Z]+)?

Usar [a-zA-Z]+ (sin Unicode) es más rápido si solo hay ASCII.

Caso: validar un número decimal con coma como separador de miles y punto decimal (1.234,56).
Patrón ineficiente: ^\d{1,3}(?:\.\d{3})*,\d{2}$ puede backtrack si la entrada no coincide. Hacerlo posesivo: ^\d{1,3}(?:\.\d{3})*+,\d{2}$ si se soporta, o usar un grupo atómico: ^\d{1,3}(?>(?:\.\d{3})*),\d{2}$.
Resumen de buenas prácticas

    Di NO al punto perezoso cuando puedas usar clase negada.

    Usa posesivos/atómicos en patrones anidados o con alternancia.

    Compila y reutiliza.

    Ancla para fallar rápido.

    Mide y prueba con inputs extremos (largos, mal formados).

    Mantén las regex tan simples como sea posible, dividiendo problemas complejos en varias etapas si es necesario.

