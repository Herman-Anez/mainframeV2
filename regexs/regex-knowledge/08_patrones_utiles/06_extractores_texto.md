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

