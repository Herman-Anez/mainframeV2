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
