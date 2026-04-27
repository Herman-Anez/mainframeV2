01 – Introducción a Java
¿Qué es Java?

Java es un lenguaje de propósito general, concurrente, orientado a objetos y fuertemente tipado. Su diseño busca minimizar las dependencias de implementación: el código compilado se ejecuta en una máquina virtual sin necesidad de recompilar.

Lema: Write Once, Run Anywhere (Escribe una vez, ejecuta en cualquier lugar).
Ediciones de la plataforma

    Java SE (Standard Edition): núcleo del lenguaje, APIs de colecciones, I/O, concurrencia, etc.

    Java EE / Jakarta EE: para aplicaciones empresariales (servlets, JPA, etc.).

    Java ME: dispositivos embebidos y móviles.

    Hoy se usa el término JDK (Java Development Kit) = herramientas + bibliotecas + JVM.

JDK, JRE, JVM

    JVM (Java Virtual Machine): ejecuta el bytecode. Proporciona gestión automática de memoria (recolector de basura), seguridad y portabilidad.

    JRE (Java Runtime Environment): JVM + bibliotecas estándar necesarias para ejecutar aplicaciones Java. No incluye herramientas de desarrollo.

    JDK: JRE + compilador (javac), debugger, javadoc, jar, etc.

Proceso de ejecución

    Escribes código fuente en archivos .java.

    El compilador javac lo transforma en bytecode (archivos .class), un código intermedio independiente de la plataforma.

    La JVM carga las clases, verifica el bytecode, lo interpreta o compila en tiempo real (JIT) a código nativo.

Estructura mínima de un programa
java

// Opcional: definición de paquete
// package com.miproyecto;

// Opcional: importaciones
// import java.util.Scanner;

public class HolaMundo {
    // Punto de entrada obligatorio
    public static void main(String[] args) {
        System.out.println("¡Hola desde Java!");
    }
}

    El nombre del archivo debe coincidir exactamente con el de la clase pública (distingue mayúsculas).

    El método main es public (accesible para la JVM), static (se puede invocar sin crear objeto) y recibe un array de String con argumentos de línea de comandos.

Paquetes

Agrupan clases relacionadas. Convención de nombres: dominio invertido (com.empresa.proyecto). La estructura de directorios refleja el paquete:
text

src/com/empresa/proyecto/HolaMundo.java

Compilación y ejecución desde terminal
bash

javac -d bin src/com/empresa/proyecto/HolaMundo.java
java -cp bin com.empresa.proyecto.HolaMundo

    -d: directorio de salida.

    -cp (classpath): dónde buscar clases compiladas.

Comentarios y Javadoc

    // una línea.

    /* ... */ multilínea.

    /** ... */ documentación (Javadoc), que puede generar documentación automática con javadoc.

Convenciones de estilo

    Clases: PascalCase (primera letra mayúscula en cada palabra).

    Métodos y variables: camelCase (primera minúscula).

    Constantes (static final): MAYÚSCULAS_CON_GUIONES.

Eras de Java

    Versiones LTS (Long Term Support): 8, 11, 17, 21. Aportan estabilidad; se recomienda usar la última LTS para proyectos serios.

    Desde Java 9, lanzamientos cada 6 meses.

02 – Tipos de datos, variables y constantes
Sistema de tipos

Java es fuertemente tipado: cada variable debe declararse con un tipo específico. Existen dos grandes categorías:

    Tipos primitivos: almacenan valores simples directamente (no son objetos).

    Tipos de referencia: almacenan una dirección a un objeto (clases, interfaces, arrays, enums).

Tipos primitivos
Tipo	Tamaño	Valor por defecto	Rango / precisión
byte	8 bits	0	-128 a 127
short	16 bits	0	-32,768 a 32,767
int	32 bits	0	-2^31 a 2^31-1
long	64 bits	0L	-2^63 a 2^63-1
float	32 bits	0.0f	±1.4E-45 a ±3.4E+38 (aprox.)
double	64 bits	0.0d	±4.9E-324 a ±1.8E+308
char	16 bits	'\u0000'	0 a 65,535 (caracteres Unicode)
boolean	no definido	false	true / false

    Los enteros pueden escribirse con subrayados (1_000_000) y en bases: binario 0b1010, octal 012, hexadecimal 0xFF.

    Los flotantes por defecto son double. Para float añadir f o F: 3.14f.

    char representa un solo carácter Unicode (UTF-16). Secuencias de escape: \n, \t, \\, \", \u0041 (código Unicode).

Tipos de referencia

Cualquier variable cuyo tipo sea una clase, interfaz, array o enum. La variable no contiene el objeto, sino una referencia a su ubicación en memoria. Si no se inicializa, su valor por defecto es null.

Ejemplo:
java

String mensaje;      // vale null
mensaje = "Hola";    // referencia a un objeto String

Declaración, inicialización y constantes
java

int edad = 25;
double salario = 45000.50;
char inicial = 'J';
boolean activo = true;

// Constante: no puede cambiar su valor tras la inicialización.
final double PI = 3.14159265;
// Convención: nombres en mayúsculas
final static int MAXIMO_INTENTOS = 5;

    Una variable final debe inicializarse una sola vez (en la declaración o en el constructor, si es de instancia).

    Las variables de clase static final son constantes globales de la clase.

Ámbito (scope)

    Variables locales: declaradas dentro de un método o bloque. No se les asigna valor por defecto; deben inicializarse antes de usarse.

    Variables de instancia (campos no estáticos): pertenecen al objeto. Se inicializan automáticamente con valores por defecto (0, 0.0, false, null).

    Variables de clase (campos estáticos): asociadas a la clase. Misma inicialización automática.

Inferencia de tipos (Java 10+)

var permite que el compilador deduzca el tipo a partir del inicializador. Solo se permite en variables locales con inicialización explícita.
java

var nombre = "Ana";           // tipo String
var lista = new ArrayList<Integer>(); // ArrayList<Integer>

No se puede usar var para campos de clase, parámetros o sin inicializador.
Conversiones de tipo (casting)

    Implícita (automática): cuando se asigna un tipo de menor rango a uno de mayor (p.ej., int a long).

    Explícita (manual): cuando puede haber pérdida de información.

java

int i = 100;
long l = i;           // implícita, sin problema
double d = l * 3.14; // implícita en la expresión

double x = 9.99;
int n = (int) x;      // n = 9, se trunca la parte decimal

Autoboxing y unboxing

Conversión automática entre tipo primitivo y su clase envoltorio correspondiente.
java

Integer obj = 5;    // autoboxing: int -> Integer
int valor = obj;    // unboxing: Integer -> int

Se usa mucho con colecciones y genéricos.
Clases envoltorio (wrappers)

Cada primitivo tiene una clase: Byte, Short, Integer, Long, Float, Double, Character, Boolean. Sirven para tratar primitivos como objetos y ofrecen métodos de utilidad (parseo, constantes, etc.).
03 – Operadores
Operadores aritméticos

+, -, *, /, % (módulo o resto).
La división entre enteros produce un resultado entero (trunca).
java

int a = 7 / 2;   // 3
double b = 7 / 2.0; // 3.5

Operadores de incremento y decremento

++ y -- en sus formas prefija (++i) y postfija (i++). La prefija incrementa y devuelve el nuevo valor; la postfija devuelve el valor original y luego incrementa.
Operadores relacionales

Comparan valores y devuelven boolean: ==, !=, >, <, >=, <=.
Para objetos, == compara referencias. Para comparar contenido se usa equals().
Operadores lógicos

    && (AND condicional / cortocircuito): evalúa el segundo operando solo si el primero es true.

    || (OR condicional / cortocircuito): evalúa el segundo solo si el primero es false.

    ! (NOT).

    Los operadores bitwise & y | también pueden actuar como lógicos sin cortocircuito (evalúan ambos operandos siempre). Se usan raramente para booleanos.

Operadores a nivel de bits

& AND, | OR, ^ XOR, ~ complemento a uno.
Desplazamiento: << (izquierda, rellena con ceros), >> (derecha con signo, replica el bit de signo), >>> (derecha sin signo, rellena con ceros).
Operador ternario

condicion ? valorSiTrue : valorSiFalse. Útil para asignaciones condicionales cortas.
java

int edad = 20;
String estado = (edad >= 18) ? "Adulto" : "Menor";

Operadores de asignación

Además del básico =, existen los compuestos: +=, -=, *=, /=, %=, &=, |=, <<=, etc.
Ejemplo: x += 5; equivale a x = x + 5;
Concatenación de cadenas

El operador + está sobrecargado para String. Si uno de los operandos es una cadena, los demás se convierten a String automáticamente.
java

int n = 10;
System.out.println("Número: " + n); // "Número: 10"

Cuidado con la precedencia: "Resultado: " + 5 + 3 produce "Resultado: 53", mientras que "Resultado: " + (5 + 3) produce "Resultado: 8".
Operador instanceof

Verifica si un objeto es de un tipo determinado.
java

if (obj instanceof String) { ... }

Desde Java 16 el pattern matching permite asignar la variable directamente: if (obj instanceof String s) { ... } (esta parte la dejamos para temas más avanzados).
Precedencia y asociatividad

Resumen (de mayor a menor prioridad):

    Postfijos: expr++ expr--

    Prefijos unarios: ++expr --expr +expr -expr ~ !

    Multiplicación/división/módulo: * / %

    Suma/resta: + -

    Desplazamiento: << >> >>>

    Relacionales: < > <= >= instanceof

    Igualdad: == !=

    AND bitwise: &

    XOR bitwise: ^

    OR bitwise: |

    AND lógico: &&

    OR lógico: ||

    Ternario: ?:

    Asignación: = += -= etc.

Utiliza paréntesis para claridad.
04 – Estructuras de control de flujo
if, else if, else
java

if (condicion1) {
    // bloque 1
} else if (condicion2) {
    // bloque 2
} else {
    // bloque por defecto
}

La condición debe ser una expresión boolean. No se permite if (x) ... si x es entero (a diferencia de C).
switch tradicional

Evalúa una expresión (hasta Java 17: byte, short, char, int, String, enums) y salta al case correspondiente.
java

switch (dia) {
    case 1:
        System.out.println("Lunes");
        break;
    case 2:
        System.out.println("Martes");
        break;
    default:
        System.out.println("Otro día");
}

Sin break, el flujo continúa al siguiente case (fall-through), lo que a veces es intencionado pero propenso a errores.
Switch mejorado (Java 14+)

Uso de flecha (->) para evitar break y bloques que pueden devolver valor (switch expresión).
java

String nombre = switch (dia) {
    case 1 -> "Lunes";
    case 2 -> "Martes";
    default -> "Desconocido";
};

También se pueden usar bloques con yield:
java

