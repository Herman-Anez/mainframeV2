# COLECCIONES
1. El Java Collections Framework (JCF)

El JCF es una arquitectura unificada para representar y manipular grupos de objetos. Proporciona:

### Interfaces (tipos abstractos de datos)

### Implementaciones concretas

### Algoritmos (ordenación, búsqueda, etc.)

La raíz de la jerarquía es la interfaz Collection<E>, de la que derivan List<E>, Set<E> y Queue<E>. Map<K,V> no extiende Collection pero es parte del framework.
2. Interfaces principales y sus contratos
Interfaz	Característica principal	Implementaciones típicas
Collection	Grupo de elementos	(no se implementa directamente)
List	Ordenada por índice, permite duplicados	ArrayList, LinkedList, Vector(legacy)
Set	No duplicados, sin orden definido por posición	HashSet (sin orden), LinkedHashSet (orden inserción), TreeSet (orden natural/comparator)
Queue	Diseñada para contener elementos antes de procesarlos	ArrayDeque, PriorityQueue, LinkedList
Deque	Cola de doble extremo (hereda de Queue)	ArrayDeque, LinkedList
Map	Asociación clave-valor, sin claves duplicadas	HashMap (sin orden), LinkedHashMap (orden inserción/acceso), TreeMap (orden natural/comparator)
3. Implementaciones clave

    ArrayList: array redimensionable, acceso rápido por índice O(1), inserción/eliminación lenta al inicio o en medio O(n). Ideal para lectura intensiva y recorrido.

    LinkedList: lista doblemente enlazada, inserciones/eliminaciones O(1) en extremos y con iterador, acceso por índice O(n). Útil cuando se necesita añadir/quitar frecuentemente en cualquier posición.

    HashSet: implementación de Set basada en HashMap. No garantiza orden. O(1) para add, remove, contains.

    LinkedHashSet: mantiene el orden de inserción, ligera penalización de rendimiento.

    TreeSet: SortedSet basado en árbol rojo-negro. Ordena los elementos según su orden natural (Comparable) o un Comparator. O(log n).

    ArrayDeque: implementación de Deque más eficiente que Stack y LinkedList para uso como cola o pila. No permite elementos null.

    PriorityQueue: cola que ordena los elementos según su orden natural o comparator. El elemento más prioritario es el de menor valor según ese orden.

    HashMap: tabla hash. O(1) promedio. Permite claves null y valores null. Poco adecuado para ordenación.

    LinkedHashMap: HashMap que mantiene lista doblemente enlazada conservando el orden de inserción o de acceso.

    TreeMap: SortedMap basado en árbol rojo‑negro. Ordena las claves.

### 4. Sequenced Collections (novedad estable en Java 21)

Java 21 introduce tres nuevas interfaces que definen un orden de encuentro explícito con operaciones sobre el primer y último elemento, y acceso a una vista invertida:

### SequencedCollection<E> (hereda de Collection)

### SequencedSet<E> (hereda de Set y SequencedCollection)

### SequencedMap<K,V> (hereda de Map)

Estas interfaces son implementadas retroactivamente por las colecciones existentes que ya tenían un orden definido (por inserción, natural, etc.).

Métodos principales:
```java
// SequencedCollection
void addFirst(E e)
void addLast(E e)
E getFirst()
E getLast()
E removeFirst()
E removeLast()
SequencedCollection<E> reversed()   // vista invertida

// SequencedSet extiende con los mismos métodos, plus reversed() devuelve SequencedSet<E>
// SequencedMap
V putFirst(K k, V v)
V putLast(K k, V v)
Entry<K,V> firstEntry()
Entry<K,V> lastEntry()
Entry<K,V> pollFirstEntry()
Entry<K,V> pollLastEntry()
SequencedMap<K,V> reversed()
SequencedSet<K> sequencedKeySet()
SequencedCollection<V> sequencedValues()
SequencedSet<Entry<K,V>> sequencedEntrySet()
```

¿Quién implementa qué?

### List (ArrayList, LinkedList) → SequencedCollection

