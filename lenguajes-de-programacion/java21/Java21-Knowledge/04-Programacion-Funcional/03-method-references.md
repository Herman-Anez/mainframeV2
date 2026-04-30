# Referencias a Métodos

## 1. ¿Qué son?

Una referencia a método es una expresión lambda aún más compacta que indica exactamente qué método debe invocarse. Utiliza el operador `::` y mejora significativamente la legibilidad cuando la lambda se limita a llamar a un método existente.

---

## 2. Los cuatro tipos de referencias a métodos

### A) Referencia a un método estático
**Formato:** `Clase::metodoEstatico`
Equivale a: `s -> Clase.metodoEstatico(s)`

```java
Function<String, Integer> parser = Integer::parseInt;
```

### B) Referencia a un método de instancia de un objeto particular
**Formato:** `instancia::metodo`
Equivale a: `x -> instancia.metodo(x)`

```java
Consumer<String> impresora = System.out::println;
```

### C) Referencia a un método de instancia de cualquier objeto de un tipo dado
**Formato:** `Clase::metodoDeInstancia`
El primer parámetro de la lambda se convierte en el receptor (el objeto que invoca el método), y los parámetros siguientes se pasan como argumentos.

```java
Function<String, String> minusculas = String::toLowerCase; // (s) -> s.toLowerCase()
BinaryOperator<String> concatenar = String::concat;       // (a, b) -> a.concat(b)
```

### D) Referencia a un constructor
**Formato:** `Clase::new`
La interfaz funcional determina qué constructor se utiliza basándose en el número y tipo de parámetros.

```java
Supplier<List<String>> proveedor = ArrayList::new;
Function<Integer, int[]> creadorArray = int[]::new;
```

---

## 3. Resolución del método adecuado

La resolución sigue las mismas reglas de sobrecarga de Java: la interfaz funcional destino determina el número y tipo de parámetros, y el compilador busca el método o constructor que coincida exactamente.

> [!NOTE]
> Si el contexto es ambiguo (por ejemplo, hay dos métodos con el mismo nombre y firmas compatibles), el compilador lanzará un error y será necesario usar una lambda explícita o un cast.

---

## 4. Uso frecuente con Streams

Las referencias a métodos son omnipresentes al trabajar con la API Stream:

- `stream.map(String::trim)`
- `stream.filter(Objects::nonNull)`
- `stream.forEach(System.out::println)`
- `stream.collect(Collectors.toCollection(ArrayList::new))`

---

## 5. Referencias a `this` y `super`

Es posible referenciar métodos de la propia clase o de la superclase utilizando las palabras clave `this` y `super`.

```java
public class Procesador {
    private String limpiar(String s) { return s.trim(); }
    
    public void procesar(List<String> lista) {
        lista.stream()
             .map(this::limpiar)
             .forEach(System.out::println);
    }
}
```

---

## 6. Captura de excepciones

> [!WARNING]
> Si el método referenciado lanza una excepción comprobada, la interfaz funcional destino debe declararla. Si no lo hace, deberás usar una lambda explícita con un bloque `try-catch` interno.

---

## 7. Comparación de legibilidad

| Lambda | Referencia a método equivalente |
| :--- | :--- |
| `x -> Math.abs(x)` | `Math::abs` |
| `s -> s.toLowerCase()` | `String::toLowerCase` |
| `(a, b) -> a.compareTo(b)` | `String::compareTo` |
| `() -> new ArrayList<>()` | `ArrayList::new` |
| `e -> System.out.println(e)` | `System.out::println` |

---

## 8. Limitaciones

1. **Transformaciones adicionales:** No se pueden usar si necesitas realizar un paso extra (ej: `s -> s.trim().toLowerCase()`).
2. **Argumentos múltiples:** No se pueden usar si necesitas fijar un argumento que no proviene de la lambda (ej: `x -> procesar(x, "fijo")`).
3. **Claridad:** Si el nombre del método no es suficientemente descriptivo en el contexto de la lambda, es mejor usar una lambda explícita.

---

[Anterior](./02-streams.md) | [Inicio](../../README.md)
