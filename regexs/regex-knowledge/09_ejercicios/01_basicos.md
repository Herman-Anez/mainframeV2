# 09 - Ejercicios Básicos de Regex

> [!IMPORTANT]
> **Instrucciones:**
> Escribe una expresión regular para cada uno de los siguientes problemas. Si el motor lo requiere, especifica las banderas. Prueba tus patrones en un probador online ([regex101.com](https://regex101.com), [pythex.org](https://pythex.org)) con los casos de ejemplo.

## 1. Buscar la palabra "gato"
Encuentra todas las apariciones de la palabra "gato" en una frase, sin distinguir mayúsculas/minúsculas. Debe coincidir como palabra completa.

```text
Test: "El gato y el GATO gatean"
Coincidencias esperadas: "gato", "GATO"
```

## 2. Validar un código de área de EE.UU.
Formato: tres dígitos entre paréntesis (seguidos de espacio y tres dígitos adicionales, pero solo valida el código de área). Por ejemplo, "(123) " debe coincidir.

```text
Test: "(123) 456-7890"  -> match "(123) "
Test: "(12) 345"        -> no match
```

## 3. Encontrar todas las palabras que terminan en "ción"
Coincide con palabras completas que tengan la terminación "ción" (ej. "canción", "acción"). Ignora mayúsculas/minúsculas.

```text
Test: "La canción y la ACCIÓN fueron bien."
Coincidencias: "canción", "ACCIÓN"
```

## 4. Validar una fecha en formato DD/MM/AAAA
Día de 01 a 31, mes de 01 a 12, año de 4 dígitos. No hace falta validar días por mes (p.ej. 31/02/2023 es válido para este ejercicio).

```text
Test: "15/08/2024" -> match
Test: "5/8/2024"   -> no match (exige dos dígitos)
```

## 5. Encontrar todas las vocales
Extrae todas las vocales (tanto mayúsculas como minúsculas) de un texto.

```text
Test: "Hola Mundo" -> ["o", "a", "u", "o"]
```

## 6. Reemplazar múltiples espacios por uno solo
Escribe un patrón que capture cualquier secuencia de uno o más espacios en blanco (espacio, tabulador, salto de línea) para luego reemplazarlas por un solo espacio.

```text
Test: "Hola    mundo.\t\tAdiós"
Después del reemplazo: "Hola mundo. Adiós"
```

## 7. Validar un nombre de usuario alfanumérico
Debe tener entre 4 y 16 caracteres, compuestos únicamente por letras (mayúsculas y minúsculas) y dígitos. No puede contener espacios ni símbolos.

```text
Test: "usuario123" -> válido
Test: "user name"  -> inválido
```

## 8. Extraer extensiones de archivo
De una lista de nombres de archivo, extrae la extensión (sin el punto). Solo debe capturar extensiones de letras (no números al final). Por ejemplo: "imagen.jpg", "documento.pdf", "script.js".

```text
Test: "foto.png"     -> extensión "png"
Test: "archivo.tar.gz" -> extensión "gz" (la última)
```

## 9. Buscar líneas que comienzan con "Error"
Procesa un texto multilínea y selecciona todas las líneas que empiezan por la palabra "Error" (sin importar mayúsculas/minúsculas). La palabra debe estar al inicio de la línea.

```text
Test:
Todo bien
Error: fallo crítico
WARNING: revisar
error menor
```
> [!NOTE]
> Se espera coincidencia en la segunda línea: "Error: fallo crítico"

## 10. Validar un número decimal simple
Formato: puede tener un signo negativo opcional, dígitos enteros obligatorios, y opcionalmente un punto seguido de uno o más dígitos decimales. Ej: "-3.14", "10", "0.5". No permite múltiples puntos ni caracteres extra.

```text
Test: "42"        -> válido
Test: "-.5"       -> inválido (falta entero)
Test: "1.2.3"     -> inválido
```

---

| [Anterior (08_patrones_utiles)](../08_patrones_utiles/06_extractores_texto.md) | [Inicio](../../index.md) | [Siguiente (Intermedios)](02_intermedios.md) |

