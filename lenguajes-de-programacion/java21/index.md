^(?:###\s+)?\d{2}\.\d{2}\s+[–-]

reemplazar por "#"

01 – SINTAXIS BÁSICA
1.1. El esqueleto de todo programa Java

Tradicionalmente, un programa Java se compone de al menos una clase y un método main con la firma exacta:
```java
public class MiApp {
    public static void main(String[] args) {
        System.out.println("Hola Java");
    }
}

    public class MiApp → la clase debe llamarse igual que el archivo (MiApp.java). La visibilidad public permite que la JVM la encuentre.

    public static void main(String[] args) → punto de entrada. static permite invocarlo sin crear una instancia.

    System.out.println() → salida estándar.
```

### Java 21 (Preview): Simplified Main Method
Para scripts, prototipos y ejemplos didácticos, Java 21 en modo preview permite una sintaxis mucho más ligera, incluso sin clase explícita ni static:
```java
void main() {
    println("Hola directamente desde una unnamed class");
}
```

También se permite:
```java
void main(String[] args) { ... }
```

Si se desea acceder a los argumentos. Esta característica requiere compilar con --enable-preview --source 21. Elimina la necesidad de escribir public class y System.out, ya que println se hereda de java.io.IO y la JVM genera una clase anónima por nosotros.
1.2. Paquetes e imports

    Paquete: package com.empresa.proyecto; como primera línea no comentada.

    Importaciones: import java.util.List;, import static java.lang.Math.*;.

    El paquete java.lang se importa automáticamente.

1.3. Comentarios

### Línea: // comentario

### Bloque: /* ... */

    Javadoc: /** ... */ (para generar documentación).

1.4. Identificadores y convenciones

    Deben comenzar con letra, _ o $. No pueden ser palabras reservadas.

    Convenciones (altamente recomendadas):

        Clases/Interfaces: PascalCase.

        Métodos/variables: camelCase.

        Constantes (static final): MAYÚSCULAS_CON_GUIONES.

        Paquetes: en minúsculas, notación inversa de dominio.

1.5. Bloques de código y ámbito

Cada par de llaves {} define un bloque. Las variables declaradas dentro de un bloque viven únicamente en ese ámbito, incluyendo parámetros de métodos y variables de control de bucles.
02 – TIPOS DE DATOS Y VARIABLES
2.1. Tipos primitivos

Java posee 8 tipos primitivos. No son objetos y viven en la pila.
Tipo	Tamaño	Rango	Ejemplo literal
byte	8 bits	-128 a 127	byte b = 100;
short	16 bits	-32 768 a 32 767	short s = 20_000;
int	32 bits	-2³¹ a 2³¹-1 (~ ±2 mil millones)	int i = 5_000_000;
long	64 bits	-2⁶³ a 2⁶³-1	long l = 123L;
float	32 bits	precisión simple IEEE 754	float f = 3.14f;
double	64 bits	precisión doble IEEE 754	double d = 3.14;
char	16 bits	0 a 65 535 (caracteres Unicode)	char c = 'A';
boolean	1 bit*	true o false	boolean flag = true;

En la práctica, el tamaño depende de la JVM, pero solo almacena los valores true y false.

Desde Java 7 se pueden usar guiones bajos en literales numéricos: 1_000_000. También se soportan literales binarios (0b1010) y hexadecimales (0x1A).
2.2. Tipos de referencia

Todo lo que no es primitivo es una referencia a un objeto en el heap. Incluye:

### Clases (String, Integer, ArrayList, etc.)

### Interfaces (List, Runnable, etc.)

### Enumeraciones (enum)

### Arrays (tanto de primitivos como de objetos)

### Clases especiales como record

El valor por defecto de una referencia es null.
2.3. La clase String y Text Blocks

String es inmutable. Se puede crear con comillas dobles: "Hola". Desde Java 15 (estable en 17, vigente en 21) se dispone de Text Blocks:
```java
String json = """
    {
        "nombre": "Juan",
        "edad": 25
    }
    """;
```

Los bloques de texto conservan los saltos de línea y permiten indentación controlada mediante el método stripIndent() (llamado implícitamente si la línea de cierre no tiene indentación adicional). Se pueden interpolar valores con String Templates (preview en Java 21):
```java
String nombre = "Ana";
String mensaje = STR."¡Hola \{nombre}!";
```

STR es el procesador de plantillas estándar. Este mecanismo es seguro contra inyecciones.
2.4. Inferencia de tipos con var (desde Java 10)

Declara variables locales sin especificar explícitamente el tipo, siempre que se inicialicen.
```java
var lista = new ArrayList<String>();    // ArrayList<String>
var numero = 42;                        // int
var saludo = "Hola";                    // String
```

El tipo se infiere en tiempo de compilación. No se puede usar var sin inicializador ni como parámetro de método (salvo en lambdas con tipos implícitos).
2.5. Variables: ámbito, inicialización y final

    Variables locales: deben inicializarse antes de usarse. Ámbito restringido al bloque.

    Variables de instancia (campos no estáticos): se inicializan automáticamente con el valor por defecto del tipo (0, false, null).

    Variables estáticas (campos static): ídem.

    Constantes: final indica que la variable no puede ser reasignada. Para constantes de clase se usa static final. Las referencias final no impiden modificar el objeto referenciado (excepto si es inmutable como String o record).

    final en parámetros: evita reasignaciones dentro del método.

2.6. Conversión de tipos (casting)

    Implícita (widening): de menor a mayor tamaño, p.ej. int → long → float → double. Siempre seguro.

    Explícita (narrowing): requiere casting y puede perder precisión o bits.

```java
double d = 3.14;
int i = (int) d;  // 3
```

    Promoción automática en expresiones: todos los byte, short, char se promueven a int al evaluar operadores.

### 03 – OPERADORES
3.1. Operadores aritméticos

+, -, *, /, % (módulo). Funcionan sobre tipos numéricos. División entera trunca. Precedencia: *, /, % antes que +, -.
3.2. Operadores unarios

### + (positivo), - (negación)

    ++ (incremento), -- (decremento), prefijo y sufijo.

### ! (negación lógica), ~ (complemento bit a bit)

3.3. Operadores relacionales y de igualdad

<, <=, >, >=, ==, !=. Devuelven boolean.

    == en tipos referencia compara identidad de objeto (direcciones), no contenido. Para igualdad de contenido se usa equals().

    Cuidado con autoboxing: Integer a = 200; Integer b = 200; a == b puede ser falso por el cache (el pool de enteros solo cubre -128 a 127).

3.4. Operadores lógicos

    Cortocircuito: && (AND), || (OR) – solo evalúan el segundo operando si es necesario.

    No cortocircuito: &, | (evalúan ambos operandos, también usados a nivel bit).

    ^ (XOR lógico o bit a bit según el contexto).

3.5. Operadores a nivel de bits

&, |, ^, ~, << (desplazamiento izquierda), >> (desplazamiento derecha con signo), >>> (desplazamiento derecha sin signo).
3.6. Operador de asignación y combinados

=, +=, -=, *=, /=, %=, &=, |=, ^=, <<=, >>=, >>>=.
```java
int x = 10;
x += 5;  // x = x + 5
```

3.7. Operador ternario

### condicion ? valorSiVerdadero : valorSiFalso
```java
String estado = (edad >= 18) ? "Adulto" : "Menor";
```

3.8. Operador instanceof y Pattern Matching

instanceof comprueba si un objeto es instancia de una clase/interface.
Desde Java 16 (estable), se puede realizar pattern matching para vincular una variable directamente:
```java
if (objeto instanceof String s) {
    System.out.println(s.toUpperCase());
}
```

La variable de patrón s existe únicamente si la comprobación es true. Además, se puede combinar con condiciones adicionales usando &&:
```java
if (objeto instanceof String s && s.length() > 5) { ... }
```

3.9. Operador de referencia a método ::

Permite referenciar métodos como lambdas: System.out::println, String::length, MiClase::new.
3.10. Operador -> (flecha)

Usado en lambdas y en switch expressions (que veremos en control de flujo). En lambdas: (a, b) -> a + b.
3.11. Precedencia de operadores

La tabla de precedencia ordena la evaluación. Lo más relevante:

### Postfijos (++ --)

### Unarios (+ - ! ~ ++ -- prefijos)

### Multiplicativos (* / %)

### Aditivos (+ -)

### Desplazamiento (<< >> >>>)

### Relacionales (< > <= >= instanceof)

### Igualdad (== !=)

### AND bit a bit (&)

### XOR bit a bit (^)

### OR bit a bit (|)

### AND lógico (&&)

### OR lógico (||)

### Ternario (?:)

### Asignación (= += ...)

Ante la duda, usar paréntesis.
04 – CONTROL DE FLUJO
4.1. Estructuras de decisión
if, else if, else

Evaluación condicional clásica:
```java
if (condicion) {
    // ...
} else if (otraCondicion) {
    // ...
} else {
    // ...
}
```

No hay tipo específico resultante. Las llaves son opcionales para una sola sentencia, pero se recomienda usarlas siempre.
4.2. switch – Tradicional, expresión y Pattern Matching (Java 21)

Java 21 convierte al switch en una herramienta potentísima. Veamos todas las formas.
4.2.1. switch clásico (sentencia)
```java
switch (variable) {
    case 1:
        System.out.println("Uno");
        break;
    case 2:
        System.out.println("Dos");
        break;
    default:
        System.out.println("Otro");
}
```

Sin break, hay fall-through (continúa el siguiente caso). Puede causar errores.
4.2.2. switch como expresión (Java 14+)

Devuelve un valor y usa la flecha -> para evitar break:
```java
int num = 2;
String texto = switch (num) {
    case 1 -> "Uno";
    case 2 -> "Dos";
    default -> "Otro";   // necesario si no se cubren todos los casos
};
```

Si un caso necesita un bloque de código, se usa yield para devolver el valor:
```java
String resultado = switch (num) {
    case 1 -> "Uno";
    case 2 -> {
        System.out.println("Procesando...");
        yield "Dos";
    }
    default -> "Otro";
};
```

La expresión es obligatoriamente exhaustiva (cubre todos los posibles valores del tipo). Para enum sin default se requieren todos los literales; con default no.
4.2.3. Pattern Matching for switch (Java 21 final)

Ahora el switch acepta patrones de tipo, de registro, de array y manejo explícito de null. La potencia se multiplica.
```java
Object obj = ...;
switch (obj) {
    case null -> System.out.println("Es nulo");
    case String s -> System.out.println("Cadena: " + s.toUpperCase());
    case Integer i -> System.out.println("Entero cuadrado: " + i * i);
    case int[] arr -> System.out.println("Array de enteros de longitud " + arr.length);
    default -> System.out.println("Tipo desconocido");
}
```

    El switch con patrones es exhaustivo para tipos sellados. Si la variable es una interfaz sellada como Figura, y cubrimos todos los permits, no se necesita default. Ejemplo con records y clases selladas:

```java
sealed interface Figura permits Circulo, Rectangulo, Triangulo {}
record Circulo(double radio) implements Figura {}
record Rectangulo(double ancho, double alto) implements Figura {}
record Triangulo(double base, double altura) implements Figura {}

static double area(Figura f) {
    return switch (f) {
        case Circulo(var r) -> Math.PI * r * r;
        case Rectangulo(var a, var h) -> a * h;
        case Triangulo(var b, var alt) -> b * alt / 2;
    };  // no requiere default porque la jerarquía es sellada
}
```

Observa el uso de record patterns: descomponen el registro dentro del case.

Además, los patrones pueden incluir cláusulas when (guardas) para añadir condiciones adicionales:
```java
switch (obj) {
    case String s when s.length() > 5 -> System.out.println("Cadena larga: " + s);
    case String s -> System.out.println("Cadena corta: " + s);
    ...
}
```

El orden importa: el caso más específico debe ir primero.
4.2.4. Manejo de null

En el switch clásico, pasar null lanza NullPointerException. Con pattern matching, si ponemos case null -> ... explícitamente, se maneja sin excepción. Si no se incluye ese caso y la variable puede ser nula, se lanzará NullPointerException. Es una mejora gigantesca en robustez.
4.3. Bucles
while
```java
while (condicion) {
    // cuerpo
}
```

### do-while
```java
do {
    // cuerpo
} while (condicion);
```

Ejecuta el bloque al menos una vez.
for clásico
```java
for (int i = 0; i < 10; i++) {
    // ...
}
```

Declaración/actualización de variable, condición e incremento. Se puede omitir cualquiera de las tres partes, pero los ; son obligatorios.
for mejorado (enhanced for-each)

Recorre arrays y cualquier objeto Iterable:
```java
for (String elemento : lista) {
    System.out.println(elemento);
}
```

No necesita índice. Desde Java 5. Internamente usa un iterador.
4.4. Sentencias de salto

    break → sale del bucle o del switch más interno.

    continue → salta a la siguiente iteración del bucle.

    return → sale del método y devuelve un valor si corresponde.

    yield (solo en switch expression) → devuelve un valor desde un bloque de caso.

### 4.5. Manejo de excepciones (control de flujo anómalo)

Las excepciones alteran el flujo normal. Java proporciona un manejo estructurado:
try-catch-finally
```java
try {
    // código que puede lanzar excepción
} catch (IOException e) {
    // manejo
} catch (SQLException | RuntimeException e) {  // multi-catch desde Java 7
    // maneja dos tipos
} finally {
    // se ejecuta siempre, haya o no excepción
}
```

El orden de los catch debe ser de más específica a más general.
try-with-resources (Java 7+)

Cierra automáticamente recursos que implementan AutoCloseable:
```java
try (var reader = new FileReader("archivo.txt")) {
    // usar reader
} // se cierra automáticamente al salir del bloque
```

### Excepciones comprobadas vs no comprobadas

    Comprobadas (herederas de Exception pero no de RuntimeException): obligan a manejarlas o declararlas con throws.

    No comprobadas (RuntimeException y sus hijas): no obligan a captura.

    Error y sus subclases: problemas graves de la JVM, normalmente no se capturan.

### 4.6. Control de flujo con Streams (adicional)

Aunque no es una estructura de control sintáctica, el API Stream (Java 8) ha cambiado la forma de iterar, filtrar y procesar colecciones:
```java
lista.stream()
     .filter(s -> s.length() > 3)
     .forEach(System.out::println);
```

Los streams usan operaciones intermedias (que devuelven stream) y terminales (que producen un resultado o efecto). Es un paradigma funcional que convive con los bucles clásicos.

Con esto completamos los cuatro pilares de la base sintáctica de Java 21.
Las nuevas posibilidades del switch con patrones, la inferencia con var, los registros y las clases selladas que vimos de pasada, y las mejoras en instanceof forman un conjunto sólido y moderno. Te recomiendo practicar cada apartado con pequeños programas para asimilar estos fundamentos antes de pasar a la Orientación a Objetos y las novedades avanzadas de concurrencia y rendimiento.

### 02.01 – CLASES Y OBJETOS
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
02.02 – ENCAPSULACIÓN
1. Principio de encapsulación

Consiste en ocultar el estado interno de un objeto y solo permitir su manipulación a través de una interfaz pública de métodos. Reduce el acoplamiento y facilita el mantenimiento.
2. Modificadores de acceso en Java

Java provee cuatro niveles de acceso, de más restrictivo a más abierto:
Modificador	Clase	Paquete	Subclase	Mundo
private	✔
(sin modificador)	✔	✔
protected	✔	✔	✔
public	✔	✔	✔	✔

    private solo dentro de la misma clase. Ideal para campos.

    Package‑private accesible desde clases del mismo paquete. Útil para clases y métodos internos al módulo/paquete.

    protected añade acceso desde subclases, incluso si están en distinto paquete. Común en métodos pensados para herencia.

    public para la API pública. Usar con moderación.

3. Uso de getters y setters

Para exponer campos de manera controlada se definen métodos:
```java
public class Cuenta {
    private double saldo;
    public double getSaldo() { return saldo; }
    public void depositar(double monto) {
        if (monto > 0) saldo += monto;
    }
}
```

Los records generan automáticamente métodos getter con el nombre del componente, pero no setters porque son inmutables.
4. Objetos inmutables

Un objeto inmutable no puede cambiar su estado una vez construido. Claves:

    Todos los campos final.

    La clase final o no proporciona métodos que modifiquen el estado.

    No exponer referencias mutables; devolver copias defensivas.

Ejemplo típico: String, BigInteger, y los record. La inmutabilidad facilita la programación concurrente.
5. Encapsulación reforzada con módulos (JPMS)

Desde Java 9, el sistema de módulos permite encapsular paquetes completos incluso del mismo módulo si no se exportan explícitamente en module-info.java:
```java
module mi.modulo {
    exports com.mi.paquete.api;
    // com.mi.paquete.internal no es accesible desde fuera
}
```

Esto añade una capa de encapsulación por encima de los modificadores de acceso tradicionales.
6. Encapsulación en records

Los registros son inmutables, pero la encapsulación se mantiene: no se pueden modificar los campos, aunque los getter exponen los valores. Se pueden definir métodos adicionales y el constructor canónico puede validar o normalizar los datos mediante el constructor compacto:
```java
public record Persona(String nombre, int edad) {
    public Persona {   // compacto, sin parámetros
        if (edad < 0) throw new IllegalArgumentException(...);
    }
}
```

Los campos siguen siendo private final y solo se accede a través de los getter automáticos.
02.03 – HERENCIA
1. Concepto de herencia

La herencia permite que una clase (subclase) reutilice los campos y métodos de otra (superclase). Se declara con la palabra clave extends:
```java
public class Empleado extends Persona {
    private String empresa;
    public Empleado(String nombre, int edad, String empresa) {
        super(nombre, edad);
        this.empresa = empresa;
    }
}
```

En Java no existe herencia múltiple de clases; una clase solo puede tener una superclase directa. La herencia múltiple se simula mediante interfaces.
2. La clase Object

Todas las clases heredan implícitamente de java.lang.Object si no extienden otra clase. Object proporciona métodos como toString(), equals(), hashCode(), clone() y finalize() (obsoleto). Es la raíz de la jerarquía.
3. Uso de super

    super() llama al constructor de la superclase. Debe ser la primera instrucción.

    super.metodo() invoca un método de la superclase, útil cuando se sobrescribe.

### 4. Sobrescritura de métodos y anotación @Override

Una subclase puede redefinir un método de la superclase con la misma firma y tipo de retorno compatible (covarianza). Se recomienda usar @Override para que el compilador verifique que realmente se está sobrescribiendo.
```java
@Override
public String toString() {
    return nombre + " (" + edad + ")";
}
```

### 5. Modificador final en métodos y clases

    Método final: no puede ser sobrescrito por una subclase.

    Clase final: no puede ser extendida (p.ej. String, Integer, los record).

    Argumento final: la variable local no puede ser reasignada dentro del método.

### 6. Clases selladas (sealed / permits) – Java 17, estable en 21

Restringen explícitamente qué clases o interfaces pueden extender o implementar un tipo dado. Dan lugar a jerarquías controladas, ideales para la exhaustividad en el pattern matching.
```java
public sealed class Figura permits Circulo, Rectangulo, Triangulo {
    // ...
}
```

Las subclases permitidas deben estar en el mismo módulo o paquete, y a su vez pueden ser:

    final: no se puede extender más.

    sealed: siguen restringiendo.

    non-sealed: permiten extensión libre (de nuevo abierta).

Ejemplo completo:
```java
sealed class Figura permits Circulo, Rectangulo, Triangulo {}
final class Circulo extends Figura { ... }
non-sealed class Rectangulo extends Figura { ... }
sealed class Triangulo extends Figura permits TrianguloEquilatero {}
final class TrianguloEquilatero extends Triangulo {}
```

Los sealed combinados con records y el nuevo switch producen un polimorfismo por descomposición muy potente y seguro.
7. Jerarquías con registros sellados (patrón algebraico)

Es frecuente usar interfaces selladas implementadas por registros:
```java
sealed interface Expr permits Num, Suma, Resta {}
record Num(int valor) implements Expr {}
record Suma(Expr izq, Expr der) implements Expr {}
record Resta(Expr izq, Expr der) implements Expr {}
```

Esta codificación, típica de lenguajes funcionales, es ahora directa en Java y explota al máximo el pattern matching.
02.04 – POLIMORFISMO
1. Definición de polimorfismo

Capacidad de una variable de un tipo base de referirse a objetos de distintas subclases y que la ejecución del método sobrescrito sea la correspondiente al objeto real (enlace dinámico o dynamic binding).
```java
Figura f = new Circulo(5.0);
double area = f.area(); // área del círculo, aunque el tipo de referencia sea Figura
```

2. Sobrescritura vs. Sobrecarga

    Sobrescritura (override): mismo método, misma firma, distinta implementación en subclase. Se resuelve en tiempo de ejecución.

    Sobrecarga (overload): mismo nombre de método pero diferentes parámetros. Se resuelve en compilación.

3. Covarianza en el tipo de retorno

En una sobrescritura se puede devolver un subtipo del tipo de retorno original:
```java
@Override
public Circulo copia() { ... } // si en Figura el método devuelve Figura
```

### 4. El operador instanceof con pattern matching (Java 16+)

Permite comprobar el tipo y vincular una variable en una sola operación:
```java
if (f instanceof Circulo c) {
    System.out.println("Radio: " + c.radio());
}
```

Elimina la necesidad de un casting posterior y reduce errores. Es una forma de polimorfismo condicional.
5. Polimorfismo con switch y patrones (Java 21)

El switch ahora acepta patrones de tipo, de registro y de array, y es exhaustivo con tipos sellados, convirtiéndolo en una potente herramienta de despacho múltiple.
```java
public double area(Figura f) {
    return switch (f) {
        case Circulo(var r) -> Math.PI * r * r;
        case Rectangulo(var ancho, var alto) -> ancho * alto;
        case Triangulo(var base, var altura) -> base * altura / 2;
    };
}
```

Aquí, el polimorfismo se expresa mediante descomposición en lugar de métodos virtuales, aunque ambos coexisten.
6. Polimorfismo paramétrico (genéricos)

Los genéricos permiten escribir código que funciona con distintos tipos:
```java
List<String> nombres = new ArrayList<>();
```

El compilador garantiza la seguridad de tipos en tiempo de compilación. Es otra forma de polimorfismo (universal).
7. Métodos virtuales en Java

Todos los métodos de instancia no static ni private son virtuales por defecto, es decir, se resuelven dinámicamente. Únicamente los métodos static y private no participan en el enlace dinámico.
02.05 – INTERFACES Y ABSTRACCIÓN
1. Clases abstractas

Una clase declarada abstract no puede instanciarse directamente. Puede contener métodos abstractos (sin implementación, obligando a las subclases concretas a implementarlos) y métodos concretos. Ejemplo:
```java
public abstract class Animal {
    public abstract String sonido();
    public void dormir() {
        System.out.println("Zzz");
    }
}
```

2. Interfaces

Una interfaz es un contrato que define un conjunto de métodos (sin implementación por defecto, aunque ahora pueden tener métodos por defecto y estáticos). Una clase puede implementar múltiples interfaces:
```java
public class Perro implements Mascota, Carnivoro { ... }
```

Desde Java 8, las interfaces pueden incluir:

    Métodos default: con implementación por defecto, que pueden ser sobrescritos.

    Métodos static: métodos de utilidad propios de la interfaz.

    Desde Java 9: métodos private para compartir código entre métodos default/static.

3. Evolución de las interfaces (resumen)

    Java 8: métodos default y static.

    Java 9: métodos private.

    Java 17/21: interfaces selladas (sealed interface) y el uso de patrones en switch sobre ellas.

### 4. Interfaces funcionales

Son interfaces con un único método abstracto (SAM). Se anotan con @FunctionalInterface. Por ejemplo, Runnable, Comparator, Predicate. Pueden ser implementadas mediante lambdas o referencias a métodos.
5. Interfaces selladas (sealed interface)

Al igual que las clases, una interfaz puede restringir quién la implementa:
```java
sealed interface Operacion permits Suma, Resta, Multiplicacion {}
record Suma(int a, int b) implements Operacion {}
```

Esto garantiza que, al analizar un objeto de tipo Operacion, el compilador conozca todas las posibles implementaciones y pueda exigir exhaustividad en el switch.
6. Abstracción con clases abstractas vs. interfaces
Característica	Clase Abstracta	Interfaz
Herencia múltiple	Solo una (extends)	Múltiple (implements)
Constructor	Sí	No
Campos	De instancia y estáticos	Solo constantes (static final)
Métodos	Abstractos y concretos	Abstractos, default, static, private
Visibilidad	Cualquier modificador	Métodos son públicos por defecto
Sellado (sealed)	Sí	Sí

Normalmente se prefiere interfaz para definir contratos puros, y clase abstracta cuando se desea compartir estado (campos) o constructores.
7. Herencia de tipo y herencia de implementación

    Las interfaces proporcionan herencia de tipo sin forzar una implementación concreta.

    Las clases abstractas permiten reutilizar código (herencia de implementación), pero en Java moderno se tiende a preferir composición sobre herencia profunda.

### 8. Nuevo paradigma con pattern matching

La combinación de interfaces selladas, registros y el switch con patrones está cambiando la forma de modelar el polimorfismo. Anteriormente se escribía un método abstracto en la interfaz y se implementaba en cada clase; ahora se puede usar un método estático con un switch exhaustivo sobre el tipo sellado. Ambas aproximaciones son válidas y se complementan.

Ejemplo clásico (método polimórfico):
```java
interface Figura {
    double area();
}
// cada implementación define area()
```

Ejemplo funcional (externo):
```java
double area(Figura f) {
    return switch (f) {
        case Circulo c -> Math.PI * c.radio() * c.radio();
        case Rectangulo r -> r.ancho() * r.alto();
    };
}
```

La primera encapsula cada comportamiento en su clase; la segunda centraliza operaciones y puede aprovecharse mejor con registros y patrones.

### 03.01 – COLECCIONES
1. El Java Collections Framework (JCF)

El JCF es una arquitectura unificada para representar y manipular grupos de objetos. Proporciona:

### Interfaces (tipos abstractos de datos)

### Implementaciones concretas

### Algoritmos (ordenación, búsqueda, etc.)

La raíz de la jerarquía es la interfaz Collection<E>, de la que derivan List<E>, Set<E> y Queue<E>. Map<K,V> no extiende Collection pero es parte del framework.
2. Interfaces principales y sus contratos
Interfaz	Característica principal	Implementaciones típicas
Collection	Grupo de elementos	(no se implementa directamente)
List	Ordenada por índice, permite duplicados	ArrayList, LinkedList, Vector(legacy)
Set	No duplicados, sin orden definido por posición	HashSet (sin orden), LinkedHashSet (orden inserción), TreeSet (orden natural/comparator)
Queue	Diseñada para contener elementos antes de procesarlos	ArrayDeque, PriorityQueue, LinkedList
Deque	Cola de doble extremo (hereda de Queue)	ArrayDeque, LinkedList
Map	Asociación clave-valor, sin claves duplicadas	HashMap (sin orden), LinkedHashMap (orden inserción/acceso), TreeMap (orden natural/comparator)
3. Implementaciones clave

    ArrayList: array redimensionable, acceso rápido por índice O(1), inserción/eliminación lenta al inicio o en medio O(n). Ideal para lectura intensiva y recorrido.

    LinkedList: lista doblemente enlazada, inserciones/eliminaciones O(1) en extremos y con iterador, acceso por índice O(n). Útil cuando se necesita añadir/quitar frecuentemente en cualquier posición.

    HashSet: implementación de Set basada en HashMap. No garantiza orden. O(1) para add, remove, contains.

    LinkedHashSet: mantiene el orden de inserción, ligera penalización de rendimiento.

    TreeSet: SortedSet basado en árbol rojo-negro. Ordena los elementos según su orden natural (Comparable) o un Comparator. O(log n).

    ArrayDeque: implementación de Deque más eficiente que Stack y LinkedList para uso como cola o pila. No permite elementos null.

    PriorityQueue: cola que ordena los elementos según su orden natural o comparator. El elemento más prioritario es el de menor valor según ese orden.

    HashMap: tabla hash. O(1) promedio. Permite claves null y valores null. Poco adecuado para ordenación.

    LinkedHashMap: HashMap que mantiene lista doblemente enlazada conservando el orden de inserción o de acceso.

    TreeMap: SortedMap basado en árbol rojo‑negro. Ordena las claves.

### 4. Sequenced Collections (novedad estable en Java 21)

Java 21 introduce tres nuevas interfaces que definen un orden de encuentro explícito con operaciones sobre el primer y último elemento, y acceso a una vista invertida:

### SequencedCollection<E> (hereda de Collection)

### SequencedSet<E> (hereda de Set y SequencedCollection)

### SequencedMap<K,V> (hereda de Map)

Estas interfaces son implementadas retroactivamente por las colecciones existentes que ya tenían un orden definido (por inserción, natural, etc.).

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

Ejemplos prácticos:
```java
SequencedCollection<String> lista = new ArrayList<>();
lista.add("A"); lista.add("B"); lista.add("C");
System.out.println(lista.getFirst());  // A
System.out.println(lista.getLast());   // C
lista.addFirst("Inicio");
lista.addLast("Fin");
System.out.println(lista);             // [Inicio, A, B, C, Fin]
```

### SequencedCollection<String> invertida = lista.reversed();
System.out.println(invertida.getFirst()); // Fin
invertida.addFirst("Nuevo"); // afecta a la vista, pero modifica la colección original al final
System.out.println(lista.getLast()); // Nuevo

Con SequencedMap:
```java
SequencedMap<Integer, String> map = new LinkedHashMap<>();
map.put(1, "Uno"); map.put(2, "Dos"); map.put(3, "Tres");
System.out.println(map.firstEntry());  // 1=Uno
map.pollLastEntry();                   // elimina y devuelve 3=Tres
for (var entry : map.reversed().entrySet()) {
    System.out.println(entry.getKey());
}
```

Estas adiciones simplifican enormemente el código que antes requería iteradores o casteos a implementaciones concretas.
5. Iteración y recorrido

### Bucle for‑each: for (String s : collection)

    Iterador explícito: Iterator<E>, permite eliminar durante el recorrido con remove().

### forEach(Consumer) (Java 8): lista.forEach(System.out::println)

    Spliterator para paralelismo y streams.

    Streams (Java 8+): lista.stream().filter(...).collect(toList()) (explicado en programación funcional).

### 6. Ordenación

    Comparable<T>: la clase implementa compareTo(T o). Define el orden natural.

    Comparator<T>: interfaz externa con compare(T o1, T o2). Multitud de métodos default (reversed(), thenComparing(), comparingInt(), etc.)

    Métodos útiles en Collections: sort(), reverseOrder().

    SortedSet/SortedMap requieren Comparator o elementos Comparable.

### 7. Colecciones inmutables (Java 9+)

    Fábricas: List.of(...), Set.of(...), Map.of(key,value,...), Map.ofEntries(...). Devuelven colecciones inmutables (no se pueden modificar, ni siquiera con iterador.remove). Lanzan UnsupportedOperationException si se intenta modificar.

    Copias inmutables: List.copyOf(collection), Set.copyOf(), Map.copyOf() (Java 10+). Si la colección de origen ya es inmutable, la devuelve sin copiar.

    Colecciones no modificables tradicionales: Collections.unmodifiableList(...) envuelven una colección mutable pero impiden modificaciones a través de la vista. La colección subyacente puede cambiar si se modifica directamente.

### 8. Colecciones concurrentes

    ConcurrentHashMap: mapa thread‑safe de alto rendimiento.

    CopyOnWriteArrayList/CopyOnWriteArraySet: útiles cuando las lecturas dominan sobre las escrituras.

    BlockingQueue (ArrayBlockingQueue, LinkedBlockingQueue) para productores/consumidores.

    ConcurrentSkipListMap/Set: implementaciones concurrentes de SortedMap/SortedSet.

### 9. Clases legacy y obsoletas

    Vector → sustituir por ArrayList (y sincronizar externamente si es necesario).

    Stack → Deque (con ArrayDeque), métodos push/pop.

    Hashtable → HashMap o ConcurrentHashMap.

    Enumeration → Iterator.

### 10. Ejemplo integrador con secuencias (Java 21)
```java
public void procesarPedidos(SequencedCollection<Pedido> pedidos) {
    Pedido urgente = pedidos.getFirst();  // antes: pedidos.get(0)
    // despachar urgente...
    var reverso = pedidos.reversed();     // vista invertida
    reverso.forEach(p -> p.archivar());
}
```

### 03.02 – GENÉRICOS
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
03.03 – OPTIONAL
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

### 04.01 – LAMBDAS
1. ¿Qué es una expresión lambda?

Una lambda es un bloque de código compacto que implementa el único método abstracto de una interfaz funcional. Permite tratar funciones como objetos y pasar comportamiento como parámetro.

Sintaxis general:
(parámetros) -> { cuerpo }

Variantes:

### Sin parámetros: () -> System.out.println("Hola")

### Un solo parámetro (paréntesis opcionales): x -> x * 2

### Varios parámetros: (a, b) -> a + b

### Cuerpo de varias líneas: (x, y) -> { int z = x + y; return z; }

Los tipos de los parámetros se pueden declarar explícitamente:
```java
(int a, int b) -> a + b
```

Normalmente se omiten y la JVM los infiere del contexto.
2. Interfaces funcionales

Una interfaz funcional es aquella que tiene exactamente un método abstracto (SAM – Single Abstract Method). Puede contener métodos default y static adicionales. Se recomienda anotarlas con @FunctionalInterface para que el compilador verifique la condición.
```java
@FunctionalInterface
public interface Operacion {
    int aplicar(int a, int b);
}
```

### Principales interfaces funcionales en java.util.function
Interfaz	Método abstracto	Descripción
Predicate<T>	boolean test(T t)	Evaluación booleana
Consumer<T>	void accept(T t)	Consume un valor sin retorno
Function<T,R>	R apply(T t)	Transforma un valor en otro
Supplier<T>	T get()	Provee un valor
UnaryOperator<T>	T apply(T t)	Function<T,T> especializado
BinaryOperator<T>	T apply(T t, T u)	BiFunction<T,T,T> especializado
BiPredicate<L,R>	boolean test(L l, R r)	Predicado de dos argumentos
BiConsumer<T,U>	void accept(T t, U u)	Consumidor de dos argumentos
BiFunction<T,U,R>	R apply(T t, U u)	Función de dos argumentos

Ejemplos de uso con lambdas:
```java
Predicate<String> isEmpty = s -> s.isEmpty();
Consumer<String> printer = s -> System.out.println(s);
Function<String, Integer> length = s -> s.length();
Supplier<Double> random = () -> Math.random();
BinaryOperator<Integer> sum = (a, b) -> a + b;
```

También existen especializaciones para tipos primitivos: IntPredicate, LongConsumer, DoubleFunction<R>, etc., que evitan el autoboxing.
3. Inferencia de tipos y “target typing”

El compilador decide qué interfaz funcional representa la lambda basándose en el contexto:

    Asignación a una variable del tipo de la interfaz.

    Paso como argumento a un método que espera dicha interfaz.

    Uso como valor de retorno donde se espera la interfaz.

    Cast explícito: (Predicate<String>) (s -> s.isEmpty()).

Es target typing: la lambda no tiene tipo por sí misma, lo adquiere del destino.
4. Captura de variables (closures)

Una lambda puede usar variables del ámbito envolvente. Las variables locales capturadas deben ser efectivamente finales (no modificadas después de inicializadas).
```java
String prefijo = "Sr. ";
Consumer<String> saludo = nombre -> System.out.println(prefijo + nombre);
// prefijo = "Sra. "; // error de compilación si se modifica
```

Las variables de instancia y estáticas no tienen esa restricción, porque se capturan por referencia al objeto (this).
5. La referencia this dentro de una lambda

Dentro de una lambda, this se refiere a la instancia de la clase que la contiene, no a la lambda en sí (que no tiene identidad propia). Es la misma semántica que una clase anónima.
```java
public class Ejemplo {
    private String nombre = "Ejemplo";
    public void probar() {
        Consumer<String> c = s -> System.out.println(this.nombre + " " + s);
        c.accept("prueba"); // imprime "Ejemplo prueba"
    }
}
```

### 6. Comparativa con clases anónimas
Característica	Lambda	Clase anónima
Ámbito de this	La clase contenedora	La propia clase anónima
Implementación interna	No genera un archivo .class aparte (usa invokedynamic y LambdaMetafactory)	Genera una clase separada al compilar
Obligatoriedad SAM	Solo interfaces funcionales	Interfaces y clases (incluso con varios métodos)
Uso de campos	No puede declarar campos propios	Puede declarar campos

Por rendimiento y limpieza, se prefieren lambdas cuando solo se necesita un SAM.
7. Usos prácticos

    Sustituir implementaciones verbosas de Comparator, Runnable, ActionListener, etc.

    Operaciones sobre colecciones con forEach, removeIf, replaceAll, sort.

### Crear hilos ligeros: new Thread(() -> { ... }).start();

    Construir flujos con la API Stream.

    Patrones de diseño como estrategia, command, observer mucho más concisos.

```java
// Ordenar con lambda
lista.sort((a, b) -> a.compareToIgnoreCase(b));
// Ejecutar tarea
Runnable tarea = () -> System.out.println("Ejecutando");
```

### 8. Excepciones en lambdas

Si el método abstracto de la interfaz funcional no declara excepciones comprobadas, la lambda no puede lanzarlas directamente. Soluciones:

    Capturarlas dentro de la lambda.

    Usar una interfaz funcional propia que declare la excepción.

    Envolver en una excepción no comprobada.

```java
// No compila: Runnable no lanza IOException
Runnable r = () -> { Files.lines(Path.of("noexiste")); };
// Opción: try-catch
Runnable r = () -> { try { Files.lines(...); } catch (IOException e) { ... } };
```

### 9. Buenas prácticas

    Pequeñas y autocontenidas: si crece más de 3-4 líneas, considerar un método con nombre.

    Evitar efectos laterales en lambdas usadas en streams (salvo forEach/peek para depuración).

    No abusar de la inferencia; a veces la legibilidad mejora explicitando el tipo en el parámetro.

    Preferir method reference cuando la lambda consista en la llamada directa a un método existente.

### 04.02 – STREAMS
1. Concepto y estructura

Un Stream es una secuencia de elementos que soporta operaciones secuenciales y paralelas de forma agregada. No es una estructura de datos; es una vista sobre una fuente (colección, array, I/O, etc.) que se procesa de forma perezosa.

Un pipeline de stream consta de:

    Origen: de donde se obtienen los datos.

    Operaciones intermedias: cero o más, devuelven un nuevo Stream (encadenamiento). Son lazy.

    Operación terminal: produce un resultado o efecto secundario, y consume el stream (no se puede reutilizar).

2. Creación de streams

    Desde una colección: coleccion.stream() (secuencial) o coleccion.parallelStream().

    Desde arrays: Arrays.stream(array) o Stream.of(array).

    Desde valores sueltos: Stream.of("a", "b", "c").

    Generación infinita: Stream.iterate(valorInicial, unaryOperator), Stream.generate(supplier).

    Desde archivos: Files.lines(path) (devuelve Stream<String>).

    Desde números aleatorios: new Random().ints().

    Desde flujos de Optional (Java 9): optional.stream().

    Stream vacío: Stream.empty().

    Concatenar: Stream.concat(s1, s2).

```java
Stream<Integer> infinito = Stream.iterate(0, n -> n + 1); // peligro si no se limita
List<String> nombres = List.of("Ana", "Luis");
Stream<String> streamNombres = nombres.stream();
```

3. Operaciones intermedias
Operación	Descripción
filter(Predicate)	Retiene elementos que cumplan el predicado.
map(Function)	Transforma cada elemento en otro.
flatMap(Function)	Aplana cada elemento a un stream de varios y luego los concatena.
distinct()	Elimina duplicados según equals().
sorted()/sorted(Comparator)	Ordena los elementos (si son Comparable o con comparador).
peek(Consumer)	Ejecuta una acción por cada elemento (para depurar).
limit(long)	Trunca el stream a los primeros n elementos.
skip(long)	Omite los primeros n elementos.
takeWhile(Predicate) (Java 9+)	Toma elementos mientras se cumple el predicado, luego corta.
dropWhile(Predicate) (Java 9+)	Descarta mientras se cumple, luego deja pasar el resto.
mapMulti(BiConsumer) (Java 16+)	Similar a flatMap, pero evita crear streams intermedios para cada elemento.

Ejemplo:
```java
lista.stream()
     .filter(s -> s.length() > 3)
     .map(String::toUpperCase)
     .sorted()
     .distinct()
     .limit(10)
     .forEach(System.out::println);
```

Importante: las operaciones intermedias no se ejecutan hasta que se invoca una operación terminal.
4. Operaciones terminales

Se dividen en:
De transformación y búsqueda

    collect(Collector): acumula los elementos en una colección, mapa, cadena, etc.

    toList() (Java 16): devuelve una lista inmutable con los elementos.

    toArray(): array de Object o con IntFunction.

    reduce(identidad, BinaryOperator): reduce el stream a un solo valor.

    count(): número de elementos.

    min(Comparator), max(Comparator): devuelven Optional.

### De efecto colateral

    forEach(Consumer): aplica una acción a cada elemento. No garantiza orden en paralelo.

    forEachOrdered(Consumer): respeta el orden incluso en paralelo.

### De coincidencia

    anyMatch(Predicate): si algún elemento cumple → boolean.

    allMatch(Predicate): si todos cumplen.

    noneMatch(Predicate): si ninguno cumple.

### De consulta

    findFirst(): primer elemento, Optional.

    findAny(): cualquier elemento (en paralelo, puede ser cualquiera), Optional.

Ejemplos:
```java
List<String> filtrados = stream.collect(Collectors.toList());  // mutable
List<String> inmutables = stream.toList();                     // Java 16+, inmutable

long conteo = stream.filter(s -> s.startsWith("A")).count();
Optional<Integer> max = stream.map(String::length).max(Integer::compare);
boolean existe = stream.anyMatch(s -> s.isEmpty());
```

### 5. Collectors (coleccionistas)

La clase Collectors proporciona implementaciones de Collector para operaciones comunes:
Método	Resultado
toList()	ArrayList (mutable, no garantiza tipo)
toSet()	HashSet
toCollection(Supplier)	Colección especificada (p.ej. TreeSet::new)
toMap(keyMapper, valueMapper)	HashMap; cuidado con claves duplicadas
joining()	Concatena Strings
groupingBy(classifier)	Map<K, List<T>> agrupando por clave
partitioningBy(predicate)	Map<Boolean, List<T>>
summarizingInt()	Estadísticas (count, sum, min, average, max)
reducing()	Reducción generalizada
```java
Map<Integer, List<Persona>> porEdad = personas.stream()
    .collect(Collectors.groupingBy(Persona::edad));
String nombres = personas.stream()
    .map(Persona::nombre)
    .collect(Collectors.joining(", "));
```

### 6. Streams paralelos

Llamar a parallel() o usar parallelStream() hace que las operaciones se ejecuten en el ForkJoinPool común. Adecuado cuando la fuente es grande y las operaciones son costosas y sin efectos colaterales.

Precauciones:

    Las operaciones no deben depender del orden ni modificar estado mutable externo.

    El overhead de paralelización puede empeorar el rendimiento en streams pequeños.

    forEachOrdered puede perder paralelismo al imponer orden.

    Usar findAny en lugar de findFirst cuando el orden no importa, para aprovechar la concurrencia.

### 7. Streams de tipos primitivos

Para evitar el autoboxing existen IntStream, LongStream y DoubleStream. Métodos específicos:

    sum(), average(), min(), max(), summaryStatistics().

    Creación con range(), rangeClosed().

    Conversiones: stream.boxed() convierte a Stream de envoltorios; mapToInt, mapToObj, etc.

```java
int suma = IntStream.rangeClosed(1, 100).sum();
double promedio = IntStream.of(3,5,7).average().orElse(0);
```

### 8. Manejo de nulos

Java 9 introdujo Stream.ofNullable(valor) que devuelve un stream vacío si el valor es null, o un stream con el elemento en caso contrario.
```java
Stream<String> flujo = Stream.ofNullable(pais).flatMap(p -> obtenerEstadoStream(p));
```

### 9. mapMulti (Java 16)

Alternativa a flatMap para cuando la transformación produce cero, uno o unos pocos elementos, y no queremos crear un stream por cada entrada. Recibe un BiConsumer<T, Consumer<R>> y el consumidor acepta cada elemento producido.
```java
stream.mapMulti((String s, Consumer<Integer> sink) -> {
    if (!s.isEmpty()) {
        sink.accept(s.length());
    }
});
```

### 10. Novedades y buenas prácticas en Java 21

    La interfaz SequencedCollection permite obtener una vista invertida con reversed(). Al invocar stream() sobre esa vista, se obtiene un stream en orden inverso:

```java
sequencedList.reversed().stream().forEach(...);

    Preferir stream.toList() en lugar de collect(Collectors.toList()) cuando se desea una lista inmutable. Es más conciso y deja clara la inmutabilidad.

    Evitar operaciones terminales que produzcan efectos laterales (como forEach para poblar otra colección) dentro de streams paralelos si no es seguro.
```

    Utilizar takeWhile/dropWhile para streams ordenados cuando se necesita cortar o saltar con condiciones.

### 04.03 – REFERENCIAS A MÉTODOS
1. ¿Qué son?

Una referencia a método es una expresión lambda aún más compacta que indica exactamente qué método debe invocarse. Usa el operador :: y mejora la legibilidad cuando la lambda se limita a llamar a un método existente.
2. Los cuatro tipos de referencias a métodos
a) Referencia a un método estático

