# UNNAMED PATTERNS AND VARIABLES (PREVIEW)

Los Patrones y Variables sin nombre permiten usar el carácter _ para declarar variables o componentes de patrón cuyo valor no se necesita, mejorando la legibilidad y reduciendo advertencias.
Unnamed variable (_)

En cualquier lugar donde se declare una variable local, parámetro de lambda o catch, se puede usar _ si el valor no se usa:
```java
try (var _ = ScopedValue.where(FLAG, true)) {
    // No necesitamos la variable del scope auto-closeable
}

// En un catch
try { ... } catch (Exception _) {
    // No nos interesa la excepción concreta
}

// En lambdas
lista.stream().collect(Collectors.toMap(k -> k, _ -> 1)); // el valor no importa

// En bucles for-each
for (var _ : lista) {
    // solo interesa contar iteraciones
}
```

El compilador no emite advertencias por no uso, y la variable no consume memoria significativa.
Unnamed patterns (_)

En patrones de registro o de switch, se puede usar _ para componentes que no interesan:
```java
record Rectangulo(double ancho, double alto) {}
if (figura instanceof Rectangulo(double _, double alto)) {
    System.out.println("Alto: " + alto);
}

switch (figura) {
    case Rectangulo(var _, var alto) -> "Alto: " + alto;
    ...
}
```

También se puede usar en patrones de registro anidados: Segmento(Punto(_, _), Punto(var x, var y)).
Unnamed pattern en case

En un switch, un pattern _ puede funcionar como default pero capturando cualquier valor sin vincular la variable:
```java
case _ -> System.out.println("Caso por defecto");
```

A diferencia de default, _ es un patrón que coincide con todo, y si hay varios case _, se aplica el orden.
Beneficios

    Claridad: se documenta explícitamente que el valor no se usa.

    Menos contaminación del espacio de nombres.

    Mejora en las revisiones de código.

    Estado: Preview en Java 21. Habilitar con --enable-preview.
