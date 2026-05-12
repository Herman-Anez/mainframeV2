/3//////////////////////////////////////////////////////////////////////////////////////////
# captura_basica.md
¿Qué es un grupo de captura?

Un grupo de captura es una subexpresión encerrada entre paréntesis (...). Cumple dos funciones:

    Agrupar partes del patrón para aplicar cuantificadores, alternancia o anidamiento.

    Capturar la subcadena que coincide con esa subexpresión, permitiendo recuperarla después (en código, reemplazos o mediante retroreferencias).

Ejemplo sencillo:
regex

(\d{3})-(\d{2})-(\d{4})

Aplicado a "123-45-6789", los paréntesis capturan tres partes: "123", "45" y "6789".
Numeración de los grupos

Los grupos de captura se numeran de izquierda a derecha según el orden del paréntesis de apertura. El grupo 0 es siempre la coincidencia completa, y los grupos 1, 2, 3... corresponden a cada paréntesis.
regex

(a(b)c)d

Coincidencia sobre "abcd":

    Grupo 0: "abcd"

    Grupo 1: "abc" (primer paréntesis)

    Grupo 2: "b" (segundo paréntesis, anidado)

    Grupo 3: no existe.

La numeración es fija y no depende de si el grupo participó o no en la coincidencia. Un grupo opcional que no casó tendrá un valor None o vacío según el motor.
Cómo acceder a las capturas desde código

La forma de obtener los grupos varía según el lenguaje:

Python:
python

import re
m = re.search(r'(\d{3})-(\d{2})-(\d{4})', '123-45-6789')
m.group(0)  # '123-45-6789'
m.group(1)  # '123'
m.group(2)  # '45'
m.group(3)  # '6789'
m.groups()  # ('123', '45', '6789')

JavaScript:
javascript

let regex = /(\d{3})-(\d{2})-(\d{4})/;
let match = '123-45-6789'.match(regex);
match[0]; // '123-45-6789'
match[1]; // '123'
match[2]; // '45'
match[3]; // '6789'

Java:
java

Pattern p = Pattern.compile("(\\d{3})-(\\d{2})-(\\d{4})");
Matcher m = p.matcher("123-45-6789");
if (m.find()) {
    m.group(1); // "123"
    m.group(2); // "45"
    m.group(3); // "6789"
}

Grupos anidados

Los paréntesis se pueden anidar; la numeración sigue el orden de apertura. Ejemplo:
regex

((a)(b(c)))d

Texto: "abcd"

    Grupo 1: "abc" (abre primero)

    Grupo 2: "a" (segundo)

    Grupo 3: "bc" (tercero, b(c))

    Grupo 4: "c" (cuarto)

Grupos opcionales y valor nulo

Un grupo puede ser condicional gracias a ? o *. Si la parte no casa, el grupo queda vacío o indefinido.
regex

(a(\d)?b)

En "ab": Grupo 1 "ab", grupo 2 None (o vacío). En "a5b": Grupo 2 "5".
Uso de grupos para aplicar cuantificadores a partes complejas

Sin captura nos sirve para agrupar, por ejemplo:
regex

(https?:\/\/)?(www\.)?example\.com

Los grupos capturan el protocolo y el subdominio si existen, permitiendo extraerlos después.
Captura y alternancia
regex

(jpg|png|gif)$

Captura la extensión del archivo. Sólo se captura la alternativa que coincide.
Eficiencia y memoria

Cada grupo de captura consume memoria porque se almacena la subcadena capturada. En patrones de gran escala puede ralentizar. Si no necesitas las capturas, considera usar grupos sin captura (?:...) (ver siguiente sección).
Buenas prácticas

    Usa nombres de grupo (siguiente sección) para mejorar la legibilidad.

    Cierra siempre los paréntesis; un paréntesis no balanceado genera error.

    Escapa los paréntesis literales: \( y \).

# grupos_sin_captura.md
Definición

Un grupo sin captura agrupa parte de la expresión sin almacenar el texto coincidente. Su sintaxis es (?: ... ). Sirve únicamente para aplicar cuantificadores, alternancia o atomizar una parte sin generar una referencia de captura.

Ejemplo:
regex

