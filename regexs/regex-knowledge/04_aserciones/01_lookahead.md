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
