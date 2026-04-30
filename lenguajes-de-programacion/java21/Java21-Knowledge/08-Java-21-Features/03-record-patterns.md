# 🧩 Record Patterns

Los **Record Patterns** permiten descomponer un registro en sus componentes directamente después de una comprobación de tipo, ya sea en un `instanceof` o en un `case` de un `switch`. Se basa en los registros y el *pattern matching* ya existente.

---

## 🔍 Uso en `instanceof`

```java
record Punto(double x, double y) {}

void imprimir(Object obj) {
    if (obj instanceof Punto(double x, double y)) {
        System.out.println("Coordenadas: " + x + ", " + y);
    }
}
```

> [!NOTE]
> La variable `x` e `y` se vinculan directamente a los componentes del registro, con su tipo inferido.

---

## 🔄 Uso en `switch`

```java
sealed interface Figura permits Circulo, Rectangulo {}
record Circulo(double radio) implements Figura {}
record Rectangulo(double ancho, double alto) implements Figura {}

double area(Figura f) {
    return switch (f) {
        case Circulo(var r) -> Math.PI * r * r;
        case Rectangulo(var a, var h) -> a * h;
    };
}
```

> [!TIP]
> `var r` equivale a `double r`, pero también se puede poner el tipo explícito.

---

## 🏗️ Patrones anidados

Se pueden descomponer registros dentro de registros:

```java
record Punto(double x, double y) {}
record Segmento(Punto inicio, Punto fin) {}

if (s instanceof Segmento(Punto(var x1, var y1), Punto(var x2, var y2))) {
    // uso directo de x1, y1, x2, y2
}
```

La legibilidad y la seguridad de tipos aumentan drásticamente.

---

## 🛠️ Características adicionales

### `when` clauses (guardas)
No hay guardas en `instanceof` (se usa `&&` adicional), pero en el `switch` los patrones de registro pueden combinarse con `when` (parte del *pattern matching* del `switch`) para refinar el caso.

### Exhaustividad con tipos sellados
Cuando se usan registros que implementan interfaces selladas, el compilador asegura que el `switch` cubra todos los casos, y los patrones de registro permiten extraer la información de golpe.

> [!IMPORTANT]
> **Estado:** Definitivo en Java 21. Es la culminación del *pattern matching* estructural.

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../../README.md)
- [☕ Java 21 Index](../../../index.md)

