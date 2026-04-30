# TIPOS DE DATOS Y VARIABLES
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

