# CONTROL DE FLUJO
4.1. Estructuras de decisión
if, else if, else

Evaluación condicional clásica:
```java
if (condicion) {
    // ...
} else if (otraCondicion) {
    // ...
} else {
    // ...
}
```

No hay tipo específico resultante. Las llaves son opcionales para una sola sentencia, pero se recomienda usarlas siempre.
4.2. switch – Tradicional, expresión y Pattern Matching (Java 21)

Java 21 convierte al switch en una herramienta potentísima. Veamos todas las formas.
4.2.1. switch clásico (sentencia)
```java
switch (variable) {
    case 1:
        System.out.println("Uno");
        break;
    case 2:
        System.out.println("Dos");
        break;
    default:
        System.out.println("Otro");
}
```

Sin break, hay fall-through (continúa el siguiente caso). Puede causar errores.
4.2.2. switch como expresión (Java 14+)

Devuelve un valor y usa la flecha -> para evitar break:
```java
int num = 2;
String texto = switch (num) {
    case 1 -> "Uno";
    case 2 -> "Dos";
    default -> "Otro";   // necesario si no se cubren todos los casos
};
```

Si un caso necesita un bloque de código, se usa yield para devolver el valor:
```java
String resultado = switch (num) {
    case 1 -> "Uno";
    case 2 -> {
        System.out.println("Procesando...");
        yield "Dos";
    }
    default -> "Otro";
};
```

La expresión es obligatoriamente exhaustiva (cubre todos los posibles valores del tipo). Para enum sin default se requieren todos los literales; con default no.
4.2.3. Pattern Matching for switch (Java 21 final)

Ahora el switch acepta patrones de tipo, de registro, de array y manejo explícito de null. La potencia se multiplica.
```java
Object obj = ...;
switch (obj) {
    case null -> System.out.println("Es nulo");
    case String s -> System.out.println("Cadena: " + s.toUpperCase());
    case Integer i -> System.out.println("Entero cuadrado: " + i * i);
    case int[] arr -> System.out.println("Array de enteros de longitud " + arr.length);
    default -> System.out.println("Tipo desconocido");
}
```

    El switch con patrones es exhaustivo para tipos sellados. Si la variable es una interfaz sellada como Figura, y cubrimos todos los permits, no se necesita default. Ejemplo con records y clases selladas:

```java
sealed interface Figura permits Circulo, Rectangulo, Triangulo {}
record Circulo(double radio) implements Figura {}
record Rectangulo(double ancho, double alto) implements Figura {}
record Triangulo(double base, double altura) implements Figura {}

static double area(Figura f) {
    return switch (f) {
        case Circulo(var r) -> Math.PI * r * r;
        case Rectangulo(var a, var h) -> a * h;
        case Triangulo(var b, var alt) -> b * alt / 2;
    };  // no requiere default porque la jerarquía es sellada
}
```

Observa el uso de record patterns: descomponen el registro dentro del case.

Además, los patrones pueden incluir cláusulas when (guardas) para añadir condiciones adicionales:
```java
switch (obj) {
    case String s when s.length() > 5 -> System.out.println("Cadena larga: " + s);
    case String s -> System.out.println("Cadena corta: " + s);
    ...
}
```

El orden importa: el caso más específico debe ir primero.
4.2.4. Manejo de null

En el switch clásico, pasar null lanza NullPointerException. Con pattern matching, si ponemos case null -> ... explícitamente, se maneja sin excepción. Si no se incluye ese caso y la variable puede ser nula, se lanzará NullPointerException. Es una mejora gigantesca en robustez.
4.3. Bucles
while
```java
while (condicion) {
    // cuerpo
}
```

### do-while
```java
do {
    // cuerpo
} while (condicion);
```

Ejecuta el bloque al menos una vez.
for clásico
```java
for (int i = 0; i < 10; i++) {
    // ...
}
```

Declaración/actualización de variable, condición e incremento. Se puede omitir cualquiera de las tres partes, pero los ; son obligatorios.
for mejorado (enhanced for-each)

Recorre arrays y cualquier objeto Iterable:
```java
for (String elemento : lista) {
    System.out.println(elemento);
}
```

No necesita índice. Desde Java 5. Internamente usa un iterador.
4.4. Sentencias de salto

    break → sale del bucle o del switch más interno.

    continue → salta a la siguiente iteración del bucle.

    return → sale del método y devuelve un valor si corresponde.

    yield (solo en switch expression) → devuelve un valor desde un bloque de caso.

### 4.5. Manejo de excepciones (control de flujo anómalo)

Las excepciones alteran el flujo normal. Java proporciona un manejo estructurado:
try-catch-finally
```java
try {
    // código que puede lanzar excepción
} catch (IOException e) {
    // manejo
} catch (SQLException | RuntimeException e) {  // multi-catch desde Java 7
    // maneja dos tipos
} finally {
    // se ejecuta siempre, haya o no excepción
}
```

El orden de los catch debe ser de más específica a más general.
try-with-resources (Java 7+)

Cierra automáticamente recursos que implementan AutoCloseable:
```java
try (var reader = new FileReader("archivo.txt")) {
    // usar reader
} // se cierra automáticamente al salir del bloque
```

### Excepciones comprobadas vs no comprobadas

    Comprobadas (herederas de Exception pero no de RuntimeException): obligan a manejarlas o declararlas con throws.

    No comprobadas (RuntimeException y sus hijas): no obligan a captura.

    Error y sus subclases: problemas graves de la JVM, normalmente no se capturan.

### 4.6. Control de flujo con Streams (adicional)

Aunque no es una estructura de control sintáctica, el API Stream (Java 8) ha cambiado la forma de iterar, filtrar y procesar colecciones:
```java
lista.stream()
     .filter(s -> s.length() > 3)
     .forEach(System.out::println);
```

Los streams usan operaciones intermedias (que devuelven stream) y terminales (que producen un resultado o efecto). Es un paradigma funcional que convive con los bucles clásicos.

Con esto completamos los cuatro pilares de la base sintáctica de Java 21.
Las nuevas posibilidades del switch con patrones, la inferencia con var, los registros y las clases selladas que vimos de pasada, y las mejoras en instanceof forman un conjunto sólido y moderno. Te recomiendo practicar cada apartado con pequeños programas para asimilar estos fundamentos antes de pasar a la Orientación a Objetos y las novedades avanzadas de concurrencia y rendimiento.
