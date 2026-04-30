# 📦 Records

Los **Records** son clases inmutables transparentes, diseñadas específicamente para transportar datos de manera concisa. Fueron previsualizados en Java 14, segunda preview en 15 y se estandarizaron en Java 16. En Java 21 son una herramienta fundamental.

---

## 🏗️ Declaración

```java
public record Persona(String nombre, int edad) {}
```

Con una sola línea se obtiene automáticamente:

*   **Campos privados y finales** para cada componente (`nombre`, `edad`).
*   **Constructor canónico** que recibe todos los componentes y los asigna.
*   **Métodos de acceso** con el nombre del componente, sin `get` (`nombre()` y `edad()`).
*   **equals() y hashCode()** basados en todos los componentes.
*   **toString()** que incluye el nombre del registro y los valores de los componentes: `Persona[nombre=Ana, edad=25]`.

---

## 🧱 Constructor compacto (Compact Canonical Constructor)

Permite validar, normalizar o hacer ajustes sin tener que volver a declarar todos los parámetros. La sintaxis omite los parámetros y asigna los campos al final de forma implícita:

```java
public record Persona(String nombre, int edad) {
    public Persona {  // compact constructor
        if (edad < 0) throw new IllegalArgumentException("Edad negativa");
        nombre = nombre.trim(); // "nombre" se refiere al campo, no al parámetro
    }
}
```

> [!IMPORTANT]
> No se pueden reasignar los campos fuera del constructor compacto; son `final`. Tampoco se permite un constructor adicional que llame a `this(...)` si no se respeta la inicialización de todos los campos.

---

## 🚫 Restricciones

*   **Herencia**: Son finales implícitamente, no pueden extender otra clase (heredan de `java.lang.Record`).
*   **Abstracción**: No pueden ser abstractas.
*   **Campos**: Los campos de instancia adicionales no están permitidos. Solo los componentes del registro.
*   **Flexibilidad**: Se pueden declarar campos estáticos, métodos estáticos y métodos de instancia adicionales.
*   **Interfaces**: Pueden implementar interfaces.

> [!TIP]
> Aunque son inmutables, se pueden añadir métodos que devuelvan nuevas instancias con valores modificados (estilo *With-er*):
>
> ```java
> public Persona conEdad(int nuevaEdad) {
>     return new Persona(this.nombre, nuevaEdad);
> }
> ```

---

## ⚙️ Características avanzadas

### Sobrescritura de accesores
Se pueden sobrescribir los accesores si se desea ocultar o transformar el valor (aunque se pierde transparencia). Por ejemplo, para devolver una copia defensiva:

```java
public List<String> hobbies() {
    return List.copyOf(hobbies); // supuesto que hobbies es List<String>
}
```

### Constructores adicionales
Se pueden añadir constructores adicionales que llamen al canónico con `this(...)`.

---

## 🚀 Integración con patrones y switch

Los registros forman la base de los **Record Patterns** (Java 19 preview, final en Java 21), que permiten descomponer un registro directamente en el `switch` o `instanceof`:

```java
if (figura instanceof Circulo(double radio)) {
    // radio es la componente del registro
}
```

Y en el `switch` con exhaustividad cuando se usan con **Sealed Types**.

---

## 💡 Cuándo usar records

*   **DTOs** (Data Transfer Objects).
*   **Mensajes o comandos** en arquitecturas CQRS.
*   **Claves compuestas** en mapas.
*   **Valores retornados** de consultas.
*   Cualquier estructura de datos inmutable cuyo único propósito sea agrupar valores.

---

## 📊 Comparación con Lombok o @Data

> [!NOTE]
> Los registros son una solución nativa que no requiere anotaciones ni procesadores. A diferencia de `@Data`, no son mutables (no tienen setters) y son adecuados solo para inmutabilidad.

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../README.md)
- [☕ Java 21 Index](../../index.md)
