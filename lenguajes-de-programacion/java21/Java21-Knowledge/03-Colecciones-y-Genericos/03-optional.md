# OPTIONAL
1. El problema del null

null puede causar NullPointerException, es opaco en la API (no sabes si un método devuelve null) y obliga a comprobaciones manuales. java.util.Optional<T> es un contenedor inmutable que puede contener o no un valor no nulo, forzando al cliente a lidiar explícitamente con la ausencia.
2. Creación de Optionals

    Optional.of(value): lanza NullPointerException si value es null.

    Optional.ofNullable(value): devuelve Optional.empty() si value es null.

    Optional.empty(): siempre vacío.

```java
Optional<String> nombre = Optional.of("Ana");   // nunca pasar null
Optional<String> posibleNombre = Optional.ofNullable(obtenerNombre());
```

3. Recuperación y consulta

    get(): devuelve el valor si está presente, o lanza NoSuchElementException. No recomendado sin comprobación previa.

    isPresent(): booleano que indica si hay valor.

    ifPresent(Consumer): ejecuta una acción si el valor está presente.

```java
nombre.ifPresent(n -> System.out.println("Hola " + n));

    ifPresentOrElse(Consumer, Runnable) (Java 9): ejecuta el Consumer si presente, o el Runnable en caso contrario.

java
```

### nombre.ifPresentOrElse(
    n -> System.out.println("Encontrado: " + n),
    () -> System.out.println("Nombre no disponible")
);

### 4. Valores por defecto

    orElse(T other): devuelve el valor si presente, si no, devuelve other. Cuidado: other se evalúa siempre aunque el Optional tenga valor.

    orElseGet(Supplier<? extends T>): como orElse pero el suplidor solo se invoca si el Optional está vacío. Útil cuando el valor por defecto es costoso de calcular.

    orElseThrow() (Java 10+): lanza NoSuchElementException si está vacío, equivalente a get() pero más descriptivo. Existe la versión con proveedor de excepción: orElseThrow(Supplier<? extends X>) desde Java 8.

```java
String nombre = Optional.ofNullable(obtenerDesdeCache())
                         .orElseGet(() -> cargarDesdeBD());
```

### 5. Transformaciones funcionales

    map(Function<? super T, ? extends U>): si hay valor, aplica la función y envuelve el resultado en un Optional.

    flatMap(Function<? super T, Optional<U>>): similar a map pero evita anidar Optional. Idóneo cuando la función ya devuelve Optional.

    filter(Predicate<? super T>): si el valor está presente y cumple el predicado, devuelve el Optional; si no, Optional.empty().

```java
Optional<Usuario> usuario = usuarioRepository.findById(id);
String ciudad = usuario.map(Usuario::getDireccion)
                       .map(Direccion::getCiudad)
                       .orElse("Desconocida");
```

### Optional<Cuenta> cuenta = usuario.flatMap(Usuario::getCuenta)
                                 .filter(Cuenta::estaActiva);

### 6. Integración con Streams (Java 9+)

stream() devuelve un Stream<T> con 0 o 1 elementos. Permite encajar Optionals en operaciones de stream.
```java
List<Optional<String>> listaDeOptionals = List.of(Optional.of("A"), Optional.empty());
List<String> valores = listaDeOptionals.stream()
                                       .flatMap(Optional::stream)
                                       .toList();
```

### 7. Buenas prácticas y antipatrones

    Nunca declarar un campo Optional<T> en una clase (no es serializable, incrementa la complejidad). Las entidades no deben tener Optional como campo.

    No usar Optional como parámetro de métodos; en su lugar, hacer sobrecargas o pasar el valor y luego envolver internamente si es necesario.

    No llamar a get() sin comprobación; siempre usar orElse* o ifPresent*.

    Usar Optional como tipo de retorno para métodos que pueden no tener un resultado lógico (búsquedas, etc.).

    Evitar Optional en contextos de alto rendimiento si no es necesario; crear objetos Optional tiene un coste mínimo pero no nulo.

### 8. Relación con records y patrones

Los records pueden tener métodos que devuelvan Optional en lugar de campos null:
```java
public record Persona(String nombre, String direccionSecundaria) {
    public Optional<String> direccionSecundaria() {
        return Optional.ofNullable(direccionSecundaria);
    }
}
```

Sin embargo, el campo direccionSecundaria sigue siendo un String potencialmente nulo. La API presentada oculta ese detalle.
9. Novedades en Java 21 para Optional

No se han añadido nuevos métodos en Java 21. Sin embargo, la combinación de Optional con el nuevo switch y pattern matching puede usarse indirectamente:
```java
Object resultado = obtenerAlgo(); // puede ser String, null, etc.
Optional<String> optStr = switch (resultado) {
    case String s -> Optional.of(s);
    case null -> Optional.empty();
    default -> Optional.empty();
};
```

Se prefiere mantener la lógica de nulos dentro de Optional y usar sus métodos.

