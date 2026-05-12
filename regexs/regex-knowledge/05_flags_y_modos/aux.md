# flags_comunes.md
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

# modo_verboso.md
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
