
# Sintaxis Básica

Java es un lenguaje fuertemente tipado y orientado a objetos. Su sintaxis es clara pero requiere seguir ciertas estructuras fundamentales para que el compilador y la JVM puedan ejecutar el código correctamente.

---

## El esqueleto de todo programa Java

Tradicionalmente, un programa Java se compone de al menos una clase y un método `main` con la firma exacta:

```java
public class MiApp {
    public static void main(String[] args) {
        System.out.println("Hola Java");
    }
}
```

- **`public class MiApp`**: La clase debe llamarse igual que el archivo (`MiApp.java`). La visibilidad `public` permite que la JVM la encuentre.
- **`public static void main(String[] args)`**: Punto de entrada. `static` permite invocarlo sin crear una instancia.
- **`System.out.println()`**: Salida estándar para imprimir texto en la consola.

---

## Java 21 (Preview): Simplified Main Method

Para scripts, prototipos y ejemplos didácticos, Java 21 (en modo preview) permite una sintaxis mucho más ligera, incluso sin clase explícita ni `static`:

```java
void main() {
    println("Hola directamente desde una unnamed class");
}
```

También se permite el uso de argumentos si se desea acceder a ellos:
```java
void main(String[] args) { ... }
```

> [!NOTE]
> Esta característica requiere compilar con `--enable-preview --source 21`. Elimina la necesidad de escribir `public class` y `System.out`, ya que `println` se hereda de `java.io.IO` y la JVM genera una clase anónima por nosotros.

---

## Paquetes e imports

- **Paquete (`package`)**: `package com.empresa.proyecto;` debe ser la primera línea no comentada del archivo.
- **Importaciones (`import`)**: `import java.util.List;`, `import static java.lang.Math.*;`.

> [!TIP]
> El paquete `java.lang` se importa automáticamente en todos los archivos Java.

---

## Comentarios

Java soporta tres tipos de comentarios:

- **Línea única**: `// comentario`
- **Bloque**: `/* ... */`
- **Javadoc**: `/** ... */` (utilizado para generar documentación técnica).

---

## Identificadores y convenciones

Los identificadores deben comenzar con letra, `_` o `$`. No pueden ser palabras reservadas del lenguaje.

### Convenciones recomendadas
Para mantener un código limpio y profesional, se siguen estas reglas de nomenclatura:

- **Clases e Interfaces**: `PascalCase` (ej: `MiServicio`).
- **Métodos y variables**: `camelCase` (ej: `calcularTotal`).
- **Constantes (`static final`)**: `MAYÚSCULAS_CON_GUIONES` (ej: `VALOR_MAXIMO`).
- **Paquetes**: En minúsculas, siguiendo la notación inversa de dominio (ej: `com.google.util`).

---

## Bloques de código y ámbito

Cada par de llaves `{}` define un bloque. Las variables declaradas dentro de un bloque viven únicamente en ese ámbito (*scope*), incluyendo parámetros de métodos y variables de control de bucles.