(?:https?:\/\/)?(?:www\.)?example\.com

Los grupos no capturan protocolo ni subdominio, pero sí están agrupados para hacerlos opcionales.
Ventajas frente a los grupos de captura

    Eficiencia: Al no almacenar la subcadena, se ahorra memoria y tiempo.

    Claridad: Indica a quien lee el patrón que esa subcoincidencia no se usará después.

    Evita interferencias: Si ya tienes varios grupos de captura y necesitas uno adicional para agrupar sin cambiar la numeración existente, un grupo sin captura no añade nuevos índices.

Por ejemplo, si tienes (\d{4})-(\d{2})-(\d{2}) y decides agrupar el separador sin capturarlo, puedes escribir (\d{4})(?:-(\d{2}))? para que el guión y el segundo número sean opcionales. El grupo 1 es el año, el grupo 2 el mes (si existe), sin introducir un grupo extra para el guión.
Sintaxis y uso

    (?:patrón) : agrupa patrón.

    Se puede aplicar cuantificadores: (?:abc)+ coincide con una o más repeticiones de "abc".

    En alternancia: (?:gato|perro) igual que gato|perro, pero a veces es necesario para encapsular.

Comparación con grupos de captura

Dado el texto "rojo verde azul":

    Captura: ((?:r|v)\w+) captura palabras que empiezan con 'r' o 'v'. El primer grupo captura toda la palabra, el grupo interno es sin captura. Así grupo 1 es la palabra sin almacenar la letra inicial por separado.

    Si usáramos (r|v)(\w+) tendríamos dos capturas: letra y resto.

Grupos sin captura y modificadores de modo

En algunos motores se pueden incluir flags localizadamente con (?flags:...), que es un grupo sin captura con modificadores. Ejemplo: (?i:abc) casará "ABC", "Abc", etc., sin afectar el resto del patrón. Funciona en PCRE, Perl, .NET, Java. Python re no soporta (?i:...) (sí soporta (?i) a nivel global o en el módulo regex externo).
Ejemplo práctico: extracción de fecha con separadores flexibles
regex

(\d{4})(?:[-/.])(\d{2})(?:[-/.])(\d{2})

Coincide con 2024-12-25, 2024/12/25, 2024.12.25. Captura año (grupo 1), mes (2) y día (3). Los separadores están en grupos sin captura.
Cuándo NO usar grupos sin captura

Si posteriormente necesitas acceder a la subcadena (por ejemplo, para reemplazos con $1 o para procesado), debes mantener los paréntesis de captura. Los grupos sin captura son invisibles para las retroreferencias y las funciones de extracción.

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

# retroreferencias.md
Definición

Una retroreferencia es una construcción que hace referencia a un grupo de captura previamente encontrado en el mismo patrón. Permite exigir que el texto actual coincida exactamente con lo capturado por ese grupo.
Sintaxis básica

    \1, \2, ... \9 (y en algunos motores \10 o más usando \10 como referencia al grupo 10, pero puede ser ambiguo; en PCRE se usa \g{10} o \10 solo si hay al menos 10 grupos, sino se interpreta como backreference 1 seguido de '0'. Mejor usar \g{n} para números grandes.)

Para grupos con nombre:

    Python (?P=name)

    PCRE/JS/Java/.NET: \k<name> o \k'name'

Ejemplo clásico: palabras repetidas
regex

\b(\w+)\s+\1\b

Coincidencia: "hola hola", "mundo mundo". Explicación:

    (\w+) captura una palabra.

    \s+ espacios.

    \1 forzosamente debe ser la misma palabra capturada.

Coincidencia de comillas y delimitadores
regex

