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
