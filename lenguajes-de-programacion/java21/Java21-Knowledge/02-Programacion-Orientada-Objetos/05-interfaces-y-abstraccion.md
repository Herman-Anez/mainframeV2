# Interfaces y Abstracción

La abstracción es el proceso de ocultar los detalles de implementación y mostrar solo la funcionalidad esencial al usuario. En Java, esto se logra principalmente mediante clases abstractas e interfaces.

---

## Clases Abstractas

Una clase declarada como `abstract` no puede instanciarse directamente. Puede contener métodos abstractos (sin implementación, obligando a las subclases a definirlos) y métodos concretos.

```java
public abstract class Animal {
    public abstract String sonido();
    public void dormir() {
        System.out.println("Zzz");
    }
}
```

---

## Interfaces

Una interfaz es un contrato que define un conjunto de métodos. A diferencia de las clases, una clase puede implementar múltiples interfaces:

```java
public class Perro implements Mascota, Carnivoro { ... }
```

### Capacidades modernas de las interfaces:
- **Métodos `default` (Java 8+)**: Poseen implementación por defecto y pueden ser sobrescritos.
- **Métodos `static` (Java 8+)**: Métodos de utilidad asociados a la interfaz.
- **Métodos `private` (Java 9+)**: Permiten compartir código entre métodos `default` y `static`.

---

## Evolución de las Interfaces (Resumen)

- **Java 8**: Introducción de métodos `default` y `static`.
- **Java 9**: Introducción de métodos `private`.
- **Java 17/21**: Interfaces selladas (`sealed interface`) y soporte para pattern matching.

---

## Interfaces Funcionales

Son interfaces con un único método abstracto (SAM - *Single Abstract Method*). Se anotan con `@FunctionalInterface`. Ejemplos típicos son `Runnable`, `Comparator` y `Predicate`. Son la base para el uso de lambdas.

---

## Interfaces Selladas (`sealed interface`)

Al igual que las clases, una interfaz puede restringir quién tiene permiso para implementarla:

```java
sealed interface Operacion permits Suma, Resta, Multiplicacion {}
record Suma(int a, int b) implements Operacion {}
```

> [!NOTE]
> Esto garantiza que el compilador conozca todas las posibles implementaciones, permitiendo la exhaustividad en expresiones `switch`.

---

## Abstracción: Clases Abstractas vs. Interfaces

| Característica | Clase Abstracta | Interfaz |
| :--- | :--- | :--- |
| **Herencia múltiple** | Solo una (`extends`) | Múltiple (`implements`) |
| **Constructor** | Sí | No |
| **Campos** | Instancia y estáticos | Solo constantes (`static final`) |
| **Métodos** | Abstractos y concretos | Abstractos, `default`, `static`, `private` |
| **Visibilidad** | Cualquier modificador | Públicos por defecto |
| **Sellado (`sealed`)** | Sí | Sí |

> [!TIP]
> Se prefiere una interfaz para definir contratos puros y una clase abstracta cuando se desea compartir estado (campos) o constructores comunes.

---

## Paradigma de Pattern Matching

La combinación de interfaces selladas, registros y el `switch` con patrones está cambiando el modelado del polimorfismo.

### Enfoque Clásico (Método Polimórfico)
```java
interface Figura {
    double area();
}
// Cada implementación define su propio area()
```

### Enfoque Moderno (Funcional/Centralizado)
```java
double area(Figura f) {
    return switch (f) {
        case Circulo c -> Math.PI * c.radio() * c.radio();
        case Rectangulo r -> r.ancho() * r.alto();
    };
}
```

> [!IMPORTANT]
> El enfoque clásico encapsula el comportamiento en la clase; el moderno centraliza las operaciones y aprovecha la potencia de los registros y patrones.