### Formato: Clase::metodoEstatico
Ejemplo: Integer::parseInt equivale a s -> Integer.parseInt(s)
```java
Function<String, Integer> parser = Integer::parseInt;
```

### b) Referencia a un método de instancia de un objeto particular

### Formato: instancia::metodo
Ejemplo: System.out::println equivale a x -> System.out.println(x)
```java
Consumer<String> impresora = System.out::println;
```

### c) Referencia a un método de instancia de cualquier objeto de un tipo dado

### Formato: Clase::metodoDeInstancia
El primer parámetro de la lambda se convierte en el receptor (objeto que invoca el método), y los siguientes (si los hay) se pasan como argumentos.
Ejemplo: String::toLowerCase equivale a (String s) -> s.toLowerCase()
```java
Function<String, String> minusculas = String::toLowerCase;
UnaryOperator<String> minusculasOp = String::toLowerCase;
```

Puede usarse con dos parámetros: String::concat equivale a (a, b) -> a.concat(b), es decir, BinaryOperator<String>.
d) Referencia a un constructor

### Formato: Clase::new
Equivale a una lambda que crea una nueva instancia. La interfaz funcional determina qué constructor se usa (por número de parámetros).

    ArrayList::new (sin argumentos) → Supplier<List<Integer>>, provee una lista vacía.

    Integer::new (con un int) → Function<String, Integer> no vale; pero IntFunction<int[]> int[]::new crea un array.

