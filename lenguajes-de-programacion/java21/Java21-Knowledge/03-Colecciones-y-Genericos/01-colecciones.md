# Colecciones

## 1. El Java Collections Framework (JCF)

El JCF es una arquitectura unificada para representar y manipular grupos de objetos. Proporciona:

- **Interfaces:** Tipos abstractos de datos que representan colecciones.
- **Implementaciones concretas:** Versiones usables de las interfaces.
- **Algoritmos:** Métodos para realizar operaciones como ordenación y búsqueda.

La raíz de la jerarquía es la interfaz `Collection<E>`, de la que derivan `List<E>`, `Set<E>` y `Queue<E>`. `Map<K,V>` no extiende `Collection` pero es parte fundamental del framework.

---

## 2. Interfaces principales y sus contratos

| Interfaz | Característica principal | Implementaciones típicas |
| :--- | :--- | :--- |
| **Collection** | Raíz de la jerarquía. | (No se implementa directamente) |
| **List** | Ordenada por índice, permite duplicados. | `ArrayList`, `LinkedList`, `Vector` (legacy) |
| **Set** | No permite duplicados, sin orden posicional definido. | `HashSet`, `LinkedHashSet`, `TreeSet` |
| **Queue** | Diseñada para procesar elementos en orden (FIFO). | `ArrayDeque`, `PriorityQueue`, `LinkedList` |
| **Deque** | Cola de doble extremo (Double Ended Queue). | `ArrayDeque`, `LinkedList` |
| **Map** | Asociación clave-valor, sin claves duplicadas. | `HashMap`, `LinkedHashMap`, `TreeMap` |

---

## 3. Implementaciones clave

- **ArrayList:** Array redimensionable. Acceso rápido por índice $O(1)$. Inserción/eliminación lenta en posiciones intermedias $O(n)$. Ideal para lectura intensiva.
- **LinkedList:** Lista doblemente enlazada. Inserciones/eliminaciones $O(1)$ en los extremos. Acceso por índice lento $O(n)$.
- **HashSet:** Basada en tabla hash. No garantiza orden. Operaciones básicas en $O(1)$ promedio.
- **LinkedHashSet:** Mantiene el orden de inserción mediante una lista enlazada interna.
- **TreeSet:** Almacena elementos en un árbol rojo-negro. Mantiene orden natural o definido por un `Comparator`. Operaciones en $O(\log n)$.
- **ArrayDeque:** Implementación de `Deque` más eficiente que `Stack` o `LinkedList`. No permite `null`.
- **PriorityQueue:** Cola con prioridad basada en un montículo (heap).
- **HashMap:** Tabla hash para pares clave-valor. $O(1)$ promedio. Permite `null`.
- **LinkedHashMap:** Mantiene el orden de inserción o de acceso.
- **TreeMap:** Almacena claves en un árbol para mantenerlas ordenadas.

---

## 4. Sequenced Collections (Java 21)

Java 21 introduce interfaces que definen un orden de encuentro explícito con operaciones sobre el primer y último elemento.

> [!NOTE]
> Estas interfaces son implementadas retroactivamente por las colecciones existentes que ya tenían un orden definido.

### Interfaces y Métodos
- **SequencedCollection<E>:** `addFirst()`, `addLast()`, `getFirst()`, `getLast()`, `removeFirst()`, `removeLast()`, `reversed()`.
- **SequencedSet<E>:** Hereda de `Set` y `SequencedCollection`.
- **SequencedMap<K,V>:** `putFirst()`, `putLast()`, `firstEntry()`, `lastEntry()`, `reversed()`, etc.

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

### Ejemplo de uso

```java
SequencedCollection<String> lista = new ArrayList<>();
lista.add("A"); lista.add("B"); lista.add("C");

System.out.println(lista.getFirst());  // A
System.out.println(lista.getLast());   // C

lista.addFirst("Inicio");
lista.addLast("Fin");
System.out.println(lista);             // [Inicio, A, B, C, Fin]

// Vista invertida
SequencedCollection<String> invertida = lista.reversed();
System.out.println(invertida.getFirst()); // Fin
```

---

## 5. Iteración y recorrido

1. **Bucle for-each:**
   ```java
   for (String s : collection) { ... }
   ```
2. **Iterador explícito:** `Iterator<E>`, permite eliminar elementos durante el recorrido.
3. **forEach (Java 8+):**
   ```java
   lista.forEach(System.out::println);
   ```
4. **Streams:** Procesamiento declarativo y funcional.

---

## 6. Ordenación

- **Comparable<T>:** La propia clase define su "orden natural" implementando `compareTo()`.
- **Comparator<T>:** Interfaz externa para definir múltiples criterios de ordenación.
- **Collections.sort():** Método de utilidad para ordenar listas.

---

## 7. Colecciones inmutables (Java 9+)

> [!TIP]
> Las colecciones inmutables son más seguras en entornos concurrentes y consumen menos memoria.

- **Fábricas:** `List.of()`, `Set.of()`, `Map.of()`.
- **Copias:** `List.copyOf()`, `Set.copyOf()`, `Map.copyOf()`.

---

## 8. Colecciones concurrentes

- **ConcurrentHashMap:** Mapa seguro para hilos de alto rendimiento.
- **CopyOnWriteArrayList:** Ideal para listas con muchas lecturas y pocas escrituras.
- **BlockingQueue:** Utilizada en patrones productor-consumidor.

---

## 9. Clases legacy (Evitar)

- **Vector:** Sustituir por `ArrayList`.
- **Stack:** Sustituir por `Deque` (`ArrayDeque`).
- **Hashtable:** Sustituir por `HashMap` o `ConcurrentHashMap`.

---

## 10. Ejemplo integrador (Java 21)

```java
public void procesarPedidos(SequencedCollection<Pedido> pedidos) {
    Pedido urgente = pedidos.getFirst(); 
    var reverso = pedidos.reversed();     
    reverso.forEach(p -> p.archivar());
}
```

---

[Anterior](../02-Programacion-Orientada-Objetos/README.md) | [Siguiente](./02-genericos.md)
