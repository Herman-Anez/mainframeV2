# Streams

## 1. Concepto y estructura

Un Stream es una secuencia de elementos que soporta operaciones secuenciales y paralelas de forma agregada. No es una estructura de datos; es una **vista** sobre una fuente (colección, array, I/O, etc.) que se procesa de forma perezosa (**lazy**).

### Un pipeline de stream consta de:
1. **Origen:** De donde se obtienen los datos.
2. **Operaciones intermedias:** Devuelven un nuevo Stream. Son perezosas y permiten el encadenamiento.
3. **Operación terminal:** Produce un resultado o efecto secundario, consume el stream y lo cierra.

---

## 2. Creación de streams

- **Desde colecciones:** `lista.stream()` o `lista.parallelStream()`.
- **Desde arrays:** `Arrays.stream(miArray)` o `Stream.of(miArray)`.
- **Desde valores sueltos:** `Stream.of("a", "b", "c")`.
- **Generación infinita:** `Stream.iterate(0, n -> n + 1)` o `Stream.generate(Math::random)`.
- **Desde archivos:** `Files.lines(path)` (devuelve `Stream<String>`).
- **Nulos (Java 9+):** `Stream.ofNullable(valor)`.

```java
Stream<Integer> infinito = Stream.iterate(0, n -> n + 1).limit(10);
List<String> nombres = List.of("Ana", "Luis");
Stream<String> streamNombres = nombres.stream();
```

---

## 3. Operaciones intermedias

| Operación | Descripción |
| :--- | :--- |
| **filter(Predicate)** | Retiene elementos que cumplen la condición. |
| **map(Function)** | Transforma cada elemento en otro. |
| **flatMap(Function)** | "Aplana" streams anidados en uno solo. |
| **distinct()** | Elimina duplicados según `equals()`. |
| **sorted()** | Ordena según orden natural o un `Comparator`. |
| **peek(Consumer)** | Ejecuta una acción por elemento (ideal para depurar). |
| **limit(long)** | Trunca el stream a los primeros $n$ elementos. |
| **skip(long)** | Omite los primeros $n$ elementos. |
| **takeWhile(Predicate)** | Toma elementos mientras se cumpla la condición (Java 9+). |
| **dropWhile(Predicate)** | Descarta elementos mientras se cumpla la condición (Java 9+). |

> [!IMPORTANT]
> Las operaciones intermedias no se ejecutan hasta que se invoca una operación terminal (**Lazy evaluation**).

---

## 4. Operaciones terminales

### De transformación y búsqueda
- **collect(Collector):** Acumula elementos en colecciones, mapas, etc.
- **toList() (Java 16+):** Devuelve una lista inmutable de forma concisa.
- **reduce(BinaryOperator):** Reduce el stream a un único valor.
- **count():** Devuelve el número de elementos.
- **min/max(Comparator):** Devuelven un `Optional` con el valor extremo.

### De coincidencia y consulta
- **anyMatch/allMatch/noneMatch:** Verificaciones booleanas sobre el contenido.
- **findFirst/findAny:** Devuelven un `Optional` con un elemento del stream.

### De efecto colateral
- **forEach(Consumer):** Aplica una acción a cada elemento.
- **forEachOrdered(Consumer):** espeta el orden incluso en paralelo.

### De coincidencia

- **anyMatch(Predicate):**  si algún elemento cumple → boolean.

- **allMatch(Predicate):**  si todos cumplen.

- **noneMatch(Predicate):**  si ninguno cumple.

### De consulta

- **findFirst():**  primer elemento, Optional.

- **findAny():**  cualquier elemento (en paralelo, puede ser cualquiera), Optional.

Ejemplos:
```java
List<String> filtrados = stream.collect(Collectors.toList());  // mutable
List<String> inmutables = stream.toList();                     // Java 16+, inmutable

long conteo = stream.filter(s -> s.startsWith("A")).count();
Optional<Integer> max = stream.map(String::length).max(Integer::compare);
boolean existe = stream.anyMatch(s -> s.isEmpty());
```

```java
List<String> inmutables = stream.filter(s -> s.length() > 3)
                                .map(String::toUpperCase)
                                .toList();
```

---

## 5. Collectors

La clase `Collectors` proporciona implementaciones listas para usar con `collect()`:

| Método | Resultado |
| :--- | :--- |
| **toList() / toSet()** | Crea una lista o conjunto mutable. |
| **toCollection(Supplier)** | Permite especificar la implementación (ej. `TreeSet::new`). |
| **toMap(K, V)** | Crea un mapa a partir de los elementos. |
| **joining(delimiter)** | Concatena Strings con un delimitador. |
| **groupingBy(classifier)** | Agrupa elementos en un `Map<K, List<T>>`. |
| **partitioningBy(predicate)** | Divide en dos grupos (true/false). |
| **summarizingInt()** | Calcula estadísticas (sum, avg, min, max, count). |

---

## 6. Streams paralelos

Al usar `parallelStream()`, el stream se divide y procesa en múltiples hilos usando el `ForkJoinPool` común.

> [!WARNING]
> - Úsalo solo para fuentes grandes y operaciones costosas.
> - Asegúrate de que las operaciones sean libres de efectos secundarios (**stateless**).
> - Evita modificar estado compartido.

---

## 7. Streams de tipos primitivos

Para evitar el coste del autoboxing, utiliza versiones especializadas:
- **IntStream, LongStream, DoubleStream.**
- Métodos extra: `sum()`, `average()`, `range()`, `rangeClosed()`.
- Conversión: `stream.boxed()` para volver a `Stream<Wrapper>`.

```java
int suma = IntStream.rangeClosed(1, 100).sum();
```

---

## 8. mapMulti (Java 16)

Alternativa a `flatMap` para cuando la transformación produce pocos elementos, evitando la creación de streams intermedios por cada entrada.

```java
stream.mapMulti((String s, Consumer<Integer> sink) -> {
    if (!s.isEmpty()) sink.accept(s.length());
});
```

---

## 9. Novedades y buenas prácticas (Java 21)

- **Sequenced Streams:** Al usar `reversed().stream()` en una `SequencedCollection`, se procesan los elementos en orden inverso automáticamente.
- **Inmutabilidad:** Prefiere `stream.toList()` sobre `collect(Collectors.toList())` si no necesitas modificar la lista resultante.
- **Claridad:** Usa `takeWhile` / `dropWhile` en lugar de filtros complejos cuando el stream está ordenado.

---

[Anterior](./01-lambdas.md) | [Siguiente](./03-method-references.md)
