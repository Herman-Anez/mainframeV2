
# basicos.md
Instrucciones

Escribe una expresión regular para cada uno de los siguientes problemas. Si el motor lo requiere, especifica las banderas. Prueba tus patrones en un probador online (regex101.com, pythex.org) con los casos de ejemplo.

1. Buscar la palabra "gato"
Encuentra todas las apariciones de la palabra "gato" en una frase, sin distinguir mayúsculas/minúsculas. Debe coincidir como palabra completa.
text

Test: "El gato y el GATO gatean"
Coincidencias esperadas: "gato", "GATO"

2. Validar un código de área de EE.UU.
Formato: tres dígitos entre paréntesis (seguidos de espacio y tres dígitos adicionales, pero solo valida el código de área). Por ejemplo, "(123) " debe coincidir.
text

Test: "(123) 456-7890"  -> match "(123) "
Test: "(12) 345"        -> no match

3. Encontrar todas las palabras que terminan en "ción"
Coincide con palabras completas que tengan la terminación "ción" (ej. "canción", "acción"). Ignora mayúsculas/minúsculas.
text

Test: "La canción y la ACCIÓN fueron bien."
Coincidencias: "canción", "ACCIÓN"

4. Validar una fecha en formato DD/MM/AAAA
Día de 01 a 31, mes de 01 a 12, año de 4 dígitos. No hace falta validar días por mes (p.ej. 31/02/2023 es válido para este ejercicio).
text

Test: "15/08/2024" -> match
Test: "5/8/2024"   -> no match (exige dos dígitos)

5. Encontrar todas las vocales
Extrae todas las vocales (tanto mayúsculas como minúsculas) de un texto.
text

Test: "Hola Mundo" -> ["o", "a", "u", "o"]

6. Reemplazar múltiples espacios por uno solo
Escribe un patrón que capture cualquier secuencia de uno o más espacios en blanco (espacio, tabulador, salto de línea) para luego reemplazarlas por un solo espacio.
text

Test: "Hola    mundo.\t\tAdiós"
Después del reemplazo: "Hola mundo. Adiós"

7. Validar un nombre de usuario alfanumérico
Debe tener entre 4 y 16 caracteres, compuestos únicamente por letras (mayúsculas y minúsculas) y dígitos. No puede contener espacios ni símbolos.
text

Test: "usuario123" -> válido
Test: "user name"  -> inválido

8. Extraer extensiones de archivo
De una lista de nombres de archivo, extrae la extensión (sin el punto). Solo debe capturar extensiones de letras (no números al final). Por ejemplo: "imagen.jpg", "documento.pdf", "script.js".
text

Test: "foto.png"     -> extensión "png"
Test: "archivo.tar.gz" -> extensión "gz" (la última)

9. Buscar líneas que comienzan con "Error"
Procesa un texto multilínea y selecciona todas las líneas que empiezan por la palabra "Error" (sin importar mayúsculas/minúsculas). La palabra debe estar al inicio de la línea.
text

Test:
Todo bien
Error: fallo crítico
WARNING: revisar
error menor
Se espera coincidencia en la segunda línea: "Error: fallo crítico"

10. Validar un número decimal simple
Formato: puede tener un signo negativo opcional, dígitos enteros obligatorios, y opcionalmente un punto seguido de uno o más dígitos decimales. Ej: "-3.14", "10", "0.5". No permite múltiples puntos ni caracteres extra.
text

Test: "42"        -> válido
Test: "-.5"       -> inválido (falta entero)
Test: "1.2.3"     -> inválido

# intermedios.md
Instrucciones

Estos ejercicios profundizan en cuantificadores perezosos, grupos de captura, lookahead/lookbehind, y patrones prácticos. Proporciona la regex y una breve explicación de su funcionamiento.

1. Extraer el texto dentro de etiquetas HTML <strong>
Dado un fragmento HTML, captura el contenido que está entre <strong> y </strong>, incluyendo posibles espacios y otras etiquetas internas, pero usando cuantificador perezoso para obtener cada bloque por separado.
text

Test: "<strong>Nota:</strong> esto es <strong>importante</strong>"
Coincidencia 1: "Nota:"  Coincidencia 2: "importante"

2. Validar un email con el patrón mejorado
Escribe una regex que valide un correo electrónico con las siguientes reglas:

    Parte local: caracteres alfanuméricos, puntos, guiones bajos, guiones, porcentajes y signos más. No puede empezar ni terminar con punto ni tener dos puntos consecutivos.

    Dominio: letras, dígitos, guiones; separado por puntos; el TLD debe tener al menos dos letras.

