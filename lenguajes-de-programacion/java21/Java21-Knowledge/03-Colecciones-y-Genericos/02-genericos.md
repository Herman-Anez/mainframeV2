# GENÉRICOS
1. Motivación y beneficios

Los genéricos permiten que una clase, interfaz o método opere sobre un tipo que se especifica como parámetro. Aportan:

    Seguridad de tipos en tiempo de compilación.

    Eliminación de casteos manuales.

    Detección temprana de errores (en lugar de ClassCastException en ejecución).

    Código más reutilizable y legible.

2. Clases e interfaces genéricas

Se define un parámetro de tipo entre < > tras el nombre:
```java
public class Caja<T> {
    private T contenido;
    public Caja(T contenido) { this.contenido = contenido; }
    public T obtener() { return contenido; }
}
Caja<String> cajaDeTexto = new Caja<>("Hola");
String texto = cajaDeTexto.obtener(); // sin casteo
```

Pueden tener varios parámetros: Map<K,V>, Pair<T,U>.
3. Métodos genéricos

Un método puede declarar sus propios parámetros de tipo, independientemente de si la clase lo es:
```java
public static <T> T primero(List<T> lista) {
    return lista.get(0);
}
String s = Util.<String>primero(listaDeStrings); // invocación explícita
String s = Util.primero(listaDeStrings);         // inferencia automática
```

### 4. Parámetros de tipo acotados (bounded)

Restringen el tipo que puede usarse:
```java
public class Calculadora<T extends Number> {
    public double sumar(T a, T b) { return a.doubleValue() + b.doubleValue(); }
}
```

T debe ser Number o una subclase. Se pueden poner múltiples cotas: <T extends Comparable<T> & Serializable> (primero clase si la hay, luego interfaces).
5. Wildcards (comodines)

Sirven para hacer las genéricos más flexibles en parámetros y variables:

    ? unbounded: representa cualquier tipo. Ej: List<?> (lista de cualquier cosa). No se pueden añadir elementos (salvo null).

    ? extends T (upper‑bounded, covarianza): acepta T o cualquier subtipo. Se puede leer elementos como tipo T, pero no se puede añadir (excepto null) porque el tipo exacto es desconocido.

    ? super T (lower‑bounded, contravarianza): acepta T o cualquier supertipo. Se puede añadir elementos de tipo T (o sus subtipos), pero al leer solo se obtiene Object.

Regla nemotécnica PECS:
Producer Extends, Consumer Super.
Si la estructura provee valores, usar extends; si consume valores, usar super.

Ejemplo:
```java
public void copiar(List<? extends Number> origen, List<? super Number> destino) {
    for (Number n : origen) { destino.add(n); }
}
```

### 6. El operador diamante <>

Desde Java 7 se puede omitir el tipo en el constructor si el compilador lo puede inferir:
```java
List<String> lista = new ArrayList<>();   // diamante
var mapa = new HashMap<Integer, String>(); // var + diamante -> HashMap<Integer, String>
```

### 7. var con genéricos

var list = new ArrayList<String>(); infiere ArrayList<String>.
var list = new ArrayList<>(); infiere ArrayList<Object> porque el diamante vacío se interpreta como Object.
Es recomendable usar el tipo completo al declarar var con colecciones genéricas.
8. Type Erasure (borrado de tipos)

Los genéricos en Java se implementan mediante borrado: el compilador elimina la información de tipo paramétrico y añade casteos allí donde sea necesario. En tiempo de ejecución, un List<String> es simplemente un List.

Consecuencias:

    No se puede usar instanceof con tipos parametrizados (excepto comodín sin acotar: if (obj instanceof List<?>)).

    No se puede crear un array de un tipo genérico (new T[10] no es válido; sí new List<?>[10]).

    No se puede instanciar un objeto del tipo paramétrico (new T() no compila).

    Las sobrecargas de método que solo difieren en el parámetro de tipo genérico no están permitidas (pues tras el borrado son idénticas).

### 9. Tipos reificables

Son aquellos cuya información de tipo se conserva en tiempo de ejecución: tipos primitivos, clases no genéricas, arrays de tipo reificable, y wildcards ilimitados (List<?>). Los tipos genéricos concretos no son reificables.
10. Bridge methods

Cuando una clase genérica extiende otra o implementa una interfaz genérica, el compilador puede generar métodos puente para mantener el polimorfismo después del borrado. Son transparentes al desarrollador.
11. Restricciones y buenas prácticas

    No se pueden usar tipos primitivos como parámetros genéricos; usar las clases envoltorio (int → Integer).

    Evitar raw types (usar List sin <>) porque omiten las comprobaciones de tipo.

    Preferir Collection<? extends Something> en lugar de Collection<Something> cuando solo se lee.

    Los genéricos no deben usarse si no se necesita polimorfismo de tipos; la complejidad extra debe justificarse.

### 12. Ejemplo avanzado
```java
public class Util {
    public static <T extends Comparable<? super T>> T max(List<? extends T> list) {
        return list.stream().max(Comparator.naturalOrder()).orElseThrow();
    }
}
```

Este método acepta una lista de cualquier subtipo de T, y T es comparable consigo mismo o con un supertipo.
