# recursion_y_subrutinas.md
Concepto de recursión en regex

La recursión permite que un patrón se llame a sí mismo, de forma similar a una función recursiva en programación. Esto habilita el emparejamiento de estructuras anidadas arbitrariamente, como paréntesis balanceados, etiquetas HTML anidadas o bloques de código, algo imposible con expresiones regulares clásicas (que solo reconocen lenguajes regulares). La recursión es una extensión presente en PCRE, Perl y el módulo regex de Python.
Sintaxis de recursión

    (?R) o (?0): llama recursivamente al patrón completo.

    (?1), (?2), etc.: llama al patrón del grupo de captura número 1, 2, etc.

    (?&nombre): llama al patrón del grupo con nombre (subrutina, similar a re-ejecutar el subpatrón).

    (?P>nombre): sintaxis alternativa en Python (regex).

No confundir con las retroreferencias: una retroreferencia (\1) exige que el texto coincida exactamente con la captura previa. La recursión/subrutina re-ejecuta el patrón del grupo, permitiendo nueva coincidencia con estructura pero no forzando igualdad literal.
Ejemplo: paréntesis balanceados con (?R)

Patrón para validar y capturar contenido entre paréntesis con anidamiento ilimitado:
regex

\( (?: [^()]++ | (?R) )* \)

    \( y \) delimitan el bloque.

    [^()]++ consume uno o más caracteres que no son paréntesis (cuantificador posesivo para eficiencia).

    | (?R) recursivamente aplica todo el patrón de nuevo cuando encuentra otro paréntesis anidado.

    (?: ... )* repite la alternancia cero o más veces.

Aplicado sobre "(a (b) c)":

    Encuentra (a (b) c), capturando todo correctamente. La recursión maneja (b) internamente.

Recursión a grupos específicos

Si solo queremos repetir un subpatrón sin recursión completa:
regex

(?<word>\w+) \s+ (?&word)

Busca una palabra, espacio, y la misma palabra después (similar a una retroreferencia, pero sin capturar previamente: aquí (?&word) re-ejecuta \w+, no fuerza igualdad de texto). Para forzar igualdad usaríamos \k<word> (retroreferencia), no (?&word).

Para forzar igual estructura: (?<tag>h[1-6])>.*?</(?&tag)> casaría con <h1>...</h1> pero también con <h1>...</h2> si no usamos retroreferencia. La recursión sola no impone igualdad de texto, solo re-aplica el patrón. Para igualdad combinar con retroreferencia o capturar antes y comparar.
Subrutinas (recursión a grupos)

Una subrutina es una llamada a un grupo con nombre que ya ha aparecido antes (o después) en el patrón. Es como un "subprograma" de regex.
regex

(?<number>\d+(?:\.\d+)?) \s+ (?&number)

Coincide con un número, espacio, y otro número con el mismo formato (pero posibles valores diferentes). Si queremos mismo valor: (?<n>\d+.\d+)\s+\k<n>.
Ejemplo complejo: etiquetas HTML emparejadas (contexto simple)
regex

<(?<tag>[a-z]+)>
  (?: [^<]++ | (?R) )*
</\k<tag>>

    Captura el nombre de etiqueta en tag.

    Contenido: caracteres que no son < o recursión completa (para etiquetas anidadas).

    Cierre con retroreferencia \k<tag> para asegurar misma etiqueta.

Soporte en motores

    PCRE (PHP, Apache): (?R), (?1), (?&name) completamente soportados.

    Perl: (?R), (?1), (?&name) (moderno).

    Python regex: soporta (?R), (?0), (?1), (?&name). El módulo estándar re no.

    Java, .NET, JavaScript: no soportan recursión nativa. .NET usa grupos balanceados como alternativa. JavaScript no tiene alternativa directa.

