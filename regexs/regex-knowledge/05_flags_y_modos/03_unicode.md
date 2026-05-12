# Unicode y Expresiones Regulares

## Definición

Originalmente, las regex trabajaban solo con el conjunto ASCII. Con la expansión global de la informática, el soporte Unicode se ha vuelto imprescindible. La flag **u** (Unicode) o configuraciones equivalentes activan la conciencia plena de caracteres multibyte, propiedades y categorías.

## ¿Qué cambia al activar el modo Unicode?

*   **Clases de caracteres:** `\w`, `\d`, `\s`, `\b` pasan a reconocer caracteres de cualquier alfabeto, no solo ASCII.
*   **Sensibilidad:** Case-insensitive (`i`) se vuelve sensible a las reglas de mayúsculas/minúsculas de Unicode (ej: 'ß' coincide con 'SS').
*   **Aserciones:** `\B` (límites de no palabra) se adapta de la misma forma.
*   **Propiedades:** Se habilitan las propiedades Unicode `\p{...}`; sin la flag `u`, muchos motores no reconocen estas secuencias.
*   **Metacarácter punto:** El punto `.` coincide con cualquier punto de código Unicode, no solo con bytes individuales.
*   **Rangos:** Las clases de caracteres invertidas y los rangos funcionan correctamente con puntos de código que exceden `\uFFFF`.
*   **Pares sustitutos:** En JavaScript, el modo `u` corrige el manejo de *surrogate pairs* para caracteres como emojis.

## Soporte por motor

| Motor | Activación | Comportamiento por defecto |
| :--- | :--- | :--- |
| **Python 3 (re)** | Unicode por defecto para `str`. Flag `re.ASCII` para forzar ASCII. | `\w` incluye letras Unicode, `\d` solo ASCII, `\s` incluye espacios Unicode. |
| **Python regex** | Por defecto Unicode. Flags `regex.U` y `regex.A`. | Soporte completo, incluyendo `\p{L}`. |
| **JavaScript** | Flag `u` (`/patrón/u`). | Sin `u`, trata la cadena como unidades UTF-16. Con `u`, por puntos de código. |
| **PCRE / PHP** | `(*UTF)` o `(?u)` o flag `u` (PHP). | En PCRE2, se controla por `PCRE2_UTF` y `PCRE2_UCP`. |
| **Java** | `Pattern.UNICODE_CHARACTER_CLASS` o `(?U)`. | Por defecto es ASCII; se debe activar explícitamente. |
| **.NET** | Unicode por defecto en todas las categorías. | `\w` y `\b` son plenamente compatibles con Unicode. |
| **Perl** | `/u` o `use feature 'unicode_strings'`. | Unicode por defecto en versiones modernas. |

## Propiedades Unicode: `\p{...}` y `\P{...}`

Permite seleccionar caracteres mediante sus propiedades definidas por el consorcio Unicode. Está disponible con la flag `u` (o en motores que lo soportan nativamente).

**Sintaxis:**
*   `\p{Property=Value}` (forma canónica)
*   `\p{Value}` (si es inequívoco)
*   `\P{...}` (negación)

### Principales categorías

*   **Letras (L):** `Lu` (Uppercase), `Ll` (Lowercase), `Lt` (Titlecase), `Lm` (Modifier), `Lo` (Other).
*   **Números (N):** `Nd` (Digit), `Nl` (Letter number), `No` (Other number).
*   **Símbolos (S):** `Sm` (Math), `Sc` (Currency), `Sk` (Modifier), `So` (Other).
*   **Puntuación (P):** `Pd` (Dash), `Ps` (Open), `Pe` (Close), etc.
*   **Separadores (Z):** `Zs` (Space), `Zl` (Line), `Zp` (Paragraph).
*   **Marcas (M):** `Mn` (Non-spacing), `Mc` (Spacing combining), `Me` (Enclosing).

### Ejemplos

```regex
\p{L}+        # una o más letras de cualquier alfabeto
\p{Nd}+       # dígitos decimales (incluye dígitos de otras escrituras)
\p{Sc}        # símbolo de moneda (£, ¥, €, $, etc.)
\p{Emoji}     # emojis (en motores compatibles)
```

> [!NOTE]
> También existen propiedades para **Scripts** (`\p{Script=Latin}`, `\p{Greek}`) y **Bloques** (`\p{Block=Basic_Latin}`).

## Uso en distintos motores

### Python (módulo `regex`)

```python
import regex
pat = regex.compile(r'\p{Lu}\p{Ll}+')  # palabra con inicial mayúscula
```

### JavaScript (ES2018+)

```javascript
let regex = /\p{Script=Greek}+/u;
"Σωκράτης".match(regex); // "Σωκράτης"
```

### PCRE/PHP

```php
preg_match('/\p{Han}/u', '漢字'); // 1
```

> [!IMPORTANT]
> En Python estándar (`re`), no se admiten `\p{}`, es necesario instalar y usar el módulo `regex` de PyPI.

## Detalles técnicos adicionales

### Límites de palabra (`\b`)
`\b` se define en función de `\w`. Con Unicode, `\b` reconoce transiciones entre caracteres de palabra Unicode y no palabra. Ejemplo: en `"Café au lait"`, `\bcafé\b` coincide correctamente.

### Case-Insensitive y Unicode
La flag `i` en modo Unicode utiliza las reglas de plegado de mayúsculas/minúsculas de Unicode. Por ejemplo, `/Straße/i` coincide con `"STRASSE"`.

### Puntos de código suplementarios (> U+FFFF)
JavaScript sin flag `u` trata caracteres como '𝄞' (U+1D11E) como dos unidades de código. Con `/u`, el motor trabaja a nivel de punto de código completo.

```javascript
/^.$/u.test('𝄞'); // true (un solo carácter)
/^.$/.test('𝄞');  // false (son dos unidades)
```

## Normalización Unicode

La misma cadena puede ser representada de diferentes formas (NFC, NFD). Las regex no normalizan automáticamente; es responsabilidad del programador normalizar el texto antes de compararlo.

> [!TIP]
> Se recomienda normalizar la entrada a **NFC** o **NFD** antes de aplicar la expresión regular mediante métodos como `text.normalize('NFC')` en JavaScript.

## Rendimiento

El modo Unicode puede ser ligeramente más lento por la gran cantidad de caracteres a considerar. Si solo trabajas con texto ASCII, usar flag `A` (en Python) o no activar `u` puede aportar pequeñas optimizaciones.

## Ejemplo completo: validación de nombre internacional

### En Python (módulo `regex`)

```python
import regex

pat = regex.compile(r'^\p{Lu}\p{Ll}*(?:[-\s]\p{Lu}\p{Ll}*)*$')
# Ej: "José", "María Cristina", "Jean-Luc"
print(pat.match("José Ángel"))   # match
```

### En JavaScript

```javascript
let nameRegex = /^\p{Lu}\p{Ll}*(?:[-\s]\p{Lu}\p{Ll}*)*$/u;
nameRegex.test("Jürgen Müller"); // true
```

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Modo Verboso](02_modo_verboso.md) | [🏠 Inicio](../../README.md) | [Resumen y Miscelánea ▶](aux.md) |

