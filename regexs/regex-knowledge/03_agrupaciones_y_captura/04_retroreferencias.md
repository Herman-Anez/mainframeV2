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
