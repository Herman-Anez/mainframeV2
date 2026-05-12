# comparativa_general.md
El ecosistema de los motores de regex

No existe una única implementación de expresiones regulares. Cada lenguaje de programación o herramienta utiliza un motor de regex que interpreta los patrones y los ejecuta contra las cadenas. Estos motores difieren en sintaxis, características avanzadas y rendimiento. Conocer las diferencias es esencial para escribir patrones portables o aprovechar al máximo cada entorno.
Principales familias de motores
Motor	Ejemplos de uso	Tipo	Observaciones
PCRE (Perl Compatible Regular Expressions)	PHP, Apache, Python (módulo regex), diversos	Backtracking con muchas extensiones	Muy completo; posee recursión, subrutinas, verbos de control.
ECMAScript	JavaScript, navegadores, Node.js	Backtracking	Mejorado significativamente desde ES2018; aún carece de grupos atómicos, posesivos y recursión.
Python re	Biblioteca estándar de Python	Backtracking	Más limitado; lookbehind fijo, sin grupos atómicos, sin \p{}.
Python regex	Módulo externo PyPI	Backtracking avanzado	Similar a PCRE; soporta Unicode completo, recursión, etc.
Java java.util.regex	Java	Backtracking	Grupos atómicos, posesivos, lookbehind con límite máximo, propiedades Unicode.
.NET	C#, VB.NET, PowerShell	Backtracking	Extremadamente potente: lookbehind variable, grupos balanceados, ejecución derecha-izquierda.
POSIX (BRE/ERE)	grep, sed, awk	Autómata finito (sin retrocesos para referencias)	Muy básico; sin aserciones, sin cuantificadores perezosos; backreferences solo en BRE.
Tabla comparativa de características
Característica	PCRE	JS (ES2024)	Python re	Python regex	Java	.NET	POSIX
Lookahead (?= ) / (?! )	✔	✔	✔	✔	✔	✔	✘
Lookbehind (?<= ) / (?<! )	✔ (variable en PCRE2)	✔ (variable)	✔ (solo fijo)	✔ (variable)	✔ (longitud máxima finita)	✔ (variable)	✘
Grupos atómicos (?> )	✔	✘	✘	✔	✔	✔	✘
Cuantificadores posesivos *+, ++	✔	✘	✘	✔	✔	✔	✘
Grupos con nombre	(?<name>...) / (?'name'...)	(?<name>...)	(?P<name>...)	(?P<name>...) / (?<name>...)	(?<name>...)	(?<name>...) / (?'name'...)	✘
Recursión (?R) / (?0)	✔	✘	✘	✔	✘	✘ (se logra con balanceo)	✘
Subrutinas (?&name)	✔	✘	✘	✔	✘	✘	✘
Condicionales (?(cond)si|no)	✔	✘	✘	✔	✘	✔	✘
Propiedades Unicode \p{...}	✔ (con flag u)	✔ (ES2018+)	✘	✔	✔ (desde Java 1.7)	✔	✘
Modo verboso / comentarios	✔	✘	✔	✔	✔	✔ (opción IgnorePatternWhitespace)	✘
Backreferences \1	✔	✔	✔	✔	✔	✔	Solo BRE
\K (keep out)	✔	✘	✘	✔	✘	✘	✘
Verbos de control (*SKIP)(*F)	✔	✘	✘	✔	✘	✘	✘
Factores que determinan la elección

    Portabilidad: si el patrón debe funcionar en distintos lenguajes (ej. front y back), adhiérete al subconjunto común: lookahead, grupos, retroreferencias básicas, clases.

    Potencia: para tareas complejas (balanceo de paréntesis, análisis léxico), elige PCRE, .NET o Python regex.

    Rendimiento: los motores con backtracking pueden sufrir patrones catastróficos. Los motores DFA (POSIX) o híbridos optimizan, pero sacrifican funcionalidades.

    Disponibilidad: en el navegador solo tienes JavaScript; en servidores PHP o Perl, PCRE es nativo; en Java y .NET, sus propias bibliotecas.

