# Control de Flujo

El control de flujo determina el orden en que se ejecutan las sentencias de un programa. Java 21 moderniza estas estructuras, especialmente el `switch`, convirtiéndolo en una herramienta extremadamente potente y robusta.

---

## Estructuras de decisión

### `if`, `else if`, `else`
Es la forma clásica de evaluación condicional.

```java
if (condicion) {
    // ...
} else if (otraCondicion) {
    // ...
} else {
    // ...
}
```

> [!TIP]
> Aunque las llaves `{}` son opcionales para bloques de una sola sentencia, se recomienda encarecidamente usarlas siempre para mejorar la legibilidad y evitar errores lógicos.

---

## `switch`: Tradicional, Expresión y Pattern Matching

Java 21 convierte al `switch` en una herramienta versátil.

### 1. `switch` clásico (Sentencia)
Funciona mediante etiquetas `case` y requiere el uso de `break` para evitar el *fall-through*.

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

### 2. `switch` como expresión (Java 14+)
Devuelve un valor directamente y utiliza la sintaxis de flecha (`->`), eliminando la necesidad de `break`.

```java
int num = 2;
String texto = switch (num) {
    case 1 -> "Uno";
    case 2 -> "Dos";
    default -> "Otro"; // Obligatorio si no se cubren todos los casos
};
```

> [!NOTE]
> Si un caso requiere un bloque de código, se utiliza la palabra clave `yield` para devolver el valor:
> ```java
> String resultado = switch (num) {
>     case 1 -> "Uno";
>     case 2 -> {
>         System.out.println("Procesando...");
>         yield "Dos";
>     }
>     default -> "Otro";
> };
> ```

### 3. Pattern Matching for `switch` (Java 21)
El `switch` ahora acepta patrones de tipo, registros, arrays y manejo explícito de `null`.

```java
Object obj = ...;
switch (obj) {
    case null -> System.out.println("Es nulo");
    case String s -> System.out.println("Cadena: " + s.toUpperCase());
    case Integer i -> System.out.println("Entero cuadrado: " + i * i);
    case int[] arr -> System.out.println("Array de longitud " + arr.length);
    default -> System.out.println("Tipo desconocido");
}
```

#### Exhaustividad y Clases Selladas
El `switch` con patrones es exhaustivo para tipos sellados. Si la variable es una interfaz sellada como `Figura`, y cubrimos todos los `permits`, no se necesita `default`.

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
    }; // No requiere default porque la jerarquía es sellada
}
```

#### Cláusulas `when` (Guardas)
Permiten añadir condiciones adicionales a los patrones:

```java
switch (obj) {
    case String s when s.length() > 5 -> System.out.println("Cadena larga: " + s);
    case String s -> System.out.println("Cadena corta: " + s);
    default -> {}
}
```

> [!IMPORTANT]
> **Orden de los casos:** El orden importa. El caso más específico debe ir siempre primero para evitar que sea "sombreado" por uno más general.

### 4. Manejo de `null`
En el `switch` clásico, pasar `null` lanza `NullPointerException`. Con pattern matching, si incluimos `case null -> ...` de forma explícita, el flujo se maneja de forma segura y robusta.

---

## Bucles

- **`while`**: Evalúa la condición antes del cuerpo.
- **`do-while`**: Ejecuta el bloque al menos una vez antes de evaluar la condición.
- **`for` clásico**: Declaración, condición e incremento.
- **`for-each` (Enhanced for)**: Recorre arrays y cualquier objeto `Iterable` sin necesidad de índices.

```java
for (String elemento : lista) {
    System.out.println(elemento);
}
```

---

## Sentencias de salto

- **`break`**: Sale del bucle o `switch` más interno.
- **`continue`**: Salta a la siguiente iteración del bucle.
- **`return`**: Sale del método devolviendo un valor.
- **`yield`**: Devuelve un valor desde un bloque de caso en un `switch expression`.

---

## Manejo de excepciones

Java proporciona un manejo estructurado para el control de flujo anómalo.

### `try-catch-finally`
```java
try {
    // Código propenso a excepciones
} catch (IOException e) {
    // Manejo
} catch (SQLException | RuntimeException e) { // Multi-catch (Java 7+)
    // Manejo de varios tipos
} finally {
    // Se ejecuta siempre (limpieza)
}
```

### `try-with-resources` (Java 7+)
Cierra automáticamente recursos que implementan `AutoCloseable`.

```java
try (var reader = new FileReader("archivo.txt")) {
    // Usar reader
} // Se cierra automáticamente al salir del bloque
```

### Tipos de excepciones
- **Comprobadas**: Obligan a ser capturadas o declaradas con `throws`.
- **No comprobadas (`RuntimeException`)**: No obligan a su captura.
- **Error**: Problemas graves de la JVM que normalmente no se capturan.

---

## Control de flujo con Streams (Paradigma Funcional)

El API Stream (Java 8) permite procesar colecciones de forma declarativa:

```java
lista.stream()
     .filter(s -> s.length() > 3)
     .forEach(System.out::println);
```

---

## Resumen

Con esto completamos los cuatro pilares de la base sintáctica de Java 21. La potencia del `switch` moderno, la inferencia con `var`, los registros y las clases selladas forman un conjunto sólido y profesional. Se recomienda practicar estos fundamentos antes de profundizar en la Orientación a Objetos avanzada.
