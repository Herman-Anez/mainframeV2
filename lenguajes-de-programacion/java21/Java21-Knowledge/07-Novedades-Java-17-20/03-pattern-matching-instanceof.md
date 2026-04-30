# 🔍 Pattern Matching para instanceof

El **Pattern Matching para `instanceof`** se estandarizó en Java 16 y elimina la ceremonia de comprobación + casting manual. Permite asignar una variable de patrón directamente dentro de la condición.

---

## 🏗️ Sintaxis

```java
if (objeto instanceof String s) {
    // s es de tipo String aquí y se puede usar directamente
    System.out.println(s.toUpperCase());
}
```

La variable `s` queda vinculada solo si la comprobación es `true`. Es una variable local al bloque `if`, aunque también puede utilizarse en la parte derecha de una conjunción:

```java
if (objeto instanceof String s && s.length() > 5) {
    // s existe en la segunda parte del &&, y en el bloque
}
```

> [!WARNING]
> En un `||` no se puede usar `s` en el segundo operando porque quizá la primera parte sea `false` y `s` no estaría vinculada.

---

## 🧠 Ámbito y flujo de control

La variable de patrón se puede usar en cualquier punto donde el compilador esté seguro de que la comprobación ha sido exitosa. En estructuras condicionales complejas se aplica el análisis de flujo:

```java
if (!(objeto instanceof String s)) {
    // s no está disponible
    return;
}
// aquí s es seguro, porque si no hubiera sido String se habría retornado
System.out.println(s.length());
```

---

## 🛡️ Pattern matching con tipo y condición adicional (guarda)

No existe una guarda explícita en `instanceof`, pero el `&&` permite añadir condiciones:

```java
if (objeto instanceof String s && s.length() > 5) {
    // ...
}
```

Aquí se está combinando la comprobación de tipo con una condición sobre la variable de patrón.

---

## 📦 Patrones con instanceof y registros (Java 16+)

Aunque no se incluyó en el `instanceof` directamente el desglose de registros (eso es parte de los **Record Patterns** que llegaron más tarde como preview en Java 19 y final en Java 21), sí se puede usar `instanceof` con tipos genéricos mediante comodines acotados:

```java
if (shape instanceof Box<?> b) {
    // b es Box<?>
}
```

---

## ✅ Ventajas

*   **Código más limpio**: Una línea en lugar de tres (comprobación, declaración de variable, casting).
*   **Seguridad**: Menor probabilidad de error de casting (`ClassCastException`).
*   **Modernización**: Integración natural con nuevas estructuras como `switch` con patrones.

---

## ⚠️ Limitaciones

*   **Borrado de tipos**: No se puede usar `instanceof` con patrones sobre tipos genéricos concretos (`List<String>`). Sí se permite con `List<?>`.
*   **Inmutabilidad**: La variable de patrón es `final` implícitamente (no se puede reasignar).

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../README.md)
- [☕ Java 21 Index](../../index.md)