Historia y evolución

    POSIX: Primera estandarización (BRE/ERE). Muy limitado, aún presente en herramientas del sistema.

    Perl 5: Revolucionó las regex añadiendo muchas extensiones; de ahí nació PCRE.

    PCRE: Se convirtió en el estándar de facto para servidores, Apache, PHP.

    JavaScript: Por mucho tiempo ignorado, pero desde ES2015/ES2018 ha incorporado lookbehind, unicode, grupos nombrados.

    Python: La estándar re no ha evolucionado mucho; el módulo regex rellena los huecos.

    Java y .NET: Cada uno con sus propias extensiones originales (balanceo en .NET, longitud finita en Java).

# PCRE.md
¿Qué es PCRE?

PCRE (Perl Compatible Regular Expressions) es una biblioteca de código abierto que implementa expresiones regulares inspiradas en las de Perl, añadiendo alguna extensión adicional. Es el motor usado por PHP (las funciones preg_*), Apache (mod_rewrite, mod_security), Postfix, y muchos otros. Existen dos versiones principales: PCRE (la original, ya obsoleta) y PCRE2 (reescrita, con soporte mejorado y nueva API).
Características destacadas

    Todas las funcionalidades comunes: lookahead, lookbehind, grupos atómicos, cuantificadores posesivos, retroreferencias, grupos con nombre, condicionales.

    Recursión y subrutinas.

    Verbos de control: (*SKIP), (*FAIL), (*COMMIT), etc.

    \K: reinicia el inicio de la coincidencia.

    Unicode completo (propiedades, scripts) con flag u o (*UTF)(*UCP).

    Compatibilidad con Perl muy alta, aunque con algunas diferencias (ej. manejo de \z y \Z es idéntico).

Versiones PCRE vs PCRE2

    PCRE (8.xx): última versión, congelada. Limitada a lookbehind de longitud fija.

    PCRE2 (10.xx): reescritura completa. Soporta lookbehind variable (con ciertas restricciones, debe poder determinarse una longitud máxima). Mejor rendimiento, nueva API.

PHP en sus versiones recientes (7.3+) ya usa PCRE2.
Sintaxis y activación de flags

En PHP (PCRE), las flags se añaden al final del delimitador: /patrón/ixu. Dentro del patrón se pueden modificar con (?i), (?-i), (?i:…).

Ejemplo de lookbehind variable en PCRE2:
php

preg_match('/(?<=abc|defg)X/', 'defgX'); // válido en PCRE2, error en PCRE antiguo

Recursión y subrutinas

Permite emparejar estructuras anidadas sin fin de grupos. Ejemplo: paréntesis balanceados.
regex

\( (?: [^()]++ | (?R) )* \)

    [^()]++ consume caracteres que no son paréntesis (posesivo).

    | (?R) permite volver a aplicar el patrón completo recursivamente.

    El asterisco * repite todo el grupo.

Subrutinas con (?&nombre) reutilizan un grupo nombrado, pero re-evaluando su patrón, no su captura.
regex

(?<word>\w+)\ (?&word)   // palabra repetida: "hola hola"

Verbos de control avanzados

Son metacomandos en la sintaxis (*... ). Algunos:

    (*SKIP)(*FAIL): Descarta todo el texto hasta la posición actual y fuerza que el motor continúe desde después de esa posición. Ideal para ignorar contenido.

regex

<.*?(*SKIP)(*FAIL)|(?<=>)\w+

Encuentra palabras que están fuera de etiquetas HTML: primero salta las etiquetas, luego busca palabras.

    (*COMMIT): Una vez que se ha pasado ese punto, no se permite backtracking que retroceda más atrás del commit. Similar a grupo atómico global.

    (*MARK:nombre) y (*THEN): para control en alternancia.

\K (Keep Out)

Descarta todo lo coincidido a su izquierda. Equivale a un lookbehind positivo variable, pero más eficiente.
regex

€\K\d+\.\d{2}   // captura solo la cantidad, descartando el símbolo €

Soporte Unicode

PCRE2 con las opciones PCRE2_UTF y PCRE2_UCP activa el modo Unicode. En PHP se usa el flag u. Permite \p{...}, \P{...}, y ajusta \w, \d, \b.
php

preg_match('/\p{Greek}/u', 'αβγ'); // true

