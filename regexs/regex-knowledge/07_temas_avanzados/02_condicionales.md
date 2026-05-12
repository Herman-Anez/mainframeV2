# condicionales.md
¿Qué son los condicionales en regex?

Son construcciones que permiten elegir entre dos (o más) patrones basándose en una condición. Sintaxis:
(?(condición)patrón-si|patrón-no)
La condición puede ser:

    Un número de grupo captura, ej. (?(1)…) (si el grupo 1 participó en la coincidencia).

    Un nombre de grupo: (?(<nombre>)…) o (?(nombre)…).

    Una aserción (lookahead o lookbehind): (?(?=…)patrón-si|patrón-no).

Condición basada en grupo existente
regex

(\+34)?(\d{9})(?(1)|(?:ERROR))

    Captura opcional de +34 en grupo 1.

    Luego dígitos.

    Condicional: si el grupo 1 existe (se capturó el prefijo), no hace nada extra (vacío después de |). Si no, intenta casar "ERROR" (o simplemente falla si no queremos match sin prefijo). Una forma más práctica: permitir formato con o sin prefijo, pero aplicar lógica.

Ejemplo real: fecha con formato flexible donde el separador debe ser consistente.
regex

(\d{4})([-/])(\d{2})\2(\d{4} | (?(1)\d{4}|\d{2}))

Patrón clásico: número de teléfono con prefijo opcional
regex

^(?:(\+34)\s?)?\d{9}(?(1)|(?=.))

Si el grupo 1 capturó +34, entonces continúa; si no, el condicional falla a menos que pongamos un patrón alternativo.
Condición con aserción
regex

(?(?=[A-Z])[A-Z]\w*|[a-z]\w*)

Si la posición actual empieza con mayúscula, usa patrón de mayúscula; si no, de minúscula. Equivalente a alternancia con lookahead, pero más elegante.
Condicionales y grupos nombrados

En PCRE, Perl, .NET, Python regex:
regex

(?<quote>['"])?(?(<quote>).*?\k<quote>|\S+)

Si se captura una comilla (simple o doble), busca contenido hasta la misma comilla. Si no, captura una palabra sin espacios.
Soporte por motor

    PCRE / PHP: condicionales completos, con grupos y aserciones.

    Perl: completo.

    Python regex: soporta grupos y aserciones; re estándar no.

    .NET: completo.

    Java, JavaScript: no soportan condicionales.

Sintaxis detallada

    (?(n)si|no) : n es el número de grupo de captura (sin escape).

    (?(<name>)si|no) o (?(name)si|no).

    (?(?=...)si|no) aserción positiva.

    (?(?!...)si|no) aserción negativa.

    Se puede omitir la rama no (dejarla vacía): (?(1)si) .

Casos de uso prácticos

    Formato de moneda condicional: si hay decimales, forzar dos dígitos; sino, número entero.
    regex

    \$(?:(\.\d{2})|(\d+))(?(1)(?=.\d{2})|\b)

    Comillas tipográficas: asegurar que citas empiecen y terminen con el mismo tipo de comilla (« » vs " ").

    Paréntesis opcionales balanceadas: (\(?\d+\)?)? ... con condicional para cerrar correctamente.

Alternativas cuando no hay soporte

En motores sin condicionales, se puede simular con una alternancia que repita partes del patrón:
regex

(\+34)?\d{9}  ->  (?:\+34\d{9}|\d{9})

Pero se pierde la capacidad de referir dinámicamente a la captura. Para lógicas más complejas, es necesario usar código huésped (dos regex separadas y una lógica if).
Precauciones

    Las condiciones pueden complicar el patrón y hacerlo menos legible; usar el modo verboso para documentar.

    Al igual que otras construcciones avanzadas, pueden aumentar el backtracking si no se acotan.
