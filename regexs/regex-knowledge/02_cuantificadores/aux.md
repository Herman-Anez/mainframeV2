
# greedy_lazy.md
¿Qué son los cuantificadores?

Los cuantificadores especifican cuántas veces debe aparecer el elemento inmediatamente anterior (un carácter, una clase o un grupo). Son los mecanismos para expresar repetición.

Lista de cuantificadores estándar:

    * → cero o más veces (equivalente a {0,})

    + → una o más veces ({1,})

    ? → cero o una vez ({0,1})

    {n} → exactamente n veces

    {n,} → n o más veces

    {n,m} → entre n y m veces inclusive

Ejemplos básicos:
regex

a*      -> "", "a", "aa", "aaa"...
a+      -> "a", "aa", "aaa"... (pero no "")
a?      -> "" o "a"
a{3}    -> "aaa"
a{2,4}  -> "aa", "aaa", "aaaa"

Modo por defecto: Codicioso (Greedy)

Todos los cuantificadores son codiciosos por defecto. Esto significa que intentan consumir la mayor cantidad posible de caracteres sin impedir que la expresión completa tenga éxito.

Por ejemplo, con la regex .* sobre el texto "abc def ghi", el motor:

    Empieza en la posición 0.

    .* consume todos los caracteres hasta el final de la cadena.

    Luego intenta continuar con el resto del patrón (si lo hubiera). Si falla, retrocede (backtrack) cediendo caracteres de derecha a izquierda hasta que el patrón global coincida.

Ejemplo clásico:
regex

a.*b

Texto: "aabab"

    Proceso greedy:

        a coincide con el primer carácter 'a'.

        .* consume el resto: "abab".

        Intenta casar b al final, pero la cadena se acabó.

        Backtrack: .* cede el último b, ahora .* = "aba", queda b al final. b coincide con ese b final.

        Coincidencia total: "aabab".

Observa cómo tomó la máxima porción antes de retroceder. El resultado es la coincidencia más larga posible que satisface todo el patrón.

Otro ejemplo con ".+":
regex

".+"

Sobre "primero" y "segundo":

    Greedy .+ consume desde la primera comilla hasta la última comilla, resultando en "primero" y "segundo". Normalmente no es lo deseado; queremos la primera frase entrecomillada.

Modo Perezoso (Lazy)

Al añadir un signo ? después del cuantificador, se vuelve perezoso. El cuantificador perezoso intenta consumir la menor cantidad posible de caracteres para que el patrón global tenga éxito.

Lista de cuantificadores perezosos:
text

*?      -> cero o más, lo mínimo
+?      -> una o más, lo mínimo
??      -> cero o una, prefiere cero
{n,}?   -> n o más, lo mínimo
{n,m}?  -> entre n y m, el menor número

Mecanismo:

    El motor expande el cuantificador perezoso paso a paso: primero intenta con cero repeticiones (o la mínima), y si el resto del patrón falla, expande una repetición y lo vuelve a intentar, hasta lograr la coincidencia global o agotar las posibilidades.

Ejemplo (mismo caso anterior):
regex

a.*?b

Texto: "aabab"

    Primera coincidencia:

        a coincide con el primer 'a' en la posición 0.

        .*? intenta coincidir con la mínima: cero caracteres. Ahora el cursor está justo después de ese 'a', queda "abab".

        Intenta casar b con el siguiente carácter, que es 'a', falla.

        .*? se expande una vez: consume 'a'. Tenemos "aa" consumido (a.*? = aa). Restante: "bab".

        Intenta b con el siguiente carácter: 'b' en "bab", éxito. Coincidencia: "aab".

        El motor devuelve "aab", la coincidencia más corta posible.

Si usamos la flag global, la siguiente coincidencia empezaría después: sobre "ab" encontraría "ab".

Ejemplo para ".+?" en "primero" y "segundo":
regex

".+?"

Coincide con "primero" (la primera comilla y la mínima cantidad de caracteres hasta la siguiente comilla). Así extraemos frases entrecomilladas individualmente.
Comparativa de comportamiento

Texto: <p>Hola</p> <p>Mundo</p>
Regex greedy: <.*>
Coincidencia: <p>Hola</p> <p>Mundo</p> (todo, desde el primer < hasta el último >).

Regex lazy: <.*?>
Primera coincidencia: <p>, luego </p>, luego <p>, luego </p>. Ideal para capturar etiquetas individuales.
¿Cuándo usar cada uno?

    Greedy: cuando queremos consumir todo hasta la última ocurrencia de un delimitador. Ejemplo: ^.*: encontrará todo hasta el último : de la línea.

    Lazy: cuando queremos detenernos en la primera ocurrencia. Ejemplo: extraer contenido entre paréntesis: \(.*?\).

Riesgos del backtracking excesivo

Los cuantificadores anidados o combinados pueden llevar a un backtracking catastrófico si la cadena no coincide. Ejemplo clásico: (a+)+b con entrada "aaaaaaaaaaaaaaaaaaaaaaaaaaaaac". El motor explora combinaciones exponenciales. Los cuantificadores perezosos también pueden sufrir backtracking, aunque a veces reducen el problema. La solución son los cuantificadores posesivos (ver siguiente sección) o grupos atómicos.