(Usa el patrón mejorado visto en los apuntes, no el básico.)
text

Test: "usuario@dominio.com"       -> válido
Test: "usuario@sub.dom.co.uk"    -> válido
Test: "usuario@dominio..com"     -> inválido
Test: ".usuario@dominio.com"     -> inválido

3. Buscar palabras que no están precedidas por el signo @
Encuentra palabras completas (secuencias de letras) que no formen parte de una mención (@usuario). Es decir, la palabra no debe estar inmediatamente después de un @.
text

Test: "@user hola mundo"
Debe coincidir "hola", "mundo", pero NO "user".

4. Extraer el nombre de un archivo sin extensión
Dado un nombre de archivo (ej. "documento.pdf"), captura solo el nombre sin la extensión. El archivo puede tener múltiples puntos (ej. "archivo.backup.tar.gz"); en ese caso extrae el nombre completo hasta el último punto.
text

Test: "foto.png"           -> "foto"
Test: "archivo.backup.gz"  -> "archivo.backup"

5. Validar una contraseña segura con lookaheads
Construye una regex que exija:

    Al menos 8 caracteres de longitud.

    Al menos una letra mayúscula.

    Al menos una letra minúscula.

    Al menos un dígito.

    Al menos un carácter especial de la lista !@#$%^&*.

text

Test: "Clave123!"  -> válido
Test: "clave123!"  -> inválido (sin mayúscula)
Test: "CLAVE123!"  -> inválido (sin minúscula)

6. Capturar los tres primeros grupos de un número de teléfono internacional
Formato: +XX (XXX) XXX-XXXX o +XX.XXX.XXX-XXXX. Los separadores pueden ser espacio, punto o guión. Captura por separado: código de país, código de área y número local (todo junto sin separadores, solo dígitos).
text

Test: "+1 (123) 456-7890"
Grupo 1: "1", Grupo 2: "123", Grupo 3: "4567890"
Test: "+34.666.777.888"
Grupo 1: "34", Grupo 2: "666", Grupo 3: "777888"

7. Reemplazar fechas de formato MM/DD/AAAA a DD/MM/AAAA
Usa una regex con grupos de captura para intercambiar el mes y el día en fechas del tipo 12/25/2024 a 25/12/2024. Escribe el patrón y la cadena de sustitución.
text

Entrada: "12/25/2024"
Salida: "25/12/2024"

8. Seleccionar líneas que contienen una palabra repetida dos veces consecutivas
En un texto multilínea, encuentra líneas donde una palabra (secuencia de letras) se repite exactamente, separada por un espacio: "hola hola". La coincidencia debe capturar la palabra repetida.
text

Test:
hola hola mundo
adiós adiós
bien bien bien
En la primera línea captura "hola", segunda "adiós", tercera no.

9. Validar una cadena que no contenga la palabra "prohibido"
Escribe un patrón que solo case si la cadena completa falla en contener la palabra "prohibido" en cualquier parte.
text

Test: "Este texto está bien"           -> match
Test: "Este texto está prohibido aquí" -> no match

10. Extraer hashtags de un tweet, ignorando signos de puntuación pegados
Encuentra todos los hashtags del estilo #regex o #OpenSource. Un hashtag comienza con # y continúa con caracteres de palabra (letras, números, guiones bajos). No debe incluir caracteres de puntuación como , o . si están pegados al final.
text

Test: "Aprendiendo #regex, #OpenSource y #python3."
Coincidencias: "#regex", "#OpenSource", "#python3"

# avanzados.md
Instrucciones

Estos problemas requieren dominio de temas como recursión, grupos atómicos, posesivos, propiedades Unicode, backtracking catastrófico y optimización. Las regex deben ser eficientes y correctas.

1. Validar paréntesis balanceados con recursión
Escribe una regex que verifique si una cadena contiene una expresión con paréntesis correctamente balanceados (puede haber texto dentro y fuera). Por ejemplo: "a(b(c)d)e" es válido, "a(b(c)d" no lo es. La recursión debe aplicarse sobre el patrón completo. (Usa PCRE, PHP, Perl o Python regex)
text

Test: "(a(b)c)"   -> válido
Test: "((a)"      -> inválido
Test: "())"       -> inválido

2. Prevenir backtracking catastrófico en (a+)+b
Transforma el patrón (a+)+b en una versión que no sufra backtracking exponencial cuando se enfrenta a una cadena larga de as sin b al final. Usa cuantificadores posesivos o grupos atómicos.
text

