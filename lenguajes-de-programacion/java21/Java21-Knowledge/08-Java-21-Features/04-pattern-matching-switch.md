# 🔄 Pattern Matching for switch

El **Pattern Matching para switch** convierte a esta estructura en una potente herramienta de despacho polimórfico. Se unifican los patrones de tipo, los patrones de registro, los patrones de array y el manejo explícito de `null`.

---

## 🌟 Características principales

*   **Polimorfismo:** `switch` sobre cualquier objeto, no solo sobre números, cadenas y enums.
*   **Patrones:** Cada `case` especifica un patrón: de tipo, de registro, de array o de literal.
*   **Exhaustividad:** El compilador garantiza que todos los casos posibles están cubiertos si el selector es una clase o interfaz sellada (o se incluye `default`).
*   **Manejo de `null`:** Manejo explícito con `case null -> ...`. Si no se incluye y la variable es `null`, se lanza `NullPointerException`.
*   **Guardas:** Se puede usar `when` para añadir condiciones adicionales a cualquier patrón.

---

## 💻 Ejemplo completo

```java
Object obj = obtenerAlgo();
switch (obj) {
    case null -> System.out.println("Es nulo");
    case String s when s.length() > 5 -> System.out.println("String largo: " + s);
    case String s -> System.out.println("String corto: " + s);
    case Integer i -> System.out.println("Entero: " + (i * i));
    case int[] arr -> System.out.println("Array de ints con " + arr.length + " elementos");
    default -> System.out.println("Tipo desconocido");
}
```

> [!IMPORTANT]
> **El orden importa:** Los casos se evalúan en orden. El más específico debe ir primero (por ejemplo, `String s when ...` antes que `String s`) para evitar que sea "sombreado" por el más general.

---

## ⚙️ Switch como Expresión

Si se usa `switch` como expresión, debe devolver un valor en cada rama y ser exhaustivo:

```java
String desc = switch (obj) {
    case null -> "nulo";
    case String s -> "texto";
    default -> "desconocido";
};
```

---

## 🏗️ Con tipos sellados y registros

```java
sealed interface Op permits Add, Mul {}
record Add(Op left, Op right) implements Op {}
record Mul(Op left, Op right) implements Op {}

int eval(Op op) {
    return switch (op) {
        case Add(var l, var r) -> eval(l) + eval(r);
        case Mul(var l, var r) -> eval(l) * eval(r);
    };
}
```

> [!NOTE]
> El compilador sabe que `Op` solo puede ser `Add` o `Mul`, por lo que no necesita `default` si se cubren todos los permisos.

---

## 📦 Patrones de array

```java
case int[] arr -> System.out.println("Longitud: " + arr.length);
case String[] arr -> System.out.println("Primer elemento: " + arr[0]);
```

Permite capturar el array y usarlo directamente sin necesidad de cast.

> [!TIP]
> **Estado:** Definitivo en Java 21. La evolución del `switch` se completa con esta poderosa función.

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../../README.md)
- [☕ Java 21 Index](../../../index.md)