```java
Supplier<List<String>> proveedor = ArrayList::new;
Function<Integer, int[]> creadorArray = int[]::new;
```

3. Cómo se resuelve el método adecuado

La resolución sigue las mismas reglas de sobrecarga: la interfaz funcional determina el número y tipo de parámetros, y el compilador busca un método/constructor que coincida.

Ejemplo de sobrecarga exitosa:
```java
public class Ejemplo {
    public static void metodo(int x) { ... }
    public static void metodo(String s) { ... }
}
// En un contexto Predicate, ninguna es válida; en un Consumer<Integer> se resuelve al que acepta int.
```

### 4. Uso frecuente con streams

### stream.map(String::trim)

### stream.filter(Objects::nonNull)

### stream.forEach(System.out::println)

### stream.collect(Collectors.toCollection(ArrayList::new))

### stream.map(Persona::new) (constructor que toma los elementos como parámetro)

### 5. Referencia a métodos privados o de instancia

Se puede usar this::metodoPrivado para referenciar un método privado de la clase envolvente, y super::metodo para un método de la superclase.
```java
public class Procesador {
    private String limpiar(String s) { return s.trim(); }
    public void procesar(List<String> lista) {
        lista.stream().map(this::limpiar).forEach(System.out::println);
    }
}
```

### 6. Captura de excepciones

Si el método referenciado lanza excepciones comprobadas, la referencia a método hereda esa restricción y la interfaz funcional destino debe declararlas, o bien hay que adaptarla (envolviendo en un bloque try-catch o usando un hack con lanzamiento de excepciones no comprobadas). Es más difícil que con lambdas directamente; en la práctica se recurre a una lambda explícita cuando se necesita manejo de excepciones.
7. Comparación de legibilidad
Lambda	Referencia a método equivalente
x -> Math.abs(x)	Math::abs
s -> s.toLowerCase()	String::toLowerCase
(a, b) -> a.compareTo(b)	String::compareTo
() -> new ArrayList<>()	ArrayList::new
e -> System.out.println(e)	System.out::println

Usar referencias a métodos cuando el código ya está bien nombrado en el método referenciado; si necesitas un paso adicional o transformación previa, la lambda es más expresiva.
8. Limitaciones

    No se pueden referenciar métodos que requieran pasar el resultado de otra expresión compleja; la lambda sería necesaria (por ejemplo, x -> procesar(x, y) donde y es una variable capturada, no se puede escribir como procesar::? porque no hay forma de fijar el segundo argumento).

    Las referencias a métodos no pueden capturar variables para usarlas como argumentos adicionales, salvo que el receptor sea el primer parámetro (tipo 3) y el resto parámetros del método, lo que limita su flexibilidad.

### 05 – MANEJO DE EXCEPCIONES

El manejo de excepciones en Java es un mecanismo robusto para controlar situaciones anómalas que pueden ocurrir en tiempo de ejecución. Java 21 mantiene el modelo consolidado desde las primeras versiones, con pequeñas mejoras de calidad de vida introducidas en versiones anteriores que siguen plenamente vigentes.
1. Jerarquía de excepciones

Todas las excepciones y errores heredan de la clase java.lang.Throwable. De ella derivan dos ramas principales:

    Error y sus subclases: representan problemas graves relacionados con la JVM (p.ej. OutOfMemoryError, StackOverflowError). Normalmente no se capturan ni se tratan, pues indican condiciones de las que una aplicación típica no puede recuperarse.

    Exception y sus subclases: condiciones que la aplicación podría querer capturar.

        Excepciones comprobadas (checked): Todas las hijas de Exception que no son RuntimeException. El compilador obliga a manejarlas (con try-catch) o a declararlas en la firma del método (throws). Ejemplos: IOException, SQLException, ClassNotFoundException.

        Excepciones no comprobadas (unchecked): Las hijas de RuntimeException. No es obligatorio capturarlas ni declararlas. Suelen indicar errores de programación (p.ej. NullPointerException, IllegalArgumentException, IndexOutOfBoundsException).

```java
Throwable
├── Error
│   ├── VirtualMachineError (OutOfMemoryError, StackOverflowError)
│   └── ...
└── Exception
    ├── IOException (checked)
    ├── SQLException (checked)
    └── RuntimeException (unchecked)
        ├── NullPointerException
        ├── IllegalArgumentException
        ├── IndexOutOfBoundsException
        └── ...
```

2. Captura de excepciones: try-catch-finally

La estructura básica para manejar excepciones es el bloque try-catch-finally.
2.1. try con uno o varios catch
```java
try {
    // Código que puede lanzar una excepción
    Files.readAllLines(Path.of("archivo.txt"));
} catch (IOException e) {
    // Manejo específico para IOException
    System.err.println("Error de E/S: " + e.getMessage());
} catch (Exception e) {
    // Manejo genérico para cualquier otra excepción
    System.err.println("Error inesperado: " + e);
}
```

Los bloques catch se evalúan en orden. Se debe poner primero el tipo más específico, ya que si un catch de supertipo aparece antes, atrapará también las excepciones de subtipos y los bloques posteriores nunca se ejecutarían (error de compilación si son del mismo nivel).
2.2. Multi-catch (Java 7+)

Se pueden capturar varios tipos de excepción en un solo bloque cuando el manejo es idéntico:
```java
try {
    // ...
} catch (IOException | SQLException e) { // e es implícitamente final
    System.err.println("Error de datos: " + e.getMessage());
}
```

La variable e es de tipo de la unión de los tipos listados, pero es final (no se puede reasignar dentro del bloque).
2.3. finally

El bloque finally se ejecuta siempre, ocurra o no una excepción, y aunque dentro del try o catch se realice un return. Se usa para liberar recursos que no implementan AutoCloseable.
```java
FileInputStream fis = null;
try {
    fis = new FileInputStream("archivo.txt");
    // leer...
} catch (IOException e) {
    // manejar
} finally {
    if (fis != null) {
        try { fis.close(); } catch (IOException ignorada) {}
    }
}
```

