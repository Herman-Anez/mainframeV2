# Validación de Emails con Regex

## La complejidad de validar un correo electrónico

Validar un email con una expresión regular que cumpla rigurosamente el RFC 5321/5322 es extremadamente complejo. La especificación permite una sintaxis muy amplia (caracteres especiales, *quoted strings*, comentarios anidados, etc.), que en la práctica casi ningún servicio implementa. Por ello, la mayoría de las aplicaciones utilizan patrones pragmáticos, que cubren el >99% de los casos reales y rechazan formatos absurdos.

## Patrones Comunes

### 1. Patrón básico (Muy tolerante)

Acepta la estructura `algo@algo.algo` con caracteres alfanuméricos y algunos símbolos. No es estricto pero es muy popular.

```regex
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

*   **Parte local**: Letras, dígitos, puntos, guiones bajos, porcentajes, más, menos.
*   **Dominio**: Letras, dígitos, puntos, guiones.
*   **Extensión**: Al menos dos letras.

> [!NOTE]
> Es simple, rechaza espacios y caracteres exóticos, pero permite dominios como `algo..com` (doble punto) o guiones al inicio/fin, aunque en la mayoría de casos prácticos no es problemático.

### 2. Patrón mejorado (Con restricciones comunes)

```regex
^[a-zA-Z0-9]+(?:[._%+-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z]{2,})+$
```

*   La parte local empieza y acaba con alfanumérico, permite un separador entre bloques alfanuméricos.
*   El dominio prohíbe guiones al inicio, permite segmentos separados por punto, y al menos un punto con extensión de letras.
*   Evita dobles puntos y otras combinaciones inválidas.

### 3. Patrón avanzado (Cercano al RFC, pero práctico)

```regex
^(?=.{1,254}$)(?=.{1,64}@)[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$
```

*   Limita la longitud total a 254 caracteres (máximo estándar) y la parte local a 64.
*   Permite un conjunto ampliado de caracteres especiales en la parte local.
*   **Dominio**: Cada etiqueta (subdominio) debe tener entre 1 y 63 caracteres, sin empezar ni terminar con guión.
*   Exige TLD de al menos 2 letras (no valida TLDs reales, eso se haría contra una lista externa).

> [!TIP]
> Es largo pero robusto para validación en backend.

> [!IMPORTANT]
> **Nota sobre Unicode**: En JavaScript este patrón puede usarse con la flag `u` si se esperan caracteres Unicode, pero entonces la parte local permitiría caracteres internacionales según el estándar (aunque no todos los servidores los aceptan). Una versión con soporte internacional usaría `\p{L}` en lugar de `a-zA-Z`, pero la complejidad crece.

## Validación por pasos (Recomendada)

Muchas veces es mejor hacer una validación básica con regex y luego comprobar existencia del dominio vía DNS o enviar un correo de confirmación. La regex solo debería garantizar que el formato es plausible.

## Consideraciones por motor

*   **JavaScript**: Para TLDs con caracteres internacionalizados (IDN), usar `[\p{L}]{2,}` con la flag `u`.
*   **Python**: `re` estándar es suficiente; para IDN, usar el módulo `regex`.
*   **Java/PCRE**: Similar a los patrones anteriores.

## Ejemplos de testeo

```javascript
const emailRegex = /^[a-zA-Z0-9]+(?:[._%+-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z]{2,})+$/;

emailRegex.test("usuario@dominio.co.uk");   // true
emailRegex.test("usuario@sub.dominio.com"); // true
emailRegex.test("usuario@dominio..com");     // false (doble punto)
emailRegex.test("usuario@-dominio.com");    // false (guion al inicio)
```

## Límites y extensiones

Si necesitas soporte para comentarios (RFC 5322) o *quoted strings*, la regex se vuelve monstruosa; es mejor utilizar una biblioteca específica. Para la mayoría de aplicaciones, el patrón mejorado es suficiente y seguro.

---

[« Anterior](../07_temas_avanzados/05_optimizacion.md) | [Siguiente »](02_urls.md)



---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| ➖ | [🏠 Inicio](../../README.md) | [Urls ▶](02_urls.md) |