Limitaciones

    No soporta grupos balanceados como .NET.

    La recursión puede causar stack overflow en profundidades extremas.

    El lookbehind variable en PCRE2 está restringido: no permite cuantificadores sin límite superior dentro del lookbehind si no se puede calcular una longitud máxima (ej. (?<=\d+)\w está bien porque la longitud máxima es ilimitada pero el motor lo maneja, aunque hay límites de recursos). En realidad, PCRE2 permite cualquier patrón, pero intenta averiguar la longitud máxima; si no puede, lo trata como no fijo internamente, y puede recurrir a probar desde el inicio de la cadena, lo cual es ineficiente. Se recomienda acotar cuantificadores.

Ejemplos prácticos en PHP
php

// Extraer números de teléfono con formato español (+34 XXX XXX XXX) sin capturar prefijo
$patron = '/\+34\K\s?\d{3}\s?\d{3}\s?\d{3}/';
preg_match_all($patron, '+34 612 345 678 y +34 987654321', $matches);
// $matches[0] contiene "612 345 678" y "987654321"

// Validar código postal español (5 dígitos, opcionalmente seguido de "-" + 4 dígitos)
$cp = '/^(\d{5})(?:-(\d{4}))?$/';

# JavaScript.md
Motor regex en JavaScript

JavaScript utiliza un motor de regex integrado en los motores V8 (Chrome, Node.js), SpiderMonkey (Firefox), JavaScriptCore (Safari). Históricamente ha sido limitado, pero las versiones modernas (ES2015 en adelante) han añadido características significativas.
Evolución y versiones
Versión	Añadidos
ES3 (1999)	Base: literales /.../, grupos de captura, backreferences, cuantificadores greedy, lookahead, m, i, g.
ES5 (2009)	"use strict" sin cambios en regex.
ES2015 (ES6)	Flag u (Unicode), flag y (sticky). Nueva sintaxis de escape unicode \u{...}.
ES2018	Flag s (dotAll), lookbehind (?<= ) / (?<! ), grupos con nombre (?<name>...), propiedades Unicode \p{...}.
ES2020	String.prototype.matchAll (iterador).
ES2021	Sin cambios importantes.
ES2022	Flag d (hasIndices) para obtener posición de grupos.
Características actuales (ES2022+)

    Lookahead positivo y negativo: soportados de siempre.

    Lookbehind (desde ES2018): soporta longitud variable sin restricciones.

    Grupos con nombre: (?<year>\d{4}) y acceso vía match.groups.year.

    Propiedades Unicode: /\p{Script=Greek}/u.

    Flag s (dotAll): . incluye \n.

    Flag y (sticky): Búsqueda desde la posición exacta indicada por lastIndex sin ignorar caracteres previos.

    Flag d (indices): match.indices retorna arrays con inicio/fin de cada grupo.

Lo que NO tiene JavaScript

    Grupos atómicos (?>...).

    Cuantificadores posesivos *+, ++.

    Recursión y subrutinas.

    Condicionales (?(cond)si|no).

    \K (keep out).

    Verbos de control como (*SKIP).

    Modo verboso (no hay flag x). Los patrones se escriben como cadenas normales.

Simulación de grupos atómicos en JS

Podemos emular un grupo atómico usando un lookahead y una backreference:
javascript

// Simular (?>a+)b
let regex = /(?=(a+))\1b/;
// El lookahead captura todas las 'a', luego \1 las consume sin poder retroceder.

Este truco funciona para patrones simples. Para casos más complejos con alternancia no es suficiente.
Flag y (sticky)

La búsqueda solo tiene éxito si la coincidencia comienza exactamente en la posición regex.lastIndex.
javascript

let regex = /\d+/y;
regex.lastIndex = 2;
"abc 123".match(regex); // null, porque en posición 2 está 'c '
regex.lastIndex = 4;
"abc 123".match(regex); // "123"

Es útil en tokenizadores.
Flag d (hasIndices)

Devuelve las posiciones de inicio y fin de la coincidencia y de cada grupo.
javascript

let regex = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/d;
let match = regex.exec('2024-12-25');
match.indices.groups.year; // [0, 4]

Buenas prácticas en JS

    Usar el constructor RegExp cuando el patrón es dinámico, escapando adecuadamente las barras.

    Aprovechar plantillas de cadena para mayor legibilidad:

javascript

let pattern = new RegExp(String.raw`
  ^
  (?<area>\d{3})
  -
  (?<number>\d{7})
  $
`.replace(/\s+/g, ''), ''); // eliminar espacios simulando modo verboso

    Cuidado con el escape de barras invertidas en cadenas normales: '\d' se convierte en d a menos que sea '\\d'.

