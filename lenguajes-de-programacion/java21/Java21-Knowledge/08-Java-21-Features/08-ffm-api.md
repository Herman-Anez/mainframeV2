# 🛠️ Foreign Function & Memory API (Preview)

La **Foreign Function & Memory API (FFM API)** reemplaza a JNI (*Java Native Interface*) para interactuar con código nativo y gestionar memoria fuera del heap de manera segura y eficiente. Unifica en una sola API el acceso a funciones externas y la manipulación de memoria nativa.

---

## 🏗️ Componentes principales

*   **`MemorySegment`**: Representa una región continua de memoria (nativa o en el heap). Permite operaciones *zero-copy* con arrays de bytes o memoria asignada mediante `malloc`.
*   **`Arena`**: Controla el ciclo de vida de los segmentos de memoria.
    *   `Arena.global()`: Memoria que nunca se libera.
    *   `Arena.ofAuto()`: Liberación gestionada automáticamente por el GC.
    *   `Arena.ofConfined()`: Control manual, limitado a un solo hilo.
    *   `Arena.ofShared()`: Control manual, accesible desde múltiples hilos.
*   **`ValueLayout`**: Describe tipos básicos (`JAVA_INT`, `JAVA_LONG`, etc.) para operaciones de lectura/escritura.
*   **`Linker`** y **`FunctionDescriptor`**: Permiten describir y llamar a funciones nativas.

---

## 💻 Acceso a memoria nativa

```java
try (var arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(10); // Asigna 10 bytes nativos
    segment.set(ValueLayout.JAVA_INT, 0, 123);  // Escribe un int en offset 0
    int valor = segment.get(ValueLayout.JAVA_INT, 0); // Lee el valor
}
```

> [!NOTE]
> Los segmentos proporcionan acceso tipado y seguro, incluyendo comprobaciones de límites (*bounds checks*) automáticas.

---

## 🔗 Llamada a funciones nativas (Downcall)

```java
Linker linker = Linker.nativeLinker();
MethodHandle strlen = linker.downcallHandle(
    linker.defaultLookup().find("strlen").get(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);

try (var arena = Arena.ofConfined()) {
    MemorySegment str = arena.allocateFrom("Hello"); // Crea una cadena compatible con C
    long len = (long) strlen.invoke(str);
}
```

### Upcalls
Es posible crear punteros a funciones Java que sean llamables directamente desde código nativo (C/C++).

---

## 🛡️ Seguridad y rendimiento

> [!IMPORTANT]
> *   **Acceso restringido:** Por defecto, se requieren flags de la JVM para realizar operaciones nativas por motivos de seguridad.
> *   **Rendimiento:** Superior a JNI al evitar transiciones de contexto complejas y permitir mejores optimizaciones por parte del compilador JIT.
> *   **Futuro:** Diseñada para ser compatible con los futuros *Value types* (Project Valhalla) y la *Vector API*.

> [!TIP]
> **Estado:** Preview en Java 21. Requiere `--enable-preview`.

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../../README.md)
- [☕ Java 21 Index](../../../index.md)