3. Try-with-resources (Java 7+)

Simplifica la gestión de recursos que implementen AutoCloseable (o Closeable). Los recursos declarados en la cabecera del try se cierran automáticamente al finalizar el bloque, en orden inverso al de creación.
```java
try (BufferedReader br = new BufferedReader(new FileReader("archivo.txt"))) {
    String linea = br.readLine();
    // ...
} // br.close() se llama automáticamente
```

Desde Java 9 se pueden usar variables efectivamente finales o ya declaradas:
```java
BufferedReader br = new BufferedReader(new FileReader("archivo.txt"));
try (br) {   // br es un recurso pasado al try
    // ...
}
```

Si el bloque try lanza una excepción y el cierre también, la excepción del cierre se suprime y se añade como suprimida a la original, accesible con Throwable.getSuppressed().
4. Declaración de excepciones: throws

Cuando un método no maneja una excepción comprobada, debe declararla en su firma:
```java
public String leerArchivo(String ruta) throws IOException {
    return Files.readString(Path.of(ruta));
}

    Sólo las excepciones comprobadas requieren declaración; las no comprobadas (RuntimeException y sus hijas) pueden declararse opcionalmente.
```

    Sobrescribir un método: no se pueden añadir más excepciones comprobadas que las declaradas por el método original, aunque sí se pueden reducir o declarar subtipos.

### 5. Creación de excepciones propias

Se pueden definir excepciones personalizadas extendiendo Exception (checked), RuntimeException (unchecked) o Throwable. Es recomendable proporcionar al menos constructores que acepten mensaje y causa.
```java
public class CuentaException extends Exception {
    public CuentaException(String mensaje) {
        super(mensaje);
    }
    public CuentaException(String mensaje, Throwable causa) {
        super(mensaje, causa);
    }
}
```

### 6. Buenas prácticas y pautas

    Captura específica: evitar catch (Exception e) genérico salvo en puntos de entrada (p.ej., un main o un hilo raíz). Capturar lo que realmente se puede manejar.

    No tragar excepciones: nunca dejar un bloque catch vacío. Al menos registrar el error.

    Envolver excepciones: si se quiere añadir contexto, usar excepción personalizada o new RuntimeException(mensaje, e) para mantener la causa original.

    Usar finally o try-with-resources para liberar recursos, incluso si no hay excepción.

    Documentar con @throws en Javadoc todas las excepciones comprobadas y las no comprobadas relevantes.

    En streams/lambdas: las interfaces funcionales no permiten lanzar excepciones comprobadas directamente. Soluciones:

        Capturar dentro y convertir a unchecked.

        Usar bibliotecas como vavr o crear interfaces funcionales propias que permitan lanzar.

    Optional evita el uso de null y reduce la necesidad de NullPointerException, pero no reemplaza el manejo de excepciones para casos de error irrecuperables.

### 7. Novedades en mensajes de excepción (Java 14+)

Aunque no es una característica del lenguaje, desde Java 14 se mejoraron los mensajes de NullPointerException con información de qué variable era nula en la línea exacta, activando la opción de JVM -XX:+ShowCodeDetailsInExceptionMessages (habilitada por defecto en muchas distribuciones).
```java
a.b.c = 5; // NPE dirá "Cannot read field 'c' because 'a.b' is null"
```

Esto está disponible y es útil en Java 21.

Con esto, el archivo 01-excepciones.md queda detallado y actualizado para Java 21.
06.01 – MÓDULOS JPMS (Java Platform Module System)

El Java Platform Module System (JPMS), introducido en Java 9 y plenamente vigente en Java 21, permite organizar el código en módulos que declaran explícitamente sus dependencias y qué paquetes exportan. Proporciona encapsulación fuerte a nivel de módulo y mejora el rendimiento de carga de clases.
1. ¿Qué es un módulo?

Un módulo es un artefacto (normalmente un archivo JAR) que contiene un descriptor module-info.class en su raíz, generado a partir del archivo fuente module-info.java. Este descriptor define:

    Nombre del módulo (único, usualmente notación inversa de dominio).

    Dependencias (requires) hacia otros módulos.

    Paquetes exportados (exports) que serán accesibles para otros módulos.

    Paquetes abiertos (opens) para acceso reflexivo.

    Servicios que consume (uses) o provee (provides … with).

2. Estructura del archivo module-info.java
```java
// module-info.java
module com.mipaquete.miapp {
    // Dependencias
    requires java.logging;            // requiere el módulo java.logging
    requires transitive java.sql;     // requiere y reexporta: quien me requiere también podrá usar java.sql

    // Paquetes públicos
    exports com.mipaquete.miapp.api;  // el paquete api es accesible por otros módulos
    exports com.mipaquete.miapp.util to modulo.amigo; // exportación restringida a un módulo concreto

    // Reflexión
    opens com.mipaquete.miapp.model;  // permite reflexión sobre este paquete a todo el mundo
    opens com.mipaquete.miapp.config to modulo.framework; // reflexión restringida

    // Servicios
    uses com.mipaquete.miapp.spi.Servicio;   // consume un servicio
    provides com.mipaquete.miapp.spi.Servicio
        with com.mipaquete.miapp.internal.Implementacion; // provee una implementación
}
```

3. Directivas detalladas
3.1. requires

Declara dependencia de otro módulo.

    Sintaxis simple: requires modulo; → el módulo nombrado debe estar presente.

    requires transitive: además de requerir, cualquier módulo que requiera al nuestro verá también como accesibles los paquetes exportados por el módulo transitivo. Fomenta la reexportación de dependencias de una API.

    requires static: dependencia opcional en tiempo de compilación. Si el módulo no está presente en ejecución, se ignorará (útil para anotaciones o dependencias de herramientas que no son necesarias en tiempo de ejecución).

3.2. exports

Hace que los tipos públicos de un paquete sean accesibles desde fuera del módulo. Sin exports, un paquete es privado al módulo aunque sus clases sean public.

    exports paquete; – todos los módulos pueden acceder.

    exports paquete to modulo1, modulo2; – acceso restringido a módulos específicos (exportación cualificada). Útil para exprimir detalles internos entre módulos amigos sin abrirlos al mundo.

3.3. opens

Permite acceso reflexivo a un paquete (incluso a sus miembros privados) en tiempo de ejecución. Necesario para frameworks como Hibernate, Jackson, etc.

    opens paquete; – cualquier módulo puede usar reflexión sobre el paquete.

    opens paquete to modulo; – restringido a un módulo.

Alternativamente, en lugar de opens en módulo-info, se puede usar la opción de línea de comandos --add-opens.
3.4. Servicios (uses y provides)

    uses: declara que el módulo consume un servicio (interfaz o clase abstracta). La JVM localizará todos los módulos que provean una implementación de esa interfaz y las cargará al usar ServiceLoader.

    provides … with: declara que el módulo provee una implementación concreta para un servicio. La implementación suele ser una clase interna no exportada.

Ejemplo:
```java
module com.api {
    exports com.api.servicio;
}
module com.provider {
    requires com.api;
    provides com.api.servicio.Servicio with com.provider.ImplementacionServicio;
}
module com.consumidor {
    requires com.api;
    uses com.api.servicio.Servicio;
}
```

El consumidor puede obtener todas las implementaciones con:
```java
ServiceLoader<Servicio> loader = ServiceLoader.load(Servicio.class);
loader.forEach(s -> s.ejecutar());
```

### 4. Encapsulación y acceso por defecto

    Paquetes no exportados: completamente encapsulados; sus clases públicas no son accesibles fuera del módulo (ni siquiera mediante reflexión, a menos que se abra explícitamente).

    Paquetes exportados: sus tipos public son accesibles en tiempo de compilación y ejecución. Sin embargo, los miembros protected y private siguen restringidos según los modificadores de acceso clásicos.

    Un módulo no puede acceder a otro módulo si no lo requiere y ese otro no le exporta el paquete.

El sistema de módulos añade una capa de encapsulación por encima de los modificadores public/private, haciendo que las API sean mucho más claras y resistentes al mal uso.
5. Módulos de la propia plataforma Java

A partir de Java 9, el JDK está modularizado en una serie de módulos estándar como java.base, java.logging, java.sql, java.xml, etc. El módulo java.base contiene las clases fundamentales (java.lang, java.util, java.io, etc.) y siempre está implícitamente requerido por cualquier módulo.

Podemos listar los módulos del JDK con:
shell

### java --list-modules

### 6. Compilación y empaquetado con módulos
Estructura de directorios típica
```text
src/
  modulo1/
    module-info.java
    com/paquete/... (fuentes)
  modulo2/
    module-info.java
    com/otro/... (fuentes)
```

### Compilación con múltiples módulos
shell

### javac -d out --module-source-path src $(find src -name "*.java")

Luego se puede empaquetar cada módulo como un JAR:
shell

jar --create --file modulo1.jar -C out/modulo1 .

### Ejecución
shell

### java --module-path mods:libs -m modulo1/com.paquete.Main

Donde mods es la carpeta de los JARs modulares y libs para dependencias.
7. Migración y compatibilidad

    Modo compatibilidad: el código clásico (sin module-info) se ejecuta en el classpath como antes. Al no tener descriptor, se coloca en el módulo sin nombre (unnamed module), el cual puede acceder a todo lo que esté en el classpath, pero los módulos explícitos no pueden requerirlo (solo puede ser accedido mediante requires especial o mediante la API de reflexión si se abre). Para migrar gradualmente, se puede empezar por añadir module-info.java a los componentes que se deseen encapsular, manteniendo otros en el classpath.

    --add-exports y --add-opens: flags de la JVM para abrir paquetes de módulos (tanto del JDK como propios) durante la migración, permitiendo accesos que el descriptor normal no permitiría. Ejemplo:
```text
    java --add-opens java.base/java.lang=ALL-UNNAMED ...
```

    Esta práctica es común en frameworks hasta que adopten completamente módulos.

### 8. Beneficios de JPMS en Java 21

    Rendimiento: arranque más rápido y menor consumo de memoria al cargar solo los módulos necesarios.

    Escalabilidad: creación de imágenes de ejecución personalizadas con jlink, que genera una JRE mínima con solo los módulos requeridos.

    Encapsulación fuerte: previene el uso de API internas del JDK (como sun.misc.Unsafe) o de las propias aplicaciones, mejorando la mantenibilidad y seguridad.

    Servicios y acoplamiento débil: el mecanismo de servicios permite desacoplar proveedores y consumidores sin dependencias directas, facilitando arquitecturas modulares orientadas a plugins.

### 9. Ejemplo completo

### Módulo api (interfaz)
```java
// src/api/module-info.java
module api {
    exports com.api;
}

java

// src/api/com/api/Saludable.java
package com.api;
public interface Saludable {
    String saludo();
}
```

### Módulo impl (proveedor)
```java
// src/impl/module-info.java
module impl {
    requires api;
    provides com.api.Saludable with com.impl.SaludableEnglish;
}

java

// src/impl/com/impl/SaludableEnglish.java
package com.impl;
import com.api.Saludable;
public class SaludableEnglish implements Saludable {
    public String saludo() { return "Hello!"; }
}
```

### Módulo app (consumidor)
```java
// src/app/module-info.java
module app {
    requires api;
    uses com.api.Saludable;
}

java

// src/app/com/app/App.java
package com.app;
import com.api.Saludable;
import java.util.ServiceLoader;

public class App {
    public static void main(String[] args) {
        ServiceLoader<Saludable> loader = ServiceLoader.load(Saludable.class);
        loader.findFirst().ifPresent(s -> System.out.println(s.saludo()));
    }
}
```

Compilación y ejecución:
```bash
javac -d out --module-source-path src $(find src -name "*.java")
java --module-path out -m app/com.app.App
```

Salida: Hello!


### 07.01 – TEXT BLOCKS

Los Text Blocks (bloques de texto) facilitan la escritura de cadenas literales que ocupan varias líneas sin necesidad de concatenaciones, escapes engorrosos ni saltos de línea explícitos. Esta característica fue previsualizada en Java 13‑14 y se convirtió en estándar definitivo en Java 15, por lo que en Java 17/21 está completamente estable.
Sintaxis básica

