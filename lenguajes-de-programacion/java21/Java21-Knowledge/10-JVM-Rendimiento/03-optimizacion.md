# 🚀 Optimización de Rendimiento en Java 21

La optimización en Java es un proceso iterativo que combina la medición precisa, el análisis de cuellos de botella y el ajuste fino tanto del código fuente como de los parámetros de la Máquina Virtual.

---

## 1. Métricas clave

Para evaluar el rendimiento, debemos centrarnos en cinco pilares:

*   **Throughput (Caudal):** Cantidad de trabajo completado por unidad de tiempo (ej. transacciones/segundo).
*   **Latencia:** Tiempo de respuesta individual a una petición (p95, p99).
*   **Footprint (Huella de memoria):** Memoria total consumida (Heap + Memoria Nativa).
*   **Startup Time:** Tiempo desde que se lanza el proceso hasta que la aplicación está lista.
*   **Warmup Time:** Tiempo necesario para que el compilador JIT optimice las rutas críticas de ejecución.

---

## 2. Herramientas de profiling y diagnóstico

| Herramienta | Descripción |
| :--- | :--- |
| **JFR + JMC** | *Java Flight Recorder* y *Mission Control*. Recopilación de eventos con bajísimo impacto (<1%). |
| **Async Profiler** | Ideal para generar *Flame Graphs* de CPU y memoria sin los sesgos de herramientas tradicionales. |
| **VisualVM** | Interfaz gráfica "todo en uno" para monitoreo en tiempo real y análisis de *heap dumps*. |
| **JMH** | *Java Microbenchmark Harness*. La herramienta estándar para realizar microbenchmarks fiables. |

---

## 3. Estrategias de optimización de memoria

1.  **Dimensionamiento:** Establecer `-Xms` igual a `-Xmx` para evitar la sobrecarga de redimensionar el heap durante la ejecución.
2.  **Reducción de Asignaciones:** Evitar el autoboxing innecesario y el uso excesivo de objetos temporales en bucles críticos.
3.  **Colecciones Eficientes:** Utilizar `List.of()` o `Map.of()` para colecciones inmutables y `records` para estructuras de datos compactas.
4.  **Gestión de Recursos:** Implementar `try-with-resources` para garantizar la liberación inmediata de memoria nativa y descriptores de archivo.

> [!CAUTION]
> Evita el uso de `finalize()`. Está obsoleto y degrada severamente el rendimiento del GC. Usa `java.lang.ref.Cleaner` si necesitas limpieza de recursos no Java.

---

## 4. Optimización de CPU

*   **Confiar en el JIT:** Evitar micro-optimizaciones manuales que dificulten el trabajo del compilador (como desenrollar bucles manualmente).
*   **Análisis de Escape:** El JIT puede realizar "asignación en pila" si detecta que un objeto no escapa del hilo actual.
*   **Streams vs Bucles:** Los Streams son excelentes para legibilidad, pero en secciones de rendimiento crítico, un bucle tradicional puede ser más eficiente al evitar objetos intermedios.

---

## 5. Optimización del arranque y despliegue

Para entornos de microservicios y *serverless*, el arranque es crítico:

*   **AppCDS (Class Data Sharing):** Permite compartir metadatos de clases entre ejecuciones, reduciendo drásticamente el tiempo de carga y el uso de memoria.
*   **jlink:** Crea un JRE personalizado que solo contiene los módulos necesarios, reduciendo el tamaño del binario final.
*   **GraalVM Native Image:** Compila la aplicación a un binario nativo para un arranque instantáneo (sacrificando algo de *peak throughput*).

---

## 6. Técnicas avanzadas en Java 21

> [!TIP]
> Java 21 introduce herramientas revolucionarias para la escalabilidad:

*   **Virtual Threads:** Permiten manejar miles de conexiones concurrentes sin el overhead de los hilos de plataforma.
*   **Scoped Values:** Una alternativa moderna y eficiente a `ThreadLocal`, optimizada para hilos virtuales.
*   **Structured Concurrency:** Mejora la gestión de tareas paralelas, facilitando la propagación de errores y cancelaciones.
*   **Generational ZGC:** Permite mantener pausas de milisegundos incluso bajo cargas de trabajo pesadas.

---

## 7. Metodología de optimización

1.  **Definir Objetivos:** Establecer metas claras (ej: "latencia p99 < 50ms").
2.  **Medir:** Obtener una línea base usando JFR o JMH.
3.  **Identificar:** Localizar el cuello de botella (¿CPU? ¿GC? ¿Bloqueos de hilos?).
4.  **Aplicar Cambios:** Realizar una sola modificación a la vez.
5.  **Validar:** Volver a medir para confirmar la mejora y asegurar que no hay regresiones.

---

## 8. Flags de la JVM para afinamiento

| Flag | Propósito |
| :--- | :--- |
| `-XX:+AlwaysPreTouch` | Inicializa toda la memoria del heap al arrancar (evita fallos de página). |
| `-XX:+UseStringDeduplication` | Elimina duplicados de Strings en el heap para ahorrar memoria. |
| `-XX:+UseTransparentHugePages` | Optimiza el acceso a memoria usando páginas grandes del SO. |
| `-XX:MaxInlineLevel=15` | Ajusta la agresividad del inlining del compilador JIT. |

---

## 9. Ejemplo de configuración: Microservicio con ZGC

Configuración recomendada para una aplicación de baja latencia en Java 21:

```bash
java -Xmx2g -Xms2g \
     -XX:+UseZGC -XX:+ZGenerational \
     -XX:+AlwaysPreTouch \
     -Xlog:gc*:file=gc.log:time,uptimemillis:filecount=5,filesize=20M \
     -jar mi-aplicacion.jar
```

---

## ⏭️ Próximos pasos: Ecosistema

El rendimiento es solo una parte del éxito. El ecosistema moderno de Java proporciona herramientas para automatizar la construcción, pruebas y despliegue:

*   **Maven y Gradle:** Gestión de dependencias y ciclos de vida.
*   **JUnit 5:** Pruebas unitarias y de integración.
*   **jlink / jpackage:** Distribución de aplicaciones ligeras.

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../README.md)
- [☕ Java 21 Index](../../index.md)
- [⬅️ Anterior: Garbage Collection](./02-garbage-collection.md)
