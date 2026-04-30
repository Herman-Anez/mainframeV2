# Lambdas

## 1. ¿Qué es una expresión lambda?

Una lambda es un bloque de código compacto que implementa el único método abstracto de una interfaz funcional. Permite tratar funciones como objetos y pasar comportamiento como parámetro.

### Sintaxis general
```java
(parámetros) -> { cuerpo }
```

### Variantes de sintaxis
- **Sin parámetros:** `() -> System.out.println("Hola")`
- **Un solo parámetro:** `x -> x * 2` (los paréntesis son opcionales).
- **Varios parámetros:** `(a, b) -> a + b`
- **Cuerpo multilinea:** `(x, y) -> { int z = x + y; return z; }`

---

## 2. Interfaces funcionales

Una interfaz funcional es aquella que tiene **exactamente un método abstracto** (SAM – Single Abstract Method). Puede contener métodos `default` y `static`.

> [!TIP]
> Se recomienda usar la anotación `@FunctionalInterface` para que el compilador valide que la interfaz cumple con la condición de ser funcional.

### Principales interfaces en `java.util.function`

| Interfaz | Método abstracto | Descripción |
| :--- | :--- | :--- |
| **Predicate<T>** | `boolean test(T t)` | Evaluación booleana. |
| **Consumer<T>** | `void accept(T t)` | Consume un valor sin retorno. |
| **Function<T, R>** | `R apply(T t)` | Transforma un valor en otro. |
| **Supplier<T>** | `T get()` | Provee un valor. |
| **UnaryOperator<T>** | `T apply(T t)` | Función donde entrada y salida son del mismo tipo. |
| **BinaryOperator<T>** | `T apply(T t, T u)` | Operación con dos argumentos del mismo tipo. |

---

## 3. Inferencia de tipos y "Target Typing"

El compilador decide qué interfaz funcional representa la lambda basándose en el contexto (**Target Typing**). La lambda no tiene un tipo por sí misma; lo adquiere del destino:
- Asignación a una variable.
- Paso como argumento a un método.
- Valor de retorno.
- Cast explícito.

---

## 4. Captura de variables (Closures)

Una lambda puede usar variables del ámbito envolvente. Sin embargo, las variables locales capturadas deben ser **efectivamente finales** (no modificadas tras su inicialización).

```java
String prefijo = "Sr. ";
Consumer<String> saludo = nombre -> System.out.println(prefijo + nombre);
// prefijo = "Sra. "; // Error: la variable capturada debe ser final.
```

> [!NOTE]
> Las variables de instancia y estáticas no tienen esta restricción, ya que se capturan por referencia al objeto (`this`).

---

## 5. La referencia `this` dentro de una lambda

Dentro de una lambda, `this` se refiere a la instancia de la clase que la contiene, no a la lambda en sí. Esto se debe a que la lambda no define un nuevo ámbito de instancia.

```java
public class Ejemplo {
    private String nombre = "Ejemplo";
    public void probar() {
        Consumer<String> c = s -> System.out.println(this.nombre + " " + s);
        c.accept("prueba"); // Imprime "Ejemplo prueba"
    }
}
```

---

## 6. Comparativa con clases anónimas

| Característica | Lambda | Clase anónima |
| :--- | :--- | :--- |
| **Ámbito de `this`** | Clase contenedora. | La propia clase anónima. |
| **Implementación** | `invokedynamic` (sin `.class` extra). | Genera un archivo `.class` separado. |
| **Restricción** | Solo interfaces funcionales (SAM). | Interfaces y clases (varios métodos). |
| **Campos** | No puede declarar campos propios. | Puede tener campos y estado. |

---

## 7. Usos prácticos

- **Ordenación:** `lista.sort((a, b) -> a.compareTo(b));`
- **Hilos:** `new Thread(() -> { ... }).start();`
- **Colecciones:** `lista.forEach(System.out::println);`
- **Streams:** Base para el procesamiento fluido de datos.

---

## 8. Excepciones en lambdas

Si el método de la interfaz funcional no declara excepciones comprobadas, la lambda no puede lanzarlas directamente.

### Soluciones:
1. Capturarlas con `try-catch` dentro de la lambda.
2. Envolverlas en una `RuntimeException`.
3. Usar interfaces funcionales personalizadas que declaren excepciones.

```java
// Opción: try-catch interno
Runnable r = () -> {
    try {
        Files.lines(Path.of("archivo.txt"));
    } catch (IOException e) {
        throw new UncheckedIOException(e);
    }
};
```

---

## 9. Buenas prácticas

- **Concisión:** Si una lambda supera las 3-4 líneas, considera extraerla a un método con nombre.
- **Efectos laterales:** Evita modificar estado externo dentro de lambdas (especialmente en streams).
- **Method References:** Prefiere referencias a métodos (`System.out::println`) sobre lambdas equivalentes (`s -> System.out.println(s)`).

---

[Anterior](../03-Colecciones-y-Genericos/03-optional.md) | [Siguiente](./02-streams.md)