Se delimitan con tres comillas dobles """ de apertura y cierre:
```java
String html = """
    <html>
        <body>
            <p>Hola, mundo</p>
        </body>
    </html>
    """;
```

### Manejo de la indentación

El compilador elimina la indentación incidental automáticamente:

    Se toma como referencia el número de espacios en blanco comunes a todas las líneas (incluyendo las líneas vacías se consideran como infinitos espacios para el cálculo).

    Los espacios sobrantes se eliminan mediante String::stripIndent.

    La posición de la triple comilla de cierre controla la indentación adicional: si se coloca en una línea separada con una determinada sangría, esa sangría se suma a la referencia común.

Importante: si no se quiere que todo el bloque esté pegado a la izquierda, se coloca la triple comilla de cierre a la altura deseada.

Ejemplo:
```java
String poema = """
          Ella en la torre
          peinaba sus cabellos
          """;  // la indentación extra se elimina, el resultado será:
// "Ella en la torre\npeinaba sus cabellos\n"
```

Si se desea que la línea final tenga un salto de línea al final, se deja la triple comilla de cierre en la línea siguiente; si se pone al final de la última línea, el bloque no añade salto final:
```java
String sinSalto = """
    Hola""";   // " Hola\n"   -> ojo, hay un espacio antes de Hola, se conserva.
String conSalto = """
    Hola
    """;   // "Hola\n"
```

### Escapes dentro de text blocks

Los caracteres especiales siguen necesitando escape: \" para comillas dobles, \\ para barra invertida. Pero no es necesario escapar las comillas dobles individuales, solo secuencias de tres comillas (\""").

Además, Java 14 introdujo dos escapes nuevos pensados para text blocks:

    \ (barra invertida al final de línea): suprime el salto de línea (continuación de línea). Útil para escribir líneas muy largas sin interrumpir la cadena visualmente.

    \s (barra invertida seguida de s): espacio explícito. Evita que el algoritmo de indentación elimine espacios en blanco finales. Muy útil para forzar un espacio antes de un salto de línea o para preservar espacios finales.

```java
String query = """
    SELECT * \
    FROM usuarios \
    WHERE activo = true
    """;
// resulta: "SELECT * FROM usuarios WHERE activo = true\n"

String poema = """
    Rosas son rojas\s
    violetas azules\s
    """;
// con \s se conservan los espacios finales antes del salto de línea.
```

### Métodos útiles

    String::stripIndent() – elimina la indentación común (se llama implícitamente en el text block).

    String::translateEscapes() – interpreta secuencias de escape como \n, \t dentro de una cadena (ya aplicadas en tiempo de compilación en text blocks).

    String::formatted(Object... args) – equivalente a String.format, pero como método de instancia (Java 15+). Muy útil con text blocks:

```java
String saludo = """
    Hola %s,
    Bienvenido a %s.
    """.formatted(nombre, aplicacion);
```

### Text blocks y String Templates (Java 21 preview)

Con los String Templates (preview en Java 21) los text blocks se vuelven aún más expresivos:
```java
String nombre = "Ana";
String mensaje = STR."""
    Hola \{nombre},
    Esto es una interpolación.
    """;
```

### Buenas prácticas

    Usar text blocks para JSON, XML, SQL, HTML, etc.

    Colocar la triple comilla de cierre en su propia línea para controlar el sangrado.

    Utilizar \ para mantener la legibilidad de consultas largas sin saltos de línea no deseados.

    Recordar que todos los espacios en blanco son significativos. Cuidado con líneas que parecen vacías pero contienen espacios.

### 07.02 – SWITCH EXPRESSIONS

Las Switch Expressions fueron introducidas como preview en Java 12 y se estandarizaron en Java 14. Permiten usar switch como una expresión que devuelve un valor, evitando la típica necesidad de variables temporales y break. Aportan un código más conciso y eliminan la fuente de bugs por olvido de break.
Forma con flecha ->
```java
int diaSemana = 3;
String nombreDia = switch (diaSemana) {
    case 1 -> "Lunes";
    case 2 -> "Martes";
    case 3 -> "Miércoles";
    default -> "Desconocido";
};
```

La flecha asocia directamente el caso con el valor devuelto o con una sentencia; no se requiere break y no hay fall‑through accidental (solo se ejecuta ese caso). Cada caso puede contener una única expresión o un bloque de código que debe finalizar con yield para devolver un valor.
Bloque con yield

Si un caso requiere varias instrucciones antes de devolver el valor, se usa un bloque y la palabra clave yield:
```java
String categoria = switch (diaSemana) {
    case 1, 7 -> {
        System.out.println("Fin de semana!");
        yield "Descanso";
    }
    case 6 -> {
        System.out.println("Viernes");
        yield "Casi finde";
    }
    default -> "Laborable";
};
```

yield tiene un ámbito léxico; no se puede usar fuera de un bloque de caso en una expresión switch.
Múltiples etiquetas por caso

Se pueden agrupar varios casos utilizando comas:
```java
case 1, 2, 3 -> "Inicio de mes";
```

### Exhaustividad

El compilador exige que una expresión switch cubra todos los posibles valores del tipo sobre el que se aplica. Es decir, debe ser exhaustiva. Para enum, hay que cubrir todos los literales o incluir default; para int, con default basta. Si no es exhaustiva, error de compilación.

Diferencias con el switch tradicional (sentencia):
Tradicional	Expresión (Java 14+)
Cada case necesita break	Usa -> o yield
No devuelve valor	Devuelve un valor
Permite fall‑through	No hay fall‑through con ->
No tiene requisito de exhaustividad	Requiere exhaustividad
default opcional	default opcional pero puede ser necesario según el tipo
Uso como sentencia con flecha

También se puede usar la notación -> en un switch que actúa como sentencia (no devuelve valor):
```java
switch (comando) {
    case "iniciar" -> System.out.println("Iniciando...");
    case "parar"   -> System.out.println("Parando...");
    default        -> System.out.println("Comando desconocido");
}
```

En este caso no se requiere exhaustividad, es una sentencia tradicional con sintaxis moderna.
Combinación con Pattern Matching (Java 21)

En Java 21, el switch se expande con pattern matching, convirtiéndose en una herramienta central para el polimorfismo. Las switch expressions con patrones permiten descomponer records y comprobar tipos de forma elegante, heredando toda la potencia de las expresiones descritas aquí.
07.03 – PATTERN MATCHING PARA INSTANCEOF

El Pattern Matching para instanceof se estandarizó en Java 16 y elimina la ceremonia de comprobación + casting manual. Permite asignar una variable de patrón directamente dentro de la condición.
Sintaxis
```java
if (objeto instanceof String s) {
    // s es de tipo String aquí y se puede usar directamente
    System.out.println(s.toUpperCase());
}
```

La variable s queda vinculada solo si la comprobación es true. Es una variable local al bloque if, aunque también puede utilizarse en la parte derecha de una conjunción:
```java
if (objeto instanceof String s && s.length() > 5) {
    // s existe en la segunda parte del &&, y en el bloque
}
```

En un || no se puede usar s en el segundo operando porque quizá la primera parte sea false y s no estaría vinculada.
Ámbito y flujo de control

La variable de patrón se puede usar en cualquier punto donde el compilador esté seguro de que la comprobación ha sido exitosa. En estructuras condicionales complejas se aplica el análisis de flujo:
```java
if (!(objeto instanceof String s)) {
    // s no está disponible
    return;
}
// aquí s es seguro, porque si no hubiera sido String se habría retornado
System.out.println(s.length());
```

### Pattern matching con tipo y condición adicional (guarda)

No existe una guarda explícita en instanceof, pero el && permite añadir condiciones:
```java
if (objeto instanceof String s && s.length() > 5) {
    // ...
}
```

Aquí se está combinando la comprobación de tipo con una condición sobre la variable de patrón.
Patrones con instanceof y registros (Java 16+)

Aunque no se incluyó en el instanceof directamente el desglose de registros (eso es parte de los Record Patterns que llegaron más tarde como preview en Java 19 y final en Java 21), sí se puede usar instanceof con tipos genéricos mediante comodines acotados:
```java
if (shape instanceof Box<?> b) {
    // b es Box<?>
}
```

### Ventajas

    Código más limpio: una línea en lugar de tres (comprobación, declaración de variable, casting).

    Menor probabilidad de error de casting.

    Integración natural con nuevas estructuras como switch con patrones.

### Limitaciones

    No se puede usar instanceof con patrones sobre tipos genéricos concretos (List<String>), debido al borrado de tipos. Sí se permite con List<?> y luego se puede comprobar cada elemento.

    La variable de patrón es final implícitamente (no se puede reasignar).

### 07.04 – RECORDS

Los Records son clases inmutables transparentes, diseñadas específicamente para transportar datos de manera concisa. Fueron previsualizados en Java 14, segunda preview en 15 y se estandarizaron en Java 16. En Java 21 son una herramienta fundamental.
Declaración
```java
public record Persona(String nombre, int edad) {}
```

Con una sola línea se obtiene automáticamente:

    Campos privados y finales para cada componente (nombre, edad).

    Constructor canónico que recibe todos los componentes y los asigna.

    Métodos de acceso con el nombre del componente, sin get (nombre() y edad()).

    equals() y hashCode() basados en todos los componentes.

    toString() que incluye el nombre del registro y los valores de los componentes: "Persona[nombre=Ana, edad=25]".

### Constructor compacto (compact canonical constructor)

Permite validar, normalizar o hacer ajustes sin tener que volver a declarar todos los parámetros. La sintaxis omite los parámetros y asigna los campos al final de forma implícita:
```java
public record Persona(String nombre, int edad) {
    public Persona {  // compact constructor
        if (edad < 0) throw new IllegalArgumentException("Edad negativa");
        nombre = nombre.trim(); // "nombre" se refiere al campo, no al parámetro
    }
}
```

No se puede reasignar los campos fuera del constructor compacto; son final. Tampoco se permite un constructor adicional que llame a this(...) si no se respeta la inicialización de todos los campos.
Restricciones

    Son finales implícitamente, no pueden extender otra clase (heredan de java.lang.Record).

    No pueden ser abstractas.

    Los campos de instancia adicionales no están permitidos (ni se pueden declarar). Solo los componentes del registro.

    Se pueden declarar campos estáticos, métodos estáticos y métodos de instancia adicionales.

    Pueden implementar interfaces.

    No se pueden declarar métodos set de modificación (ya que los campos son final), pero sí métodos que devuelvan nuevas instancias con valores modificados (estilo inmutable):

```java
public Persona conEdad(int nuevaEdad) {
    return new Persona(this.nombre, nuevaEdad);
}
```

### Características avanzadas

    Se pueden sobrescribir los accesores si se desea ocultar o transformar el valor (aunque se pierde transparencia). Por ejemplo, para devolver una copia defensiva:

```java
public List<String> hobbies() {
    return List.copyOf(hobbies); // supuesto que hobbies es List<String>
}

    Se pueden añadir constructores adicionales que llamen al canónico con this(...).
```

### Integración con patrones y switch

Los registros forman la base de los Record Patterns (Java 19 preview, final en Java 21), que permiten descomponer un registro directamente en el switch o instanceof:
```java
if (figura instanceof Circulo(double radio)) {
    // radio es la componente del registro
}
```

Y en el switch con exhaustividad cuando se usan con sealed types.
Cuándo usar records

    DTOs (Data Transfer Objects).

    Mensajes o comandos en arquitecturas CQRS.

    Claves compuestas en mapas.

    Valores retornados de consultas.

    Cualquier estructura de datos inmutable cuyo único propósito sea agrupar valores.

### Comparación con Lombok o @Data

Los registros son una solución nativa que no requiere anotaciones ni procesadores. A diferencia de @Data, no son mutables (no tienen setters) y son adecuados solo para inmutabilidad.
07.05 – SEALED CLASSES (CLASES SELLADAS)

Las Clases Selladas permiten controlar explícitamente qué subclases pueden extender una clase o qué implementaciones tiene una interfaz. Se estandarizaron en Java 17. Son el complemento perfecto para los records y el pattern matching exhaustivo.
Declaración
```java
public sealed class Figura permits Circulo, Rectangulo, Triangulo {
    // cuerpo de la clase sellada
}
```

La clase Figura declara que solo las clases listadas en permits pueden extenderla. Las subclases permitidas deben estar en el mismo módulo (o paquete si no se usa módulo) y a su vez deben elegir uno de estos modificadores:

    final → no se puede extender más.

    sealed → sigue restringiendo la herencia (con su propio permits).

    non‑sealed → permite que cualquier clase pueda extenderla (rompe el sellado).

Ejemplo:
```java
sealed interface Expr permits Suma, Resta, Num {}
record Suma(Expr izq, Expr der) implements Expr {}
record Resta(Expr izq, Expr der) implements Expr {}
final class Num implements Expr { int valor; }
```

O bien usando records y clases finales.
Reglas

    La clase sellada y sus subclases permitidas deben pertenecer al mismo módulo (o al mismo paquete sin módulos). No se pueden declarar subclases en otro módulo sin usar permits explícito, pero aun así deben ser del mismo módulo.

    Si las subclases son anidadas o están en el mismo archivo, se puede omitir permits y el compilador las deduce:

```java
sealed class Op {
    final class A extends Op {}
    final class B extends Op {}
}
```

    No se pueden declarar permits con clases que no pertenezcan al mismo módulo/paquete.

    La clase sellada puede ser abstracta.

    Las interfaces también pueden ser selladas.

### Exhaustividad en el switch

La gran ventaja es que el compilador conoce todas las posibilidades, por lo que en un switch con pattern matching no se necesita default si se cubren todos los permits:
```java
double evaluar(Expr e) {
    return switch (e) {
        case Suma(var i, var d) -> evaluar(i) + evaluar(d);
        case Resta(var i, var d) -> evaluar(i) - evaluar(d);
        case Num n          -> n.valor;
    };  // sin default, exhaustivo
}
```

Esto hace que los añadidos futuros a la jerarquía sellada provoquen un error de compilación en los switch que no los contemplen, aumentando la robustez del código (comportamiento deseable en patrones modelo‑vista o intérpretes).
Compatibilidad con instanceof

El patrón de instanceof con tipos sellados permite comprobaciones en cascada; también el compilador puede inferir exhaustividad en flujos de control si se usa una cadena de if‑else if. Sin embargo, el switch es la forma más clara y concisa.
Cuándo usar clases selladas

    Modelado de tipos algebraicos (sum types) junto con records.

    Jerarquías de dominio restringidas (p.ej., estados de un pedido: Pendiente, Enviado, Entregado, Cancelado).

    Reemplazo de enumeraciones complejas que necesitan comportamientos distintos por estado.

    API internas en las que no se desea que terceros extiendan ciertas clases.

### Relación con records

A menudo se combinan sealed interface con varios record que la implementan. Esto permite un modelado funcional muy potente y seguro para manipular datos.
Ejemplo completo
```java
sealed interface Figura permits Rectangulo, Circulo, Triangulo {}
record Rectangulo(double ancho, double alto) implements Figura {}
record Circulo(double radio) implements Figura {}
final class Triangulo implements Figura { double base, altura; } // o record

// Uso
double area(Figura f) {
    return switch (f) {
        case Rectangulo(var a, var al) -> a * al;
        case Circulo(var r) -> Math.PI * r * r;
        case Triangulo t -> (t.base * t.altura) / 2;
    };
}
```

### 08.01 – VIRTUAL THREADS (PROJECT LOOM, FINAL)

Los hilos virtuales son la respuesta de Java para la programación concurrente masiva de una manera sencilla y eficiente. Se integran sin cambios en la gran mayoría del código existente.
¿Qué son?

Los hilos del sistema operativo (hilos de plataforma) son recursos costosos (típicamente ~1 MB de pila por hilo). Los hilos virtuales son hilos ligeros gestionados por la JVM que se multiplexan sobre un pequeño número de hilos de plataforma (carriers). Cuando un hilo virtual se bloquea (por I/O, sleep, espera en un lock), su carrier puede ejecutar otro hilo virtual, liberando el recurso del SO.

Esto permite el modelo «un hilo por petición» escalando a millones de tareas concurrentes sin el coste de memoria ni de cambio de contexto.
Creación y uso
Mediante Thread.startVirtualThread
```java
Thread.startVirtualThread(() -> {
    System.out.println("Ejecutando en hilo virtual: " + Thread.currentThread());
});
```

### Con Executors.newVirtualThreadPerTaskExecutor()

Devuelve un ExecutorService que asigna un nuevo hilo virtual a cada tarea:
```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> procesar());
    executor.submit(() -> recuperar());
} // se cierra el executor tras las tareas
```

### Con el nuevo Thread.Builder (API más flexible)
```java
Thread.Builder builder = Thread.ofVirtual()
        .name("worker-", 0)
        .uncaughtExceptionHandler((t, e) -> e.printStackTrace());
Thread hilo = builder.start(() -> { ... });
```

### Características importantes

    Los hilos virtuales son daemon por defecto y no tienen prioridad (no aplica).

    No se deben agrupar en pools: crear un hilo virtual es tan barato (~1 KB) que se crean y descartan según necesidad. La API del executor proporciona un pool conceptual que genera uno nuevo por tarea.

    No hay problema si un hilo virtual bloquea (con sleep, LockSupport.park(), I/O síncrona). La JVM desacopla el carrier.

    Los problemas tradicionales con ThreadLocal y synchronized son más evidentes con millones de hilos: synchronized en grano grueso puede causar pinning (el hilo virtual se ancla al carrier, impidiendo su liberación). Se recomienda sustituir synchronized por ReentrantLock en nuevos desarrollos de alta concurrencia.

    Herramientas: jcmd, jstack muestran hilos virtuales sin coste.

### Ejemplo de servicio web
```java
try (var serverSocket = new ServerSocket(8080)) {
    while (true) {
        Socket socket = serverSocket.accept();
        Thread.startVirtualThread(() -> handleRequest(socket));
    }
}
```

Con miles de conexiones simultáneas, este código sigue funcionando con un consumo mínimo de recursos.
Migración

No es necesario reescribir código legacy. Cualquier aplicación que use ExecutorService, Thread o frameworks como Spring Boot 3.2+ (activando spring.threads.virtual.enabled=true) puede aprovechar los hilos virtuales casi de inmediato.

    Estado: Definitivo en Java 21. Sin necesidad de flags adicionales.

### 08.02 – SEQUENCED COLLECTIONS (FINAL)

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

### 08.03 – RECORD PATTERNS (FINAL)

Los Record Patterns permiten descomponer un registro en sus componentes directamente después de una comprobación de tipo, ya sea en un instanceof o en un case de un switch. Se basa en los registros y el pattern matching ya existente.
Uso en instanceof
```java
record Punto(double x, double y) {}

void imprimir(Object obj) {
    if (obj instanceof Punto(double x, double y)) {
        System.out.println("Coordenadas: " + x + ", " + y);
    }
}
```

La variable x e y se vinculan directamente a los componentes del registro, con su tipo inferido.
Uso en switch
```java
sealed interface Figura permits Circulo, Rectangulo {}
record Circulo(double radio) implements Figura {}
record Rectangulo(double ancho, double alto) implements Figura {}

double area(Figura f) {
    return switch (f) {
        case Circulo(var r) -> Math.PI * r * r;
        case Rectangulo(var a, var h) -> a * h;
    };
}

var r equivale a double r, pero también se puede poner el tipo explícito.
Patrones anidados
```

Se pueden descomponer registros dentro de registros:
```java
record Punto(double x, double y) {}
record Segmento(Punto inicio, Punto fin) {}

if (s instanceof Segmento(Punto(var x1, var y1), Punto(var x2, var y2))) {
    // uso directo de x1, y1, x2, y2
}
```

La legibilidad y la seguridad de tipos aumentan drásticamente.
when clauses (guardas)

No hay guardas en instanceof (se usa && adicional), pero en el switch los patrones de registro pueden combinarse con when (parte del pattern matching del switch) para refinar el caso.
Exhaustividad con tipos sellados

Cuando se usan registros que implementan interfaces selladas, el compilador asegura que el switch cubra todos los casos, y los patrones de registro permiten extraer la información de golpe.

    Estado: Definitivo en Java 21. Es la culminación del pattern matching estructural.

### 08.04 – PATTERN MATCHING FOR SWITCH (FINAL)

El Pattern Matching para switch convierte a esta estructura en una potente herramienta de despacho polimórfico. Se unifican los patrones de tipo, los patrones de registro, los patrones de array y el manejo explícito de null.
Características principales

    switch sobre cualquier objeto, no solo sobre números, strings y enums.

    Cada case especifica un patrón: de tipo, de registro, de array o de literal.

    Exhaustividad: el compilador garantiza que todos los casos posibles están cubiertos si el selector es una clase o interfaz sellada (o se incluye default).

    Manejo de null explícito con case null -> .... Si no se incluye y la variable es null, se lanza NullPointerException.

    Se puede usar when para añadir guardas a cualquier patrón.

### Ejemplo completo
```java
Object obj = obtenerAlgo();
switch (obj) {
    case null -> System.out.println("Es nulo");
    case String s when s.length() > 5 -> System.out.println("String largo: " + s);
    case String s -> System.out.println("String corto: " + s);
    case Integer i -> System.out.println("Entero: " + (i * i));
    case int[] arr -> System.out.println("Array de ints con " + arr.length + " elementos");
    default -> System.out.println("Tipo desconocido");
}

    Los casos se evalúan en orden. El más específico debe ir primero (por ejemplo, String s when ... antes que String s).
```

    Si se usa switch como expresión, debe devolver un valor en cada rama y ser exhaustivo:

```java
String desc = switch (obj) {
    case null -> "nulo";
    case String s -> "texto";
    default -> "desconocido";
};
```

### Con tipos sellados y registros
```java
sealed interface Op permits Add, Mul {}
record Add(Op left, Op right) implements Op {}
record Mul(Op left, Op right) implements Op {}

int eval(Op op) {
    return switch (op) {
        case Add(var l, var r) -> eval(l) + eval(r);
        case Mul(var l, var r) -> eval(l) * eval(r);
    };
}
```

El compilador sabe que Op solo puede ser Add o Mul, por lo que no necesita default.
Patrones de array

case int[] arr -> o case String[] arr -> permite capturar el array y usarlo directamente.

    Estado: Definitivo en Java 21. La evolución del switch se completa con esta poderosa función.

### 08.05 – STRING TEMPLATES (PREVIEW)

Los String Templates permiten la interpolación de expresiones dentro de cadenas de forma segura, evitando concatenaciones manuales y riesgos de inyección.
Sintaxis

Se utiliza un procesador de plantillas (normalmente STR) seguido de un punto y un bloque de texto delimitado por """ (o también con comillas simples):
```java
String nombre = "Mundo";
String mensaje = STR."Hola \{nombre}!";
// Resultado: "Hola Mundo!"
```

Las expresiones van entre \{ y }. Pueden ser cualquier expresión Java que devuelva un valor convertible a String.
Procesadores incorporados

    STR: reemplaza cada expresión por su representación toString().

    FMT: similar a STR pero permite especificar formatos al estilo printf en las expresiones:
```java
    double precio = 123.456;
    String texto = FMT."Precio: %.2f\{precio}";
```

    RAW: no procesa el resultado, devuelve un StringTemplate para inspeccionar las partes y valores antes de procesarlos. Útil para crear procesadores personalizados.

### Procesadores personalizados

Se puede crear un procesador implementando StringTemplate.Processor<R, E>:
```java
var SQL = StringTemplate.Processor.of((template) -> {
    // template.fragments() y template.values() para construir sentencia
    return new SQLQuery(...);
});
SQLQuery q = SQL."SELECT * FROM \{tabla} WHERE id = \{id}";
```

### Seguridad

A diferencia de la concatenación ingenua, los procesadores pueden escapar caracteres especiales o aplicar políticas de seguridad. Por ejemplo, un procesador para SQL podría parametrizar automáticamente las expresiones, evitando inyección SQL.
Text blocks y templates

Las plantillas funcionan perfectamente con text blocks:
```java
String json = STR."""
    {
        "name": "\{nombre}",
        "age": \{edad}
    }
    """;
```

### Consideraciones

    Es una feature en preview; requiere --enable-preview para compilar y ejecutar.

    Los nombres de procesadores (STR, FMT, RAW) se importan implícitamente (están en java.lang).

    No es un simple azúcar sintáctico: la separación entre fragmentos literales y valores permite construir DSLs seguros.

    Estado: Preview en Java 21. Activar con --enable-preview --source 21.

### 08.06 – SCOPED VALUES (PREVIEW)

Los Scoped Values son una alternativa moderna a ThreadLocal para compartir datos inmutables dentro de un hilo y sus hijos (virtuales o no), especialmente en concurrencia estructurada. Ofrecen mejor rendimiento y un ciclo de vida claramente delimitado.
Problema de ThreadLocal

    Acoplamiento implícito: cualquier código dentro del hilo puede leer/modificar un ThreadLocal.

    Dificultad en la limpieza (memory leaks si no se elimina adecuadamente, especialmente con pools de hilos).

    Coste en hilos virtuales: heredar ThreadLocal al crear un hilo virtual añade sobrecarga.

### Uso de ScopedValue
```java
final static ScopedValue<String> USUARIO_ACTUAL = ScopedValue.newInstance();
```

### ScopedValue.where(USUARIO_ACTUAL, "admin").run(() -> {
    System.out.println("Usuario: " + USUARIO_ACTUAL.get());
});
// Fuera del bloque, USUARIO_ACTUAL no está definido (llamar a get() lanza NoSuchElementException)

where crea un binding (asociación) que dura durante la ejecución del Runnable proporcionado. Los hilos hijos heredan automáticamente el valor, pero no pueden cambiarlo. Es inmutable.
Vinculación con hilos virtuales y concurrencia estructurada
```java
ScopedValue.where(USUARIO_ACTUAL, "admin").run(() -> {
    Thread.startVirtualThread(() -> {
        // dentro del hilo virtual, USUARIO_ACTUAL.get() == "admin"
    });
});
```

El valor se hereda sin sobrecarga adicional, ya que los hilos virtuales pueden compartir el contenedor de scoped values de manera eficiente.
API adicional

    ScopedValue.getWhere(ScopedValue<T>, T, Supplier<Runnable>) para obtener un Runnable con un binding alternativo de manera funcional.

    ScopedValue.where(..., ...).call(() -> ...) para tareas que devuelven valor (con Callable).

### Ventajas sobre ThreadLocal

    Inmutabilidad: los valores no se pueden cambiar una vez establecidos.

    Ámbito visible: el binding solo existe dentro de la ejecución del bloque, imposible de olvidar limpiar.

    Mejor rendimiento y escalabilidad (especialmente en hilos virtuales).

    Herencia clara sin fugas.

    Estado: Preview en Java 21. Habilitar con --enable-preview.

### 08.07 – STRUCTURED CONCURRENCY (PREVIEW)

La Concurrencia Estructurada busca tratar varias tareas concurrentes como una unidad de trabajo, confinando su ciclo de vida a un bloque sintáctico. Esto facilita la cancelación, el manejo de errores y la observabilidad.
Idea central

En lugar de lanzar hilos y unirlos manualmente, se usa un StructuredTaskScope que controla las subtareas. Cuando el bloque termina, el scope espera a que todas las tareas finalicen (o las cancela si falla alguna) antes de continuar. Se asemeja a un try-with-resources.
Ejemplo con ShutdownOnFailure
```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> tarea1 = scope.fork(() -> leerBaseDatos());
    Future<Integer> tarea2 = scope.fork(() -> calcularEstadisticas());

    scope.join();            // espera a que todas las subtareas terminen o fallen
    scope.throwIfFailed();   // si alguna falló, lanza la excepción

    String resultado1 = tarea1.resultNow();
    int resultado2 = tarea2.resultNow();
    return combinar(resultado1, resultado2);
}

    fork lanza la tarea y devuelve un Future.

    join() bloquea hasta que todas las tareas finalicen o alguna falle (según política).

    throwIfFailed() propaga cualquier excepción ocurrida en las subtareas.
```

### Políticas de manejo de errores

    ShutdownOnFailure: si cualquier subtarea falla, se cancelan las demás y la excepción se lanza en throwIfFailed.

    ShutdownOnSuccess: obtiene el primer resultado exitoso y cancela las otras (útil para consultas redundantes).

    Se pueden crear políticas propias extendiendo StructuredTaskScope.

### Ventajas

    Árbol de tareas observable: la relación padre‑hijo queda reflejada en los volcados de hilos y herramientas de monitoreo.

    Cancelación automática: al cerrar el scope, se cancelan las subtareas aún en ejecución.

    Código más simple: sin CountDownLatch, ExecutorService manual ni colecciones externas para recolectar resultados.

    Integración con hilos virtuales para máxima escalabilidad.

### Consideraciones

    Al ser preview, puede haber cambios en la API final.

    Requiere habilitar --enable-preview.

    Los Future devueltos por fork no son los mismos Future de java.util.concurrent (son internos del scope), y no se deben pasar fuera del bloque del scope.

    Estado: Preview en Java 21.

### 08.08 – FOREIGN FUNCTION & MEMORY API (PREVIEW)

La Foreign Function & Memory API (FFM API) reemplaza a JNI (Java Native Interface) para interactuar con código nativo y gestionar memoria fuera del heap de manera segura y eficiente. Unifica en una sola API el acceso a funciones externas y la manipulación de memoria nativa.
Componentes principales

    MemorySegment: representa una región continua de memoria (nativa o en el heap). Puede ser cero-copy con arrays de bytes, o provenir de malloc, etc.

    Arena: controla el ciclo de vida de los segmentos de memoria (similar a un asignador). Tipos:

        Arena.global(): memoria que nunca se libera.

        Arena.ofAuto(): liberación gestionada por el garbage collector.

        Arena.ofConfined() y Arena.ofShared(): control manual o thread‑safe.

    ValueLayout: describe tipos básicos (JAVA_INT, JAVA_LONG, etc.) para leer/escribir en segmentos.

    FunctionDescriptor y Linker: permiten describir funciones nativas y llamarlas.

### Acceso a memoria nativa
```java
try (var arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(10); // 10 bytes nativos
    segment.set(ValueLayout.JAVA_INT, 0, 123); // escribe un int en offset 0
    int valor = segment.get(ValueLayout.JAVA_INT, 0); // lee
}
```

Los segmentos proporcionan acceso tipado y seguro (con bounds checks en modo depuración).
Llamada a funciones nativas (downcall)
```java
Linker linker = Linker.nativeLinker();
MethodHandle strlen = linker.downcallHandle(
    linker.defaultLookup().find("strlen").get(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);
MemorySegment str = arena.allocateFrom("Hello"); // guarda una cadena C
long len = (long) strlen.invoke(str);
```

### Exposición de funciones Java a código nativo (upcall)

Es posible crear punteros a funciones Java que sean llamables desde C.
Seguridad y rendimiento

    Acceso restringido por defecto; se requieren permisos o flags de JVM para operaciones nativas.

    Mejor rendimiento que JNI al evitar transiciones complejas y permitir optimizaciones del compilador JIT.

    La API está diseñada para ser amigable con los Value types (futuros) y el vector API.

    Estado: Preview en Java 21 (tercera incubación). Requiere --enable-preview.

### 08.09 – UNNAMED PATTERNS AND VARIABLES (PREVIEW)

Los Patrones y Variables sin nombre permiten usar el carácter _ para declarar variables o componentes de patrón cuyo valor no se necesita, mejorando la legibilidad y reduciendo advertencias.
Unnamed variable (_)

En cualquier lugar donde se declare una variable local, parámetro de lambda o catch, se puede usar _ si el valor no se usa:
```java
try (var _ = ScopedValue.where(FLAG, true)) {
    // No necesitamos la variable del scope auto-closeable
}

// En un catch
try { ... } catch (Exception _) {
    // No nos interesa la excepción concreta
}

// En lambdas
lista.stream().collect(Collectors.toMap(k -> k, _ -> 1)); // el valor no importa

// En bucles for-each
for (var _ : lista) {
    // solo interesa contar iteraciones
}
```

El compilador no emite advertencias por no uso, y la variable no consume memoria significativa.
Unnamed patterns (_)

En patrones de registro o de switch, se puede usar _ para componentes que no interesan:
```java
record Rectangulo(double ancho, double alto) {}
if (figura instanceof Rectangulo(double _, double alto)) {
    System.out.println("Alto: " + alto);
}

switch (figura) {
    case Rectangulo(var _, var alto) -> "Alto: " + alto;
    ...
}
```

También se puede usar en patrones de registro anidados: Segmento(Punto(_, _), Punto(var x, var y)).
Unnamed pattern en case

En un switch, un pattern _ puede funcionar como default pero capturando cualquier valor sin vincular la variable:
```java
case _ -> System.out.println("Caso por defecto");
```

A diferencia de default, _ es un patrón que coincide con todo, y si hay varios case _, se aplica el orden.
Beneficios

    Claridad: se documenta explícitamente que el valor no se usa.

    Menos contaminación del espacio de nombres.

    Mejora en las revisiones de código.

    Estado: Preview en Java 21. Habilitar con --enable-preview.

### 09 – CONCURRENCIA AVANZADA EN JAVA 21

Esta sección está dedicada a la concurrencia clásica y moderna en Java. Aunque los hilos de plataforma y los Executors llevan años con nosotros, entenderlos a fondo es imprescindible para apreciar las innovaciones de Java 21 y para combinar ambas aproximaciones en aplicaciones reales. A continuación, se presentan los contenidos detallados para cada uno de los tres archivos.
09.01 – HILOS DE PLATAFORMA (PLATFORM THREADS)
1. Modelo de hilos tradicional

Un hilo de plataforma es un hilo del sistema operativo envuelto por la JVM. Cada uno tiene su propia pila (típicamente ~1 MB) y es gestionado directamente por el SO. Crear miles de estos hilos consume una cantidad de memoria prohibitiva y el cambio de contexto puede degradar el rendimiento.

En Java, la clase java.lang.Thread representa un hilo de plataforma (también llamado kernel thread). Aunque en Java 21 existe Thread.ofVirtual(), el constructor clásico new Thread(...) sigue creando un hilo de plataforma.
2. Ciclo de vida de un hilo de plataforma

Los estados definidos en Thread.State son:

    NEW: creado pero no iniciado (start() no llamado).

    RUNNABLE: ejecutándose o listo para ejecutarse.

    BLOCKED: esperando adquirir un monitor (bloqueo intrínseco con synchronized).

    WAITING: esperando indefinidamente a que otro hilo realice una acción (Object.wait(), Thread.join(), LockSupport.park()).

    TIMED_WAITING: espera con tiempo límite (sleep(), wait(timeout), join(timeout), etc.).

    TERMINATED: el hilo ha finalizado su ejecución.

3. Creación de hilos de plataforma
Extendiendo Thread
```java
class MiHilo extends Thread {
    @Override public void run() {
        System.out.println("Hilo ejecutándose: " + Thread.currentThread().getName());
    }
}
MiHilo h = new MiHilo();
h.start(); // inicia el nuevo hilo
```

### Implementando Runnable
```java
Runnable tarea = () -> System.out.println("Tarea en hilo: " + Thread.currentThread().getName());
new Thread(tarea).start();
```

Desde Java 8 podemos usar lambdas o referencias a métodos para definir el Runnable.
4. Propiedades y métodos útiles

    setName(String) / getName(): nombre del hilo.

    setDaemon(boolean): un hilo demonio termina cuando todos los hilos no demonio han finalizado.

    setPriority(int): prioridad (1..10), solo una sugerencia al SO.

    join(): espera a que el hilo termine.

    interrupt(): envía una señal de interrupción. El hilo destino debe cooperar verificando Thread.interrupted() o manejando InterruptedException.

    Thread.sleep(long): suspende el hilo actual durante un tiempo; puede lanzar InterruptedException.

### 5. Sincronización básica
synchronized

Mecanismo de bloqueo intrínseco sobre objetos.

    Método sincronizado:
```java
    public synchronized void incrementar() {
        contador++;
    }
```

    Bloque sincronizado:
```java
    synchronized (objetoBloqueo) {
        // sección crítica
    }
```

wait(), notify(), notifyAll() deben llamarse dentro de un bloque synchronized y sobre el objeto de bloqueo.
volatile

Garantiza visibilidad de los cambios en una variable entre hilos, pero no atómica.
```java
private volatile boolean detenido = false;
public void detener() { detenido = true; }
```

### 6. Problemas clásicos

    Condiciones de carrera: múltiples hilos acceden desordenadamente a datos compartidos.

    Deadlock: dos o más hilos se bloquean mutuamente esperando cerrojos que nunca liberan.

    Starvation: un hilo nunca obtiene acceso a un recurso.

    Inanición de hilos: mal uso de notify() en lugar de notifyAll().

### 7. Limitaciones del modelo de plataforma

    Escalabilidad: un hilo por petición no escala a decenas de miles de conexiones simultáneas.

    Consumo de recursos: memoria de pila y coste de creación.

    Gestión explícita: hay que definir pools, sincronización, etc.

Estas limitaciones motivaron la evolución hacia los Executors (siguiente tema) y, en Java 21, hacia los hilos virtuales.
09.02 – EXECUTORS Y FUTURES

El framework Executors (desde Java 5) desacopla la definición de una tarea de la mecánica de ejecución. Permite manejar pools de hilos, programación periódica y obtener resultados de manera asincrónica.
1. La interfaz Executor
```java
void execute(Runnable command);
```

La implementación más simple ejecuta el comando en un hilo nuevo o directamente en el invocador. No se usa casi nunca directamente; su subinterfaz ExecutorService es la relevante.
2. ExecutorService y sus implementaciones

ExecutorService añade métodos para el ciclo de vida:

    submit(Callable<T>) y submit(Runnable) devuelven un Future.

    invokeAll(), invokeAny().

    shutdown() y shutdownNow().

Obtenemos instancias mediante la clase Executors (factory methods):

    Executors.newFixedThreadPool(int): pool con un número fijo de hilos.

    Executors.newCachedThreadPool(): crea hilos bajo demanda y los reutiliza.

    Executors.newSingleThreadExecutor(): un único hilo que ejecuta tareas secuencialmente.

    Executors.newScheduledThreadPool(int): para tareas programadas o periódicas.

    Executors.newWorkStealingPool(): pool basado en ForkJoinPool.

    En Java 21: Executors.newVirtualThreadPerTaskExecutor(): crea un hilo virtual por cada tarea.

3. Callable y Future

Callable<V> es como Runnable pero devuelve un resultado y puede lanzar excepciones comprobadas.
```java
Callable<Integer> tarea = () -> {
    Thread.sleep(100);
    return 42;
};
Future<Integer> futuro = executor.submit(tarea);
// ... hacer otras cosas
Integer resultado = futuro.get(); // bloquea hasta que esté disponible
```

Future ofrece:

    get() con o sin timeout.

    cancel(boolean): intenta cancelar la tarea.

    isDone(), isCancelled().

### 4. Limitaciones de Future

    No hay forma de componer múltiples futures sin bloqueos manuales.

    No se puede reaccionar a la finalización de una tarea de manera no bloqueante (salvo encuestas).

    Errores difíciles de manejar en cadenas.

### 5. CompletableFuture (Java 8+)

CompletableFuture<T> implementa Future y CompletionStage, proporcionando un modelo de programación asíncrona rico y no bloqueante.
Creación
```java
CompletableFuture.supplyAsync(() -> calcular());
CompletableFuture.runAsync(() -> enviarMensaje());
```

Sin especificar Executor usan el ForkJoinPool.commonPool(); se puede pasar un Executor.
Composición

    thenApply(Function): transforma el resultado.

    thenAccept(Consumer): consume el resultado.

    thenRun(Runnable): ejecuta acción tras finalizar, sin usar el resultado.

    thenCompose(Function): encadena otro CompletableFuture (flatMap).

    thenCombine(other, BiFunction): combina dos futures independientes.

```java
CompletableFuture<String> futuro = CompletableFuture
    .supplyAsync(() -> obtenerId())
    .thenCompose(id -> CompletableFuture.supplyAsync(() -> buscarPorId(id)))
    .thenApply(entidad -> entidad.getNombre())
    .exceptionally(ex -> "Error: " + ex.getMessage());
```

### Métodos de coordinación

    allOf(...): espera a que todos los futures especificados terminen.

    anyOf(...): devuelve el resultado del primero que termine.

### Completado manual

    complete(valor): completa el futuro con un valor si aún no se ha completado.

    completeExceptionally(Throwable): completa con una excepción.

### 6. ScheduledExecutorService