int puntos = switch (letra) {
    case "A" -> 10;
    case "B" -> {
        int extra = 2;
        yield 8 + extra;
    }
    default -> 0;
};

Bucle while

Se ejecuta mientras la condición sea verdadera (puede que nunca entre).
java

while (condicion) {
    // instrucciones
}

Bucle do-while

Ejecuta el cuerpo al menos una vez y luego repite mientras la condición sea verdadera.
java

do {
    // instrucciones
} while (condicion);

Bucle for clásico
java

for (inicialización; condición; actualización) {
    // cuerpo
}

Ejemplo:
java

for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

Las tres partes son opcionales; un for(;;) es un bucle infinito.
Bucle for-each (enhanced for)

Itera sobre arrays y colecciones que implementen Iterable. No se puede modificar la colección durante el recorrido (puede lanzar ConcurrentModificationException).
java

int[] numeros = {1, 2, 3};
for (int n : numeros) {
    System.out.println(n);
}

break y continue

    break: termina el bucle actual (o el bloque del switch).

    continue: salta a la siguiente iteración del bucle.
    Ambos pueden usar etiquetas para referirse a bucles externos:

java

externo:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (j == 1) break externo; // sale del for externo
    }
}

Las etiquetas son útiles pero deben usarse con moderación.
return

Se usa para salir de un método, devolviendo un valor si es necesario. En métodos void solo se usa return; sin valor.
05 – Arrays y cadenas
Arrays
Declaración e inicialización

Un array es un objeto que contiene un número fijo de elementos del mismo tipo.
java

// Solo declaración
int[] numeros;
// Creación con tamaño
numeros = new int[5]; // longitud 5, valores iniciales 0

// Declaración e inicialización directa
String[] dias = {"Lunes", "Martes", "Miércoles"};

// Otras sintaxis válidas (menos comunes)
int[] arr1 = new int[]{1, 2, 3};
int otro[];

    La longitud se obtiene con array.length (propiedad, no método).

    Los índices van de 0 a length - 1. Fuera de rango se lanza ArrayIndexOutOfBoundsException.

Arrays multidimensionales

En realidad son arrays de arrays.
java

int[][] matriz = new int[3][4];       // 3 filas, 4 columnas
int[][] irregular = new int[3][];     // filas no definidas aún
irregular[0] = new int[2];
irregular[1] = new int[5];

Acceso: matriz[i][j]. Se puede recorrer con bucles anidados.
Copia de arrays

    System.arraycopy(src, srcPos, dest, destPos, length) – copia eficiente.

    Arrays.copyOf(array, nuevaLongitud) – crea una nueva copia.

    array.clone() – copia superficial.

Clase java.util.Arrays

Proporciona métodos estáticos para manipular arrays: sort(), binarySearch(), fill(), equals(), toString(), asList() (convierte a lista fija).
Peculiaridades

    Los arrays son covariantes: un String[] es un Object[]. Esto puede causar ArrayStoreException en tiempo de ejecución si intentas meter un objeto incompatible.

    Los arrays de tipos primitivos almacenan directamente los valores, los de objetos almacenan referencias.

Cadenas (String, StringBuilder, StringBuffer)
String – inmutable

Todos los objetos String son inmutables: cualquier operación que parece modificar una cadena en realidad crea un nuevo objeto. Esto aporta seguridad y eficiencia al compartir referencias (pool de strings).

Pool de strings: Cuando se crea una cadena mediante literal ("Hola"), la JVM la guarda en un área especial. Si luego se usa el mismo literal, se reutiliza la misma referencia. Con new String("Hola") se fuerza una nueva instancia fuera del pool (normalmente se evita).
java

String a = "Hola";
String b = "Hola";
System.out.println(a == b); // true (misma referencia)

String c = new String("Hola");
System.out.println(a == c); // false (objetos distintos)

Métodos principales
Método	Descripción
length()	Número de caracteres
charAt(int index)	Carácter en la posición dada
substring(inicio, final)	Extrae subcadena [inicio, final-1]
indexOf(char/str)	Posición de la primera ocurrencia (-1 si no existe)
lastIndexOf(...)	Última ocurrencia
equals(Object)	Compara contenido, no referencia
equalsIgnoreCase(String)	Compara ignorando mayúsculas
toLowerCase() / toUpperCase()	Convierte a minúsculas / mayúsculas
trim()	Elimina espacios en blanco al inicio y final
split(String regex)	Divide en un array según una expresión regular
replace(old, new)	Reemplaza caracteres o subcadenas
contains(CharSequence)	Verifica si contiene una secuencia
startsWith(String) / endsWith()	Prefijo / sufijo
compareTo(String)	Orden lexicográfico (negativo si menor, 0 igual, positivo)
join(delimitador, elementos)	Une varios elementos con un delimitador (estático, Java 8)
Concatenación

El operador + es práctico, pero en bucles intensivos puede generar muchos objetos temporales y degradar el rendimiento.
java

String s = "";
for (int i = 0; i < 10000; i++) {
    s += i; // Ineficiente: crea un nuevo String en cada iteración
}

Para construir cadenas de forma dinámica se recomienda StringBuilder (o StringBuffer si hace falta sincronización).
StringBuilder y StringBuffer

Son mutables y permiten modificar la cadena sin crear nuevos objetos cada vez.

    StringBuilder: no sincronizado → más rápido en un solo hilo.

    StringBuffer: sincronizado → seguro en múltiples hilos (herencia antigua).

java

StringBuilder sb = new StringBuilder();
sb.append("Hola");
sb.append(" Mundo");
String resultado = sb.toString();

Métodos útiles: append(), insert(), delete(), deleteCharAt(), reverse(), setCharAt().
Text Blocks (Java 15+)

Permiten escribir cadenas multilínea de forma legible, manteniendo los saltos de línea y espacios.
java

String bloque = """
        {
            "nombre": "Ana",
            "edad": 30
        }
        """;

El compilador elimina la indentación común automáticamente.

Con estos cinco temas cubiertos en profundidad, tendrás una base sólida para continuar con los siguientes bloques de conocimiento. Te sugiero crear cada archivo .md con este contenido y acompañarlo de pequeños programas de práctica en la carpeta codigo correspondiente.

01 – Clases y objetos
Definición de clase

Una clase es una plantilla o molde que describe el estado (atributos) y el comportamiento (métodos) de un conjunto de objetos. En Java todo código ejecutable está dentro de una clase.
java

public class Coche {
    // Atributos (estado)
    private String marca;
    private String modelo;
    private int velocidad;

    // Constructor
    public Coche(String marca, String modelo) {
        this.marca = marca;
        this.modelo = modelo;
        this.velocidad = 0;
    }

    // Método (comportamiento)
    public void acelerar(int incremento) {
        velocidad += incremento;
    }

    public int getVelocidad() {
        return velocidad;
    }
}

Creación de objetos (instanciación)

Un objeto es una instancia concreta de una clase. Se crea con el operador new, que reserva memoria, invoca al constructor y devuelve una referencia.
java

Coche miCoche = new Coche("Toyota", "Corolla");
miCoche.acelerar(50);
System.out.println(miCoche.getVelocidad()); // 50

    Cada objeto tiene su propia copia de los atributos de instancia.

    La variable miCoche almacena una referencia, no el objeto en sí.

Uso de this

Dentro de un método o constructor, this es una referencia al objeto actual. Se usa para:

    Distinguir atributos de parámetros con el mismo nombre (this.marca = marca).

    Llamar a otro constructor de la misma clase: this(otrosParametros) (debe ser la primera instrucción).

Miembros de clase (static)

Un miembro static pertenece a la clase, no a las instancias. Se accede con NombreClase.miembro.
java

public class Contador {
    public static int total = 0;

    public Contador() {
        total++;
    }
}
// Acceso: Contador.total

    Los métodos static solo pueden acceder directamente a otros miembros static.

    El método main es static para que la JVM pueda invocarlo sin crear un objeto.

Inicialización de objetos

Java garantiza la inicialización de los campos antes del constructor:

    Valores por defecto: 0, 0.0, false, null según el tipo.

    Inicializadores de instancia (bloques {} sin static) y asignación en la declaración (int x = 5;). Se ejecutan en orden textual antes de cada constructor.

    Constructor: el código específico que tú defines.

Existen también inicializadores estáticos (static {}) para campos static.
Sobrecarga de métodos

Se pueden definir varios métodos con el mismo nombre si sus parámetros difieren en número, tipo u orden.
java

public void configurar(int velocidad) { ... }
public void configurar(int velocidad, boolean turbo) { ... }

    El tipo de retorno no se tiene en cuenta para la sobrecarga; la ambigüedad da error.

    La sobrecarga es una forma de polimorfismo en tiempo de compilación.

Constructores sobrecargados
java

public Coche() {
    this("Desconocida", "Desconocido"); // llama al constructor principal
}

02 – Encapsulación
Definición

La encapsulación consiste en ocultar los detalles internos de una clase y exponer solo lo necesario mediante una interfaz pública. Protege la integridad de los datos y facilita la evolución del código.
Modificadores de acceso
Modificador	Clase	Paquete	Subclase	Cualquiera
private	✔️			
(default)	✔️	✔️		
protected	✔️	✔️	✔️	
public	✔️	✔️	✔️	✔️

    private: solo accesible dentro de la misma clase.

    default (sin modificador): accesible desde clases del mismo paquete.

    protected: como default más herencia (subclases aunque estén en otro paquete).

    public: desde cualquier lugar.

Buenas prácticas de encapsulación

    Declarar todos los atributos como private.

    Proporcionar métodos getters y setters públicos para acceder/modificar los datos necesarios.

    Incluir validaciones dentro de los setters para proteger invariantes.

java

public class CuentaBancaria {
    private double saldo; // encapsulado

    public double getSaldo() {
        return saldo;
    }

    public void depositar(double cantidad) {
        if (cantidad <= 0) {
            throw new IllegalArgumentException("Cantidad inválida");
        }
        saldo += cantidad;
    }

    public void retirar(double cantidad) {
        if (cantidad <= 0 || cantidad > saldo) {
            throw new IllegalArgumentException("Fondos insuficientes");
        }
        saldo -= cantidad;
    }
}

Ventajas

    Mantenibilidad: al cambiar la representación interna no se rompe el código cliente.

    Control: validaciones, sincronización, registro de accesos.

    Principio del menor privilegio: cada clase expone solo lo que otras necesitan.

Relación con paquetes

Agrupar clases relacionadas en paquetes permite usar el nivel de acceso default para que colaboren entre sí sin exponerse al exterior.
03 – Herencia
Concepto

La herencia permite que una clase (subclase) adquiera los atributos y métodos de otra (superclase) mediante la palabra clave extends. Representa una relación "es-un" (un Coche es un Vehículo).
java

