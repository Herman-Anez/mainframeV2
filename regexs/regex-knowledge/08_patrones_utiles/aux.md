# validacion_emails.md
La complejidad de validar un correo electrónico

Validar un email con una expresión regular que cumpla rigurosamente el RFC 5321/5322 es extremadamente complejo. La especificación permite una sintaxis muy amplia (caracteres especiales, quoted strings, comentarios anidados, etc.), que en la práctica casi ningún servicio implementa. Por ello, la mayoría de las aplicaciones utilizan patrones pragmáticos, que cubren el >99% de los casos reales y rechazan formatos absurdos.
Patrón básico (muy tolerante)

Acepta la estructura algo@algo.algo con caracteres alfanuméricos y algunos símbolos. No es estricto pero muy popular.
regex

^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

    Parte local: letras, dígitos, puntos, guiones bajos, porcentajes, más, menos.

    Dominio: letras, dígitos, puntos, guiones.

    Extensión: al menos dos letras.
    Es simple, rechaza espacios y caracteres exóticos, pero permite dominios como algo..com (doble punto) o guiones al inicio/fin, aunque en la mayoría de casos prácticos no es problemático.

Patrón mejorado, con restricciones comunes
regex

^[a-zA-Z0-9]+(?:[._%+-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z]{2,})+$

    La parte local empieza y acaba con alfanumérico, permite un separador entre bloques alfanuméricos.

    El dominio prohíbe guiones al inicio, permite segmentos separados por punto, y al menos un punto con extensión de letras.

    Evita dobles puntos y otras combinaciones inválidas.

Patrón avanzado (cercano al RFC, pero práctico)
regex

