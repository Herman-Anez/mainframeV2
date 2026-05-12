
javascript_cheatsheet.pdf (contenido)
Creación de regex

    Literal: /patrón/flags

    Constructor: new RegExp('patrón', 'flags')

Métodos importantes
Método	Descripción
regex.exec(str)	Devuelve objeto Match (actualiza lastIndex)
regex.test(str)	Devuelve booleano
str.match(regex)	Array de coincidencias (sin grupos con g)
str.matchAll(regex)	Iterador (con grupos, necesita flag g)
str.search(regex)	Índice de primera coincidencia
str.replace(regex, sub)	Sustitución
str.split(regex)	División
Flags JS
Flag	Descripción
g	Global
i	Ignorar mayúsculas
m	Multilínea
s	Dotall (ES2018)
u	Unicode (ES2015)
y	Sticky (desde lastIndex)
d	Índices de grupos (ES2022)
Propiedades Unicode (con u)

    \p{L}, \p{Lu}, \p{Script=Greek}, \p{Emoji_Presentation}, etc.

Grupos con nombre (ES2018)

    (?<name>...) y acceso con match.groups.name

Lookbehind (ES2018)

    (?<=...) y (?<!...) con longitud variable.

Limitaciones

    Sin grupos atómicos, sin posesivos, sin recursión, sin condicionales, sin \K, sin flags inline.

Tips

    Para simular grupo atómico: (?=(...))\1.

    Usar \\ en cadenas para escapar barras invertidas, o usar String.raw.
