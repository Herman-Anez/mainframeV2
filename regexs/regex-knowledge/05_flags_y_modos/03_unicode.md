# unicode.md
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
