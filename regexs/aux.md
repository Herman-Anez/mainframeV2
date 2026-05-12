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

/////////////////////////////////////////////////////////////////////////////

/1//////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////

/1//////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////

/1//////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////

/1//////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////

/1//////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////

/1//////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////

/1//////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////

/1//////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////