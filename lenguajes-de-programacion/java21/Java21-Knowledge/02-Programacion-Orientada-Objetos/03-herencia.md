# Herencia

La herencia es un mecanismo fundamental de la POO que permite crear nuevas clases basadas en clases existentes, promoviendo la reutilización de código y la creación de jerarquías lógicas.

---

## Concepto de Herencia

La herencia permite que una clase (subclase) reutilice los campos y métodos de otra (superclase). Se declara con la palabra clave `extends`:

```java
public class Empleado extends Persona {
    private String empresa;

    public Empleado(String nombre, int edad, String empresa) {
        super(nombre, edad);
        this.empresa = empresa;
    }
}
```

> [!IMPORTANT]
> En Java **no existe herencia múltiple de clases**; una clase solo puede tener una superclase directa. La herencia múltiple se simula mediante el uso de interfaces.

---

## La Clase `Object`

Todas las clases heredan implícitamente de `java.lang.Object` si no extienden otra clase. `Object` es la raíz de la jerarquía y proporciona métodos fundamentales como `toString()`, `equals()`, `hashCode()`, `clone()` y `finalize()` (este último obsoleto).

---

## Uso de la palabra clave `super`

- **`super()`**: Llama al constructor de la superclase. Debe ser obligatoriamente la primera instrucción del constructor.
- **`super.metodo()`**: Invoca un método de la superclase, lo cual es útil cuando el método ha sido sobrescrito en la subclase.

---

## Sobrescritura de Métodos (`@Override`)

Una subclase puede redefinir un método de la superclase con la misma firma y un tipo de retorno compatible (covarianza).

```java
@Override
public String toString() {
    return nombre + " (" + edad + ")";
}
```

> [!TIP]
> Se recomienda usar siempre la anotación `@Override` para que el compilador verifique que realmente se está sobrescribiendo un método existente.

---

## Modificador `final` en Herencia

- **Método `final`**: No puede ser sobrescrito por ninguna subclase.
- **Clase `final`**: No puede ser extendida (ejemplo: `String`, `Integer` y todos los `record`).
- **Argumento `final`**: La variable local no puede ser reasignada dentro del método.

---

## Clases Selladas (`sealed` / `permits`)

Introducidas en Java 17 y vigentes en Java 21, permiten restringir explícitamente qué clases o interfaces pueden extender o implementar un tipo dado.

```java
public sealed class Figura permits Circulo, Rectangulo, Triangulo {
    // ...
}
```

### Estados de las subclases permitidas:
- **`final`**: No se puede extender más.
- **`sealed`**: Sigue restringiendo sus propias subclases.
- **`non-sealed`**: Permite la extensión libre (jerarquía abierta de nuevo).

### Ejemplo de jerarquía sellada:
```java
sealed class Figura permits Circulo, Rectangulo, Triangulo {}
final class Circulo extends Figura { ... }
non-sealed class Rectangulo extends Figura { ... }
sealed class Triangulo extends Figura permits TrianguloEquilatero {}
final class TrianguloEquilatero extends Triangulo {}
```

---

## Jerarquías con Registros Sellados

Es un patrón muy potente (patrón algebraico) usar interfaces selladas implementadas por registros:

```java
sealed interface Expr permits Num, Suma, Resta {}

record Num(int valor) implements Expr {}
record Suma(Expr izq, Expr der) implements Expr {}
record Resta(Expr izq, Expr der) implements Expr {}
```

> [!NOTE]
> Esta codificación facilita enormemente el **Pattern Matching**, permitiendo que el compilador verifique la exhaustividad de los casos en expresiones `switch`.
