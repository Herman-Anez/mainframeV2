# 🙈 Unnamed Patterns and Variables (Preview)

Los **Patrones y Variables sin nombre** permiten usar el carácter `_` para declarar variables o componentes de patrón cuyo valor no se necesita, mejorando la legibilidad y reduciendo advertencias del compilador.

---

## 🗑️ Variable sin nombre (`_`)

En cualquier lugar donde se declare una variable local, parámetro de lambda o bloque `catch`, se puede usar `_` si el valor no se va a utilizar:

```java
// En try-with-resources
try (var _ = ScopedValue.where(FLAG, true)) {
    // No necesitamos la variable del scope auto-closeable
}

// En un bloque catch
try { 
    ... 
} catch (Exception _) {
    // No nos interesa la excepción concreta
}

// En lambdas
lista.stream().collect(Collectors.toMap(k -> k, _ -> 1)); // el valor no importa

// En bucles for-each
for (var _ : lista) {
    // solo interesa contar iteraciones
}
```

> [!NOTE]
> El compilador no emite advertencias por "variable no utilizada" y la intención del código queda mucho más clara para otros desarrolladores.

---

## 🧩 Patrones sin nombre (`_`)

En patrones de registro o de `switch`, se puede usar `_` para componentes que no interesan:

```java
record Rectangulo(double ancho, double alto) {}

if (figura instanceof Rectangulo(double _, double alto)) {
    System.out.println("Alto: " + alto);
}

switch (figura) {
    case Rectangulo(var _, var alto) -> "Alto: " + alto;
    // ...
}
```

> [!TIP]
> También se puede usar en patrones de registro **anidados**: `Segmento(Punto(_, _), Punto(var x, var y))`.

---

## 🔄 Patrón sin nombre en `case`

En un `switch`, un patrón `_` puede funcionar de forma similar a un `default`, pero capturando cualquier valor sin necesidad de vincular una variable:

```java
switch (obj) {
    case String s -> System.out.println("Es string");
    case _ -> System.out.println("Es cualquier otra cosa");
}
```

> [!IMPORTANT]
> A diferencia de `default`, `_` es un patrón que coincide con todo. Si hay varios `case _`, se aplica el orden de declaración.

---

## 🌟 Beneficios

*   **Claridad:** Se documenta explícitamente que el valor no se usa.
*   **Limpieza:** Menos contaminación del espacio de nombres con variables irrelevantes.
*   **Mantenibilidad:** Mejora drásticamente las revisiones de código al eliminar ruido.

> [!TIP]
> **Estado:** Preview en Java 21. Habilitar con `--enable-preview`.

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../../README.md)
- [☕ Java 21 Index](../../../index.md)