^(?=.{1,254}$)(?=.{1,64}@)[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$

    Limita la longitud total a 254 caracteres (máximo estándar) y la parte local a 64.

    Permite un conjunto ampliado de caracteres especiales en la parte local.

    Dominio: cada etiqueta (subdominio) debe tener entre 1 y 63 caracteres, sin empezar ni terminar con guión.

    Exige TLD de al menos 2 letras (no valida TLDs reales, eso se haría contra una lista externa).
    Es largo pero robusto para validación en backend.

Nota: En JavaScript este patrón puede usarse con la flag u si se esperan caracteres Unicode, pero entonces la parte local permitiría caracteres internacionales según el estándar (aunque no todos los servidores los aceptan). Una versión con soporte internacional usaría \p{L} en lugar de a-zA-Z, pero la complejidad crece.
Validación por pasos (recomendada)

Muchas veces es mejor hacer una validación básica con regex y luego comprobar existencia del dominio vía DNS o enviar un correo de confirmación. La regex solo debería garantizar que el formato es plausible.
Consideraciones por motor

    JavaScript: Para TLDs con caracteres internacionalizados (IDN), usar [\p{L}]{2,} con la flag u.

    Python: re estándar es suficiente; para IDN, usar el módulo regex.

    Java/PCRE: Similar a los patrones anteriores.

Ejemplos de testeo
javascript

const emailRegex = /^[a-zA-Z0-9]+(?:[._%+-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z]{2,})+$/;
emailRegex.test("usuario@dominio.co.uk"); // true
emailRegex.test("usuario@sub.dominio.com"); // true
emailRegex.test("usuario@dominio..com"); // false (doble punto)
emailRegex.test("usuario@-dominio.com"); // false (guion al inicio)

Límites y extensiones

Si necesitas soporte para comentarios (RFC 5322) o quoted strings, la regex se vuelve monstruosa; es mejor utilizar una biblioteca específica. Para la mayoría de aplicaciones, el patrón mejorado es suficiente y seguro.

# urls.md
¿Qué es una URL?

Una URL estándar (HTTP/HTTPS) sigue la estructura:
protocolo://[usuario:contraseña@]dominio[:puerto]/[ruta]?[query]#[fragmento]
Los patrones regex pueden capturar todos o algunos de estos componentes.
Patrón básico para extraer URLs de un texto
regex

https?://[^\s/$.?#].[^\s]*

    https?:// exige el protocolo.

    [^\s/$.?#] obliga a que el primer carácter del dominio no sea espacio ni algunos símbolos.

    [^\s]* consume todo hasta un espacio en blanco.
    Esto captura la mayoría de URLs en textos planos, pero puede incluir paréntesis o puntos finales no deseados.

Patrón más robusto que delimita con caracteres de puntuación
regex

https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?::\d+)?(?:/[^\s]*)?

    Dominio: nombre de host con letras, dígitos, guiones, puntos, y soporte para caracteres escapados con %.

    Puerto opcional :\d+.

    Ruta opcional: cualquier cosa sin espacios.
    Mejor que el básico, pero puede seguir capturando un punto final como parte de la URL.

Extracción precisa con límites por paréntesis y comillas

En entornos controlados como HTML, se puede usar un patrón que respete los delimitadores naturales:
regex

(?:"|')((?:https?|ftp)://[^"'\s]+)(?:"|')   // entre comillas
(?:href|src)=["']?((?:https?|ftp)://[^"'\s>]+) // atributos HTML

Validación de una URL completa

El siguiente patrón verifica el formato e impone que la URL no esté mal construida:
regex

^https?://([\w\-]+\.)+[\w\-]+(:\d+)?(/[\w\-./?%&=+#]*)?$

    Protocolo obligatorio.

    Dominio con al menos un punto y segmentos.

    Puerto opcional.

    Ruta opcional con caracteres válidos.
    Es útil para validar entradas de usuario donde se espera una URL absoluta.

Soporte para dominios internacionalizados (IDN)

En dominios pueden aparecer caracteres Unicode (ej. http://españa.es). Para capturarlos:
regex

https?://(?:[-\p{L}\p{N}_]|(?:%[\da-fA-F]{2}))+\.(?:\p{L}{2,})(?::\d+)?(?:/[^\s]*)?

(Requiere flag u en JavaScript, y \p{L} en PCRE/Python regex).
Fragmentos y query string

Si quieres analizar los componentes, usa grupos de captura:
regex

^(https?)://([\w\-\.]+)(?::(\d+))?(/[^?#]*)?(?:\?([^#]*))?(?:#(.*))?$

Grupos:

    protocolo

    host

    puerto

    ruta

    query string

    fragmento

Ejemplos prácticos en código

Extraer todas las URLs de un texto (JavaScript):
javascript

let urlRegex = /https?:\/\/[^\s/$.?#].[^\s]*/g;
let matches = texto.match(urlRegex);
// Limpiar puntuación final con slice si es necesario.

Validar URL en Python:
python

import re
pat = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(:\d+)?(/[-\w./?%&=+#]*)?$'
re.match(pat, url) is not None

Consideraciones y limitaciones

    Estas regex no validan que el TLD sea real (por ejemplo, .com, .es). Para una validación rigurosa, se necesita una lista de TLDs actualizada.

    Tampoco restringen caracteres ilegales en la ruta según el contexto (como espacios sin codificar). Para eso se debe escapar o usar encodeURI.

    En entornos donde se permiten fragmentos, ten cuidado con los caracteres # internos.

# fechas_y_horas.md
Formatos comunes de fecha

Las fechas varían enormemente según la región. Los patrones más comunes incluyen:

    ISO 8601: YYYY-MM-DD (recomendado para sistemas)

    Europeo: DD/MM/YYYY

    EE.UU.: MM/DD/YYYY

    Formato largo: 12 de enero de 2024
    Cada uno requiere un patrón específico.

Patrón para fecha ISO estándar
regex

^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$

    Año: cuatro dígitos.

    Mes: 01-12.

    Día: 01-31 (no valida meses con menos días; esto es un problema).
    Limitación: Acepta 2023-02-31. Para validar días por mes se necesita una lógica más compleja, que puede hacerse con alternancia o condicionales en regex avanzadas, pero generalmente es mejor validar con código.

Validación estricta de fecha (incluyendo febrero)
regex

^(?:\d{4}-(?:(?:0[13578]|1[02])-31|(?:0[1,3-9]|1[0-2])-(?:29|30)|(?:0[1-9]|1\d|2[0-8])-(?:0[1-9]|1\d|2[0-8]))|(?:(?:\d{2}(?:0[48]|[2468][048]|[13579][26])|(?:[02468][048]|[13579][26])00)-02-29)$

Este patrón valida fechas en formato YYYY-MM-DD, incluyendo bisiestos para febrero. Es bastante ilegible; se recomienda usar código en su lugar.

Alternativa híbrida: usar una regex simple para el formato y luego una función para validar rangos.
python

import re
from datetime import datetime
def validar_fecha(texto):
    if re.match(r'^\d{4}-\d{2}-\d{2}$', texto):
        try:
            datetime.strptime(texto, '%Y-%m-%d')
            return True
        except ValueError:
            pass
    return False

Fechas en formato DD/MM/YYYY o MM/DD/YYYY

    DD/MM/YYYY: ^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/\d{4}$
    (Con separadores / o - intercambiables usando grupo: [-/]).

    MM/DD/YYYY: ^(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/\d{4}$
    Ninguno distingue entre meses de 30 o 31 días.

Horas en formato 24h y 12h

    24 horas: ^(?:[01]\d|2[0-3]):[0-5]\d$ (sin segundos)
    Con segundos: ^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$

    12 horas (AM/PM): ^(?:1[0-2]|0?[1-9]):[0-5]\d(?::[0-5]\d)?\s?[APap][Mm]$

Fecha y hora combinadas (ISO 8601 completo)
regex

^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$

Ejemplo: 2023-10-05T14:30:00Z, 2024-01-01T00:00:00+01:00.

    La parte decimal de segundos es opcional.

    Zona horaria Z o offset.

Extracción de fechas en texto libre

Para encontrar fechas en formato DD de Mes de YYYY (español), se puede usar:
regex

\b(\d{1,2})\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+de\s+(\d{4})\b

Grupos capturan día, mes y año.
Consideraciones de regionalización

    En aplicaciones web, se debe saber de antemano el formato esperado; no intentar adivinar entre múltiples formatos con una sola regex.

    Los nombres de meses y días de la semana son dependientes del idioma.

    Las regex son una herramienta de pre-validación; la validación final debe usar las funciones de fecha del lenguaje.

# numeros_y_monedas.md
Números enteros y decimales básicos

    Entero (positivo y negativo): ^-?\d+$

    Decimal con punto: ^-?\d+\.\d+$

    Decimal con posible parte decimal opcional: ^-?\d+(?:\.\d+)?$

    Notación científica: ^-?\d+(?:\.\d+)?[eE][+-]?\d+$

Números con separadores de miles

Formato estándar con coma para miles y punto decimal (ej. 1,234.56):
regex

^-?\d{1,3}(?:,\d{3})*(?:\.\d{2})?$

Variante con espacio como separador de miles y coma decimal (ej. 1 234,56):
regex

^-?\d{1,3}(?:[ ]\d{3})*(?:,\d{2})?$

Combinando ambos (poco común) se puede permitir tanto coma como punto mediante un patrón más complejo.
Monedas con símbolo

    Dólar/euro con símbolo prefijo: ^\$\s?-?\d+(?:\.\d{2})?$ o ^[€$]\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?$

    Símbolo al final (ej. 100€): ^\d+(?:\.\d{2})?\s?[€$]$

    Con código de moneda: ^[A-Z]{3}\s?\d+(?:\.\d{2})?$

Extracción flexible de cantidades monetarias en texto
regex

(?:[\$\€\£]|USD|EUR)?\s?\d{1,3}(?:[,.]\d{3})*(?:\.\d{2})?(?:\s?(?:€|USD))?

Esto captura cantidades como $1,000.50, 2000 EUR, 3.500,75 € (con formato europeo, pero se confundiría con separador de miles). La ambigüedad entre millares y decimales puede resolverse con un patrón más inteligente que detecte el último punto/coma como decimal.

Patrón que supone que el último separador especial es el decimal:
regex

[-+]?\d{1,3}(?:[.,]\d{3})*[.,]\d{2}\b

Pero fallaría si no hay decimales. Para cantidades sin decimales: \b\d{1,3}(?:[.,]\d{3})+\b (sin decimales).
Porcentajes
regex

^-?\d+(?:\.\d+)?%$

O con restricción de rango 0-100: no es práctico con regex pura; mejor validar después.
Validaciones adicionales

    No permitir ceros a la izquierda (excepto el número 0 o 0.xx): ^(?:0|[1-9]\d*)(?:\.\d+)?$

    Números negativos precisos: el signo menos solo al inicio.

Optimizaciones y compatibilidad

    Todos estos patrones funcionan en cualquier motor con pequeñas adaptaciones (escapado de $, uso de \d).

    Para aplicaciones financieras, valida la cantidad con regex y después conviértela a un tipo numérico para comprobar límites.

    No uses regex para sumas o comparaciones, solo para formato.

Ejemplos prácticos

Python: extraer todos los precios en euros de un texto
python

import re
pat = r'(\d{1,3}(?:\.\d{3})*,\d{2})\s?€|\d{1,3}(?:,\d{3})*\.\d{2}\s?EUR'
precios = re.findall(pat, texto)

JavaScript: validar número de teléfono (aunque no es moneda) y monedas
javascript

const moneyRegex = /^\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?$/;
moneyRegex.test("$1,234.56"); // true

# contrasenas.md
Requisitos típicos de una contraseña segura

    Longitud mínima (generalmente 8 o más caracteres).

    Al menos una letra mayúscula.

    Al menos una letra minúscula.

    Al menos un dígito.

    Al menos un carácter especial (símbolos como !@#$%^&*).

Estos requisitos se expresan elegantemente con lookaheads al inicio del patrón.
Patrón estándar con lookaheads
regex

^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]|\p{P}|_?).{8,}$

Cada lookahead verifica la presencia de una categoría en cualquier parte de la cadena. Después, .{8,} consume toda la contraseña.

Versión explícita y legible (desglosada):
regex

^
  (?=.*[a-z])      # al menos una minúscula
  (?=.*[A-Z])      # al menos una mayúscula
  (?=.*\d)         # al menos un dígito
  (?=.*[#?!@$%^&*-]) # al menos un carácter especial de una lista concreta
  .{8,}            # longitud mínima 8
$

Nota sobre caracteres especiales: En lugar de [^\w\s], es mejor definir explícitamente el conjunto permitido para evitar caracteres no imprimibles. Por ejemplo: [!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?] o una lista acotada.
Longitud mínima y máxima
regex

^.{8,32}$

Combinado con los lookaheads para restringir composición.
Prohibir caracteres repetidos o secuencias

    No permitir 3 o más caracteres idénticos seguidos: (?!.*(.)\1{2,})

    No permitir secuencias de teclado como "qwerty": difícil con regex pura, mejor verificar con código.

Contraseñas que excluyen ciertos patrones (por ejemplo, el nombre de usuario)

Si se tiene el nombre de usuario, se puede construir la regex dinámicamente para rechazarlo. Por ejemplo, en JavaScript:
javascript

let user = "john";
let passRegex = new RegExp(`^(?!.*${user})(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).{8,}$`, 'i');

El lookahead negativo (?!.*${user}) prohíbe la aparición del nombre de usuario en cualquier parte de la contraseña.
Sin necesidad de lookaheads (motores limitados)

Si el motor no soporta lookaheads (POSIX), no se pueden hacer estas comprobaciones en una sola regex. Se usarían varias comprobaciones secuenciales:
bash

grep -E '.{8,}' fichero | grep -E '[a-z]' | grep -E '[A-Z]' | grep -E '[0-9]' | grep -E '[^a-zA-Z0-9]'

Exigir que al menos N de M condiciones se cumplan

Para requerir, por ejemplo, al menos 3 de 4 categorías, se puede usar una combinatoria de lookaheads que sumen. Por ejemplo, usando grupos y alternancia con (?=.*[a-z])(?=.*[A-Z])(?=.*\d)|(?=.*[a-z])(?=.*[A-Z])(?=.*[especial])|.... Sin embargo, es más limpio hacerlo con código.
Patrón para contraseña con todas las categorías y longitud exacta de 8 a 20
regex

^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,20}$

Compatibilidad y limitaciones

    Los lookaheads funcionan en todos los motores modernos (salvo POSIX). En JavaScript, disponibles desde siempre.

    La parte .{8,} podría permitir saltos de línea si no se especifica; normalmente en campos de contraseña no hay \n, pero es seguro usar [\s\S]{8,} o limitar a caracteres visibles.

    Los caracteres Unicode están permitidos si usamos \p{L} etc., pero muchas aplicaciones restringen a ASCII.

Buenas prácticas

    No almacenar los requisitos solo en la regex; acompañar con explicación textual al usuario.

    Permitir espacios al final/inicio no suele ser deseable; usar ^\S{8,}$ si se prohíben espacios.

    Para entornos de alta seguridad, la complejidad se mide con entropía, no con reglas fijas. La regex solo es una primera validación.

Ejemplo completo Python (usando módulo re)
python

import re
password = "MiClave123!"
patron = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$')
if patron.match(password):
    print("Contraseña válida")

# extractores_texto.md
Extracción de hashtags (#etiqueta)
regex

(?<![^\s])#[a-zA-Z0-9_áéíóúüñ]+

O con soporte Unicode (\p{L}):
regex

(?<!\S)#[\p{L}\p{N}_]+

    El lookbehind (?<!\S) o (?<=\s|^) asegura que la almohadilla esté al inicio o precedida de espacio.

    Permite letras, números y guiones bajos; ajusta según el caso.

Menciones @usuario
regex

(?<!\S)@[a-zA-Z0-9_]+

Puede refinarse para aceptar puntos o guiones según la red social.
Extracción de palabras entre comillas

Para obtener texto dentro de comillas dobles, respetando escapes básicos:
regex

"((?:[^"\\]|\\.)*)"

Para comillas simples:
regex

'((?:[^'\\]|\\.)*)'

El grupo 1 contiene el texto interior.
Extracción de URLs (visto anteriormente)

Recapitulando:
regex

https?://[^\s/$.?#].[^\s]*

Con lookbehind para evitar capturar desde mitad de palabra:
regex

(?<!\S)(https?://[^\s]+)

Direcciones de correo electrónico en texto
regex

[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

Números de teléfono (formato genérico)
regex

(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4

Captura formatos como 123-456-7890, (123) 456-7890, +1-123-456-7890.
Extracción de fechas (sencilla)
regex

\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{4}-\d{1,2}-\d{1,2}\b

Extracción de palabras clave que empiezan con mayúscula (posibles nombres propios)
regex

\b\p{Lu}\p{L}*\b

Requiere flag u en JavaScript, y \p{Lu} en PCRE/Python regex.
Patrones para logs comunes

Log de Apache (formato común)
regex

^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d+) (\d+|-)

Grupos: IP, ident, usuario, fecha, petición, código, tamaño.
Extracción de código postal de varios países

    España (5 dígitos): \b\d{5}\b

    EE.UU. (5 dígitos o 5+4): \b\d{5}(?:-\d{4})?\b

    Reino Unido (formato complejo): \b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b

Extracción de etiquetas HTML simples
regex

<\/?([a-zA-Z][a-zA-Z0-9]*)[^>]*>

Obtiene la etiqueta en el grupo 1.
Extracción de contenido entre tags específicos

Para extraer el texto dentro de <title>...</title>:
regex

<title[^>]*>(.*?)</title>

Extracción de todos los números decimales de un texto
regex

\d+\.\d+|\d+

Pero cuidado, porque capturaría fechas como 2023.10.05 como dos números. Se puede afinar con límites.
Consejos para extractores eficientes

    Siempre usar clases negadas en lugar de .*? cuando sea posible: <tag([^>]*)> en lugar de <tag.*?>.

    Utilizar lookaheads/lookbehinds para aislar sin consumir contexto.

    En procesamiento pesado, dividir el texto con split y aplicar regex simples es más rápido que una super-regex.

Ejemplo combinado: extraer enlaces, menciones y hashtags de un tweet
javascript

let tweet = "Aprendiendo #regex con @usuario visita https://regex101.com";
let patterns = {
    hashtag: /#[\w]+/g,
    mention: /@[\w]+/g,
    url: /https?:\/\/[^\s]+/g
};
console.log(tweet.match(patterns.hashtag)); // ["#regex"]
console.log(tweet.match(patterns.mention)); // ["@usuario"]
console.log(tweet.match(patterns.url));     // ["https://regex101.com"]

