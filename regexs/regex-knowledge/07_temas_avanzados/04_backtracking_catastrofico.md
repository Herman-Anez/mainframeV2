# backtracking_catastrofico.md
¿Qué es el backtracking?

En los motores de regex basados en NFA (la mayoría: Perl, PCRE, Java, Python, .NET, JS), cuando una parte del patrón puede casar de múltiples maneras (cuantificadores, alternancia), el motor prueba una posibilidad, y si falla más adelante, retrocede (backtrack) para intentar otra combinación. Este mecanismo es flexible pero puede degenerar en una explosión combinatoria.
El problema: backtracking catastrófico

Ocurre cuando un patrón requiere un número enorme de pasos de retroceso para determinar que no hay coincidencia, creciendo de forma exponencial con la longitud de la entrada. Esto puede causar que la aplicación se congele, consuma toda la CPU o reciba un timeout.

El ejemplo más famoso es (a+)+b aplicado a una cadena larga de as sin b al final, como "aaaaaaaaaaaaaaaaaaaaX".
Análisis detallado del ejemplo (a+)+b

    (a+)+ significa uno o más grupos de una o más as.

    Para una cadena "aaaa":

        El primer a+ puede tomar 4 as (como grupo), y el cuantificador externo + permite repetir ese grupo 1 vez. Luego espera b.

        Si b no existe, el motor puede hacer backtrack: el + externo cede caracteres, el a+ interno redistribuye.

        Número de formas de particionar las as en grupos: para 4 as, hay múltiples combinaciones (ej. 4 grupos de 1, 2+2, 1+1+2, etc.). El motor probará todas.

    Con 10 as el número de combinaciones es ~512, con 20 as ya es cientos de miles, con 30 puede ser millones o más, crecimiento exponencial.

Otros patrones problemáticos comunes

    (a|aa)+b : Explosión similar.

    .*.*=.* : Múltiples puntos greedys anidados pueden disparar backtracking interno.

    [^,]*,[^,]*,[^,]* con entrada que tiene menos comas de las esperadas.

    (".*?"|'.*?') cuando hay muchas comillas en el texto y no está ordenado.

Cómo identificarlos

Síntomas:

    Regex extremadamente lentas con ciertas entradas (aunque sean cortas).

    Falla con timeout en validadores online.

    Herramientas como regex101.com muestran el número de pasos; si es excesivo (> 1000 para entradas simples).

    Buscar patrones con cuantificadores anidados (...+)+, (...*)*, (.+?) dentro de grupos que se repiten.

Estrategias para prevenir y solucionar

    Cuantificadores posesivos (++, *+, ?+, {n,m}+): eliminan el backtracking dentro del cuantificador. Una vez que coinciden, no ceden caracteres.
    regex

    (a++)+b  // en "aaaaX" falla inmediatamente

    Grupos atómicos (?>…): igual que posesivos, pero aplicado a un grupo más complejo.
    regex

    (?>a+)+b

    Reescribir el patrón eliminando anidamiento innecesario. En lugar de (a+)+b, usar a+b (sin anidar) cuando sea posible.

    Usar clases negadas en lugar de puntos perezosos: [^"]* en vez de .*? para contenido entre comillas.

    Limitar cuantificadores sin límite: cuando se pueda, usar {1,100} en lugar de * o + sin cota.

    Aprovechar anclas para fallar temprano: ^…$.

    Reordenar alternancias: poner la opción más probable o la que casa menos primero puede reducir retrocesos.

    Lookaheads para restringir sin consumir, ej. (?=[a-z]+\d)[a-z0-9]+ puede evitar backtrack.

Herramientas de diagnóstico

    regex101.com: en el panel "debugger" muestra paso a paso y cuenta los pasos. Avisa con "catastrophic backtracking" si detecta patrón peligroso.

    Node.js: uso de la librería re2 (más segura, sin backtracking) o limitar tiempo con safe-regex.

    Python regex: permite poner límite de tiempo (regex.match(pattern, text, timeout=1)).

Ejemplo práctico: extraer campos CSV evitando backtracking

Patrón inseguro: (?:[^;]*;)+ con entrada larga sin punto y coma al final.
Seguro: [^;]*+(?:;[^;]*+)*+ usando posesivos, o usar split a nivel de código.
Impacto en entornos de producción

Un servidor web que valida entradas de usuario con una regex vulnerable puede ser blanco de un ataque ReDoS (Regular expression Denial of Service). Por eso en aplicaciones críticas se evitan patrones complejos no acotados o se usan motores alternativos como RE2/Hyperscan (garantizados en tiempo lineal).
Conclusión

Conocer el backtracking catastrófico es vital para escribir regex robustas. Ante patrones complejos, siempre pensar en el peor caso y utilizar las herramientas de optimización (posesivos, atómicos, reestructuración) para mantener el rendimiento predecible.
