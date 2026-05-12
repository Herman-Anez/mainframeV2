# literales_y_escape.md
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
