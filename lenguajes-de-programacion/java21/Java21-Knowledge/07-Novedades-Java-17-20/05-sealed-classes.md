# 🛡️ Sealed Classes (Clases Selladas)

Las **Clases Selladas** permiten controlar explícitamente qué subclases pueden extender una clase o qué implementaciones tiene una interfaz. Se estandarizaron en Java 17. Son el complemento perfecto para los **Records** y el pattern matching exhaustivo.

---

## 🏗️ Declaración

```java
public sealed class Figura permits Circulo, Rectangulo, Triangulo {
    // cuerpo de la clase sellada
}
```

La clase `Figura` declara que solo las clases listadas en `permits` pueden extenderla. Las subclases permitidas deben estar en el mismo módulo (o paquete si no se usa módulo) y a su vez deben elegir uno de estos modificadores:

*   **final**: No se puede extender más.
*   **sealed**: Sigue restringiendo la herencia (con su propio `permits`).
*   **non-sealed**: Permite que cualquier clase pueda extenderla (rompe el sellado).

**Ejemplo:**

```java
sealed interface Expr permits Suma, Resta, Num {}

record Suma(Expr izq, Expr der) implements Expr {}
record Resta(Expr izq, Expr der) implements Expr {}

final class Num implements Expr { 
    int valor; 
}
```

---

## 📏 Reglas de uso

*   **Ubicación**: La clase sellada y sus subclases permitidas deben pertenecer al mismo módulo (o al mismo paquete sin módulos).
*   **Inferencia**: Si las subclases son anidadas o están en el mismo archivo, se puede omitir `permits` y el compilador las deduce:

```java
sealed class Op {
    final class A extends Op {}
    final class B extends Op {}
}
```

*   **Restricción de permisos**: No se pueden declarar `permits` con clases que no pertenezcan al mismo módulo/paquete.
*   **Abstracción**: La clase sellada puede ser abstracta.
*   **Interfaces**: Las interfaces también pueden ser selladas.

---

## ✅ Exhaustividad en el switch

La gran ventaja es que el compilador conoce todas las posibilidades, por lo que en un `switch` con pattern matching no se necesita `default` si se cubren todos los `permits`:

```java
double evaluar(Expr e) {
    return switch (e) {
        case Suma(var i, var d) -> evaluar(i) + evaluar(d);
        case Resta(var i, var d) -> evaluar(i) - evaluar(d);
        case Num n              -> n.valor;
    };  // sin default, exhaustivo
}
```

> [!IMPORTANT]
> Esto hace que los añadidos futuros a la jerarquía sellada provoquen un error de compilación en los `switch` que no los contemplen, aumentando la robustez del código.

---

## 🔄 Compatibilidad con instanceof

El patrón de `instanceof` con tipos sellados permite comprobaciones en cascada; también el compilador puede inferir exhaustividad en flujos de control si se usa una cadena de `if-else if`. Sin embargo, el `switch` es la forma más clara y concisa.

---

## 💡 Cuándo usar clases selladas

*   Modelado de **tipos algebraicos** (*sum types*) junto con records.
*   **Jerarquías de dominio restringidas** (p.ej., estados de un pedido: Pendiente, Enviado, Entregado, Cancelado).
*   Reemplazo de **enumeraciones complejas** que necesitan comportamientos distintos por estado.
*   **API internas** en las que no se desea que terceros extiendan ciertas clases.

---

## 🤝 Relación con records

> [!TIP]
> A menudo se combinan `sealed interface` con varios `record` que la implementan. Esto permite un modelado funcional muy potente y seguro para manipular datos.

---

## 🛠️ Ejemplo completo

```java
sealed interface Figura permits Rectangulo, Circulo, Triangulo {}

record Rectangulo(double ancho, double alto) implements Figura {}
record Circulo(double radio) implements Figura {}
final class Triangulo implements Figura { 
    double base, altura; 
}

// Uso
double area(Figura f) {
    return switch (f) {
        case Rectangulo(var a, var al) -> a * al;
        case Circulo(var r) -> Math.PI * r * r;
        case Triangulo t -> (t.base * t.altura) / 2;
    };
}
```

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../README.md)
- [☕ Java 21 Index](../../index.md)

