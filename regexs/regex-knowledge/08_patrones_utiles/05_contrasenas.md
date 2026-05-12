# Validación de Contraseñas con Regex

## Requisitos típicos de una contraseña segura

Una política de contraseñas robusta suele exigir el cumplimiento de varias condiciones simultáneamente:

*   **Longitud mínima**: Generalmente 8 o más caracteres.
*   **Letras Mayúsculas**: Al menos una letra mayúscula.
*   **Letras Minúsculas**: Al menos una letra minúscula.
*   **Dígitos**: Al menos un dígito.
*   **Caracteres Especiales**: Al menos un carácter especial (símbolos como `!@#$%^&*`).

Estos requisitos se expresan elegantemente con *lookaheads* al inicio del patrón.

## Patrón estándar con lookaheads

```regex
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]|\p{P}|_?).{8,}$
```

Cada *lookahead* verifica la presencia de una categoría en cualquier parte de la cadena. Después, `.{8,}` consume toda la contraseña.

### Versión explícita y legible (desglosada)

```regex
^
  (?=.*[a-z])        # al menos una minúscula
  (?=.*[A-Z])        # al menos una mayúscula
  (?=.*\d)           # al menos un dígito
  (?=.*[#?!@$%^&*-]) # al menos un carácter especial de una lista concreta
  .{8,}              # longitud mínima 8
$
```

> [!NOTE]
> **Nota sobre caracteres especiales**: En lugar de `[^\w\s]`, es mejor definir explícitamente el conjunto permitido para evitar caracteres no imprimibles. Por ejemplo: `[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]` o una lista acotada.

## Longitud mínima y máxima

```regex
^.{8,32}$
```

Combinado con los *lookaheads* para restringir composición.

## Prohibir caracteres repetidos o secuencias

*   **No permitir 3 o más caracteres idénticos seguidos**: `(?!.*(.)\1{2,})`
*   **No permitir secuencias de teclado como "qwerty"**: difícil con regex pura, mejor verificar con código.

## Contraseñas que excluyen ciertos patrones (por ejemplo, el nombre de usuario)

Si se tiene el nombre de usuario, se puede construir la regex dinámicamente para rechazarlo. Por ejemplo, en JavaScript:

```javascript
let user = "john";
let passRegex = new RegExp(`^(?!.*${user})(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).{8,}$`, 'i');
```

El *lookahead* negativo `(?!.*${user})` prohíbe la aparición del nombre de usuario en cualquier parte de la contraseña.

## Sin necesidad de lookaheads (motores limitados)

Si el motor no soporta *lookaheads* (como **POSIX**), no se pueden hacer estas comprobaciones en una sola regex. Se usarían varias comprobaciones secuenciales:

```bash
grep -E '.{8,}' fichero | grep -E '[a-z]' | grep -E '[A-Z]' | grep -E '[0-9]' | grep -E '[^a-zA-Z0-9]'
```

## Exigir que al menos N de M condiciones se cumplan

Para requerir, por ejemplo, al menos 3 de 4 categorías, se puede usar una combinatoria de *lookaheads* que sumen. Por ejemplo, usando grupos y alternancia con `(?=.*[a-z])(?=.*[A-Z])(?=.*\d)|(?=.*[a-z])(?=.*[A-Z])(?=.*[especial])|....` Sin embargo, es más limpio hacerlo con código.

## Patrón para contraseña con todas las categorías y longitud exacta de 8 a 20

```regex
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,20}$
```

## Compatibilidad y limitaciones

*   **Motores modernos**: Los *lookaheads* funcionan en todos los motores modernos (salvo POSIX). En JavaScript, están disponibles desde siempre.
*   **Saltos de línea**: La parte `.{8,}` podría permitir saltos de línea si no se especifica; normalmente en campos de contraseña no hay `\n`, pero es seguro usar `[\s\S]{8,}` o limitar a caracteres visibles.
*   **Unicode**: Los caracteres Unicode están permitidos si usamos `\p{L}` etc., pero muchas aplicaciones restringen a ASCII.

## Buenas prácticas

> [!IMPORTANT]
> **Claridad**: No almacenar los requisitos solo en la regex; acompañar con explicación textual al usuario.

*   **Espacios**: Permitir espacios al final/inicio no suele ser deseable; usar `^\S{8,}$` si se prohíben espacios.
*   **Seguridad**: Para entornos de alta seguridad, la complejidad se mide con entropía, no con reglas fijas. La regex solo es una primera validación.

## Ejemplo completo en Python (usando módulo re)

```python
import re

password = "MiClave123!"
patron = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$')

if patron.match(password):
    print("Contraseña válida")
```

---

[« Anterior](04_numeros_y_monedas.md) | [Siguiente »](06_extractores_texto.md)



---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Numeros Y Monedas](04_numeros_y_monedas.md) | [🏠 Inicio](../../README.md) | [Extractores Texto ▶](06_extractores_texto.md) |
