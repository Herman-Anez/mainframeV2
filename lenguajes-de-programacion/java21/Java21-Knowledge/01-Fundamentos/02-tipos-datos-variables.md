# Tipos de Datos y Variables

Java es un lenguaje de tipado estático, lo que significa que cada variable debe tener un tipo definido en tiempo de compilación. Los datos se dividen principalmente en tipos primitivos y tipos de referencia.

---

## Tipos primitivos

Java posee 8 tipos primitivos que no son objetos y se almacenan directamente en la pila (*stack*).

| Tipo | Tamaño | Rango | Ejemplo literal |
| :--- | :--- | :--- | :--- |
| **byte** | 8 bits | -128 a 127 | `byte b = 100;` |
| **short** | 16 bits | -32,768 a 32,767 | `short s = 20_000;` |
| **int** | 32 bits | -2³¹ a 2³¹-1 (~ ±2 mil millones) | `int i = 5_000_000;` |
| **long** | 64 bits | -2⁶³ a 2⁶³-1 | `long l = 123L;` |
| **float** | 32 bits | Precisión simple IEEE 754 | `float f = 3.14f;` |
| **double** | 64 bits | Precisión doble IEEE 754 | `double d = 3.14;` |
| **char** | 16 bits | 0 a 65,535 (Unicode) | `char c = 'A';` |
| **boolean**| 1 bit* | `true` o `false` | `boolean flag = true;` |

> [!NOTE]
> *En la práctica, el tamaño del tipo `boolean` depende de la JVM, pero solo puede almacenar los valores `true` y `false`.

> [!TIP]
> Desde Java 7 se pueden usar guiones bajos en literales numéricos para mejorar la legibilidad: `1_000_000`. También se soportan literales binarios (`0b1010`) y hexadecimales (`0x1A`).

---

## Tipos de referencia

Todo lo que no es un tipo primitivo es una referencia a un objeto almacenado en el *heap*. Esto incluye:

- **Clases**: `String`, `Integer`, `ArrayList`, etc.
- **Interfaces**: `List`, `Runnable`, etc.
- **Enumeraciones**: `enum`.
- **Arrays**: Tanto de primitivos como de objetos.
- **Registros**: Clases especiales como `record`.

> [!IMPORTANT]
> El valor por defecto de cualquier tipo de referencia es `null`.

---

## La clase String y Text Blocks

`String` es una clase inmutable en Java. Se puede crear con comillas dobles estándar o mediante **Text Blocks** (disponibles desde Java 15).

### Text Blocks
Permiten escribir cadenas multilínea de forma limpia:

```java
String json = """
    {
        "nombre": "Juan",
        "edad": 25
    }
    """;
```

Los bloques de texto conservan los saltos de línea y permiten una indentación controlada mediante el método `stripIndent()` (llamado implícitamente).

### String Templates (Preview en Java 21)
Java 21 introduce la interpolación de valores de forma segura:

```java
String nombre = "Ana";
String mensaje = STR."¡Hola \{nombre}!";
```

`STR` es el procesador de plantillas estándar. Este mecanismo es robusto y protege contra ataques de inyección.

---

## Inferencia de tipos con `var` (desde Java 10)

Es posible declarar variables locales sin especificar explícitamente el tipo, siempre que se inicialicen.

```java
var lista = new ArrayList<String>();    // El tipo se infiere como ArrayList<String>
var numero = 42;                        // El tipo se infiere como int
var saludo = "Hola";                    // El tipo se infiere como String
```

- El tipo se infiere en **tiempo de compilación**.
- **No** se puede usar `var` sin inicializador ni como parámetro de método (salvo en lambdas con tipos implícitos).

---

## Variables: ámbito, inicialización y final

- **Variables locales**: Deben inicializarse obligatoriamente antes de usarse. Ámbito restringido al bloque.
- **Variables de instancia**: Campos no estáticos. Se inicializan automáticamente con valores por defecto (`0`, `false`, `null`).
- **Variables estáticas**: Campos `static`. Se inicializan igual que las de instancia.

### Constantes
La palabra clave `final` indica que la variable no puede ser reasignada.
- Para constantes de clase se usa `static final`.
- Una referencia `final` impide que la variable apunte a otro objeto, pero **no impide** modificar el estado interno del objeto referenciado (excepto si es inmutable como `String` o `record`).

---

## Conversión de tipos (Casting)

- **Implícita (Widening)**: De menor a mayor tamaño (ej: `int` → `long` → `float` → `double`). Es siempre seguro.
- **Explícita (Narrowing)**: Requiere casting y puede resultar en pérdida de precisión o de bits.

```java
double d = 3.14;
int i = (int) d;  // El valor de i será 3
```

> [!NOTE]
> **Promoción automática:** En expresiones aritméticas, todos los `byte`, `short` y `char` se promueven automáticamente a `int` al evaluar operadores.