(["'])(.*?)\1

En "una frase" o 'otra', captura la frase dentro de comillas iguales. El grupo 1 captura la comilla de apertura y \1 fuerza la misma de cierre.
Numeración y retroreferencias en grupos anidados

Dado ((a)(b(c)))d, las referencias:

    \1 → abc

    \2 → a

    \3 → bc

    \4 → c

Las retroreferencias pueden referirse a grupos que aparecen después (en motores que permiten backreferences hacia adelante, aunque son muy raras y generalmente no se recomiendan). Lo normal es que el grupo referenciado esté a la izquierda de la retroreferencia.
Referencias en cadenas de reemplazo

Muchas herramientas usan $1, $2 o \1, \2 en la cadena de sustitución, refiriéndose a los grupos capturados en la búsqueda. Por ejemplo:

    s/(\w+)\s+(\w+)/$2 $1/ en sed/Perl invierte dos palabras.

    En Python: re.sub(r'(\w+)\s+(\w+)', r'\2 \1', texto).

Atención: Las retroreferencias en la cadena de reemplazo no son iguales a las del patrón. En el patrón se usa \1 (sólo motores), en reemplazo depende del motor; en Python se usa \1, en JavaScript $1. Las retroreferencias en el patrón exigen coincidencia exacta de la subcadena capturada.
Retroreferencias a grupos no existentes o que no participaron

Si un grupo es opcional y no casa, la retroreferencia puede considerarse un carácter vacío y casará con el vacío (en muchos motores) o fallará. Ejemplo: (a)? \1 en "b b". El grupo 1 no casa, entonces \1 intenta casar con vacío; normalmente no hay casamiento porque espera algo. En la práctica, una referencia a un grupo que no participó hace fallar la expresión. Específicamente, en PCRE una backreference a un grupo que no capturó provoca un fallo de coincidencia a menos que se permita referencia vacía. En Python re, si el grupo no participó, la backreference falla (no coincide con nada). Por eso es aconsejable que el grupo sea obligatorio si se va a referenciar.
Retroreferencias y recursión / subrutinas

En motores con soporte avanzado (PCRE, Perl), se puede usar (?1), (?&nombre) para llamar a un subpatrón como subrutina (no solo comparar con lo capturado, sino re-ejecutar el subpatrón). Esto es distinto a las retroreferencias, que simplemente comparan con la cadena literal previamente capturada. Las retroreferencias comprueban igualdad de texto, no repetición del patrón.

Ejemplo: (\d{3})-\1 obliga a que los dos bloques de dígitos sean idénticos. Si quisieras repetir el patrón (tres dígitos cualesquiera), simplemente repetirías \d{3}.
Número máximo de retroreferencias

En la mayoría de motores, \1 a \9 están disponibles. Para números de dos dígitos, se usa \10 o \g{10} para evitar ambigüedad. En PCRE, \10 se interpreta como backreference 10 si hay al menos 10 grupos, sino como backreference 1 seguido de '0'. La notación \g{10} es segura para cualquier número. Python re no soporta \g{n} estándar, pero en la práctica con números mayores de 99 es extremadamente raro.
Limitaciones y riesgos

    Las retroreferencias pueden causar backtracking intenso porque el motor debe volver a intentar la captura de la referencia si hay múltiples posibilidades. Ejemplo: ^(a+)\1$ sobre "aaaa" funciona bien, pero si se extiende, puede degradar.

    No son implementables en autómatas finitos puros; los motores híbridos (DFA) no las soportan.

# grupos_atomicos.md
Definición

Un grupo atómico es una agrupación que, una vez que ha coincidido, no permite backtracking hacia su interior. Su sintaxis es (?> ... ). Está disponible en PCRE, Perl, Java, .NET, Python con el módulo regex externo. No está presente en JavaScript ni en el módulo re estándar de Python.
Comportamiento

Cuando el motor entra en un grupo atómico (?>subexpresión), intenta casar la subexpresión. Si tiene éxito, sale del grupo y descarta todos los estados internos de backtracking. Si posteriormente el resto del patrón falla, el motor no reintentará con menos repeticiones ni otras alternativas dentro del grupo atómico. Simplemente fallará la coincidencia global desde esa posición y buscará en otro lugar (si procede).

Esto es muy similar a los cuantificadores posesivos (un cuantificador posesivo es equivalente a un grupo atómico que envuelve un elemento con cuantificador). Por ejemplo:
a++ es equivalente a (?>a+).
Ejemplo de funcionamiento
regex

(?>a+)b

Texto: "aaaab"

    Entra en el grupo, a+ consume todas las as (4). Sale del grupo atómico.

    Luego intenta casar b con el siguiente carácter. Como es posesivo, no retrocede para ceder as. En "aaaab" el siguiente es b, éxito, capture "aaaab".

Texto: "aaaa"

    a+ consume las 4 as. Sale del grupo atómico.

    Intenta b pero no hay más caracteres. Falla global sin backtracking interior. Habría fallado igual que con a++b.

Diferencia crucial con grupo normal (no atómico)

Con un grupo normal (a+)b en "aaaa":

    a+ consume todas las as.

    Intenta b, falla.

    Backtrack: a+ cede una a, ahora tiene 3 as. Intenta b, aún falla, cede otra, etc., hasta agotar. Esto genera varios pasos de retroceso, pero en este caso simple no es grave. En patrones complejos con anidamientos, la ausencia de backtracking mejora enormemente el rendimiento.

Usos principales

    Optimización: Evitar backtracking catastrófico. Si sabemos que dentro del grupo no necesitamos que el motor reconsidere cuántos caracteres tomó, lo encerramos en un grupo atómico. Ejemplo clásico: (?>.*?) no tiene sentido porque .*? es perezoso, pero un grupo atómico con .* puede ser útil para capturar hasta un delimitador sin retroceder: (?>[^"]*) para contenido sin comillas, aunque una clase negada no provoca backtracking de todas formas.

    Patrones de desastre: (a+)*b con entrada "aaaa..." causa backtracking exponencial. Si transformamos a (?>a+)*b o (a++)*b, eliminamos el problema.

    Garantizar que una palabra completa se capture sin retroceder: \b(?>\w+)\b asegura que una vez que se toma una palabra no se suelte parte para intentar un casamiento más largo (útil si hay alternancia que podría casar con prefijos). Pero normalmente las clases negadas o cuantificadores greedys sin opciones no causan problema; el grupo atómico es relevante cuando hay alternancia interior.

Simulación en motores sin soporte

En JavaScript (sin grupos atómicos ni posesivos), se puede simular un grupo atómico con un lookahead y una retroreferencia:
javascript

// Simular (?>a+)b
/(?=(a+))\1b/

El lookahead captura a+ de forma greedy, la retroreferencia \1 consume exactamente esa captura sin posibilidad de backtracking. Así se evita que el motor ceda as. Pero hay limitaciones: no se puede simular un grupo atómico complejo con múltiples alternativas si hay solapamientos. Otra técnica en JS: usar (?:a+)(?!...) no es igual.

En Python re estándar, no hay grupos atómicos; se puede recurrir al módulo regex.
Combinación con otros constructos

Los grupos atómicos pueden contener otras agrupaciones y cuantificadores.

Ejemplo avanzado: validar un número racional con formato \d+(\.\d+)? sin permitir retroceso en la parte entera si la parte decimal falla:
regex

(?> \d+ ) (?: \. \d+ )?

Aunque en este caso el backtracking no sería perjudicial, es un ejemplo.
Precauciones

Un grupo atómico no debe usarse si la coincidencia global puede requerir retroceder dentro de él. Por ejemplo, (?>".*?") para buscar cadenas entre comillas fallará con "hola" y "mundo" porque .*? dentro del grupo atómico consume lo mínimo y nunca retrocede, pero en realidad necesitamos que el grupo abarque "hola". Si ponemos (?>".*?"), en "hola" y "mundo" la primera comilla se empareja, .*? toma cero caracteres, luego espera la comilla final, encuentra " inmediatamente (porque "hola" tiene una comilla tras "). En realidad (?>".*?") sí podría funcionar porque .*? se expande como parte de su propia lógica perezosa, pero el grupo es atómico y eso impediría que una vez que el grupo encontró una coincidencia válida (una cadena mínima), si luego falla el resto del patrón, no se reconsideren más cadenas más largas. Podría no ser lo deseado. La regla: úsalo cuando la subexpresión interior no necesita ser ajustada para dar paso a la coincidencia global tras la salida del grupo.
Ejemplo de optimización real: números con miles separados
regex

(?> \d{1,3} (?: , \d{3} )* ) (?: \. \d+ )?

Agrupar la parte entera en grupo atómico evita que el motor intente distribuciones alternativas de comas si la entrada es inválida, acelerando el fallo.
/////////////////////////////////////////////////////////////////////////////
