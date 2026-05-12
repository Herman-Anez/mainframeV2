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