### SortedSet (TreeSet) y LinkedHashSet → SequencedSet

### Deque (ArrayDeque, LinkedList) → SequencedCollection

### SortedMap (TreeMap) y LinkedHashMap → SequencedMap

Ejemplos prácticos:
```java
SequencedCollection<String> lista = new ArrayList<>();
lista.add("A"); lista.add("B"); lista.add("C");
System.out.println(lista.getFirst());  // A
System.out.println(lista.getLast());   // C
lista.addFirst("Inicio");
lista.addLast("Fin");
System.out.println(lista);             // [Inicio, A, B, C, Fin]
```

### SequencedCollection<String> invertida = lista.reversed();
System.out.println(invertida.getFirst()); // Fin
invertida.addFirst("Nuevo"); // afecta a la vista, pero modifica la colección original al final
System.out.println(lista.getLast()); // Nuevo

Con SequencedMap:
```java
SequencedMap<Integer, String> map = new LinkedHashMap<>();
map.put(1, "Uno"); map.put(2, "Dos"); map.put(3, "Tres");
System.out.println(map.firstEntry());  // 1=Uno
map.pollLastEntry();                   // elimina y devuelve 3=Tres
for (var entry : map.reversed().entrySet()) {
    System.out.println(entry.getKey());
}
```

Estas adiciones simplifican enormemente el código que antes requería iteradores o casteos a implementaciones concretas.
5. Iteración y recorrido

### Bucle for‑each: for (String s : collection)

    Iterador explícito: Iterator<E>, permite eliminar durante el recorrido con remove().

### forEach(Consumer) (Java 8): lista.forEach(System.out::println)

    Spliterator para paralelismo y streams.

    Streams (Java 8+): lista.stream().filter(...).collect(toList()) (explicado en programación funcional).

### 6. Ordenación

    Comparable<T>: la clase implementa compareTo(T o). Define el orden natural.

    Comparator<T>: interfaz externa con compare(T o1, T o2). Multitud de métodos default (reversed(), thenComparing(), comparingInt(), etc.)

    Métodos útiles en Collections: sort(), reverseOrder().

    SortedSet/SortedMap requieren Comparator o elementos Comparable.

### 7. Colecciones inmutables (Java 9+)

    Fábricas: List.of(...), Set.of(...), Map.of(key,value,...), Map.ofEntries(...). Devuelven colecciones inmutables (no se pueden modificar, ni siquiera con iterador.remove). Lanzan UnsupportedOperationException si se intenta modificar.

    Copias inmutables: List.copyOf(collection), Set.copyOf(), Map.copyOf() (Java 10+). Si la colección de origen ya es inmutable, la devuelve sin copiar.

    Colecciones no modificables tradicionales: Collections.unmodifiableList(...) envuelven una colección mutable pero impiden modificaciones a través de la vista. La colección subyacente puede cambiar si se modifica directamente.

### 8. Colecciones concurrentes

    ConcurrentHashMap: mapa thread‑safe de alto rendimiento.

    CopyOnWriteArrayList/CopyOnWriteArraySet: útiles cuando las lecturas dominan sobre las escrituras.

    BlockingQueue (ArrayBlockingQueue, LinkedBlockingQueue) para productores/consumidores.

    ConcurrentSkipListMap/Set: implementaciones concurrentes de SortedMap/SortedSet.

### 9. Clases legacy y obsoletas

    Vector → sustituir por ArrayList (y sincronizar externamente si es necesario).

    Stack → Deque (con ArrayDeque), métodos push/pop.

    Hashtable → HashMap o ConcurrentHashMap.

    Enumeration → Iterator.

### 10. Ejemplo integrador con secuencias (Java 21)
```java
public void procesarPedidos(SequencedCollection<Pedido> pedidos) {
    Pedido urgente = pedidos.getFirst();  // antes: pedidos.get(0)
    // despachar urgente...
    var reverso = pedidos.reversed();     // vista invertida
    reverso.forEach(p -> p.archivar());
}
```

