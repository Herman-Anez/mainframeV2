# lookahead.md
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

# lookbehind.md
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

# ejemplos_validacion.md

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
