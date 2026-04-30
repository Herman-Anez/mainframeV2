# REFERENCIAS A MÉTODOS
1. ¿Qué son?

Una referencia a método es una expresión lambda aún más compacta que indica exactamente qué método debe invocarse. Usa el operador :: y mejora la legibilidad cuando la lambda se limita a llamar a un método existente.
2. Los cuatro tipos de referencias a métodos
a) Referencia a un método estático

### Formato: Clase::metodoEstatico
Ejemplo: Integer::parseInt equivale a s -> Integer.parseInt(s)
```java
Function<String, Integer> parser = Integer::parseInt;
```

### b) Referencia a un método de instancia de un objeto particular

### Formato: instancia::metodo
Ejemplo: System.out::println equivale a x -> System.out.println(x)
```java
Consumer<String> impresora = System.out::println;
```

### c) Referencia a un método de instancia de cualquier objeto de un tipo dado

### Formato: Clase::metodoDeInstancia
El primer parámetro de la lambda se convierte en el receptor (objeto que invoca el método), y los siguientes (si los hay) se pasan como argumentos.
Ejemplo: String::toLowerCase equivale a (String s) -> s.toLowerCase()
```java
Function<String, String> minusculas = String::toLowerCase;
UnaryOperator<String> minusculasOp = String::toLowerCase;
```

Puede usarse con dos parámetros: String::concat equivale a (a, b) -> a.concat(b), es decir, BinaryOperator<String>.
d) Referencia a un constructor

### Formato: Clase::new
Equivale a una lambda que crea una nueva instancia. La interfaz funcional determina qué constructor se usa (por número de parámetros).

    ArrayList::new (sin argumentos) → Supplier<List<Integer>>, provee una lista vacía.

    Integer::new (con un int) → Function<String, Integer> no vale; pero IntFunction<int[]> int[]::new crea un array.

```java
Supplier<List<String>> proveedor = ArrayList::new;
Function<Integer, int[]> creadorArray = int[]::new;
```

3. Cómo se resuelve el método adecuado

La resolución sigue las mismas reglas de sobrecarga: la interfaz funcional determina el número y tipo de parámetros, y el compilador busca un método/constructor que coincida.

Ejemplo de sobrecarga exitosa:
```java
public class Ejemplo {
    public static void metodo(int x) { ... }
    public static void metodo(String s) { ... }
}
// En un contexto Predicate, ninguna es válida; en un Consumer<Integer> se resuelve al que acepta int.
```

### 4. Uso frecuente con streams

### stream.map(String::trim)

### stream.filter(Objects::nonNull)

### stream.forEach(System.out::println)

### stream.collect(Collectors.toCollection(ArrayList::new))

### stream.map(Persona::new) (constructor que toma los elementos como parámetro)

### 5. Referencia a métodos privados o de instancia

Se puede usar this::metodoPrivado para referenciar un método privado de la clase envolvente, y super::metodo para un método de la superclase.
```java
public class Procesador {
    private String limpiar(String s) { return s.trim(); }
    public void procesar(List<String> lista) {
        lista.stream().map(this::limpiar).forEach(System.out::println);
    }
}
```

### 6. Captura de excepciones

Si el método referenciado lanza excepciones comprobadas, la referencia a método hereda esa restricción y la interfaz funcional destino debe declararlas, o bien hay que adaptarla (envolviendo en un bloque try-catch o usando un hack con lanzamiento de excepciones no comprobadas). Es más difícil que con lambdas directamente; en la práctica se recurre a una lambda explícita cuando se necesita manejo de excepciones.
7. Comparación de legibilidad
Lambda	Referencia a método equivalente
x -> Math.abs(x)	Math::abs
s -> s.toLowerCase()	String::toLowerCase
(a, b) -> a.compareTo(b)	String::compareTo
() -> new ArrayList<>()	ArrayList::new
e -> System.out.println(e)	System.out::println

Usar referencias a métodos cuando el código ya está bien nombrado en el método referenciado; si necesitas un paso adicional o transformación previa, la lambda es más expresiva.
8. Limitaciones

    No se pueden referenciar métodos que requieran pasar el resultado de otra expresión compleja; la lambda sería necesaria (por ejemplo, x -> procesar(x, y) donde y es una variable capturada, no se puede escribir como procesar::? porque no hay forma de fijar el segundo argumento).

    Las referencias a métodos no pueden capturar variables para usarlas como argumentos adicionales, salvo que el receptor sea el primer parámetro (tipo 3) y el resto parámetros del método, lo que limita su flexibilidad.