public class Vehiculo {
    protected String matricula;
    private double velocidad; // no accesible directamente en subclases

    public void acelerar(double cantidad) {
        velocidad += cantidad;
    }
    // getters y setters públicos permiten a la subclase manipular velocidad
}

public class Coche extends Vehiculo {
    private int puertas;

    public Coche(String matricula, int puertas) {
        this.matricula = matricula; // accesible por ser protected
        this.puertas = puertas;
    }

    // puedo sobreescribir métodos si lo deseo
    @Override
    public void acelerar(double cantidad) {
        // comportamiento específico para coche
        super.acelerar(cantidad * 1.1); // llamada al método del padre
    }
}

La clase Object

Toda clase hereda implícitamente de java.lang.Object. Métodos como toString(), equals(), hashCode() siempre están disponibles.
¿Qué NO se hereda?

    Constructores: cada clase define sus propios constructores.

    Miembros private: no son directamente accesibles en la subclase, aunque la herencia del estado interno existe (se puede acceder mediante getters protegidos/públicos).

Uso de super

    super(): invoca al constructor de la superclase (debe ser la primera línea).

    super.metodo(): llama a un método sobrescrito en el padre.

    Si no se escribe super(), implícitamente se llama al constructor sin argumentos del padre (si existe).

java

public class Coche extends Vehiculo {
    public Coche() {
        super(); // llamada implícita al constructor sin argumentos de Vehiculo
    }
}

Si el padre no tiene constructor sin argumentos, la subclase debe llamar a super(...) explícitamente.
Sobrescritura de métodos (@Override)

Una subclase puede redefinir un método heredado si cumple:

    Misma firma (nombre y lista de parámetros).

    Tipo de retorno igual o subtipo (covarianza de retorno).

    Visibilidad no más restrictiva (por ejemplo, protected puede pasar a public, pero no a private).

    No puede lanzar excepciones checked más amplias que el método original.

Se recomienda anotar con @Override para que el compilador verifique.
Métodos y clases final

    Un método marcado final no puede ser sobrescrito en subclases.

    Una clase final no puede ser extendida.

Herencia simple vs múltiple

Java soporta herencia simple de clases (una clase solo puede extender de una superclase) para evitar ambigüedades, pero permite herencia múltiple de interfaces.
Inicialización en herencia

La construcción de un objeto hijo sigue este orden:

    Se invoca al constructor de la clase padre (hasta Object).

    Se ejecutan los inicializadores de instancia de la propia clase.

    Se ejecuta el resto del constructor de la clase hija.

04 – Polimorfismo
Definición

Capacidad de una variable de referencia de un tipo padre de apuntar a objetos de distintas subclases, y que el método invocado se resuelva según el objeto real en tiempo de ejecución (enlace dinámico).
java

Vehiculo v1 = new Coche();
Vehiculo v2 = new Moto();

v1.acelerar(50); // llama a Coche.acelerar() si está sobrescrito
v2.acelerar(50); // llama a Moto.acelerar()

Tipos de polimorfismo en Java

    En tiempo de compilación (sobrecarga): el compilador selecciona la versión del método según los parámetros.

    En tiempo de ejecución (sobrescritura): la JVM selecciona el método basándose en el tipo real del objeto.

Variables polimórficas

Una variable de tipo más general puede contener referencias de subtipos. Esto es esencial para colecciones, parámetros de métodos, etc.
java

public void matricular(Vehiculo v) { ... }
// acepta Coche, Moto, Camion... todos Vehiculo

Casting de objetos (conversión)

    Upcasting: implícito, de subclase a superclase (Vehiculo v = new Coche();).

    Downcasting: explícito, necesario para acceder a métodos específicos de la subclase.

java

Vehiculo v = new Coche();
Coche c = (Coche) v; // válido solo si v realmente apunta a un Coche
c.abrirMaletero();   // método propio de Coche

Un downcasting incorrecto lanza ClassCastException. Por eso se verifica con instanceof:
java

if (v instanceof Coche) {
    Coche c = (Coche) v;
}

Desde Java 16 se puede hacer pattern matching:
java

if (v instanceof Coche c) {
    c.abrirMaletero(); // c ya está declarada y casteada
}

El enlace dinámico

El compilador comprueba que el método existe en el tipo de la referencia, pero el código invocado será el del objeto real. Esto permite escribir código genérico que trabaje con abstracciones.
Arrays y polimorfismo

Los arrays son covariantes: Coche[] es un Vehiculo[]. Pero esto puede causar excepciones en tiempo de ejecución si se intenta almacenar un objeto no compatible:
java

Coche[] coches = new Coche[3];
Vehiculo[] vehiculos = coches; // OK en compilación
vehiculos[0] = new Moto();     // ArrayStoreException en runtime

Beneficios del polimorfismo

    Código extensible: añadir nuevos subtipos no modifica el código que usa la superclase.

    Colecciones heterogéneas: List<Animal> puede contener perros, gatos...

    Inyección de dependencias y patrones de diseño (Estrategia, Factoría, etc.)

05 – Clases abstractas
Definición

Una clase abstracta es aquella que se declara con la palabra clave abstract. No puede instanciarse directamente. Su propósito es servir de base común para un grupo de subclases, compartiendo parte de la implementación y definiendo a la vez un contrato parcial.
java

public abstract class Figura {
    protected String color;

    public Figura(String color) {
        this.color = color;
    }

    // Método abstracto: sin implementación
    public abstract double area();
    public abstract double perimetro();

    // Método concreto: comportamiento común
    public void imprimirDescripcion() {
        System.out.println("Soy una figura de color " + color +
                           " con área " + area());
    }
}

Características

    Una clase abstracta puede tener constructores (los llaman las subclases mediante super).

    Puede contener tanto métodos abstractos (sin cuerpo) como métodos concretos.

    Si una clase contiene al menos un método abstracto, debe declararse abstract.

    Una clase abstracta puede no tener métodos abstractos; eso solo impide que se instancie.

    Una subclase concreta debe implementar todos los métodos abstractos heredados, o declararse también abstract.

Ejemplo de herencia
java

public class Circulo extends Figura {
    private double radio;

    public Circulo(String color, double radio) {
        super(color);       // constructor de Figura
        this.radio = radio;
    }

    @Override
    public double area() {
        return Math.PI * radio * radio;
    }

    @Override
    public double perimetro() {
        return 2 * Math.PI * radio;
    }
}

Cuándo usar clases abstractas vs interfaces

    Usa clase abstracta cuando quieras proporcionar una implementación parcial (estado, métodos concretos) y las subclases compartan un ancestro común.

    Usa interfaces cuando solo quieras definir un contrato sin estado (o con comportamiento por defecto no ligado a atributos).

06 – Interfaces
Definición

Una interfaz es un tipo de referencia que define un conjunto de métodos (contrato) que las clases pueden implementar. Hasta Java 7 solo podían contener métodos abstractos y constantes. A partir de Java 8 se enriquecieron con métodos default y static.
java

public interface Volador {
    // Constantes (implicitamente public static final)
    int ALTITUD_MAXIMA = 10000;

    // Método abstracto (implicitamente public abstract)
    void despegar();
    void volar();
    void aterrizar();

    // Método default (Java 8+)
    default void planear() {
        System.out.println("Planeando suavemente");
    }

    // Método estático (Java 8+)
    static void mostrarTipo() {
        System.out.println("Soy un objeto volador");
    }
}

Implementación de una interfaz

Una clase utiliza la palabra implements. Debe proporcionar implementación para todos los métodos abstractos definidos en la interfaz (salvo que sea abstracta).
java

public class Pajaro implements Volador {
    @Override
    public void despegar() {
        System.out.println("El pájaro salta y bate las alas");
    }
    @Override
    public void volar() { ... }
    @Override
    public void aterrizar() { ... }
}

Una clase puede implementar múltiples interfaces:
java

public class Hidroavion implements Volador, Navegable { ... }

Herencia entre interfaces

Una interfaz puede heredar de varias interfaces con extends:
java

public interface VehiculoAnfibio extends Volador, Navegable {
    void activarModoAnfibio();
}

Métodos default y resolución de conflictos

Un método default tiene implementación. Si una clase implementa dos interfaces con métodos default con la misma firma, la clase debe sobrescribir el método y puede llamar a la versión deseada con Interfaz.super.metodo().
java

public class C implements A, B {
    @Override
    public void accion() {
        A.super.accion(); // elijo la implementación de A
    }
}

Métodos private en interfaces (Java 9+)

Sirven para compartir código entre métodos default y static sin exponerlo.
java

public interface Calculadora {
    default int sumar(int a, int b) {
        log("Sumando...");
        return a + b;
    }
    private void log(String mensaje) {
        System.out.println("Log: " + mensaje);
    }
}

Interfaces funcionales

Son interfaces con exactamente un método abstracto. Son la base de las expresiones lambda.
java

@FunctionalInterface
public interface Operacion {
    int ejecutar(int a, int b);
}
// Uso con lambda
Operacion suma = (a, b) -> a + b;

Consideraciones de diseño

    Las interfaces definen capacidades (que algo sea “Volador”, “Comparable”) y normalmente no contienen estado (salvo constantes).

    A partir de Java 8, la línea entre interfaces y clases abstractas se difuminó. La regla general: si necesitas estado (atributos) usa clase abstracta; si quieres un contrato puro o comportamientos adicionales mezclables, prefiere interfaces.

07 – Clases anidadas (Nested Classes)

Java permite definir una clase dentro de otra. Según el contexto y los modificadores, tenemos cuatro tipos:

    Clase interna miembro (no estática, dentro de otra clase).

    Clase estática anidada (static).

    Clase local (dentro de un método o bloque).

    Clase anónima (expresión sin nombre que implementa una interfaz o extiende una clase al vuelo).

1. Clase interna miembro

Está definida dentro de una clase sin el modificador static. Tiene acceso directo a todos los miembros (incluso private) de la clase externa, porque existe ligada a una instancia de la externa.
java

public class Contenedor {
    private int dato = 10;

    // Clase interna miembro
    public class Interna {
        public void mostrar() {
            System.out.println(dato); // acceso directo al privado
        }
    }

    public void crearYMostrar() {
        Interna i = new Interna();
        i.mostrar();
    }
}

// Uso externo: necesitamos un objeto de la clase externa
Contenedor c = new Contenedor();
Contenedor.Interna i = c.new Interna();
i.mostrar();

Características:

    La clase interna genera un fichero .class con nombre Externa$Interna.class.

    No puede tener miembros static (a menos que sean static final constantes).

    Puede implementar interfaces o heredar de otras clases.

    El objeto interno tiene una referencia implícita al objeto externo que lo creó. Para referirse explícitamente: Externa.this.

