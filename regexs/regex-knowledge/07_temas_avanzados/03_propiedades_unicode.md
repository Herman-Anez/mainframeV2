# Propiedades Unicode

Las propiedades Unicode permiten describir conjuntos de caracteres según sus atributos definidos en el estándar Unicode: categoría (letra, número, símbolo...), script (alfabeto), bloque (rango de códigos) y propiedades binarias (emoji, signo de puntuación, etc.). Esto posibilita la manipulación precisa de texto internacional, superando las limitaciones del `\w` ASCII tradicional.

> [!IMPORTANT]
> Están disponibles en **PCRE** (flag `u`), **JavaScript** (flag `u` desde ES2018), **Python** (con el módulo `regex`), **Java** y **.NET**. No están soportadas en el módulo `re` estándar de Python ni en **POSIX**.

## Sintaxis general

*   **`\p{Propiedad}`**: Carácter que posee esa propiedad.
*   **`\P{Propiedad}`**: Carácter que **NO** posee esa propiedad.
*   **Notación larga**: `\p{Categoría=Valor}`.
*   **Notación corta**: `\p{Valor}` (si no hay ambigüedad).

## Categorías generales (General Category)

Abreviatura de una letra:
*   **L**: Letra (Letter)
*   **M**: Marca (Mark)
*   **N**: Número (Number)
*   **P**: Puntuación (Punctuation)
*   **S**: Símbolo (Symbol)
*   **Z**: Separador (Separator)
*   **C**: Control / No asignado

Subdivisiones comunes (dos letras):
*   **Lu**: Letra mayúscula (Letter, uppercase)
*   **Ll**: Letra minúscula (Letter, lowercase)
*   **Lt**: Letra título (Letter, titlecase)
*   **Lm**: Letra modificadora
*   **Lo**: Letra, otra
*   **Nd**: Número decimal dígito (Number, decimal digit)
*   **Nl**: Número letra (como números romanos)
*   **No**: Número otro
*   **Pc**: Puntuación conectiva (`_`)
*   **Pd**: Guión
*   **Ps**: Apertura paréntesis
*   **Pe**: Cierre paréntesis
*   **Sc**: Símbolo moneda (`$`, `€`, `¥`...)
*   **Sk**: Símbolo modificador (`^`, `` ` ``, `¨`)
*   **Sm**: Símbolo matemático (`+`, `=`, `~`)
*   **Zs**: Espacio separador (espacio normal)
*   **Zl**: Separador de línea
*   **Zp**: Separador de párrafo

### Ejemplos de categorías
```regex
\p{Lu}           # Una mayúscula cualquiera (A, Á, Б, Ω...)
\p{Nd}+          # Dígitos decimales (0-9, ٠-٩, etc.)
\p{Sc}           # Cualquier símbolo monetario
\P{L}            # Cualquier carácter que NO sea una letra
```

## Scripts (Alfabetos)

Especifican un sistema de escritura específico:
*   `\p{Script=Latin}` o `\p{Latin}`
*   `\p{Greek}`, `\p{Cyrillic}`, `\p{Arabic}`
*   `\p{Han}` (caracteres chinos), `\p{Hiragana}`, etc.

```regex
\p{Script=Latin}+  # Palabra en alfabeto latino
\p{Han}+           # Secuencia de caracteres Han (chino, japonés)
```

## Bloques Unicode (Rangos)

Útiles para limitar a un rango de códigos concreto, aunque menos semánticos que el Script:
```regex
\p{Block=Basic_Latin}       # U+0000..U+007F
\p{Block=Latin_Supplement}  # U+0080..U+00FF
```

## Propiedades binarias

Características on/off:
*   **`\p{Emoji}`**: Caracteres emoji.
*   **`\p{Emoji_Presentation}`**: Emojis que se muestran con presentación gráfica por defecto.
*   **`\p{White_Space}`**: Espacio en blanco (más amplio que `\s` en algunos motores).
*   **`\p{Alphabetic}`**: Letra o carácter con propiedad alfabética.
*   **`\p{Lowercase}`, `\p{Uppercase}`**

## Uso en motores

### JavaScript (ES2018+)
Requiere siempre la flag `u`.
```javascript
let regex = /\p{Script=Greek}+/u;
regex.test('Σωκράτης'); // true
```

### Python (módulo `regex`)
```python
import regex
regex.findall(r'\p{Lu}\p{Ll}+', 'José Ángel')  # ['José', 'Ángel']
```

### PCRE/PHP
```php
preg_match('/\p{Hiragana}+/u', 'こんにちは'); // 1
```

### Java
Soporta `\p{Is...}`, por ejemplo `\p{IsLatin}` para script, o `\p{Lu}` para categoría.

## Normalización Unicode y su impacto

> [!WARNING]
> Un mismo carácter puede representarse de múltiples formas (ej. `ñ` = `U+00F1` (NFC) o `U+006E` + `U+0303` (NFD)). Las regex **no normalizan automáticamente**.
>
> Por ejemplo, `\p{Ll}` casaría con `ñ` precompuesto pero no con la secuencia `n` + `tilde combinante` (porque la `n` es `Ll` pero la tilde es una marca `M`). Se recomienda normalizar el texto antes de procesarlo (ej. `text.normalize('NFC')` en JS).

## Coincidencia de mayúsculas/minúsculas

Con la flag `i` (case-insensitive) y Unicode activado, algunas implementaciones permiten que `/ß/i` coincida con `SS`. Esto depende del **case folding** del motor. Las propiedades como `\p{Lowercase}` no se ven afectadas por la flag `i`.

## Ejemplos prácticos

1.  **Detectar texto con al menos una mayúscula griega:**
    ```regex
    \p{Script=Greek}*\p{Lu}\p{Script=Greek}*
    ```
2.  **Extraer emojis de un mensaje:**
    ```regex
    \p{Emoji_Presentation}
    ```
3.  **Validar nombre de usuario (letras, números, guiones y guiones bajos de cualquier alfabeto):**
    ```regex
    ^[\p{L}\p{N}_-]+$
    ```
4.  **Tokenizar palabras multilingües (secuencias de letras):**
    ```regex
    \p{L}+
    ```

## Limitaciones y buenas prácticas

> [!NOTE]
> *   **Longitud:** Las propiedades Unicode pueden alargar el patrón; usa modo verboso para documentar.
> *   **Soporte:** No todos los motores soportan todas las propiedades (especialmente las binarias).
> *   **Python:** El módulo estándar `re` no soporta estas propiedades; usa el módulo `regex`.
> *   **Responsabilidad:** La normalización del texto es responsabilidad del desarrollador.

---

### 📖 Temas relacionados
| Archivo | Descripción |
| :--- | :--- |
| [01_recursion_y_subrutinas.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/07_temas_avanzados/01_recursion_y_subrutinas.md) | Patrones recursivos |
| [05_optimizacion.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/07_temas_avanzados/05_optimizacion.md) | Mejora de rendimiento |
| [06_motores_y_dialectos](../06_motores_y_dialectos/01_comparativa_general.md) | Soporte por motor |


---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Condicionales](02_condicionales.md) | [🏠 Inicio](../../README.md) | [Backtracking Catastrofico ▶](04_backtracking_catastrofico.md) |
