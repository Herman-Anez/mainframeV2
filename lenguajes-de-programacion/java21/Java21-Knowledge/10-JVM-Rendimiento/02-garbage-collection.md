# GARBAGE COLLECTION
1. Principios básicos del GC

El recolector de basura libera memoria ocupada por objetos que ya no son alcanzables desde las raíces (variables locales, estáticas, referencias activas de hilos, etc.). La JVM divide el heap en regiones (o generaciones) para aplicar distintos algoritmos según la longevidad de los objetos.
2. Hipótesis generacional

    La mayoría de los objetos mueren jóvenes (weak generational hypothesis).

    Los objetos viejos que sobreviven tienden a persistir mucho tiempo.
    Por ello, se divide en:

    Young Generation: objeto recién creado. Subdividida en Eden y dos espacios Survivor (S0, S1).

    Old Generation (Tenured): objetos que han sobrevivido varios ciclos de GC menor.

    Metaspace (fuera del heap): metadatos de clases.

3. Conceptos comunes

    GC menor (Minor GC): recolecta solo la generación joven. Rápido.

    GC mayor (Major GC) / Full GC: involucra la generación vieja y a menudo todo el heap. Pausas largas, intentar minimizarlas.

    Stop-The-World (STW): todos los hilos de aplicación se detienen para que el GC realice su trabajo.

    Compactación: reorganiza objetos vivos para eliminar fragmentación.

    Promoción: mover objetos supervivientes de la generación joven a la vieja.

### 4. Recolectores disponibles en Java 21
Serial GC ( -XX:+UseSerialGC )

    Un solo hilo para GC menor y mayor.

    Adecuado para aplicaciones con heap pequeño (~<100 MB) o entornos embebidos.

    Pausas largas con heap grande.

### Parallel GC ( -XX:+UseParallelGC )

    Varios hilos para GC menor y mayor (stop-the-world en ambos).

    Maximiza throughput (rendimiento).

    Buena opción para procesos batch que toleran pausas.

### G1 GC ( -XX:+UseG1GC ) – Predeterminado desde Java 9

    Divide el heap en regiones de tamaño fijo y recolecta preferentemente las regiones con más basura.

    Balance entre pausas y throughput.

    Pausas configurables con -XX:MaxGCPauseMillis (por defecto 200 ms).

    Realiza compactaciones parciales y ciclos de marcado concurrente (SATB).

    Mejoras en Java 21: refinamiento de la predicción de pausa, mejor manejo de regiones humongous.

### ZGC ( -XX:+UseZGC )

    Diseñado para pausas inferiores a 1 ms, incluso con heaps de terabytes.

    Concurrente en casi todas las fases (marcado, compactación, referencias).

    A partir de Java 21, ZGC soporta generaciones (activando -XX:+ZGenerational). Separa objetos jóvenes de viejos para recolectar los jóvenes con mucha más frecuencia, reduciendo la presión de asignación.

    Sus algoritmos de “punteros coloreados” y “load barriers” permiten mover objetos sin detener los hilos de aplicación.

    Muy recomendado para aplicaciones que requieren baja latencia.

### Shenandoah GC ( -XX:+UseShenandoahGC )

    También de latencia ultrabaja, con compactación concurrente mediante evacuación.

    A diferencia de ZGC, no requiere punteros coloreados; usa barreras de lectura y escritura.

    Soporta generaciones opcionales (modo generacional en desarrollo/preview).

    Disponible en JDK builds que lo incluyan; en Oracle JDK está presente.

### Epsilon GC ( -XX:+UseEpsilonGC )

    No recolecta basura; solo asigna memoria hasta que se acaba.

    Útil para pruebas de rendimiento, benchmarks, o aplicaciones de vida corta.

### 5. Factores que afectan la elección del GC

    Latencia máxima aceptable: ZGC / Shenandoah.

    Throughput: Parallel GC.

    Equilibrio: G1.

    Tamaño del heap: ZGC escala mejor a heaps muy grandes.

    Número de núcleos: Parallel GC y G1 se benefician de muchos cores; ZGC requiere algunos cores para concurrencia.

### 6. Parámetros de ajuste comunes
Parámetro	Descripción
-Xmx<size>	Tamaño máximo del heap (ej: -Xmx2g)
-Xms<size>	Tamaño inicial del heap
-XX:MaxGCPauseMillis	Objetivo de pausa máxima (G1)
-XX:+UseStringDeduplication	Elimina duplicados de String en el heap (G1, ZGC)
-XX:+PrintGCDetails	(obsoleto, usar -Xlog:gc*)
-Xlog:gc	Logging unificado del GC
-XX:MetaspaceSize	Tamaño inicial del metaspace
-XX:MaxMetaspaceSize	Tamaño máximo del metaspace
-XX:+UseZGC	Activa ZGC
-XX:+ZGenerational	Modo generacional en ZGC (Java 21+)
-XX:ConcGCThreads	Número de hilos para fases concurrentes
-XX:ParallelGCThreads	Número de hilos para fases STW
7. Logs y análisis

Con el sistema unificado de logging (-Xlog):
```text
-Xlog:gc*=info:file=gc.log:time,uptimemillis:filecount=5,filesize=10M
```

Herramientas como GCViewer, GCEasy, o JMC permiten visualizar los logs y ajustar parámetros.
