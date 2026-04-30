# LAMBDAS
1. ¿Qué es una expresión lambda?

Una lambda es un bloque de código compacto que implementa el único método abstracto de una interfaz funcional. Permite tratar funciones como objetos y pasar comportamiento como parámetro.

Sintaxis general:
(parámetros) -> { cuerpo }

Variantes:

### Sin parámetros: () -> System.out.println("Hola")

### Un solo parámetro (paréntesis opcionales): x -> x * 2

### Varios parámetros: (a, b) -> a + b

### Cuerpo de varias líneas: (x, y) -> { int z = x + y; return z; }

Los tipos de los parámetros se pueden declarar explícitamente:
```java
(int a, int b) -> a + b
```

Normalmente se omiten y la JVM los infiere del contexto.
2. Interfaces funcionales

Una interfaz funcional es aquella que tiene exactamente un método abstracto (SAM – Single Abstract Method). Puede contener métodos default y static adicionales. Se recomienda anotarlas con @FunctionalInterface para que el compilador verifique la condición.
```java
@FunctionalInterface
public interface Operacion {
    int aplicar(int a, int b);
}
```

### Principales interfaces funcionales en java.util.function
Interfaz	Método abstracto	Descripción
Predicate<T>	boolean test(T t)	Evaluación booleana
Consumer<T>	void accept(T t)	Consume un valor sin retorno
Function<T,R>	R apply(T t)	Transforma un valor en otro
Supplier<T>	T get()	Provee un valor
UnaryOperator<T>	T apply(T t)	Function<T,T> especializado
BinaryOperator<T>	T apply(T t, T u)	BiFunction<T,T,T> especializado
BiPredicate<L,R>	boolean test(L l, R r)	Predicado de dos argumentos
BiConsumer<T,U>	void accept(T t, U u)	Consumidor de dos argumentos
BiFunction<T,U,R>	R apply(T t, U u)	Función de dos argumentos

Ejemplos de uso con lambdas:
```java
Predicate<String> isEmpty = s -> s.isEmpty();
Consumer<String> printer = s -> System.out.println(s);
Function<String, Integer> length = s -> s.length();
Supplier<Double> random = () -> Math.random();
BinaryOperator<Integer> sum = (a, b) -> a + b;
```

También existen especializaciones para tipos primitivos: IntPredicate, LongConsumer, DoubleFunction<R>, etc., que evitan el autoboxing.
3. Inferencia de tipos y “target typing”

El compilador decide qué interfaz funcional representa la lambda basándose en el contexto:

    Asignación a una variable del tipo de la interfaz.

    Paso como argumento a un método que espera dicha interfaz.

    Uso como valor de retorno donde se espera la interfaz.

    Cast explícito: (Predicate<String>) (s -> s.isEmpty()).

Es target typing: la lambda no tiene tipo por sí misma, lo adquiere del destino.
4. Captura de variables (closures)

Una lambda puede usar variables del ámbito envolvente. Las variables locales capturadas deben ser efectivamente finales (no modificadas después de inicializadas).
```java
String prefijo = "Sr. ";
Consumer<String> saludo = nombre -> System.out.println(prefijo + nombre);
// prefijo = "Sra. "; // error de compilación si se modifica
```

Las variables de instancia y estáticas no tienen esa restricción, porque se capturan por referencia al objeto (this).
5. La referencia this dentro de una lambda

Dentro de una lambda, this se refiere a la instancia de la clase que la contiene, no a la lambda en sí (que no tiene identidad propia). Es la misma semántica que una clase anónima.
```java
public class Ejemplo {
    private String nombre = "Ejemplo";
    public void probar() {
        Consumer<String> c = s -> System.out.println(this.nombre + " " + s);
        c.accept("prueba"); // imprime "Ejemplo prueba"
    }
}
```

### 6. Comparativa con clases anónimas
Característica	Lambda	Clase anónima
Ámbito de this	La clase contenedora	La propia clase anónima
Implementación interna	No genera un archivo .class aparte (usa invokedynamic y LambdaMetafactory)	Genera una clase separada al compilar
Obligatoriedad SAM	Solo interfaces funcionales	Interfaces y clases (incluso con varios métodos)
Uso de campos	No puede declarar campos propios	Puede declarar campos

Por rendimiento y limpieza, se prefieren lambdas cuando solo se necesita un SAM.
7. Usos prácticos

    Sustituir implementaciones verbosas de Comparator, Runnable, ActionListener, etc.

    Operaciones sobre colecciones con forEach, removeIf, replaceAll, sort.

### Crear hilos ligeros: new Thread(() -> { ... }).start();

    Construir flujos con la API Stream.

    Patrones de diseño como estrategia, command, observer mucho más concisos.

```java
// Ordenar con lambda
lista.sort((a, b) -> a.compareToIgnoreCase(b));
// Ejecutar tarea
Runnable tarea = () -> System.out.println("Ejecutando");
```

### 8. Excepciones en lambdas

Si el método abstracto de la interfaz funcional no declara excepciones comprobadas, la lambda no puede lanzarlas directamente. Soluciones:

    Capturarlas dentro de la lambda.

    Usar una interfaz funcional propia que declare la excepción.

    Envolver en una excepción no comprobada.

```java
// No compila: Runnable no lanza IOException
Runnable r = () -> { Files.lines(Path.of("noexiste")); };
// Opción: try-catch
Runnable r = () -> { try { Files.lines(...); } catch (IOException e) { ... } };
```

### 9. Buenas prácticas

    Pequeñas y autocontenidas: si crece más de 3-4 líneas, considerar un método con nombre.

    Evitar efectos laterales en lambdas usadas en streams (salvo forEach/peek para depuración).

    No abusar de la inferencia; a veces la legibilidad mejora explicitando el tipo en el parámetro.

    Preferir method reference cuando la lambda consista en la llamada directa a un método existente.