2. Clase estática anidada

Lleva el modificador static. Es similar a una clase de nivel superior, pero anidada para organización. No tiene acceso directo a miembros no estáticos de la clase externa (necesita una instancia).
java

public class Externa {
    private static int contador = 1;
    private int id = 5;

    public static class AnidadaEstatica {
        public void mostrar() {
            System.out.println(contador); // sí, es estática
            // System.out.println(id); // error, id no es estático
        }
    }
}

// Uso sin objeto externo:
Externa.AnidadaEstatica ae = new Externa.AnidadaEstatica();
ae.mostrar();

Cuándo usarla: cuando la clase anidada solo necesita usar miembros estáticos de la externa o se quiere agrupar lógicamente sin acoplar la instancia.
3. Clase local

Se define dentro de un método (o bloque, como un bucle). Su alcance es ese bloque. Puede acceder a variables locales del método si son final o effectively final (a partir de Java 8, effectively final: no se modifican tras su inicialización).
java

public class Impresora {
    public void imprimir(boolean detalle) {
        int version = 1; // effectively final (no se reasigna)

        class FormatoDetallado {
            void aplicar(String texto) {
                // Acceso a variable local del método (debe ser effectively final)
                System.out.println("v" + version + " " + texto);
            }
        }

        if (detalle) {
            FormatoDetallado fd = new FormatoDetallado();
            fd.aplicar("Reporte");
        }
    }
}

Reglas:

    Solo puede definirse dentro de un bloque con llaves.

    Puede implementar interfaces o heredar.

    Puede acceder a variables locales y parámetros del método siempre que sean final o effectively final.

    No puede declarar miembros estáticos (salvo constantes).

4. Clase anónima

Es una expresión, no una declaración con nombre. Se usa para crear una instancia de una interfaz o una clase abstracta concreta sobre la marcha, sin necesidad de crear una clase aparte.
java

// Implementando interfaz Runnable
Runnable tarea = new Runnable() {
    @Override
    public void run() {
        System.out.println("Ejecutando");
    }
};

// Extendiendo una clase (abstracta o no) e implementando método
Figura circulo = new Figura("rojo") {
    @Override
    public double area() {
        return 3.14 * 5 * 5;
    }
    @Override
    public double perimetro() {
        return 2 * 3.14 * 5;
    }
};

Características:

    Se crean con new Interfaz() { ... } o new Clase(parámetros) { ... }.

    Pueden acceder a variables del contexto que las envuelve, con la misma regla de efectividad final.

    Útiles en callbacks, listeners, comparators y como evolución antes de las lambdas.

    No pueden tener constructores explícitos (solo el inicializador de instancia {}).

Nota: Desde Java 8, las interfaces funcionales se implementan más limpiamente con lambdas, dejando las anónimas para cuando necesites varias métodos o estado adicional.
08 – Records (Java 14 como preview, definitivo en 16)
Concepto

Un record es un tipo especial de clase inmutable diseñada para transportar datos de forma transparente. El compilador genera automáticamente:

    Constructor canónico (con todos los componentes).

    Métodos de acceso (getters) con el mismo nombre que el componente (sin el prefijo get).

    equals(), hashCode() y toString() basados en los componentes.

java

public record Punto(int x, int y) { }

Punto p = new Punto(3, 4);
System.out.println(p.x()); // 3, getter automático
System.out.println(p.y()); // 4
System.out.println(p);     // Punto[x=3, y=4]

Propiedades

    Son finales: no se puede extender un record (el compilador marca la clase como final).

    Inmutables: los campos son private final. No hay setters.

    Se puede declarar el constructor canónico para validar o normalizar parámetros:

java

public record Punto(int x, int y) {
    // Constructor compacto: no se repiten los parámetros, se asignan al final.
    public Punto {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException("Coordenadas no negativas");
        }
    }
}

También se puede escribir el constructor canónico completo, pero el compacto es más conciso.
Métodos adicionales y personalización

Puedes sobrescribir cualquier método generado (como toString()) o añadir métodos de instancia y estáticos.
java

public record Persona(String nombre, int edad) {
    public boolean esMayorDeEdad() {
        return edad >= 18;
    }

    public static Persona crearAnonimo() {
        return new Persona("Anónimo", 0);
    }
}

Los records pueden contener campos estáticos, pero no pueden declarar campos de instancia adicionales (romperían la definición de dato).
Implementación de interfaces

Un record puede implementar interfaces, por ejemplo para ordenar:
java

public record Medicion(double valor, String unidad) implements Comparable<Medicion> {
    @Override
    public int compareTo(Medicion otra) {
        return Double.compare(this.valor, otra.valor);
    }
}

Desestructuración con Pattern Matching (Java 19+ preview)

Permite extraer componentes directamente:
java

if (obj instanceof Punto(int x, int y)) {
    System.out.println("Coordenada: " + x + ", " + y);
}

¿Cuándo usarlos?

    DTOs (Data Transfer Objects).

    Claves compuestas para mapas.

    Tuplas y resultados de consultas.

    Cualquier modelo de valor inmutable.

Ventajas: reducen el boilerplate, mejoran la legibilidad, serialización y compatibilidad con nuevas funcionalidades.
09 – Enumeraciones (enum)
Definición

Un enum es un tipo especial de clase que define un conjunto fijo de constantes. Cada constante es una instancia pública, estática y final del propio enum.
java

public enum DiaSemana {
    LUNES, MARTES, MIERCOLES, JUEVES, VIERNES, SABADO, DOMINGO
}

DiaSemana hoy = DiaSemana.LUNES;

Características principales

    enum extiende implícitamente java.lang.Enum. No puede heredar de otra clase, pero puede implementar interfaces.

    Las constantes se definen en la primera línea, separadas por comas; si hay código adicional (constructores, métodos), se termina con punto y coma.

    El constructor de un enum es privado (implícitamente), no se pueden crear nuevas instancias fuera del enum.

    Pueden tener atributos, constructores y métodos como cualquier clase.

Ejemplo con atributos y constructor
java

public enum Color {
    ROJO(255, 0, 0),
    VERDE(0, 255, 0),
    AZUL(0, 0, 255);

    private final int r, g, b;

    Color(int r, int g, int b) {
        this.r = r;
        this.g = g;
        this.b = b;
    }

    public String rgb() {
        return String.format("(%d,%d,%d)", r, g, b);
    }
}

System.out.println(Color.ROJO.rgb()); // (255,0,0)

Métodos implícitos de Enum

    values(): devuelve un array con todas las constantes en orden de declaración.

    valueOf(String): obtiene la constante por nombre (DiaSemana.valueOf("LUNES")).

    name(): nombre exacto de la constante.

    ordinal(): posición en la declaración (0-index). ¡Cuidado al usarlo! El orden puede cambiar entre versiones.

Enum con métodos abstractos (comportamiento específico)

Cada constante puede sobrescribir métodos definidos en el enum.
java

public enum Operacion {
    SUMA {
        @Override
        public double aplicar(double a, double b) { return a + b; }
    },
    RESTA {
        @Override
        public double aplicar(double a, double b) { return a - b; }
    };

    public abstract double aplicar(double a, double b);
}

Uso de interfaces y enum body

Un enum puede implementar interfaces y cada constante proporcionar la implementación.
java

public interface Saludable {
    String mensaje();
}

public enum Estado implements Saludable {
    ACTIVO { public String mensaje() { return "En marcha"; } },
    INACTIVO { public String mensaje() { return "Detenido"; } }
}

Patrones de diseño con enum

    Singleton: un enum con una sola constante (INSTANCIA). Es la forma más segura (serialización, reflexión).

    Strategy: cada constante implementa un algoritmo.

    Maquina de estados: cada constante es un estado y los métodos realizan transiciones.

Consideraciones avanzadas

    No se pueden crear instancias con new, pero se pueden usar en switch directamente (sin calificar el enum en los case desde Java 14+).

    Son comparables por == (las constantes son singletons) y por compareTo (según ordinal).

    Poseen equals y hashCode automáticos.

10 – Sealed Classes (Java 17)
Concepto

Las sealed classes (clases selladas) permiten restringir qué clases pueden extender o implementar una clase o interfaz. Con esto se consigue un modelado de dominio cerrado, que permite al compilador verificar exhaustividad en switch y pattern matching.

Se declaran con sealed y la cláusula permits (opcional si las subclases están en el mismo archivo o paquete).
java

public sealed class Figura permits Circulo, Cuadrado, Triangulo {
}

Las clases permitidas deben estar en el mismo módulo o paquete (si no hay módulo) y deben especificar su relación:

    final: no admite más subclases.

    sealed: da otra capa de permisos.

    non-sealed: vuelve a abrir la jerarquía para cualquier extensión.

java

final class Circulo extends Figura { ... }
non-sealed class Cuadrado extends Figura { ... } // cualquiera puede extender Cuadrado
sealed class Triangulo extends Figura permits Equilatero, Isosceles { ... }

Interfaces selladas

Las interfaces también pueden sellarse:
java

public sealed interface OperacionMatematica permits Suma, Resta, Multiplicacion { }

Los permits pueden ser otras interfaces o clases concretas.
Ventajas

    Seguridad en el modelado: sabes exactamente qué subtipos pueden existir.

    Exhaustividad en pattern matching: si usas switch sobre una sealed class, el compilador puede comprobar que cubriste todos los casos sin necesidad de default.

java

Figura f = ...;
double area = switch (f) {
    case Circulo c -> Math.PI * c.radio() * c.radio();
    case Cuadrado c -> c.lado() * c.lado();
    case Triangulo t -> t.base() * t.altura() / 2;
    // Si faltara un caso, error en compilación
};

    Diseño orientado a dominio: modela conceptos cerrados (por ejemplo, un tipo de resultado: Éxito o Error).

Combinación con records

Muy potente: definen una jerarquía de datos cerrada y el compilador puede “desestructurar” con pattern matching.
java

sealed interface Resultado permits Exito, Fallo { }
record Exito(String mensaje) implements Resultado { }
record Fallo(int codigo, String razon) implements Resultado { }

void manejar(Resultado r) {
    switch (r) {
        case Exito(var msg) -> System.out.println("OK: " + msg);
        case Fallo(var code, var razon) -> System.out.println("Error " + code);
    }
}

Reglas de ubicación

    Las clases permitidas deben ser accesibles en tiempo de compilación.

    Si el archivo fuente contiene la clase sellada, las subclases permitidas pueden estar en el mismo archivo (sin necesidad de permits).

    Si se especifica permits, todas las listadas deben extender/implementar la sellada.

