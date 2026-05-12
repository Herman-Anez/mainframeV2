# ejemplos_practicos.md

A continuación, ejemplos que muestran la aplicación real de cuantificadores codiciosos, perezosos y posesivos, con explicaciones paso a paso.
1. Extracción de etiquetas HTML

Objetivo: Obtener el contenido entre etiquetas <strong>...</strong>.

Texto: Este es <strong>un texto</strong> importante y <strong>otro</strong> más.

    Greedy incorrecto: <strong>.*</strong>
    Coincidencia: "<strong>un texto</strong> importante y <strong>otro</strong>"
    El .* consume todo hasta el último </strong>. Malo si queremos capturas individuales.

    Lazy correcto: <strong>.*?</strong>
    Coincidencias (global): <strong>un texto</strong> y <strong>otro</strong>.
    .*? se detiene en el primer </strong>.

    Posesivo inadecuado: <strong>.*+</strong>
    El .*+ consumiría todo el resto del documento y nunca encontraría el </strong>, fallando por completo.

2. Validación de números de teléfono con formato flexible

Requerimiento: Dígitos, posible guiones o espacios como separadores, longitud total controlada.

Regex: ^[\d]+([\s-]?[\d]+)*$

    [\d]+ uno o más dígitos al inicio.

    Grupo ([\s-]?[\d]+)* cero o más bloques de opcional separador + dígitos.
    Funciona bien con greedy, pero puede tener backtracking con entradas como "123-456-7890" que son válidas.

Si se aplica un cuantificador posesivo: ^[\d]++([\s-]?+[\d]++)*+$ para optimizar y asegurar que no retroceda en dígitos. (Sólo en motores con soporte)
3. Manejo de cadenas entre comillas escapadas

Problema: Extraer cadenas delimitadas por comillas dobles, donde dentro puede haber comillas escapadas \".

Texto: "hola \"mundo\" bien" "adiós"

Patrón greedy básico: "(.*?)" sólo coge "hola \" (porque la primera comilla de cierre está después de hola \). Necesitamos ignorar comillas escapadas.

Solución robusta con perezoso y alternancia:
regex

"([^"\\]|\\.)*?"

Explicación:

    " comilla inicial.

    ([^"\\]|\\.)*? cero o más veces (perezoso) de:

        [^"\\] cualquier carácter que no sea comilla ni barra.

        \\. barra invertida seguida de cualquier carácter (captura escapados).

    " comilla final.

Al usar *? nos aseguramos que se detenga en la primera comilla no escapada.
4. Log parsing: extracción de direcciones IP del primer campo

Línea de log: 192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /page HTTP/1.1" 200 2326

Para extraer la IP: ^(\S+).

    ^ inicio de línea.

    \S+ uno o más caracteres no espacio (greedy, pero como \S no puede cruzar espacios, no hay riesgo).

    Captura la IP eficientemente.

Si hubiese riesgo de backtracking, podríamos usar posesivo \S++ en motores que lo permitan, pero no es necesario porque la clase negada no puede match espacio.
5. Búsqueda de comentarios multilínea /* ... */

Texto con código:
text

int a; /* comentario
   multilínea */ int b; /* otro */

Patrón perezoso: /\*.*?\*/ funciona porque .*? se expande hasta encontrar */. Pero con la flag s (DOTALL) para que . incluya saltos de línea.

Sin embargo, puede haber problemas si dentro del comentario aparece un asterisco solitario. Mejor patrón: /\*[^*]*\*+(?:[^/*][^*]*\*+)*/ (patrón eficiente para comentarios C). Aquí usamos * y + greedy, pero estructurados para no saltar delimitadores.
6. Uso de posesivos para cortar backtracking en patrones anidados

Problema: Validar que una cadena consta de paréntesis balanceados con un máximo de profundidad (caso teórico).

Un patrón simple recursivo (en PCRE): \(([^()]|(?R))*\) es greedy normal y puede sufrir backtracking con cadenas largas no balanceadas. Para optimizar: \(([^()]++|(?R))*+\) usando posesivos. Esto restringe retrocesos inútiles dentro de la repetición de caracteres no paréntesis.
7. Contrastando greedy vs. lazy en reemplazo

Texto: "primero" y "segundo"

    Si queremos eliminar todo entre la primera y la última comilla usando greedy: ".*" selecciona "primero" y "segundo", lo cual puede ser deseado si queremos limpiar un gran bloque.

    Si queremos eliminar cada frase entrecomillada por separado, usamos lazy: ".*?" con reemplazo global.

Ejemplo en Python:
python

import re
texto = '"primero" y "segundo"'
re.sub(r'"[^"]*"', 'X', texto)  # clase negada: mejor que lazy, más seguro.

8. Cuantificadores y límites de palabra

Patrón para encontrar palabras de 4 letras exactas: \b\w{4}\b

    \b límite de palabra.

    \w{4} exactamente cuatro caracteres de palabra.
    No hay ambigüedad, greedy y lazy son iguales aquí porque es un número fijo.

Para palabras de al menos 4 letras: \b\w{4,}\b greedy consume toda la palabra, que es lo deseado.
9. Backtracking catastrófico y cómo solucionarlo

Ejemplo de patrón vulnerable (validación de número de serie con partes opcionales): (\d+,)*\d+
Entrada: "123,456,789" funciona bien. Entrada malformada: "123,456,789," puede causar backtracking intenso.

Solución con grupo atómico \b(?>\d+,)*\d+\b o usando cuantificadores posesivos \d++(?:,\d++)*+ (no es exactamente igual, hay que reestructurar). El grupo atómico (?>...) evita retroceso dentro del grupo, acelerando el fallo.
10. Cuantificadores con condiciones

En PCRE podemos usar condicionales con cuantificadores. Ejemplo: ^(?:(\())\d+(?(1)\))$ que coincide con (123) o 123, pero no (123. Aquí la repetición es \d+ (greedy), podríamos hacerla posesiva para evitar backtracking: \d++.

