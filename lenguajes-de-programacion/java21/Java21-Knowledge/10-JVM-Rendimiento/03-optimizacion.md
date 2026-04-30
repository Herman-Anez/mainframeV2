# OPTIMIZACIÓN DE RENDIMIENTO

Optimizar una aplicación Java implica un proceso iterativo de medición, análisis y ajuste tanto del código como de la JVM.
1. Métricas clave

    Throughput: cantidad de trabajo por unidad de tiempo.

    Latencia: tiempo de respuesta a una petición.

    Footprint: memoria ocupada (heap + nativa).

    Tiempo de arranque: desde inicio hasta que la aplicación está lista.

    Tiempo de calentamiento (warmup): hasta que el JIT ha optimizado los caminos calientes.

2. Herramientas de profiling y diagnóstico

    Java Flight Recorder (JFR) + Java Mission Control (JMC): recopilación de eventos de la JVM con bajo overhead. Permite analizar asignación de memoria, GC, bloqueos, actividad de hilos, etc.

    Async Profiler: genera flamegraphs de CPU y memoria utilizando perf sin instrumentación costosa.

    VisualVM: herramienta gráfica para monitoreo y profiling.

    JMH (Java Microbenchmark Harness): imprescindible para microbenchmarks precisos, evitando la interferencia del JIT (ej: @BenchmarkMode, @Warmup).

3. Estrategias de optimización de memoria

    Dimensionar correctamente el heap: establecer -Xms igual a -Xmx para evitar redimensionamientos.

    Elegir el GC adecuado y afinarlo con pausas objetivo.

    Reducir el uso de objetos temporales en bucles calientes (autoboxing, Strings concatenados → usar StringBuilder o text blocks en tiempo de compilación).

    Aprovechar colecciones inmutables (List.of) y records para evitar mutabilidad innecesaria.

    Uso de Optional sin abusar; no para campos de entidades.

    Liberar recursos explícitamente (try-with-resources).

    Evitar finalize() (obsoleto y costoso). Usar Cleaner si es imprescindible.

### 4. Optimización de CPU

    Dejar que el JIT trabaje: evite micro-optimizaciones prematuras; el JIT inlinea métodos y elimina código muerto.

    Perfiles de compilación: el JIT aprovecha perfiles de tipos para devirtualizar llamadas a métodos. Cuanto más estable sea el flujo de tipos, mejor.

    Conversión escalar y eliminación de autoboxing: los análisis de escape permiten eliminar objetos si no escapan del hilo.

    Usar Streams con criterio: para operaciones sencillas pueden generar objetos intermedios; para cálculos críticos medir si conviene un bucle tradicional.

    Concurrencia virtual: sustituir pools de hilos de plataforma por hilos virtuales y concurrencia estructurada para reducir latencia y mejorar throughput en aplicaciones I/O-bound.

### 5. Optimización del arranque y despliegue

    CDS (Class Data Sharing): -Xshare:on y creación de archivo compartido (-XX:ArchiveClassesAtExit / -XX:SharedArchiveFile) para reducir tiempo de carga.

    AOT con GraalVM Native Image si el tiempo de arranque es crítico (microservicios ephemeral), sacrificando algunas optimizaciones de pico.

    AppCDS permite incluir clases de la aplicación en el archivo compartido.

    Usar módulos y jlink para generar una JRE personalizada y ligera.

### 6. Técnicas avanzadas en Java 21

    Hilos virtuales para I/O intensiva: migrar servidores y procesos batch que antes requerían pools enormes.

    Scoped Values en lugar de ThreadLocal: menor consumo de memoria, herencia automática sin coste en hilos virtuales.

    Structured Concurrency: evita la pérdida de hilos, mejora la cancelación y la observabilidad.

    Pattern matching y records: reducen el código propenso a errores y la creación de clases intermedias, mejorando el uso de caché de instrucciones.

### 7. Pasos prácticos de optimización

    Definir objetivos de rendimiento (ej: p95 < 10ms, 1000 req/s).

    Establecer un entorno de pruebas reproducible.

    Perfilar con JFR/Async Profiler para identificar cuellos de botella (CPU, asignación, bloqueos).

    Analizar logs de GC y ajustar tamaño de heap o cambiar de GC si es necesario.

    Aplicar mejoras de código (evitar antipatrones, reducir asignaciones).

    Medir nuevamente para validar la mejora.

    Automatizar pruebas de rendimiento en el CI/CD para detectar regresiones.

### 8. Flags de JVM útiles para afinamiento
Flag	Propósito
-server	Selecciona el compilador servidor (suele ser por defecto en 64 bits)
-XX:+AggressiveOpts	Habilita optimizaciones experimentales (no necesario hoy)
-XX:TieredStopAtLevel=1	Solo compila con C1; reduce calentamiento a costa de máximo rendimiento
-XX:+AlwaysPreTouch	Toca toda la memoria del heap al inicio (evita page faults)
-XX:+UseStringDeduplication	Deduplicación de Strings (G1, ZGC)
-XX:+UseTransparentHugePages	Mejora rendimiento con páginas grandes de memoria
-XX:MaxInlineLevel=15	Ajusta la profundidad máxima de inlining
9. Ejemplo: ajuste para un microservicio con ZGC generacional
```text
java -Xmx2g -Xms2g -XX:+UseZGC -XX:+ZGenerational \
     -Xlog:gc*:file=gc.log:time,uptimemillis:filecount=5,filesize=20M \
     -XX:+AlwaysPreTouch \
     -jar aplicacion.jar
```

Se logra latencia de GC < 1ms y buen rendimiento incluso bajo cargas altas.


# ECOSISTEMA DE CONSTRUCCIÓN, PRUEBAS Y EMPAQUETADO

El ecosistema moderno de Java gira en torno a herramientas que automatizan la construcción, las pruebas y la distribución de aplicaciones. Esta sección profundiza en Maven y Gradle como gestores de proyectos, JUnit 5 como plataforma de pruebas y jlink / jpackage para crear distribuciones nativas y ligeras. Todas las explicaciones están actualizadas para Java 21.
