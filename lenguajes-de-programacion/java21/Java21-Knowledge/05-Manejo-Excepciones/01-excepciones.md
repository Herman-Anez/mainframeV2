# Manejo de Excepciones

El manejo de excepciones en Java es un mecanismo robusto para controlar situaciones anómalas en tiempo de ejecución. Java 21 mantiene el modelo consolidado, con mejoras de calidad de vida que facilitan la depuración y gestión de recursos.

---

## 1. Jerarquía de excepciones

Todas las excepciones y errores heredan de la clase `java.lang.Throwable`. De ella derivan dos ramas principales:

### Error

Representan problemas graves de la JVM (ej. `OutOfMemoryError`, `StackOverflowError`). Normalmente la aplicación no debe intentar capturarlos.

### Exception

Condiciones que la aplicación puede capturar y manejar:

- **Excepciones comprobadas (Checked):** Hijas de `Exception` (excepto `RuntimeException`). El compilador obliga a manejarlas o declararlas con `throws`. Ej: `IOException`.
- **Excepciones no comprobadas (Unchecked):** Hijas de `RuntimeException`. Indican errores de programación. No es obligatorio capturarlas. Ej: `NullPointerException`.

```text
Throwable
├── Error (Irrecuperables)
└── Exception
    ├── Checked Exceptions (IOException, SQLException...)
    └── RuntimeException (NullPointerException, IllegalArgumentException...)
```

---

## 2. Captura de excepciones: try-catch-finally

### 2.1. Bloques try-catch

Permite capturar excepciones específicas. El orden de los bloques `catch` importa: debe ir de la excepción más específica a la más genérica.

```java
try {
    Files.readAllLines(Path.of("archivo.txt"));
} catch (IOException e) {
    System.err.println("Error de E/S: " + e.getMessage());
} catch (Exception e) {
    System.err.println("Error inesperado: " + e);
}
```

### 2.2. Multi-catch (Java 7+)

Permite capturar varios tipos de excepción en un solo bloque si el manejo es idéntico.

```java
try {
    // ...
} catch (IOException | SQLException e) {
    System.err.println("Error de datos: " + e.getMessage());
}
```

### 2.3. Bloque finally

Se ejecuta **siempre**, haya o no excepción, incluso después de un `return`. Ideal para tareas de limpieza manual.

---

## 3. Try-with-resources (Java 7+)

Gestiona automáticamente el cierre de recursos que implementan `AutoCloseable` (streams, conexiones, etc.).

```java
try (BufferedReader br = new BufferedReader(new FileReader("archivo.txt"))) {
    String linea = br.readLine();
} // br.close() se llama automáticamente aquí
```

> [!TIP]
> Desde Java 9, puedes pasar al bloque `try` variables que ya hayan sido declaradas, siempre que sean **efectivamente finales**.

---

## 4. Declaración de excepciones: throws

Si un método no maneja una excepción comprobada, debe delegarla a quien lo invoque mediante la palabra clave `throws`.

```java
public String leerArchivo(String ruta) throws IOException {
    return Files.readString(Path.of(ruta));
}
```

> [!NOTE]
> Al sobrescribir un método, no puedes declarar excepciones comprobadas más generales o nuevas que las del método original.

---

## 5. Creación de excepciones propias

Puedes crear tus propias excepciones extendiendo `Exception` o `RuntimeException`.

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

---

## 6. Buenas prácticas

 **Captura específica:** evitar catch (Exception e) genérico salvo en puntos de entrada (p.ej., un main o un hilo raíz). Capturar lo que realmente se puede manejar.

 **No tragar excepciones:** nunca dejar un bloque catch vacío. Al menos registrar el error.

 **Envolver excepciones:** si se quiere añadir contexto, usar excepción personalizada o new RuntimeException(mensaje, e) para mantener la causa original.

- *Usar finally o try-with-resources para liberar recursos, incluso si no hay excepción.

- *Documentar con @throws en Javadoc todas las excepciones comprobadas y las no comprobadas relevantes.

 **En streams/lambdas:** las interfaces funcionales no permiten lanzar excepciones comprobadas directamente. Soluciones:

        Capturar dentro y convertir a unchecked.

        Usar bibliotecas como vavr o crear interfaces funcionales propias que permitan lanzar.

 **Optional evita el uso de null y reduce la necesidad de NullPointerException, pero no reemplaza el manejo de excepciones para casos de error irrecuperables.

- **Captura específica:** Evita `catch (Exception e)` si puedes capturar excepciones más concretas.
- **No silencies excepciones:** Nunca dejes un bloque `catch` vacío. Al menos registra el error en un log.
- **Mantén la causa:** Al relanzar una excepción, pasa la excepción original al constructor para no perder el stack trace (`new RuntimeException(msg, e)`).
- **Try-with-resources:** Es preferible a cerrar recursos manualmente en un bloque `finally`.

---

## 7. Mensajes de NPE mejorados (Java 14+)

Desde Java 14, la JVM proporciona mensajes de `NullPointerException` mucho más detallados, indicando exactamente qué variable o método devolvió `null`.

```java
a.b.c = 5; 
// Mensaje: "Cannot read field 'c' because 'a.b' is null"
```

---

[Anterior](../04-Programacion-Funcional/03-method-references.md) | [Siguiente](../06-Modulos-JPMS/01-modulos.md)
