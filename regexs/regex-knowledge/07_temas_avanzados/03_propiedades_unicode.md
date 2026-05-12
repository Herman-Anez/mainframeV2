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
