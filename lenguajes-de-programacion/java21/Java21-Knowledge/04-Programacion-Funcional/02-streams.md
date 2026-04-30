
# STREAMS
1. Concepto y estructura

Un Stream es una secuencia de elementos que soporta operaciones secuenciales y paralelas de forma agregada. No es una estructura de datos; es una vista sobre una fuente (colección, array, I/O, etc.) que se procesa de forma perezosa.

Un pipeline de stream consta de:

    Origen: de donde se obtienen los datos.

    Operaciones intermedias: cero o más, devuelven un nuevo Stream (encadenamiento). Son lazy.

    Operación terminal: produce un resultado o efecto secundario, y consume el stream (no se puede reutilizar).

2. Creación de streams

    Desde una colección: coleccion.stream() (secuencial) o coleccion.parallelStream().

    Desde arrays: Arrays.stream(array) o Stream.of(array).

    Desde valores sueltos: Stream.of("a", "b", "c").

    Generación infinita: Stream.iterate(valorInicial, unaryOperator), Stream.generate(supplier).

    Desde archivos: Files.lines(path) (devuelve Stream<String>).

    Desde números aleatorios: new Random().ints().

    Desde flujos de Optional (Java 9): optional.stream().

    Stream vacío: Stream.empty().

    Concatenar: Stream.concat(s1, s2).

```java
Stream<Integer> infinito = Stream.iterate(0, n -> n + 1); // peligro si no se limita
List<String> nombres = List.of("Ana", "Luis");
Stream<String> streamNombres = nombres.stream();
```

3. Operaciones intermedias
Operación	Descripción
filter(Predicate)	Retiene elementos que cumplan el predicado.
map(Function)	Transforma cada elemento en otro.
flatMap(Function)	Aplana cada elemento a un stream de varios y luego los concatena.
distinct()	Elimina duplicados según equals().
sorted()/sorted(Comparator)	Ordena los elementos (si son Comparable o con comparador).
peek(Consumer)	Ejecuta una acción por cada elemento (para depurar).
limit(long)	Trunca el stream a los primeros n elementos.
skip(long)	Omite los primeros n elementos.
takeWhile(Predicate) (Java 9+)	Toma elementos mientras se cumple el predicado, luego corta.
dropWhile(Predicate) (Java 9+)	Descarta mientras se cumple, luego deja pasar el resto.
mapMulti(BiConsumer) (Java 16+)	Similar a flatMap, pero evita crear streams intermedios para cada elemento.

Ejemplo:
```java
lista.stream()
     .filter(s -> s.length() > 3)
     .map(String::toUpperCase)
     .sorted()
     .distinct()
     .limit(10)
     .forEach(System.out::println);
```

Importante: las operaciones intermedias no se ejecutan hasta que se invoca una operación terminal.
4. Operaciones terminales

Se dividen en:
De transformación y búsqueda

    collect(Collector): acumula los elementos en una colección, mapa, cadena, etc.

    toList() (Java 16): devuelve una lista inmutable con los elementos.

    toArray(): array de Object o con IntFunction.

    reduce(identidad, BinaryOperator): reduce el stream a un solo valor.

    count(): número de elementos.

    min(Comparator), max(Comparator): devuelven Optional.

### De efecto colateral

    forEach(Consumer): aplica una acción a cada elemento. No garantiza orden en paralelo.

    forEachOrdered(Consumer): respeta el orden incluso en paralelo.

### De coincidencia

    anyMatch(Predicate): si algún elemento cumple → boolean.

    allMatch(Predicate): si todos cumplen.

    noneMatch(Predicate): si ninguno cumple.

### De consulta

    findFirst(): primer elemento, Optional.

    findAny(): cualquier elemento (en paralelo, puede ser cualquiera), Optional.

Ejemplos:
```java
List<String> filtrados = stream.collect(Collectors.toList());  // mutable
List<String> inmutables = stream.toList();                     // Java 16+, inmutable

long conteo = stream.filter(s -> s.startsWith("A")).count();
Optional<Integer> max = stream.map(String::length).max(Integer::compare);
boolean existe = stream.anyMatch(s -> s.isEmpty());
```

### 5. Collectors (coleccionistas)

La clase Collectors proporciona implementaciones de Collector para operaciones comunes:
Método	Resultado
toList()	ArrayList (mutable, no garantiza tipo)
toSet()	HashSet
toCollection(Supplier)	Colección especificada (p.ej. TreeSet::new)
toMap(keyMapper, valueMapper)	HashMap; cuidado con claves duplicadas
joining()	Concatena Strings
groupingBy(classifier)	Map<K, List<T>> agrupando por clave
partitioningBy(predicate)	Map<Boolean, List<T>>
summarizingInt()	Estadísticas (count, sum, min, average, max)
reducing()	Reducción generalizada
```java
Map<Integer, List<Persona>> porEdad = personas.stream()
    .collect(Collectors.groupingBy(Persona::edad));
String nombres = personas.stream()
    .map(Persona::nombre)
    .collect(Collectors.joining(", "));
```

### 6. Streams paralelos

Llamar a parallel() o usar parallelStream() hace que las operaciones se ejecuten en el ForkJoinPool común. Adecuado cuando la fuente es grande y las operaciones son costosas y sin efectos colaterales.

Precauciones:

    Las operaciones no deben depender del orden ni modificar estado mutable externo.

    El overhead de paralelización puede empeorar el rendimiento en streams pequeños.

    forEachOrdered puede perder paralelismo al imponer orden.

    Usar findAny en lugar de findFirst cuando el orden no importa, para aprovechar la concurrencia.

### 7. Streams de tipos primitivos

Para evitar el autoboxing existen IntStream, LongStream y DoubleStream. Métodos específicos:

    sum(), average(), min(), max(), summaryStatistics().

    Creación con range(), rangeClosed().

    Conversiones: stream.boxed() convierte a Stream de envoltorios; mapToInt, mapToObj, etc.

```java
int suma = IntStream.rangeClosed(1, 100).sum();
double promedio = IntStream.of(3,5,7).average().orElse(0);
```

### 8. Manejo de nulos

Java 9 introdujo Stream.ofNullable(valor) que devuelve un stream vacío si el valor es null, o un stream con el elemento en caso contrario.
```java
Stream<String> flujo = Stream.ofNullable(pais).flatMap(p -> obtenerEstadoStream(p));
```

### 9. mapMulti (Java 16)

Alternativa a flatMap para cuando la transformación produce cero, uno o unos pocos elementos, y no queremos crear un stream por cada entrada. Recibe un BiConsumer<T, Consumer<R>> y el consumidor acepta cada elemento producido.
```java
stream.mapMulti((String s, Consumer<Integer> sink) -> {
    if (!s.isEmpty()) {
        sink.accept(s.length());
    }
});
```

### 10. Novedades y buenas prácticas en Java 21

    La interfaz SequencedCollection permite obtener una vista invertida con reversed(). Al invocar stream() sobre esa vista, se obtiene un stream en orden inverso:

```java
sequencedList.reversed().stream().forEach(...);

    Preferir stream.toList() en lugar de collect(Collectors.toList()) cuando se desea una lista inmutable. Es más conciso y deja clara la inmutabilidad.

    Evitar operaciones terminales que produzcan efectos laterales (como forEach para poblar otra colección) dentro de streams paralelos si no es seguro.
```

    Utilizar takeWhile/dropWhile para streams ordenados cuando se necesita cortar o saltar con condiciones.

