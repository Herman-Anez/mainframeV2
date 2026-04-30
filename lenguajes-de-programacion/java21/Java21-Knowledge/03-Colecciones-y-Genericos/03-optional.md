# Optional

## 1. El problema del null

`null` puede causar `NullPointerException`, es opaco en la API (no indica si un método puede devolverlo) y obliga a realizar comprobaciones manuales repetitivas. 

`java.util.Optional<T>` es un contenedor inmutable que puede o no contener un valor no nulo, forzando al desarrollador a gestionar explícitamente la ausencia de un valor.

---

## 2. Creación de Optionals

- **`Optional.of(value)`:** Lanza `NullPointerException` si `value` es `null`.
- **`Optional.ofNullable(value)`:** Devuelve `Optional.empty()` si `value` es `null`.
- **`Optional.empty()`:** Representa la ausencia de valor.

```java
Optional<String> nombre = Optional.of("Ana"); 
Optional<String> posibleNombre = Optional.ofNullable(obtenerNombre());
```

---

## 3. Recuperación y consulta

- **`get()`:** Devuelve el valor si está presente, o lanza `NoSuchElementException`. No se recomienda sin comprobación previa.
- **`isPresent()`:** Devuelve `true` si hay un valor presente.
- **`ifPresent(Consumer)`:** Ejecuta una acción si el valor está presente.
- **`ifPresentOrElse(Consumer, Runnable)` (Java 9+):** Ejecuta el consumidor si está presente, o el runnable si está vacío.

```java
nombre.ifPresent(n -> System.out.println("Hola " + n));

nombre.ifPresentOrElse(
    n -> System.out.println("Encontrado: " + n),
    () -> System.out.println("Nombre no disponible")
);
```

---

## 4. Valores por defecto

- **`orElse(T other)`:** Devuelve el valor o `other`. **Cuidado:** `other` se evalúa siempre, incluso si el Optional tiene valor.
- **`orElseGet(Supplier)`:** Como `orElse`, pero el suplidor solo se invoca si el Optional está vacío. Ideal para valores costosos.
- **`orElseThrow()` (Java 10+):** Lanza `NoSuchElementException` si está vacío. Es la alternativa preferida a `get()`.

```java
String nombre = Optional.ofNullable(obtenerDesdeCache())
                         .orElseGet(() -> cargarDesdeBD());
```

---

## 5. Transformaciones funcionales

- **`map(Function)`:** Aplica una función al valor si está presente y envuelve el resultado en un nuevo `Optional`.
- **`flatMap(Function)`:** Similar a `map`, pero evita anidar `Optional<Optional<T>>` cuando la función ya devuelve un `Optional`.
- **`filter(Predicate)`:** Devuelve el `Optional` si el valor cumple el predicado; de lo contrario, devuelve `Optional.empty()`.

```java
String ciudad = usuario.map(Usuario::getDireccion)
                       .map(Direccion::getCiudad)
                       .orElse("Desconocida");

Optional<Cuenta> cuenta = usuario.flatMap(Usuario::getCuenta)
                                 .filter(Cuenta::estaActiva);
```

---

## 6. Integración con Streams (Java 9+)

El método `stream()` permite encadenar un `Optional` dentro de operaciones de stream de forma fluida.

```java
List<Optional<String>> listaDeOptionals = List.of(Optional.of("A"), Optional.empty());

List<String> valores = listaDeOptionals.stream()
                                       .flatMap(Optional::stream)
                                       .toList();
```

---

## 7. Buenas prácticas y antipatrones

> [!CAUTION]
> **No declarar campos Optional:** No es serializable y aumenta la complejidad de los objetos. Úsalo solo para retornos de métodos.

- **No usar como parámetros de métodos:** Es preferible usar sobrecarga de métodos o manejar nulos internamente.
- **Evitar `get()` sin comprobación:** Usar siempre `orElse*` o `ifPresent*`.
- **Rendimiento:** Aunque el coste es mínimo, evita `Optional` en bucles de rendimiento crítico si no es necesario.

---

## 8. Relación con records

Los records pueden exponer métodos que devuelvan `Optional` para campos que permitan nulos:

```java
public record Persona(String nombre, String direccionSecundaria) {
    public Optional<String> direccionSecundariaOpt() {
        return Optional.ofNullable(direccionSecundaria);
    }
}
```

---

## 9. Novedades en Java 21 para Optional

Java 21 no introduce nuevos métodos, pero el uso de `Optional` se integra perfectamente con las nuevas expresiones `switch`:

```java
Optional<String> optStr = switch (resultado) {
    case String s -> Optional.of(s);
    case null, default -> Optional.empty();
};
```

---

[Anterior](./02-genericos.md) | [Inicio](../../README.md)
