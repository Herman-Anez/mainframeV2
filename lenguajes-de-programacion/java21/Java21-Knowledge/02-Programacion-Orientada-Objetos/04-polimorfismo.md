# Polimorfismo

El polimorfismo es la capacidad de una variable de un tipo base para referirse a objetos de distintas subclases, asegurando que se ejecute la implementación correcta del método en tiempo de ejecución.

---

## Definición y Enlace Dinámico

Es la capacidad de una variable de un tipo base de referirse a objetos de distintas subclases y que la ejecución del método sobrescrito sea la correspondiente al objeto real. Este proceso se conoce como **enlace dinámico** (*dynamic binding*).

```java
Figura f = new Circulo(5.0);
double area = f.area(); // Se calcula el área del círculo, aunque la referencia sea de tipo Figura
```

---

## Sobrescritura vs. Sobrecarga

- **Sobrescritura (*Override*)**: Mismo método, misma firma, distinta implementación en la subclase. Se resuelve en **tiempo de ejecución**.
- **Sobrecarga (*Overload*)**: Mismo nombre de método pero diferentes parámetros. Se resuelve en **tiempo de compilación**.

---

## Covarianza en el Tipo de Retorno

En una sobrescritura se puede devolver un subtipo del tipo de retorno original definido en la superclase:

```java
@Override
public Circulo copia() { ... } // Si en Figura el método original devuelve Figura
```

---

## El operador `instanceof` con Pattern Matching (Java 16+)

Permite comprobar el tipo y vincular una variable directamente en una sola operación:

```java
if (f instanceof Circulo c) {
    System.out.println("Radio: " + c.radio());
}
```

> [!NOTE]
> Esto elimina la necesidad de realizar un casting manual posterior y reduce significativamente los errores en tiempo de ejecución.

---

## Polimorfismo con `switch` y Patrones (Java 21)

El `switch` ahora acepta patrones de tipo, de registro y de array. Es especialmente potente cuando se utiliza con tipos sellados, ya que se vuelve exhaustivo.

```java
public double area(Figura f) {
    return switch (f) {
        case Circulo(var r) -> Math.PI * r * r;
        case Rectangulo(var ancho, var alto) -> ancho * alto;
        case Triangulo(var base, var altura) -> base * altura / 2;
    };
}
```

> [!TIP]
> En este escenario, el polimorfismo se expresa mediante **descomposición** en lugar de métodos virtuales, aunque ambos enfoques coexisten perfectamente.

---

## Polimorfismo Paramétrico (Genéricos)

Los genéricos permiten escribir código que funciona de manera segura con distintos tipos de datos:

```java
List<String> nombres = new ArrayList<>();
```

---

## Métodos Virtuales en Java

En Java, todos los métodos de instancia que **no** sean `static` ni `private` son virtuales por defecto. Esto significa que su resolución se realiza de forma dinámica en tiempo de ejecución.

> [!IMPORTANT]
> Los métodos `static` y `private` no participan en el enlace dinámico; su resolución es estática en tiempo de compilación.