Permite programar tareas para ejecutarse tras un retraso o de forma periódica:

    schedule(Callable, delay, unit): ejecución única diferida.

    scheduleAtFixedRate(Runnable, delay, period, unit): tarea periódica a intervalos regulares, sin importar el tiempo de ejecución.

    scheduleWithFixedDelay(Runnable, delay, delay, unit): tarea periódica con retraso entre finalización e inicio de la siguiente.

### 7. Fork/Join Framework (breve)

ForkJoinPool está optimizado para trabajo que se puede dividir recursivamente (divide y vencerás). Es la base del parallelStream(). Se programa con RecursiveTask<V> o RecursiveAction.
8. El nuevo Executor de hilos virtuales (Java 21)

Executors.newVirtualThreadPerTaskExecutor() devuelve un ExecutorService que crea un nuevo hilo virtual por cada tarea. Es una recomendación para la mayoría de las cargas de trabajo de alta concurrencia, ya que combina la facilidad de uso de un Executor con la escalabilidad de los hilos virtuales. Internamente, cada tarea obtiene su propio hilo virtual; no hay pool de hilos virtuales (no es necesario). Ejemplo:
```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000; i++) {
        executor.submit(() -> procesarPeticion());
    }
}
```

### 09.03 – VIRTUAL THREADS Y CONCURRENCIA ESTRUCTURADA EN PROFUNDIDAD
1. Arquitectura interna de los hilos virtuales

Los hilos virtuales se implementan sobre una pequeña cantidad de hilos de plataforma llamados carriers. Cuando un hilo virtual ejecuta una operación que lo bloquearía (I/O, sleep, park), la JVM desmonta el hilo virtual del carrier y lo registra en un heap interno hasta que la condición se complete. El carrier queda libre para ejecutar otro hilo virtual.

    El programador (scheduler) de hilos virtuales es ForkJoinPool con un modo de paralelismo que por defecto iguala al número de procesadores disponibles.

    La pila del hilo virtual se almacena en el heap como objetos Java; al cambiar de contexto solo se intercambian referencias (muy eficiente).

    Se puede monitorear con jcmd y jstack; los volcados muestran hilos virtuales sin coste adicional.

2. Modelo de uso recomendado

    No reutilizar hilos virtuales: son desechables y muy baratos (~1 KB de sobrecarga inicial). Se crea uno por tarea.

    No usar pools: ni Executors.newFixedThreadPool con hilos virtuales; usar directamente el executor virtual.

    Cuidado con el pinning: si un hilo virtual ejecuta código que no se puede desmontar (por ejemplo, un bloque synchronized que no se libera pronto, o un método nativo JNI que bloquea), el carrier queda ocupado y puede reducir la capacidad de concurrencia. En Java 21, algunas situaciones comunes de pinning se han eliminado o mitigado (p.ej., Object.wait() libera el carrier). Para evitar pinning en secciones críticas largas, usar ReentrantLock en lugar de synchronized.

    ThreadLocal: los hilos virtuales soportan ThreadLocal, pero su uso excesivo puede incrementar la memoria porque cada hilo virtual mantiene su copia. En su lugar, se recomiendan Scoped Values (preview) para datos de ámbito controlado.

3. Ejemplo de migración de un servidor

Antes (con pool de plataforma):
```java
ExecutorService pool = Executors.newFixedThreadPool(200);
while (true) {
    Socket s = server.accept();
    pool.submit(() -> manejar(s));
}
```

Ahora (con hilos virtuales):
```java
while (true) {
    Socket s = server.accept();
    Thread.startVirtualThread(() -> manejar(s));
}
```

El código se simplifica, el límite pasa a ser la memoria general de la JVM en lugar de los hilos del SO.
4. Concurrencia estructurada (Structured Concurrency, preview)

La concurrencia estructurada extiende el concepto de hilos virtuales al agrupar varias tareas relacionadas como una unidad de trabajo, confinando su ciclo de vida a un bloque léxico. Se implementa mediante StructuredTaskScope (en java.util.concurrent, preview en Java 21).
StructuredTaskScope.ShutdownOnFailure

El más común: si una subtarea falla, se cancelan las demás y se propaga la excepción.
```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> pedido = scope.fork(() -> obtenerPedido(id));
    Future<Cliente> cliente = scope.fork(() -> obtenerCliente(idCliente));

    scope.join();           // espera a que todas las subtareas terminen o falle alguna
    scope.throwIfFailed();  // si alguna falló, lanza la excepción

    // Aquí ambas tareas han finalizado con éxito
    return new Factura(cliente.resultNow(), pedido.resultNow());
}

    fork(Callable) devuelve un Future interno que NO debe salir del scope.

    join() bloquea al hilo virtual actual de manera eficiente. Internamente, la JVM puede desmontar el hilo virtual mientras espera.
```

    Si lanza ThrowIfFailed, las excepciones de las subtareas se agrupan adecuadamente.

### StructuredTaskScope.ShutdownOnSuccess

Útil para obtener el primer resultado exitoso de un conjunto de tareas redundantes y cancelar las otras.
```java
try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
    scope.fork(() -> consultarApi1());
    scope.fork(() -> consultarApi2());

    scope.join();
    String resultado = scope.result();  // obtiene el resultado del primero exitoso
    // las demás tareas se cancelaron automáticamente
}
```

### Custom policies

Podemos extender StructuredTaskScope y sobrescribir handleComplete(Future) para decidir cuándo detener otras tareas.
Integración con Scoped Values

Los valores de ámbito se heredan automáticamente dentro de las subtareas lanzadas por el scope.
```java
ScopedValue.where(TRACE_ID, trace).run(() -> {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        scope.fork(() -> logWithTrace());
        ...
    }
});
```

La combinación de hilos virtuales, scoped values y concurrencia estructurada representa el nuevo estándar para aplicaciones concurrentes seguras y escalables en Java.
5. Observabilidad

    Los hilos virtuales se integran con el sistema de monitoreo: jcmd Thread.dump_to_file captura todos los hilos sin overhead.

    La concurrencia estructurada refleja las relaciones padre-hijo en los nombres de hilos y en los volcados, facilitando la depuración de fallos en cascada.

### 6. Buenas prácticas y transición

    Nuevas aplicaciones: usar hilos virtuales y concurrencia estructurada cuando sea posible.

    Código heredado: las bibliotecas que realizan I/O bloqueante (p.ej., JDBC antiguo) se benefician automáticamente sin cambios; miles de hilos virtuales pueden estar bloqueados en lectura de base de datos sin agotar los hilos del SO.

    Frameworks: Spring Boot 3.2+ ofrece opción para hilos virtuales en Tomcat; Quarkus y Micronaut también.

    Cuidado con la limitación de recursos: aunque los hilos virtuales son baratos, aún se pueden agotar recursos como conexiones de base de datos o memoria total.

### 10 – JVM Y RENDIMIENTO EN JAVA 21

La Máquina Virtual Java (JVM) es el entorno de ejecución que convierte el bytecode en instrucciones nativas y gestiona los recursos de la aplicación. Comprenderla a fondo es indispensable para escribir código eficiente, diagnosticar problemas de rendimiento y aprovechar al máximo las mejoras que trae Java 21. A continuación se desarrollan los tres ficheros de esta sección.
10.01 – FUNCIONAMIENTO DE LA JVM
1. Arquitectura global de la JVM

La especificación de la JVM define varios subsistemas:

    Cargador de clases (Class Loader): carga, enlaza e inicializa las clases.

    Áreas de datos en tiempo de ejecución (Runtime Data Areas): pilas, heap, área de métodos, registros del PC, etc.

    Motor de ejecución (Execution Engine): interpreta el bytecode, ejecuta métodos nativos y realiza la compilación JIT.

    Interfaz nativa (JNI) y Foreign Function & Memory API (preview en 21): interacción con código no Java.

En Java 21, la JVM sigue siendo un proceso nativo que aloja el ecosistema Java y ha evolucionado para soportar hilos virtuales, nuevos GCs y mejoras de rendimiento.
2. Carga de clases

Se realiza bajo demanda (lazy loading). El proceso consta de:

    Carga: el ClassLoader busca el archivo .class y genera la representación interna (Class<?>).

    Enlace (Linking):

        Verificación: comprueba que el bytecode es correcto y seguro.

        Preparación: asigna memoria para variables estáticas y las inicializa con valores por defecto.

        Resolución (opcional): convierte referencias simbólicas a referencias directas (a clases, campos, métodos).

    Inicialización: ejecuta los inicializadores estáticos y asigna los valores iniciales definidos por el programador.

Jerarquía de ClassLoaders (típicamente):

    Bootstrap ClassLoader (nativo, carga las clases del núcleo de java.base).

    Platform ClassLoader (carga APIs de la plataforma, antiguo Extension ClassLoader).

    Application ClassLoader (carga clases del classpath).

En el sistema de módulos (JPMS), cada módulo tiene su propio cargador o se apoya en el de la aplicación.
3. Áreas de datos en tiempo de ejecución

    Registro del contador de programa (PC Register): por cada hilo, apunta a la instrucción actual.

    Pilas de la JVM (JVM Stacks): cada hilo tiene una pila que almacena marcos (frames). Un marco contiene variables locales, pila de operandos y referencia al runtime constant pool. La pila puede ser de tamaño fijo o dinámico (-Xss). Al lanzar una excepción, se recorre la pila para buscar un manejador.

    Heap: área compartida donde residen los objetos y arrays. Gestionado por el recolector de basura. Se puede dimensionar con -Xms (tamaño inicial) y -Xmx (máximo).

    Área de métodos (Metaspace desde Java 8): almacena metadatos de las clases (estructuras del class, constant pool, métodos, campos). Fuera del heap, en memoria nativa. Su tamaño se controla con -XX:MaxMetaspaceSize.

    Runtime Constant Pool: por cada clase, contiene constantes simbólicas, strings y referencias a métodos.

### 4. Motor de ejecución

Ejecuta las instrucciones bytecode. Combina dos modos:
Interpretación

Cada bytecode se decodifica y ejecuta por un intérprete. Arranque rápido pero ejecución lenta.
Compilación Just-In-Time (JIT)

Cuando un método o bucle se considera “caliente” (basado en contadores de invocación y ciclos), el compilador JIT lo traduce a código nativo optimizado.

Compiladores JIT en HotSpot:

    C1 (Client Compiler): compilación rápida con optimizaciones ligeras. Adecuado para aplicaciones con tiempo de arranque limitado.

    C2 (Server Compiler): optimizaciones agresivas, compilación más lenta pero código final muy eficiente.

Java 21 introduce mejoras en el compilador JIT: refinamiento de inlining, eliminación de bloqueos innecesarios, y soporte para nuevas instrucciones de CPU.

Compilación por niveles (Tiered Compilation) (activada por defecto):

    Nivel 0: interpretación.

    Nivel 1-3: compilación C1 con diferentes grados de optimización y recolección de perfiles.

    Nivel 4: compilación C2 usando los perfiles recogidos.

Compilación anticipada (AOT): mediante jaotc (en desuso a favor de GraalVM Native Image) no es soportada directamente en Java 21; GraalVM Native Image permite compilar a binario nativo con sus propias ventajas.
5. Hilos en la JVM

Java 21 soporta dos tipos de hilos:

    Hilos de plataforma: mapeados 1:1 a hilos del SO.

    Hilos virtuales: gestionados por la JVM sobre un pequeño número de carriers.

La JVM utiliza librerías nativas para la gestión de hilos y para operaciones de bloqueo (como Unsafe.park). Con los hilos virtuales, la JVM puede desacoplar el bloqueo virtual del bloqueo del carrier.
6. Herramientas de monitoreo en Java 21

    jps, jstat, jinfo, jmap, jstack, jcmd siguen siendo las herramientas estándar.

    jconsole y Java Mission Control (JMC) para monitoreo gráfico.

    jcmd permite obtener volcados de hilos de forma ligera (especialmente importante con hilos virtuales).

    -XX:+PrintFlagsFinal muestra las flags de la JVM.

    -Xlog:gc proporciona logs detallados del GC (unificado desde Java 9).

### 10.02 – GARBAGE COLLECTION
1. Principios básicos del GC

El recolector de basura libera memoria ocupada por objetos que ya no son alcanzables desde las raíces (variables locales, estáticas, referencias activas de hilos, etc.). La JVM divide el heap en regiones (o generaciones) para aplicar distintos algoritmos según la longevidad de los objetos.
2. Hipótesis generacional

    La mayoría de los objetos mueren jóvenes (weak generational hypothesis).

    Los objetos viejos que sobreviven tienden a persistir mucho tiempo.
    Por ello, se divide en:

    Young Generation: objeto recién creado. Subdividida en Eden y dos espacios Survivor (S0, S1).

    Old Generation (Tenured): objetos que han sobrevivido varios ciclos de GC menor.

    Metaspace (fuera del heap): metadatos de clases.

3. Conceptos comunes

    GC menor (Minor GC): recolecta solo la generación joven. Rápido.

    GC mayor (Major GC) / Full GC: involucra la generación vieja y a menudo todo el heap. Pausas largas, intentar minimizarlas.

    Stop-The-World (STW): todos los hilos de aplicación se detienen para que el GC realice su trabajo.

    Compactación: reorganiza objetos vivos para eliminar fragmentación.

    Promoción: mover objetos supervivientes de la generación joven a la vieja.

### 4. Recolectores disponibles en Java 21
Serial GC ( -XX:+UseSerialGC )

    Un solo hilo para GC menor y mayor.

    Adecuado para aplicaciones con heap pequeño (~<100 MB) o entornos embebidos.

    Pausas largas con heap grande.

### Parallel GC ( -XX:+UseParallelGC )

    Varios hilos para GC menor y mayor (stop-the-world en ambos).

    Maximiza throughput (rendimiento).

    Buena opción para procesos batch que toleran pausas.

### G1 GC ( -XX:+UseG1GC ) – Predeterminado desde Java 9

    Divide el heap en regiones de tamaño fijo y recolecta preferentemente las regiones con más basura.

    Balance entre pausas y throughput.

    Pausas configurables con -XX:MaxGCPauseMillis (por defecto 200 ms).

    Realiza compactaciones parciales y ciclos de marcado concurrente (SATB).

    Mejoras en Java 21: refinamiento de la predicción de pausa, mejor manejo de regiones humongous.

### ZGC ( -XX:+UseZGC )

    Diseñado para pausas inferiores a 1 ms, incluso con heaps de terabytes.

    Concurrente en casi todas las fases (marcado, compactación, referencias).

    A partir de Java 21, ZGC soporta generaciones (activando -XX:+ZGenerational). Separa objetos jóvenes de viejos para recolectar los jóvenes con mucha más frecuencia, reduciendo la presión de asignación.

    Sus algoritmos de “punteros coloreados” y “load barriers” permiten mover objetos sin detener los hilos de aplicación.

    Muy recomendado para aplicaciones que requieren baja latencia.

### Shenandoah GC ( -XX:+UseShenandoahGC )

    También de latencia ultrabaja, con compactación concurrente mediante evacuación.

    A diferencia de ZGC, no requiere punteros coloreados; usa barreras de lectura y escritura.

    Soporta generaciones opcionales (modo generacional en desarrollo/preview).

    Disponible en JDK builds que lo incluyan; en Oracle JDK está presente.

### Epsilon GC ( -XX:+UseEpsilonGC )

    No recolecta basura; solo asigna memoria hasta que se acaba.

    Útil para pruebas de rendimiento, benchmarks, o aplicaciones de vida corta.

### 5. Factores que afectan la elección del GC

    Latencia máxima aceptable: ZGC / Shenandoah.

    Throughput: Parallel GC.

    Equilibrio: G1.

    Tamaño del heap: ZGC escala mejor a heaps muy grandes.

    Número de núcleos: Parallel GC y G1 se benefician de muchos cores; ZGC requiere algunos cores para concurrencia.

### 6. Parámetros de ajuste comunes
Parámetro	Descripción
-Xmx<size>	Tamaño máximo del heap (ej: -Xmx2g)
-Xms<size>	Tamaño inicial del heap
-XX:MaxGCPauseMillis	Objetivo de pausa máxima (G1)
-XX:+UseStringDeduplication	Elimina duplicados de String en el heap (G1, ZGC)
-XX:+PrintGCDetails	(obsoleto, usar -Xlog:gc*)
-Xlog:gc	Logging unificado del GC
-XX:MetaspaceSize	Tamaño inicial del metaspace
-XX:MaxMetaspaceSize	Tamaño máximo del metaspace
-XX:+UseZGC	Activa ZGC
-XX:+ZGenerational	Modo generacional en ZGC (Java 21+)
-XX:ConcGCThreads	Número de hilos para fases concurrentes
-XX:ParallelGCThreads	Número de hilos para fases STW
7. Logs y análisis

Con el sistema unificado de logging (-Xlog):
```text
-Xlog:gc*=info:file=gc.log:time,uptimemillis:filecount=5,filesize=10M
```

Herramientas como GCViewer, GCEasy, o JMC permiten visualizar los logs y ajustar parámetros.
10.03 – OPTIMIZACIÓN DE RENDIMIENTO

Optimizar una aplicación Java implica un proceso iterativo de medición, análisis y ajuste tanto del código como de la JVM.
1. Métricas clave

    Throughput: cantidad de trabajo por unidad de tiempo.

    Latencia: tiempo de respuesta a una petición.

    Footprint: memoria ocupada (heap + nativa).

    Tiempo de arranque: desde inicio hasta que la aplicación está lista.

    Tiempo de calentamiento (warmup): hasta que el JIT ha optimizado los caminos calientes.