# posesivos.md
Definición y sintaxis

Los cuantificadores posesivos son una extensión presente en algunos motores (PCRE, Java, .NET, Perl, módulo regex de Python). Se forman añadiendo un + después del cuantificador normal.

Lista:
text

*+     -> cero o más, posesivo
++     -> una o más, posesivo
?+     -> cero o una, posesivo
{n,}+  -> n o más, posesivo
{n,m}+ -> entre n y m, posesivo

Comportamiento

Un cuantificador posesivo consume la máxima cantidad posible de caracteres, igual que el greedy, pero con una diferencia crucial: nunca retrocede (backtrack). Una vez que toma una porción, no la devuelve aunque eso impida que el resto del patrón coincida.

Esto significa que si el resto de la expresión falla, el motor no intentará ceder caracteres del cuantificador posesivo; simplemente fallará esa rama de la búsqueda y continuará probando desde otras posiciones (backtrack global), pero sin reajustar el interior del cuantificador.

Ejemplo:
regex

a++b

Sobre "aaaab":

    a++ consume todas las as (4 as).

    Luego intenta coincidir b, pero el carácter siguiente es b → éxito, coincide "aaaab".

Sobre "aaaa":

    a++ come todas las as (4 as).

    Luego intenta b, pero no hay más caracteres. Como el cuantificador es posesivo, no retrocede para ceder as. Fallo global inmediato. Con un greedy normal a+b, el motor cedería una a, probaría b, cedería otra, etc., generando backtracking que finalmente falla igual, pero con coste computacional.

Ventajas

    Eficiencia y prevención de backtracking catastrófico: Al eliminar estados de retroceso interiores, se reduce drásticamente el número de intentos. Es una herramienta de optimización.

    Seguridad: En patrones complejos donde sabemos que no queremos que el cuantificador ceda, el posesivo garantiza que no habrá retroceso, evitando bucles infinitos.

Caso de uso típico: cuantificadores anidados

El patrón (?:a+)*b sobre "aaaaaaaaaaaaaaac" sufre backtracking exponencial. Si usamos un grupo atómico o cuantificadores posesivos en el interior (?:a++)*b (o (?>a+)*b), el motor falla mucho más rápido porque no retrocede dentro de a+ para intentar distribuciones alternativas.

Ejemplo real: Validar que una cadena no contiene ciertos patrones puede requerir cuantificadores posesivos para ser eficiente.
Soporte en motores

    PCRE / PHP: *+, ++, etc. disponibles.

    Perl: Soportados.

    Java: Soportados.

    .NET: Soportados.

    Python: El módulo re estándar NO soporta cuantificadores posesivos. El módulo externo regex (PyPI) sí los soporta.

    JavaScript (ECMAScript): NO los soporta. No hay sintaxis disponible. Se pueden simular usando grupos atómicos (que tampoco están soportados) o mediante trucos con lookahead.

Simulación en motores que no los soportan

Si necesitas un comportamiento posesivo en JS o Python re, puedes usar un grupo atómico (si está disponible) o una construcción de lookahead:

Para a++b sin posesivo, la equivalencia sería (?=a+)\1b, pero solo en motores con retroreferencias. Sin embargo, no es exactamente igual; en casos complejos es mejor reestructurar la lógica.

Otra opción: usar (?>a+)b (grupo atómico), pero en JS esto no existe. En JavaScript, un truco para a++b podría ser (?=(a+))\1b. El lookahead captura las as y la retroreferencia las consume sin posibilidad de retroceder en el grupo externo (porque la retroreferencia es una coincidencia fija). Esto imita parcialmente el posesivo.
Precauciones

Los cuantificadores posesivos pueden cambiar la semántica. Si la coincidencia global podría lograrse cediendo caracteres del cuantificador, un posesivo lo impedirá. Solo deben usarse cuando sabemos que no se necesita tal cesión.

Ejemplo patrón: ".*+" nunca coincidiría con "hola" porque .*+ consumiría todo hasta el final, incluyendo la comilla de cierre, y luego no podría retroceder para que la comilla final case. Mientras que el greedy ".*" sí lo haría. El posesivo aquí es inadecuado.

# ejemplos_practicos.md

A continuación, ejemplos que muestran la aplicación real de cuantificadores codiciosos, perezosos y posesivos, con explicaciones paso a paso.
1. Extracción de etiquetas HTML

Objetivo: Obtener el contenido entre etiquetas <strong>...</strong>.

Texto: Este es <strong>un texto</strong> importante y <strong>otro</strong> más.

    Greedy incorrecto: <strong>.*</strong>
    Coincidencia: "<strong>un texto</strong> importante y <strong>otro</strong>"
    El .* consume todo hasta el último </strong>. Malo si queremos capturas individuales.

    Lazy correcto: <strong>.*?</strong>
    Coincidencias (global): <strong>un texto</strong> y <strong>otro</strong>.
    .*? se detiene en el primer </strong>.

    Posesivo inadecuado: <strong>.*+</strong>
    El .*+ consumiría todo el resto del documento y nunca encontraría el </strong>, fallando por completo.

