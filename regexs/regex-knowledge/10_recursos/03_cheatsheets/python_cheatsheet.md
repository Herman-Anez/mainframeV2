python_cheatsheet.pdf (contenido)

Incluye las mismas secciones de metacaracteres, clases, anclas, etc., pero resaltando las diferencias:

    Módulo re: Lookbehind solo fijo. Sin grupos atómicos, sin posesivos, sin recursión, sin \K, sin \p{}.

    Módulo regex: Incluye todo lo de PCRE.

Funciones principales
Función re	Propósito
re.search(pattern, text)	Busca la primera coincidencia en cualquier lugar
re.match(pattern, text)	Coincidencia al inicio de la cadena
re.fullmatch(pattern, text)	Coincidencia con toda la cadena
re.findall(pattern, text)	Lista de todas las coincidencias
re.finditer(pattern, text)	Iterador de objetos Match
re.sub(pattern, repl, text)	Sustitución
re.split(pattern, text)	Dividir cadena
re.compile(pattern, flags)	Compilar patrón
Flags
Constante	Significado
re.I / re.IGNORECASE	Ignorar mayúsculas
re.M / re.MULTILINE	^ y $ por línea
re.S / re.DOTALL	. incluye \n
re.X / re.VERBOSE	Modo verboso
re.A / re.ASCII	Solo ASCII para \w, \b, etc.
re.U / re.UNICODE	Unicode (por defecto en Python 3)
Grupos con nombre

    Sintaxis (?P<name>...)

    Retroreferencia dentro del patrón: (?P=name)

    Acceso: match.group('name')

    En substitución: \g<name>

Diferencias con PCRE

    No posesivos (en re)

    Lookbehind fijo

    Sin \K (en re)

    Sin recursión