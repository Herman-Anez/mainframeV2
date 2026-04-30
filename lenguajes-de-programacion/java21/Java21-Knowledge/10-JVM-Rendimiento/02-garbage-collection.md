# ♻️ Garbage Collection en Java 21

El recolector de basura (GC) es el componente de la JVM encargado de gestionar la memoria de forma automática, liberando el espacio ocupado por objetos que ya no son alcanzables desde las raíces del programa (*GC Roots*).

---

## 1. Principios básicos del GC

La JVM identifica los objetos "vivos" recorriendo el grafo de referencias desde:
*   Variables locales en las pilas de los hilos.
*   Variables estáticas de las clases cargadas.
*   Referencias JNI (nativas).

Los objetos no alcanzables son marcados como basura y su memoria es reclamada para futuras asignaciones.

---

## 2. Hipótesis generacional

La mayoría de los algoritmos de GC se basan en la **hipótesis generacional débil**:
1.  La mayoría de los objetos "mueren" jóvenes.
2.  Los objetos que sobreviven tienden a persistir por mucho tiempo.

Para optimizar esto, el heap se divide típicamente en:
*   **Young Generation:** Donde se crean los objetos nuevos. Incluye el espacio **Eden** y dos espacios **Survivor (S0, S1)**.
*   **Old Generation (Tenured):** Donde residen los objetos de larga vida tras sobrevivir a varios ciclos en la generación joven.
*   **Metaspace:** Espacio de memoria nativa para metadatos de clases.

---

## 3. Conceptos fundamentales

| Término | Definición |
| :--- | :--- |
| **Minor GC** | Recolecta solo la generación joven. Es frecuente y rápido. |
| **Major / Full GC** | Involucra la generación vieja o todo el heap. Suele causar pausas mayores. |
| **Stop-The-World (STW)** | Pausa total de los hilos de la aplicación para realizar tareas de limpieza. |
| **Compactación** | Reorganización de objetos vivos para eliminar huecos de memoria (fragmentación). |
| **Promoción** | Paso de un objeto de la generación joven a la vieja. |

---

## 4. Recolectores disponibles en Java 21

### Serial GC (`-XX:+UseSerialGC`)
*   Utiliza un único hilo para todas las tareas de recolección.
*   **Uso ideal:** Aplicaciones con heaps pequeños (<100MB) o entornos de un solo núcleo.

### Parallel GC (`-XX:+UseParallelGC`)
*   Utiliza múltiples hilos para maximizar el *throughput* (rendimiento bruto).
*   Causa pausas STW tanto en recolecciones jóvenes como viejas.
*   **Uso ideal:** Procesamiento por lotes (*batch*) donde el rendimiento es prioridad sobre la latencia.

### G1 GC (`-XX:+UseG1GC`)
*   Recolector predeterminado desde Java 9. Divide el heap en regiones de tamaño fijo.
*   Permite definir objetivos de pausa mediante `-XX:MaxGCPauseMillis`.
*   **Mejoras en Java 21:** Optimización en la predicción de pausas y mejor gestión de objetos de gran tamaño (*humongous objects*).

### ZGC (`-XX:+UseZGC`)
*   Diseñado para latencia ultra baja (pausas constantes de <1ms) incluso en heaps de terabytes.
*   Realiza casi todo el trabajo de forma concurrente con la aplicación.

> [!IMPORTANT]
> **Generational ZGC (Java 21+):** Se activa con `-XX:+ZGenerational`. Divide el trabajo en generaciones para recolectar objetos jóvenes con mayor frecuencia, mejorando drásticamente el rendimiento y reduciendo la carga de CPU comparado con el modo no generacional.

### Shenandoah GC (`-XX:+UseShenandoahGC`)
*   Similar a ZGC en latencia baja, pero utiliza barreras de lectura/escritura en lugar de punteros coloreados.
*   Realiza compactación concurrente.

### Epsilon GC (`-XX:+UseEpsilonGC`)
*   Un "No-Op" GC: asigna memoria pero nunca la libera.
*   **Uso ideal:** Pruebas de rendimiento, benchmarks o microservicios de vida extremadamente corta.

---

## 5. Criterios de selección

*   **Baja Latencia:** ZGC o Shenandoah.
*   **Alto Rendimiento (Throughput):** Parallel GC.
*   **Equilibrio General:** G1 GC.
*   **Heaps Gigantes:** ZGC es la opción más escalable.

---

## 6. Parámetros de configuración comunes

| Parámetro | Descripción |
| :--- | :--- |
| `-Xms` / `-Xmx` | Tamaño inicial y máximo del heap. |
| `-XX:MaxGCPauseMillis` | Objetivo de pausa máxima (especialmente para G1). |
| `-XX:+UseStringDeduplication` | Reduce el uso de memoria eliminando duplicados de Strings. |
| `-Xlog:gc*` | Sistema unificado de logging para el GC. |
| `-XX:MetaspaceSize` | Tamaño inicial del área de metadatos. |
| `-XX:+ZGenerational` | Activa el modo generacional en ZGC (Recomendado en Java 21). |

---

## 7. Diagnóstico y logs

Para obtener un análisis detallado del comportamiento del GC, se recomienda el uso del flag `-Xlog`:

```bash
-Xlog:gc*=info:file=gc.log:time,uptimemillis:filecount=5,filesize=10M
```

> [!TIP]
> Herramientas como **GCViewer**, **GCEasy** o **Java Mission Control (JMC)** son esenciales para visualizar estos logs e identificar cuellos de botella.

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../README.md)
- [☕ Java 21 Index](../../index.md)
- [⬅️ Anterior: Funcionamiento JVM](./01-funcionamiento-jvm.md)
- [Siguiente: Optimización ➡️](./03-optimizacion.md)
