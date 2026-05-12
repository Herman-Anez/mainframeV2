# Herramientas Online para Expresiones Regulares

Las herramientas web para expresiones regulares permiten escribir, probar, depurar y compartir patrones de manera interactiva. Son imprescindibles tanto para principiantes como para expertos, ya que visualizan paso a paso el funcionamiento del motor, muestran coincidencias, grupos capturados y advierten sobre posibles problemas de rendimiento.

## ¿Por qué usar herramientas online?

El uso de estas plataformas facilita enormemente el desarrollo de patrones complejos. Al proporcionar retroalimentación visual inmediata, ayudan a identificar errores de lógica y cuellos de botella en el rendimiento antes de integrar el código en una aplicación.

## Las mejores herramientas online

### 1. Regex101 ([regex101.com](https://regex101.com))

> [!NOTE]
> Considerada la "navaja suiza" de las regex. Soporta múltiples sabores como PCRE2, PCRE, JavaScript, Python, Golang, Java, .NET y Rust.

**Características:**
*   **Explicación automática:** Detalla el significado de cada token del patrón.
*   **Panel de coincidencias:** Resaltado visual de grupos y capturas.
*   **Debugger:** Muestra paso a paso las operaciones del motor (ideal para entender greedy/lazy y backtracking).
*   **Análisis de rendimiento:** Indica el número de pasos y advierte sobre backtracking catastrófico.
*   **Generador de código:** Exporta el patrón a diferentes lenguajes de programación.
*   **Compartir:** Posibilidad de guardar y compartir patrones mediante URL únicas.
*   **Unit Tests:** Opción de añadir casos de prueba unitarios para validación continua.

**Uso recomendado:** Prototipado de patrones complejos, aprendizaje interactivo, validación de estructuras críticas (como contraseñas o emails) y depuración profunda de fallos.

### 2. Regexr ([regexr.com](https://regexr.com))

> [!TIP]
> Herramienta visual con un fuerte enfoque educativo, basada principalmente en el motor de JavaScript.

**Características:**
*   **Interfaz limpia:** Diseño intuitivo con una *cheat sheet* integrada de fácil acceso.
*   **Resaltado en tiempo real:** Muestra todas las coincidencias mientras se escribe el patrón.
*   **Panel de referencia:** Acceso rápido a tokens, clases de caracteres y ejemplos prácticos.
*   **Comunidad:** Posibilidad de votar, buscar y compartir patrones con otros usuarios.
*   **Editor versátil:** Incluye editor de texto de muestra y configuración de banderas (*flags*).

**Uso recomendado:** Aprender expresiones regulares desde cero, probar rápidamente patrones para JavaScript y explorar soluciones creadas por la comunidad.

### 3. Debuggex ([debuggex.com](https://debuggex.com))

> [!IMPORTANT]
> Se destaca por su visualización gráfica mediante diagramas de ferrocarril (*railroad diagrams*). Soporta JavaScript, PCRE y Python.

**Características:**
*   **Representación visual:** Muestra el flujo lógico de la expresión regular de forma gráfica.
*   **Seguimiento de ruta:** Resalta el camino seguido en el diagrama al probar una cadena específica.
*   **Claridad estructural:** Aunque es menos detallado en sintaxis que Regex101, es excelente para comprender la arquitectura de patrones complejos.

**Uso recomendado:** Comprender visualmente patrones anidados y utilizarlo como apoyo didáctico en presentaciones o documentación.

### 4. Pythex ([pythex.org](https://pythex.org))

**Descripción:** Probador de regex específico para el módulo `re` de Python. Posee una interfaz minimalista y directa.

**Características:**
*   **Validación Python:** Indica si el patrón es sintácticamente correcto para Python.
*   **Resultados claros:** Muestra coincidencias y grupos capturados de forma sencilla.
*   **Banderas:** Permite elegir y probar banderas como `IGNORECASE`, `MULTILINE`, entre otras.

**Uso recomendado:** Verificar la compatibilidad estricta con Python y probar el comportamiento de escapes y *raw strings*.

### 5. RegExLib ([regexlib.com](https://regexlib.com))

**Descripción:** Repositorio masivo de patrones enviados por usuarios, que incluye votaciones y comentarios de la comunidad.

**Características:**
*   **Buscador categorizado:** Localiza patrones por tipo (email, teléfono, código postal, etc.).
*   **Pruebas integradas:** Permite probar los patrones encontrados directamente en la web.

**Uso recomendado:** Encontrar inspiración o soluciones predefinidas para problemas comunes (se recomienda revisar siempre la calidad y seguridad del patrón).

### 6. ExtendsClass Regex Tester ([extendsclass.com](https://extendsclass.com/regex-tester.html))

**Descripción:** Herramienta en línea compatible con múltiples motores (Python, JavaScript, PHP, Java, etc.) y capacidad de generación de código.

**Uso recomendado:** Funciona como una alternativa sólida a Regex101, especialmente cuando se requiere generar rápidamente código de reemplazo.

### 7. Scriptular ([scriptular.com](https://scriptular.com))

**Descripción:** Probador orientado específicamente a JavaScript con una interfaz simplificada y referencias rápidas de consulta.

**Uso recomendado:** Realización de pruebas rápidas y ligeras para desarrollos frontend.

### 8. iHateRegex ([ihateregex.io](https://ihateregex.io))

**Descripción:** Buscador visual de regex con un enfoque moderno y amigable. Presenta patrones comunes acompañados de diagramas y explicaciones claras.

**Uso recomendado:** Localizar rápidamente patrones para casos de uso típicos sin necesidad de escribirlos desde cero.

### 9. Regulex ([jex.im/regulex](https://jex.im/regulex))

**Descripción:** Generador de diagramas de ferrocarril similar a Debuggex, pero con mayores opciones de personalización y exportación.

**Uso recomendado:** Creación de imágenes técnicas de patrones para incluir en documentación o presentaciones.

## Aplicaciones de escritorio

*   **RegexBuddy (Comercial, Windows):** Entorno extremadamente potente con depuración avanzada, generación de código y traducción entre sabores de regex. Es considerada la herramienta profesional por excelencia.
*   **Kodos (Python):** Aunque es una herramienta más antigua, sigue siendo funcional para testear regex directamente en el entorno de Python de forma gráfica.
*   **Expressions (macOS):** Una aplicación con diseño minimalista y elegante para usuarios de Mac que buscan rapidez y simplicidad.

## Consejos de uso

> [!WARNING]
> No confíes ciegamente en patrones obtenidos de repositorios públicos sin entenderlos completamente; siempre adapta y valida según tus necesidades.

*   **Motor de producción:** Asegúrate de probar siempre el patrón en el mismo motor que utilizarás en el entorno real de ejecución.
*   **Pruebas de regresión:** Aprovecha las herramientas de *unit testing* (como las de Regex101) para verificar casos límite y evitar errores inesperados.
*   **Compatibilidad:** Si desarrollas para JavaScript, recuerda que el soporte para funciones avanzadas (como *lookbehind* o Unicode) depende de la versión del motor; verifica siempre en el navegador o entorno de destino.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Ejercicios Avanzados](../09_ejercicios/03_avanzados.md) | [🏠 Inicio](../../README.md) | [Libros y Guías ▶](02_libros_y_guias.md) |

