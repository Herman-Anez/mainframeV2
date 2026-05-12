# herramientas_online.md
¿Por qué usar herramientas online?

Las herramientas web para expresiones regulares permiten escribir, probar, depurar y compartir patrones de manera interactiva. Son imprescindibles tanto para principiantes como para expertos, ya que visualizan paso a paso el funcionamiento del motor, muestran coincidencias, grupos capturados y advierten sobre posibles problemas de rendimiento.
Las mejores herramientas online
1. Regex101 (regex101.com)

    Descripción: La navaja suiza de las regex. Soporta múltiples sabores (PCRE2, PCRE, JavaScript, Python, Golang, Java, .NET, Rust).

    Características:

        Explicación automática de cada token del patrón.

        Panel de coincidencias con resaltado de grupos.

        Debugger: muestra paso a paso las operaciones del motor (ideal para entender greedy/lazy y backtracking).

        Análisis de rendimiento: número de pasos, advertencia de backtracking catastrófico.

        Posibilidad de generar código para diferentes lenguajes.

        Posibilidad de guardar y compartir patrones mediante URL.

        Opción de añadir casos de prueba unitarios.

    Uso recomendado: Prototipado de patrones complejos, aprendizaje interactivo, validación de contraseñas/emails, depuración de fallos.

2. Regexr (regexr.com)

    Descripción: Herramienta visual con enfoque educativo. Basada en el motor de JavaScript.

    Características:

        Interfaz limpia con cheat sheet integrada.

        Resalta todas las coincidencias mientras escribes.

        Panel de referencia con tokens, clases y ejemplos.

        Posibilidad de votar y compartir patrones en la comunidad.

        Incluye editor de texto de muestra y banderas configurables.

    Uso recomendado: Aprender regex desde cero, probar rápidamente patrones en JavaScript, explorar ejemplos comunitarios.

3. Debuggex (debuggex.com)

    Descripción: Visualización gráfica mediante diagramas de ferrocarril (railroad diagrams). Soporta JavaScript, PCRE y Python.

    Características:

        Representación visual del flujo de la expresión regular.

        Resalta el camino seguido en el diagrama al probar una cadena.

        No tan detallado en la sintaxis como Regex101, pero excelente para entender la estructura.

    Uso recomendado: Comprender visualmente patrones anidados, enseñar regex en presentaciones.

4. Pythex (pythex.org)

    Descripción: Probador de regex específico para Python (módulo re). Interfaz minimalista.

    Características:

        Indica si el patrón es válido en Python.

        Muestra coincidencias y grupos.

        Permite elegir banderas (IGNORECASE, MULTILINE, etc.).

    Uso recomendado: Verificar compatibilidad con Python, probar escapes y raw strings.

5. RegExLib (regexlib.com)

    Descripción: Repositorio de patrones enviados por usuarios, con votaciones y comentarios.

    Características:

        Buscador de patrones por categoría (email, teléfono, código postal…).

        Permite probar los patrones directamente.

    Uso recomendado: Encontrar inspiración o soluciones predefinidas (pero siempre revisar la calidad).

6. ExtendsClass Regex Tester (extendsclass.com/regex-tester.html)

    Descripción: Herramienta en línea para múltiples motores (Python, JavaScript, PHP, Java, etc.), con capacidad de generar código.

    Uso recomendado: Alternativa a Regex101 cuando se necesita generar rápidamente código de reemplazo.

7. Scriptular (scriptular.com)

    Descripción: Probador orientado a JavaScript con una interfaz sencilla y referencias rápidas.

    Uso recomendado: Pruebas rápidas para frontend.

8. iHateRegex (ihateregex.io)

    Descripción: Buscador visual de regex con un enfoque amigable. Presenta patrones comunes con diagramas y explicaciones.

    Uso recomendado: Encontrar patrones para casos de uso típicos sin tener que escribirlos desde cero.

9. Regulex (jex.im/regulex)

    Descripción: Generador de diagramas de ferrocarril similar a Debuggex, pero con más opciones de personalización y exportación.

    Uso recomendado: Crear imágenes de patrones para documentación.

Aplicaciones de escritorio

    RegexBuddy (comercial, Windows): Potente entorno con depuración, generación de código para múltiples lenguajes, y traducción entre sabores. La opción profesional por excelencia.

    Kodos (Python, obsoleto pero funcional): Herramienta gráfica para testear regex en Python.

    Expressions (macOS): Aplicación minimalista para Mac.

Consejos de uso

    Siempre prueba el patrón en el mismo motor que usarás en producción.

    Aprovecha los tests unitarios de Regex101 para verificar casos límite.

    Si usas JavaScript, recuerda que el soporte de lookbehind y Unicode depende de la versión; compruébalo en el navegador o con Node.js.

    No confíes ciegamente en patrones de repositorios públicos sin entenderlos; adapta y valida.

