# 📁 Agrupación y Captura: Captura Básica

## 📌 ¿Qué es un grupo de captura?

Un grupo de captura es una subexpresión encerrada entre paréntesis `(...)`. Cumple dos funciones principales:

1.  **Agrupar** partes del patrón para aplicar cuantificadores, alternancia o anidamiento de forma conjunta.
2.  **Capturar** la subcadena que coincide con esa subexpresión, permitiendo recuperarla posteriormente (en el código, en operaciones de reemplazo o mediante retroreferencias).

### 🔹 Ejemplo sencillo

```regex
(\d{3})-(\d{2})-(\d{4})
```

Aplicado al texto `"123-45-6789"`, los paréntesis capturan tres partes: `"123"`, `"45"` y `"6789"`.

---

## 📌 Numeración de los grupos

Los grupos de captura se numeran de izquierda a derecha según el orden del paréntesis de apertura. 

- El **Grupo 0** es siempre la coincidencia completa del patrón.
- Los **Grupos 1, 2, 3...** corresponden a cada par de paréntesis en orden de aparición.

### 🔹 Ejemplo de numeración

```regex
(a(b)c)d
```

Coincidencia sobre `"abcd"`:
- **Grupo 0:** `"abcd"`
- **Grupo 1:** `"abc"` (primer paréntesis de apertura)
- **Grupo 2:** `"b"` (segundo paréntesis, anidado)

> [!NOTE]
> La numeración es fija y no depende de si el grupo participó o no en la coincidencia. Un grupo opcional que no casó tendrá un valor `null`, `None` o una cadena vacía, dependiendo del motor de regex utilizado.

---

## 📌 Cómo acceder a las capturas desde código

La forma de obtener el contenido de los grupos varía según el lenguaje de programación:

### 🔹 Python
```python
import re
m = re.search(r'(\d{3})-(\d{2})-(\d{4})', '123-45-6789')
m.group(0)  # '123-45-6789'
m.group(1)  # '123'
m.group(2)  # '45'
m.group(3)  # '6789'
m.groups()  # ('123', '45', '6789')
```

### 🔹 JavaScript
```javascript
let regex = /(\d{3})-(\d{2})-(\d{4})/;
let match = '123-45-6789'.match(regex);
match[0]; // '123-45-6789'
match[1]; // '123'
match[2]; // '45'
match[3]; // '6789'
```

### 🔹 Java
```java
Pattern p = Pattern.compile("(\\d{3})-(\\d{2})-(\\d{4})");
Matcher m = p.matcher("123-45-6789");
if (m.find()) {
    m.group(1); // "123"
    m.group(2); // "45"
    m.group(3); // "6789"
}
```

---

## 📌 Grupos anidados

Los paréntesis se pueden anidar libremente; la numeración siempre sigue el orden de apertura de los paréntesis.

### 🔹 Ejemplo de anidamiento
```regex
((a)(b(c)))d
```

Texto: `"abcd"`
- **Grupo 1:** `"abc"` (abre primero)
- **Grupo 2:** `"a"` (abre segundo)
- **Grupo 3:** `"bc"` (abre tercero, corresponde a `b(c)`)
- **Grupo 4:** `"c"` (abre cuarto)

---

## 📌 Grupos opcionales y valor nulo

Un grupo puede ser condicional gracias a cuantificadores como `?` o `*`. Si la parte del patrón no coincide, el grupo sigue existiendo pero su valor queda vacío o indefinido.

### 🔹 Ejemplo
```regex
(a(\d)?b)
```

- En `"ab"`: Grupo 1 es `"ab"`, Grupo 2 es `None` (o vacío).
- En `"a5b"`: Grupo 2 es `"5"`.

---

## 📌 Uso de grupos para aplicar cuantificadores

Los grupos nos permiten aplicar repeticiones a secuencias complejas, no solo a caracteres individuales.

```regex
(https?:\/\/)?(www\.)?example\.com
```

Los grupos capturan el protocolo y el subdominio si existen, permitiendo extraerlos o validarlos opcionalmente.

### 🔹 Captura y alternancia
```regex
(jpg|png|gif)$
```
Este patrón captura la extensión del archivo. Solo se captura la alternativa que finalmente coincide con el texto.

---

## 📌 Eficiencia y memoria

Cada grupo de captura consume recursos de memoria porque el motor debe almacenar la subcadena capturada para su uso posterior. 

> [!IMPORTANT]
> En patrones de gran escala o procesamiento masivo de datos, el uso excesivo de capturas puede ralentizar la ejecución. Si solo necesitas agrupar pero no capturar la información, utiliza **grupos sin captura** `(?:...)`.

---

## 📌 Buenas prácticas

- **Usa nombres de grupo:** Para mejorar la legibilidad en patrones complejos (ver sección de Grupos Nombrados).
- **Equilibra paréntesis:** Asegúrate siempre de cerrar todos los paréntesis abiertos para evitar errores de sintaxis.
- **Escapa caracteres literales:** Si necesitas buscar un paréntesis literal en el texto, usa `\(` y `\)`.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Ejemplos Prácticos](../02_cuantificadores/03_ejemplos_practicos.md) | [Índice](../README.md) | [Grupos sin Captura](02_grupos_sin_captura.md) |
