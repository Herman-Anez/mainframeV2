# posesivos.md
Definición y sintaxis

Los cuantificadores posesivos son una extensión presente en algunos motores (PCRE, Java, .NET, Perl, módulo regex de Python). Se forman añadiendo un + después del cuantificador normal.

Lista:
text

*+     -> cero o más, posesivo
++     -> una o más, posesivo
?+     -> cero o una, posesivo
{n,}+  -> n o más, posesivo
{n,m}+ -> entre n y m, posesivo

Comportamiento

Un cuantificador posesivo consume la máxima cantidad posible de caracteres, igual que el greedy, pero con una diferencia crucial: nunca retrocede (backtrack). Una vez que toma una porción, no la devuelve aunque eso impida que el resto del patrón coincida.

Esto significa que si el resto de la expresión falla, el motor no intentará ceder caracteres del cuantificador posesivo; simplemente fallará esa rama de la búsqueda y continuará probando desde otras posiciones (backtrack global), pero sin reajustar el interior del cuantificador.

Ejemplo:
regex

a++b

Sobre "aaaab":

    a++ consume todas las as (4 as).

    Luego intenta coincidir b, pero el carácter siguiente es b → éxito, coincide "aaaab".

Sobre "aaaa":

    a++ come todas las as (4 as).

    Luego intenta b, pero no hay más caracteres. Como el cuantificador es posesivo, no retrocede para ceder as. Fallo global inmediato. Con un greedy normal a+b, el motor cedería una a, probaría b, cedería otra, etc., generando backtracking que finalmente falla igual, pero con coste computacional.

Ventajas

    Eficiencia y prevención de backtracking catastrófico: Al eliminar estados de retroceso interiores, se reduce drásticamente el número de intentos. Es una herramienta de optimización.

    Seguridad: En patrones complejos donde sabemos que no queremos que el cuantificador ceda, el posesivo garantiza que no habrá retroceso, evitando bucles infinitos.

Caso de uso típico: cuantificadores anidados

El patrón (?:a+)*b sobre "aaaaaaaaaaaaaaac" sufre backtracking exponencial. Si usamos un grupo atómico o cuantificadores posesivos en el interior (?:a++)*b (o (?>a+)*b), el motor falla mucho más rápido porque no retrocede dentro de a+ para intentar distribuciones alternativas.

Ejemplo real: Validar que una cadena no contiene ciertos patrones puede requerir cuantificadores posesivos para ser eficiente.
Soporte en motores

    PCRE / PHP: *+, ++, etc. disponibles.

    Perl: Soportados.

    Java: Soportados.

    .NET: Soportados.

    Python: El módulo re estándar NO soporta cuantificadores posesivos. El módulo externo regex (PyPI) sí los soporta.

    JavaScript (ECMAScript): NO los soporta. No hay sintaxis disponible. Se pueden simular usando grupos atómicos (que tampoco están soportados) o mediante trucos con lookahead.

Simulación en motores que no los soportan

Si necesitas un comportamiento posesivo en JS o Python re, puedes usar un grupo atómico (si está disponible) o una construcción de lookahead:

Para a++b sin posesivo, la equivalencia sería (?=a+)\1b, pero solo en motores con retroreferencias. Sin embargo, no es exactamente igual; en casos complejos es mejor reestructurar la lógica.

Otra opción: usar (?>a+)b (grupo atómico), pero en JS esto no existe. En JavaScript, un truco para a++b podría ser (?=(a+))\1b. El lookahead captura las as y la retroreferencia las consume sin posibilidad de retroceder en el grupo externo (porque la retroreferencia es una coincidencia fija). Esto imita parcialmente el posesivo.
Precauciones

Los cuantificadores posesivos pueden cambiar la semántica. Si la coincidencia global podría lograrse cediendo caracteres del cuantificador, un posesivo lo impedirá. Solo deben usarse cuando sabemos que no se necesita tal cesión.

Ejemplo patrón: ".*+" nunca coincidiría con "hola" porque .*+ consumiría todo hasta el final, incluyendo la comilla de cierre, y luego no podría retroceder para que la comilla final case. Mientras que el greedy ".*" sí lo haría. El posesivo aquí es inadecuado.
