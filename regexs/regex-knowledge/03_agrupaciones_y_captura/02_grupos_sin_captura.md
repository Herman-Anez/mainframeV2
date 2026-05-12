# grupos_sin_captura.md
Definición

Un grupo sin captura agrupa parte de la expresión sin almacenar el texto coincidente. Su sintaxis es (?: ... ). Sirve únicamente para aplicar cuantificadores, alternancia o atomizar una parte sin generar una referencia de captura.

Ejemplo:
regex

(?:https?:\/\/)?(?:www\.)?example\.com

Los grupos no capturan protocolo ni subdominio, pero sí están agrupados para hacerlos opcionales.
Ventajas frente a los grupos de captura

    Eficiencia: Al no almacenar la subcadena, se ahorra memoria y tiempo.

    Claridad: Indica a quien lee el patrón que esa subcoincidencia no se usará después.

    Evita interferencias: Si ya tienes varios grupos de captura y necesitas uno adicional para agrupar sin cambiar la numeración existente, un grupo sin captura no añade nuevos índices.

Por ejemplo, si tienes (\d{4})-(\d{2})-(\d{2}) y decides agrupar el separador sin capturarlo, puedes escribir (\d{4})(?:-(\d{2}))? para que el guión y el segundo número sean opcionales. El grupo 1 es el año, el grupo 2 el mes (si existe), sin introducir un grupo extra para el guión.
Sintaxis y uso

    (?:patrón) : agrupa patrón.

    Se puede aplicar cuantificadores: (?:abc)+ coincide con una o más repeticiones de "abc".

    En alternancia: (?:gato|perro) igual que gato|perro, pero a veces es necesario para encapsular.

Comparación con grupos de captura

Dado el texto "rojo verde azul":

    Captura: ((?:r|v)\w+) captura palabras que empiezan con 'r' o 'v'. El primer grupo captura toda la palabra, el grupo interno es sin captura. Así grupo 1 es la palabra sin almacenar la letra inicial por separado.

    Si usáramos (r|v)(\w+) tendríamos dos capturas: letra y resto.

Grupos sin captura y modificadores de modo

En algunos motores se pueden incluir flags localizadamente con (?flags:...), que es un grupo sin captura con modificadores. Ejemplo: (?i:abc) casará "ABC", "Abc", etc., sin afectar el resto del patrón. Funciona en PCRE, Perl, .NET, Java. Python re no soporta (?i:...) (sí soporta (?i) a nivel global o en el módulo regex externo).
Ejemplo práctico: extracción de fecha con separadores flexibles
regex

(\d{4})(?:[-/.])(\d{2})(?:[-/.])(\d{2})

Coincide con 2024-12-25, 2024/12/25, 2024.12.25. Captura año (grupo 1), mes (2) y día (3). Los separadores están en grupos sin captura.
Cuándo NO usar grupos sin captura

Si posteriormente necesitas acceder a la subcadena (por ejemplo, para reemplazos con $1 o para procesado), debes mantener los paréntesis de captura. Los grupos sin captura son invisibles para las retroreferencias y las funciones de extracción.
