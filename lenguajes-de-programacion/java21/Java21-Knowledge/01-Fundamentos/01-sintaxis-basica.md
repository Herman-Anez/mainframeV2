
# SINTAXIS BÁSICA
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
