# Genéricos

## 1. Motivación y beneficios

Los genéricos permiten que una clase, interfaz o método opere sobre un tipo que se especifica como parámetro. Sus principales ventajas son:

- **Seguridad de tipos:** Comprobación en tiempo de compilación.
- **Eliminación de casteos:** El compilador inserta los casteos necesarios automáticamente.
- **Detección temprana de errores:** Evita `ClassCastException` en tiempo de ejecución.
- **Reutilización de código:** Permite algoritmos que funcionan con diferentes tipos de datos.

---

## 2. Clases e interfaces genéricas

Se define un parámetro de tipo entre `< >` tras el nombre de la clase o interfaz.

```java
public class Caja<T> {
    private T contenido;
    
    public Caja(T contenido) {
        this.contenido = contenido;
    }
    
    public T obtener() {
        return contenido;
    }
}

// Uso
Caja<String> cajaDeTexto = new Caja<>("Hola");
String texto = cajaDeTexto.obtener(); // Sin casteo manual
```

> [!NOTE]
> Una clase puede tener múltiples parámetros de tipo, como `Map<K, V>` o `Pair<T, U>`.

---

## 3. Métodos genéricos

Un método puede declarar sus propios parámetros de tipo, independientemente de la clase.

```java
public static <T> T primero(List<T> lista) {
    return lista.get(0);
}

// Invocación explícita
String s1 = Util.<String>primero(listaDeStrings);

// Inferencia automática (preferido)
String s2 = Util.primero(listaDeStrings);
```

---

## 4. Parámetros de tipo acotados (Bounded)

Permiten restringir los tipos que pueden usarse como argumentos de tipo.

```java
public class Calculadora<T extends Number> {
    public double sumar(T a, T b) {
        return a.doubleValue() + b.doubleValue();
    }
}
```

> [!IMPORTANT]
> Se pueden definir múltiples cotas: `<T extends Clase & Interfaz1 & Interfaz2>`. Si hay una clase, debe ir siempre en primer lugar.

---

## 5. Wildcards (Comodines)

Representados por el símbolo `?`, aumentan la flexibilidad en el uso de genéricos.

1. **Unbounded (`?`):** Representa cualquier tipo. `List<?>` es una lista de tipo desconocido.
2. **Upper-Bounded (`? extends T`):** Covarianza. Acepta `T` o cualquier subclase. Útil para **lectura**.
3. **Lower-Bounded (`? super T`):** Contravarianza. Acepta `T` o cualquier superclase. Útil para **escritura**.

### Regla PECS (Producer Extends, Consumer Super)

> [!TIP]
> - **Producer Extends:** Si la estructura provee valores (lectura), usa `extends`.
> - **Consumer Super:** Si la estructura consume valores (escritura), usa `super`.

```java
public void copiar(List<? extends Number> origen, List<? super Number> destino) {
    for (Number n : origen) {
        destino.add(n);
    }
}
```

---

## 6. El operador diamante `<>`

Desde Java 7, se puede omitir el tipo en el constructor si el compilador puede inferirlo.

```java
List<String> lista = new ArrayList<>(); // Diamante
```

---

## 7. `var` con genéricos

- `var list = new ArrayList<String>();` → Infiere `ArrayList<String>`.
- `var list = new ArrayList<>();` → Infiere `ArrayList<Object>` (Cuidado).

> [!NOTE]
> Es recomendable usar el tipo completo en el constructor al declarar con `var` para asegurar la inferencia correcta.

---

## 8. Type Erasure (Borrado de tipos)

Java implementa genéricos mediante el borrado de tipos: el compilador elimina la información de tipo paramétrico tras las comprobaciones y añade los casteos necesarios.

### Consecuencias:
- No se puede usar `instanceof` con tipos parametrizados (excepto `List<?>`).
- No se puede crear un array de un tipo genérico (`new T[10]` no es válido).
- No se puede instanciar un tipo paramétrico (`new T()`).
- No se permiten sobrecargas que solo difieran en el parámetro de tipo genérico.

---

## 9. Tipos reificables

Son aquellos cuya información de tipo se conserva en tiempo de ejecución:
- Tipos primitivos.
- Clases no genéricas.
- Wildcards ilimitados (`List<?>`).
- Arrays de tipos reificables.

---

## 10. Bridge Methods

El compilador genera automáticamente "métodos puente" para mantener el polimorfismo tras el borrado de tipos cuando una clase genérica extiende otra. Son transparentes para el desarrollador.

---

## 11. Restricciones y buenas prácticas

- **No usar tipos primitivos:** Usar clases envoltorio (`Integer`, `Double`, etc.).
- **Evitar Raw Types:** No usar `List` sin `<>`, ya que se pierde la seguridad de tipos.
- **Preferir Comodines:** Aumentan la flexibilidad de las APIs.
- **Justificar el uso:** No añadir complejidad genérica si no es necesaria.

---

## 12. Ejemplo avanzado

```java
public class Util {
    public static <T extends Comparable<? super T>> T max(List<? extends T> list) {
        return list.stream()
                   .max(Comparator.naturalOrder())
                   .orElseThrow();
    }
}
```

---

[Anterior](./01-colecciones.md) | [Siguiente](./03-optional.md)