Cuándo usarlas

    Jerarquías de tipos acotadas (por ejemplo, un AST de un lenguaje, respuestas de una API).

    Cuando quieras garantizar que solo existen las variantes definidas, para facilitar la evolución y el mantenimiento.

Bloque 03 – Excepciones
01-excepciones.md
1. ¿Qué es una excepción?

Una excepción es un evento que ocurre durante la ejecución de un programa y que interrumpe el flujo normal de instrucciones. Java proporciona un mecanismo robusto para manejar estas situaciones mediante objetos que representan el error y se propagan por la pila de llamadas hasta ser capturados.

Ventajas del manejo de excepciones:

    Separar código normal del código de gestión de errores.

    Propagar errores hacia capas superiores de forma ordenada.

    Agrupar y diferenciar tipos de error.

2. Jerarquía de excepciones
text

java.lang.Throwable
├── java.lang.Error
└── java.lang.Exception
    └── java.lang.RuntimeException

    Throwable: raíz de todo. Métodos: getMessage(), printStackTrace(), etc.

    Error: condiciones excepcionales externas a la aplicación (p.ej. OutOfMemoryError, StackOverflowError). Normalmente no se capturan ni se tratan.

    Exception: situaciones que una aplicación podría querer capturar. Se subdivide en:

        Checked exceptions (excepciones verificadas): herencia directa de Exception pero no de RuntimeException. El compilador obliga a declararlas en la firma (throws) o capturarlas. Ejemplos: IOException, SQLException.

        Unchecked exceptions: RuntimeException y sus subclases. No obligan a captura; suelen indicar errores de programación. Ejemplos: NullPointerException, ArrayIndexOutOfBoundsException, IllegalArgumentException.

3. Bloques try-catch

Estructura básica:
java

try {
    // Código que puede lanzar una excepción
} catch (TipoExcepcion nombre) {
    // Manejo del error
}

Flujo:

    Si dentro del try ocurre una excepción de tipo TipoExcepcion, se ejecuta el bloque catch y luego el programa continúa después del bloque.

    Si no ocurre, se salta el catch.

    Los bloques catch se evalúan en orden; debe capturarse primero la excepción más específica.

Múltiples catch:
java

try {
    // ...
} catch (FileNotFoundException e) {
    // específica
} catch (IOException e) {
    // más genérica
}

Multi-catch (Java 7+): captura varias excepciones en un solo catch separadas por |.
java

try {
    // ...
} catch (IOException | SQLException e) {
    // manejo común
}

4. finally

El bloque finally se ejecuta siempre, haya o no excepción, e incluso si se ejecuta return dentro del try o catch (excepto si se llama a System.exit()).
java

try {
    // operación riesgosa
} catch (Exception e) {
    // manejo
} finally {
    // liberar recursos (cerrar ficheros, conexiones, etc.)
    // se ejecuta siempre
}

Importante: Si un método tiene return en try, el finally se ejecuta antes de retornar. Si el finally también tiene return, ese valor sobrescribe al anterior.
5. throw y throws

    throw: lanza explícitamente una excepción.
    java

    throw new IllegalArgumentException("Edad no válida");

    throws: declara en la firma de un método qué excepciones verificadas puede lanzar.
    java

    public void leerArchivo(String ruta) throws IOException {
        // ...
    }

    Una subclase que sobrescribe un método no puede declarar más excepciones verificadas que el método original (puede declarar ninguna o subtipos).

6. try-with-resources (Java 7+)

Cuando se usan recursos que implementan java.lang.AutoCloseable (como FileInputStream, Connection), se pueden declarar dentro de paréntesis en el try. El recurso se cierra automáticamente al final, incluso si ocurre una excepción.
java

try (BufferedReader br = new BufferedReader(new FileReader("datos.txt"))) {
    String linea = br.readLine();
} catch (IOException e) {
    e.printStackTrace();
}
// br.close() se llama automáticamente

Pueden declararse múltiples recursos separados por ;. Se cierran en orden inverso al de declaración. Si tanto el bloque try como el cierre lanzan excepción, se suprime la del cierre (se puede acceder con getSuppressed()).
7. Excepciones personalizadas

Se pueden crear extendiendo Exception (checked) o RuntimeException (unchecked).
java

public class SaldoInsuficienteException extends Exception {
    public SaldoInsuficienteException(String mensaje) {
        super(mensaje);
    }
    public SaldoInsuficienteException(String mensaje, Throwable causa) {
        super(mensaje, causa);
    }
}

Uso:
java

if (saldo < cantidad) {
    throw new SaldoInsuficienteException("No hay fondos");
}

Conveniencia: incluir siempre constructores con mensaje y causa para facilitar el encadenamiento.
8. Encadenamiento de excepciones

Al capturar una excepción y lanzar otra, se puede conservar la causa original pasándola como segundo argumento.
java

try {
    // ...
} catch (IOException e) {
    throw new MiExcepcion("Error al procesar", e);
}

Al imprimir la traza, se mostrará la causa raíz. Métodos: getCause().
9. Buenas prácticas

    No tragar excepciones: evitar catch (Exception e) { } sin al menos registrar el error.

    Usar excepciones específicas: NumberFormatException en lugar de Exception.

    Preferir excepciones estándar cuando apliquen: IllegalArgumentException, IllegalStateException, NullPointerException, IndexOutOfBoundsException.

    No lanzar o capturar Throwable, salvo casos muy especiales.

    Documentar con @throws en Javadoc.

    Liberar recursos con try-with-resources, no en finally manual.

    No usar excepciones como flujo de control; son caras y oscurecen el código.

10. Resumen visual del flujo
text

try {
    // 1. Código normal
    // 2. Si ocurre una excepción, salta al catch
    // 3. Si no, sigue
} catch (Tipo1 e) {
    // solo si excepción es Tipo1
} catch (Tipo2 e) {
    // ...
} finally {
    // siempre se ejecuta
}

Bloque 04 – Colecciones y Genéricos
01-generics.md
1. Introducción

Los genéricos permiten que clases, interfaces y métodos operen con un tipo de dato parametrizado, garantizando seguridad en tiempo de compilación y eliminando la necesidad de casteos explícitos. Fueron introducidos en Java 5.

Antes de los genéricos:
java

List lista = new ArrayList();
lista.add("Hola");
String s = (String) lista.get(0); // casteo necesario

Con genéricos:
java

List<String> lista = new ArrayList<>();
lista.add("Hola");
String s = lista.get(0); // sin casteo

2. Clases genéricas

Una clase con un parámetro de tipo:
java

public class Caja<T> {
    private T contenido;

    public void guardar(T valor) {
        this.contenido = valor;
    }
    public T obtener() {
        return contenido;
    }
}

Caja<String> cajaStr = new Caja<>();
cajaStr.guardar("Libro");
String contenido = cajaStr.obtener();

    Se pueden usar múltiples parámetros: class Par<K, V>.

    Por convención se usan letras mayúsculas: E (elemento), K (clave), V (valor), T, S, U.

3. Métodos genéricos

Los métodos pueden tener sus propios parámetros de tipo, independientes de la clase.
java

public <T> void imprimir(T[] array) {
    for (T elem : array) {
        System.out.println(elem);
    }
}

Invocación con inferencia de tipo: imprimir(numerosInteger); o explícita Util.<String>imprimir(cadenas);
4. Tipos parametrizados acotados (bounded)

Se restringe el tipo permitido con extends (que significa “es un subtipo de”):
java

public class OperacionesMatematicas<T extends Number> {
    public double sumar(T a, T b) {
        return a.doubleValue() + b.doubleValue();
    }
}

T puede ser Number o cualquier subclase.
En métodos:
java

public <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) > 0 ? a : b;
}

Múltiples límites: <T extends Clase & Interfaz1 & Interfaz2>. La clase (si la hay) debe ir primero.
5. Wildcards (comodines)

Permiten flexibilidad cuando se usa un tipo genérico como parámetro de un método.

    ? (comodín no acotado): representa cualquier tipo.
    java

    public void imprimir(List<?> lista) {
        for (Object elem : lista) { ... }
    }

    ? extends T (upper bounded wildcard): acepta T o cualquier subtipo. Útil para leer datos (covarianza).
    java

    public double sumaTotal(List<? extends Number> numeros) {
        double total = 0;
        for (Number n : numeros) total += n.doubleValue();
        return total;
    }

    No se puede escribir en la lista (excepto null).

    ? super T (lower bounded wildcard): acepta T o cualquier supertipo. Útil para escribir datos (contravarianza).
    java

    public void agregarNumeros(List<? super Integer> lista) {
        lista.add(10); // OK, Integer cabe en cualquier supertipo de Integer
    }

    Se puede añadir T o subtipos, pero al leer se obtiene Object.

Principio PECS (Producer Extends, Consumer Super):

    Si una función recibe una colección para leer de ella, usa ? extends T.

    Si recibe para escribir en ella, usa ? super T.

    Si hace ambas, no usar comodín (tipo exacto).

6. Type erasure (borrado de tipos)

Los genéricos en Java se implementan mediante un mecanismo llamado borrado de tipos. En tiempo de compilación, el compilador elimina la información genérica y reemplaza:

    Los tipos sin límite por Object.

    Los tipos acotados por su primer límite.

    Inserta conversiones (cast) cuando es necesario.

Consecuencias:

    No se puede usar instanceof con un tipo parametrizado: if (objeto instanceof List<String>) no compila.

    No se puede crear instancias de T (new T()).

    No se pueden crear arrays de tipos genéricos (new T[10]), pero se puede (T[]) new Object[10].

    No se sobrecargan métodos porque tras el borrado las firmas pueden ser iguales.

7. Restricciones suavizadas

    No hay tipos primitivos como parámetro: debes usar los wrappers (List<Integer> no List<int>).

    Un método estático no puede usar el tipo genérico de la clase porque pertenece a la clase sin instancia; debe declarar sus propios parámetros de tipo.

8. Operador diamante (Java 7)
java

List<String> lista = new ArrayList<>(); // <> infiere el tipo del contexto

Es obligatorio en el lado derecho (si no, funciona como raw type y emite advertencia).
9. Raw types

Usar una clase genérica sin parámetros (raw type) es compatible hacia atrás, pero pierde la seguridad y genera advertencias. Evitar siempre.
02-list-set-map.md
1. Framework de Colecciones

Conjunto de interfaces y clases que proporcionan estructuras de datos reutilizables. Principales interfaces:
text

                    Iterable
                       |
                    Collection
           (add, remove, size, etc.)
           /           |          \
        List          Set        Queue
       (ordenada,    (sin          (cola)
        duplicados)  duplicados)

         Map
   (pares clave-valor; no es Collection)

El paquete es java.util.

Métodos comunes en Collection:

    boolean add(E e)

    boolean remove(Object o)

    boolean contains(Object o)

    int size()

    boolean isEmpty()

    void clear()

    Iterator<E> iterator()

