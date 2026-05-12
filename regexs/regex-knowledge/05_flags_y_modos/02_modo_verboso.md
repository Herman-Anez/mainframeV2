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
