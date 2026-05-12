# Extractores de Texto con Regex

## Redes Sociales: Hashtags y Menciones

### 1. Hashtags (`#etiqueta`)

```regex
(?<![^\s])#[a-zA-Z0-9_áéíóúüñ]+
```

**Soporte Unicode (`\p{L}`):**
```regex
(?<!\S)#[\p{L}\p{N}_]+
```

*   **Lookbehind (`(?<!\S)`)**: Asegura que la almohadilla esté al inicio de la línea o precedida por un espacio en blanco.
*   **Contenido**: Permite letras, números y guiones bajos.

### 2. Menciones (`@usuario`)

```regex
(?<!\S)@[a-zA-Z0-9_]+
```

> [!TIP]
> Este patrón puede refinarse para aceptar puntos o guiones medios según los requisitos específicos de cada red social.

## Delimitadores y Contenedores

### 1. Texto entre Comillas

Para obtener el contenido dentro de comillas, respetando escapes básicos:

*   **Comillas dobles**: `"((?:[^"\\]|\\.)*)"`
*   **Comillas simples**: `'((?:[^'\\]|\\.)*)'`

> [!NOTE]
> En ambos casos, el **Grupo 1** contiene el texto interior capturado.

## Datos de Contacto y Referencias

### 1. URLs (Recapitulando)

```regex
(?<!\S)(https?://[^\s]+)
```

### 2. Direcciones de Email

```regex
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```

### 3. Números de Teléfono (Genérico)

```regex
(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}
```

> [!NOTE]
> Captura formatos comunes como `123-456-7890`, `(123) 456-7890` o `+1-123-456-7890`.

## Otros Extractores Útiles

### 1. Fechas Sencillas
```regex
\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{4}-\d{1,2}-\d{1,2}\b
```

### 2. Nombres Propios (Mayúsculas)
```regex
\b\p{Lu}\p{L}*\b
```
*(Requiere flag `u` en JavaScript, y soporte para `\p{Lu}` en el motor)*.

### 3. Códigos Postales
*   **España (5 dígitos)**: `\b\d{5}\b`
*   **EE.UU. (5 o 5+4 dígitos)**: `\b\d{5}(?:-\d{4})?\b`
*   **Reino Unido**: `\b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b`

## Análisis de Logs e HTML

### 1. Log de Apache (Formato Común)
```regex
^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d+) (\d+|-)
```
**Grupos**: `1. IP`, `2. Ident`, `3. Usuario`, `4. Fecha`, `5. Petición`, `6. Código`, `7. Tamaño`.

### 2. Etiquetas HTML
```regex
<\/?([a-zA-Z][a-zA-Z0-9]*)[^>]*>
```
*Captura el nombre de la etiqueta en el **Grupo 1**.*

### 3. Contenido entre Tags Específicos (ej. `<title>`)
```regex
<title[^>]*>(.*?)</title>
```

## Estrategias para Extractores Eficientes

1.  **Clases Negadas**: Siempre que sea posible, usa clases negadas en lugar de cuantificadores perezosos (`.*?`). Ejemplo: `<tag([^>]*)>` es más eficiente que `<tag.*?>`.
2.  **Aislamiento**: Utiliza lookaheads y lookbehinds para aislar el objetivo sin consumir el contexto circundante.
3.  **Divide y Vencerás**: En procesamientos pesados, a veces es más rápido dividir el texto con `split()` y aplicar regex simples que intentar usar una única expresión extremadamente compleja.

## Ejemplo Combinado (JavaScript)

```javascript
let tweet = "Aprendiendo #regex con @usuario visita https://regex101.com";
let patterns = {
    hashtag: /#[\w]+/g,
    mention: /@[\w]+/g,
    url: /https?:\/\/[^\s]+/g
};

console.log(tweet.match(patterns.hashtag)); // ["#regex"]
console.log(tweet.match(patterns.mention)); // ["@usuario"]
console.log(tweet.match(patterns.url));     // ["https://regex101.com"]
```

---

[« Anterior](05_contrasenas.md) | [Siguiente »](../09_ejercicios/01_basicos.md)


