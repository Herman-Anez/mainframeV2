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
