# MANEJO DE EXCEPCIONES

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
