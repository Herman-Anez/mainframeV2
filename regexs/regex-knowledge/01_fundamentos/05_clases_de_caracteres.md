# 📁 Fundamentos: Clases de Caracteres

## 📌 Definición

Una **clase de caracteres** es una construcción entre corchetes `[...]` que define un conjunto de caracteres. Coincide con un único carácter que pertenezca a ese conjunto.

## 📌 Sintaxis básica

```regex
[abc]  → a, b o c
[a-z]  → cualquier letra minúscula del alfabeto inglés
[0-9]  → cualquier dígito
[A-Za-z] → cualquier letra
```

Se pueden combinar múltiples rangos y caracteres sueltos:

```regex
[a-zA-Z0-9_] → carácter de palabra inglés (igual que \w)
```

## 📌 Carácter especial dentro de corchetes

### 🔹 `-` (guion)

- Si se coloca entre dos caracteres que pueden formar un rango según el orden de la tabla ASCII/Unicode, define un **rango**.
- Para tratarlo como **literal** debe ir al principio, al final, justo después de `^` (en clase negada) o escapado `\-`.

> [!WARNING]
> Ejemplo de rango inverso no permitido: `[z-a]` no es válido. En algunos motores es ignorado o genera un error.

### 🔹 `^` (circunflejo)

Si se escribe inmediatamente después del corchete de apertura, **niega** la clase: `[^...]` coincide con cualquier carácter que NO esté en la lista.

```regex
[^aeiou] → cualquier carácter que no sea vocal minúscula.
```

> [!NOTE]
> Si `^` aparece en otra posición (no al inicio), se trata como un literal `^`.

### 🔹 `]` (corchete de cierre)

El corchete de cierre debe escaparse `\]` o colocarse como primer carácter de la clase (después de `^` si la hay) para que se tome como literal.

```regex
[]]   → clase que contiene ']' (válido: ']' como primer carácter).
[]abc] → ']', 'a', 'b', 'c'.
[^]]  → cualquier carácter excepto ']'.
```

### 🔹 `\` (barra invertida)

La barra invertida mantiene su función de escape, por lo que `\d`, `\w`, `\s` y cualquier escape funcionan dentro de corchetes. `\\` es la barra literal.

## 📌 Clases predefinidas (shorthands)

Estas secuencias se pueden usar dentro o fuera de corchetes y representan clases comunes.

| Secuencia | Equivalencia ASCII | Significado |
| :--- | :--- | :--- |
| `\d` | `[0-9]` | Dígito |
| `\D` | `[^0-9]` | No dígito |
| `\w` | `[a-zA-Z0-9_]` | Carácter de palabra |
| `\W` | `[^a-zA-Z0-9_]` | No palabra |
| `\s` | `[ \t\n\r\f\v]` | Espacio en blanco |
| `\S` | `[^ \t\n\r\f\v]` | No espacio |
| `\h` | `[ \t]` | Espacio horizontal |
| `\v` | `[\n\r]` | Espacio vertical (varía según motor) |
| `\R` | `\r\n\|\n\|\r` | Salto de línea universal |

> [!IMPORTANT]
> Con el flag unicode activado, `\w`, `\d`, etc. pueden ampliarse para incluir letras y dígitos de otros alfabetos (ñ, ü, cirílicos, etc.).

## 📌 Clases POSIX

Son clases nombradas, encerradas entre dobles corchetes y dos puntos. Aparecen en motores como PCRE, Perl, Python (módulo regex) y algunos sabores de Unix.

```regex
[[:alnum:]]  → [a-zA-Z0-9]
[[:alpha:]]  → letras
[[:digit:]]  → [0-9]
[[:upper:]]  → mayúsculas
[[:lower:]]  → minúsculas
[[:punct:]]  → signos de puntuación
[[:space:]]  → espacios (incluye \n, \t)
[[:xdigit:]] → dígitos hexadecimales
```

> [!TIP]
> Estas clases se pueden combinar en una misma clase: `[[:upper:][:digit:]]`.

## 📌 Propiedades Unicode (`\p{...}`)

Con soporte unicode (flag `u` en JS, por defecto en Python 3), podemos usar propiedades generales o específicas.

| Propiedad | Significado |
| :--- | :--- |
| `\p{L}` | Cualquier letra (Letter) |
| `\p{Ll}` | Letra minúscula (lowercase) |
| `\p{Lu}` | Letra mayúscula |
| `\p{N}` | Cualquier número (Number) |
| `\p{Nd}` | Dígito decimal |
| `\p{P}` | Puntuación |
| `\p{S}` | Símbolo |
| `\p{Sc}` | Símbolo de moneda |
| `\p{Han}` | Caracteres Han |
| `\p{Greek}` | Letras griegas |

> [!NOTE]
> La negación se hace con `\P{...}` (P mayúscula). Ejemplo: `\P{L}` (no letra).

## 📌 Clases avanzadas: sustracción e intersección

Soportado en motores como .NET, Java y el módulo `regex` de Python.

- **Intersección:** `[a-z&&[^aeiou]]` en Java (consonantes).
- **Sustracción:** `[a-z-[aeiou]]` en .NET o `[a-z--[aeiou]]` en Python `regex`.

## 📌 Cuidados con rangos

Un rango como `[A-z]` incluye caracteres entre 'A' (65) y 'z' (122), que en ASCII contiene `[`, `\`, `]`, `^`, `_`, `` ` ``.

> [!TIP]
> Es mejor usar `[A-Za-z]` para evitar caracteres intermedios no deseados. Los rangos dependen del orden numérico de los puntos de código, no del alfabeto humano.

## 📌 Uso de clases en expresiones

Las clases siempre casan **un solo carácter**. Para múltiples caracteres debemos usar cuantificadores: `[0-9]+` para uno o más dígitos.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Anclas y Límites](04_anclas_y_limites.md) | [Índice](../README.md) | ➖ |
