
# CLASES Y OBJETOS
1. Definición de clase

Una clase es la plantilla que describe los atributos (campos) y comportamientos (métodos) que tendrán sus instancias. Se define con la palabra clave class:
```java
public class Persona {
    // campos (variables de instancia)
    private String nombre;
    private int edad;

    // constructor
    public Persona(String nombre, int edad) {
        this.nombre = nombre;
        this.edad = edad;
    }

    // métodos
    public void saludar() {
        System.out.println("Hola, soy " + nombre);
    }
}
```

2. Modificadores de clase

    public: visible desde cualquier otro paquete.

    Sin modificador (package-private): visible solo dentro del mismo paquete.

    final: no se puede heredar.

    abstract: no se puede instanciar, puede contener métodos abstractos.

    sealed (Java 17/21): permite listar explícitamente las subclases con permits (más adelante en Herencia).

3. Miembros de una clase

    Campos (fields): variables de instancia o de clase (static).

    Métodos: funciones que operan sobre los campos. Pueden ser de instancia o estáticos.

    Constructores: métodos especiales para inicializar objetos. Pueden sobrecargarse y llamarse entre sí con this(...) o a la superclase con super(...).

    Bloques de inicialización: código que se ejecuta antes del constructor.

        Inicializador de instancia: { ... } dentro de la clase.

        Inicializador estático: static { ... }.

    Clases internas: una clase definida dentro de otra (miembro, local, anónima).

### 4. Creación de objetos

Un objeto se instancia con new seguido del constructor adecuado:
```java
Persona p = new Persona("Ana", 25);
```

La referencia p se almacena en la pila, el objeto con sus campos en el heap.
5. La palabra clave this

this se refiere a la instancia actual. Se usa para:

### Desambiguar entre parámetros y campos: this.nombre = nombre;

### Llamar a otro constructor de la misma clase: this(nombre, 0);

### Pasar la instancia actual como argumento: metodo(this);

No puede usarse en contextos estáticos.
6. Miembros estáticos (static)

Pertenecen a la clase, no a las instancias. Se accede con NombreClase.metodo() o NombreClase.campo. Métodos estáticos no tienen acceso a this ni a campos de instancia directamente. Se utilizan para utilidades, constantes (static final), factories, etc.
7. Sobrecarga de métodos y constructores

Varios métodos con el mismo nombre pero distinta firma (tipo y orden de parámetros). El tipo de retorno no basta para distinguir.
8. Inferencia de tipo local (var)

Desde Java 10, se puede declarar una variable local sin especificar su tipo:
```java
var p = new Persona("Luis", 30); // p es de tipo Persona
var lista = new ArrayList<String>();  // ArrayList<String>
```

No se puede usar en campos de clase ni en parámetros de método.
9. El registro record (Java 16+ estable)

Un tipo especial de clase inmutable y transparente para transportar datos. Define automáticamente:

    Campos private final por cada componente.

    Constructor canónico (asigna cada componente al campo del mismo nombre).

    Métodos de acceso (getter) con el nombre del componente, sin get.

    equals(), hashCode(), toString() basados en todos los componentes.

```java
public record Persona(String nombre, int edad) {}
```

Se pueden añadir métodos, validaciones en el constructor compacto (public Persona { ... }), e implementar interfaces (no puede heredar de otra clase porque implícitamente hereda java.lang.Record). Son finales (no se puede extender un registro) y no pueden ser abstractos. Perfectos para DTOs, mensajes y claves compuestas.
10. Enumeraciones (enum)

Son tipos especiales que definen un conjunto fijo de constantes. Son clases que heredan implícitamente de java.lang.Enum. Pueden tener campos, métodos y constructores privados.
```java
public enum DiaSemana {
    LUNES("L"), MARTES("M"), ...;
    private String codigo;
    DiaSemana(String cod) { this.codigo = cod; }
}
```

Desde Java 21 su uso se potencia con el pattern matching exhaustivo en switch.
11. Clases anónimas y lambdas

    Clase anónima: implementación local de una interfaz o extensión de una clase.

```java
Runnable r = new Runnable() {
    @Override public void run() { System.out.println("Ejecutando"); }
};

    Expresiones lambda (Java 8+): forma concisa para interfaces funcionales.

java
```

### Runnable r = () -> System.out.println("Ejecutando");

Ambas crean objetos que se comportan según lo especificado, y son parte esencial del polimorfismo funcional.
