# SCOPED VALUES (PREVIEW)

Los Scoped Values son una alternativa moderna a ThreadLocal para compartir datos inmutables dentro de un hilo y sus hijos (virtuales o no), especialmente en concurrencia estructurada. Ofrecen mejor rendimiento y un ciclo de vida claramente delimitado.
Problema de ThreadLocal

    Acoplamiento implícito: cualquier código dentro del hilo puede leer/modificar un ThreadLocal.

    Dificultad en la limpieza (memory leaks si no se elimina adecuadamente, especialmente con pools de hilos).

    Coste en hilos virtuales: heredar ThreadLocal al crear un hilo virtual añade sobrecarga.

### Uso de ScopedValue
```java
final static ScopedValue<String> USUARIO_ACTUAL = ScopedValue.newInstance();
```

### ScopedValue.where(USUARIO_ACTUAL, "admin").run(() -> {
    System.out.println("Usuario: " + USUARIO_ACTUAL.get());
});
// Fuera del bloque, USUARIO_ACTUAL no está definido (llamar a get() lanza NoSuchElementException)

where crea un binding (asociación) que dura durante la ejecución del Runnable proporcionado. Los hilos hijos heredan automáticamente el valor, pero no pueden cambiarlo. Es inmutable.
Vinculación con hilos virtuales y concurrencia estructurada
```java
ScopedValue.where(USUARIO_ACTUAL, "admin").run(() -> {
    Thread.startVirtualThread(() -> {
        // dentro del hilo virtual, USUARIO_ACTUAL.get() == "admin"
    });
});
```

El valor se hereda sin sobrecarga adicional, ya que los hilos virtuales pueden compartir el contenedor de scoped values de manera eficiente.
API adicional

    ScopedValue.getWhere(ScopedValue<T>, T, Supplier<Runnable>) para obtener un Runnable con un binding alternativo de manera funcional.

    ScopedValue.where(..., ...).call(() -> ...) para tareas que devuelven valor (con Callable).

### Ventajas sobre ThreadLocal

    Inmutabilidad: los valores no se pueden cambiar una vez establecidos.

    Ámbito visible: el binding solo existe dentro de la ejecución del bloque, imposible de olvidar limpiar.

    Mejor rendimiento y escalabilidad (especialmente en hilos virtuales).

    Herencia clara sin fugas.

    Estado: Preview en Java 21. Habilitar con --enable-preview.

