# SEQUENCED COLLECTIONS (FINAL)

Las Secuenciated Collections son un conjunto de nuevas interfaces que aportan un contrato uniforme para colecciones con un orden de encuentro definido, permitiendo operar con el primer y el último elemento de manera directa y obtener una vista invertida. Afecta a List, SortedSet, LinkedHashSet, Deque, SortedMap y LinkedHashMap.
Nuevas interfaces en java.util

### SequencedCollection<E> extendiendo Collection<E>

### SequencedSet<E> extendiendo Set<E> y SequencedCollection<E>

### SequencedMap<K,V> extendiendo Map<K,V>

Todas las colecciones que ya tenían un orden (inserción o natural) han sido retroactivamente modificadas para implementar estas interfaces.
Métodos principales
SequencedCollection
```java
void    addFirst(E e)
void    addLast(E e)
E       getFirst()
E       getLast()
E       removeFirst()
E       removeLast()
SequencedCollection<E> reversed()   // vista invertida (no copia)
```

### SequencedSet

Hereda los mismos métodos y reversed() devuelve SequencedSet<E>.
SequencedMap
```java
V       putFirst(K k, V v)
V       putLast(K k, V v)
Entry<K,V> firstEntry()
Entry<K,V> lastEntry()
Entry<K,V> pollFirstEntry()
Entry<K,V> pollLastEntry()
SequencedMap<K,V> reversed()
SequencedSet<K> sequencedKeySet()
SequencedCollection<V> sequencedValues()
SequencedSet<Entry<K,V>> sequencedEntrySet()
```

### Ejemplos
```java
SequencedCollection<String> lista = new ArrayList<>();
lista.add("A"); lista.add("B"); lista.add("C");
System.out.println(lista.getFirst()); // A
System.out.println(lista.getLast());  // C
lista.addFirst("Inicio");
lista.addLast("Fin");
System.out.println(lista); // [Inicio, A, B, C, Fin]
```

### SequencedCollection<String> invertida = lista.reversed();
invertida.addFirst("Nuevo");       // modifica la original al final
System.out.println(lista.getLast()); // Nuevo

### SequencedMap<Integer, String> mapa = new LinkedHashMap<>();
mapa.put(1, "Uno"); mapa.put(2, "Dos"); mapa.put(3, "Tres");
System.out.println(mapa.firstEntry()); // 1=Uno
mapa.pollLastEntry();                  // elimina 3=Tres
for (var entry : mapa.reversed().entrySet()) {
    System.out.println(entry.getKey()); // 2, 1
}

### Beneficios

    Código más expresivo sin necesidad de list.get(list.size()-1) o list.get(0).

    La vista invertida facilita recorridos en orden inverso sin crear copias.

    Unificación de API: antes SortedSet y List tenían formas distintas de acceder a los extremos; ahora todas las colecciones ordenadas comparten el mismo contrato.

    Estado: Definitivo en Java 21. Listo para producción.

