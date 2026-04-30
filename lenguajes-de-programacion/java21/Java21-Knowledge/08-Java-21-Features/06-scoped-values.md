# 🔭 Scoped Values (Preview)

Los **Scoped Values** son una alternativa moderna a `ThreadLocal` para compartir datos inmutables dentro de un hilo y sus hijos (virtuales o no), especialmente en concurrencia estructurada. Ofrecen mejor rendimiento y un ciclo de vida claramente delimitado.

---

## 🛑 El problema de `ThreadLocal`

*   **Acoplamiento implícito:** Cualquier código dentro del hilo puede leer/modificar un `ThreadLocal`.
*   **Gestión de memoria:** Dificultad en la limpieza (fugas de memoria si no se elimina adecuadamente, especialmente en pools).
*   **Sobrecarga:** Heredar `ThreadLocal` al crear millones de hilos virtuales añade un coste significativo.

---

## 🛠️ Uso de `ScopedValue`

Primero se declara la instancia:

```java
final static ScopedValue<String> USUARIO_ACTUAL = ScopedValue.newInstance();
```

Luego se vincula un valor durante un ámbito específico:

```java
ScopedValue.where(USUARIO_ACTUAL, "admin").run(() -> {
    System.out.println("Usuario: " + USUARIO_ACTUAL.get());
});
```

> [!IMPORTANT]
> Fuera del bloque, `USUARIO_ACTUAL` no está definido. Llamar a `get()` fuera del ámbito lanzará una excepción `NoSuchElementException`.

---

## 🧵 Vinculación con Hilos Virtuales

`where` crea un **binding** (asociación) que dura durante la ejecución del bloque proporcionado. Los hilos hijos heredan automáticamente el valor de manera eficiente y segura:

```java
ScopedValue.where(USUARIO_ACTUAL, "admin").run(() -> {
    Thread.startVirtualThread(() -> {
        // Dentro del hilo virtual, USUARIO_ACTUAL.get() devuelve "admin"
    });
});
```

> [!NOTE]
> El valor se hereda sin sobrecarga adicional, ya que los hilos virtuales comparten el contenedor de *scoped values* de manera optimizada.

---

## 🌟 Ventajas sobre `ThreadLocal`

> [!TIP]
> *   **Inmutabilidad:** Los valores no se pueden cambiar una vez establecidos en el ámbito.
> *   **Ámbito visible:** El binding solo existe dentro de la ejecución del bloque; es imposible olvidar la limpieza.
> *   **Rendimiento:** Mejor escalabilidad, diseñado específicamente para trabajar con millones de hilos virtuales.
> *   **Herencia segura:** Los hijos acceden al valor del padre sin riesgo de fugas de memoria.

---

## ⚙️ API adicional

*   **`ScopedValue.where(..., ...).call(() -> ...)`**: Para tareas que devuelven un valor (usando `Callable`).
*   **`ScopedValue.isBound()`**: Permite verificar si el valor tiene una asociación en el hilo actual.

> [!IMPORTANT]
> **Estado:** Preview en Java 21. Habilitar con `--enable-preview`.

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../../README.md)
- [☕ Java 21 Index](../../../index.md)

