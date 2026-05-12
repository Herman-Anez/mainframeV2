/1//////////////////////////////////////////////////////////////////////////////////////////
01_que_es_regex.md
¿Qué es una expresión regular?

Una expresión regular (regex o regexp) es una secuencia de caracteres que define un patrón de búsqueda. Se utiliza para encontrar, validar, extraer o modificar cadenas de texto. Con una única expresión podemos describir un conjunto potencialmente infinito de combinaciones que comparten una misma estructura.
Fundamento teórico

Las expresiones regulares tienen su origen en la teoría de autómatas y los lenguajes formales. En ciencia de la computación, un lenguaje regular es aquel que puede ser reconocido por una máquina de estados finitos (determinista o no determinista, DFA/NFA). Toda expresión regular define un lenguaje regular.

Steven Kleene formalizó la notación en la década de 1950. Hoy en día, los motores de regex modernos extienden esta teoría con capacidades que van más allá de los lenguajes estrictamente regulares (por ejemplo, retroreferencias y recursión), lo que los hace más potentes pero también abre puertas a problemas de rendimiento (backtracking catastrófico).
Partes de una regex

    Literales: caracteres que coinciden consigo mismos (ej. a, 1, @).

    Metacaracteres: símbolos con significado especial (. ^ $ * + ? { } [ ] \ | ( )).

    Cuantificadores: indican cuántas veces debe aparecer un elemento.

    Clases de caracteres: conjuntos o rangos entre corchetes [...].

    Anclas: posiciones sin consumo de caracteres (^, $, \b).

    Grupos y captura: paréntesis para agrupar y recordar subcoincidencias.

    Aserciones de ancho cero: lookahead y lookbehind.

¿Para qué se usan?

    Validación de formularios (email, teléfono, DNI).

    Extracción de datos de logs, scraping básico.

    Transformación de texto (reemplazar formatos, limpiar espacios).

    Resaltado de sintaxis en editores de código.

    Enrutamiento de URLs en frameworks web.

    Análisis léxico en compiladores e intérpretes.

Motores y dialectos

No todas las regex son iguales. Existen varios dialectos según el motor que las procesa:
Motor	Presente en	Características destacadas
PCRE	Perl, PHP, Apache, Python (módulo regex)	Recursión, grupos atómicos, lookbehind variable, subrutinas
ECMAScript	JavaScript moderno	Lookbehind (ES2018), propiedades Unicode \p{}, \k para grupos con nombre
Python re	Python estándar	Limitado: sin lookbehind variable, sin grupos atómicos
.NET	C#, PowerShell	Lookbehind variable, grupos balanceados para anidamiento
Java	java.util.regex	Grupos atómicos, lookbehind finito
POSIX (ERE/BRE)	grep, sed, awk	Muy básico, sin retroreferencias ni aserciones
Sintaxis genérica de una regex

Generalmente se escribe entre delimitadores /patrón/flags en JavaScript y Perl, o como cadena cruda r'patrón' en Python. Las banderas (i, g, m, s) modifican el comportamiento global.

Ejemplo conceptual:
text

/^([A-Z][a-z]+)\s(\d{2,4})$/gm

    ^ inicio de línea

    ([A-Z][a-z]+) captura palabra que empieza con mayúscula

    \s espacio

    (\d{2,4}) captura número de 2 a 4 dígitos

    $ fin de línea

    Bandera m (multilínea), g (global)

02_metacaracteres.md
Definición

Un metacaracter es un símbolo que en una expresión regular tiene un significado especial, no se interpreta de manera literal. Para tratarlo como un carácter normal hay que escaparlo anteponiendo una barra invertida \.
Lista de metacaracteres estándar

En la mayoría de los motores, los metacaracteres son:
text

. ^ $ * + ? { } [ ] \ | ( )

Cada uno tiene uno o varios roles según el contexto. Vamos a desgranarlos.
. (punto)

Coincide con cualquier carácter excepto un salto de línea (\n). En algunos motores, si se activa el flag s (DOTALL), también coincide con saltos de línea.
regex

a.b → "aab", "a3b", "a b", pero NO "a\nb" (sin flag s)

^ (circunflejo / sombrerito)

Doble función:

    Ancla de inicio: colocado al principio de la regex (o justo tras un |) indica comienzo de línea (o de cadena, según el flag m).

    Negación en clases: si es el primer carácter dentro de [^...], invierte la clase.

regex

^hola → "hola mundo" coincide (inicio)
[^0-9] → cualquier carácter no dígito

$ (dólar)

Ancla de fin: colocado al final (o justo antes de un | y cierre) indica final de línea o de cadena.
regex

mundo$ → "hola mundo" coincide al final

* + ? (cuantificadores simples)

    *: 0 o más repeticiones.

    +: 1 o más repeticiones.

    ?: 0 o 1 repetición, y también convierte cuantificadores en perezosos (*?, +?).

regex

a* → "", "a", "aaaa"
a+ → "a", "aaaa" (pero no "")
a? → "" o "a"

Pueden aplicarse a un carácter, clase o grupo.
{n,m} (cuantificador de intervalo)

Define un número exacto o rango de repeticiones.
regex

a{3} → exactamente "aaa"
a{2,4} → entre 2 y 4 "a"s
a{3,} → 3 o más
a{,5} → hasta 5 (raramente usado, según motor)

[ ] (clase de caracteres)

Define un conjunto de caracteres; coincide con un solo carácter que esté en la lista.
regex

[aeiou] → cualquier vocal
[0-9a-fA-F] → dígito hexadecimal
[^...] → negación (cualquiera que no esté)

Dentro de los corchetes muchos metacaracteres pierden su significado especial (solo algunos lo mantienen, ver más en clases_de_caracteres.md).
\ (barra invertida)

Símbolo de escape. Se usa para:

    Convertir un metacaracter en literal: \. busca un punto literal.

    Iniciar clases predefinidas: \d, \w, etc.

    Denotar anclas: \b, \B.

    Indicar secuencias especiales: \n (nueva línea), \t (tabulador).

| (tubería / alternancia)

Operador OR. Hace que la regex coincida con la expresión de la izquierda o con la de la derecha. Tiene la precedencia más baja, por lo que conviene delimitar con paréntesis.
regex

gato|perro → "gato" o "perro"
a(b|c)d → "abd" o "acd"

( ) (paréntesis)

Cumplen dos propósitos:

    Agrupar partes de la expresión para aplicar cuantificadores o alternancia.

    Capturar la subcoincidencia para usarla después (retroreferencias, extracción).
    Existen variantes:

    (?:...) grupo sin captura.

    (?<nombre>...) grupo con nombre.

    (?=...) aserciones (lookahead).

Metacaracteres que cambian de rol dentro de clases [ ]

Dentro de los corchetes, sólo son metacaracteres: \, ^ (sólo al inicio), - (en medio) y ] (que debe ser el primero o escaparse). Los demás . * + ? { } ( ) | se tratan como literales.
text

[.+*?] → coincide con uno de esos símbolos literalmente.
[a-z] → rango.
[-a] → guion literal si es el primero o inmediato después de ^.
[^a] → negación.

Siempre escapar [ y ] si aparecen fuera de su función.
03_literales_y_escape.md
Literales en regex

Un carácter literal es aquel que coincide consigo mismo. En regex casi todos los caracteres se interpretan de forma literal, a excepción de los metacaracteres. Por ejemplo:
regex

abc → "abc" en "abc123"

Los literales incluyen letras, dígitos, espacios, signos de puntuación que no son metacaracteres (como ,, ;, !, @, #, etc.). Sin embargo, ciertos símbolos como \, ., *, +, ? deben ser escapados si se quieren usar de forma literal.
Escape con barra invertida \

Cuando anteponemos \ a un metacaracter, éste pierde su significado especial y se convierte en un literal. Ejemplo:
regex

punto\. → "punto." literal
3\+2 → "3+2"
\*asterisco → "*asterisco"
\[a\] → "[a]"

Escapado de caracteres no especiales

En muchos motores, escapar un carácter no metacaracter puede tener un efecto diferente o simplemente ser ignorado. Por ejemplo, \q podría tratar de interpretarse como la letra q con barra en algunos contextos, pero en Python re da una advertencia de escape desconocido (aunque aún así se trata como \\q). Mejor práctica: escapar solo los metacaracteres.
El caso de la barra invertida literal

Para representar una barra invertida en la regex se debe usar \\\\ porque cada barra se convierte en un metacarácter de escape: en el patrón se escribe \\ (que representa una barra literal en la mayoría de lenguajes). En cadenas de texto de los lenguajes: es posible que necesitemos escapar la barra también según las reglas del lenguaje (por ejemplo en Python raw string r"\\" es una sola barra, mientras que "\\\\" son dos barras). Recomendación: usar strings crudas (r'\\') para regex en lenguajes que lo permitan.
Secuencias de escape para caracteres especiales

Además de quitar poder a los metacaracteres, el \ se usa para representar caracteres no imprimibles o unicode.
Secuencia	Significado
\n	Salto de línea (LF, Unix)
\r	Retorno de carro (CR)
\t	Tabulador horizontal
\v	Tabulador vertical
\f	Avance de página
\xhh	Carácter con código hexadecimal de 2 dígitos (ej. \x41 → 'A')
\x{hhhh}	Código hexadecimal de longitud variable (Perl, PCRE)
\uhhhh	Carácter Unicode con 4 dígitos hex (JavaScript, Python)
\Uhhhhhhhh	Unicode con 8 dígitos (Python, PCRE)
\cX	Carácter de control (Ctrl+X)
\0	Carácter nulo

Ejemplos:
regex

línea 1\r?\nlínea 2 → captura línea con posible retorno de carro
\x41 → "A"
\u00F1 → "ñ"

Escapes específicos de cada motor

    \Q...\E: Comienzo y fin de zona literal. Todo lo que está dentro se trata como texto literal, incluidos metacaracteres. Soportado en Java, PCRE, Python no lo tiene nativo (el módulo regex sí).

regex

\Q[a-z]\E → busca literalmente "[a-z]"

    \U...\E, \L...\E: Cambio a mayúsculas/minúsculas (PCRE, Perl).

Metacaracteres en cadenas de caracteres del lenguaje huésped

A veces hay doble interpretación. En Python, si escribimos "\n" es un salto de línea, pero en una expresión regular escrita como r"\n" es la secuencia regex \n. Si se usa "\\n" en cadena normal, se convierte en \n para la regex. Por eso se recomienda usar raw strings (r"patrón").
Literales y metacaracteres dentro de clases [ ]

En el interior de una clase, los únicos que necesitan escape son \, ], y ^ si no es al inicio. El guion - se escapa si se quiere literal y no estamos formando un rango. Los demás metacaracteres, incluso (, ), *, +, ., se pueden poner sin escapar.
regex

[(+*)] → clase que busca '(' '+' '*' o ')'
[\\]\] → clase con '\' y ']' (necesita escapes)
[a-z._%+-] → clase típica para emails, el guion al final evita ambigüedad.

04_anclas_y_limites.md
Concepto: anclas y límites

Son posiciones dentro de la cadena que no consumen caracteres, sino que afirman que en ese punto se cumple una condición. Su función es delimitar dónde debe ocurrir una coincidencia sin añadir caracteres al resultado.
^ - Inicio

    Modo normal (flag m inactivo): coincide con el inicio de la cadena.

    Modo multilínea (m): coincide con el inicio de cada línea (después de cada \n o al inicio de la cadena).

regex

^a → en "abc\naaa" sin flag m: coincide solo con el primer 'a'.
Con flag m: coincide con el primer 'a' de "abc" y el primer 'a' de "aaa".

Nota: El ancla no consume el salto de línea.
$ - Final

    Normal: final de la cadena o justo antes de un \n al final de la cadena (varía según motor; PCRE: justo antes del salto final si existe).

    Multilínea: final de cada línea (antes de \n o final de cadena).

regex

a$ → "abc\naaa", con flag m, coincide con el 'a' final de "aaa" y con el 'a' de "abc"? No porque después de "abc\na" hay salto, pero en "abc\n", $ justo después de "abc\n"? Depende del motor. Mejor no confiar; usar \z para final absoluto.

\A - Inicio absoluto

Coincide únicamente con el comienzo de la cadena, sin importar el flag multilínea.
regex

\Aabc → "abc\ndef", con o sin m, solo al principio.

\z y \Z - Final absoluto

    \z (minúscula) final absoluto de la cadena, sin excepciones.

    \Z (mayúscula) final de la cadena o justo antes de un salto de línea al final de la cadena (en Python re, \Z es final absoluto, ojo). Sólo en motores como PCRE y .NET.

regex

abc\z → "abc\n" NO coincidirá (porque hay \n luego).
abc\Z → Puede coincidir con "abc" y "abc\n" según motor.

\b - Límite de palabra (word boundary)

Coincide en una posición entre un carácter de palabra (\w = [a-zA-Z0-9_]) y uno no palabra (\W) o entre un no palabra y uno palabra. También coincide al inicio de cadena si el primer carácter es \w, y al final si el último es \w.

Sirve para aislar palabras completas.
regex

\bgato\b → busca la palabra "gato" como palabra entera.
"No es un gato, es un gato." coincide con las dos.

Importante: \b depende de la definición de \w. Si \w incluye guion bajo, \b lo considerará parte de palabra. Para límites de palabra Unicode se pueden usar propiedades unicode \b{g} (en algunos motores) o (?<=\P{L})(?=\p{L}) etc.
\B - No límite de palabra

Coincide en cualquier posición donde \b no coincide. Se usa para patrones que deben estar en medio de palabras.
regex

\Bton\B → encuentra "ton" dentro de "tonelada" o "ratón" pero no si "ton" es palabra aislada.

Combinación de anclas

Las anclas no consumen caracteres, por lo que podemos tener varias juntas (aunque normalmente no tendría sentido salvo en cero-longitud). Por ejemplo, ^\b exige que al inicio haya un límite de palabra (es decir, que el primer carácter tras el inicio sea \w).
Uso incorrecto como caracteres dentro de clase

Dentro de [...], ^ NO funciona como ancla, sino como negación de la clase (sólo si es el primer carácter). $ y \b pierden su significado dentro de la clase y se tratan como literales. Evitar escribirlos sin sentido: [$] es un dólar literal.
05_clases_de_caracteres.md
Definición

Una clase de caracteres es una construcción entre corchetes [...] que define un conjunto de caracteres. Coincide con un único carácter que pertenezca a ese conjunto.
Sintaxis básica
regex

[abc]  → a, b o c
[a-z]  → cualquier letra minúscula del alfabeto inglés
[0-9]  → cualquier dígito
[A-Za-z] → cualquier letra

Se pueden combinar múltiples rangos y caracteres sueltos:
regex

[a-zA-Z0-9_] → carácter de palabra inglés (igual que \w)

Carácter especial dentro de corchetes
- (guion)

    Si se coloca entre dos caracteres que pueden formar un rango según el orden de la tabla ASCII/Unicode, define un rango.

    Para tratarlo como literal debe ir al principio, al final, justo después de ^ (en clase negada) o escapado \-.

Ejemplo de rango inverso no permitido: [z-a] no es válido. En algunos motores es ignorado o error.
^

Si se escribe inmediatamente después del corchete de apertura, niega la clase: [^...] coincide con cualquier carácter que NO esté en la lista.
regex

[^aeiou] → cualquier carácter que no sea vocal minúscula.

Si ^ aparece en otra posición (no al inicio), es un literal ^.
]

El corchete de cierre debe escaparse \] o colocarse como primer carácter de la clase (después de ^ si la hay) para que se tome literal.
regex

[]]   → clase que contiene ']' (válido: ']' como primer carácter).
[]abc] → ']', 'a', 'b', 'c'.
[^]]  → cualquier carácter excepto ']'.

\

La barra invertida mantiene su función de escape, por lo que \d, \w, \s y cualquier escape funcionan dentro de corchetes. \\ es la barra literal.
Clases predefinidas (shorthands)

Estas secuencias se pueden usar dentro o fuera de corchetes y representan clases comunes.
Secuencia	Equivalencia ASCII (sin unicode)	Significado
\d	[0-9]	Dígito
\D	[^0-9]	No dígito
\w	[a-zA-Z0-9_]	Carácter de palabra
\W	[^a-zA-Z0-9_]	No palabra
\s	[ \t\n\r\f\v] (varía)	Espacio en blanco
\S	[^ \t\n\r\f\v]	No espacio
\h	Espacio horizontal (sólo algunos motores)	[ \t]
\v	Espacio vertical	[\n\r] (cuidado: en PCRE \v es tab vertical)
\R	Salto de línea universal (PCRE, Java, .NET)	\r\n|\n|\r

Con el flag unicode activado (/u en JS, re.UNICODE en Python), \w, \d, etc. pueden ampliarse para incluir letras y dígitos de otros alfabetos. Por ejemplo \w con unicode incluye ñ, ü, caracteres cirílicos, etc. Depende del motor.
Clases POSIX

Son clases nombradas, encerradas entre dobles corchetes y dos puntos. Aparecen en motores como PCRE, Perl, Python (módulo regex), y algunos sabores de Unix.
regex

[[:alnum:]]  → [a-zA-Z0-9]
[[:alpha:]]  → letras
[[:digit:]]  → [0-9]
[[:upper:]]  → mayúsculas
[[:lower:]]  → minúsculas
[[:punct:]]  → signos de puntuación
[[:space:]]  → espacios (incluye \n, \t)
[[:xdigit:]] → dígitos hexadecimales

Estas clases se pueden combinar en una misma clase: [[:upper:][:digit:]].
Propiedades Unicode (\p{...})

Con soporte unicode (flag u en JS, por defecto en Python 3), podemos usar propiedades generales o específicas.
regex

\p{L}   → cualquier letra (Letter)
\p{Ll}  → letra minúscula (Letter, lowercase)
\p{Lu}  → letra mayúscula
\p{N}   → cualquier número (Number)
\p{Nd}  → dígito decimal
\p{P}   → puntuación
\p{S}   → símbolo
\p{Sc}  → símbolo de moneda
\p{Han} → caracteres Han
\p{Greek} → letras griegas
\p{IsLatin} → bloque Latin (en Java, \p{IsLatin})

Negación: \P{...} (mayúscula P). Ejemplo: \P{L} no letra.

Se pueden usar dentro de corchetes: [\p{L}\d].
Clases avanzadas: sustracción e intersección (.NET, Java, Python regex)

    Intersección: [a-z&&[^aeiou]] en Java → consonantes. En .NET: [a-z-[aeiou]] es sustracción directa.

    Python regex permite [a-z--[aeiou]] para diferencia.

En otros motores, no hay soporte directo y hay que usar lookaheads.
Cuidados con rangos

