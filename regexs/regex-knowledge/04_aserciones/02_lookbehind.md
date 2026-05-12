# Lookbehind (Inspección hacia atrás)

## Definición

Un **lookbehind** (inspección hacia atrás) comprueba si una subexpresión coincide inmediatamente antes de la posición actual. Tampoco consume caracteres.

*   **Lookbehind positivo:** `(?<= … )` → la posición está precedida por el patrón.
*   **Lookbehind negativo:** `(?<! … )` → la posición NO está precedida por el patrón.

> [!NOTE]
> El cursor está en la posición de interés; el motor “mira hacia atrás” para ver si se cumple la condición. La longitud del texto inspeccionado no se incluye en el match.

## Limitaciones históricas y actuales

La implementación del lookbehind es la parte más heterogénea entre motores:

| Motor | Longitud fija / variable | Observaciones |
| :--- | :--- | :--- |
| **Perl 5.30+** | Variable (experimental) | Antes solo fija. |
| **PCRE2 (PHP >=7.3)** | Variable (con restricciones) | Debe poder determinar una longitud máxima (no permite `*` o `+` sin límite superior). Alternativamente se puede usar `\K`. |
| **PCRE / Perl antiguo** | Sólo fija | Patrón debe tener longitud exacta (ej: `(?<=abc|def)` ambas opciones deben misma longitud). |
| **JavaScript (ES2018+)** | Variable | Sin restricciones de longitud. |
| **Python re (estándar)** | Sólo fija | Sin cuantificadores variables; cada alternativa debe tener la misma longitud. |
| **Python regex (ext)** | Variable | Soporte completo. |
| **Java** | Longitud máx. limitada | Se permiten cuantificadores con límite superior finito: `{0,n}`. `*` y `+` no permitidos a menos que tengan un máximo explícito. |
| **.NET** | Variable | Sin restricciones. Soporta incluso patrones complejos sin límite. |

> [!IMPORTANT]
> Cuando un motor exige longitud fija, el patrón dentro del lookbehind no puede contener `*`, `+`, `?` ni `{n,}`. Solo puede tener literales, clases de caracteres, grupos y alternancias con todas las ramas de igual longitud.

### Ejemplos de validez (Python `re`)

```regex
(?<=abc|def)X
# ✅ Válido: Ambas opciones tienen longitud 3.

(?<=a+)X
# ❌ Error: look-behind requiere patrón de ancho fijo.
```

## Lookbehind positivo: `(?<=patrón)`

Coincide en una posición si justo antes se encuentra `patrón`.

### Casos de uso

*   **Extraer un valor precedido por un prefijo:** `(?<=\$)\d+\.\d{2}` captura números decimales después de un dólar, sin incluir el signo `$`.
*   **Asegurar un contexto previo:** `(?<=@)\w+` extrae el nombre de usuario en un correo electrónico después de la `@`.
*   **Evitar capturar el delimitador:** en `(?<=\/)\w+` para obtener la última parte de una URL.

## Lookbehind negativo: `(?<!patrón)`

Coincide si la posición **NO** está precedida por `patrón`.

### Uso típico: cadenas entre comillas escapadas

```regex
(?<!\\)".*?"
```

> [!TIP]
> Encuentra comillas dobles que no están precedidas por una barra invertida. Si una comilla va precedida de `\`, el lookbehind negativo falla, evitando que se tome como delimitador.

## Anclas dentro de lookbehind

`^` y `$` dentro de un lookbehind no tienen un significado global; se refieren a la posición relativa a la actual.

> [!WARNING]
> En general, no se usan porque no tienen sentido: `^` dentro de un lookbehind positivo `(?<=^)` significaría "la posición actual es justo después del inicio de la cadena", lo cual es equivalente a `\A` o similar. Es más claro usar anclas normales.

## Soporte en reemplazos

A veces se usan lookbehinds para reemplazar patrones que están precedidos por algo, sin eliminar ese prefijo.

**Ejemplo en Python:**

```python
import re
text = "Price $100, discount $20"
re.sub(r'(?<=\$)\d+', 'XXX', text)
# Resultado: "Price $XXX, discount $XXX"
```

## Alternativa con `\K`

En PCRE y Perl (y en el módulo `regex` de Python), `\K` descarta lo coincidido hasta ese punto, logrando un efecto similar a lookbehind positivo de longitud variable.

```regex
\$\K\d+
```

> [!NOTE]
> Equivale a `(?<=\$)\d+` pero es mucho más eficiente y sin restricciones de longitud fija. Tras `\K`, la parte izquierda no forma parte del match.

## Simulación y workarounds en motores limitados

Si tu motor no soporta lookbehind (por ej. JavaScript antiguo), puedes:

1.  **Invertir la cadena** y aplicar lookahead.
2.  **Capturar la parte previa** y luego usar código para descartarla.
3.  **En validaciones**, usar `(?:patrón_previo)(lo_que_quiero)` y luego comprobar el grupo capturado.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Lookahead](01_lookahead.md) | [🏠 Inicio](../../README.md) | [Ejemplos de Validación ▶](03_ejemplos_validacion.md) |

