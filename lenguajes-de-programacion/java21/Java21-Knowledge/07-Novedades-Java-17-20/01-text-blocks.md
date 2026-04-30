# 📝 Text Blocks

Los **Text Blocks** (bloques de texto) facilitan la escritura de cadenas literales que ocupan varias líneas sin necesidad de concatenaciones, escapes engorrosos ni saltos de línea explícitos. Esta característica fue previsualizada en Java 13-14 y se convirtió en estándar definitivo en Java 15, por lo que en Java 17/21 está completamente estable.

---

## 🏗️ Sintaxis básica

Se delimitan con tres comillas dobles `"""` de apertura y cierre:

```java
String html = """
    <html>
        <body>
            <p>Hola, mundo</p>
        </body>
    </html>
    """;
```

---

## 📏 Manejo de la indentación

El compilador elimina la indentación incidental automáticamente:

*   Se toma como referencia el número de espacios en blanco comunes a todas las líneas (incluyendo las líneas vacías se consideran como infinitos espacios para el cálculo).
*   Los espacios sobrantes se eliminan mediante `String::stripIndent`.
*   La posición de la triple comilla de cierre controla la indentación adicional: si se coloca en una línea separada con una determinada sangría, esa sangría se suma a la referencia común.

> [!IMPORTANT]
> Si no se quiere que todo el bloque esté pegado a la izquierda, se coloca la triple comilla de cierre a la altura deseada.

**Ejemplo:**

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

---

## 🔓 Escapes dentro de text blocks

Los caracteres especiales siguen necesitando escape: `\"` para comillas dobles, `\\` para barra invertida. Pero no es necesario escapar las comillas dobles individuales, solo secuencias de tres comillas (`\"""`).

Además, Java 14 introdujo dos escapes nuevos pensados para text blocks:

*   `\` (barra invertida al final de línea): Suprime el salto de línea (continuación de línea). Útil para escribir líneas muy largas sin interrumpir la cadena visualmente.
*   `\s` (barra invertida seguida de s): Espacio explícito. Evita que el algoritmo de indentación elimine espacios en blanco finales. Muy útil para forzar un espacio antes de un salto de línea o para preservar espacios finales.

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

---

## 🛠️ Métodos útiles

*   `String::stripIndent()`: Elimina la indentación común (se llama implícitamente en el text block).
*   `String::translateEscapes()`: Interpreta secuencias de escape como `\n`, `\t` dentro de una cadena (ya aplicadas en tiempo de compilación en text blocks).
*   `String::formatted(Object... args)`: Equivalente a `String.format`, pero como método de instancia (Java 15+). Muy útil con text blocks:

```java
String saludo = """
    Hola %s,
    Bienvenido a %s.
    """.formatted(nombre, aplicacion);
```

---

## 🧪 Text blocks y String Templates (Java 21 Preview)

Con los **String Templates** (preview en Java 21) los text blocks se vuelven aún más expresivos:

```java
String nombre = "Ana";
String mensaje = STR."""
    Hola \{nombre},
    Esto es una interpolación.
    """;
```

---

## 💡 Buenas prácticas

> [!TIP]
> *   Usar text blocks para JSON, XML, SQL, HTML, etc.
> *   Colocar la triple comilla de cierre en su propia línea para controlar el sangrado.
> *   Utilizar `\` para mantener la legibilidad de consultas largas sin saltos de línea no deseados.
> *   Recordar que todos los espacios en blanco son significativos. Cuidado con líneas que parecen vacías pero contienen espacios.

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../README.md)
- [☕ Java 21 Index](../../index.md)