Ejemplos prácticos en JS
javascript

// Extraer hashtags de un tweet, devolviendo solo palabras sin #
let tweet = "Hola #gente #regex #JS2024";
let hashtags = [...tweet.matchAll(/(?<=#)\w+/gu)].map(m => m[0]);
// ["gente", "regex", "JS2024"]

// Validar email con Unicode
let emailRegex = /^[\p{L}._%+\-]+@[\p{L}.\-]+\.[\p{L}]{2,}$/u;
emailRegex.test("jörn@müller.de"); // true

# Python.md
Dos motores en Python

Python tiene dos opciones para trabajar con regex:

    Módulo re: incluido en la biblioteca estándar. Limitado en funcionalidades avanzadas.

    Módulo regex (externo, PyPI): instalable con pip install regex. Superset compatible con re pero añade soporte de PCRE (recursión, lookbehind variable, grupos atómicos, etc.).

Módulo re estándar
Características

    Lookahead positivo/negativo.

    Lookbehind positivo/negativo solo con patrones de ancho fijo (cada alternativa debe tener la misma longitud, sin cuantificadores variables).

    Grupos con nombre (?P<name>...) (única sintaxis).

    Flags: re.I (IGNORECASE), re.M (MULTILINE), re.S (DOTALL), re.X (VERBOSE), re.A (ASCII), re.U (UNICODE, por defecto en Python 3).

    No posee: grupos atómicos, cuantificadores posesivos, \K, recursión, condicionales, \p{Unicode}.

Limitaciones del lookbehind
python

import re
re.search(r'(?<=abc|def)x', 'abcx')   # OK, longitudes iguales (3)
re.search(r'(?<=a+)x', 'aax')        # Error: look-behind requires fixed-width pattern

El módulo re también es bastante estricto con los escapes; no admite escapes desconocidos (como \q), mostrando advertencias.
Flags como constante de función

Se pasan a re.compile() o directamente a las funciones:
python

re.findall(r'patrón', texto, re.IGNORECASE | re.DOTALL)

Modo verboso

Muy útil para patrones complejos:
python

pattern = re.compile(r"""
    ^
    (\d{4})   # año
    -
    (\d{2})   # mes
    -
    (\d{2})   # día
    $
""", re.VERBOSE)

Módulo regex (externo)
Instalación y compatibilidad
bash

pip install regex

python

import regex

Su API es casi idéntica a re, pero añade más capacidades. Se maneja con las mismas funciones (search, match, findall, sub), y soporta las mismas flags más algunas nuevas (regex.VERBOSE, etc.).
Nuevas características

    Lookbehind variable sin restricciones.

    Grupos atómicos (?>...).

    Cuantificadores posesivos *+, ++.

    Recursión (?R), (?0), subrutinas (?&nombre).

    Condicionales (?(cond)si|no).

    Propiedades Unicode \p{Lu}, \p{Script=Latin}.

    \K para descartar lo coincidido a la izquierda.

    Coincidencia aproximada (módulo fuzzy).

    Flags inline (?i), (?-i), (?i:...).

Ejemplo de lookbehind variable en regex
python

import regex
m = regex.search(r'(?<=a+)b', 'aaab')
m.group()  # 'b'

Ejemplo de grupo atómico
python

regex.search(r'(?>a+)b', 'aab')   # match (con aab)
regex.search(r'(?>a+)b', 'aaaa')  # None, sin backtracking

Recursión
python

regex.search(r'\( ( [^()] | (?R) )* \)', '( (a) (b) )', regex.X)

Modo Unicode completo

El módulo regex maneja Unicode de forma excelente; \w reconoce caracteres de palabra de cualquier alfabeto como el módulo re en Python 3 (por defecto Unicode), pero además \d también puede ser dígito Unicode si se usa la flag regex.U (activada por defecto) mejorada. Además \p{...} funciona.
Comparación rápida re vs regex
Característica	re	regex
Lookbehind fijo	✔	✔
Lookbehind variable	✘	✔
Grupos atómicos	✘	✔
Posesivos	✘	✔
Recursión	✘	✔
\K	✘	✔
\p{Unicode}	✘	✔
Coincidencia aproximada	✘	✔ (fuzzy)
Rendimiento (general)	Rápido (implementación en C)	Más lento en algunas operaciones
Buenas prácticas en Python

    Usa raw strings r'' para evitar dobles escapes.

    Prefiere re.compile() cuando el patrón se reutiliza.

    Si necesitas funcionalidades avanzadas, adopta regex; su interfaz es compatible.

    Para textos con Unicode, el módulo re ya es adecuado; para propiedades o recursión, ve a regex.

# Java.md
Motor java.util.regex

Java incluye un motor de regex rico en características, aunque no tan completo como PCRE o .NET. Se basa en backtracking y ofrece:

    Lookahead positivo/negativo.

    Lookbehind positivo/negativo con longitud máxima finita (debe poder determinarse un máximo de caracteres consumidos).

    Grupos atómicos (?>...).

    Cuantificadores posesivos *+, ++, ?+, {n,m}+.

    Grupos con nombre (?<name>...) (desde Java 7).

    Propiedades Unicode \p{...} (ej. \p{Lu}, \p{IsLatin}).

    Condicionales NO soportados (a diferencia de PCRE/.NET).

    Recursión, subrutinas, \K: no soportados.

    Flags: Pattern.CASE_INSENSITIVE, MULTILINE, DOTALL, UNICODE_CHARACTER_CLASS, COMMENTS (verboso), CANON_EQ, UNIX_LINES.

Lookbehind con límite finito

Java permite cuantificadores dentro del lookbehind siempre que tengan un límite superior explícito. * y + solos están prohibidos porque no hay máximo finito; en su lugar se deben usar {0,n}.
java

Pattern p = Pattern.compile("(?<=a{1,10})b"); // válido
Pattern.compile("(?<=a+)b"); // ERROR: Look-behind pattern does not have an obvious maximum length

Las alternativas pueden tener longitudes diferentes.
Clases Character y Unicode

Con la flag Pattern.UNICODE_CHARACTER_CLASS (o (?U)), las clases predefinidas \w, \d, \s siguen el estándar Unicode. Sin ella, \d es [0-9] y \w es [a-zA-Z0-9_].
java

Pattern p = Pattern.compile("\\w+", Pattern.UNICODE_CHARACTER_CLASS);
Matcher m = p.matcher("café");
// Con UNICODE_CHARACTER_CLASS, 'é' es parte de \w.

Grupos con nombre (Java 7+)
java

Pattern p = Pattern.compile("(?<year>\\d{4})-(?<month>\\d{2})");
Matcher m = p.matcher("2024-12");
String year = m.group("year");

La retroreferencia interna se hace con \k<name>.
Ejemplo de grupo atómico
java

String patron = "(?>a+)b";
Pattern.compile(patron).matcher("aaab").find(); // true
Pattern.compile(patron).matcher("aaaa").find(); // false (sin backtrack)

Flags y modo verboso

Java soporta el flag COMMENTS (equivalente a x de Perl). Permite espacios y comentarios en el patrón.
java

Pattern p = Pattern.compile(
    "^         # inicio\n" +
    "(\\d{4})  # año\n" +
    "$",
    Pattern.COMMENTS
);

Limitaciones principales respecto a PCRE/.NET

    No hay recursión ni subrutinas.

    No hay \K.

    No hay condicionales.

    El lookbehind debe tener un máximo finito; no se puede escribir (?<=.*)x.

    No hay verbos de control como (*SKIP).

Consejos

    Precompilar los patrones con Pattern.compile para reutilizarlos.

    Escapar bien las barras invertidas en las cadenas Java: \\d, \\s.

    Para texto internacional, usa Pattern.UNICODE_CHARACTER_CLASS.

    Si necesitas funcionalidades no presentes, evalúa usar una biblioteca externa o procesamiento adicional.

Ejemplo práctico

Validar un código postal español (5 dígitos) permitiendo un grupo opcional de 4 dígitos tras guión:
java

Pattern cp = Pattern.compile("^(\\d{5})(?:-(\\d{4}))?$");
Matcher m = cp.matcher("28001-1234");
if (m.find()) {
    String codigo = m.group(1); // "28001"
    String extensión = m.group(2); // "1234"
}

# NET.md
El motor de .NET

El espacio de nombres System.Text.RegularExpressions de .NET (C#, VB.NET, PowerShell) implementa uno de los motores de regex más potentes y flexibles. Data de los primeros Framework y ha sido mejorado en .NET Core y .NET 5+.
Características exclusivas

    Lookbehind completamente variable sin restricciones de longitud.

    Grupos balanceados: permiten emparejar construcciones anidadas arbitrarias (paréntesis, tags) sin recursión.

    Agrupaciones con mismo nombre: varios grupos pueden tener el mismo nombre y capturar múltiples valores a lo largo de la cadena.

    Ejecución de derecha a izquierda con RegexOptions.RightToLeft.

    Soporte completo para Unicode, propiedades, scripts.

    Condicionales (?(cond)si|no).

    Grupos atómicos (?>...).

    Cuantificadores posesivos (solo en algunas versiones, aunque *+ es raro; el grupo atómico suple).

    Sustitución dinámica con MatchEvaluator.

Lookbehind variable

En .NET, cualquier patrón puede aparecer dentro de un lookbehind. El motor retrocede desde la posición actual hacia la izquierda aplicando el patrón.
csharp

Regex.Match("123abc", @"(?<=\d{2,})abc"); // éxito, "abc" precedido por al menos 2 dígitos

Grupos balanceados

Son la joya de .NET para parsear anidamientos. Utilizan los nombres open y close con una pila.

Sintaxis básica:

    (?<nombre>) apila una captura.

    (?<-nombre>) desapila.

    (?(nombre)(?!)) verifica si la pila está vacía.

Ejemplo: paréntesis balanceados en una cadena.
csharp

string pattern = @"
  \(
  (?>
      [^()]+
    | \( (?<depth>)
    | \) (?<-depth>)
  )*
  (?(depth)(?!))
  \)
";
Match m = Regex.Match("(a (b) c)", pattern, RegexOptions.IgnorePatternWhitespace);

    \( y \) delimitan.

    [^()]+ secuencias sin paréntesis.

    \( (?<depth>) empuja en la pila.

    \) (?<-depth>) saca.

    (?(depth)(?!)) falla si la pila no está vacía.

Grupos con el mismo nombre y capturas múltiples

En .NET, (?<num>\d+) aplicado varias veces conserva todas las capturas bajo el mismo nombre, accesibles vía match.Groups["num"].Captures.
csharp

Match m = Regex.Match("12,34,56", @"(?<num>\d+)(?:,(?<num>\d+))*");
foreach (Capture cap in m.Groups["num"].Captures)
    Console.WriteLine(cap.Value); // 12, 34, 56

Condicionales

Soportan condiciones basadas en si un grupo capturó, o si una aserción se cumple.
csharp

// Coincide con "abc" o "ABC" según un prefijo
Regex.Replace("prefix:abc", @"(prefix:)?(?(1)[A-Z]+|[a-z]+)", "...");

Si existe el grupo 1, exige mayúsculas; si no, minúsculas.
Flags y opciones

    RegexOptions.IgnoreCase

    RegexOptions.Multiline

    RegexOptions.Singleline (dotall)

    RegexOptions.IgnorePatternWhitespace (x)

    RegexOptions.ExplicitCapture (solo grupos con nombre capturan)

    RegexOptions.RightToLeft (empieza desde el final de la cadena, útil para búsquedas desde atrás)

    RegexOptions.ECMAScript (comportamiento compatible con JavaScript, desactiva algunas extensiones)

Reemplazos con MatchEvaluator

Permite usar una lambda para decidir la cadena de reemplazo en base al Match.
csharp

Regex.Replace("hola MUNDO", @"\w+", m => m.Value.ToUpper()); // "HOLA MUNDO"

Limitaciones

    No tiene recursión explícita (?R), pero los grupos balanceados cubren la mayoría de casos de anidamiento.

    La sintaxis de posesivos (*+) es aceptada en .NET Core/.NET 5+, aunque no está documentada en todas partes; el grupo atómico es preferible.

    El motor es backtracking y sufre los mismos riesgos de patrones catastróficos.

Ejemplo práctico completo

Extraer todas las urls de un texto, evitando las que están en etiquetas HTML:
csharp

string pattern = @"<a\s[^>]*>.*?</a>(*SKIP)(*FAIL)|https?://[^\s""']+";
// Sin embargo (*SKIP) no existe en .NET. Alternativa con balanceo o MatchEvaluator complejo.

En .NET, para saltar regiones se suele usar un enfoque de split o Regex.Replace con un evaluador.

# POSIX.md
Expresiones regulares POSIX

El estándar POSIX define dos tipos de expresiones regulares para herramientas de línea de comandos Unix/Linux: BRE (Basic Regular Expressions) y ERE (Extended Regular Expressions). Son mucho más simples que los motores modernos y no incluyen la mayoría de las funcionalidades avanzadas.
BRE (Basic Regular Expressions)

Utilizadas por defecto en grep, sed y ed. Características:

    La mayoría de metacaracteres requieren escape: { }, ( ), ?, +, | no son metacaracteres a menos que se escapen con \.

    * sí actúa como cuantificador (cero o más).

    . y [ ] funcionan como siempre.

    ^ y $ representan inicio/fin de línea.

    Retroreferencias: \( ... \) captura un grupo y \1 hace referencia a él. Esto es exclusivo de BRE; ERE no tiene backreferences.

    No hay + nativo (hay que escribir \+), ni ? (\?), ni | (\|).

Ejemplo de BRE:
bash

grep '^\(hello\).*\1$' file.txt   # línea que empieza y termina con "hello" (usando captura)

ERE (Extended Regular Expressions)

Activan con grep -E (o egrep) y sed -E. Añaden metacaracteres sin necesidad de escape:

    +, ?, { }, |, ( ) son reconocidos directamente como especiales.

    Sin retroreferencias: \1 es tratado como carácter literal (error o escape no válido, depende de la implementación). No hay memoria de capturas (aunque ( ) se usan para agrupar, no capturan en el sentido de backreference; en algunas implementaciones pueden capturar pero no se puede hacer backreference).

    No tienen \b ni \B, ni \w/\d/\s (aunque algunas versiones de grep con la opción -w buscan palabras completas externamente).

    No hay lookahead, lookbehind, grupos atómicos, etc.

    Clases POSIX: [[:alnum:]], [[:digit:]], [[:space:]], etc., son soportadas.

Ejemplo de ERE:
bash

grep -E 'colou?r' file.txt   # "color" o "colour"
grep -E '[0-9]{3}-[0-9]{2}' file.txt  # número de seguro social formato USA

Herramientas y uso
Herramienta	Modo por defecto	Activación ERE
grep	BRE	grep -E o egrep
sed	BRE	sed -E (o -r en GNU)
awk	ERE (en la mayoría de implementaciones actuales)	Por defecto (en mawk, gawk)
vi/vim	BRE (en búsquedas con /)	\v (very magic) para ERE
Limitaciones generales

    No admiten cuantificadores no greedy (perezosos). *? no existe.

    No hay anclas de palabra \b; se puede simular con [[:<:]] y [[:>:]] en algunas implementaciones (GNU) pero no es estándar.

    No hay metacaracteres predefinidos como \d, \w; se usan clases POSIX [[:digit:]], [[:alnum:]] o rangos.

    No hay grupos atómicos ni posesivos.

    Son motores DFA (o híbridos en GNU) que evitan el backtracking, por lo que son rápidos y no sufren backtracking catastrófico. Sin embargo, sacrifican funcionalidad.

Escapado en BRE

Para usar (, ), {, }, ?, +, | como metacaracteres, se requiere \. De lo contrario, coinciden literalmente.

    Sin escape: a{3} busca "a{3}" literal.

    Con escape: a\{3\} busca exactamente 3 'a's.

Esto hace que los patrones BRE sean confusos y propensos a errores. Muchos usuarios prefieren siempre el modo ERE para scripts.
POSIX en la práctica moderna

Hoy en día, las herramientas del sistema siguen usando POSIX. Por ejemplo, para validar un email simple en un script de shell con grep -E:
bash

echo "user@domain.com" | grep -E '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

Aunque no es una validación robusta, cubre casos sencillos.
Consejos

    En scripts portables, limítate a POSIX ERE o BRE según la necesidad.

    Para tareas complejas, delega a un lenguaje moderno (Perl, Python, etc.) en vez de luchar con sed/grep.

    Las clases POSIX son la forma más clara de expresar conjuntos en estos entornos.

Ejemplo práctico en sed

Reemplazar múltiples espacios por uno solo:
bash

sed -E 's/[[:space:]]+/ /g' archivo.txt