2. List

Interfaz que representa una secuencia ordenada que admite duplicados. Ofrece acceso posicional.

Implementaciones principales:

    ArrayList: array redimensionable. Acceso rápido por índice O(1). Inserciones/eliminaciones en el medio costosas O(n). Buen rendimiento como lista general.

    LinkedList: lista doblemente enlazada. Buen rendimiento en inserciones/eliminaciones en los extremos y en el medio O(1) si ya tenemos la referencia. Acceso por índice O(n). También implementa Deque.

    Vector: antigua, sincronizada, casi en desuso.

Ejemplos:
java

List<String> lista = new ArrayList<>();
lista.add("A");
lista.add("B");
lista.add(0, "X"); // inserta en posición
String primer = lista.get(0);  // "X"

for (String s : lista) {
    System.out.println(s);
}

3. Set

Interfaz que modela un conjunto matemático: sin duplicados (según equals()). Puede permitir a lo sumo un null.

Implementaciones:

    HashSet: basado en HashMap. Orden no predecible. Operaciones básicas O(1). Requiere que los elementos implementen correctamente hashCode() y equals().

    LinkedHashSet: mantiene una lista enlazada que preserva el orden de inserción. Un poco más lento que HashSet.

    TreeSet: implementa SortedSet y NavigableSet. Los elementos se ordenan según su orden natural (Comparable) o un Comparator dado en el constructor. Complejidad O(log n). No permite null (si se usa comparación natural salvo que se permita en el comparador).

java

Set<String> set = new HashSet<>();
set.add("uno");
set.add("uno"); // ignorado
set.add("dos");
System.out.println(set); // ej: [uno, dos]

4. Map

Almacena pares clave-valor. No extiende Collection. Las claves son únicas y se basan en equals() y hashCode() (para versiones hash).

Métodos básicos:

    V put(K key, V value): inserta o actualiza, retorna el valor anterior o null.

    V get(Object key)

    boolean containsKey(Object key)

    boolean containsValue(Object value)

    Set<K> keySet(): conjunto de claves.

    Collection<V> values()

    Set<Map.Entry<K,V>> entrySet(): pares clave-valor.

Implementaciones:

    HashMap: tabla hash sin orden. Operaciones O(1). Permite una clave null y múltiples valores null.

    LinkedHashMap: mantiene orden de inserción (o de acceso si se configura). Ligeramente más lento.

    TreeMap: ordena las claves (orden natural o Comparator). O(log n). No admite claves null.

    Hashtable: legado, sincronizada, no permite null. Sustituida por ConcurrentHashMap para concurrencia.

Recorrer un mapa:
java

Map<String, Integer> mapa = new HashMap<>();
mapa.put("A", 1);
mapa.put("B", 2);

for (Map.Entry<String, Integer> entry : mapa.entrySet()) {
    System.out.println(entry.getKey() + " -> " + entry.getValue());
}

// Java 8+ forEach
mapa.forEach((k, v) -> System.out.println(k + ": " + v));

5. Queue y Deque

    Queue: define operaciones de cola (FIFO). Métodos: offer (inserta), poll (extrae y retorna cabeza o null), peek (consulta cabeza). Clases: LinkedList, PriorityQueue.

    Deque: cola doblemente terminada (puede actuar como pila o cola). Métodos: addFirst, addLast, offerFirst, etc. ArrayDeque es mejor que LinkedList como pila (no sincronizada, más rápida).

6. Contratos importantes

Para usar correctamente HashSet, HashMap y otros basados en hash, debes asegurar:

    Si dos objetos son iguales según equals(), sus hashCode() deben ser iguales.

    Si dos objetos tienen el mismo hashCode(), no es obligatorio que sean equals() (colisiones).

    La implementación de estos métodos debe ser estable durante el tiempo que el objeto esté en la colección.

    Siempre sobrescribir ambos juntos.

03-ordenacion.md
1. Orden natural con Comparable<T>

La interfaz java.lang.Comparable<T> impone un orden natural a los objetos de una clase. Tiene un único método:
java

public int compareTo(T o);

Reglas:

    Retorna un entero negativo si this < o

    Cero si this == o (según equivalencia para ordenación)

    Positivo si this > o

Muchas clases de Java la implementan: String, Integer, LocalDate, etc.
java

List<Integer> numeros = Arrays.asList(3, 1, 2);
Collections.sort(numeros); // usa compareTo de Integer

Para que una clase propia tenga orden natural:
java

public class Persona implements Comparable<Persona> {
    private String nombre;
    private int edad;

    @Override
    public int compareTo(Persona o) {
        return this.nombre.compareTo(o.nombre); // orden por nombre
    }
}

Importante: La consistencia con equals es recomendada pero no obligatoria. Si compareTo dice 0 pero equals dice false, las colecciones ordenadas como TreeSet pueden comportarse de manera extraña (no perder elementos pero Set espera igualdad lógica).
2. Orden personalizado con Comparator<T>

java.util.Comparator<T> permite definir múltiples criterios de ordenación externos a la clase.

Método: int compare(T o1, T o2). Mismas reglas de retorno que compareTo.

Creación tradicional (clase anónima):
java

Comparator<Persona> porEdad = new Comparator<>() {
    public int compare(Persona p1, Persona p2) {
        return Integer.compare(p1.getEdad(), p2.getEdad());
    }
};

Con lambda:
java

Comparator<Persona> porEdad = (p1, p2) -> Integer.compare(p1.getEdad(), p2.getEdad());

3. Métodos de utilidad de Comparator (Java 8+)

La clase Comparator ofrece métodos estáticos que simplifican la creación de comparadores:

    Comparator.comparing(Function keyExtractor): crea un comparador que aplica la función a los objetos y compara los resultados (que deben implementar Comparable).

    Comparator.comparingInt/ToDouble/ToLong para primitivos.

    .thenComparing(keyExtractor) para encadenar criterios.

    .reversed() para orden inverso.

    .nullsFirst() / .nullsLast() para manejar nulos.

Ejemplo elegante:
java

Comparator<Persona> comp = Comparator.comparing(Persona::getApellido)
                                     .thenComparing(Persona::getNombre)
                                     .reversed();

List<Persona> personas = ...;
personas.sort(comp);

4. Ordenación de colecciones

    Collections.sort(List<T> list): ordena una lista según el orden natural (requiere T extends Comparable).

    Collections.sort(List<T> list, Comparator<? super T> c): ordena con comparador.

    A partir de Java 8, todas las listas tienen list.sort(Comparator).

    Stream.sorted() con o sin comparador.

5. Colecciones ordenadas: TreeSet y TreeMap

    TreeSet: implementa SortedSet. Sus elementos se mantienen en orden ascendente según el orden natural o un Comparator suministrado en el constructor. No permite null.
    java

    TreeSet<String> palabras = new TreeSet<>(Comparator.comparing(String::length));
    palabras.add("abc");

    TreeMap: implementa SortedMap. Análogo con claves.

Requisito: o bien los elementos implementan Comparable, o bien se pasa un Comparator explícito. En caso contrario, ClassCastException en tiempo de ejecución al insertar.
6. Resumen de estrategias de ordenación
Situación	Solución
Una única forma natural de ordenar la clase	Implementar Comparable
Múltiples criterios, o no puedes modificar la clase	Usar Comparator (lambdas, comparing)
Necesitas una colección siempre ordenada	TreeSet/TreeMap con comparador
Ordenar una lista una vez	list.sort(comparator) o Collections.sort

Bloque 05 – Entrada/Salida y NIO.2
01-flujos-archivos.md
1. Introducción a I/O en Java

Java proporciona dos grandes API para trabajar con entrada/salida:

    java.io: clásica, basada en streams (flujos de bytes o caracteres). Modelo secuencial, bloqueante.

    java.nio.file (NIO.2): moderna, añadida en Java 7. Basada en canales y buffers, con operaciones no bloqueantes y gestión avanzada del sistema de archivos.

Ambas conviven; para tareas sencillas con archivos se recomienda NIO.2 por su simplicidad y claridad.
2. Streams de bytes (InputStream / OutputStream)
Lectura de bytes
java

InputStream is = new FileInputStream("archivo.bin");
int byteLeido;
while ((byteLeido = is.read()) != -1) {
    // procesar byteLeido (0-255)
}
is.close();

    read() devuelve un int (0-255) o -1 al final.

    read(byte[] buffer) lee hasta buffer.length bytes y retorna el número real leído o -1.

Escritura de bytes
java

OutputStream os = new FileOutputStream("salida.bin");
os.write(65); // escribe el byte 65 ('A')
byte[] datos = {66, 67, 68};
os.write(datos);
os.close();

Decoradores para eficiencia y funcionalidad

El patrón Decorador envuelve un stream básico añadiendo capacidades:

    BufferedInputStream / BufferedOutputStream: añaden un buffer para minimizar las llamadas al sistema operativo, mejorando el rendimiento.
    java

    InputStream in = new BufferedInputStream(new FileInputStream("archivo.bin"));

    DataInputStream / DataOutputStream: permiten leer/escribir tipos primitivos y cadenas.
    java

    DataOutputStream dos = new DataOutputStream(new BufferedOutputStream(
                                    new FileOutputStream("data.bin")));
    dos.writeInt(10);
    dos.writeUTF("Hola");

    ObjectInputStream / ObjectOutputStream: para serialización de objetos (ver sección correspondiente).

Cierre: siempre en try-with-resources para evitar fugas.
3. Streams de caracteres (Reader / Writer)

Trabajan con caracteres en lugar de bytes, manejando automáticamente las codificaciones de texto.
java

Reader reader = new FileReader("texto.txt", StandardCharsets.UTF_8);
BufferedReader br = new BufferedReader(reader);
String linea;
while ((linea = br.readLine()) != null) {
    System.out.println(linea);
}
br.close();

    FileReader / FileWriter: puente entre bytes y caracteres; se puede especificar el Charset.

    BufferedReader / BufferedWriter: buffer y métodos como readLine() y newLine().

    PrintWriter: métodos print, println, printf. Ideal para escritura de texto formateado.

4. Archivos: la clase File (legado) vs NIO.2
Clase File

Representa una ruta abstracta. Métodos útiles: exists(), createNewFile(), mkdir(), list(), delete(). No proporciona operaciones de lectura/escritura directamente; necesita streams.

Limitaciones: API pobre, mal manejo de errores, sin soporte simbólico.
NIO.2 (Paquete java.nio.file)

Centrado en Path y Files.

    Path: inmutable, generada a través de Paths.get("ruta") o Path.of("ruta") (Java 11+). Maneja direcciones relativas, absolutas, normalización.

    Files: clase de utilidad con métodos estáticos para operaciones comunes.