Entrada de prueba: "aaaaaaaaaaaaaaaaaaaaX"
Explica por qué la versión original fallaría estrepitosamente y cómo la nueva lo evita.

3. Tokenizar un texto en palabras según propiedades Unicode
Exclusivamente con propiedades Unicode, extrae todas las palabras de un texto multilingüe. Una palabra se define como una secuencia de caracteres de categoría Letra (\p{L}). Debe ignorar números y puntuación.
text

Test: "Hola, ¿cómo estás? 123 números и русский текст"
Resultado esperado: ["Hola", "cómo", "estás", "русский", "текст"]

4. Reemplazar comillas tipográficas conservando el contenido
Dado un texto con comillas latinas («...») y comillas inglesas (“...”), escribe un patrón que capture el texto interior y permita reemplazar ambos estilos por comillas dobles estándar, preservando el contenido. Utiliza grupos con nombre o retroreferencias para manejar el cierre correcto.
text

Entrada: «Hola» y “mundo”
Salida (tras reemplazo): "Hola" y "mundo"

5. Validar un número de tarjeta de crédito (Visa, MasterCard, American Express) con una sola regex
Utiliza lookaheads para distinguir los formatos de inicio:

    Visa: empieza con 4, longitud 16.

    MasterCard: empieza con 51-55 o 2221-2720, longitud 16.

    American Express: empieza con 34 o 37, longitud 15.
    No es necesario aplicar el algoritmo de Luhn.

text

Test: "4111111111111111" -> Visa
Test: "5105105105105100" -> MasterCard
Test: "371449635398431" -> American Express
Test: "1234567812345670" -> no válido

6. Modo verboso: reescribe un patrón complejo con comentarios
Toma el siguiente patrón para validar un código postal español (5 dígitos) y una extensión opcional de 4 dígitos tras guión, con espacios opcionales: ^\d{5}\s*-?\s*(\d{4})?$. Reescríbelo en modo verboso (con flag x o comentarios) explicando cada parte.

7. Extraer todas las claves JSON de primer nivel
Dada una cadena JSON simple (sin anidamiento de objetos), extrae las claves de las propiedades de primer nivel. Por ejemplo: {"nombre":"Juan","edad":30,"ciudad":"Madrid"} debería capturar nombre, edad, ciudad. Asume un formato sin espacios alrededor de comillas y dos puntos.
text

Test: '{"nombre":"Juan","edad":30,"ciudad":"Madrid"}'
Capturas: "nombre", "edad", "ciudad"

8. Encontrar todas las palabras que contienen al menos dos vocales consecutivas
Usando clases de caracteres y cuantificadores, identifica palabras completas que tengan dos o más vocales seguidas (mayúsculas/minúsculas, considerando también vocales acentuadas: áéíóúü). No importa el resto de la palabra.
text

Test: "El caos y la poesía en el cielo"
Debe coincidir: "caos", "poesía", "cielo"

9. Simular un grupo atómico en JavaScript
JavaScript no soporta grupos atómicos. Escribe un patrón equivalente para (?>a+)b utilizando lookahead y retroreferencia. Demuestra que funciona con la entrada "aaab" y que no funciona con "aaaa".
text

Explicación: usa (?=(a+))\1b

10. Optimizar una regex para logs de Apache
Dado un patrón típico para analizar una línea de log de Apache: ^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d{3}) (\d+|-), sugiere mejoras de rendimiento utilizando cuantificadores posesivos o grupos atómicos donde sea posible, y explica por qué podrían reducir el backtracking en caso de líneas mal formadas.
soluciones/01_basicos_sol.md
Soluciones – Ejercicios Básicos

1. Buscar la palabra "gato"
Regex: /\bgato\b/gi

    \b límite de palabra, gato literal, bandera i para insensibilidad y g global.

2. Código de área
Regex: /\(\d{3}\) /

    \( \d{3} \) coincide con paréntesis y tres dígitos, seguido de espacio literal.

3. Palabras terminadas en "ción"
Regex: /\w+ción\b/gi (si \w soporta acentos y ñ con Unicode) o /[a-zA-Záéíóúüñ]+ción\b/gi.

    \w+ una o más letras/dígitos/guion bajo, luego "ción", límite de palabra.

4. Fecha DD/MM/AAAA
Regex: /^(0[1-9]|[12]\d|3[01])\/(0[1-9]|1[0-2])\/\d{4}$/

    Día: 01-31, mes: 01-12, año: 4 dígitos. Los separadores son barras.

