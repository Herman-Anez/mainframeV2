# grupos_nombrados.md
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

Retroreferencia dentro del patrón: (?P=year) para casar el mismo año.

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
# grupos_nombrados.md
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

Retroreferencia dentro del patrón: (?P=year) para casar el mismo año.

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
