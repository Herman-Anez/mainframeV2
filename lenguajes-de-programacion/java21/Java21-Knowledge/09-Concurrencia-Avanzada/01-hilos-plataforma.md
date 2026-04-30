
# HILOS DE PLATAFORMA (PLATFORM THREADS)

NOTA CONCURRENCIA AVANZADA EN JAVA 21

Esta sección está dedicada a la concurrencia clásica y moderna en Java. Aunque los hilos de plataforma y los Executors llevan años con nosotros, entenderlos a fondo es imprescindible para apreciar las innovaciones de Java 21 y para combinar ambas aproximaciones en aplicaciones reales. A continuación, se presentan los contenidos detallados para cada uno de los tres archivos.

1. Modelo de hilos tradicional

Un hilo de plataforma es un hilo del sistema operativo envuelto por la JVM. Cada uno tiene su propia pila (típicamente ~1 MB) y es gestionado directamente por el SO. Crear miles de estos hilos consume una cantidad de memoria prohibitiva y el cambio de contexto puede degradar el rendimiento.

En Java, la clase java.lang.Thread representa un hilo de plataforma (también llamado kernel thread). Aunque en Java 21 existe Thread.ofVirtual(), el constructor clásico new Thread(...) sigue creando un hilo de plataforma.
2. Ciclo de vida de un hilo de plataforma

Los estados definidos en Thread.State son:

    NEW: creado pero no iniciado (start() no llamado).

    RUNNABLE: ejecutándose o listo para ejecutarse.

    BLOCKED: esperando adquirir un monitor (bloqueo intrínseco con synchronized).

    WAITING: esperando indefinidamente a que otro hilo realice una acción (Object.wait(), Thread.join(), LockSupport.park()).

    TIMED_WAITING: espera con tiempo límite (sleep(), wait(timeout), join(timeout), etc.).

    TERMINATED: el hilo ha finalizado su ejecución.

3. Creación de hilos de plataforma
Extendiendo Thread

```java
class MiHilo extends Thread {
    @Override public void run() {
        System.out.println("Hilo ejecutándose: " + Thread.currentThread().getName());
    }
}
MiHilo h = new MiHilo();
h.start(); // inicia el nuevo hilo
```

### Implementando Runnable

```java
Runnable tarea = () -> System.out.println("Tarea en hilo: " + Thread.currentThread().getName());
new Thread(tarea).start();
```

Desde Java 8 podemos usar lambdas o referencias a métodos para definir el Runnable.
4. Propiedades y métodos útiles

    setName(String) / getName(): nombre del hilo.

    setDaemon(boolean): un hilo demonio termina cuando todos los hilos no demonio han finalizado.

    setPriority(int): prioridad (1..10), solo una sugerencia al SO.

    join(): espera a que el hilo termine.

    interrupt(): envía una señal de interrupción. El hilo destino debe cooperar verificando Thread.interrupted() o manejando InterruptedException.

    Thread.sleep(long): suspende el hilo actual durante un tiempo; puede lanzar InterruptedException.

### 5. Sincronización básica

synchronized

Mecanismo de bloqueo intrínseco sobre objetos.

    Método sincronizado:

```java
    public synchronized void incrementar() {
        contador++;
    }
```

    Bloque sincronizado:

```java
    synchronized (objetoBloqueo) {
        // sección crítica
    }
```

wait(), notify(), notifyAll() deben llamarse dentro de un bloque synchronized y sobre el objeto de bloqueo.
volatile

Garantiza visibilidad de los cambios en una variable entre hilos, pero no atómica.

```java
private volatile boolean detenido = false;
public void detener() { detenido = true; }
```

### 6. Problemas clásicos

    Condiciones de carrera: múltiples hilos acceden desordenadamente a datos compartidos.

    Deadlock: dos o más hilos se bloquean mutuamente esperando cerrojos que nunca liberan.

    Starvation: un hilo nunca obtiene acceso a un recurso.

    Inanición de hilos: mal uso de notify() en lugar de notifyAll().

### 7. Limitaciones del modelo de plataforma

    Escalabilidad: un hilo por petición no escala a decenas de miles de conexiones simultáneas.

    Consumo de recursos: memoria de pila y coste de creación.

    Gestión explícita: hay que definir pools, sincronización, etc.

Estas limitaciones motivaron la evolución hacia los Executors (siguiente tema) y, en Java 21, hacia los hilos virtuales.
