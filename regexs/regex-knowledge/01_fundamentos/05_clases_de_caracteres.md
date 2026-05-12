# clases_de_caracteres.md
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