5. Vocales
Regex: /[aeiou]/gi

    Clase con las cinco vocales. g global, i case-insensitive.

6. Múltiples espacios
Patrón de búsqueda: /\s+/g
Cadena de reemplazo: un espacio .

    \s+ uno o más caracteres de espacio.

7. Nombre de usuario
Regex: /^[a-zA-Z0-9]{4,16}$/

    Clase alfanumérica, cuantificador de 4 a 16. ^ y $ para toda la cadena.

8. Extensión de archivo
Regex: /\.([a-zA-Z]+)$/

    Busca un punto literal seguido de una o más letras hasta el final de la cadena. El grupo 1 contiene la extensión.

9. Líneas que empiezan con "Error"
Regex: /^Error\b.*/gim

    ^ inicio de línea (con flag m), Error literal, \b límite de palabra, luego cualquier cosa. Flags: g global, i ignore case, m multilínea.

10. Número decimal simple
Regex: /^-?\d+(\.\d+)?$/

    -? signo opcional. \d+ entero obligatorio. (\.\d+)? parte decimal opcional con punto y al menos un dígito.

soluciones/02_intermedios_sol.md
Soluciones – Ejercicios Intermedios

1. Texto en <strong>
Regex: /<strong>(.*?)<\/strong>/gi

    .*? perezoso captura contenido en el grupo 1. Flags global e ignore case.

2. Validar email (mejorado)
Regex:
text

/^[a-zA-Z0-9]+(?:[._%+-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z]{2,})+$/

Explicación: La parte local empieza con alfanumérico, luego permite separadores únicos entre bloques alfanuméricos. El dominio valida segmentos sin guiones al inicio/fin, y TLD de al menos 2 letras.

3. Palabras no precedidas por @
Regex: /(?<!@)\b[a-zA-Z]+\b/g

    Lookbehind negativo (?<!@) asegura que no haya @ justo antes. \b...\b palabra de letras.

4. Nombre de archivo sin extensión
Regex: /^(.+)\.([^.]+)$/ (aplicado con match y grupo 1).
O usando lookahead: /.+(?=\.)/.

    Captura todo hasta el último punto. Grupo 1 contiene el nombre.

5. Contraseña segura
Regex: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/

    Cuatro lookaheads que verifican presencia de cada categoría. .{8,} consume la cadena.

6. Teléfono internacional
Regex: /^\+(\d+)[ .-]\(?(\d+)\)?[ .-]?(\d+)[ .-](\d+)$/ (se ajusta la agrupación para capturar tres partes).
Una versión más flexible: /^\+(\d{1,3})[ .-]\(?(\d{1,4})\)?[ .-](\d{1,14})$/ y luego reorganizar dígitos. Pero según el requerimiento específico:
Para +1 (123) 456-7890:
\+\s?(\d+)\s?\(?(\d+)\)?[\s.-]?(\d+)[\s.-]?(\d+) y unir grupos 3 y 4 en código. Mejor con nombre de grupo:
Patrón: \+\s?(?<pais>\d+)\s?\(?(?<area>\d+)\)?[\s.-]?(?<local>\d+)[\s.-]?(?<resto>\d+). Pero el enunciado pide grupo 1,2,3. Optamos por:
text

/^\+(\d+)\D*\(?(\d+)\)?\D*(\d+)\D*(\d+)$/

Luego concatenar grupo 3 y 4 para el número local.

7. Intercambiar fecha MM/DD/AAAA
Patrón: /(\d{2})\/(\d{2})\/(\d{4})/
Cadena de reemplazo: $2/$1/$3

    Grupo 1: mes, Grupo 2: día, Grupo 3: año. Se invierten 1 y 2.

8. Palabra repetida consecutiva
Regex: /\b(\w+)\s+\1\b/g

    (\w+) captura palabra. \s+ espacios. \1 exige la misma palabra. \b límites aseguran palabra completa.

9. Cadena sin "prohibido"
Regex: /^(?!.*prohibido).*$/ (o con flags i si no importa mayúsculas).

    El lookahead negativo (?!.*prohibido) falla si en cualquier lugar aparece "prohibido".

10. Hashtags limpios
Regex: /#\w+\b/g

    #\w+ hashtag. El \b al final impide que caracteres extra como , se incluyan (porque , no es parte de \w). En algunos contextos puede necesitar (?<=^|\s)#\w+ para evitar falsos hashtags en URLs.

