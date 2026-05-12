# Manejo de URLs con Regex

## ¿Qué es una URL?

Una URL estándar (HTTP/HTTPS) sigue la estructura:
`protocolo://[usuario:contraseña@]dominio[:puerto]/[ruta]?[query]#[fragmento]`

Los patrones regex pueden capturar todos o algunos de estos componentes según la necesidad.

## Extracción de URLs

### 1. Patrón básico para extraer URLs de un texto

```regex
https?://[^\s/$.?#].[^\s]*
```

*   `https?://`: Exige el protocolo.
*   `[^\s/$.?#]`: Obliga a que el primer carácter del dominio no sea espacio ni algunos símbolos.
*   `[^\s]*`: Consume todo hasta un espacio en blanco.

> [!NOTE]
> Esto captura la mayoría de URLs en textos planos, pero puede incluir paréntesis o puntos finales no deseados si la URL está al final de una oración.

### 2. Patrón robusto (Delimitación por puntuación)

```regex
https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?::\d+)?(?:/[^\s]*)?
```

*   **Dominio**: Nombre de host con letras, dígitos, guiones, puntos, y soporte para caracteres escapados con `%`.
*   **Puerto opcional**: `:\d+`.
*   **Ruta opcional**: Cualquier cosa sin espacios.

> [!TIP]
> Es mejor que el básico, aunque en algunos casos específicos puede seguir capturando un punto final si no se añade un límite de palabra negativo.

### 3. Extracción precisa en HTML

En entornos controlados como HTML, se puede usar un patrón que respeite los delimitadores naturales:

```regex
(?:"|')((?:https?|ftp)://[^"'\s]+)(?:"|')     // Entre comillas
(?:href|src)=["']?((?:https?|ftp)://[^"'\s>]+) // Atributos HTML
```

## Validación de URLs completas

El siguiente patrón verifica el formato e impone que la URL no esté mal construida:

```regex
^https?://([\w\-]+\.)+[\w\-]+(:\d+)?(/[\w\-./?%&=+#]*)?$
```

*   **Protocolo**: Obligatorio.
*   **Dominio**: Con al menos un punto y segmentos.
*   **Puerto**: Opcional.
*   **Ruta**: Opcional con caracteres válidos.

> [!IMPORTANT]
> Es útil para validar entradas de usuario donde se espera una URL absoluta y bien formada.

## Soporte para Dominios Internacionalizados (IDN)

En dominios pueden aparecer caracteres Unicode (ej. `http://españa.es`). Para capturarlos:

```regex
https?://(?:[-\p{L}\p{N}_]|(?:%[\da-fA-F]{2}))+\.(?:\p{L}{2,})(?::\d+)?(?:/[^\s]*)?
```

> [!NOTE]
> Requiere flag `u` en JavaScript, y soporte para `\p{L}` en motores como PCRE o el módulo `regex` de Python.

## Análisis de Componentes (Fragmentos y Query String)

Si quieres analizar los componentes individuales, usa grupos de captura:

```regex
^(https?)://([\w\-\.]+)(?::(\d+))?(/[^?#]*)?(?:\?([^#]*))?(?:#(.*))?$
```

**Grupos capturados:**
1. Protocolo
2. Host
3. Puerto
4. Ruta
5. Query String
6. Fragmento

## Ejemplos prácticos en código

### JavaScript: Extraer todas las URLs
```javascript
let urlRegex = /https?:\/\/[^\s/$.?#].[^\s]*/g;
let matches = texto.match(urlRegex);
// Limpiar puntuación final con slice si es necesario.
```

### Python: Validar URL
```python
import re
pat = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(:\d+)?(/[-\w./?%&=+#]*)?$'
re.match(pat, url) is not None
```

## Consideraciones y limitaciones

*   **Validación de TLD**: Estas regex no validan que el TLD sea real (por ejemplo, `.com`, `.es`). Para una validación rigurosa, se necesita una lista de TLDs actualizada.
*   **Caracteres ilegales**: Tampoco restringen caracteres ilegales en la ruta según el contexto (como espacios sin codificar). Para eso se debe escapar o usar `encodeURI`.
*   **Fragmentos**: En entornos donde se permiten fragmentos, ten cuidado con los caracteres `#` internos.

---

[« Anterior](01_validacion_emails.md) | [Siguiente »](03_fechas_y_horas.md)

