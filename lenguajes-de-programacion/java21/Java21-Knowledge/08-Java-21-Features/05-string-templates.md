# STRING TEMPLATES (PREVIEW)

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