Operaciones básicas con Files:
java

Path archivo = Path.of("datos.txt");

// Lectura completa
String contenido = Files.readString(archivo);
List<String> lineas = Files.readAllLines(archivo);

// Escritura
Files.writeString(archivo, "nuevo texto");

// Copiar, mover, eliminar
Files.copy(origen, destino, StandardCopyOption.REPLACE_EXISTING);
Files.move(origen, destino);
Files.delete(archivo); // lanza excepción si no existe
Files.deleteIfExists(archivo);

// Verificar existencia, permisos, atributos
boolean existe = Files.exists(archivo);
boolean legible = Files.isReadable(archivo);
FileTime ultimaMod = Files.getLastModifiedTime(archivo);

Recorrer directorios:
java

try (Stream<Path> paths = Files.list(dir)) { // solo primer nivel
    paths.forEach(System.out::println);
}
// O con walk para recursivo
try (Stream<Path> paths = Files.walk(dir)) {
    paths.filter(Files::isRegularFile).forEach(System.out::println);
}

Vigilancia de directorios (WatchService):
Permite monitorizar cambios: creación, modificación, eliminación de archivos.
java

WatchService watcher = FileSystems.getDefault().newWatchService();
Path dir = Path.of(".");
dir.register(watcher, StandardWatchEventKinds.ENTRY_CREATE,
                         StandardWatchEventKinds.ENTRY_DELETE,
                         StandardWatchEventKinds.ENTRY_MODIFY);

while (true) {
    WatchKey key = watcher.take(); // bloquea hasta que ocurra evento
    for (WatchEvent<?> event : key.pollEvents()) {
        System.out.println(event.kind() + ": " + event.context());
    }
    key.reset();
}

5. Serialización

Proceso de convertir un objeto a una secuencia de bytes (y viceversa) para almacenarlo o transmitirlo. La clase debe implementar la interfaz marcadora java.io.Serializable.
java

class Persona implements Serializable {
    private static final long serialVersionUID = 1L;
    String nombre;
    int edad;
}

    serialVersionUID controla la compatibilidad de versiones.

    Se puede marcar campos como transient para que no se serialicen.

    Uso:
    java

    // Serializar
    try (ObjectOutputStream oos = new ObjectOutputStream(
                      new FileOutputStream("persona.ser"))) {
        oos.writeObject(persona);
    }
    // Deserializar
    try (ObjectInputStream ois = new ObjectInputStream(
                      new FileInputStream("persona.ser"))) {
        Persona p = (Persona) ois.readObject();
    }

Hoy en día se prefieren formatos como JSON o XML por interoperabilidad y seguridad.
6. Try-with-resources en detalle

Desde Java 7 cualquier recurso que implemente AutoCloseable se puede declarar en el try y se cerrará automáticamente, incluso si se lanza una excepción. El cierre ocurre en orden inverso a la declaración.
java

try (FileInputStream fis = new FileInputStream("in.bin");
     FileOutputStream fos = new FileOutputStream("out.bin")) {
    // lectura/escritura
} // ambos cierran automáticamente

Si se lanza una excepción en el bloque try y otra en el cierre, esta última es suprimida (accesible con excepcionPrincipal.getSuppressed()).
Bloque 06 – Concurrencia
01-threads.md
1. Conceptos básicos de hilos

Un hilo (thread) es la unidad más pequeña de ejecución que puede ser gestionada por el sistema operativo. Java ofrece soporte nativo para programación multihilo. Cada hilo tiene su propia pila pero comparte el heap y los objetos con otros hilos del mismo proceso.

Ventajas: aprovechamiento de CPU multinúcleo, mejor respuesta en interfaces de usuario, servidores, etc.

Riesgos: condiciones de carrera, interbloqueos, visibilidad inconsistente, problemas de sincronización.
2. Crear y lanzar hilos

Forma 1: Extender Thread
java

class MiHilo extends Thread {
    public void run() {
        System.out.println("Ejecutando en hilo: " + getName());
    }
}
MiHilo hilo = new MiHilo();
hilo.start(); // NUNCA llamar run() directamente

Forma 2: Implementar Runnable (preferida)
java

class MiRunnable implements Runnable {
    public void run() {
        System.out.println("Tarea ejecutada");
    }
}
Thread t = new Thread(new MiRunnable());
t.start();

Con lambda (Java 8+):
java

Thread t = new Thread(() -> System.out.println("Hilo lambda"));
t.start();

3. Ciclo de vida de un hilo

Estados definidos en Thread.State:

    NEW: creado pero no iniciado.

    RUNNABLE: ejecutándose o listo para ejecución en la JVM.

    BLOCKED: esperando adquirir un monitor (bloqueado en synchronized).

    WAITING: espera indefinida hasta que otro hilo lo notifique (wait(), join() sin tiempo).

    TIMED_WAITING: espera con tiempo límite (sleep(), wait(time), join(time)).

    TERMINATED: ha completado su ejecución.

Métodos importantes:

    start(): inicia el hilo.

    sleep(long millis): pausa el hilo actual; no libera bloqueos.

    join(): espera a que el hilo termine.

    interrupt(): interrumpe un hilo que está en wait/sleep/join (lanza InterruptedException).

4. Sincronización con synchronized

Cuando múltiples hilos acceden a datos compartidos, se necesita sincronizar para evitar condiciones de carrera y asegurar visibilidad.

Bloque sincronizado:
java

synchronized (objetoBloqueo) {
    // sección crítica
}

Solo un hilo puede poseer el monitor de objetoBloqueo a la vez.

Método sincronizado:
java

public synchronized void incrementar() {
    contador++;
}

Es equivalente a synchronized(this) en métodos de instancia, o a synchronized(MiClase.class) en métodos static.

Visibilidad y volatile
La palabra clave volatile garantiza que los cambios en una variable se vean inmediatamente desde otros hilos, sin almacenar en cachés locales. No da atomicidad; para operaciones compuestas (como contador++) se necesita sincronización o clases atómicas.
5. Comunicación entre hilos: wait, notify, notifyAll

Se usan dentro de bloques sincronizados para coordinar la ejecución:

    wait(): libera el monitor y espera notificación.

    notify(): despierta un hilo arbitrario que esté esperando en ese monitor.

    notifyAll(): despierta a todos los hilos en espera.

Ejemplo clásico productor-consumidor:
java

class Buffer {
    private int dato;
    private boolean lleno = false;

    public synchronized void poner(int valor) throws InterruptedException {
        while (lleno) wait();
        dato = valor;
        lleno = true;
        notifyAll();
    }

    public synchronized int obtener() throws InterruptedException {
        while (!lleno) wait();
        lleno = false;
        notifyAll();
        return dato;
    }
}

6. Clases atómicas (java.util.concurrent.atomic)

Proveen operaciones atómicas sin bloquear con synchronized. Ejemplos: AtomicInteger, AtomicLong, AtomicReference, LongAdder.
java

AtomicInteger contador = new AtomicInteger(0);
contador.incrementAndGet(); // atómico
contador.compareAndSet(valorEsperado, nuevoValor);

Son la base para contadores, generadores de secuencias y estructuras sin bloqueo.
7. Interbloqueos (deadlocks)

Situación donde dos o más hilos se bloquean mutuamente esperando recursos que el otro posee. Para evitarlos:

    Orden fijo en la adquisición de bloqueos.

    Usar tryLock() de java.util.concurrent.locks.Lock con tiempo de espera.

    Evitar bloqueos anidados innecesarios.

8. ThreadLocal

Permite que cada hilo tenga su propia copia de una variable.
java

ThreadLocal<SimpleDateFormat> formateador = ThreadLocal.withInitial(
    () -> new SimpleDateFormat("yyyy-MM-dd"));
// cada hilo obtiene su propia instancia segura

02-executors.md
1. Limitaciones de crear hilos manualmente

Crear un new Thread(...) cada vez es costoso y poco escalable. Los ejecutores abstraen la gestión de hilos, reutilizándolos y ofreciendo políticas de rechazo, planificación y resultados.
2. La interfaz Executor
java

public interface Executor {
    void execute(Runnable command);
}

Ejecuta tareas Runnable. La implementación decide el hilo en que se ejecuta.
3. ExecutorService – Ejecutores con ciclo de vida

Extiende Executor. Añade métodos para enviar tareas que devuelven valor (Callable), control de ciclo de vida (shutdown(), shutdownNow(), isShutdown(), awaitTermination()).
Creación mediante Executors (factory)

    Executors.newFixedThreadPool(n): pool con n hilos fijos. Útil para carga constante.

    Executors.newCachedThreadPool(): crea nuevos hilos bajo demanda, reutiliza los inactivos. Ideal para muchas tareas cortas y asíncronas.

    Executors.newSingleThreadExecutor(): un solo hilo; garantiza ejecución secuencial de tareas.

    Executors.newScheduledThreadPool(n): para tareas programadas o periódicas.

Tareas con resultado: Callable y Future
java

Callable<Integer> tarea = () -> {
    Thread.sleep(1000);
    return 42;
};
ExecutorService executor = Executors.newFixedThreadPool(2);
Future<Integer> futuro = executor.submit(tarea); // no bloquea

// Hacer otras cosas...
Integer resultado = futuro.get(); // bloquea hasta que esté listo
// .get(timeout, TimeUnit) para no esperar indefinidamente

Future permite cancelar (futuro.cancel(true)), comprobar estado (isDone(), isCancelled()).
Cierre del executor
java

executor.shutdown(); // no acepta más tareas, termina las pendientes
// executor.shutdownNow(); intenta interrumpir las tareas activas
executor.awaitTermination(10, TimeUnit.SECONDS);

4. ScheduledExecutorService

Permite programar tareas con retardo o a intervalos regulares.
java

ScheduledExecutorService sch = Executors.newScheduledThreadPool(1);
// ejecutar tras 5 segundos de retardo
sch.schedule(() -> System.out.println("Tarea retardada"), 5, TimeUnit.SECONDS);
// ejecutar cada 3 segundos (periodo fijo entre inicio de ejecuciones)
sch.scheduleAtFixedRate(() -> System.out.println("Cada 3 seg"),
                        0, 3, TimeUnit.SECONDS);

5. ForkJoinPool (Java 7+)

Pool especializado para tareas que se pueden dividir recursivamente (divide y vencerás). Utiliza el concepto de work-stealing. Ideal para algoritmos paralelos. Se usa mediante ForkJoinTask (subclases RecursiveAction y RecursiveTask<T>).

Normalmente no se instancia directamente; se accede al común con ForkJoinPool.commonPool(), usado por streams paralelos.
6. CompletableFuture (Java 8+)

Evolución de Future que permite composición asíncrona y programación reactiva sin bloquear.
java

