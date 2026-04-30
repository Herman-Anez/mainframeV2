
# Clases y Objetos

La Programación Orientada a Objetos (POO) en Java se fundamenta en el uso de clases como planos y objetos como instancias concretas de esos planos.

---

## Definición de Clase

Una clase es la plantilla que describe los atributos (campos) y comportamientos (métodos) que tendrán sus instancias. Se define con la palabra clave `class`.

```java
public class Persona {
    // Campos (variables de instancia)
    private String nombre;
    private int edad;

    // Constructor
    public Persona(String nombre, int edad) {
        this.nombre = nombre;
        this.edad = edad;
    }

    // Métodos
    public void saludar() {
        System.out.println("Hola, soy " + nombre);
    }
}
```

---

## Modificadores de Clase

Determinan la visibilidad y el comportamiento de la clase en la jerarquía de herencia:

- **`public`**: Visible desde cualquier otro paquete.
- **Sin modificador (`package-private`)**: Visible solo dentro del mismo paquete.
- **`final`**: La clase no se puede heredar (ej: la clase `String`).
- **`abstract`**: No se puede instanciar; sirve como base para otras clases y puede contener métodos abstractos.
- **`sealed` (Java 17/21)**: Permite restringir qué subclases pueden heredar de ella mediante la cláusula `permits`.

---

## Miembros de una Clase

1. **Campos (*Fields*)**: Variables que almacenan el estado del objeto o de la clase (`static`).
2. **Métodos**: Bloques de código que definen el comportamiento. Pueden ser de instancia o estáticos.
3. **Constructores**: Métodos especiales para inicializar objetos. Pueden sobrecargarse y llamarse entre sí con `this(...)` o a la superclase con `super(...)`.
4. **Bloques de inicialización**:
   - **Inicializador de instancia**: `{ ... }` se ejecuta cada vez que se crea un objeto.
   - **Inicializador estático**: `static { ... }` se ejecuta una sola vez al cargar la clase.
5. **Clases internas**: Clases definidas dentro de otra clase (miembro, local o anónima).

---

## Creación de Objetos

Un objeto se instancia utilizando la palabra clave `new` seguida del constructor adecuado.

```java
Persona p = new Persona("Ana", 25);
```

> [!NOTE]
> La referencia `p` se almacena en la **pila** (*stack*), mientras que el objeto real con todos sus campos se almacena en el **heap**.

---

## La palabra clave `this`

`this` hace referencia a la instancia actual del objeto. Se utiliza principalmente para:

- **Desambiguar**: Diferenciar entre parámetros del método y campos de la clase (`this.nombre = nombre`).
- **Encadenar constructores**: Llamar a otro constructor de la misma clase (`this(nombre, 0)`).
- **Pasar la instancia**: Enviar el objeto actual como argumento a otro método (`metodo(this)`).

> [!WARNING]
> `this` **no puede** usarse dentro de contextos estáticos (`static`), ya que estos no pertenecen a ninguna instancia en particular.

---

## Miembros Estáticos (`static`)

Los miembros marcados como `static` pertenecen a la clase y no a las instancias.

- Se accede a ellos mediante `NombreClase.metodo()` o `NombreClase.campo`.
- Los métodos estáticos no tienen acceso a `this` ni a campos de instancia directamente.
- Son útiles para utilidades generales, constantes (`static final`) o fábricas (*factories*).

---

## Sobrecarga de Métodos y Constructores

Permite tener varios métodos con el mismo nombre pero diferente firma (distinto número, tipo o orden de parámetros).

> [!IMPORTANT]
> El tipo de retorno **no** es suficiente para distinguir entre métodos sobrecargados; la firma debe ser distinta en sus parámetros.

---

## Inferencia de Tipo Local (`var`)

Desde Java 10, es posible declarar variables locales sin especificar su tipo explícitamente:

```java
var p = new Persona("Luis", 30); // p es de tipo Persona
var lista = new ArrayList<String>();  // ArrayList<String>
```

> [!NOTE]
> `var` **no** se puede usar en campos de clase ni en parámetros de método; su uso está restringido al ámbito local.

---

## El Registro `record` (Java 16+)

Un `record` es un tipo especial de clase inmutable diseñada para transportar datos de forma transparente.

```java
public record Persona(String nombre, int edad) {}
```

### Características automáticas:
- Campos `private final` para cada componente.
- Constructor canónico.
- Métodos de acceso con el nombre del componente (sin el prefijo `get`).
- Implementaciones de `equals()`, `hashCode()` y `toString()`.

> [!TIP]
> Los registros son ideales para DTOs y mensajes. Son finales por defecto y no pueden ser abstractos.

---

## Enumeraciones (`enum`)

Definen un conjunto fijo de constantes. Son clases que heredan de `java.lang.Enum` y pueden tener campos, métodos y constructores privados.

```java
public enum DiaSemana {
    LUNES("L"), MARTES("M"), MIERCOLES("X");
    private String codigo;
    DiaSemana(String cod) { this.codigo = cod; }
}
```

---

## Clases Anónimas y Lambdas

### Clase Anónima
Implementación local de una interfaz o extensión de una clase:
```java
Runnable r = new Runnable() {
    @Override 
    public void run() { 
        System.out.println("Ejecutando..."); 
    }
};
```

### Expresión Lambda (Java 8+)
Forma concisa para implementar interfaces funcionales:
```java
Runnable r = () -> System.out.println("Ejecutando...");
```
