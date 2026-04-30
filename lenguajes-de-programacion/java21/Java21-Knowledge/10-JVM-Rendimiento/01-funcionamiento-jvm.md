# FUNCIONAMIENTO DE LA JVM
1. Arquitectura global de la JVM

La especificación de la JVM define varios subsistemas:

    Cargador de clases (Class Loader): carga, enlaza e inicializa las clases.

    Áreas de datos en tiempo de ejecución (Runtime Data Areas): pilas, heap, área de métodos, registros del PC, etc.

    Motor de ejecución (Execution Engine): interpreta el bytecode, ejecuta métodos nativos y realiza la compilación JIT.

    Interfaz nativa (JNI) y Foreign Function & Memory API (preview en 21): interacción con código no Java.

En Java 21, la JVM sigue siendo un proceso nativo que aloja el ecosistema Java y ha evolucionado para soportar hilos virtuales, nuevos GCs y mejoras de rendimiento.
2. Carga de clases

Se realiza bajo demanda (lazy loading). El proceso consta de:

    Carga: el ClassLoader busca el archivo .class y genera la representación interna (Class<?>).

    Enlace (Linking):

        Verificación: comprueba que el bytecode es correcto y seguro.

        Preparación: asigna memoria para variables estáticas y las inicializa con valores por defecto.

        Resolución (opcional): convierte referencias simbólicas a referencias directas (a clases, campos, métodos).

    Inicialización: ejecuta los inicializadores estáticos y asigna los valores iniciales definidos por el programador.

Jerarquía de ClassLoaders (típicamente):

    Bootstrap ClassLoader (nativo, carga las clases del núcleo de java.base).

    Platform ClassLoader (carga APIs de la plataforma, antiguo Extension ClassLoader).

    Application ClassLoader (carga clases del classpath).

En el sistema de módulos (JPMS), cada módulo tiene su propio cargador o se apoya en el de la aplicación.
3. Áreas de datos en tiempo de ejecución

    Registro del contador de programa (PC Register): por cada hilo, apunta a la instrucción actual.

    Pilas de la JVM (JVM Stacks): cada hilo tiene una pila que almacena marcos (frames). Un marco contiene variables locales, pila de operandos y referencia al runtime constant pool. La pila puede ser de tamaño fijo o dinámico (-Xss). Al lanzar una excepción, se recorre la pila para buscar un manejador.

    Heap: área compartida donde residen los objetos y arrays. Gestionado por el recolector de basura. Se puede dimensionar con -Xms (tamaño inicial) y -Xmx (máximo).

    Área de métodos (Metaspace desde Java 8): almacena metadatos de las clases (estructuras del class, constant pool, métodos, campos). Fuera del heap, en memoria nativa. Su tamaño se controla con -XX:MaxMetaspaceSize.

    Runtime Constant Pool: por cada clase, contiene constantes simbólicas, strings y referencias a métodos.

### 4. Motor de ejecución

Ejecuta las instrucciones bytecode. Combina dos modos:
Interpretación

Cada bytecode se decodifica y ejecuta por un intérprete. Arranque rápido pero ejecución lenta.
Compilación Just-In-Time (JIT)

Cuando un método o bucle se considera “caliente” (basado en contadores de invocación y ciclos), el compilador JIT lo traduce a código nativo optimizado.

Compiladores JIT en HotSpot:

    C1 (Client Compiler): compilación rápida con optimizaciones ligeras. Adecuado para aplicaciones con tiempo de arranque limitado.

    C2 (Server Compiler): optimizaciones agresivas, compilación más lenta pero código final muy eficiente.

Java 21 introduce mejoras en el compilador JIT: refinamiento de inlining, eliminación de bloqueos innecesarios, y soporte para nuevas instrucciones de CPU.

Compilación por niveles (Tiered Compilation) (activada por defecto):

    Nivel 0: interpretación.

    Nivel 1-3: compilación C1 con diferentes grados de optimización y recolección de perfiles.

    Nivel 4: compilación C2 usando los perfiles recogidos.

Compilación anticipada (AOT): mediante jaotc (en desuso a favor de GraalVM Native Image) no es soportada directamente en Java 21; GraalVM Native Image permite compilar a binario nativo con sus propias ventajas.
5. Hilos en la JVM

Java 21 soporta dos tipos de hilos:

    Hilos de plataforma: mapeados 1:1 a hilos del SO.

    Hilos virtuales: gestionados por la JVM sobre un pequeño número de carriers.

La JVM utiliza librerías nativas para la gestión de hilos y para operaciones de bloqueo (como Unsafe.park). Con los hilos virtuales, la JVM puede desacoplar el bloqueo virtual del bloqueo del carrier.
6. Herramientas de monitoreo en Java 21

    jps, jstat, jinfo, jmap, jstack, jcmd siguen siendo las herramientas estándar.

    jconsole y Java Mission Control (JMC) para monitoreo gráfico.

    jcmd permite obtener volcados de hilos de forma ligera (especialmente importante con hilos virtuales).

    -XX:+PrintFlagsFinal muestra las flags de la JVM.

    -Xlog:gc proporciona logs detallados del GC (unificado desde Java 9).

