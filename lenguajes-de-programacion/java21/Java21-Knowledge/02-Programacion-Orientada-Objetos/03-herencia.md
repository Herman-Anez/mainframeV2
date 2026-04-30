# HERENCIA
1. Concepto de herencia

La herencia permite que una clase (subclase) reutilice los campos y métodos de otra (superclase). Se declara con la palabra clave extends:
```java
public class Empleado extends Persona {
    private String empresa;
    public Empleado(String nombre, int edad, String empresa) {
        super(nombre, edad);
        this.empresa = empresa;
    }
}
```

En Java no existe herencia múltiple de clases; una clase solo puede tener una superclase directa. La herencia múltiple se simula mediante interfaces.
2. La clase Object

Todas las clases heredan implícitamente de java.lang.Object si no extienden otra clase. Object proporciona métodos como toString(), equals(), hashCode(), clone() y finalize() (obsoleto). Es la raíz de la jerarquía.
3. Uso de super

    super() llama al constructor de la superclase. Debe ser la primera instrucción.

    super.metodo() invoca un método de la superclase, útil cuando se sobrescribe.

### 4. Sobrescritura de métodos y anotación @Override

Una subclase puede redefinir un método de la superclase con la misma firma y tipo de retorno compatible (covarianza). Se recomienda usar @Override para que el compilador verifique que realmente se está sobrescribiendo.
```java
@Override
public String toString() {
    return nombre + " (" + edad + ")";
}
```

### 5. Modificador final en métodos y clases

    Método final: no puede ser sobrescrito por una subclase.

    Clase final: no puede ser extendida (p.ej. String, Integer, los record).

    Argumento final: la variable local no puede ser reasignada dentro del método.

### 6. Clases selladas (sealed / permits) – Java 17, estable en 21

Restringen explícitamente qué clases o interfaces pueden extender o implementar un tipo dado. Dan lugar a jerarquías controladas, ideales para la exhaustividad en el pattern matching.
```java
public sealed class Figura permits Circulo, Rectangulo, Triangulo {
    // ...
}
```

Las subclases permitidas deben estar en el mismo módulo o paquete, y a su vez pueden ser:

    final: no se puede extender más.

    sealed: siguen restringiendo.

    non-sealed: permiten extensión libre (de nuevo abierta).

Ejemplo completo:
```java
sealed class Figura permits Circulo, Rectangulo, Triangulo {}
final class Circulo extends Figura { ... }
non-sealed class Rectangulo extends Figura { ... }
sealed class Triangulo extends Figura permits TrianguloEquilatero {}
final class TrianguloEquilatero extends Triangulo {}
```

Los sealed combinados con records y el nuevo switch producen un polimorfismo por descomposición muy potente y seguro.
7. Jerarquías con registros sellados (patrón algebraico)

Es frecuente usar interfaces selladas implementadas por registros:
```java
sealed interface Expr permits Num, Suma, Resta {}
record Num(int valor) implements Expr {}
record Suma(Expr izq, Expr der) implements Expr {}
record Resta(Expr izq, Expr der) implements Expr {}
```

Esta codificación, típica de lenguajes funcionales, es ahora directa en Java y explota al máximo el pattern matching.