# libros_y_guias.md
Libros imprescindibles
Mastering Regular Expressions (Jeffrey E. F. Friedl)

    Edición: 3ª edición (2006). Sigue siendo la referencia definitiva.

    Contenido: Cubre a fondo el funcionamiento de los motores NFA/DFA, dialéctos (Perl, Java, .NET, PHP, etc.), técnicas de optimización, y ejemplos prácticos.

    Por qué leerlo: Proporciona una comprensión mental del backtracking y cómo escribir patrones eficientes. Es el "libro de cabecera" para cualquiera que use regex de forma intensiva.

Regular Expressions Cookbook (Jan Goyvaerts & Steven Levithan)

    Edición: 2ª edición (2012).

    Contenido: Recetario con cientos de soluciones para problemas comunes en 8 lenguajes (Perl, PCRE, Python, JavaScript, Java, .NET, Ruby, etc.). Cada receta explica el patrón y las diferencias entre sabores.

    Por qué leerlo: Ideal para consultar rápidamente cómo validar un email, extraer datos o manipular cadenas en el lenguaje deseado.

Introducing Regular Expressions (Michael Fitzgerald)

    Edición: 2012.

    Contenido: Introducción amigable para principiantes. Cubre lo esencial con ejemplos claros.

    Por qué leerlo: Buen comienzo si nunca has usado regex; más práctico que académico.

Guías y tutoriales online gratuitos

    MDN Web Docs – Regular Expressions (developer.mozilla.org/es/docs/Web/JavaScript/Guide/Regular_expressions): Guía oficial de JavaScript. Muy completa y actualizada con ES2022+.

    RegexOne (regexone.com): Lecciones interactivas paso a paso. Empieza desde cero y añade complejidad gradualmente. Ideal para principiantes.

    RegexLearn (regexlearn.com): Plataforma interactiva con ejercicios, desde lo básico hasta avanzado. Similar a RegexOne pero con una interfaz moderna.

    RegExr Cheatsheet (regexr.com): Dentro de la propia herramienta, la pestaña "Cheatsheet" es una guía de referencia rápida muy útil.

    Python docs – re module (docs.python.org/3/library/re.html): Documentación oficial del módulo re. Incluye ejemplos y limitaciones. Para regex, consulta su documentación en PyPI.

    PHP.net – PCRE (php.net/manual/es/book.pcre.php): Documentación de las funciones preg y patrones soportados.

    Java Tutorials – Regular Expressions (docs.oracle.com/javase/tutorial/essential/regex/): Guía oficial de Oracle.

Cursos y vídeos

    "Regular Expressions for Dummies" (YouTube): Muchos canales de programación dedican listas de reproducción. Busca Derek Banas, The Coding Train, FreeCodeCamp.

    "Mastering Regular Expressions in JavaScript" (Udemy / Pluralsight): Varios cursos pagos, pero con profundidad en el motor JS.

    "Regular Expressions in Python" (Real Python, realpython.com): Tutorial excelente con ejemplos prácticos.

Comunidades y foros

    Stack Overflow (etiqueta [regex]): Miles de preguntas y respuestas. Ideal para ver soluciones a problemas específicos. Aprovecha también la etiqueta del lenguaje correspondiente.

    Reddit (r/regex): Comunidad activa donde se comparten patrones y se discuten técnicas.

    Regex101 Community: Dentro de la herramienta, se pueden buscar patrones públicos y ver cómo otros resolvieron problemas.

# cheatsheets/

A continuación se detalla el contenido textual que deberían incluir las hojas de trucos (en formato Markdown, que luego puedes exportar a PDF). Las secciones se presentan en tablas y listas para una consulta rápida.