Un rango como [A-z] incluye caracteres entre 'A' (65) y 'z' (122), que en ASCII contiene [\]^_\`` porque en el medio están esos símbolos. Mejor usar [A-Za-z]`. Los rangos dependen del orden numérico de los puntos de código, no del alfabeto humano.
Uso de clases en expresiones

Las clases siempre casan un solo carácter. Para múltiples debemos usar cuantificadores: [0-9]+ para uno o más dígitos. La clase vacía [] es inválida (error).
/////////////////////////////////////////////////////////////////////////////

/2//////////////////////////////////////////////////////////////////////////////////////////
01_greedy_lazy.md
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
02_posesivos.md
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
03_ejemplos_practicos.md

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

/////////////////////////////////////////////////////////////////////////////

/3//////////////////////////////////////////////////////////////////////////////////////////
01_captura_basica.md
¿Qué es un grupo de captura?

Un grupo de captura es una subexpresión encerrada entre paréntesis (...). Cumple dos funciones:

    Agrupar partes del patrón para aplicar cuantificadores, alternancia o anidamiento.

    Capturar la subcadena que coincide con esa subexpresión, permitiendo recuperarla después (en código, reemplazos o mediante retroreferencias).

Ejemplo sencillo:
regex

(\d{3})-(\d{2})-(\d{4})

Aplicado a "123-45-6789", los paréntesis capturan tres partes: "123", "45" y "6789".
Numeración de los grupos

Los grupos de captura se numeran de izquierda a derecha según el orden del paréntesis de apertura. El grupo 0 es siempre la coincidencia completa, y los grupos 1, 2, 3... corresponden a cada paréntesis.
regex

(a(b)c)d

Coincidencia sobre "abcd":

    Grupo 0: "abcd"

    Grupo 1: "abc" (primer paréntesis)

    Grupo 2: "b" (segundo paréntesis, anidado)

    Grupo 3: no existe.

La numeración es fija y no depende de si el grupo participó o no en la coincidencia. Un grupo opcional que no casó tendrá un valor None o vacío según el motor.
Cómo acceder a las capturas desde código

La forma de obtener los grupos varía según el lenguaje:

Python:
python

import re
m = re.search(r'(\d{3})-(\d{2})-(\d{4})', '123-45-6789')
m.group(0)  # '123-45-6789'
m.group(1)  # '123'
m.group(2)  # '45'
m.group(3)  # '6789'
m.groups()  # ('123', '45', '6789')

JavaScript:
javascript

let regex = /(\d{3})-(\d{2})-(\d{4})/;
let match = '123-45-6789'.match(regex);
match[0]; // '123-45-6789'
match[1]; // '123'
match[2]; // '45'
match[3]; // '6789'

Java:
java

Pattern p = Pattern.compile("(\\d{3})-(\\d{2})-(\\d{4})");
Matcher m = p.matcher("123-45-6789");
if (m.find()) {
    m.group(1); // "123"
    m.group(2); // "45"
    m.group(3); // "6789"
}

Grupos anidados

Los paréntesis se pueden anidar; la numeración sigue el orden de apertura. Ejemplo:
regex

((a)(b(c)))d

Texto: "abcd"

    Grupo 1: "abc" (abre primero)

    Grupo 2: "a" (segundo)

    Grupo 3: "bc" (tercero, b(c))

    Grupo 4: "c" (cuarto)

Grupos opcionales y valor nulo

Un grupo puede ser condicional gracias a ? o *. Si la parte no casa, el grupo queda vacío o indefinido.
regex

(a(\d)?b)

En "ab": Grupo 1 "ab", grupo 2 None (o vacío). En "a5b": Grupo 2 "5".
Uso de grupos para aplicar cuantificadores a partes complejas

Sin captura nos sirve para agrupar, por ejemplo:
regex

(https?:\/\/)?(www\.)?example\.com

Los grupos capturan el protocolo y el subdominio si existen, permitiendo extraerlos después.
Captura y alternancia
regex

(jpg|png|gif)$

Captura la extensión del archivo. Sólo se captura la alternativa que coincide.
Eficiencia y memoria

Cada grupo de captura consume memoria porque se almacena la subcadena capturada. En patrones de gran escala puede ralentizar. Si no necesitas las capturas, considera usar grupos sin captura (?:...) (ver siguiente sección).
Buenas prácticas

    Usa nombres de grupo (siguiente sección) para mejorar la legibilidad.

    Cierra siempre los paréntesis; un paréntesis no balanceado genera error.

    Escapa los paréntesis literales: \( y \).

02_grupos_sin_captura.md
Definición

Un grupo sin captura agrupa parte de la expresión sin almacenar el texto coincidente. Su sintaxis es (?: ... ). Sirve únicamente para aplicar cuantificadores, alternancia o atomizar una parte sin generar una referencia de captura.

Ejemplo:
regex

(?:https?:\/\/)?(?:www\.)?example\.com

Los grupos no capturan protocolo ni subdominio, pero sí están agrupados para hacerlos opcionales.
Ventajas frente a los grupos de captura

    Eficiencia: Al no almacenar la subcadena, se ahorra memoria y tiempo.

    Claridad: Indica a quien lee el patrón que esa subcoincidencia no se usará después.

    Evita interferencias: Si ya tienes varios grupos de captura y necesitas uno adicional para agrupar sin cambiar la numeración existente, un grupo sin captura no añade nuevos índices.

Por ejemplo, si tienes (\d{4})-(\d{2})-(\d{2}) y decides agrupar el separador sin capturarlo, puedes escribir (\d{4})(?:-(\d{2}))? para que el guión y el segundo número sean opcionales. El grupo 1 es el año, el grupo 2 el mes (si existe), sin introducir un grupo extra para el guión.
Sintaxis y uso

    (?:patrón) : agrupa patrón.

    Se puede aplicar cuantificadores: (?:abc)+ coincide con una o más repeticiones de "abc".

    En alternancia: (?:gato|perro) igual que gato|perro, pero a veces es necesario para encapsular.

Comparación con grupos de captura

Dado el texto "rojo verde azul":

    Captura: ((?:r|v)\w+) captura palabras que empiezan con 'r' o 'v'. El primer grupo captura toda la palabra, el grupo interno es sin captura. Así grupo 1 es la palabra sin almacenar la letra inicial por separado.

    Si usáramos (r|v)(\w+) tendríamos dos capturas: letra y resto.

Grupos sin captura y modificadores de modo

En algunos motores se pueden incluir flags localizadamente con (?flags:...), que es un grupo sin captura con modificadores. Ejemplo: (?i:abc) casará "ABC", "Abc", etc., sin afectar el resto del patrón. Funciona en PCRE, Perl, .NET, Java. Python re no soporta (?i:...) (sí soporta (?i) a nivel global o en el módulo regex externo).
Ejemplo práctico: extracción de fecha con separadores flexibles
regex

(\d{4})(?:[-/.])(\d{2})(?:[-/.])(\d{2})

Coincide con 2024-12-25, 2024/12/25, 2024.12.25. Captura año (grupo 1), mes (2) y día (3). Los separadores están en grupos sin captura.
Cuándo NO usar grupos sin captura

Si posteriormente necesitas acceder a la subcadena (por ejemplo, para reemplazos con $1 o para procesado), debes mantener los paréntesis de captura. Los grupos sin captura son invisibles para las retroreferencias y las funciones de extracción.
03_grupos_nombrados.md
Concepto

Los grupos con nombre asignan un identificador textual a un grupo de captura, en lugar de depender de un número. Esto mejora la legibilidad y evita problemas cuando se modifica la expresión añadiendo o quitando grupos.
Variantes de sintaxis según motor

Lamentablemente no hay un estándar único, pero los más comunes son:
Motor / Lenguaje	Sintaxis de definición	Retroreferencia interna	Uso en reemplazo
Python (re)	(?P<nombre>...)	(?P=nombre)	\g<nombre> en reemplazo
PCRE / Perl	(?<nombre>...) o (?'nombre'...)	\k<nombre> o \k'nombre'	$+{nombre} (Perl) o \g<nombre>
JavaScript (ES2018+)	(?<nombre>...)	\k<nombre>	$<nombre> en reemplazo
.NET	(?<nombre>...) o (?'nombre'...)	\k<nombre>	${nombre} en reemplazo
Java (Java 7+)	(?<nombre>...)	\k<nombre>	${nombre} en reemplazo

Nota: En Python, el módulo re solo soporta (?P<nombre>). El módulo externo regex soporta ambas.
Ejemplo con diferentes sintaxis

Python:
python

import re
patron = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
m = re.search(patron, '2024-12-25')
m.group('year')   # '2024'
m.group('month')  # '12'
m.group('day')    # '25'
# Retroreferencia dentro del patrón: (?P=year) para casar el mismo año.

JavaScript:
javascript

let regex = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;
let match = regex.exec('2024-12-25');
match.groups.year   // '2024'
match.groups.month  // '12'
match.groups.day    // '25'

Java:
java

Pattern p = Pattern.compile("(?<year>\\d{4})-(?<month>\\d{2})-(?<day>\\d{2})");
Matcher m = p.matcher("2024-12-25");
if (m.find()) {
    m.group("year"); // "2024"
    m.group("month"); // "12"
    m.group("day"); // "25"
}

Ventajas de los nombres

    Código más legible: m.group('year') vs m.group(1).

    Resistente a cambios: si insertas un nuevo grupo antes, la numeración cambia, pero los nombres permanecen intactos.

    Documentación interna: el propio patrón describe lo que captura.

Reglas y compatibilidades

    Los nombres deben ser identificadores válidos (letras, dígitos, guiones bajos, sin empezar por dígito en la mayoría de motores).

    No puede haber dos grupos con el mismo nombre dentro del mismo patrón (aunque algunos motores como .NET permiten grupos con el mismo nombre, compartiendo la captura; en PCRE/JS es error).

    Si un motor no soporta grupos nombrados, hay que limitarse a la numeración clásica.

Uso en reemplazos

Python:
python

re.sub(r'(?P<nombre>\w+)', r'\g<nombre>', texto)

JavaScript:
javascript

texto.replace(/(?<nombre>\w+)/g, '$<nombre>')

Compatibilidad con cuantificadores y anidamiento

Los grupos con nombre pueden anidarse y combinarse con grupos sin nombre. La numeración de todos los grupos sigue el orden de apertura; los nombres no alteran la numeración. Se puede referenciar un grupo por número aunque tenga nombre.
04_retroreferencias.md
Definición

Una retroreferencia es una construcción que hace referencia a un grupo de captura previamente encontrado en el mismo patrón. Permite exigir que el texto actual coincida exactamente con lo capturado por ese grupo.
Sintaxis básica

    \1, \2, ... \9 (y en algunos motores \10 o más usando \10 como referencia al grupo 10, pero puede ser ambiguo; en PCRE se usa \g{10} o \10 solo si hay al menos 10 grupos, sino se interpreta como backreference 1 seguido de '0'. Mejor usar \g{n} para números grandes.)

Para grupos con nombre:

    Python (?P=name)

    PCRE/JS/Java/.NET: \k<name> o \k'name'

Ejemplo clásico: palabras repetidas
regex

\b(\w+)\s+\1\b

Coincidencia: "hola hola", "mundo mundo". Explicación:

    (\w+) captura una palabra.

    \s+ espacios.

    \1 forzosamente debe ser la misma palabra capturada.

Coincidencia de comillas y delimitadores
regex

(["'])(.*?)\1

En "una frase" o 'otra', captura la frase dentro de comillas iguales. El grupo 1 captura la comilla de apertura y \1 fuerza la misma de cierre.
Numeración y retroreferencias en grupos anidados

Dado ((a)(b(c)))d, las referencias:

    \1 → abc

    \2 → a

    \3 → bc

    \4 → c

Las retroreferencias pueden referirse a grupos que aparecen después (en motores que permiten backreferences hacia adelante, aunque son muy raras y generalmente no se recomiendan). Lo normal es que el grupo referenciado esté a la izquierda de la retroreferencia.
Referencias en cadenas de reemplazo

Muchas herramientas usan $1, $2 o \1, \2 en la cadena de sustitución, refiriéndose a los grupos capturados en la búsqueda. Por ejemplo:

    s/(\w+)\s+(\w+)/$2 $1/ en sed/Perl invierte dos palabras.

    En Python: re.sub(r'(\w+)\s+(\w+)', r'\2 \1', texto).

Atención: Las retroreferencias en la cadena de reemplazo no son iguales a las del patrón. En el patrón se usa \1 (sólo motores), en reemplazo depende del motor; en Python se usa \1, en JavaScript $1. Las retroreferencias en el patrón exigen coincidencia exacta de la subcadena capturada.
Retroreferencias a grupos no existentes o que no participaron

Si un grupo es opcional y no casa, la retroreferencia puede considerarse un carácter vacío y casará con el vacío (en muchos motores) o fallará. Ejemplo: (a)? \1 en "b b". El grupo 1 no casa, entonces \1 intenta casar con vacío; normalmente no hay casamiento porque espera algo. En la práctica, una referencia a un grupo que no participó hace fallar la expresión. Específicamente, en PCRE una backreference a un grupo que no capturó provoca un fallo de coincidencia a menos que se permita referencia vacía. En Python re, si el grupo no participó, la backreference falla (no coincide con nada). Por eso es aconsejable que el grupo sea obligatorio si se va a referenciar.
Retroreferencias y recursión / subrutinas

En motores con soporte avanzado (PCRE, Perl), se puede usar (?1), (?&nombre) para llamar a un subpatrón como subrutina (no solo comparar con lo capturado, sino re-ejecutar el subpatrón). Esto es distinto a las retroreferencias, que simplemente comparan con la cadena literal previamente capturada. Las retroreferencias comprueban igualdad de texto, no repetición del patrón.

Ejemplo: (\d{3})-\1 obliga a que los dos bloques de dígitos sean idénticos. Si quisieras repetir el patrón (tres dígitos cualesquiera), simplemente repetirías \d{3}.
Número máximo de retroreferencias

En la mayoría de motores, \1 a \9 están disponibles. Para números de dos dígitos, se usa \10 o \g{10} para evitar ambigüedad. En PCRE, \10 se interpreta como backreference 10 si hay al menos 10 grupos, sino como backreference 1 seguido de '0'. La notación \g{10} es segura para cualquier número. Python re no soporta \g{n} estándar, pero en la práctica con números mayores de 99 es extremadamente raro.
Limitaciones y riesgos

    Las retroreferencias pueden causar backtracking intenso porque el motor debe volver a intentar la captura de la referencia si hay múltiples posibilidades. Ejemplo: ^(a+)\1$ sobre "aaaa" funciona bien, pero si se extiende, puede degradar.

    No son implementables en autómatas finitos puros; los motores híbridos (DFA) no las soportan.

05_grupos_atomicos.md
Definición

Un grupo atómico es una agrupación que, una vez que ha coincidido, no permite backtracking hacia su interior. Su sintaxis es (?> ... ). Está disponible en PCRE, Perl, Java, .NET, Python con el módulo regex externo. No está presente en JavaScript ni en el módulo re estándar de Python.
Comportamiento

Cuando el motor entra en un grupo atómico (?>subexpresión), intenta casar la subexpresión. Si tiene éxito, sale del grupo y descarta todos los estados internos de backtracking. Si posteriormente el resto del patrón falla, el motor no reintentará con menos repeticiones ni otras alternativas dentro del grupo atómico. Simplemente fallará la coincidencia global desde esa posición y buscará en otro lugar (si procede).

Esto es muy similar a los cuantificadores posesivos (un cuantificador posesivo es equivalente a un grupo atómico que envuelve un elemento con cuantificador). Por ejemplo:
a++ es equivalente a (?>a+).
Ejemplo de funcionamiento
regex

(?>a+)b

Texto: "aaaab"

    Entra en el grupo, a+ consume todas las as (4). Sale del grupo atómico.

    Luego intenta casar b con el siguiente carácter. Como es posesivo, no retrocede para ceder as. En "aaaab" el siguiente es b, éxito, capture "aaaab".

Texto: "aaaa"

    a+ consume las 4 as. Sale del grupo atómico.

    Intenta b pero no hay más caracteres. Falla global sin backtracking interior. Habría fallado igual que con a++b.

Diferencia crucial con grupo normal (no atómico)

Con un grupo normal (a+)b en "aaaa":

    a+ consume todas las as.

    Intenta b, falla.

    Backtrack: a+ cede una a, ahora tiene 3 as. Intenta b, aún falla, cede otra, etc., hasta agotar. Esto genera varios pasos de retroceso, pero en este caso simple no es grave. En patrones complejos con anidamientos, la ausencia de backtracking mejora enormemente el rendimiento.

Usos principales

    Optimización: Evitar backtracking catastrófico. Si sabemos que dentro del grupo no necesitamos que el motor reconsidere cuántos caracteres tomó, lo encerramos en un grupo atómico. Ejemplo clásico: (?>.*?) no tiene sentido porque .*? es perezoso, pero un grupo atómico con .* puede ser útil para capturar hasta un delimitador sin retroceder: (?>[^"]*) para contenido sin comillas, aunque una clase negada no provoca backtracking de todas formas.

    Patrones de desastre: (a+)*b con entrada "aaaa..." causa backtracking exponencial. Si transformamos a (?>a+)*b o (a++)*b, eliminamos el problema.

    Garantizar que una palabra completa se capture sin retroceder: \b(?>\w+)\b asegura que una vez que se toma una palabra no se suelte parte para intentar un casamiento más largo (útil si hay alternancia que podría casar con prefijos). Pero normalmente las clases negadas o cuantificadores greedys sin opciones no causan problema; el grupo atómico es relevante cuando hay alternancia interior.

Simulación en motores sin soporte

En JavaScript (sin grupos atómicos ni posesivos), se puede simular un grupo atómico con un lookahead y una retroreferencia:
javascript

// Simular (?>a+)b
/(?=(a+))\1b/

El lookahead captura a+ de forma greedy, la retroreferencia \1 consume exactamente esa captura sin posibilidad de backtracking. Así se evita que el motor ceda as. Pero hay limitaciones: no se puede simular un grupo atómico complejo con múltiples alternativas si hay solapamientos. Otra técnica en JS: usar (?:a+)(?!...) no es igual.

En Python re estándar, no hay grupos atómicos; se puede recurrir al módulo regex.
Combinación con otros constructos

Los grupos atómicos pueden contener otras agrupaciones y cuantificadores.

Ejemplo avanzado: validar un número racional con formato \d+(\.\d+)? sin permitir retroceso en la parte entera si la parte decimal falla:
regex

(?> \d+ ) (?: \. \d+ )?

Aunque en este caso el backtracking no sería perjudicial, es un ejemplo.
Precauciones

Un grupo atómico no debe usarse si la coincidencia global puede requerir retroceder dentro de él. Por ejemplo, (?>".*?") para buscar cadenas entre comillas fallará con "hola" y "mundo" porque .*? dentro del grupo atómico consume lo mínimo y nunca retrocede, pero en realidad necesitamos que el grupo abarque "hola". Si ponemos (?>".*?"), en "hola" y "mundo" la primera comilla se empareja, .*? toma cero caracteres, luego espera la comilla final, encuentra " inmediatamente (porque "hola" tiene una comilla tras "). En realidad (?>".*?") sí podría funcionar porque .*? se expande como parte de su propia lógica perezosa, pero el grupo es atómico y eso impediría que una vez que el grupo encontró una coincidencia válida (una cadena mínima), si luego falla el resto del patrón, no se reconsideren más cadenas más largas. Podría no ser lo deseado. La regla: úsalo cuando la subexpresión interior no necesita ser ajustada para dar paso a la coincidencia global tras la salida del grupo.
Ejemplo de optimización real: números con miles separados
regex

(?> \d{1,3} (?: , \d{3} )* ) (?: \. \d+ )?

Agrupar la parte entera en grupo atómico evita que el motor intente distribuciones alternativas de comas si la entrada es inválida, acelerando el fallo.
/////////////////////////////////////////////////////////////////////////////

/4//////////////////////////////////////////////////////////////////////////////////////////
01_lookahead.md
Definición

Un lookahead (inspección hacia adelante) es una aserción de ancho cero que verifica si una subexpresión coincide (o no coincide) inmediatamente después de la posición actual, sin consumir caracteres.

Existen dos tipos:

    Lookahead positivo (?= … ) : comprueba que lo que sigue SÍ coincida.

    Lookahead negativo (?! … ) : comprueba que lo que sigue NO coincida.

En ambos casos, tras evaluar la aserción, el cursor regresa a la posición donde se encontraba. El texto inspeccionado no forma parte de la coincidencia final.
Mecanismo de funcionamiento

    El motor alcanza la posición donde aparece el lookahead.

    Intenta emparejar la subexpresión interna contra el texto desde esa posición.

    Si tiene éxito (lookahead positivo) o fracaso (lookahead negativo), la aserción se considera satisfecha; en caso contrario, falla y la coincidencia global retrocede.

    El puntero de búsqueda vuelve exactamente a la posición inicial.

Ejemplo:
regex

X(?=Y)

    Busca X solo si a continuación viene Y.

    En "XY", la coincidencia es únicamente "X" (la Y no se consume).

    En "XZ", falla.

Lookahead positivo: (?=patrón)

Coincide en una posición si desde ahí se puede casar patrón.

Casos de uso:

    Imponer condiciones sin consumir. Validar contraseña: ^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$.
    Cada lookahead verifica la presencia de una categoría en cualquier lugar de la cadena.

    Overlapping matches (solapadas). Para encontrar todas las apariciones de "ana" dentro de "banana": (?=ana) devolverá coincidencias de longitud cero en las posiciones 1 y 3 (en motores que permiten matches vacíos con findall/match). Luego se puede extraer manualmente.

    Asegurar un delimitador pero no incluirlo. Extraer texto antes de un punto: \w+(?=\.) coincide con la palabra antes del punto sin incluir el punto.

Lookahead negativo: (?!patrón)

Coincide en una posición si desde ahí NO se puede casar patrón.

Casos de uso:

    Excluir patrones: (?!unwanted)\w+ encuentra palabras que no son "unwanted".

    Negaciones complejas: ^(?!.*\.\.).*$ prohíbe dos puntos seguidos en una cadena (se evita el backtracking catastrófico frente a otros enfoques).

    Limitar cuantificadores: \b(?!\d+\b)\w+\b encuentra palabras que no están compuestas exclusivamente por dígitos.

Combinación de varios lookaheads

Se pueden poner varios seguidos; todos deben cumplirse en la misma posición.
regex

(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[#?!@$%^&*-])\S{8,}

Cada lookahead inspecciona desde el principio de la cadena, pero como son de ancho cero, se superponen. Así exigimos que la cadena contenga al menos una mayúscula, una minúscula, un dígito y un carácter especial.
Lookaheads anidados

Es posible anidar lookaheads, aunque no es muy frecuente. Ejemplo: (?=(?=\d)\w{3}) verificar que la posición siguiente cumple dos condiciones simultáneas (aquí, que empieza con dígito y tiene 3 caracteres de palabra).
Compatibilidad entre motores

Los lookaheads están soportados en todos los motores modernos: JavaScript, Python (re), Java, .NET, PCRE, Perl, etc. La sintaxis es universal. La única diferencia es que en motores que no permiten lookbehind, a veces hay que simularlos (pero lookahead siempre funciona).
Consideraciones de rendimiento

    Los lookaheads pueden ralentizar si contienen cuantificadores codiciosos que examinan gran parte de la cadena, pues se ejecutan en cada posición potencial.

    Sin embargo, un lookahead puede actuar como un grupo atómico en algunos contextos. Por ejemplo, (?=a*)\1 es una forma de simular un grupo atómico (en JS) porque el lookahead no retrocede; (?=(a*))\1 captura todas las a y luego \1 las consume sin posibilidad de cesión.

    Poner (?=.*palabra) al inicio de una cadena puede ralentizar si la cadena es muy larga y no contiene "palabra", ya que .* recorre todo el texto.

02_lookbehind.md
Definición

Un lookbehind (inspección hacia atrás) comprueba si una subexpresión coincide inmediatamente antes de la posición actual. Tampoco consume caracteres.

    Lookbehind positivo: (?<= … ) → la posición está precedida por el patrón.

    Lookbehind negativo: (?<! … ) → la posición NO está precedida por el patrón.

El cursor está en la posición de interés; el motor “mira hacia atrás” para ver si se cumple la condición. La longitud del texto inspeccionado no se incluye en el match.
Limitaciones históricas y actuales

La implementación del lookbehind es la parte más heterogénea entre motores:
Motor	Longitud fija / variable	Observaciones
Perl 5.30+	Variable (experimental)	Antes solo fija.
PCRE2 (PHP >=7.3)	Variable (con restricciones)	Debe poder determinar una longitud máxima (no permite * o + sin límite superior). Alternativamente se puede usar \K.
PCRE (antiguo) / Perl antiguo	Sólo fija	Patrón debe tener longitud exacta (por ejemplo: (?<=abc|def) ambas opciones deben misma longitud).
JavaScript (ES2018+)	Variable	Sin restricciones de longitud.
Python re (estándar)	Sólo fija	Sin cuantificadores variables; cada alternativa debe tener la misma longitud.
Python regex (externo)	Variable	Soporte completo.
Java	Longitud máxima limitada	Se permiten cuantificadores con límite superior finito: {0,n}. * y + no permitidos a menos que tengan un máximo explícito. Debe poder calcularse el máximo de caracteres que puede consumir.
.NET	Variable	Sin restricciones. Soporta incluso patrones complejos sin límite.

Cuando un motor exige longitud fija, el patrón dentro del lookbehind no puede contener *, +, ? ni {n,}. Solo puede tener literales, clases de caracteres, grupos y alternancias con todas las ramas de igual longitud.

Ejemplo válido en Python re:
regex

(?<=abc|def)X
# Ambas opciones tienen longitud 3.

Ejemplo inválido en Python re:
regex

(?<=a+)X   # error: look-behind requiere patrón de ancho fijo

Lookbehind positivo: (?<=patrón)

Coincide en una posición si justo antes se encuentra patrón.

Casos de uso:

    Extraer un valor precedido por un prefijo: (?<=\$)\d+\.\d{2} captura números decimales después de un dólar, sin incluir el signo $.

    Asegurar un contexto previo: (?<=@)\w+ extrae el nombre de usuario en un correo electrónico después de la @.

    Evitar capturar el delimitador: en (?<=\/)\w+ para obtener la última parte de una URL.

Lookbehind negativo: (?<!patrón)

Coincide si la posición NO está precedida por patrón.

Uso típico: cadenas entre comillas escapadas.
regex

(?<!\\)".*?"

Encuentra comillas dobles que no están precedidas por una barra invertida. Si una comilla va precedida de \, el lookbehind negativo falla, evitando que se tome como delimitador.
Anclas dentro de lookbehind

^ y $ dentro de un lookbehind no tienen un significado global; se refieren a la posición relativa a la actual. En general, no se usan porque no tienen sentido: ^ dentro de un lookbehind positivo (?<=^) significaría "la posición actual es justo después del inicio de la cadena", lo cual es equivalente a \A o similar. (?<=^)X es igual a ^X, pero con lookbehind. Sin embargo, ^ en lookbehind no está permitido en muchos motores o puede no funcionar como se espera. Es más claro usar anclas normales.
Soporte en reemplazos

A veces se usan lookbehinds para reemplazar patrones que están precedidos por algo, sin eliminar ese prefijo. Ejemplo Python:
python

import re
text = "Price $100, discount $20"
re.sub(r'(?<=\$)\d+', 'XXX', text)
# "Price $XXX, discount $XXX"

Alternativa con \K

En PCRE y Perl (y en el módulo regex de Python), \K descarta lo coincidido hasta ese punto, logrando un efecto similar a lookbehind positivo de longitud variable. Ejemplo: \$\K\d+ equivale a (?<=\$)\d+ pero mucho más eficiente y sin restricciones de longitud fija. Tras \K, la parte izquierda no forma parte del match.
Simulación y workarounds en motores limitados

Si tu motor no soporta lookbehind (por ej. JavaScript antiguo), puedes:

    Invertir la cadena y aplicar lookahead.

    Capturar la parte previa y luego usar código para descartarla.

    En validaciones, usar (?:patrón_previo)(lo_que_quiero) y luego comprobar el grupo capturado.

03_ejemplos_validacion.md

Aquí se presentan casos reales de validación y extracción que combinan lookahead y lookbehind, destacando trucos y soluciones prácticas.
1. Contraseña segura con múltiples requisitos

Requisitos: al menos 8 caracteres, una mayúscula, una minúscula, un dígito y un carácter especial.
regex

^
(?=.*[a-z])      # al menos una minúscula
(?=.*[A-Z])      # al menos una mayúscula
(?=.*\d)         # al menos un dígito
(?=.*[#?!@$%^&*-]) # al menos un especial (lista ampliable)
.{8,}
$

Cada lookahead se ejecuta desde el inicio y verifica la presencia de cada tipo de carácter en cualquier parte de la cadena. La parte final .{8,} consume la contraseña completa.
2. Validar que una cadena NO contiene ciertas palabras prohibidas

Evitar que aparezca "admin" o "root" en un nombre de usuario, en cualquier posición.
regex

^(?!.*\badmin\b)(?!.*\broot\b)\w+$

Explicación: desde el inicio, (?!.*\badmin\b) asegura que en ningún lugar (gracias a .*) se encuentra la palabra completa admin. El segundo lookahead hace lo propio con root. Si ambos son negativos, la cadena es válida.
3. Buscar números que no formen parte de una fecha

Supongamos que queremos números que no estén precedidos por 20 ni seguidos por /. Entrada: "20/23 es diferente a 23".
regex

(?<!20\/)\d+(?!\/)

El (?<!20\/) exige que no esté precedido por 20/. El (?!\/) que no esté seguido de /. Así en 20/23, no coincidirá 23. En 23 aislado, sí.
4. Extraer monedas con símbolo y formato flotante

Texto: "El precio es $12.50, pero con descuento €9.99 y $10."

Extraer la cantidad numérica detrás del símbolo de moneda (sin capturar el símbolo) usando lookbehind positivo:
regex

(?<=[$€])\d+(?:\.\d{2})?

En motores con lookbehind variable (JS, .NET, regex Python), esto funciona sin problema. En Python re, si solo tenemos longitud fija, [$€] es un único carácter (longitud 1), así que también es válido. Coincide con 12.50, 9.99, 10.
5. Validar formato de usuario con restricciones en extremos

Un nombre de usuario debe tener entre 3 y 16 caracteres alfanuméricos y guiones, pero no puede empezar ni terminar con guión.
regex

^(?!-)[a-zA-Z0-9-]{3,16}(?<!-)$

El lookahead al inicio (?!-) prohíbe que el primer carácter sea un guión. El lookbehind al final (?<!-) prohíbe que el último carácter sea un guión. La parte central [a-zA-Z0-9-]+ permite combinaciones válidas.
6. Cadenas entre comillas con escapado interno

Buscar textos entrecomillados que soporten \" dentro:
regex

(?<!\\)"((?:[^"\\]|\\.)*)(?<!\\)"

    (?<!\\)" : comilla de apertura no escapada.

    (?:[^"\\]|\\.)* : contenido: o bien caracteres que no son comillas ni barras, o bien secuencias de escape.

    (?<!\\)" : comilla de cierre no escapada.

Este patrón utiliza dos lookbehinds negativos, útiles para ignorar comillas precedidas por barra invertida.
7. Números de teléfono con formato libre pero longitud exacta

Validar un teléfono de 10 dígitos, que pueda tener espacios o guiones separadores, pero al extraer ignoramos los no dígitos.
regex

^(?=.{10,15}$)\d[\d\s-]*\d$

El lookahead (?=.{10,15}$) impone un largo total entre 10 y 15 caracteres (para dar cabida a separadores). Luego \d al inicio y \d al final aseguran que extremos son dígitos. Finalmente, extraer solo dígitos con programación adicional.
8. Encontrar palabras que no estén precedidas por un punto (en código fuente)

En código, queremos seleccionar identificadores sueltos que no sean acceso a propiedad (ej: obj.metodo). Palabras que no van precedidas de punto.
regex

(?<!\.)\b[a-zA-Z_]\w*\b

El (?<!\.) garantiza que no haya un punto justo antes del identificador. El \b luego asegura que sea una palabra completa. Así obj.metodo no casará con metodo, pero metodo aislado sí.
9. Detectar números de tarjeta de crédito sin capturar el contexto

Extraer números de 16 dígitos (posiblemente separados en grupos de 4 con espacios o guiones) usando lookbehind y lookahead para asegurar que no están pegados a más dígitos.
regex

(?<!\d)(\d{4}[-\s]?){3}\d{4}(?!\d)

El (?<!\d) y (?!\d) funcionan como límites de dígito, garantizando que el número esté aislado.
10. Validar una IP v4 sin grupos de captura complicados

Podemos comprobar que cada octeto esté en el rango 0-255 usando lookbehind embebido? Mejor usar expresión normal, pero con lookahead podemos validar estructura:
regex

^(?=\d+\.\d+\.\d+\.\d+$)((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$

El lookahead inicial (?=\d+\.\d+\.\d+\.\d+$) solo verifica que haya 4 bloques numéricos separados por puntos, sin evaluar rangos. Luego la regex principal impone los rangos. Esto separa la validación de formato de la de valor.

Con estos contenidos, el bloque 04_aserciones queda completamente documentado, con explicaciones paso a paso y un banco de ejemplos prácticos para referencia inmediata.
Profundiza en estos temas
├── 05_flags_y_modos/
│   ├── 01_flags_comunes.md
│   ├── 02_modo_verboso.md
│   └── 03_unicode.md

We need to provide detailed content for the three files in the "05_flags_y_modos" block: 01_flags_comunes.md, 02_modo_verboso.md, and 03_unicode.md. The user expects thorough, in-depth explanations similar to the previous responses. We'll cover common flags (global, case-insensitive, multiline, dotall, etc.), verbose mode (extended), and Unicode handling (unicode flag, properties, scripts, normalization, etc.). We'll structure each file with definitions, examples, cross-engine differences, and practical uses.

Let's craft the content.

First, 01_flags_comunes.md:

    What are flags/modifiers? How they change regex behavior.

    List common flags: g (global), i (case-insensitive), m (multiline), s (dotall/single line), x (extended/verbose), u (unicode), A (ascii only in Python).

    For each flag, explain its effect, examples, how it's specified in different languages, and important considerations.

    Possibly mention flags that are engine-specific (like PCRE's J, X, etc., but we'll stick to widely available ones).

Second, 02_modo_verboso.md:

    What is verbose mode (flag x)? Allows whitespace and comments in regex.

    Syntax in various engines: Python re.X, JavaScript? JS does not have a native flag, but workarounds. PCRE uses (?x) or /x.

    Benefits: readability, documentation, breaking complex patterns into lines.

    Examples: complex pattern broken down with comments.

    How to match literal whitespace when using x: escape or use \s, put in character class.

    Mention global vs local (inline) mode: (?x) within pattern.

Third, 03_unicode.md:

    Unicode as a flag and as a mode.

    Unicode basics: code points, characters beyond ASCII.

    The 'u' flag: ECMAScript 2015, Python 3 default (str patterns), PCRE (?u) or PCRE2_U.

    How u flag affects \w, \d, \s, \b (word boundaries) to include Unicode letters/digits/whitespace.

    Case-insensitive matching with Unicode.

    Unicode property escapes: \p{...} and \P{...}, supported with u flag in JS, PCRE, .NET, Java, Python regex module. Categories (L, N, S, P, etc.), Script (Greek, Cyrillic, Han), Block (Basic_Latin).

    Normalization issues (NFC, NFD) and regex matching.

    Python's re module default behavior (Unicode by default in Python 3, but \w matches only ASCII letters unless re.UNICODE/re.ASCII flags are used). We'll clarify.

    Example of Unicode-aware word matching.

    Surrogate pairs in JavaScript (ES2015+ 'u' flag handles them properly).

    Performance considerations.

I'll structure each .md with headers and subheaders, code blocks, and tables as needed. The response will be the content for these three markdown files, just as before.

Let's write.

A continuación se desarrollan en profundidad los tres temas del bloque 05_flags_y_modos, con explicaciones, sintaxis según el motor y ejemplos de uso.
01_flags_comunes.md
¿Qué son las flags (modificadores)?

Las flags (o modificadores) son parámetros que alteran el comportamiento global de una expresión regular. Se suelen indicar fuera del patrón (por ejemplo, como segundo argumento en JavaScript, o como constante en Python) o, en algunos motores, dentro del mismo patrón con la sintaxis (?flags).

Cada flag activa una funcionalidad específica y puede combinarse con otras para ajustar con precisión cómo se realiza la búsqueda.
Flags fundamentales (compatibles en la mayoría de motores)
Flag	Nombre	Efecto
g	Global	Encuentra todas las coincidencias en lugar de detenerse en la primera.
i	Case-Insensitive	Ignora diferencias entre mayúsculas y minúsculas.
m	Multiline	Cambia el significado de ^ y $ para que coincidan con inicio/fin de cada línea, no solo de toda la cadena.
s	Dotall / Single line	Hace que el punto . coincida también con saltos de línea \n.
x	Extended / Verbose	Permite escribir el patrón con espacios y comentarios para mejorar la legibilidad.
u	Unicode	Activa el soporte completo de Unicode (afecta a \w, \b, propiedades, etc.).
A / a	ASCII-only (en Python)	Fuerza que \w, \d, \s, \b solo reconozcan caracteres ASCII.

No todos los motores soportan todas las flags ni con los mismos caracteres. A continuación se detalla cada una.
1. Global (g)

Propósito: Encontrar todas las ocurrencias del patrón en la cadena, no solo la primera.

    En JavaScript: /patrón/g

    En Python: No existe como flag. La función re.findall() o re.finditer() devuelven todas las coincidencias; re.search() y re.match() solo la primera. Algunas bibliotecas (como regex) aceptan regex.findall(patrón, texto) sin flag extra.

    En PHP/PCRE: preg_match_all() o usar el modificador g en preg_replace (que reemplaza todas por defecto).

Ejemplo en JavaScript:
javascript

let texto = "gato gato";
let regex = /gato/g;
texto.match(regex); // ["gato", "gato"]

Sin la flag g, .match() devuelve solo la primera coincidencia.
2. Case-Insensitive (i)

Propósito: Ignorar diferencias entre mayúsculas y minúsculas.

    /patrón/i (JS, Perl)

    re.IGNORECASE o re.I (Python)

    Pattern.compile("patrón", Pattern.CASE_INSENSITIVE) (Java)

    (?i) dentro del patrón en PCRE, .NET, Java, Python (módulo regex).

Ejemplo:
regex

/gato/i

Coincide con "gato", "Gato", "GATO", etc.

Importante: El efecto puede depender de la configuración regional y del soporte Unicode. Con la flag u también se manejan equivalencias de mayúsculas/minúsculas específicas de idiomas (ej: 'ß' coincide con 'SS' en modo Unicode en algunos motores).
3. Multiline (m)

Propósito: Cambia el comportamiento de las anclas ^ y $.

    Sin m: ^ coincide con el inicio de la cadena; $ con el final (o justo antes de un salto de línea final).

    Con m: ^ coincide con el inicio de la cadena e inmediatamente después de cada salto de línea; $ coincide con el final de la cadena e inmediatamente antes de cada salto de línea.

Ejemplo:
text

/^hola/m

Sobre el texto:
text

hola
adiós
hola mundo

Coincide con la primera y tercera línea.

Precaución: \A y \Z/\z no se ven afectados por m; siempre representan inicio/fin absolutos de la cadena.
4. Dotall / Single Line (s)

Propósito: El metacarácter . normalmente no coincide con saltos de línea (\n, y a veces \r). Con s, el punto los incluye, comportándose como [\s\S].

    JavaScript: /patrón/s (ES2018+)

    Python: re.DOTALL o re.S

    PCRE: (?s) o flag s después del delimitador.

Ejemplo:
regex

/a.b/s

"a\nb" coincide.

Sin s, a.b no coincidiría porque hay un salto de línea entre a y b.

Nota: Algunos motores tienen una flag m para multilínea y s para dotall. No confundir.
5. Otras flags importantes
x (Extended / Verbose)

Se trata en detalle en el siguiente archivo. Permite comentarios y espacios en el patrón.
u (Unicode)

Se aborda en profundidad en 03_unicode.md. Activa el tratamiento completo de caracteres Unicode.
A / a (ASCII-only)

Exclusiva de Python (módulo re). Fuerza que las secuencias \w, \W, \b, \B, \d, \D, \s, \S solo casen caracteres ASCII, en lugar de la configuración Unicode por defecto en Python 3.
python

import re
re.findall(r'\w+', 'cañón')   # ['cañón'] (Unicode)
re.findall(r'\w+', 'cañón', re.A)  # ['ca'] (ASCII, porque 'ñ' no es \w)

U (Ungreedy en PCRE)

En PCRE/Perl, U invierte la codicia: todos los cuantificadores se vuelven perezosos por defecto, y ? los hace codiciosos. Poco usado, puede confundir.
Especificación de flags según el lenguaje
Lenguaje / Motor	Cómo se indican	Ejemplo
JavaScript	Literal: /patrón/gi; Constructor: new RegExp("patrón", "gi")	/hola/i
Python re	Constante en re.compile() o funciones: re.IGNORECASE	re.findall(r'hola', texto, re.I)
Python regex	Igual que re, pero además soporta flags inline como (?i)	regex.compile(r'(?i)hola')
PHP (PCRE)	En el delimitador: /patrón/i o usando funciones preg_match(..., $flags)	preg_match('/hola/i', $texto)
Java	Pattern.compile("patrón", Pattern.CASE_INSENSITIVE | Pattern.MULTILINE)	Pattern.compile("hola", Pattern.CASE_INSENSITIVE)
.NET	RegexOptions en el constructor: RegexOptions.IgnoreCase	new Regex("hola", RegexOptions.IgnoreCase)
Perl	/patrón/gi	$texto =~ /hola/i
Inserción de flags dentro del patrón (modo inline)

Muchos motores permiten cambiar las flags en medio del patrón usando las sintaxis:

    (?i) – activa case-insensitive desde ese punto en adelante.

    (?-i) – lo desactiva.

    (?i:grupo) – afecta solo al grupo.

    (?is-m) – combina varias.

Esto permite granularidad sin modificar el resto.

Ejemplo (PCRE/Java/.NET/Python regex):
regex

hola (?i:mundo) cruel

Coincidirá con "hola Mundo cruel" y "hola MUNDO cruel", pero hola y cruel mantienen su sensibilidad normal.

Soporte en JavaScript: NO soporta flags inline. Solo se aplican globalmente en el constructor o literal.
02_modo_verboso.md
¿Qué es el modo verboso?

El modo verboso (flag x o re.VERBOSE) permite escribir expresiones regulares con espacios, tabulaciones, saltos de línea y comentarios, todo lo cual es ignorado por el motor. Así se pueden formatear patrones complejos de manera legible, como si fuera código con documentación embebida.
Motores que lo soportan

    Python: re.VERBOSE (o re.X)

    PCRE / PHP: flag x después del delimitador o (?x) dentro del patrón.

    Perl: /x

    .NET: RegexOptions.IgnorePatternWhitespace

    Java: Pattern.COMMENTS

    Ruby: opción x en Regexp.new

    JavaScript: NO lo soporta de manera nativa. Algunas bibliotecas (XRegExp) lo implementan. La alternativa es construir el patrón con literales de plantilla multilínea y concatenación, aunque los comentarios no se ignoran.

Reglas de ignorado en modo verboso

    Todos los espacios y tabuladores (excepto dentro de clases de caracteres [...]) son ignorados.

    Los saltos de línea son ignorados.

    Los comentarios comienzan con el carácter # y se extienden hasta el final de la línea (ese texto no es parte del patrón). Si se necesita un # literal, debe escaparse \# o incluirse en una clase [#].

Ventajas

    Patrones largos, como validación de contraseñas o direcciones, se vuelven autodocumentados.

    Facilita el mantenimiento y la colaboración.

    Permite desglosar patrones anidados en líneas separadas.

Ejemplo de patrón complejo tradicional vs. verboso

Validación de email simplificada (sin modo verboso):
regex

^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

Versión verbosa en Python:
python

import re

pattern = re.compile(r"""
    ^                      # inicio de cadena
    [a-zA-Z0-9._%+-]+      # parte local (nombre de usuario)
    @                      # símbolo arroba
    [a-zA-Z0-9.-]+         # dominio
    \.                     # punto literal
    [a-zA-Z]{2,}           # extensión (al menos 2 letras)
    $                      # final de cadena
""", re.VERBOSE)

Mucho más claro, especialmente si el patrón sigue creciendo.
Cómo incluir espacios o # literales en modo verboso

Hay que escapar los espacios (con \ o [ ]) y el símbolo # (con \#).

Ejemplo:
python

re.compile(r"""
    \d+        # uno o más dígitos
    [ ]        # un espacio en blanco literal (mejor usar \s si es espacio general)
    \#\d+      # almohadilla literal seguida de dígitos
""", re.VERBOSE)

También se puede usar \s cuando se quiere un espacio genérico, lo cual no se ve afectado por la supresión de espacios del modo verboso porque \s es una clase predefinida.
Ámbito del flag x

Se puede activar para todo el patrón (mediante la bandera externa o (?x) al inicio) o solo para una porción:

    (?x)patrón activa el modo.

    (?-x)patrón lo desactiva.

    (?x:patrón) aplica solo al grupo.

Esto es útil cuando solo una parte necesita comentarios o contiene muchos espacios que no deben ignorarse.
Ejemplo de combinación con otras flags

En Python:
python

re.compile(r"""
    ^
    (?=.*\d)    # al menos un dígito
    .{8,}
    $
""", re.VERBOSE | re.IGNORECASE)

En PCRE/PHP:
php

preg_match('/
    ^
    (?=.*\d)    # dígito
    .{8,}
    $
/xi', $texto);

Importante: En PCRE, los comentarios terminan con el final de la línea; no se puede poner nada tras # en esa línea, salvo que se usen delimitadores no usuales y todo vaya seguido.
Alternativas en JavaScript

Como JS carece de modo verboso, se puede usar una plantilla multilínea y unir:
javascript

let patrón = [
    '^',                    // inicio
    '[a-zA-Z0-9._%+-]+',    // usuario
    '@',
    '[a-zA-Z0-9.-]+',       // dominio
    '\\.',
    '[a-zA-Z]{2,}',
    '$'
].join('');
let regex = new RegExp(patrón);

No es tan limpio como los comentarios, pero ayuda a estructurar.
03_unicode.md
Unicode y las expresiones regulares

Originalmente, las regex trabajaban solo con el conjunto ASCII. Con la expansión global de la informática, el soporte Unicode se ha vuelto imprescindible. La flag u (Unicode) o configuraciones equivalentes activan la conciencia plena de caracteres multibyte, propiedades y categorías.
¿Qué cambia al activar el modo Unicode?

    \w, \d, \s, \b pasan a reconocer caracteres de cualquier alfabeto, no solo ASCII.

    Case-insensitive (i) se vuelve sensible a las reglas de mayúsculas/minúsculas de Unicode (por ejemplo, 'ß' coincide con 'SS', 'ς' con 'σ' según el contexto).

    \B (límites de no palabra) se adapta igual.

    Propiedades Unicode (\p{...}) se habilitan; sin la flag u, muchos motores no reconocen estas secuencias.

    El punto . coincide con cualquier punto de código Unicode, no solo con bytes.

    Las clases de caracteres invertidas y los rangos funcionan correctamente con puntos de código que exceden \uFFFF.

    En JavaScript, el modo u corrige el manejo de pares sustitutos (surrogate pairs) para caracteres como emojis.

Soporte por motor
Motor	Activación	Comportamiento por defecto
Python 3 (módulo re)	Unicode es el comportamiento por defecto para cadenas str. La flag re.ASCII fuerza modo ASCII.	\w incluye letras Unicode, \d solo ASCII por razones históricas (solo [0-9]), pero \s sí incluye espacios Unicode.
Python regex (externo)	Por defecto Unicode. Flags regex.U (por defecto), regex.A para ASCII.	Mucho más completo: \p{L} disponible.
JavaScript (ES2015+)	Flag u (/patrón/u).	Sin u, las expresiones tratan la cadena como unidades de código UTF-16. Con u, se procesa por puntos de código completos.
PCRE / PHP	(*UTF) o (?u) (PCRE2) o flag u (PHP).	En PCRE2, el modo Unicode se controla por PCRE2_UTF y PCRE2_UCP. PHP con u flag.
Java	Por defecto, Pattern.UNICODE_CHARACTER_CLASS para que \w etc. sean Unicode; si no, son ASCII. También (?U) para activarlo.	Se debe pasar Pattern.UNICODE_CHARACTER_CLASS o usar (?U).
.NET	Por defecto Unicode en todas las categorías.	\w reconoce letras Unicode; \b es Unicode. Se puede desactivar con RegexOptions.ECMAScript.
Perl	/u o use feature 'unicode_strings'.	Moderno: Unicode por defecto.
El estándar de propiedades Unicode: \p{...} y \P{...}

Permite seleccionar caracteres mediante sus propiedades definidas por el consorcio Unicode. Está disponible con la flag u (o en motores que lo soportan nativamente).

Sintaxis:

    \p{Property=Value} (forma canónica)

    \p{Value} (si es inequívoco)

    \P{...} (negación)

Principales categorías (abreviaturas):

    Letras: L (Letter), Lu (Uppercase), Ll (Lowercase), Lt (Titlecase), Lm (Modifier), Lo (Other).

    Números: N (Number), Nd (Digit), Nl (Letter number), No (Other number).

    Símbolos: S (Symbol), Sm (Math), Sc (Currency), Sk (Modifier), So (Other).

    Puntuación: P (Punctuation), Pd (Dash), Ps (Open), Pe (Close), etc.

    Separadores: Z (Separator), Zs (Space), Zl (Line), Zp (Paragraph).

    Marcas: M (Mark), Mn (Non-spacing), Mc (Spacing combining), Me (Enclosing).

Ejemplos:
regex

\p{L}+        # una o más letras de cualquier alfabeto
\p{Nd}+       # dígitos decimales (incluye dígitos de otras escrituras)
\p{Sc}        # símbolo de moneda (£, ¥, €, $, etc.)
\p{Emoji}     # emojis (en motores que soportan esta propiedad)

Scripts: \p{Script=Latin}, \p{Greek}, \p{Cyrillic}, \p{Han}, etc.

Bloques: \p{Block=Basic_Latin}, \p{Arabic}, etc. Cuidado: bloques ≠ scripts.
Uso en distintos motores

Python (módulo regex, no re estándar):
python

import regex
pat = regex.compile(r'\p{Lu}\p{Ll}+')  # palabra con inicial mayúscula

JavaScript (ES2018+):
javascript

let regex = /\p{Script=Greek}+/u;
"Σωκράτης".match(regex); // "Σωκράτης"

PCRE/PHP:
php

preg_match('/\p{Han}/u', '漢字'); // 1

Java:
java

Pattern p = Pattern.compile("\\p{IsLatin}");

Nota: En Python estándar (re), no se admiten \p{}, hay que usar regex (PyPI).
Unicode y clases invertidas

Con la flag Unicode, \W coincide con cualquier carácter que NO sea una letra o dígito Unicode, etc. Esto es mucho más amplio que el ASCII.
Límites de palabra (\b) y Unicode

\b se define en función de \w. Con Unicode, \b reconoce transiciones entre caracteres de palabra Unicode y no palabra. Ejemplo: en la cadena "Café au lait", \bcafé\b coincide correctamente porque é es \w Unicode.
Case-Insensitive y Unicode

La flag i en modo Unicode utiliza las reglas de plegado de mayúsculas/minúsculas de Unicode. Por ejemplo, /Straße/i coincide con "STRASSE" en alemán. Esto se controla con \p{Cased} o propiedades específicas.
Manejo de puntos de código suplementarios (> U+FFFF)

JavaScript sin flag u trata caracteres como '𝄞' (U+1D11E) como dos unidades de código \uD834\uDD1E. El punto . coincide con cada mitad, y cuantificadores pueden romper el carácter. Con /u, el motor trabaja a nivel de punto de código completo, así que . coincide con '𝄞' entero y {2} exige dos de estos símbolos.

Ejemplo JS:
javascript

/^.$/u.test('𝄞'); // true (un solo carácter)
/^.$/.test('𝄞');  // false (son dos unidades)

Normalización Unicode

La misma cadena puede ser representada de diferentes formas (NFC, NFD). Por ejemplo, 'ñ' puede ser U+00F1 o U+006E + U+0303. Las regex no normalizan automáticamente; es responsabilidad del programador comparar tras normalizar el texto con un método como text.normalize('NFC') en JavaScript o unicodedata.normalize('NFC', text) en Python.

Para hacer una regex que case con ambas formas, se puede combinar las posibilidades:
regex

n\u0303|ñ

Pero no es práctico. La recomendación es normalizar la entrada a NFC o NFD antes de aplicar la regex.
Rendimiento

El modo Unicode puede ser más lento por la gran cantidad de caracteres a considerar. Sin embargo, en la mayoría de casos, la diferencia es insignificante. Si solo trabajas con texto ASCII, usar flag A (Python) o no activar u puede aportar pequeñas optimizaciones.
Ejemplo completo: validación de nombre internacional
python

import regex

pat = regex.compile(r'^\p{Lu}\p{Ll}*(?:[-\s]\p{Lu}\p{Ll}*)*$')
# Ej: "José", "María Cristina", "Jean-Luc"
print(pat.match("José Ángel"))   # match

En JavaScript:
javascript

let nameRegex = /^\p{Lu}\p{Ll}*(?:[-\s]\p{Lu}\p{Ll}*)*$/u;
nameRegex.test("Jürgen Müller"); // true
/////////////////////////////////////////////////////////////////////////////

/5//////////////////////////////////////////////////////////////////////////////////////////
01_flags_comunes.md
¿Qué son las flags (modificadores)?

Las flags (o modificadores) son parámetros que alteran el comportamiento global de una expresión regular. Se suelen indicar fuera del patrón (por ejemplo, como segundo argumento en JavaScript, o como constante en Python) o, en algunos motores, dentro del mismo patrón con la sintaxis (?flags).

Cada flag activa una funcionalidad específica y puede combinarse con otras para ajustar con precisión cómo se realiza la búsqueda.
Flags fundamentales (compatibles en la mayoría de motores)
Flag	Nombre	Efecto
g	Global	Encuentra todas las coincidencias en lugar de detenerse en la primera.
i	Case-Insensitive	Ignora diferencias entre mayúsculas y minúsculas.
m	Multiline	Cambia el significado de ^ y $ para que coincidan con inicio/fin de cada línea, no solo de toda la cadena.
s	Dotall / Single line	Hace que el punto . coincida también con saltos de línea \n.
x	Extended / Verbose	Permite escribir el patrón con espacios y comentarios para mejorar la legibilidad.
u	Unicode	Activa el soporte completo de Unicode (afecta a \w, \b, propiedades, etc.).
A / a	ASCII-only (en Python)	Fuerza que \w, \d, \s, \b solo reconozcan caracteres ASCII.

No todos los motores soportan todas las flags ni con los mismos caracteres. A continuación se detalla cada una.
1. Global (g)

Propósito: Encontrar todas las ocurrencias del patrón en la cadena, no solo la primera.

    En JavaScript: /patrón/g

    En Python: No existe como flag. La función re.findall() o re.finditer() devuelven todas las coincidencias; re.search() y re.match() solo la primera. Algunas bibliotecas (como regex) aceptan regex.findall(patrón, texto) sin flag extra.

    En PHP/PCRE: preg_match_all() o usar el modificador g en preg_replace (que reemplaza todas por defecto).

Ejemplo en JavaScript:
javascript

let texto = "gato gato";
let regex = /gato/g;
texto.match(regex); // ["gato", "gato"]

Sin la flag g, .match() devuelve solo la primera coincidencia.
2. Case-Insensitive (i)

Propósito: Ignorar diferencias entre mayúsculas y minúsculas.

    /patrón/i (JS, Perl)

    re.IGNORECASE o re.I (Python)

    Pattern.compile("patrón", Pattern.CASE_INSENSITIVE) (Java)

    (?i) dentro del patrón en PCRE, .NET, Java, Python (módulo regex).

Ejemplo:
regex

/gato/i

Coincide con "gato", "Gato", "GATO", etc.

Importante: El efecto puede depender de la configuración regional y del soporte Unicode. Con la flag u también se manejan equivalencias de mayúsculas/minúsculas específicas de idiomas (ej: 'ß' coincide con 'SS' en modo Unicode en algunos motores).
3. Multiline (m)

Propósito: Cambia el comportamiento de las anclas ^ y $.

    Sin m: ^ coincide con el inicio de la cadena; $ con el final (o justo antes de un salto de línea final).

    Con m: ^ coincide con el inicio de la cadena e inmediatamente después de cada salto de línea; $ coincide con el final de la cadena e inmediatamente antes de cada salto de línea.

Ejemplo:
text

/^hola/m

Sobre el texto:
text

hola
adiós
hola mundo

Coincide con la primera y tercera línea.

Precaución: \A y \Z/\z no se ven afectados por m; siempre representan inicio/fin absolutos de la cadena.
4. Dotall / Single Line (s)

Propósito: El metacarácter . normalmente no coincide con saltos de línea (\n, y a veces \r). Con s, el punto los incluye, comportándose como [\s\S].

    JavaScript: /patrón/s (ES2018+)

    Python: re.DOTALL o re.S

    PCRE: (?s) o flag s después del delimitador.

Ejemplo:
regex

/a.b/s

"a\nb" coincide.

Sin s, a.b no coincidiría porque hay un salto de línea entre a y b.

Nota: Algunos motores tienen una flag m para multilínea y s para dotall. No confundir.
5. Otras flags importantes
x (Extended / Verbose)

Se trata en detalle en el siguiente archivo. Permite comentarios y espacios en el patrón.
u (Unicode)

Se aborda en profundidad en 03_unicode.md. Activa el tratamiento completo de caracteres Unicode.
A / a (ASCII-only)

Exclusiva de Python (módulo re). Fuerza que las secuencias \w, \W, \b, \B, \d, \D, \s, \S solo casen caracteres ASCII, en lugar de la configuración Unicode por defecto en Python 3.
python

import re
re.findall(r'\w+', 'cañón')   # ['cañón'] (Unicode)
re.findall(r'\w+', 'cañón', re.A)  # ['ca'] (ASCII, porque 'ñ' no es \w)

U (Ungreedy en PCRE)

En PCRE/Perl, U invierte la codicia: todos los cuantificadores se vuelven perezosos por defecto, y ? los hace codiciosos. Poco usado, puede confundir.
Especificación de flags según el lenguaje
Lenguaje / Motor	Cómo se indican	Ejemplo
JavaScript	Literal: /patrón/gi; Constructor: new RegExp("patrón", "gi")	/hola/i
Python re	Constante en re.compile() o funciones: re.IGNORECASE	re.findall(r'hola', texto, re.I)
Python regex	Igual que re, pero además soporta flags inline como (?i)	regex.compile(r'(?i)hola')
PHP (PCRE)	En el delimitador: /patrón/i o usando funciones preg_match(..., $flags)	preg_match('/hola/i', $texto)
Java	Pattern.compile("patrón", Pattern.CASE_INSENSITIVE | Pattern.MULTILINE)	Pattern.compile("hola", Pattern.CASE_INSENSITIVE)
.NET	RegexOptions en el constructor: RegexOptions.IgnoreCase	new Regex("hola", RegexOptions.IgnoreCase)
Perl	/patrón/gi	$texto =~ /hola/i
Inserción de flags dentro del patrón (modo inline)

Muchos motores permiten cambiar las flags en medio del patrón usando las sintaxis:

    (?i) – activa case-insensitive desde ese punto en adelante.

    (?-i) – lo desactiva.

    (?i:grupo) – afecta solo al grupo.

    (?is-m) – combina varias.

Esto permite granularidad sin modificar el resto.

Ejemplo (PCRE/Java/.NET/Python regex):
regex

hola (?i:mundo) cruel

Coincidirá con "hola Mundo cruel" y "hola MUNDO cruel", pero hola y cruel mantienen su sensibilidad normal.

Soporte en JavaScript: NO soporta flags inline. Solo se aplican globalmente en el constructor o literal.
02_modo_verboso.md
¿Qué es el modo verboso?

El modo verboso (flag x o re.VERBOSE) permite escribir expresiones regulares con espacios, tabulaciones, saltos de línea y comentarios, todo lo cual es ignorado por el motor. Así se pueden formatear patrones complejos de manera legible, como si fuera código con documentación embebida.
Motores que lo soportan

    Python: re.VERBOSE (o re.X)

    PCRE / PHP: flag x después del delimitador o (?x) dentro del patrón.

    Perl: /x

    .NET: RegexOptions.IgnorePatternWhitespace

    Java: Pattern.COMMENTS

    Ruby: opción x en Regexp.new

    JavaScript: NO lo soporta de manera nativa. Algunas bibliotecas (XRegExp) lo implementan. La alternativa es construir el patrón con literales de plantilla multilínea y concatenación, aunque los comentarios no se ignoran.

Reglas de ignorado en modo verboso

    Todos los espacios y tabuladores (excepto dentro de clases de caracteres [...]) son ignorados.

    Los saltos de línea son ignorados.

    Los comentarios comienzan con el carácter # y se extienden hasta el final de la línea (ese texto no es parte del patrón). Si se necesita un # literal, debe escaparse \# o incluirse en una clase [#].

Ventajas

    Patrones largos, como validación de contraseñas o direcciones, se vuelven autodocumentados.

    Facilita el mantenimiento y la colaboración.

    Permite desglosar patrones anidados en líneas separadas.

Ejemplo de patrón complejo tradicional vs. verboso

Validación de email simplificada (sin modo verboso):
regex

^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

Versión verbosa en Python:
python

import re

pattern = re.compile(r"""
    ^                      # inicio de cadena
    [a-zA-Z0-9._%+-]+      # parte local (nombre de usuario)
    @                      # símbolo arroba
    [a-zA-Z0-9.-]+         # dominio
    \.                     # punto literal
    [a-zA-Z]{2,}           # extensión (al menos 2 letras)
    $                      # final de cadena
""", re.VERBOSE)

Mucho más claro, especialmente si el patrón sigue creciendo.
Cómo incluir espacios o # literales en modo verboso

Hay que escapar los espacios (con \ o [ ]) y el símbolo # (con \#).

Ejemplo:
python

re.compile(r"""
    \d+        # uno o más dígitos
    [ ]        # un espacio en blanco literal (mejor usar \s si es espacio general)
    \#\d+      # almohadilla literal seguida de dígitos
""", re.VERBOSE)

También se puede usar \s cuando se quiere un espacio genérico, lo cual no se ve afectado por la supresión de espacios del modo verboso porque \s es una clase predefinida.
Ámbito del flag x

Se puede activar para todo el patrón (mediante la bandera externa o (?x) al inicio) o solo para una porción:

    (?x)patrón activa el modo.

    (?-x)patrón lo desactiva.

    (?x:patrón) aplica solo al grupo.

Esto es útil cuando solo una parte necesita comentarios o contiene muchos espacios que no deben ignorarse.
Ejemplo de combinación con otras flags

En Python:
python

re.compile(r"""
    ^
    (?=.*\d)    # al menos un dígito
    .{8,}
    $
""", re.VERBOSE | re.IGNORECASE)

En PCRE/PHP:
php

preg_match('/
    ^
    (?=.*\d)    # dígito
    .{8,}
    $
/xi', $texto);

Importante: En PCRE, los comentarios terminan con el final de la línea; no se puede poner nada tras # en esa línea, salvo que se usen delimitadores no usuales y todo vaya seguido.
Alternativas en JavaScript

Como JS carece de modo verboso, se puede usar una plantilla multilínea y unir:
javascript

let patrón = [
    '^',                    // inicio
    '[a-zA-Z0-9._%+-]+',    // usuario
    '@',
    '[a-zA-Z0-9.-]+',       // dominio
    '\\.',
    '[a-zA-Z]{2,}',
    '$'
].join('');
let regex = new RegExp(patrón);

No es tan limpio como los comentarios, pero ayuda a estructurar.
03_unicode.md
Unicode y las expresiones regulares

Originalmente, las regex trabajaban solo con el conjunto ASCII. Con la expansión global de la informática, el soporte Unicode se ha vuelto imprescindible. La flag u (Unicode) o configuraciones equivalentes activan la conciencia plena de caracteres multibyte, propiedades y categorías.
¿Qué cambia al activar el modo Unicode?

    \w, \d, \s, \b pasan a reconocer caracteres de cualquier alfabeto, no solo ASCII.

    Case-insensitive (i) se vuelve sensible a las reglas de mayúsculas/minúsculas de Unicode (por ejemplo, 'ß' coincide con 'SS', 'ς' con 'σ' según el contexto).

    \B (límites de no palabra) se adapta igual.

    Propiedades Unicode (\p{...}) se habilitan; sin la flag u, muchos motores no reconocen estas secuencias.

    El punto . coincide con cualquier punto de código Unicode, no solo con bytes.

    Las clases de caracteres invertidas y los rangos funcionan correctamente con puntos de código que exceden \uFFFF.

    En JavaScript, el modo u corrige el manejo de pares sustitutos (surrogate pairs) para caracteres como emojis.

Soporte por motor
Motor	Activación	Comportamiento por defecto
Python 3 (módulo re)	Unicode es el comportamiento por defecto para cadenas str. La flag re.ASCII fuerza modo ASCII.	\w incluye letras Unicode, \d solo ASCII por razones históricas (solo [0-9]), pero \s sí incluye espacios Unicode.
Python regex (externo)	Por defecto Unicode. Flags regex.U (por defecto), regex.A para ASCII.	Mucho más completo: \p{L} disponible.
JavaScript (ES2015+)	Flag u (/patrón/u).	Sin u, las expresiones tratan la cadena como unidades de código UTF-16. Con u, se procesa por puntos de código completos.
PCRE / PHP	(*UTF) o (?u) (PCRE2) o flag u (PHP).	En PCRE2, el modo Unicode se controla por PCRE2_UTF y PCRE2_UCP. PHP con u flag.
Java	Por defecto, Pattern.UNICODE_CHARACTER_CLASS para que \w etc. sean Unicode; si no, son ASCII. También (?U) para activarlo.	Se debe pasar Pattern.UNICODE_CHARACTER_CLASS o usar (?U).
.NET	Por defecto Unicode en todas las categorías.	\w reconoce letras Unicode; \b es Unicode. Se puede desactivar con RegexOptions.ECMAScript.
Perl	/u o use feature 'unicode_strings'.	Moderno: Unicode por defecto.
El estándar de propiedades Unicode: \p{...} y \P{...}

Permite seleccionar caracteres mediante sus propiedades definidas por el consorcio Unicode. Está disponible con la flag u (o en motores que lo soportan nativamente).

Sintaxis:

    \p{Property=Value} (forma canónica)

    \p{Value} (si es inequívoco)

    \P{...} (negación)

Principales categorías (abreviaturas):

    Letras: L (Letter), Lu (Uppercase), Ll (Lowercase), Lt (Titlecase), Lm (Modifier), Lo (Other).

    Números: N (Number), Nd (Digit), Nl (Letter number), No (Other number).

    Símbolos: S (Symbol), Sm (Math), Sc (Currency), Sk (Modifier), So (Other).

    Puntuación: P (Punctuation), Pd (Dash), Ps (Open), Pe (Close), etc.

    Separadores: Z (Separator), Zs (Space), Zl (Line), Zp (Paragraph).

    Marcas: M (Mark), Mn (Non-spacing), Mc (Spacing combining), Me (Enclosing).

Ejemplos:
regex

\p{L}+        # una o más letras de cualquier alfabeto
\p{Nd}+       # dígitos decimales (incluye dígitos de otras escrituras)
\p{Sc}        # símbolo de moneda (£, ¥, €, $, etc.)
\p{Emoji}     # emojis (en motores que soportan esta propiedad)

Scripts: \p{Script=Latin}, \p{Greek}, \p{Cyrillic}, \p{Han}, etc.

Bloques: \p{Block=Basic_Latin}, \p{Arabic}, etc. Cuidado: bloques ≠ scripts.
Uso en distintos motores

Python (módulo regex, no re estándar):
python

import regex
pat = regex.compile(r'\p{Lu}\p{Ll}+')  # palabra con inicial mayúscula

JavaScript (ES2018+):
javascript

let regex = /\p{Script=Greek}+/u;
"Σωκράτης".match(regex); // "Σωκράτης"

PCRE/PHP:
php

preg_match('/\p{Han}/u', '漢字'); // 1

Java:
java

Pattern p = Pattern.compile("\\p{IsLatin}");

Nota: En Python estándar (re), no se admiten \p{}, hay que usar regex (PyPI).
Unicode y clases invertidas

Con la flag Unicode, \W coincide con cualquier carácter que NO sea una letra o dígito Unicode, etc. Esto es mucho más amplio que el ASCII.
Límites de palabra (\b) y Unicode

\b se define en función de \w. Con Unicode, \b reconoce transiciones entre caracteres de palabra Unicode y no palabra. Ejemplo: en la cadena "Café au lait", \bcafé\b coincide correctamente porque é es \w Unicode.
Case-Insensitive y Unicode

La flag i en modo Unicode utiliza las reglas de plegado de mayúsculas/minúsculas de Unicode. Por ejemplo, /Straße/i coincide con "STRASSE" en alemán. Esto se controla con \p{Cased} o propiedades específicas.
Manejo de puntos de código suplementarios (> U+FFFF)

JavaScript sin flag u trata caracteres como '𝄞' (U+1D11E) como dos unidades de código \uD834\uDD1E. El punto . coincide con cada mitad, y cuantificadores pueden romper el carácter. Con /u, el motor trabaja a nivel de punto de código completo, así que . coincide con '𝄞' entero y {2} exige dos de estos símbolos.

Ejemplo JS:
javascript

/^.$/u.test('𝄞'); // true (un solo carácter)
/^.$/.test('𝄞');  // false (son dos unidades)

Normalización Unicode

La misma cadena puede ser representada de diferentes formas (NFC, NFD). Por ejemplo, 'ñ' puede ser U+00F1 o U+006E + U+0303. Las regex no normalizan automáticamente; es responsabilidad del programador comparar tras normalizar el texto con un método como text.normalize('NFC') en JavaScript o unicodedata.normalize('NFC', text) en Python.

Para hacer una regex que case con ambas formas, se puede combinar las posibilidades:
regex

n\u0303|ñ

Pero no es práctico. La recomendación es normalizar la entrada a NFC o NFD antes de aplicar la regex.
Rendimiento

El modo Unicode puede ser más lento por la gran cantidad de caracteres a considerar. Sin embargo, en la mayoría de casos, la diferencia es insignificante. Si solo trabajas con texto ASCII, usar flag A (Python) o no activar u puede aportar pequeñas optimizaciones.
Ejemplo completo: validación de nombre internacional
python

import regex

pat = regex.compile(r'^\p{Lu}\p{Ll}*(?:[-\s]\p{Lu}\p{Ll}*)*$')
# Ej: "José", "María Cristina", "Jean-Luc"
print(pat.match("José Ángel"))   # match

En JavaScript:
javascript

let nameRegex = /^\p{Lu}\p{Ll}*(?:[-\s]\p{Lu}\p{Ll}*)*$/u;
nameRegex.test("Jürgen Müller"); // true


/////////////////////////////////////////////////////////////////////////////

/6//////////////////////////////////////////////////////////////////////////////////////////
01_recursion_y_subrutinas.md
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
02_condicionales.md
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

03_propiedades_unicode.md
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

04_backtracking_catastrofico.md
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
05_optimizacion.md
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

/////////////////////////////////////////////////////////////////////////////

/7//////////////////////////////////////////////////////////////////////////////////////////
01_validacion_emails.md
La complejidad de validar un correo electrónico

Validar un email con una expresión regular que cumpla rigurosamente el RFC 5321/5322 es extremadamente complejo. La especificación permite una sintaxis muy amplia (caracteres especiales, quoted strings, comentarios anidados, etc.), que en la práctica casi ningún servicio implementa. Por ello, la mayoría de las aplicaciones utilizan patrones pragmáticos, que cubren el >99% de los casos reales y rechazan formatos absurdos.
Patrón básico (muy tolerante)

Acepta la estructura algo@algo.algo con caracteres alfanuméricos y algunos símbolos. No es estricto pero muy popular.
regex

^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

    Parte local: letras, dígitos, puntos, guiones bajos, porcentajes, más, menos.

    Dominio: letras, dígitos, puntos, guiones.

    Extensión: al menos dos letras.
    Es simple, rechaza espacios y caracteres exóticos, pero permite dominios como algo..com (doble punto) o guiones al inicio/fin, aunque en la mayoría de casos prácticos no es problemático.

Patrón mejorado, con restricciones comunes
regex

^[a-zA-Z0-9]+(?:[._%+-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z]{2,})+$

    La parte local empieza y acaba con alfanumérico, permite un separador entre bloques alfanuméricos.

    El dominio prohíbe guiones al inicio, permite segmentos separados por punto, y al menos un punto con extensión de letras.

    Evita dobles puntos y otras combinaciones inválidas.

Patrón avanzado (cercano al RFC, pero práctico)
regex

^(?=.{1,254}$)(?=.{1,64}@)[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$

    Limita la longitud total a 254 caracteres (máximo estándar) y la parte local a 64.

    Permite un conjunto ampliado de caracteres especiales en la parte local.

    Dominio: cada etiqueta (subdominio) debe tener entre 1 y 63 caracteres, sin empezar ni terminar con guión.

    Exige TLD de al menos 2 letras (no valida TLDs reales, eso se haría contra una lista externa).
    Es largo pero robusto para validación en backend.

Nota: En JavaScript este patrón puede usarse con la flag u si se esperan caracteres Unicode, pero entonces la parte local permitiría caracteres internacionales según el estándar (aunque no todos los servidores los aceptan). Una versión con soporte internacional usaría \p{L} en lugar de a-zA-Z, pero la complejidad crece.
Validación por pasos (recomendada)

Muchas veces es mejor hacer una validación básica con regex y luego comprobar existencia del dominio vía DNS o enviar un correo de confirmación. La regex solo debería garantizar que el formato es plausible.
Consideraciones por motor

    JavaScript: Para TLDs con caracteres internacionalizados (IDN), usar [\p{L}]{2,} con la flag u.

    Python: re estándar es suficiente; para IDN, usar el módulo regex.

    Java/PCRE: Similar a los patrones anteriores.

Ejemplos de testeo
javascript

const emailRegex = /^[a-zA-Z0-9]+(?:[._%+-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z]{2,})+$/;
emailRegex.test("usuario@dominio.co.uk"); // true
emailRegex.test("usuario@sub.dominio.com"); // true
emailRegex.test("usuario@dominio..com"); // false (doble punto)
emailRegex.test("usuario@-dominio.com"); // false (guion al inicio)

Límites y extensiones

Si necesitas soporte para comentarios (RFC 5322) o quoted strings, la regex se vuelve monstruosa; es mejor utilizar una biblioteca específica. Para la mayoría de aplicaciones, el patrón mejorado es suficiente y seguro.
02_urls.md
¿Qué es una URL?

Una URL estándar (HTTP/HTTPS) sigue la estructura:
protocolo://[usuario:contraseña@]dominio[:puerto]/[ruta]?[query]#[fragmento]
Los patrones regex pueden capturar todos o algunos de estos componentes.
Patrón básico para extraer URLs de un texto
regex

https?://[^\s/$.?#].[^\s]*

    https?:// exige el protocolo.

    [^\s/$.?#] obliga a que el primer carácter del dominio no sea espacio ni algunos símbolos.

    [^\s]* consume todo hasta un espacio en blanco.
    Esto captura la mayoría de URLs en textos planos, pero puede incluir paréntesis o puntos finales no deseados.

Patrón más robusto que delimita con caracteres de puntuación
regex

https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?::\d+)?(?:/[^\s]*)?

    Dominio: nombre de host con letras, dígitos, guiones, puntos, y soporte para caracteres escapados con %.

    Puerto opcional :\d+.

    Ruta opcional: cualquier cosa sin espacios.
    Mejor que el básico, pero puede seguir capturando un punto final como parte de la URL.

Extracción precisa con límites por paréntesis y comillas

En entornos controlados como HTML, se puede usar un patrón que respete los delimitadores naturales:
regex

(?:"|')((?:https?|ftp)://[^"'\s]+)(?:"|')   // entre comillas
(?:href|src)=["']?((?:https?|ftp)://[^"'\s>]+) // atributos HTML

Validación de una URL completa

El siguiente patrón verifica el formato e impone que la URL no esté mal construida:
regex

^https?://([\w\-]+\.)+[\w\-]+(:\d+)?(/[\w\-./?%&=+#]*)?$

    Protocolo obligatorio.

    Dominio con al menos un punto y segmentos.

    Puerto opcional.

    Ruta opcional con caracteres válidos.
    Es útil para validar entradas de usuario donde se espera una URL absoluta.

Soporte para dominios internacionalizados (IDN)

En dominios pueden aparecer caracteres Unicode (ej. http://españa.es). Para capturarlos:
regex

https?://(?:[-\p{L}\p{N}_]|(?:%[\da-fA-F]{2}))+\.(?:\p{L}{2,})(?::\d+)?(?:/[^\s]*)?

(Requiere flag u en JavaScript, y \p{L} en PCRE/Python regex).
Fragmentos y query string

Si quieres analizar los componentes, usa grupos de captura:
regex

^(https?)://([\w\-\.]+)(?::(\d+))?(/[^?#]*)?(?:\?([^#]*))?(?:#(.*))?$

Grupos:

    protocolo

    host

    puerto

    ruta

    query string

    fragmento

Ejemplos prácticos en código

Extraer todas las URLs de un texto (JavaScript):
javascript

let urlRegex = /https?:\/\/[^\s/$.?#].[^\s]*/g;
let matches = texto.match(urlRegex);
// Limpiar puntuación final con slice si es necesario.

Validar URL en Python:
python

import re
pat = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(:\d+)?(/[-\w./?%&=+#]*)?$'
re.match(pat, url) is not None

Consideraciones y limitaciones

    Estas regex no validan que el TLD sea real (por ejemplo, .com, .es). Para una validación rigurosa, se necesita una lista de TLDs actualizada.

    Tampoco restringen caracteres ilegales en la ruta según el contexto (como espacios sin codificar). Para eso se debe escapar o usar encodeURI.

    En entornos donde se permiten fragmentos, ten cuidado con los caracteres # internos.

03_fechas_y_horas.md
Formatos comunes de fecha

Las fechas varían enormemente según la región. Los patrones más comunes incluyen:

    ISO 8601: YYYY-MM-DD (recomendado para sistemas)

    Europeo: DD/MM/YYYY

    EE.UU.: MM/DD/YYYY

    Formato largo: 12 de enero de 2024
    Cada uno requiere un patrón específico.

Patrón para fecha ISO estándar
regex

^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$

    Año: cuatro dígitos.

    Mes: 01-12.

    Día: 01-31 (no valida meses con menos días; esto es un problema).
    Limitación: Acepta 2023-02-31. Para validar días por mes se necesita una lógica más compleja, que puede hacerse con alternancia o condicionales en regex avanzadas, pero generalmente es mejor validar con código.

Validación estricta de fecha (incluyendo febrero)
regex

^(?:\d{4}-(?:(?:0[13578]|1[02])-31|(?:0[1,3-9]|1[0-2])-(?:29|30)|(?:0[1-9]|1\d|2[0-8])-(?:0[1-9]|1\d|2[0-8]))|(?:(?:\d{2}(?:0[48]|[2468][048]|[13579][26])|(?:[02468][048]|[13579][26])00)-02-29)$

Este patrón valida fechas en formato YYYY-MM-DD, incluyendo bisiestos para febrero. Es bastante ilegible; se recomienda usar código en su lugar.

Alternativa híbrida: usar una regex simple para el formato y luego una función para validar rangos.
python

import re
from datetime import datetime
def validar_fecha(texto):
    if re.match(r'^\d{4}-\d{2}-\d{2}$', texto):
        try:
            datetime.strptime(texto, '%Y-%m-%d')
            return True
        except ValueError:
            pass
    return False

Fechas en formato DD/MM/YYYY o MM/DD/YYYY

    DD/MM/YYYY: ^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/\d{4}$
    (Con separadores / o - intercambiables usando grupo: [-/]).

    MM/DD/YYYY: ^(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/\d{4}$
    Ninguno distingue entre meses de 30 o 31 días.

Horas en formato 24h y 12h

    24 horas: ^(?:[01]\d|2[0-3]):[0-5]\d$ (sin segundos)
    Con segundos: ^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$

    12 horas (AM/PM): ^(?:1[0-2]|0?[1-9]):[0-5]\d(?::[0-5]\d)?\s?[APap][Mm]$

Fecha y hora combinadas (ISO 8601 completo)
regex

^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$

Ejemplo: 2023-10-05T14:30:00Z, 2024-01-01T00:00:00+01:00.

    La parte decimal de segundos es opcional.

    Zona horaria Z o offset.

Extracción de fechas en texto libre

Para encontrar fechas en formato DD de Mes de YYYY (español), se puede usar:
regex

\b(\d{1,2})\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+de\s+(\d{4})\b

Grupos capturan día, mes y año.
Consideraciones de regionalización

    En aplicaciones web, se debe saber de antemano el formato esperado; no intentar adivinar entre múltiples formatos con una sola regex.

    Los nombres de meses y días de la semana son dependientes del idioma.

    Las regex son una herramienta de pre-validación; la validación final debe usar las funciones de fecha del lenguaje.

04_numeros_y_monedas.md
Números enteros y decimales básicos

    Entero (positivo y negativo): ^-?\d+$

    Decimal con punto: ^-?\d+\.\d+$

    Decimal con posible parte decimal opcional: ^-?\d+(?:\.\d+)?$

    Notación científica: ^-?\d+(?:\.\d+)?[eE][+-]?\d+$

Números con separadores de miles

Formato estándar con coma para miles y punto decimal (ej. 1,234.56):
regex

^-?\d{1,3}(?:,\d{3})*(?:\.\d{2})?$

Variante con espacio como separador de miles y coma decimal (ej. 1 234,56):
regex

^-?\d{1,3}(?:[ ]\d{3})*(?:,\d{2})?$

Combinando ambos (poco común) se puede permitir tanto coma como punto mediante un patrón más complejo.
Monedas con símbolo

    Dólar/euro con símbolo prefijo: ^\$\s?-?\d+(?:\.\d{2})?$ o ^[€$]\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?$

    Símbolo al final (ej. 100€): ^\d+(?:\.\d{2})?\s?[€$]$

    Con código de moneda: ^[A-Z]{3}\s?\d+(?:\.\d{2})?$

Extracción flexible de cantidades monetarias en texto
regex

(?:[\$\€\£]|USD|EUR)?\s?\d{1,3}(?:[,.]\d{3})*(?:\.\d{2})?(?:\s?(?:€|USD))?

Esto captura cantidades como $1,000.50, 2000 EUR, 3.500,75 € (con formato europeo, pero se confundiría con separador de miles). La ambigüedad entre millares y decimales puede resolverse con un patrón más inteligente que detecte el último punto/coma como decimal.

Patrón que supone que el último separador especial es el decimal:
regex

[-+]?\d{1,3}(?:[.,]\d{3})*[.,]\d{2}\b

Pero fallaría si no hay decimales. Para cantidades sin decimales: \b\d{1,3}(?:[.,]\d{3})+\b (sin decimales).
Porcentajes
regex

^-?\d+(?:\.\d+)?%$

O con restricción de rango 0-100: no es práctico con regex pura; mejor validar después.
Validaciones adicionales

    No permitir ceros a la izquierda (excepto el número 0 o 0.xx): ^(?:0|[1-9]\d*)(?:\.\d+)?$

    Números negativos precisos: el signo menos solo al inicio.

Optimizaciones y compatibilidad

    Todos estos patrones funcionan en cualquier motor con pequeñas adaptaciones (escapado de $, uso de \d).

    Para aplicaciones financieras, valida la cantidad con regex y después conviértela a un tipo numérico para comprobar límites.

    No uses regex para sumas o comparaciones, solo para formato.

Ejemplos prácticos

Python: extraer todos los precios en euros de un texto
python

import re
pat = r'(\d{1,3}(?:\.\d{3})*,\d{2})\s?€|\d{1,3}(?:,\d{3})*\.\d{2}\s?EUR'
precios = re.findall(pat, texto)

JavaScript: validar número de teléfono (aunque no es moneda) y monedas
javascript

const moneyRegex = /^\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?$/;
moneyRegex.test("$1,234.56"); // true

05_contrasenas.md
Requisitos típicos de una contraseña segura

    Longitud mínima (generalmente 8 o más caracteres).

    Al menos una letra mayúscula.

    Al menos una letra minúscula.

    Al menos un dígito.

    Al menos un carácter especial (símbolos como !@#$%^&*).

Estos requisitos se expresan elegantemente con lookaheads al inicio del patrón.
Patrón estándar con lookaheads
regex

^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]|\p{P}|_?).{8,}$

Cada lookahead verifica la presencia de una categoría en cualquier parte de la cadena. Después, .{8,} consume toda la contraseña.

Versión explícita y legible (desglosada):
regex

^
  (?=.*[a-z])      # al menos una minúscula
  (?=.*[A-Z])      # al menos una mayúscula
  (?=.*\d)         # al menos un dígito
  (?=.*[#?!@$%^&*-]) # al menos un carácter especial de una lista concreta
  .{8,}            # longitud mínima 8
$

Nota sobre caracteres especiales: En lugar de [^\w\s], es mejor definir explícitamente el conjunto permitido para evitar caracteres no imprimibles. Por ejemplo: [!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?] o una lista acotada.
Longitud mínima y máxima
regex

^.{8,32}$

Combinado con los lookaheads para restringir composición.
Prohibir caracteres repetidos o secuencias

    No permitir 3 o más caracteres idénticos seguidos: (?!.*(.)\1{2,})

    No permitir secuencias de teclado como "qwerty": difícil con regex pura, mejor verificar con código.

Contraseñas que excluyen ciertos patrones (por ejemplo, el nombre de usuario)

Si se tiene el nombre de usuario, se puede construir la regex dinámicamente para rechazarlo. Por ejemplo, en JavaScript:
javascript

let user = "john";
let passRegex = new RegExp(`^(?!.*${user})(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).{8,}$`, 'i');

El lookahead negativo (?!.*${user}) prohíbe la aparición del nombre de usuario en cualquier parte de la contraseña.
Sin necesidad de lookaheads (motores limitados)

Si el motor no soporta lookaheads (POSIX), no se pueden hacer estas comprobaciones en una sola regex. Se usarían varias comprobaciones secuenciales:
bash

grep -E '.{8,}' fichero | grep -E '[a-z]' | grep -E '[A-Z]' | grep -E '[0-9]' | grep -E '[^a-zA-Z0-9]'

Exigir que al menos N de M condiciones se cumplan

Para requerir, por ejemplo, al menos 3 de 4 categorías, se puede usar una combinatoria de lookaheads que sumen. Por ejemplo, usando grupos y alternancia con (?=.*[a-z])(?=.*[A-Z])(?=.*\d)|(?=.*[a-z])(?=.*[A-Z])(?=.*[especial])|.... Sin embargo, es más limpio hacerlo con código.
Patrón para contraseña con todas las categorías y longitud exacta de 8 a 20
regex

^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,20}$

Compatibilidad y limitaciones

    Los lookaheads funcionan en todos los motores modernos (salvo POSIX). En JavaScript, disponibles desde siempre.

    La parte .{8,} podría permitir saltos de línea si no se especifica; normalmente en campos de contraseña no hay \n, pero es seguro usar [\s\S]{8,} o limitar a caracteres visibles.

    Los caracteres Unicode están permitidos si usamos \p{L} etc., pero muchas aplicaciones restringen a ASCII.

Buenas prácticas

    No almacenar los requisitos solo en la regex; acompañar con explicación textual al usuario.

    Permitir espacios al final/inicio no suele ser deseable; usar ^\S{8,}$ si se prohíben espacios.

    Para entornos de alta seguridad, la complejidad se mide con entropía, no con reglas fijas. La regex solo es una primera validación.

Ejemplo completo Python (usando módulo re)
python

import re
password = "MiClave123!"
patron = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$')
if patron.match(password):
    print("Contraseña válida")

06_extractores_texto.md
Extracción de hashtags (#etiqueta)
regex

(?<![^\s])#[a-zA-Z0-9_áéíóúüñ]+

O con soporte Unicode (\p{L}):
regex

(?<!\S)#[\p{L}\p{N}_]+

    El lookbehind (?<!\S) o (?<=\s|^) asegura que la almohadilla esté al inicio o precedida de espacio.

    Permite letras, números y guiones bajos; ajusta según el caso.

Menciones @usuario
regex

(?<!\S)@[a-zA-Z0-9_]+

Puede refinarse para aceptar puntos o guiones según la red social.
Extracción de palabras entre comillas

Para obtener texto dentro de comillas dobles, respetando escapes básicos:
regex

"((?:[^"\\]|\\.)*)"

Para comillas simples:
regex

'((?:[^'\\]|\\.)*)'

El grupo 1 contiene el texto interior.
Extracción de URLs (visto anteriormente)

Recapitulando:
regex

https?://[^\s/$.?#].[^\s]*

Con lookbehind para evitar capturar desde mitad de palabra:
regex

(?<!\S)(https?://[^\s]+)

Direcciones de correo electrónico en texto
regex

[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

Números de teléfono (formato genérico)
regex

(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4

Captura formatos como 123-456-7890, (123) 456-7890, +1-123-456-7890.
Extracción de fechas (sencilla)
regex

\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{4}-\d{1,2}-\d{1,2}\b

Extracción de palabras clave que empiezan con mayúscula (posibles nombres propios)
regex

\b\p{Lu}\p{L}*\b

Requiere flag u en JavaScript, y \p{Lu} en PCRE/Python regex.
Patrones para logs comunes

Log de Apache (formato común)
regex

^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d+) (\d+|-)

Grupos: IP, ident, usuario, fecha, petición, código, tamaño.
Extracción de código postal de varios países

    España (5 dígitos): \b\d{5}\b

    EE.UU. (5 dígitos o 5+4): \b\d{5}(?:-\d{4})?\b

    Reino Unido (formato complejo): \b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b

Extracción de etiquetas HTML simples
regex

<\/?([a-zA-Z][a-zA-Z0-9]*)[^>]*>

Obtiene la etiqueta en el grupo 1.
Extracción de contenido entre tags específicos

Para extraer el texto dentro de <title>...</title>:
regex

<title[^>]*>(.*?)</title>

Extracción de todos los números decimales de un texto
regex

\d+\.\d+|\d+

Pero cuidado, porque capturaría fechas como 2023.10.05 como dos números. Se puede afinar con límites.
Consejos para extractores eficientes

    Siempre usar clases negadas en lugar de .*? cuando sea posible: <tag([^>]*)> en lugar de <tag.*?>.

    Utilizar lookaheads/lookbehinds para aislar sin consumir contexto.

    En procesamiento pesado, dividir el texto con split y aplicar regex simples es más rápido que una super-regex.

Ejemplo combinado: extraer enlaces, menciones y hashtags de un tweet
javascript

let tweet = "Aprendiendo #regex con @usuario visita https://regex101.com";
let patterns = {
    hashtag: /#[\w]+/g,
    mention: /@[\w]+/g,
    url: /https?:\/\/[^\s]+/g
};
console.log(tweet.match(patterns.hashtag)); // ["#regex"]
console.log(tweet.match(patterns.mention)); // ["@usuario"]
console.log(tweet.match(patterns.url));     // ["https://regex101.com"]


/////////////////////////////////////////////////////////////////////////////

/8//////////////////////////////////////////////////////////////////////////////////////////
01_basicos.md
Instrucciones

Escribe una expresión regular para cada uno de los siguientes problemas. Si el motor lo requiere, especifica las banderas. Prueba tus patrones en un probador online (regex101.com, pythex.org) con los casos de ejemplo.

1. Buscar la palabra "gato"
Encuentra todas las apariciones de la palabra "gato" en una frase, sin distinguir mayúsculas/minúsculas. Debe coincidir como palabra completa.
text

Test: "El gato y el GATO gatean"
Coincidencias esperadas: "gato", "GATO"

2. Validar un código de área de EE.UU.
Formato: tres dígitos entre paréntesis (seguidos de espacio y tres dígitos adicionales, pero solo valida el código de área). Por ejemplo, "(123) " debe coincidir.
text

Test: "(123) 456-7890"  -> match "(123) "
Test: "(12) 345"        -> no match

3. Encontrar todas las palabras que terminan en "ción"
Coincide con palabras completas que tengan la terminación "ción" (ej. "canción", "acción"). Ignora mayúsculas/minúsculas.
text

Test: "La canción y la ACCIÓN fueron bien."
Coincidencias: "canción", "ACCIÓN"

4. Validar una fecha en formato DD/MM/AAAA
Día de 01 a 31, mes de 01 a 12, año de 4 dígitos. No hace falta validar días por mes (p.ej. 31/02/2023 es válido para este ejercicio).
text

Test: "15/08/2024" -> match
Test: "5/8/2024"   -> no match (exige dos dígitos)

5. Encontrar todas las vocales
Extrae todas las vocales (tanto mayúsculas como minúsculas) de un texto.
text

Test: "Hola Mundo" -> ["o", "a", "u", "o"]

6. Reemplazar múltiples espacios por uno solo
Escribe un patrón que capture cualquier secuencia de uno o más espacios en blanco (espacio, tabulador, salto de línea) para luego reemplazarlas por un solo espacio.
text

Test: "Hola    mundo.\t\tAdiós"
Después del reemplazo: "Hola mundo. Adiós"

7. Validar un nombre de usuario alfanumérico
Debe tener entre 4 y 16 caracteres, compuestos únicamente por letras (mayúsculas y minúsculas) y dígitos. No puede contener espacios ni símbolos.
text

Test: "usuario123" -> válido
Test: "user name"  -> inválido

8. Extraer extensiones de archivo
De una lista de nombres de archivo, extrae la extensión (sin el punto). Solo debe capturar extensiones de letras (no números al final). Por ejemplo: "imagen.jpg", "documento.pdf", "script.js".
text

Test: "foto.png"     -> extensión "png"
Test: "archivo.tar.gz" -> extensión "gz" (la última)

9. Buscar líneas que comienzan con "Error"
Procesa un texto multilínea y selecciona todas las líneas que empiezan por la palabra "Error" (sin importar mayúsculas/minúsculas). La palabra debe estar al inicio de la línea.
text

Test:
Todo bien
Error: fallo crítico
WARNING: revisar
error menor
Se espera coincidencia en la segunda línea: "Error: fallo crítico"

10. Validar un número decimal simple
Formato: puede tener un signo negativo opcional, dígitos enteros obligatorios, y opcionalmente un punto seguido de uno o más dígitos decimales. Ej: "-3.14", "10", "0.5". No permite múltiples puntos ni caracteres extra.
text

Test: "42"        -> válido
Test: "-.5"       -> inválido (falta entero)
Test: "1.2.3"     -> inválido

02_intermedios.md
Instrucciones

Estos ejercicios profundizan en cuantificadores perezosos, grupos de captura, lookahead/lookbehind, y patrones prácticos. Proporciona la regex y una breve explicación de su funcionamiento.

1. Extraer el texto dentro de etiquetas HTML <strong>
Dado un fragmento HTML, captura el contenido que está entre <strong> y </strong>, incluyendo posibles espacios y otras etiquetas internas, pero usando cuantificador perezoso para obtener cada bloque por separado.
text

Test: "<strong>Nota:</strong> esto es <strong>importante</strong>"
Coincidencia 1: "Nota:"  Coincidencia 2: "importante"

2. Validar un email con el patrón mejorado
Escribe una regex que valide un correo electrónico con las siguientes reglas:

    Parte local: caracteres alfanuméricos, puntos, guiones bajos, guiones, porcentajes y signos más. No puede empezar ni terminar con punto ni tener dos puntos consecutivos.

    Dominio: letras, dígitos, guiones; separado por puntos; el TLD debe tener al menos dos letras.

(Usa el patrón mejorado visto en los apuntes, no el básico.)
text

Test: "usuario@dominio.com"       -> válido
Test: "usuario@sub.dom.co.uk"    -> válido
Test: "usuario@dominio..com"     -> inválido
Test: ".usuario@dominio.com"     -> inválido

3. Buscar palabras que no están precedidas por el signo @
Encuentra palabras completas (secuencias de letras) que no formen parte de una mención (@usuario). Es decir, la palabra no debe estar inmediatamente después de un @.
text

Test: "@user hola mundo"
Debe coincidir "hola", "mundo", pero NO "user".

4. Extraer el nombre de un archivo sin extensión
Dado un nombre de archivo (ej. "documento.pdf"), captura solo el nombre sin la extensión. El archivo puede tener múltiples puntos (ej. "archivo.backup.tar.gz"); en ese caso extrae el nombre completo hasta el último punto.
text

Test: "foto.png"           -> "foto"
Test: "archivo.backup.gz"  -> "archivo.backup"

5. Validar una contraseña segura con lookaheads
Construye una regex que exija:

    Al menos 8 caracteres de longitud.

    Al menos una letra mayúscula.

    Al menos una letra minúscula.

    Al menos un dígito.

    Al menos un carácter especial de la lista !@#$%^&*.

text

Test: "Clave123!"  -> válido
Test: "clave123!"  -> inválido (sin mayúscula)
Test: "CLAVE123!"  -> inválido (sin minúscula)

6. Capturar los tres primeros grupos de un número de teléfono internacional
Formato: +XX (XXX) XXX-XXXX o +XX.XXX.XXX-XXXX. Los separadores pueden ser espacio, punto o guión. Captura por separado: código de país, código de área y número local (todo junto sin separadores, solo dígitos).
text

Test: "+1 (123) 456-7890"
Grupo 1: "1", Grupo 2: "123", Grupo 3: "4567890"
Test: "+34.666.777.888"
Grupo 1: "34", Grupo 2: "666", Grupo 3: "777888"

7. Reemplazar fechas de formato MM/DD/AAAA a DD/MM/AAAA
Usa una regex con grupos de captura para intercambiar el mes y el día en fechas del tipo 12/25/2024 a 25/12/2024. Escribe el patrón y la cadena de sustitución.
text

Entrada: "12/25/2024"
Salida: "25/12/2024"

8. Seleccionar líneas que contienen una palabra repetida dos veces consecutivas
En un texto multilínea, encuentra líneas donde una palabra (secuencia de letras) se repite exactamente, separada por un espacio: "hola hola". La coincidencia debe capturar la palabra repetida.
text

Test:
hola hola mundo
adiós adiós
bien bien bien
En la primera línea captura "hola", segunda "adiós", tercera no.

9. Validar una cadena que no contenga la palabra "prohibido"
Escribe un patrón que solo case si la cadena completa falla en contener la palabra "prohibido" en cualquier parte.
text

Test: "Este texto está bien"           -> match
Test: "Este texto está prohibido aquí" -> no match

10. Extraer hashtags de un tweet, ignorando signos de puntuación pegados
Encuentra todos los hashtags del estilo #regex o #OpenSource. Un hashtag comienza con # y continúa con caracteres de palabra (letras, números, guiones bajos). No debe incluir caracteres de puntuación como , o . si están pegados al final.
text

Test: "Aprendiendo #regex, #OpenSource y #python3."
Coincidencias: "#regex", "#OpenSource", "#python3"

03_avanzados.md
Instrucciones

Estos problemas requieren dominio de temas como recursión, grupos atómicos, posesivos, propiedades Unicode, backtracking catastrófico y optimización. Las regex deben ser eficientes y correctas.

1. Validar paréntesis balanceados con recursión
Escribe una regex que verifique si una cadena contiene una expresión con paréntesis correctamente balanceados (puede haber texto dentro y fuera). Por ejemplo: "a(b(c)d)e" es válido, "a(b(c)d" no lo es. La recursión debe aplicarse sobre el patrón completo. (Usa PCRE, PHP, Perl o Python regex)
text

Test: "(a(b)c)"   -> válido
Test: "((a)"      -> inválido
Test: "())"       -> inválido

2. Prevenir backtracking catastrófico en (a+)+b
Transforma el patrón (a+)+b en una versión que no sufra backtracking exponencial cuando se enfrenta a una cadena larga de as sin b al final. Usa cuantificadores posesivos o grupos atómicos.
text

Entrada de prueba: "aaaaaaaaaaaaaaaaaaaaX"
Explica por qué la versión original fallaría estrepitosamente y cómo la nueva lo evita.

3. Tokenizar un texto en palabras según propiedades Unicode
Exclusivamente con propiedades Unicode, extrae todas las palabras de un texto multilingüe. Una palabra se define como una secuencia de caracteres de categoría Letra (\p{L}). Debe ignorar números y puntuación.
text

Test: "Hola, ¿cómo estás? 123 números и русский текст"
Resultado esperado: ["Hola", "cómo", "estás", "русский", "текст"]

4. Reemplazar comillas tipográficas conservando el contenido
Dado un texto con comillas latinas («...») y comillas inglesas (“...”), escribe un patrón que capture el texto interior y permita reemplazar ambos estilos por comillas dobles estándar, preservando el contenido. Utiliza grupos con nombre o retroreferencias para manejar el cierre correcto.
text

Entrada: «Hola» y “mundo”
Salida (tras reemplazo): "Hola" y "mundo"

5. Validar un número de tarjeta de crédito (Visa, MasterCard, American Express) con una sola regex
Utiliza lookaheads para distinguir los formatos de inicio:

    Visa: empieza con 4, longitud 16.

    MasterCard: empieza con 51-55 o 2221-2720, longitud 16.

    American Express: empieza con 34 o 37, longitud 15.
    No es necesario aplicar el algoritmo de Luhn.

text

Test: "4111111111111111" -> Visa
Test: "5105105105105100" -> MasterCard
Test: "371449635398431" -> American Express
Test: "1234567812345670" -> no válido

6. Modo verboso: reescribe un patrón complejo con comentarios
Toma el siguiente patrón para validar un código postal español (5 dígitos) y una extensión opcional de 4 dígitos tras guión, con espacios opcionales: ^\d{5}\s*-?\s*(\d{4})?$. Reescríbelo en modo verboso (con flag x o comentarios) explicando cada parte.

7. Extraer todas las claves JSON de primer nivel
Dada una cadena JSON simple (sin anidamiento de objetos), extrae las claves de las propiedades de primer nivel. Por ejemplo: {"nombre":"Juan","edad":30,"ciudad":"Madrid"} debería capturar nombre, edad, ciudad. Asume un formato sin espacios alrededor de comillas y dos puntos.
text

Test: '{"nombre":"Juan","edad":30,"ciudad":"Madrid"}'
Capturas: "nombre", "edad", "ciudad"

8. Encontrar todas las palabras que contienen al menos dos vocales consecutivas
Usando clases de caracteres y cuantificadores, identifica palabras completas que tengan dos o más vocales seguidas (mayúsculas/minúsculas, considerando también vocales acentuadas: áéíóúü). No importa el resto de la palabra.
text

Test: "El caos y la poesía en el cielo"
Debe coincidir: "caos", "poesía", "cielo"

9. Simular un grupo atómico en JavaScript
JavaScript no soporta grupos atómicos. Escribe un patrón equivalente para (?>a+)b utilizando lookahead y retroreferencia. Demuestra que funciona con la entrada "aaab" y que no funciona con "aaaa".
text

Explicación: usa (?=(a+))\1b

10. Optimizar una regex para logs de Apache
Dado un patrón típico para analizar una línea de log de Apache: ^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d{3}) (\d+|-), sugiere mejoras de rendimiento utilizando cuantificadores posesivos o grupos atómicos donde sea posible, y explica por qué podrían reducir el backtracking en caso de líneas mal formadas.
soluciones/01_basicos_sol.md
Soluciones – Ejercicios Básicos

1. Buscar la palabra "gato"
Regex: /\bgato\b/gi

    \b límite de palabra, gato literal, bandera i para insensibilidad y g global.

2. Código de área
Regex: /\(\d{3}\) /

    \( \d{3} \) coincide con paréntesis y tres dígitos, seguido de espacio literal.

3. Palabras terminadas en "ción"
Regex: /\w+ción\b/gi (si \w soporta acentos y ñ con Unicode) o /[a-zA-Záéíóúüñ]+ción\b/gi.

    \w+ una o más letras/dígitos/guion bajo, luego "ción", límite de palabra.

4. Fecha DD/MM/AAAA
Regex: /^(0[1-9]|[12]\d|3[01])\/(0[1-9]|1[0-2])\/\d{4}$/

    Día: 01-31, mes: 01-12, año: 4 dígitos. Los separadores son barras.

5. Vocales
Regex: /[aeiou]/gi

    Clase con las cinco vocales. g global, i case-insensitive.

6. Múltiples espacios
Patrón de búsqueda: /\s+/g
Cadena de reemplazo: un espacio .

    \s+ uno o más caracteres de espacio.

7. Nombre de usuario
Regex: /^[a-zA-Z0-9]{4,16}$/

    Clase alfanumérica, cuantificador de 4 a 16. ^ y $ para toda la cadena.

8. Extensión de archivo
Regex: /\.([a-zA-Z]+)$/

    Busca un punto literal seguido de una o más letras hasta el final de la cadena. El grupo 1 contiene la extensión.

9. Líneas que empiezan con "Error"
Regex: /^Error\b.*/gim

    ^ inicio de línea (con flag m), Error literal, \b límite de palabra, luego cualquier cosa. Flags: g global, i ignore case, m multilínea.

10. Número decimal simple
Regex: /^-?\d+(\.\d+)?$/

    -? signo opcional. \d+ entero obligatorio. (\.\d+)? parte decimal opcional con punto y al menos un dígito.

soluciones/02_intermedios_sol.md
Soluciones – Ejercicios Intermedios

1. Texto en <strong>
Regex: /<strong>(.*?)<\/strong>/gi

    .*? perezoso captura contenido en el grupo 1. Flags global e ignore case.

2. Validar email (mejorado)
Regex:
text

/^[a-zA-Z0-9]+(?:[._%+-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z]{2,})+$/

Explicación: La parte local empieza con alfanumérico, luego permite separadores únicos entre bloques alfanuméricos. El dominio valida segmentos sin guiones al inicio/fin, y TLD de al menos 2 letras.

3. Palabras no precedidas por @
Regex: /(?<!@)\b[a-zA-Z]+\b/g

    Lookbehind negativo (?<!@) asegura que no haya @ justo antes. \b...\b palabra de letras.

4. Nombre de archivo sin extensión
Regex: /^(.+)\.([^.]+)$/ (aplicado con match y grupo 1).
O usando lookahead: /.+(?=\.)/.

    Captura todo hasta el último punto. Grupo 1 contiene el nombre.

5. Contraseña segura
Regex: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/

    Cuatro lookaheads que verifican presencia de cada categoría. .{8,} consume la cadena.

6. Teléfono internacional
Regex: /^\+(\d+)[ .-]\(?(\d+)\)?[ .-]?(\d+)[ .-](\d+)$/ (se ajusta la agrupación para capturar tres partes).
Una versión más flexible: /^\+(\d{1,3})[ .-]\(?(\d{1,4})\)?[ .-](\d{1,14})$/ y luego reorganizar dígitos. Pero según el requerimiento específico:
Para +1 (123) 456-7890:
\+\s?(\d+)\s?\(?(\d+)\)?[\s.-]?(\d+)[\s.-]?(\d+) y unir grupos 3 y 4 en código. Mejor con nombre de grupo:
Patrón: \+\s?(?<pais>\d+)\s?\(?(?<area>\d+)\)?[\s.-]?(?<local>\d+)[\s.-]?(?<resto>\d+). Pero el enunciado pide grupo 1,2,3. Optamos por:
text

/^\+(\d+)\D*\(?(\d+)\)?\D*(\d+)\D*(\d+)$/

Luego concatenar grupo 3 y 4 para el número local.

7. Intercambiar fecha MM/DD/AAAA
Patrón: /(\d{2})\/(\d{2})\/(\d{4})/
Cadena de reemplazo: $2/$1/$3

    Grupo 1: mes, Grupo 2: día, Grupo 3: año. Se invierten 1 y 2.

8. Palabra repetida consecutiva
Regex: /\b(\w+)\s+\1\b/g

    (\w+) captura palabra. \s+ espacios. \1 exige la misma palabra. \b límites aseguran palabra completa.

9. Cadena sin "prohibido"
Regex: /^(?!.*prohibido).*$/ (o con flags i si no importa mayúsculas).

    El lookahead negativo (?!.*prohibido) falla si en cualquier lugar aparece "prohibido".

10. Hashtags limpios
Regex: /#\w+\b/g

    #\w+ hashtag. El \b al final impide que caracteres extra como , se incluyan (porque , no es parte de \w). En algunos contextos puede necesitar (?<=^|\s)#\w+ para evitar falsos hashtags en URLs.

soluciones/03_avanzados_sol.md
Soluciones – Ejercicios Avanzados

1. Paréntesis balanceados con recursión
Regex (PCRE/Python regex): /^[^()]*\((?>[^()]+|(?R))*\)[^()]*$/
O para toda la cadena:
text

/^(?:[^()]* \((?: (?: [^()]++ | (?R) )* )\) [^()]* )+$/x

Explicación: Desde el inicio, permite texto sin paréntesis, luego \(, dentro un grupo atómico que repite caracteres no paréntesis o recursión, y cierra \). [^()]++ es posesivo para eficiencia.

2. Prevenir backtracking catastrófico
Regex original: (a+)+b
Regex optimizada: (a++)+b o (?>a+)+b o simplemente a+b (si no es necesario el anidamiento).
Con a++ el cuantificador no cede caracteres, eliminando el retroceso exponencial. Al aplicarlo sobre "aaaa...X" falla inmediatamente porque tras consumir todas las as no hay b y no intenta redistribuir.

3. Tokenizar con propiedades Unicode
Regex: /\p{L}+/gu en JavaScript, o en Python regex: \p{L}+.

    \p{L} cualquier letra Unicode. Flag u y g dan todas las secuencias de letras.

4. Comillas tipográficas a comillas rectas
Buscar: «(.*?)» y también “.*?”.
Patrón unificado con alternancia y retroreferencia para asegurar mismo tipo:
text

/«([^«»]+)»|“([^“”]+)”/

Reemplazo: "$1$2".
Se puede usar un solo grupo con nombre y condicional (en motores que lo permitan), pero con alternancia simple y dos grupos es fácil: la coincidencia tendrá grupo 1 o grupo 2. En sustitución "$1$2" (uno estará vacío).

5. Tarjeta de crédito
Regex (con espacios opcionales):
text

/^(?:4\d{15}|(?:5[1-5]\d{14}|222[1-9]\d{12}|22[3-9]\d{13}|2[3-6]\d{14}|27[0-1]\d{12}|2720\d{12})|3[47]\d{13})$/

Se simplifica con lookahead para el tipo y luego longitud:
text

/^(?:(?=4)\d{16}|(?=5[1-5]|222[1-9]|22[3-9]|2[3-6]|27[0-1]|2720)\d{16}|(?=3[47])\d{15})$/

Ajuste para MasterCard: comienzo 51-55 o 2221-2720.

6. Modo verboso
regex

(?x)          # modo verboso
^             # inicio
\d{5}         # cinco dígitos básicos
\s*           # espacios opcionales
-?            # guion opcional
\s*           # espacios opcionales
(\d{4})?      # extensión opcional de 4 dígitos (grupo 1)
$             # fin

En Python:
python

pattern = re.compile(r"""
    ^
    \d{5}      # código postal base
    \s* -? \s* # separador flexible
    (\d{4})?   # extensión opcional
    $
""", re.VERBOSE)

7. Claves JSON de primer nivel
Regex: /"([^"]+)":/g

    Busca comilla, captura uno o más caracteres no comilla, luego comilla y dos puntos. Grupo 1 contiene la clave.

8. Palabras con al menos dos vocales consecutivas
Regex (con vocales acentuadas): /\b\w*[aeiouáéíóúü]{2}\w*\b/gi

    \b\w* inicio de palabra, luego dos vocales seguidas, luego resto de palabra.

9. Simular grupo atómico en JavaScript
Para (?>a+)b:
javascript

let regex = /(?=(a+))\1b/;

Prueba:

    "aaab" → regex.exec("aaab") devuelve match (grupo 1: "aaa").

    "aaaa" → no hay match.

10. Optimizar Apache log regex
Patrón original: ^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d{3}) (\d+|-)
Mejoras:

    Usar [^][]* en lugar de [^\]]+ (es igual pero más directo).

    Cambiar \S+ a \S++ o envolver en grupos atómicos para evitar backtracking en logs malformados donde campos no coincidan.

    Para la petición ([^"]*) podría ser ([^"]*+) posesivo, porque una vez capturada la cadena entre comillas no se querrá ceder caracteres.

    La regex completa con posesivos:

text

^(\S++) (\S++) (\S++) \[([^][]*+)\] "([^"]*+)" (\d{3}) (\d++|-)

Explicación: cada ++ y *+ evita que, en caso de fallo más adelante, el motor intente reducir la captura y redistribuir, evitando backtracking innecesario en líneas incompletas.

/////////////////////////////////////////////////////////////////////////////

/9//////////////////////////////////////////////////////////////////////////////////////////
01_basicos.md
Instrucciones

Escribe una expresión regular para cada uno de los siguientes problemas. Si el motor lo requiere, especifica las banderas. Prueba tus patrones en un probador online (regex101.com, pythex.org) con los casos de ejemplo.

1. Buscar la palabra "gato"
Encuentra todas las apariciones de la palabra "gato" en una frase, sin distinguir mayúsculas/minúsculas. Debe coincidir como palabra completa.
text

Test: "El gato y el GATO gatean"
Coincidencias esperadas: "gato", "GATO"

2. Validar un código de área de EE.UU.
Formato: tres dígitos entre paréntesis (seguidos de espacio y tres dígitos adicionales, pero solo valida el código de área). Por ejemplo, "(123) " debe coincidir.
text

Test: "(123) 456-7890"  -> match "(123) "
Test: "(12) 345"        -> no match

3. Encontrar todas las palabras que terminan en "ción"
Coincide con palabras completas que tengan la terminación "ción" (ej. "canción", "acción"). Ignora mayúsculas/minúsculas.
text

Test: "La canción y la ACCIÓN fueron bien."
Coincidencias: "canción", "ACCIÓN"

4. Validar una fecha en formato DD/MM/AAAA
Día de 01 a 31, mes de 01 a 12, año de 4 dígitos. No hace falta validar días por mes (p.ej. 31/02/2023 es válido para este ejercicio).
text

Test: "15/08/2024" -> match
Test: "5/8/2024"   -> no match (exige dos dígitos)

5. Encontrar todas las vocales
Extrae todas las vocales (tanto mayúsculas como minúsculas) de un texto.
text

Test: "Hola Mundo" -> ["o", "a", "u", "o"]

6. Reemplazar múltiples espacios por uno solo
Escribe un patrón que capture cualquier secuencia de uno o más espacios en blanco (espacio, tabulador, salto de línea) para luego reemplazarlas por un solo espacio.
text

Test: "Hola    mundo.\t\tAdiós"
Después del reemplazo: "Hola mundo. Adiós"

7. Validar un nombre de usuario alfanumérico
Debe tener entre 4 y 16 caracteres, compuestos únicamente por letras (mayúsculas y minúsculas) y dígitos. No puede contener espacios ni símbolos.
text

Test: "usuario123" -> válido
Test: "user name"  -> inválido

8. Extraer extensiones de archivo
De una lista de nombres de archivo, extrae la extensión (sin el punto). Solo debe capturar extensiones de letras (no números al final). Por ejemplo: "imagen.jpg", "documento.pdf", "script.js".
text

Test: "foto.png"     -> extensión "png"
Test: "archivo.tar.gz" -> extensión "gz" (la última)

9. Buscar líneas que comienzan con "Error"
Procesa un texto multilínea y selecciona todas las líneas que empiezan por la palabra "Error" (sin importar mayúsculas/minúsculas). La palabra debe estar al inicio de la línea.
text

Test:
Todo bien
Error: fallo crítico
WARNING: revisar
error menor
Se espera coincidencia en la segunda línea: "Error: fallo crítico"

10. Validar un número decimal simple
Formato: puede tener un signo negativo opcional, dígitos enteros obligatorios, y opcionalmente un punto seguido de uno o más dígitos decimales. Ej: "-3.14", "10", "0.5". No permite múltiples puntos ni caracteres extra.
text

Test: "42"        -> válido
Test: "-.5"       -> inválido (falta entero)
Test: "1.2.3"     -> inválido

02_intermedios.md
Instrucciones

Estos ejercicios profundizan en cuantificadores perezosos, grupos de captura, lookahead/lookbehind, y patrones prácticos. Proporciona la regex y una breve explicación de su funcionamiento.

1. Extraer el texto dentro de etiquetas HTML <strong>
Dado un fragmento HTML, captura el contenido que está entre <strong> y </strong>, incluyendo posibles espacios y otras etiquetas internas, pero usando cuantificador perezoso para obtener cada bloque por separado.
text

Test: "<strong>Nota:</strong> esto es <strong>importante</strong>"
Coincidencia 1: "Nota:"  Coincidencia 2: "importante"

2. Validar un email con el patrón mejorado
Escribe una regex que valide un correo electrónico con las siguientes reglas:

    Parte local: caracteres alfanuméricos, puntos, guiones bajos, guiones, porcentajes y signos más. No puede empezar ni terminar con punto ni tener dos puntos consecutivos.

    Dominio: letras, dígitos, guiones; separado por puntos; el TLD debe tener al menos dos letras.

(Usa el patrón mejorado visto en los apuntes, no el básico.)
text

Test: "usuario@dominio.com"       -> válido
Test: "usuario@sub.dom.co.uk"    -> válido
Test: "usuario@dominio..com"     -> inválido
Test: ".usuario@dominio.com"     -> inválido

3. Buscar palabras que no están precedidas por el signo @
Encuentra palabras completas (secuencias de letras) que no formen parte de una mención (@usuario). Es decir, la palabra no debe estar inmediatamente después de un @.
text

Test: "@user hola mundo"
Debe coincidir "hola", "mundo", pero NO "user".

4. Extraer el nombre de un archivo sin extensión
Dado un nombre de archivo (ej. "documento.pdf"), captura solo el nombre sin la extensión. El archivo puede tener múltiples puntos (ej. "archivo.backup.tar.gz"); en ese caso extrae el nombre completo hasta el último punto.
text

Test: "foto.png"           -> "foto"
Test: "archivo.backup.gz"  -> "archivo.backup"

5. Validar una contraseña segura con lookaheads
Construye una regex que exija:

    Al menos 8 caracteres de longitud.

    Al menos una letra mayúscula.

    Al menos una letra minúscula.

    Al menos un dígito.

    Al menos un carácter especial de la lista !@#$%^&*.

text

Test: "Clave123!"  -> válido
Test: "clave123!"  -> inválido (sin mayúscula)
Test: "CLAVE123!"  -> inválido (sin minúscula)

6. Capturar los tres primeros grupos de un número de teléfono internacional
Formato: +XX (XXX) XXX-XXXX o +XX.XXX.XXX-XXXX. Los separadores pueden ser espacio, punto o guión. Captura por separado: código de país, código de área y número local (todo junto sin separadores, solo dígitos).
text

Test: "+1 (123) 456-7890"
Grupo 1: "1", Grupo 2: "123", Grupo 3: "4567890"
Test: "+34.666.777.888"
Grupo 1: "34", Grupo 2: "666", Grupo 3: "777888"

7. Reemplazar fechas de formato MM/DD/AAAA a DD/MM/AAAA
Usa una regex con grupos de captura para intercambiar el mes y el día en fechas del tipo 12/25/2024 a 25/12/2024. Escribe el patrón y la cadena de sustitución.
text

Entrada: "12/25/2024"
Salida: "25/12/2024"

8. Seleccionar líneas que contienen una palabra repetida dos veces consecutivas
En un texto multilínea, encuentra líneas donde una palabra (secuencia de letras) se repite exactamente, separada por un espacio: "hola hola". La coincidencia debe capturar la palabra repetida.
text

Test:
hola hola mundo
adiós adiós
bien bien bien
En la primera línea captura "hola", segunda "adiós", tercera no.

9. Validar una cadena que no contenga la palabra "prohibido"
Escribe un patrón que solo case si la cadena completa falla en contener la palabra "prohibido" en cualquier parte.
text

Test: "Este texto está bien"           -> match
Test: "Este texto está prohibido aquí" -> no match

10. Extraer hashtags de un tweet, ignorando signos de puntuación pegados
Encuentra todos los hashtags del estilo #regex o #OpenSource. Un hashtag comienza con # y continúa con caracteres de palabra (letras, números, guiones bajos). No debe incluir caracteres de puntuación como , o . si están pegados al final.
text

Test: "Aprendiendo #regex, #OpenSource y #python3."
Coincidencias: "#regex", "#OpenSource", "#python3"

03_avanzados.md
Instrucciones

Estos problemas requieren dominio de temas como recursión, grupos atómicos, posesivos, propiedades Unicode, backtracking catastrófico y optimización. Las regex deben ser eficientes y correctas.

1. Validar paréntesis balanceados con recursión
Escribe una regex que verifique si una cadena contiene una expresión con paréntesis correctamente balanceados (puede haber texto dentro y fuera). Por ejemplo: "a(b(c)d)e" es válido, "a(b(c)d" no lo es. La recursión debe aplicarse sobre el patrón completo. (Usa PCRE, PHP, Perl o Python regex)
text

Test: "(a(b)c)"   -> válido
Test: "((a)"      -> inválido
Test: "())"       -> inválido

2. Prevenir backtracking catastrófico en (a+)+b
Transforma el patrón (a+)+b en una versión que no sufra backtracking exponencial cuando se enfrenta a una cadena larga de as sin b al final. Usa cuantificadores posesivos o grupos atómicos.
text

Entrada de prueba: "aaaaaaaaaaaaaaaaaaaaX"
Explica por qué la versión original fallaría estrepitosamente y cómo la nueva lo evita.

3. Tokenizar un texto en palabras según propiedades Unicode
Exclusivamente con propiedades Unicode, extrae todas las palabras de un texto multilingüe. Una palabra se define como una secuencia de caracteres de categoría Letra (\p{L}). Debe ignorar números y puntuación.
text

Test: "Hola, ¿cómo estás? 123 números и русский текст"
Resultado esperado: ["Hola", "cómo", "estás", "русский", "текст"]

4. Reemplazar comillas tipográficas conservando el contenido
Dado un texto con comillas latinas («...») y comillas inglesas (“...”), escribe un patrón que capture el texto interior y permita reemplazar ambos estilos por comillas dobles estándar, preservando el contenido. Utiliza grupos con nombre o retroreferencias para manejar el cierre correcto.
text

Entrada: «Hola» y “mundo”
Salida (tras reemplazo): "Hola" y "mundo"

5. Validar un número de tarjeta de crédito (Visa, MasterCard, American Express) con una sola regex
Utiliza lookaheads para distinguir los formatos de inicio:

    Visa: empieza con 4, longitud 16.

    MasterCard: empieza con 51-55 o 2221-2720, longitud 16.

    American Express: empieza con 34 o 37, longitud 15.
    No es necesario aplicar el algoritmo de Luhn.

text

Test: "4111111111111111" -> Visa
Test: "5105105105105100" -> MasterCard
Test: "371449635398431" -> American Express
Test: "1234567812345670" -> no válido

6. Modo verboso: reescribe un patrón complejo con comentarios
Toma el siguiente patrón para validar un código postal español (5 dígitos) y una extensión opcional de 4 dígitos tras guión, con espacios opcionales: ^\d{5}\s*-?\s*(\d{4})?$. Reescríbelo en modo verboso (con flag x o comentarios) explicando cada parte.

7. Extraer todas las claves JSON de primer nivel
Dada una cadena JSON simple (sin anidamiento de objetos), extrae las claves de las propiedades de primer nivel. Por ejemplo: {"nombre":"Juan","edad":30,"ciudad":"Madrid"} debería capturar nombre, edad, ciudad. Asume un formato sin espacios alrededor de comillas y dos puntos.
text

Test: '{"nombre":"Juan","edad":30,"ciudad":"Madrid"}'
Capturas: "nombre", "edad", "ciudad"

8. Encontrar todas las palabras que contienen al menos dos vocales consecutivas
Usando clases de caracteres y cuantificadores, identifica palabras completas que tengan dos o más vocales seguidas (mayúsculas/minúsculas, considerando también vocales acentuadas: áéíóúü). No importa el resto de la palabra.
text

Test: "El caos y la poesía en el cielo"
Debe coincidir: "caos", "poesía", "cielo"

9. Simular un grupo atómico en JavaScript
JavaScript no soporta grupos atómicos. Escribe un patrón equivalente para (?>a+)b utilizando lookahead y retroreferencia. Demuestra que funciona con la entrada "aaab" y que no funciona con "aaaa".
text

Explicación: usa (?=(a+))\1b

10. Optimizar una regex para logs de Apache
Dado un patrón típico para analizar una línea de log de Apache: ^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d{3}) (\d+|-), sugiere mejoras de rendimiento utilizando cuantificadores posesivos o grupos atómicos donde sea posible, y explica por qué podrían reducir el backtracking en caso de líneas mal formadas.
soluciones/01_basicos_sol.md
Soluciones – Ejercicios Básicos

1. Buscar la palabra "gato"
Regex: /\bgato\b/gi

    \b límite de palabra, gato literal, bandera i para insensibilidad y g global.

2. Código de área
Regex: /\(\d{3}\) /

    \( \d{3} \) coincide con paréntesis y tres dígitos, seguido de espacio literal.

3. Palabras terminadas en "ción"
Regex: /\w+ción\b/gi (si \w soporta acentos y ñ con Unicode) o /[a-zA-Záéíóúüñ]+ción\b/gi.

    \w+ una o más letras/dígitos/guion bajo, luego "ción", límite de palabra.

4. Fecha DD/MM/AAAA
Regex: /^(0[1-9]|[12]\d|3[01])\/(0[1-9]|1[0-2])\/\d{4}$/

    Día: 01-31, mes: 01-12, año: 4 dígitos. Los separadores son barras.

5. Vocales
Regex: /[aeiou]/gi

    Clase con las cinco vocales. g global, i case-insensitive.

6. Múltiples espacios
Patrón de búsqueda: /\s+/g
Cadena de reemplazo: un espacio .

    \s+ uno o más caracteres de espacio.

7. Nombre de usuario
Regex: /^[a-zA-Z0-9]{4,16}$/

    Clase alfanumérica, cuantificador de 4 a 16. ^ y $ para toda la cadena.

8. Extensión de archivo
Regex: /\.([a-zA-Z]+)$/

    Busca un punto literal seguido de una o más letras hasta el final de la cadena. El grupo 1 contiene la extensión.

9. Líneas que empiezan con "Error"
Regex: /^Error\b.*/gim

    ^ inicio de línea (con flag m), Error literal, \b límite de palabra, luego cualquier cosa. Flags: g global, i ignore case, m multilínea.

10. Número decimal simple
Regex: /^-?\d+(\.\d+)?$/

    -? signo opcional. \d+ entero obligatorio. (\.\d+)? parte decimal opcional con punto y al menos un dígito.

soluciones/02_intermedios_sol.md
Soluciones – Ejercicios Intermedios

1. Texto en <strong>
Regex: /<strong>(.*?)<\/strong>/gi

    .*? perezoso captura contenido en el grupo 1. Flags global e ignore case.

2. Validar email (mejorado)
Regex:
text

/^[a-zA-Z0-9]+(?:[._%+-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z]{2,})+$/

Explicación: La parte local empieza con alfanumérico, luego permite separadores únicos entre bloques alfanuméricos. El dominio valida segmentos sin guiones al inicio/fin, y TLD de al menos 2 letras.

3. Palabras no precedidas por @
Regex: /(?<!@)\b[a-zA-Z]+\b/g

    Lookbehind negativo (?<!@) asegura que no haya @ justo antes. \b...\b palabra de letras.

4. Nombre de archivo sin extensión
Regex: /^(.+)\.([^.]+)$/ (aplicado con match y grupo 1).
O usando lookahead: /.+(?=\.)/.

    Captura todo hasta el último punto. Grupo 1 contiene el nombre.

5. Contraseña segura
Regex: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/

    Cuatro lookaheads que verifican presencia de cada categoría. .{8,} consume la cadena.

6. Teléfono internacional
Regex: /^\+(\d+)[ .-]\(?(\d+)\)?[ .-]?(\d+)[ .-](\d+)$/ (se ajusta la agrupación para capturar tres partes).
Una versión más flexible: /^\+(\d{1,3})[ .-]\(?(\d{1,4})\)?[ .-](\d{1,14})$/ y luego reorganizar dígitos. Pero según el requerimiento específico:
Para +1 (123) 456-7890:
\+\s?(\d+)\s?\(?(\d+)\)?[\s.-]?(\d+)[\s.-]?(\d+) y unir grupos 3 y 4 en código. Mejor con nombre de grupo:
Patrón: \+\s?(?<pais>\d+)\s?\(?(?<area>\d+)\)?[\s.-]?(?<local>\d+)[\s.-]?(?<resto>\d+). Pero el enunciado pide grupo 1,2,3. Optamos por:
text

/^\+(\d+)\D*\(?(\d+)\)?\D*(\d+)\D*(\d+)$/

Luego concatenar grupo 3 y 4 para el número local.

7. Intercambiar fecha MM/DD/AAAA
Patrón: /(\d{2})\/(\d{2})\/(\d{4})/
Cadena de reemplazo: $2/$1/$3

    Grupo 1: mes, Grupo 2: día, Grupo 3: año. Se invierten 1 y 2.

8. Palabra repetida consecutiva
Regex: /\b(\w+)\s+\1\b/g

    (\w+) captura palabra. \s+ espacios. \1 exige la misma palabra. \b límites aseguran palabra completa.

9. Cadena sin "prohibido"
Regex: /^(?!.*prohibido).*$/ (o con flags i si no importa mayúsculas).

    El lookahead negativo (?!.*prohibido) falla si en cualquier lugar aparece "prohibido".

10. Hashtags limpios
Regex: /#\w+\b/g

    #\w+ hashtag. El \b al final impide que caracteres extra como , se incluyan (porque , no es parte de \w). En algunos contextos puede necesitar (?<=^|\s)#\w+ para evitar falsos hashtags en URLs.

soluciones/03_avanzados_sol.md
Soluciones – Ejercicios Avanzados

1. Paréntesis balanceados con recursión
Regex (PCRE/Python regex): /^[^()]*\((?>[^()]+|(?R))*\)[^()]*$/
O para toda la cadena:
text

/^(?:[^()]* \((?: (?: [^()]++ | (?R) )* )\) [^()]* )+$/x

Explicación: Desde el inicio, permite texto sin paréntesis, luego \(, dentro un grupo atómico que repite caracteres no paréntesis o recursión, y cierra \). [^()]++ es posesivo para eficiencia.

2. Prevenir backtracking catastrófico
Regex original: (a+)+b
Regex optimizada: (a++)+b o (?>a+)+b o simplemente a+b (si no es necesario el anidamiento).
Con a++ el cuantificador no cede caracteres, eliminando el retroceso exponencial. Al aplicarlo sobre "aaaa...X" falla inmediatamente porque tras consumir todas las as no hay b y no intenta redistribuir.

3. Tokenizar con propiedades Unicode
Regex: /\p{L}+/gu en JavaScript, o en Python regex: \p{L}+.

    \p{L} cualquier letra Unicode. Flag u y g dan todas las secuencias de letras.

4. Comillas tipográficas a comillas rectas
Buscar: «(.*?)» y también “.*?”.
Patrón unificado con alternancia y retroreferencia para asegurar mismo tipo:
text

/«([^«»]+)»|“([^“”]+)”/

Reemplazo: "$1$2".
Se puede usar un solo grupo con nombre y condicional (en motores que lo permitan), pero con alternancia simple y dos grupos es fácil: la coincidencia tendrá grupo 1 o grupo 2. En sustitución "$1$2" (uno estará vacío).

5. Tarjeta de crédito
Regex (con espacios opcionales):
text

/^(?:4\d{15}|(?:5[1-5]\d{14}|222[1-9]\d{12}|22[3-9]\d{13}|2[3-6]\d{14}|27[0-1]\d{12}|2720\d{12})|3[47]\d{13})$/

Se simplifica con lookahead para el tipo y luego longitud:
text

/^(?:(?=4)\d{16}|(?=5[1-5]|222[1-9]|22[3-9]|2[3-6]|27[0-1]|2720)\d{16}|(?=3[47])\d{15})$/

Ajuste para MasterCard: comienzo 51-55 o 2221-2720.

6. Modo verboso
regex

(?x)          # modo verboso
^             # inicio
\d{5}         # cinco dígitos básicos
\s*           # espacios opcionales
-?            # guion opcional
\s*           # espacios opcionales
(\d{4})?      # extensión opcional de 4 dígitos (grupo 1)
$             # fin

En Python:
python

pattern = re.compile(r"""
    ^
    \d{5}      # código postal base
    \s* -? \s* # separador flexible
    (\d{4})?   # extensión opcional
    $
""", re.VERBOSE)

7. Claves JSON de primer nivel
Regex: /"([^"]+)":/g

    Busca comilla, captura uno o más caracteres no comilla, luego comilla y dos puntos. Grupo 1 contiene la clave.

8. Palabras con al menos dos vocales consecutivas
Regex (con vocales acentuadas): /\b\w*[aeiouáéíóúü]{2}\w*\b/gi

    \b\w* inicio de palabra, luego dos vocales seguidas, luego resto de palabra.

9. Simular grupo atómico en JavaScript
Para (?>a+)b:
javascript

let regex = /(?=(a+))\1b/;

Prueba:

    "aaab" → regex.exec("aaab") devuelve match (grupo 1: "aaa").

    "aaaa" → no hay match.

10. Optimizar Apache log regex
Patrón original: ^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d{3}) (\d+|-)
Mejoras:

    Usar [^][]* en lugar de [^\]]+ (es igual pero más directo).

    Cambiar \S+ a \S++ o envolver en grupos atómicos para evitar backtracking en logs malformados donde campos no coincidan.

    Para la petición ([^"]*) podría ser ([^"]*+) posesivo, porque una vez capturada la cadena entre comillas no se querrá ceder caracteres.

    La regex completa con posesivos:

text

^(\S++) (\S++) (\S++) \[([^][]*+)\] "([^"]*+)" (\d{3}) (\d++|-)

Explicación: cada ++ y *+ evita que, en caso de fallo más adelante, el motor intente reducir la captura y redistribuir, evitando backtracking innecesario en líneas incompletas.

/////////////////////////////////////////////////////////////////////////////

/1//////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////