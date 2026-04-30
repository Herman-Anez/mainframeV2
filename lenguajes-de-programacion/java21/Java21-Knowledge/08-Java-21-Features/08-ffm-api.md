# FOREIGN FUNCTION & MEMORY API (PREVIEW)

La Foreign Function & Memory API (FFM API) reemplaza a JNI (Java Native Interface) para interactuar con código nativo y gestionar memoria fuera del heap de manera segura y eficiente. Unifica en una sola API el acceso a funciones externas y la manipulación de memoria nativa.
Componentes principales

    MemorySegment: representa una región continua de memoria (nativa o en el heap). Puede ser cero-copy con arrays de bytes, o provenir de malloc, etc.

    Arena: controla el ciclo de vida de los segmentos de memoria (similar a un asignador). Tipos:

        Arena.global(): memoria que nunca se libera.

        Arena.ofAuto(): liberación gestionada por el garbage collector.

        Arena.ofConfined() y Arena.ofShared(): control manual o thread‑safe.

    ValueLayout: describe tipos básicos (JAVA_INT, JAVA_LONG, etc.) para leer/escribir en segmentos.

    FunctionDescriptor y Linker: permiten describir funciones nativas y llamarlas.

### Acceso a memoria nativa
```java
try (var arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(10); // 10 bytes nativos
    segment.set(ValueLayout.JAVA_INT, 0, 123); // escribe un int en offset 0
    int valor = segment.get(ValueLayout.JAVA_INT, 0); // lee
}
```

Los segmentos proporcionan acceso tipado y seguro (con bounds checks en modo depuración).
Llamada a funciones nativas (downcall)
```java
Linker linker = Linker.nativeLinker();
MethodHandle strlen = linker.downcallHandle(
    linker.defaultLookup().find("strlen").get(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);
MemorySegment str = arena.allocateFrom("Hello"); // guarda una cadena C
long len = (long) strlen.invoke(str);
```

### Exposición de funciones Java a código nativo (upcall)

Es posible crear punteros a funciones Java que sean llamables desde C.
Seguridad y rendimiento

    Acceso restringido por defecto; se requieren permisos o flags de JVM para operaciones nativas.

    Mejor rendimiento que JNI al evitar transiciones complejas y permitir optimizaciones del compilador JIT.

    La API está diseñada para ser amigable con los Value types (futuros) y el vector API.

    Estado: Preview en Java 21 (tercera incubación). Requiere --enable-preview.