pcre_cheatsheet.pdf (contenido)
Metacaracteres básicos
Símbolo	Significado
.	Cualquier carácter excepto nueva línea (con s incluye \n)
^	Inicio de cadena/línea (con m)
$	Fin de cadena/línea (con m)
*	0 o más
+	1 o más
?	0 o 1 / perezoso
{n}	Exactamente n
{n,}	n o más
{n,m}	Entre n y m
*+, ++, etc.	Posesivos
( ... )	Grupo de captura
(?: ... )	Grupo sin captura
(?<name>...)	Grupo con nombre
(?> ... )	Grupo atómico
|	Alternancia
\	Escape
Clases de caracteres
Símbolo	Equivalente
\d	Dígito [0-9] (con u Unicode)
\D	No dígito
\w	Carácter de palabra [a-zA-Z0-9_] (Unicode con u)
\W	No palabra
\s	Espacio blanco
\S	No espacio
\h	Espacio horizontal
\v	Espacio vertical
\R	Salto de línea universal
Anclas y límites
Símbolo	Significado
\b	Límite de palabra
\B	No límite
\A	Inicio absoluto
\z	Final absoluto
\Z	Final o antes de \n al final
Lookahead / Lookbehind
Constructo	Significado
(?=...)	Lookahead positivo
(?!...)	Lookahead negativo
(?<=...)	Lookbehind positivo (fijo o variable en PCRE2)
(?<!...)	Lookbehind negativo
Flags comunes
Flag	Descripción
i	Ignora mayúsculas
m	Multilínea
s	Dotall (. incluye \n)
x	Modo verboso
u	Unicode
U	Ungreedy (invertir codicia)
Avanzado PCRE
Constructo	Descripción
(?R), (?0)	Recursión (patrón completo)
(?1), (?2)	Recursión a grupo específico
(?&name)	Subrutina a grupo con nombre
\k<name>	Retroreferencia a grupo con nombre
\g{n}	Retroreferencia con número grande
(?(cond)si|no)	Condicional
\K	Descartar lo coincidido a la izquierda
(*SKIP)(*FAIL)	Saltar y fallar (control de backtrack)
(*COMMIT)	Confirmar avance sin retroceso
\p{L}, \p{Script=Latin}	Propiedades Unicode
Secuencias de escape
Secuencia	Significado
\n	Nueva línea
\r	Retorno de carro
\t	Tabulador
\x{2020}	Carácter Unicode (hex)
\Q...\E	Literal entre medias


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

# enlaces_utiles.md
Herramientas y aprendizaje interactivo

    Regex101 – Probador multilenguaje con debugger.

    Regexr – Aprendizaje visual con referencias.

    Debuggex – Diagramas de ferrocarril.

    Regulex – Diagramas personalizables.

    RegexOne – Lecciones interactivas.

    RegexLearn – Plataforma de ejercicios.

    Pythex – Probador Python.

    iHateRegex – Patrones comunes con explicaciones.

    ExtendsClass Regex Tester – Multimotor.

Documentación oficial por lenguaje

    Python re: docs.python.org/3/library/re.html

    Python regex: pypi.org/project/regex/

    JavaScript (MDN): developer.mozilla.org/es/docs/Web/JavaScript/Guide/Regular_expressions

    PHP (PCRE): php.net/manual/es/book.pcre.php

    Java: docs.oracle.com/javase/tutorial/essential/regex/

    .NET: docs.microsoft.com/en-us/dotnet/standard/base-types/regular-expressions

Bibliotecas y motores alternativos

    RE2 (C++, Python, Go, Node): Motor de tiempo lineal sin backtracking. github.com/google/re2

    Hyperscan (Intel): Motor de alto rendimiento para múltiples patrones simultáneos.

    Node.js re2: Binding de RE2 para JavaScript.

    XRegExp (JavaScript): Extensión que añade soporte para grupos atómicos, posesivos, comentarios, etc. xregexp.com

Comunidades y foros

    Stack Overflow (regex): stackoverflow.com/questions/tagged/regex

    Reddit r/regex: reddit.com/r/regex

    Regex101 Community Patterns: Sección de patrones públicos dentro de la herramienta.

Cheatsheets imprimibles

    QuickRef.me – Regex

    RexEgg – Sitio con referencias exhaustivas y trucos avanzados.

    Cheatography – Regex Cheat Sheet

Videos y cursos

    "Learn Regular Expressions In 20 Minutes" (Web Dev Simplified, YouTube).

    "Regular Expressions (Regex) Tutorial" (Simplilearn, YouTube).

    "Regular Expressions in Python" (Real Python, YouTube).

    Curso de FreeCodeCamp "Regular Expressions" (YouTube, 1 hora).

Libros (Amazon / editoriales)

    Mastering Regular Expressions – Jeffrey Friedl (O'Reilly).

    Regular Expressions Cookbook – Jan Goyvaerts & Steven Levithan (O'Reilly).

    Introducing Regular Expressions – Michael Fitzgerald (O'Reilly).

Herramientas de generación de código

    Regex101 Code Generator: Dentro de la herramienta, genera snippet en JavaScript, Python, PHP, etc.

    RegexBuddy: Exporta a muchos lenguajes.

Artículos y blogs destacados

    RexEgg (rexegg.com): La web más completa sobre regex, con tutoriales avanzados (recursión, balanceo, retroreferencias).

    "Regex tutorial — A quick cheatsheet by examples" (Factory Mind, medium.com).

    "Regular Expressions: Now You Have Two Problems" (blog.codinghorror.com): Reflexión clásica de Jeff Atwood sobre cuándo usar (y no usar) regex.

    "Catastrophic backtracking" (regular-expressions.info): Explicación con ejemplos y soluciones.

Aplicaciones y extensiones

    VS Code – Soporte nativo para regex en búsqueda/reemplazo.

    Notepad++ – Regex en buscar y reemplazar.

    grep, sed, awk – Herramientas de línea de comandos (POSIX).

    Sublime Text – Búsqueda con regex.

    Browser DevTools – La consola permite ejecutar regex en JS.