2. Validación de números de teléfono con formato flexible

Requerimiento: Dígitos, posible guiones o espacios como separadores, longitud total controlada.

Regex: ^[\d]+([\s-]?[\d]+)*$

    [\d]+ uno o más dígitos al inicio.

    Grupo ([\s-]?[\d]+)* cero o más bloques de opcional separador + dígitos.
    Funciona bien con greedy, pero puede tener backtracking con entradas como "123-456-7890" que son válidas.

Si se aplica un cuantificador posesivo: ^[\d]++([\s-]?+[\d]++)*+$ para optimizar y asegurar que no retroceda en dígitos. (Sólo en motores con soporte)
3. Manejo de cadenas entre comillas escapadas

Problema: Extraer cadenas delimitadas por comillas dobles, donde dentro puede haber comillas escapadas \".

Texto: "hola \"mundo\" bien" "adiós"

Patrón greedy básico: "(.*?)" sólo coge "hola \" (porque la primera comilla de cierre está después de hola \). Necesitamos ignorar comillas escapadas.

Solución robusta con perezoso y alternancia:
regex

"([^"\\]|\\.)*?"

Explicación:

    " comilla inicial.

    ([^"\\]|\\.)*? cero o más veces (perezoso) de:

        [^"\\] cualquier carácter que no sea comilla ni barra.

        \\. barra invertida seguida de cualquier carácter (captura escapados).

    " comilla final.

Al usar *? nos aseguramos que se detenga en la primera comilla no escapada.
4. Log parsing: extracción de direcciones IP del primer campo

Línea de log: 192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /page HTTP/1.1" 200 2326

Para extraer la IP: ^(\S+).

    ^ inicio de línea.

    \S+ uno o más caracteres no espacio (greedy, pero como \S no puede cruzar espacios, no hay riesgo).

    Captura la IP eficientemente.

Si hubiese riesgo de backtracking, podríamos usar posesivo \S++ en motores que lo permitan, pero no es necesario porque la clase negada no puede match espacio.
5. Búsqueda de comentarios multilínea /* ... */

Texto con código:
text

int a; /* comentario
   multilínea */ int b; /* otro */

Patrón perezoso: /\*.*?\*/ funciona porque .*? se expande hasta encontrar */. Pero con la flag s (DOTALL) para que . incluya saltos de línea.

Sin embargo, puede haber problemas si dentro del comentario aparece un asterisco solitario. Mejor patrón: /\*[^*]*\*+(?:[^/*][^*]*\*+)*/ (patrón eficiente para comentarios C). Aquí usamos * y + greedy, pero estructurados para no saltar delimitadores.
6. Uso de posesivos para cortar backtracking en patrones anidados

Problema: Validar que una cadena consta de paréntesis balanceados con un máximo de profundidad (caso teórico).

Un patrón simple recursivo (en PCRE): \(([^()]|(?R))*\) es greedy normal y puede sufrir backtracking con cadenas largas no balanceadas. Para optimizar: \(([^()]++|(?R))*+\) usando posesivos. Esto restringe retrocesos inútiles dentro de la repetición de caracteres no paréntesis.
7. Contrastando greedy vs. lazy en reemplazo

Texto: "primero" y "segundo"

    Si queremos eliminar todo entre la primera y la última comilla usando greedy: ".*" selecciona "primero" y "segundo", lo cual puede ser deseado si queremos limpiar un gran bloque.

    Si queremos eliminar cada frase entrecomillada por separado, usamos lazy: ".*?" con reemplazo global.

Ejemplo en Python:
python

import re
texto = '"primero" y "segundo"'
re.sub(r'"[^"]*"', 'X', texto)  # clase negada: mejor que lazy, más seguro.

8. Cuantificadores y límites de palabra

Patrón para encontrar palabras de 4 letras exactas: \b\w{4}\b

    \b límite de palabra.

    \w{4} exactamente cuatro caracteres de palabra.
    No hay ambigüedad, greedy y lazy son iguales aquí porque es un número fijo.

Para palabras de al menos 4 letras: \b\w{4,}\b greedy consume toda la palabra, que es lo deseado.
9. Backtracking catastrófico y cómo solucionarlo

Ejemplo de patrón vulnerable (validación de número de serie con partes opcionales): (\d+,)*\d+
Entrada: "123,456,789" funciona bien. Entrada malformada: "123,456,789," puede causar backtracking intenso.

Solución con grupo atómico \b(?>\d+,)*\d+\b o usando cuantificadores posesivos \d++(?:,\d++)*+ (no es exactamente igual, hay que reestructurar). El grupo atómico (?>...) evita retroceso dentro del grupo, acelerando el fallo.
10. Cuantificadores con condiciones

En PCRE podemos usar condicionales con cuantificadores. Ejemplo: ^(?:(\())\d+(?(1)\))$ que coincide con (123) o 123, pero no (123. Aquí la repetición es \d+ (greedy), podríamos hacerla posesiva para evitar backtracking: \d++.

