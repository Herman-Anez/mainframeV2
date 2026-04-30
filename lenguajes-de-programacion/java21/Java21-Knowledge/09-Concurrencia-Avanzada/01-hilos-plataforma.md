
# 🧵 Hilos de Plataforma (Platform Threads)

Esta sección está dedicada a la concurrencia clásica y moderna en Java. Aunque los hilos de plataforma y los Executors llevan años con nosotros, entenderlos a fondo es imprescindible para apreciar las innovaciones de Java 21 y para combinar ambas aproximaciones en aplicaciones reales.

---

> [!NOTE]
> **Concurrencia Avanzada en Java 21:**
> Esta serie de documentos explora desde el modelo tradicional hasta las potentes capacidades de los hilos virtuales y la concurrencia estructurada.

---

## 🏗️ Modelo de hilos tradicional

Un hilo de plataforma es un hilo del sistema operativo envuelto por la JVM. Cada uno tiene su propia pila (típicamente ~1 MB) y es gestionado directamente por el SO. Crear miles de estos hilos consume una cantidad de memoria prohibitiva y el cambio de contexto puede degradar el rendimiento.

En Java, la clase `java.lang.Thread` representa un hilo de plataforma (también llamado kernel thread). Aunque en Java 21 existe `Thread.ofVirtual()`, el constructor clásico `new Thread(...)` sigue creando un hilo de plataforma.

---

## 🔄 Ciclo de vida de un hilo de plataforma

Los estados definidos en `Thread.State` son:

*   **NEW:** Creado pero no iniciado (`start()` no llamado).
*   **RUNNABLE:** Ejecutándose o listo para ejecutarse.
*   **BLOCKED:** Esperando adquirir un monitor (bloqueo intrínseco con `synchronized`).
*   **WAITING:** Esperando indefinidamente a que otro hilo realice una acción (`Object.wait()`, `Thread.join()`, `LockSupport.park()`).
*   **TIMED_WAITING:** Espera con tiempo límite (`sleep()`, `wait(timeout)`, `join(timeout)`, etc.).
*   **TERMINATED:** El hilo ha finalizado su ejecución.

---

## 🛠️ Creación de hilos de plataforma

### Extendiendo `Thread`

```java
class MiHilo extends Thread {
    @Override 
    public void run() {
        System.out.println("Hilo ejecutándose: " + Thread.currentThread().getName());
    }
}

MiHilo h = new MiHilo();
h.start(); // inicia el nuevo hilo
```

### Implementando `Runnable`

```java
Runnable tarea = () -> System.out.println("Tarea en hilo: " + Thread.currentThread().getName());
new Thread(tarea).start();
```

> [!TIP]
> Desde Java 8 podemos usar lambdas o referencias a métodos para definir el `Runnable`.

---

## ⚙️ Propiedades y métodos útiles

*   **`setName(String)` / `getName()`**: Nombre del hilo.
*   **`setDaemon(boolean)`**: Un hilo demonio termina cuando todos los hilos no demonio han finalizado.
*   **`setPriority(int)`**: Prioridad (1..10), solo una sugerencia al SO.
*   **`join()`**: Espera a que el hilo termine.
*   **`interrupt()`**: Envía una señal de interrupción. El hilo destino debe cooperar verificando `Thread.interrupted()` o manejando `InterruptedException`.
*   **`Thread.sleep(long)`**: Suspende el hilo actual durante un tiempo; puede lanzar `InterruptedException`.

---

## 🔒 Sincronización básica

### `synchronized`

Mecanismo de bloqueo intrínseco sobre objetos.

*   **Método sincronizado:**
    ```java
    public synchronized void incrementar() {
        contador++;
    }
    ```
*   **Bloque sincronizado:**
    ```java
    synchronized (objetoBloqueo) {
        // sección crítica
    }
    ```

> [!IMPORTANT]
> `wait()`, `notify()`, `notifyAll()` deben llamarse dentro de un bloque `synchronized` y sobre el objeto de bloqueo.

### `volatile`

Garantiza visibilidad de los cambios en una variable entre hilos, pero no atómica.

```java
private volatile boolean detenido = false;
public void detener() { detenido = true; }
```

---

## ⚠️ Problemas clásicos

*   **Condiciones de carrera:** Múltiples hilos acceden desordenadamente a datos compartidos.
*   **Deadlock:** Dos o más hilos se bloquean mutuamente esperando cerrojos que nunca liberan.
*   **Starvation:** Un hilo nunca obtiene acceso a un recurso.
*   **Inanición de hilos:** Mal uso de `notify()` en lugar de `notifyAll()`.

---

## 📉 Limitaciones del modelo de plataforma

*   **Escalabilidad:** Un hilo por petición no escala a decenas de miles de conexiones simultáneas.
*   **Consumo de recursos:** Memoria de pila y coste de creación.
*   **Gestión explícita:** Hay que definir pools, sincronización, etc.

Estas limitaciones motivaron la evolución hacia los Executors y, en Java 21, hacia los hilos virtuales.

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../../README.md)
- [☕ Java 21 Index](../../../index.md)
- [➡️ Siguiente: Executors y Futures](./02-executors-futures.md)