CompletableFuture.supplyAsync(() -> "Hola")
        .thenApply(s -> s + " Mundo")
        .thenAccept(System.out::println); // imprime "Hola Mundo"

Métodos principales:

    supplyAsync(Supplier): ejecuta en un hilo del ForkJoinPool común (o se puede pasar un Executor).

    thenApply(Function): transforma el resultado.

    thenAccept(Consumer): consume el resultado.

    thenCompose(Function): aplana dos futuros encadenados.

    thenCombine(otherFuture, BiFunction): combina resultados de dos futuros.

    exceptionally(Function): manejo de errores.

    allOf(...) / anyOf(...): coordinar múltiples CompletableFutures.

Fomenta código no bloqueante, similar a las promesas de JavaScript.
Bloque 07 – Programación funcional y Stream API
01-lambdas.md
1. ¿Qué es una expresión lambda?

Una lambda es una función anónima que puede ser tratada como un valor. Se escribe:
text

(parámetros) -> cuerpo

Ejemplos:
java

// Sin parámetros
() -> System.out.println("Hola")

// Un parámetro sin tipo (puede omitir paréntesis)
s -> s.length()

// Varios parámetros con tipos
(int a, int b) -> a + b

// Bloque de código
(x, y) -> {
    int z = x + y;
    return z;
}

2. Contexto e inferencia de tipos

Las lambdas se utilizan donde se espera una interfaz funcional (interfaz con un solo método abstracto). El compilador deduce el tipo de los parámetros de la lambda a partir de dicha interfaz.
java

// Predicate<String> tiene el método abstracto boolean test(String s)
Predicate<String> noVacio = s -> !s.isEmpty();

// Consumer<String> tiene void accept(String s)
Consumer<String> imprimir = s -> System.out.println(s);

3. Características del target typing

La misma lambda puede ser compatible con diferentes interfaces funcionales si su firma coincide:
java

Comparable<String> c = s -> s.length(); // compareTo(String) retorna int
ToIntFunction<String> f = s -> s.length(); // applyAsInt(String) retorna int

4. Métodos de referencia (method references)

Atajos sintácticos cuando la lambda solo llama a un método existente:
Tipo	Sintaxis	Equivalente lambda
Método estático	Clase::metodoEstatico	(x) -> Clase.metodo(x)
Método de instancia (objeto específico)	objeto::metodo	(x) -> objeto.metodo(x)
Método de instancia (clase)	Clase::metodoInstancia	(obj, args) -> obj.metodo(args)
Constructor	Clase::new	() -> new Clase()
java

// Estático
IntFunction<String> f = String::valueOf;

// Instancia particular
String str = "hola";
Supplier<Integer> sup = str::length;

// Instancia (primer parámetro es el objeto)
BiPredicate<String, String> equals = String::equals;

// Constructor
Supplier<ArrayList<String>> creaLista = ArrayList::new;

5. Captura de variables (closures)

Una lambda puede usar variables del ámbito que la rodea, siempre que esas variables sean efectivamente finales (su valor no se modifica después de inicializarse).
java

String prefijo = "Señor: ";
List<String> nombres = List.of("Juan", "Ana");
nombres.forEach(n -> System.out.println(prefijo + n)); // prefijo efectivamente final

Esto incluye parámetros de métodos y variables locales. Las lambdas no introducen un nuevo ámbito de variable (no se puede redeclarar una variable local con el mismo nombre dentro de la lambda).
6. Comparación con clases anónimas

Las lambdas no generan una clase extra a nivel de bytecode (las implementa el compilador con invokedynamic), son más ligeras y legibles. Sin embargo, no permiten crear un nuevo estado (no puedes declarar campos). Si necesitas estado interno, usa una clase anónima.
02-interfaces-funcionales.md
1. Paquete java.util.function

Java 8 proporciona un conjunto de interfaces funcionales de propósito general. Se pueden agrupar por el número de parámetros y tipo de retorno.
2. Principales interfaces
Predicate<T>

Método abstracto: boolean test(T t). Sirve para evaluar una condición.

    Métodos por defecto: and(), or(), negate().

    isEqual(Object): predicado que compara con equals.

java

Predicate<Integer> esPar = n -> n % 2 == 0;
Predicate<Integer> positivo = n -> n > 0;
esPar.and(positivo).test(10); // true

Consumer<T>

Método abstracto: void accept(T t). Consume un valor sin retornar nada.

    Método por defecto: andThen(Consumer) para encadenar.

java

Consumer<String> saludo = s -> System.out.println("Hola " + s);
Consumer<String> mayus = s -> System.out.println(s.toUpperCase());
saludo.andThen(mayus).accept("Ana");

Function<T, R>

Método abstracto: R apply(T t). Transforma un valor de tipo T en R.

    Métodos por defecto: compose(Function before), andThen(Function after).

    identity(): función que devuelve su argumento sin cambios.

java

Function<String, Integer> longitud = s -> s.length();
Function<Integer, String> asteriscos = n -> "*".repeat(n);
String resultado = longitud.andThen(asteriscos).apply("abc"); // "***"

Supplier<T>

Método abstracto: T get(). No recibe argumentos; proporciona un valor. Útil para fábricas o generación perezosa.
java

Supplier<Double> aleatorio = () -> Math.random();

UnaryOperator<T> y BinaryOperator<T>

Son funciones especializadas donde entrada y salida son del mismo tipo.

    UnaryOperator<T> extiende Function<T, T>.

    BinaryOperator<T> extiende BiFunction<T, T, T>.

    Contienen métodos estáticos: minBy, maxBy (reciben comparador).

Interfaces con dos argumentos

    BiPredicate<T, U>: boolean test(T t, U u)

    BiConsumer<T, U>: void accept(T t, U u)

    BiFunction<T, U, R>: R apply(T t, U u)

3. Interfaces para tipos primitivos

Para evitar autoboxing se proveen versiones especializadas: IntPredicate, LongConsumer, DoubleFunction<R>, ToIntFunction<T>, etc. La nomenclatura sigue el patrón: TipoOperacion (por ejemplo, IntToDoubleFunction).
4. Uso de lambdas con estas interfaces

Las lambdas son la implementación directa de estos métodos abstractos. Al usar la API de streams, verás muchas de estas interfaces en acción.
03-stream-api.md
1. ¿Qué es un Stream?

Un Stream es una secuencia de elementos sobre la que se pueden aplicar operaciones de forma declarativa. No es una estructura de datos; no almacena elementos. Se obtiene a partir de una fuente (colección, array, archivo, etc.) y se define un pipeline de operaciones.
2. Creación de Streams
java

// De colección
List<String> lista = Arrays.asList("a", "b");
Stream<String> stream1 = lista.stream(); // secuencial
Stream<String> stream2 = lista.parallelStream(); // paralelo (usa ForkJoinPool común)

// De array
Stream<String> stream3 = Arrays.stream(new String[]{"x","y"});
Stream<Integer> stream4 = Stream.of(1, 2, 3);

// Generación
Stream<Double> aleatorios = Stream.generate(Math::random); // infinito
Stream<Integer> secuencia = Stream.iterate(0, n -> n + 1); // infinito
// Rango (desde IntStream, etc.)
IntStream.range(0, 10); // 0..9
IntStream.rangeClosed(1, 5); // 1..5

3. Operaciones intermedias (lazy)

Transforman el stream y devuelven un nuevo stream. No se ejecutan hasta que se invoca una operación terminal.
Operación	Descripción
filter(Predicate)	Filtra elementos según condición
map(Function)	Transforma cada elemento en otro
flatMap(Function)	Convierte cada elemento en un stream y los concatena (aplana)
distinct()	Elimina duplicados (según equals())
sorted() / sorted(Comparator)	Ordena
peek(Consumer)	Realiza una acción por cada elemento sin modificar el stream (útil para depurar)
limit(n)	Trunca a los primeros n elementos
skip(n)	Descarta los primeros n elementos
takeWhile(Predicate) (Java 9+)	Toma mientras se cumpla (ordenado)
dropWhile(Predicate) (Java 9+)	Descarta mientras se cumpla
4. Operaciones terminales (disparan el pipeline)
Operación	Descripción
forEach(Consumer)	Consume cada elemento (no recomendado en paralelo)
collect(Collector)	Agrupa elementos en una colección o resultado (muy potente)
toList() (Java 16+)	stream.toList() (inmutable)
count()	Número de elementos
reduce(identidad, acumulador)	Combina elementos en un solo resultado (suma, producto, etc.)
anyMatch(Predicate)	¿Algún elemento cumple?
allMatch(Predicate)	¿Todos cumplen?
noneMatch(Predicate)	¿Ninguno cumple?
findFirst()	Primer elemento (Optional)
findAny()	Cualquier elemento (útil en paralelo para rendimiento)
min(Comparator) / max(Comparator)	Mínimo / máximo

Un stream no puede reutilizarse después de ejecutar una operación terminal.
5. Reducción con reduce
java

List<Integer> numeros = List.of(1, 2, 3, 4);
int suma = numeros.stream().reduce(0, (a, b) -> a + b); // 0 + 1 + 2 + 3 + 4 = 10
Optional<Integer> max = numeros.stream().reduce(Integer::max);

6. Colección con Collectors

Collectors ofrece métodos estáticos para recolectar en listas, conjuntos, mapas, cadenas, etc.

    Collectors.toList(): mutable (ArrayList).

    Collectors.toSet(), toUnmodifiableList() (Java 10+).

    Collectors.joining(): concatena cadenas con o sin separador.

    Collectors.groupingBy(Function): agrupa en un Map<K, List<T>>.
    java

    Map<String, List<Persona>> porCiudad = personas.stream()
        .collect(Collectors.groupingBy(Persona::getCiudad));

    Collectors.partitioningBy(Predicate): particiona en Map<Boolean, List<T>>.

    Collectors.toMap(keyMapper, valueMapper): crea un mapa. Cuidado con claves duplicadas.

7. Parallel Streams

Con .parallelStream() las operaciones se ejecutan en múltiples hilos usando el ForkJoinPool común. Útil cuando las operaciones son costosas e independientes. No siempre es más rápido; mide antes.
java

lista.parallelStream().filter(...).map(...).collect(...)

Evita efectos secundarios y estados compartidos; los streams paralelos no garantizan orden si no se usa forEachOrdered.
8. Consideraciones finales

    Los streams son adecuados para procesamiento de datos en pipeline; no reemplazan a los bucles cuando hay lógica compleja o necesidad de modificar estado.

    Prefiere streams para código más legible y encadenado, pero no sacrifiques la claridad.

    Existen también streams especializados: IntStream, LongStream, DoubleStream con operaciones específicas como sum(), average(), summaryStatistics().