2. Herramientas de profiling y diagnóstico

    Java Flight Recorder (JFR) + Java Mission Control (JMC): recopilación de eventos de la JVM con bajo overhead. Permite analizar asignación de memoria, GC, bloqueos, actividad de hilos, etc.

    Async Profiler: genera flamegraphs de CPU y memoria utilizando perf sin instrumentación costosa.

    VisualVM: herramienta gráfica para monitoreo y profiling.

    JMH (Java Microbenchmark Harness): imprescindible para microbenchmarks precisos, evitando la interferencia del JIT (ej: @BenchmarkMode, @Warmup).

3. Estrategias de optimización de memoria

    Dimensionar correctamente el heap: establecer -Xms igual a -Xmx para evitar redimensionamientos.

    Elegir el GC adecuado y afinarlo con pausas objetivo.

    Reducir el uso de objetos temporales en bucles calientes (autoboxing, Strings concatenados → usar StringBuilder o text blocks en tiempo de compilación).

    Aprovechar colecciones inmutables (List.of) y records para evitar mutabilidad innecesaria.

    Uso de Optional sin abusar; no para campos de entidades.

    Liberar recursos explícitamente (try-with-resources).

    Evitar finalize() (obsoleto y costoso). Usar Cleaner si es imprescindible.

### 4. Optimización de CPU

    Dejar que el JIT trabaje: evite micro-optimizaciones prematuras; el JIT inlinea métodos y elimina código muerto.

    Perfiles de compilación: el JIT aprovecha perfiles de tipos para devirtualizar llamadas a métodos. Cuanto más estable sea el flujo de tipos, mejor.

    Conversión escalar y eliminación de autoboxing: los análisis de escape permiten eliminar objetos si no escapan del hilo.

    Usar Streams con criterio: para operaciones sencillas pueden generar objetos intermedios; para cálculos críticos medir si conviene un bucle tradicional.

    Concurrencia virtual: sustituir pools de hilos de plataforma por hilos virtuales y concurrencia estructurada para reducir latencia y mejorar throughput en aplicaciones I/O-bound.

### 5. Optimización del arranque y despliegue

    CDS (Class Data Sharing): -Xshare:on y creación de archivo compartido (-XX:ArchiveClassesAtExit / -XX:SharedArchiveFile) para reducir tiempo de carga.

    AOT con GraalVM Native Image si el tiempo de arranque es crítico (microservicios ephemeral), sacrificando algunas optimizaciones de pico.

    AppCDS permite incluir clases de la aplicación en el archivo compartido.

    Usar módulos y jlink para generar una JRE personalizada y ligera.

### 6. Técnicas avanzadas en Java 21

    Hilos virtuales para I/O intensiva: migrar servidores y procesos batch que antes requerían pools enormes.

    Scoped Values en lugar de ThreadLocal: menor consumo de memoria, herencia automática sin coste en hilos virtuales.

    Structured Concurrency: evita la pérdida de hilos, mejora la cancelación y la observabilidad.

    Pattern matching y records: reducen el código propenso a errores y la creación de clases intermedias, mejorando el uso de caché de instrucciones.

### 7. Pasos prácticos de optimización

    Definir objetivos de rendimiento (ej: p95 < 10ms, 1000 req/s).

    Establecer un entorno de pruebas reproducible.

    Perfilar con JFR/Async Profiler para identificar cuellos de botella (CPU, asignación, bloqueos).

    Analizar logs de GC y ajustar tamaño de heap o cambiar de GC si es necesario.

    Aplicar mejoras de código (evitar antipatrones, reducir asignaciones).

    Medir nuevamente para validar la mejora.

    Automatizar pruebas de rendimiento en el CI/CD para detectar regresiones.

### 8. Flags de JVM útiles para afinamiento
Flag	Propósito
-server	Selecciona el compilador servidor (suele ser por defecto en 64 bits)
-XX:+AggressiveOpts	Habilita optimizaciones experimentales (no necesario hoy)
-XX:TieredStopAtLevel=1	Solo compila con C1; reduce calentamiento a costa de máximo rendimiento
-XX:+AlwaysPreTouch	Toca toda la memoria del heap al inicio (evita page faults)
-XX:+UseStringDeduplication	Deduplicación de Strings (G1, ZGC)
-XX:+UseTransparentHugePages	Mejora rendimiento con páginas grandes de memoria
-XX:MaxInlineLevel=15	Ajusta la profundidad máxima de inlining
9. Ejemplo: ajuste para un microservicio con ZGC generacional
```text
java -Xmx2g -Xms2g -XX:+UseZGC -XX:+ZGenerational \
     -Xlog:gc*:file=gc.log:time,uptimemillis:filecount=5,filesize=20M \
     -XX:+AlwaysPreTouch \
     -jar aplicacion.jar
```

Se logra latencia de GC < 1ms y buen rendimiento incluso bajo cargas altas.


### 11 – ECOSISTEMA DE CONSTRUCCIÓN, PRUEBAS Y EMPAQUETADO

El ecosistema moderno de Java gira en torno a herramientas que automatizan la construcción, las pruebas y la distribución de aplicaciones. Esta sección profundiza en Maven y Gradle como gestores de proyectos, JUnit 5 como plataforma de pruebas y jlink / jpackage para crear distribuciones nativas y ligeras. Todas las explicaciones están actualizadas para Java 21.
11.01 – MAVEN Y GRADLE: GESTIÓN AVANZADA DE PROYECTOS
1. El papel de las herramientas de construcción

Antes de Maven/Gradle se usaba Ant (scripts XML) o simplemente javac. Hoy es impensable un proyecto sin gestión automática de dependencias, ciclo de vida estandarizado y plugins.
2. Maven

Maven se basa en la convención sobre configuración. Utiliza un archivo pom.xml que describe el proyecto, sus dependencias y los plugins que ejecutan tareas.
2.1. Estructura de un proyecto Maven
```text
miapp/
├── pom.xml
└── src/
    ├── main/java/         # código fuente
    ├── main/resources/    # recursos (application.properties, etc.)
    ├── test/java/         # pruebas
    └── test/resources/
```

2.2. pom.xml mínimo para Java 21
xml

### <project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

### <groupId>com.empresa</groupId>
    <artifactId>miapp</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

### <properties>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

### <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.10.1</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

### <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <release>21</release>
                    <!-- para características preview: <compilerArgs>--enable-preview</compilerArgs> -->
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>

2.3. Ciclo de vida de Maven

Fases principales:

    validate, compile, test, package, verify, install, deploy.
    Ejecutar mvn package compila, ejecuta tests y empaqueta un JAR.

2.4. Plugins importantes

    maven-compiler-plugin: configura la versión de Java.

    maven-surefire-plugin: ejecución de tests unitarios.

    maven-failsafe-plugin: tests de integración.

    maven-jar-plugin: empaquetado base.

    maven-shade-plugin / maven-assembly-plugin: crear fat JAR con dependencias.

    maven-jlink-plugin: construir imágenes JRE personalizadas.

    maven-jpackage-plugin: invocar jpackage.

2.5. Gestión de dependencias

Las dependencias se declaran con groupId, artifactId, version y scope (compile, test, provided, runtime). Maven resuelve las dependencias transitivas y las almacena en el repositorio local (~/.m2).

Para evitar conflictos se puede usar <dependencyManagement> y la sección <exclusions>.
3. Gradle

Gradle usa un DSL basado en Groovy o Kotlin. Es más flexible y se adapta mejor a proyectos grandes o multimódulo.
3.1. Estructura típica
```text
miapp/
├── build.gradle (o build.gradle.kts)
├── settings.gradle
└── src/
    ├── main/java/
    ├── main/resources/
    ├── test/java/
    └── test/resources/
```

3.2. build.gradle.kts mínimo (Kotlin DSL) para Java 21
kotlin

### plugins {
```java
    application
}
```

### group = "com.empresa"
version = "1.0.0"

### java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
    // para preview: options.compilerArgs.add("--enable-preview")
}

### application {
    mainClass.set("com.empresa.Main")
}

### repositories {
    mavenCentral()
}

### dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.1")
}

### tasks.test {
    useJUnitPlatform()
}

3.3. Ciclo de vida y tareas

    gradle build compila, ejecuta tests y empaqueta.

    gradle run ejecuta la aplicación.

    Las tareas pueden encadenarse y crearse automáticamente por los plugins.

3.4. Plugins principales

### java, application

    org.gradlex.java.enable-preview (para preview fácil).

    org.beryx.jlink (para jlink).

    com.github.johnrengelman.shadow (fat JAR).

    org.panteleyev.jpackage o com.github.ben-manes.gradle-versions-plugin.

3.5. Gestión de dependencias

    implementation: dependencia necesaria en compilación y ejecución, no expuesta a consumidores del módulo.

    api: expuesta a consumidores.

    testImplementation, testRuntimeOnly, etc.

    Se pueden usar BOMs (Bill of Materials) para alinear versiones, por ejemplo Spring Boot, Jackson, etc.

### 4. Comparativa rápida Maven vs Gradle
Característica	Maven	Gradle
Lenguaje	XML	Groovy/Kotlin DSL
Extensibilidad	Plugins XML	Scripts/plugins program.
Rendimiento	Más lento en builds grandes	Mayor velocidad, incremental y build cache
Convención	Muy estricta y homogénea	Flexible, adaptable
Curva aprendizaje	Menor	Moderada

Ambos son perfectamente capaces y se integran con IDEs y CI/CD. Gradle suele preferirse en nuevos desarrollos de Android, grandes multimódulos o cuando se necesita mucha personalización; Maven sigue siendo el estándar en muchos entornos enterprise.
11.02 – PRUEBAS CON JUNIT 5
1. JUnit 5: la plataforma moderna de testing

JUnit 5 (Jupiter) es el estándar para pruebas unitarias y de integración en Java. Lanzado en 2017, ha ido mejorando cada versión y en Java 21 sigue evolucionando (versión 5.10+). Está compuesto por:

    JUnit Platform: base que permite ejecutar cualquier motor de tests (JUnit Vintage para JUnit 3/4, Jupiter, etc.).

    JUnit Jupiter: nuevo API de programación de tests.

    JUnit Vintage: retrocompatibilidad con JUnit 3/4.

2. Anotaciones y estructura básica de un test
```java
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class CalculadoraTest {
```

### Calculadora calc;

### @BeforeAll
    void initAll() {
        System.out.println("Antes de todos los tests");
    }

### @BeforeEach
    void init() {
        calc = new Calculadora();
    }

### @Test
    @DisplayName("Suma de dos números positivos")
    void testSuma() {
        assertEquals(5, calc.sumar(2, 3), "2+3 debería ser 5");
    }

### @Test
    @Disabled("Funcionalidad aún no implementada")
    void testResta() { }

### @AfterEach
    void tearDown() {
        calc = null;
    }

### @AfterAll
    static void cleanAll() {
        System.out.println("Después de todos los tests");
    }
}

3. Aserciones principales

### assertEquals(expected, actual)

### assertTrue(condition), assertFalse(condition)

### assertNull(obj), assertNotNull(obj)

### assertSame, assertNotSame

    assertThrows(Exception.class, () -> { ... }) → captura y verifica excepciones.

### assertTimeout(Duration.ofMillis(100), () -> { ... })

    assertAll(...) para agrupar varias aserciones y que se ejecuten todas aunque alguna falle.

Desde JUnit 5.8 se pueden usar aserciones con mensaje como Supplier (() -> "mensaje costoso") para evaluación perezosa.
4. Test parametrizados

Ejecutan un mismo test con múltiples conjuntos de datos.
```java
@ParameterizedTest
@ValueSource(ints = {1, 2, 3, 4, 5})
void testCuadrado(int numero) {
    assertEquals(numero * numero, calc.cuadrado(numero));
}

@ParameterizedTest
@CsvSource({
    "1, 2, 3",
    "0, 0, 0",
    "-1, -1, -2"
})
void testSuma(int a, int b, int resultado) {
    assertEquals(resultado, calc.sumar(a, b));
}
```

Otras fuentes: @MethodSource, @EnumSource, @CsvFileSource, @ArgumentsSource.
5. Ciclo de vida y extensión

El modelo de extensión permite hooks avanzados mediante @ExtendWith.

    SpringExtension para integrar Spring TestContext Framework.

    MockitoExtension para inicializar mocks de Mockito.

    Extensiones propias implementando BeforeEachCallback, AfterEachCallback, etc.

### 6. Testing de hilos virtuales y concurrencia

Con JUnit 5 podemos probar código asíncrono con assertTimeoutPreemptively o utilizando Thread.startVirtualThread dentro de los tests. Para probar concurrencia estructurada, se puede ejecutar un try (scope) { ... } y verificar resultados con assertAll.
7. Tests de integración con testcontainers

Aunque no es parte de JUnit 5, se integra perfectamente. Testcontainers permite arrancar una base de datos real en un contenedor Docker dentro del test, ideal para pruebas de repositorio. La anotación @Testcontainers y el GenericContainer se combinan con JUnit Jupiter.
8. Prácticas recomendadas

    Nombre descriptivo de tests: usar @DisplayName o el método en estilo shouldReturnSum_whenGivenTwoNumbers.

    Seguir la estructura AAA: Arrange, Act, Assert.

    No realizar I/O real en tests unitarios; usar mocks o stubs.

    Limpiar recursos compartidos en @AfterEach.

    Aislar tests: no deben depender del orden de ejecución.

    Ejecutar tests frecuentemente, integrados con Maven/Gradle.

### 11.03 – EMPAQUETADO CON JLINK Y JPACKAGE
1. El declive del JRE monolítico

Con la modularización (JPMS), podemos crear imágenes de ejecución ligeras que contengan solo los módulos necesarios para nuestra aplicación. Para distribuir aplicaciones a usuarios finales de forma nativa, jpackage genera instaladores como .exe, .dmg o .deb.
2. jlink: imagen JRE personalizada

jlink crea una imagen de tiempo de ejecución a partir de un conjunto de módulos. Requiere que la aplicación esté modularizada (tener module-info.java) o al menos que conozcamos los módulos que necesita (se puede hacer con jdeps).
2.1. Comando básico
```bash
jlink --module-path módulos:libs --add-modules com.miapp.mimodulo \
      --output mi-jre --launcher mi-app=com.miapp.mimodulo/com.miapp.Main

    --add-modules: lista los módulos a incluir (el raíz y sus dependencias transitivas).

    --output: directorio de la imagen generada (contiene binarios, libs, etc.).

    --launcher: crea un script ejecutable en mi-jre/bin.
```

2.2. Plugins de Maven/Gradle

    Maven: maven-jlink-plugin se configura dentro del pom.xml.

    Gradle: plugin org.beryx.jlink (badass-jlink-plugin).
    Ambos simplifican la invocación y se integran en el ciclo de package.

2.3. Ejemplo con Gradle (Kotlin DSL)
kotlin

### plugins {
    id("org.beryx.jlink") version "2.25.0"
}

### jlink {
    imageDir.set(file("$buildDir/image"))
    options.set(listOf("--strip-debug", "--compress", "2", "--no-header-files", "--no-man-pages"))
    launcher {
        name = "miapp"
        jvmArgs = listOf("-Xmx256m")
    }
}

3. jpackage: empaquetado nativo

jpackage toma la imagen generada por jlink y crea un paquete nativo para el sistema operativo. Genera un instalador autocontenido que no requiere que el usuario instale Java.
3.1. Modos de operación

    Aplicación nativa (--type app-image): genera una carpeta ejecutable ligada a una JRE ya incluida.

    Instalador (--type msi, --type deb, --type rpm, --type dmg, --type pkg): crea un instalador para distribución.

3.2. Requisitos

    La aplicación debe estar empaquetada como JAR modular o no modular (puede usar classpath, pero mejor si está en una imagen jlink previa).

    Se necesita tener herramientas nativas (En Windows: Wix para MSI; en macOS: herramientas de línea de comandos; en Linux: dpkg, rpm).

3.3. Comando típico desde jlink a jpackage

Primero creamos la imagen con jlink, luego ejecutamos jpackage:
```bash
# 1) jlink crea la JRE personalizada y launcher
jlink --module-path libs --add-modules com.mi.modulo \
      --output build/app-jre --launcher mi-app=com.mi.modulo/com.mi.Main

# 2) jpackage empaqueta esa imagen como instalador
jpackage --type deb \
         --name "MiAplicacion" \
         --input build/app-jre/bin \
         --main-jar miapp.jar \
         --main-class com.mi.Main \
         --java-options "-Xmx256m" \
         --dest build/dist
```

Alternativamente, se puede saltar jlink y que jpackage genere la JRE automáticamente con --runtime-image (señalando a un JDK).
3.4. Personalización

    --icon icono.ico (Windows) o --icon icono.icns (macOS).

    --file-associations para asociar extensiones de archivo.

    --install-dir, --vendor, --description.

    --win-console para habilitar consola en Windows.

3.5. Integración con herramientas de construcción

    Maven: org.panteleyev.jpackageplugin o se.vidstige.jpackage-maven-plugin.

    Gradle: org.panteleyev.jpackageplugin.

Ejemplo básico con Gradle:
kotlin

### plugins {
    id("org.panteleev.jpackageplugin") version "1.5.0"
}

### tasks.jpackage {
    dependsOn("build")
    appName = "MiApp"
    appVersion = project.version.toString()
    inputDir = file("${buildDir}/libs")
    mainJar = bootJar.archiveFileName.get()
    mainClass = "com.mi.Main"
    type = "deb" // o "msi", "dmg", etc.
    destinationDir = file("${buildDir}/dist")
    javaOptions = listOf("-Xmx256m")
}

3.6. Ventajas de jpackage en Java 21

    Distribuciones más seguras y pequeñas.

    Experiencia de instalación nativa.

    Compatibilidad con actualizaciones futuras (firma de código).

    Integración fluida con pipelines CI/CD.