soluciones/03_avanzados_sol.md
Soluciones – Ejercicios Avanzados

1. Paréntesis balanceados con recursión
Regex (PCRE/Python regex): /^[^()]*\((?>[^()]+|(?R))*\)[^()]*$/
O para toda la cadena:
text

/^(?:[^()]* \((?: (?: [^()]++ | (?R) )* )\) [^()]* )+$/x

Explicación: Desde el inicio, permite texto sin paréntesis, luego \(, dentro un grupo atómico que repite caracteres no paréntesis o recursión, y cierra \). [^()]++ es posesivo para eficiencia.

2. Prevenir backtracking catastrófico
Regex original: (a+)+b
Regex optimizada: (a++)+b o (?>a+)+b o simplemente a+b (si no es necesario el anidamiento).
Con a++ el cuantificador no cede caracteres, eliminando el retroceso exponencial. Al aplicarlo sobre "aaaa...X" falla inmediatamente porque tras consumir todas las as no hay b y no intenta redistribuir.

3. Tokenizar con propiedades Unicode
Regex: /\p{L}+/gu en JavaScript, o en Python regex: \p{L}+.

    \p{L} cualquier letra Unicode. Flag u y g dan todas las secuencias de letras.

4. Comillas tipográficas a comillas rectas
Buscar: «(.*?)» y también “.*?”.
Patrón unificado con alternancia y retroreferencia para asegurar mismo tipo:
text

/«([^«»]+)»|“([^“”]+)”/

Reemplazo: "$1$2".
Se puede usar un solo grupo con nombre y condicional (en motores que lo permitan), pero con alternancia simple y dos grupos es fácil: la coincidencia tendrá grupo 1 o grupo 2. En sustitución "$1$2" (uno estará vacío).

5. Tarjeta de crédito
Regex (con espacios opcionales):
text

/^(?:4\d{15}|(?:5[1-5]\d{14}|222[1-9]\d{12}|22[3-9]\d{13}|2[3-6]\d{14}|27[0-1]\d{12}|2720\d{12})|3[47]\d{13})$/

Se simplifica con lookahead para el tipo y luego longitud:
text

/^(?:(?=4)\d{16}|(?=5[1-5]|222[1-9]|22[3-9]|2[3-6]|27[0-1]|2720)\d{16}|(?=3[47])\d{15})$/

Ajuste para MasterCard: comienzo 51-55 o 2221-2720.

6. Modo verboso
regex

(?x)          # modo verboso
^             # inicio
\d{5}         # cinco dígitos básicos
\s*           # espacios opcionales
-?            # guion opcional
\s*           # espacios opcionales
(\d{4})?      # extensión opcional de 4 dígitos (grupo 1)
$             # fin

En Python:
python

pattern = re.compile(r"""
    ^
    \d{5}      # código postal base
    \s* -? \s* # separador flexible
    (\d{4})?   # extensión opcional
    $
""", re.VERBOSE)

7. Claves JSON de primer nivel
Regex: /"([^"]+)":/g

    Busca comilla, captura uno o más caracteres no comilla, luego comilla y dos puntos. Grupo 1 contiene la clave.

8. Palabras con al menos dos vocales consecutivas
Regex (con vocales acentuadas): /\b\w*[aeiouáéíóúü]{2}\w*\b/gi

    \b\w* inicio de palabra, luego dos vocales seguidas, luego resto de palabra.

9. Simular grupo atómico en JavaScript
Para (?>a+)b:
javascript

let regex = /(?=(a+))\1b/;

Prueba:

    "aaab" → regex.exec("aaab") devuelve match (grupo 1: "aaa").

    "aaaa" → no hay match.

10. Optimizar Apache log regex
Patrón original: ^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d{3}) (\d+|-)
Mejoras:

    Usar [^][]* en lugar de [^\]]+ (es igual pero más directo).

    Cambiar \S+ a \S++ o envolver en grupos atómicos para evitar backtracking en logs malformados donde campos no coincidan.

    Para la petición ([^"]*) podría ser ([^"]*+) posesivo, porque una vez capturada la cadena entre comillas no se querrá ceder caracteres.

    La regex completa con posesivos:

text

^(\S++) (\S++) (\S++) \[([^][]*+)\] "([^"]*+)" (\d{3}) (\d++|-)

Explicación: cada ++ y *+ evita que, en caso de fallo más adelante, el motor intente reducir la captura y redistribuir, evitando backtracking innecesario en líneas incompletas.