Consideraciones importantes

    Profundidad y stack: la recursión consume pila; niveles muy profundos pueden causar error de stack overflow. PCRE2 permite ajustar el límite con (?{... no, se configura desde el código.

    Rendimiento: la recursión es potente pero puede ser lenta en estructuras grandes. Combinar con posesivos y grupos atómicos mejora.

    No es mágica: no cubre todos los casos de parseo (por ejemplo, HTML arbitrario requiere un parser real). Útil para formatos con anidamiento conocido.

Equivalencia sin recursión (grupos balanceados .NET)

En .NET, los grupos balanceados sustituyen la recursión con una pila explícita (ver sección .NET en motores). La idea es contar aperturas/cierres sin necesidad de llamada recursiva.

# condicionales.md
¿Qué son los condicionales en regex?

Son construcciones que permiten elegir entre dos (o más) patrones basándose en una condición. Sintaxis:
(?(condición)patrón-si|patrón-no)
La condición puede ser:

    Un número de grupo captura, ej. (?(1)…) (si el grupo 1 participó en la coincidencia).

    Un nombre de grupo: (?(<nombre>)…) o (?(nombre)…).

    Una aserción (lookahead o lookbehind): (?(?=…)patrón-si|patrón-no).

Condición basada en grupo existente
regex

(\+34)?(\d{9})(?(1)|(?:ERROR))

    Captura opcional de +34 en grupo 1.

    Luego dígitos.

    Condicional: si el grupo 1 existe (se capturó el prefijo), no hace nada extra (vacío después de |). Si no, intenta casar "ERROR" (o simplemente falla si no queremos match sin prefijo). Una forma más práctica: permitir formato con o sin prefijo, pero aplicar lógica.

Ejemplo real: fecha con formato flexible donde el separador debe ser consistente.
regex

(\d{4})([-/])(\d{2})\2(\d{4} | (?(1)\d{4}|\d{2}))

Patrón clásico: número de teléfono con prefijo opcional
regex

^(?:(\+34)\s?)?\d{9}(?(1)|(?=.))

Si el grupo 1 capturó +34, entonces continúa; si no, el condicional falla a menos que pongamos un patrón alternativo.
Condición con aserción
regex

(?(?=[A-Z])[A-Z]\w*|[a-z]\w*)

Si la posición actual empieza con mayúscula, usa patrón de mayúscula; si no, de minúscula. Equivalente a alternancia con lookahead, pero más elegante.
Condicionales y grupos nombrados

En PCRE, Perl, .NET, Python regex:
regex

(?<quote>['"])?(?(<quote>).*?\k<quote>|\S+)

Si se captura una comilla (simple o doble), busca contenido hasta la misma comilla. Si no, captura una palabra sin espacios.
Soporte por motor

    PCRE / PHP: condicionales completos, con grupos y aserciones.

    Perl: completo.

    Python regex: soporta grupos y aserciones; re estándar no.

    .NET: completo.

    Java, JavaScript: no soportan condicionales.

Sintaxis detallada

    (?(n)si|no) : n es el número de grupo de captura (sin escape).

    (?(<name>)si|no) o (?(name)si|no).

    (?(?=...)si|no) aserción positiva.

    (?(?!...)si|no) aserción negativa.

    Se puede omitir la rama no (dejarla vacía): (?(1)si) .

Casos de uso prácticos

    Formato de moneda condicional: si hay decimales, forzar dos dígitos; sino, número entero.
    regex

    \$(?:(\.\d{2})|(\d+))(?(1)(?=.\d{2})|\b)

    Comillas tipográficas: asegurar que citas empiecen y terminen con el mismo tipo de comilla (« » vs " ").

    Paréntesis opcionales balanceadas: (\(?\d+\)?)? ... con condicional para cerrar correctamente.

Alternativas cuando no hay soporte

En motores sin condicionales, se puede simular con una alternancia que repita partes del patrón:
regex

(\+34)?\d{9}  ->  (?:\+34\d{9}|\d{9})

Pero se pierde la capacidad de referir dinámicamente a la captura. Para lógicas más complejas, es necesario usar código huésped (dos regex separadas y una lógica if).
Precauciones

    Las condiciones pueden complicar el patrón y hacerlo menos legible; usar el modo verboso para documentar.

    Al igual que otras construcciones avanzadas, pueden aumentar el backtracking si no se acotan.

# propiedades_unicode.md
Propósito y alcance

Las propiedades Unicode permiten describir conjuntos de caracteres según sus atributos definidos en el estándar Unicode: categoría (letra, número, símbolo...), script (alfabeto), bloque (rango de códigos), y propiedades binarias (emoji, signo de puntuación, etc.). Esto posibilita la manipulación precisa de texto internacional, más allá del limitado \w ASCII.

Están disponibles en PCRE (flag u), JavaScript (flag u desde ES2018), Python con el módulo regex, Java y .NET. No en el módulo re de Python ni en POSIX.
Sintaxis general

    \p{Propiedad} : carácter con esa propiedad.

    \P{Propiedad} : carácter que NO la tiene.

    Notación larga: \p{Categoría=Valor}.

    Notación corta: \p{Valor} si no hay ambigüedad.

Categorías generales principales (General Category)

Abreviatura de una letra:

    L (Letra), M (Marca), N (Número), P (Puntuación), S (Símbolo), Z (Separador), C (Control/No asignado).

Subdivisiones más comunes (dos letras):

    Lu: Letra mayúscula (Letter, uppercase)

    Ll: Letra minúscula (Letter, lowercase)

    Lt: Letra título (Letter, titlecase)

    Lm: Letra modificadora

    Lo: Letra, otra

    Nd: Número decimal dígito (Number, decimal digit)

    Nl: Número letra (como números romanos)

    No: Número otro

    Pc: Puntuación conectiva (_)

    Pd: Guión

    Ps: Apertura paréntesis

    Pe: Cierre paréntesis

    Sc: Símbolo moneda ($, €, ¥...)

    Sk: Símbolo modificador (^, `, ¨)

    Sm: Símbolo matemático (+, =, ~)

    Zs: Espacio separador (espacio normal)

    Zl: Separador de línea

    Zp: Separador de párrafo

Ejemplos:
regex

\p{Lu}           # una mayúscula cualquiera (A, Á, Б, Ω...)
\p{Nd}+          # dígitos decimales (0-9, ٠-٩, etc.)
\p{Sc}           # cualquier símbolo monetario
\P{L}            # cualquier carácter NO letra

Scripts (alfabetos)

Especifican un sistema de escritura.

    \p{Script=Latin} o \p{Latin}

    \p{Greek}, \p{Cyrillic}, \p{Arabic}, \p{Han} (caracteres chinos), \p{Hiragana}, etc.

regex

\p{Script=Latin}+  # palabra en alfabeto latino
\p{Han}+           # secuencia de caracteres Han (chino, japonés)

Bloques Unicode (rangos)
regex

\p{Block=Basic_Latin}       # U+0000..U+007F
\p{Block=Latin_Supplement}  # U+0080..U+00FF

Útiles para limitar a un rango concreto, pero menos semántico que Script.
Propiedades binarias

Características on/off:

    \p{Emoji} : caracteres emoji.

    \p{Emoji_Presentation} : emojis que por defecto se muestran con presentación gráfica.

    \p{White_Space} : espacio en blanco (más amplio que \s en algunos motores).

    \p{Alphabetic} : letra o carácter con propiedad alfabética.

    \p{Lowercase}, \p{Uppercase}

Uso en motores

JavaScript (ES2018+)
javascript

let regex = /\p{Script=Greek}+/u;
regex.test('Σωκράτης'); // true

Siempre con flag u. Sin ella, \p{...} es un error.

Python regex
python

import regex
regex.findall(r'\p{Lu}\p{Ll}+', 'José Ángel')  # ['José', 'Ángel']

PCRE/PHP
php

preg_match('/\p{Hiragana}+/u', 'こんにちは'); // 1

Java
Se pueden usar \p{Is...} por ejemplo \p{IsLatin} para script, \p{Lu} para categoría.
Normalización Unicode y su impacto

El mismo carácter puede representarse de múltiples formas (por ejemplo, ñ = U+00F1 (NFC) o U+006E + U+0303 (NFD)). Las regex no normalizan automáticamente, por lo que \p{Ll} casaría con ñ precompuesto pero no con la secuencia n + tilde (porque n es Ll pero la tilde combina). Para evitar problemas, se debe normalizar el texto antes (por ej. text.normalize('NFC') en JS, unicodedata.normalize('NFC', text) en Python).
Coincidencia de mayúsculas/minúsculas Unicode

Con la flag i y Unicode activado, /ß/i puede coincidir con SS en algunos motores (como Perl/PCRE). Esto depende de la implementación del "case folding". Las propiedades \p{Lowercase} no se ven afectadas por la flag i (siguen distinguiendo).
Ejemplos prácticos

    Detectar texto que contiene al menos una letra mayúscula griega:
    regex

    \p{Script=Greek}*\p{Lu}\p{Script=Greek}*

    Extraer emojis de un mensaje:
    regex

    \p{Emoji_Presentation}

    Validar que un nombre de usuario no contenga caracteres de puntuación (solo letras, números y guiones bajos de cualquier alfabeto):
    regex

    ^[\p{L}\p{N}_-]+$

    Tokenizar palabras en un texto multilingüe (secuencias de letras):
    regex

    \p{L}+

Limitaciones y buenas prácticas

    Las propiedades Unicode pueden hacer la regex más larga; usa nombres significativos y modo verboso.

    No todos los motores soportan todas las propiedades; verifica la documentación.

    El módulo re de Python no soporta propiedades; usa regex.

    La normalización es responsabilidad del programador.

# backtracking_catastrofico.md
¿Qué es el backtracking?

En los motores de regex basados en NFA (la mayoría: Perl, PCRE, Java, Python, .NET, JS), cuando una parte del patrón puede casar de múltiples maneras (cuantificadores, alternancia), el motor prueba una posibilidad, y si falla más adelante, retrocede (backtrack) para intentar otra combinación. Este mecanismo es flexible pero puede degenerar en una explosión combinatoria.
El problema: backtracking catastrófico

Ocurre cuando un patrón requiere un número enorme de pasos de retroceso para determinar que no hay coincidencia, creciendo de forma exponencial con la longitud de la entrada. Esto puede causar que la aplicación se congele, consuma toda la CPU o reciba un timeout.

El ejemplo más famoso es (a+)+b aplicado a una cadena larga de as sin b al final, como "aaaaaaaaaaaaaaaaaaaaX".
Análisis detallado del ejemplo (a+)+b

    (a+)+ significa uno o más grupos de una o más as.

    Para una cadena "aaaa":

        El primer a+ puede tomar 4 as (como grupo), y el cuantificador externo + permite repetir ese grupo 1 vez. Luego espera b.

        Si b no existe, el motor puede hacer backtrack: el + externo cede caracteres, el a+ interno redistribuye.

        Número de formas de particionar las as en grupos: para 4 as, hay múltiples combinaciones (ej. 4 grupos de 1, 2+2, 1+1+2, etc.). El motor probará todas.

    Con 10 as el número de combinaciones es ~512, con 20 as ya es cientos de miles, con 30 puede ser millones o más, crecimiento exponencial.

Otros patrones problemáticos comunes

    (a|aa)+b : Explosión similar.

    .*.*=.* : Múltiples puntos greedys anidados pueden disparar backtracking interno.

    [^,]*,[^,]*,[^,]* con entrada que tiene menos comas de las esperadas.

    (".*?"|'.*?') cuando hay muchas comillas en el texto y no está ordenado.

Cómo identificarlos

Síntomas:

    Regex extremadamente lentas con ciertas entradas (aunque sean cortas).

    Falla con timeout en validadores online.

    Herramientas como regex101.com muestran el número de pasos; si es excesivo (> 1000 para entradas simples).

    Buscar patrones con cuantificadores anidados (...+)+, (...*)*, (.+?) dentro de grupos que se repiten.

Estrategias para prevenir y solucionar

    Cuantificadores posesivos (++, *+, ?+, {n,m}+): eliminan el backtracking dentro del cuantificador. Una vez que coinciden, no ceden caracteres.
    regex

    (a++)+b  // en "aaaaX" falla inmediatamente

    Grupos atómicos (?>…): igual que posesivos, pero aplicado a un grupo más complejo.
    regex

    (?>a+)+b

    Reescribir el patrón eliminando anidamiento innecesario. En lugar de (a+)+b, usar a+b (sin anidar) cuando sea posible.

    Usar clases negadas en lugar de puntos perezosos: [^"]* en vez de .*? para contenido entre comillas.

    Limitar cuantificadores sin límite: cuando se pueda, usar {1,100} en lugar de * o + sin cota.

    Aprovechar anclas para fallar temprano: ^…$.

    Reordenar alternancias: poner la opción más probable o la que casa menos primero puede reducir retrocesos.

    Lookaheads para restringir sin consumir, ej. (?=[a-z]+\d)[a-z0-9]+ puede evitar backtrack.

Herramientas de diagnóstico

    regex101.com: en el panel "debugger" muestra paso a paso y cuenta los pasos. Avisa con "catastrophic backtracking" si detecta patrón peligroso.

    Node.js: uso de la librería re2 (más segura, sin backtracking) o limitar tiempo con safe-regex.

    Python regex: permite poner límite de tiempo (regex.match(pattern, text, timeout=1)).

Ejemplo práctico: extraer campos CSV evitando backtracking

Patrón inseguro: (?:[^;]*;)+ con entrada larga sin punto y coma al final.
Seguro: [^;]*+(?:;[^;]*+)*+ usando posesivos, o usar split a nivel de código.
Impacto en entornos de producción

Un servidor web que valida entradas de usuario con una regex vulnerable puede ser blanco de un ataque ReDoS (Regular expression Denial of Service). Por eso en aplicaciones críticas se evitan patrones complejos no acotados o se usan motores alternativos como RE2/Hyperscan (garantizados en tiempo lineal).
Conclusión

Conocer el backtracking catastrófico es vital para escribir regex robustas. Ante patrones complejos, siempre pensar en el peor caso y utilizar las herramientas de optimización (posesivos, atómicos, reestructuración) para mantener el rendimiento predecible.

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

