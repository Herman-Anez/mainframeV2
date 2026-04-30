# POLIMORFISMO
1. Definición de polimorfismo

Capacidad de una variable de un tipo base de referirse a objetos de distintas subclases y que la ejecución del método sobrescrito sea la correspondiente al objeto real (enlace dinámico o dynamic binding).
```java
Figura f = new Circulo(5.0);
double area = f.area(); // área del círculo, aunque el tipo de referencia sea Figura
```

2. Sobrescritura vs. Sobrecarga

    Sobrescritura (override): mismo método, misma firma, distinta implementación en subclase. Se resuelve en tiempo de ejecución.

    Sobrecarga (overload): mismo nombre de método pero diferentes parámetros. Se resuelve en compilación.

3. Covarianza en el tipo de retorno

En una sobrescritura se puede devolver un subtipo del tipo de retorno original:
```java
@Override
public Circulo copia() { ... } // si en Figura el método devuelve Figura
```

### 4. El operador instanceof con pattern matching (Java 16+)

Permite comprobar el tipo y vincular una variable en una sola operación:
```java
if (f instanceof Circulo c) {
    System.out.println("Radio: " + c.radio());
}
```

Elimina la necesidad de un casting posterior y reduce errores. Es una forma de polimorfismo condicional.
5. Polimorfismo con switch y patrones (Java 21)

El switch ahora acepta patrones de tipo, de registro y de array, y es exhaustivo con tipos sellados, convirtiéndolo en una potente herramienta de despacho múltiple.
```java
public double area(Figura f) {
    return switch (f) {
        case Circulo(var r) -> Math.PI * r * r;
        case Rectangulo(var ancho, var alto) -> ancho * alto;
        case Triangulo(var base, var altura) -> base * altura / 2;
    };
}
```

Aquí, el polimorfismo se expresa mediante descomposición en lugar de métodos virtuales, aunque ambos coexisten.
6. Polimorfismo paramétrico (genéricos)

Los genéricos permiten escribir código que funciona con distintos tipos:
```java
List<String> nombres = new ArrayList<>();
```

El compilador garantiza la seguridad de tipos en tiempo de compilación. Es otra forma de polimorfismo (universal).
7. Métodos virtuales en Java

Todos los métodos de instancia no static ni private son virtuales por defecto, es decir, se resuelven dinámicamente. Únicamente los métodos static y private no participan en el enlace dinámico.
