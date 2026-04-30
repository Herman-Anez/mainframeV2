# Funcionamiento de la JVM

## 1. Arquitectura Global de la JVM

La especificación de la JVM define varios subsistemas clave:

*   **Cargador de clases (Class Loader)**: Carga, enlaza e inicializa las clases.
*   **Áreas de datos en tiempo de ejecución (Runtime Data Areas)**: Pilas, heap, área de métodos, registros del PC, etc.
*   **Motor de ejecución (Execution Engine)**: Interpreta el bytecode, ejecuta métodos nativos y realiza la compilación JIT.
*   **Interfaz nativa (JNI) y Foreign Function & Memory API (Preview en 21)**: Interacción con código no Java.

> [!NOTE]
> En Java 21, la JVM sigue siendo un proceso nativo que aloja el ecosistema Java y ha evolucionado para soportar hilos virtuales, nuevos GCs y mejoras de rendimiento.

---

## 2. Carga de Clases

Se realiza bajo demanda (*lazy loading*). El proceso consta de tres etapas principales:

1.  **Carga**: El `ClassLoader` busca el archivo `.class` y genera la representación interna (`Class<?>`).
2.  **Enlace (Linking)**:
    *   **Verificación**: Comprueba que el bytecode es correcto y seguro.
    *   **Preparación**: Asigna memoria para variables estáticas y las inicializa con valores por defecto.
    *   **Resolución (opcional)**: Convierte referencias simbólicas a referencias directas (a clases, campos, métodos).
3.  **Inicialización**: Ejecuta los inicializadores estáticos y asigna los valores iniciales definidos por el programador.

### Jerarquía de ClassLoaders (Típicamente)

*   **Bootstrap ClassLoader**: Nativo, carga las clases del núcleo de `java.base`.
*   **Platform ClassLoader**: Carga APIs de la plataforma (antiguo *Extension ClassLoader*).
*   **Application ClassLoader**: Carga clases del *classpath*.

> [!IMPORTANT]
> En el sistema de módulos (JPMS), cada módulo puede tener su propio cargador o apoyarse en el de la aplicación para mayor aislamiento.

---

## 3. Áreas de Datos en Tiempo de Ejecución

*   **Registro del contador de programa (PC Register)**: Por cada hilo, apunta a la instrucción actual.
*   **Pilas de la JVM (JVM Stacks)**: Cada hilo tiene una pila que almacena marcos (*frames*). Un marco contiene variables locales, pila de operandos y referencia al *runtime constant pool*. La pila puede ser de tamaño fijo o dinámico (`-Xss`). Al lanzar una excepción, se recorre la pila para buscar un manejador.
*   **Heap**: Área compartida donde residen los objetos y arrays. Gestionado por el recolector de basura. Se puede dimensionar con `-Xms` (tamaño inicial) y `-Xmx` (máximo).
*   **Área de métodos (Metaspace desde Java 8)**: Almacena metadatos de las clases (estructuras del class, *constant pool*, métodos, campos). Fuera del heap, en memoria nativa. Su tamaño se controla con `-XX:MaxMetaspaceSize`.
*   **Runtime Constant Pool**: Por cada clase, contiene constantes simbólicas, strings y referencias a métodos.

---

## 4. Motor de Ejecución

Ejecuta las instrucciones bytecode combinando dos modos:

### Interpretación
Cada bytecode se decodifica y ejecuta por un intérprete. Ofrece un arranque rápido pero una ejecución más lenta en comparación con el código nativo.

### Compilación Just-In-Time (JIT)
Cuando un método o bucle se considera "caliente" (basado en contadores de invocación y ciclos), el compilador JIT lo traduce a código nativo optimizado.

#### Compiladores JIT en HotSpot:
*   **C1 (Client Compiler)**: Compilación rápida con optimizaciones ligeras. Adecuado para aplicaciones con tiempo de arranque limitado.
*   **C2 (Server Compiler)**: Optimizaciones agresivas, compilación más lenta pero código final muy eficiente.

> [!TIP]
> Java 21 introduce mejoras en el compilador JIT: refinamiento de *inlining*, eliminación de bloqueos innecesarios y soporte para nuevas instrucciones de CPU.

#### Compilación por Niveles (Tiered Compilation)
Activada por defecto, gestiona la transición entre niveles:
*   **Nivel 0**: Interpretación.
*   **Nivel 1-3**: Compilación C1 con diferentes grados de optimización y recolección de perfiles.
*   **Nivel 4**: Compilación C2 usando los perfiles recogidos.

---

## 5. Hilos en la JVM

Java 21 soporta dos tipos de hilos:

*   **Hilos de plataforma**: Mapeados 1:1 a hilos del sistema operativo.
*   **Hilos virtuales**: Gestionados por la JVM sobre un pequeño número de *carriers*.

La JVM utiliza librerías nativas para la gestión de hilos y para operaciones de bloqueo (como `Unsafe.park`). Con los hilos virtuales, la JVM puede desacoplar el bloqueo virtual del bloqueo del *carrier*.

---

## 6. Herramientas de Monitoreo en Java 21

*   **Línea de comandos**: `jps`, `jstat`, `jinfo`, `jmap`, `jstack`, `jcmd` (herramientas estándar).
*   **Monitoreo gráfico**: `jconsole` y **Java Mission Control (JMC)**.
*   **Comandos útiles**:
    *   `jcmd`: Permite obtener volcados de hilos de forma ligera (vital con hilos virtuales).
    *   `-XX:+PrintFlagsFinal`: Muestra todas las *flags* actuales de la JVM.
    *   `-Xlog:gc`: Proporciona logs detallados del GC (formato unificado desde Java 9).

---

| Anterior | Inicio | Siguiente |
| :---: | :---: | :---: |
| [Concurrencia Estructurada](../09-Concurrencia-Avanzada/03-concurrencia-estructurada.md) | [Índice](../../README.md) | [Garbage Collection](02-garbage-collection.md) |


