# INTERFACES Y ABSTRACCIÓN
1. Clases abstractas

Una clase declarada abstract no puede instanciarse directamente. Puede contener métodos abstractos (sin implementación, obligando a las subclases concretas a implementarlos) y métodos concretos. Ejemplo:
```java
public abstract class Animal {
    public abstract String sonido();
    public void dormir() {
        System.out.println("Zzz");
    }
}
```

2. Interfaces

Una interfaz es un contrato que define un conjunto de métodos (sin implementación por defecto, aunque ahora pueden tener métodos por defecto y estáticos). Una clase puede implementar múltiples interfaces:
```java
public class Perro implements Mascota, Carnivoro { ... }
```

Desde Java 8, las interfaces pueden incluir:

    Métodos default: con implementación por defecto, que pueden ser sobrescritos.

    Métodos static: métodos de utilidad propios de la interfaz.

    Desde Java 9: métodos private para compartir código entre métodos default/static.

3. Evolución de las interfaces (resumen)

    Java 8: métodos default y static.

    Java 9: métodos private.

    Java 17/21: interfaces selladas (sealed interface) y el uso de patrones en switch sobre ellas.

### 4. Interfaces funcionales

Son interfaces con un único método abstracto (SAM). Se anotan con @FunctionalInterface. Por ejemplo, Runnable, Comparator, Predicate. Pueden ser implementadas mediante lambdas o referencias a métodos.
5. Interfaces selladas (sealed interface)

Al igual que las clases, una interfaz puede restringir quién la implementa:
```java
sealed interface Operacion permits Suma, Resta, Multiplicacion {}
record Suma(int a, int b) implements Operacion {}
```

Esto garantiza que, al analizar un objeto de tipo Operacion, el compilador conozca todas las posibles implementaciones y pueda exigir exhaustividad en el switch.
6. Abstracción con clases abstractas vs. interfaces
Característica	Clase Abstracta	Interfaz
Herencia múltiple	Solo una (extends)	Múltiple (implements)
Constructor	Sí	No
Campos	De instancia y estáticos	Solo constantes (static final)
Métodos	Abstractos y concretos	Abstractos, default, static, private
Visibilidad	Cualquier modificador	Métodos son públicos por defecto
Sellado (sealed)	Sí	Sí

Normalmente se prefiere interfaz para definir contratos puros, y clase abstracta cuando se desea compartir estado (campos) o constructores.
7. Herencia de tipo y herencia de implementación

    Las interfaces proporcionan herencia de tipo sin forzar una implementación concreta.

    Las clases abstractas permiten reutilizar código (herencia de implementación), pero en Java moderno se tiende a preferir composición sobre herencia profunda.

### 8. Nuevo paradigma con pattern matching

La combinación de interfaces selladas, registros y el switch con patrones está cambiando la forma de modelar el polimorfismo. Anteriormente se escribía un método abstracto en la interfaz y se implementaba en cada clase; ahora se puede usar un método estático con un switch exhaustivo sobre el tipo sellado. Ambas aproximaciones son válidas y se complementan.

Ejemplo clásico (método polimórfico):
```java
interface Figura {
    double area();
}
// cada implementación define area()
```

Ejemplo funcional (externo):
```java
double area(Figura f) {
    return switch (f) {
        case Circulo c -> Math.PI * c.radio() * c.radio();
        case Rectangulo r -> r.ancho() * r.alto();
    };
}
```

La primera encapsula cada comportamiento en su clase; la segunda centraliza operaciones y puede aprovecharse mejor con registros y patrones.

