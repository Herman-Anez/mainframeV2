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
