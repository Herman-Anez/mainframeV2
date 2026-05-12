# 09 - Ejercicios Intermedios de Regex

> [!IMPORTANT]
> **Instrucciones:**
> Estos ejercicios profundizan en cuantificadores perezosos, grupos de captura, lookahead/lookbehind, y patrones prácticos. Proporciona la regex y una breve explicación de su funcionamiento.

## 1. Extraer el texto dentro de etiquetas HTML <strong>
Dado un fragmento HTML, captura el contenido que está entre `<strong>` y `</strong>`, incluyendo posibles espacios y otras etiquetas internas, pero usando cuantificador perezoso para obtener cada bloque por separado.

```text
Test: "<strong>Nota:</strong> esto es <strong>importante</strong>"
Coincidencia 1: "Nota:"  Coincidencia 2: "importante"
```

## 2. Validar un email con el patrón mejorado
Escribe una regex que valide un correo electrónico con las siguientes reglas:

* **Parte local:** caracteres alfanuméricos, puntos, guiones bajos, guiones, porcentajes y signos más. No puede empezar ni terminar con punto ni tener dos puntos consecutivos.
* **Dominio:** letras, dígitos, guiones; separado por puntos; el TLD debe tener al menos dos letras.

> [!TIP]
> Usa el patrón mejorado visto en los apuntes, no el básico.

```text
Test: "usuario@dominio.com"       -> válido
Test: "usuario@sub.dom.co.uk"    -> válido
Test: "usuario@dominio..com"     -> inválido
Test: ".usuario@dominio.com"     -> inválido
```

## 3. Buscar palabras que no están precedidas por el signo @
Encuentra palabras completas (secuencias de letras) que no formen parte de una mención (`@usuario`). Es decir, la palabra no debe estar inmediatamente después de un `@`.

```text
Test: "@user hola mundo"
Debe coincidir "hola", "mundo", pero NO "user".
```

## 4. Extraer el nombre de un archivo sin extensión
Dado un nombre de archivo (ej. "documento.pdf"), captura solo el nombre sin la extensión. El archivo puede tener múltiples puntos (ej. "archivo.backup.tar.gz"); en ese caso extrae el nombre completo hasta el último punto.

```text
Test: "foto.png"           -> "foto"
Test: "archivo.backup.gz"  -> "archivo.backup"
```

## 5. Validar una contraseña segura con lookaheads
Construye una regex que exija:
* Al menos 8 caracteres de longitud.
* Al menos una letra mayúscula.
* Al menos una letra minúscula.
* Al menos un dígito.
* Al menos un carácter especial de la lista `!@#$%^&*`.

```text
Test: "Clave123!"  -> válido
Test: "clave123!"  -> inválido (sin mayúscula)
Test: "CLAVE123!"  -> inválido (sin minúscula)
```

## 6. Capturar los tres primeros grupos de un número de teléfono internacional
Formato: `+XX (XXX) XXX-XXXX` o `+XX.XXX.XXX-XXXX`. Los separadores pueden ser espacio, punto o guión. Captura por separado: código de país, código de área y número local (todo junto sin separadores, solo dígitos).

```text
Test: "+1 (123) 456-7890"
Grupo 1: "1", Grupo 2: "123", Grupo 3: "4567890"

Test: "+34.666.777.888"
Grupo 1: "34", Grupo 2: "666", Grupo 3: "777888"
```

## 7. Reemplazar fechas de formato MM/DD/AAAA a DD/MM/AAAA
Usa una regex con grupos de captura para intercambiar el mes y el día en fechas del tipo `12/25/2024` a `25/12/2024`. Escribe el patrón y la cadena de sustitución.

```text
Entrada: "12/25/2024"
Salida: "25/12/2024"
```

## 8. Seleccionar líneas que contienen una palabra repetida dos veces consecutivas
En un texto multilínea, encuentra líneas donde una palabra (secuencia de letras) se repite exactamente, separada por un espacio: "hola hola". La coincidencia debe capturar la palabra repetida.

```text
Test:
hola hola mundo
adiós adiós
bien bien bien
```
> [!NOTE]
> En la primera línea captura "hola", segunda "adiós", tercera no.

## 9. Validar una cadena que no contenga la palabra "prohibido"
Escribe un patrón que solo case si la cadena completa falla en contener la palabra "prohibido" en cualquier parte.

```text
Test: "Este texto está bien"           -> match
Test: "Este texto está prohibido aquí" -> no match
```

## 10. Extraer hashtags de un tweet, ignorando signos de puntuación pegados
Encuentra todos los hashtags del estilo `#regex` o `#OpenSource`. Un hashtag comienza con `#` y continúa con caracteres de palabra (letras, números, guiones bajos). No debe incluir caracteres de puntuación como `,` o `.` si están pegados al final.

```text
Test: "Aprendiendo #regex, #OpenSource y #python3."
Coincidencias: "#regex", "#OpenSource", "#python3"
```

---

| [Anterior (Básicos)](01_basicos.md) | [Inicio](../../index.md) | [Siguiente (Avanzados)](03_avanzados.md) |



---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Basicos](01_basicos.md) | [🏠 Inicio](../../README.md) | [Avanzados ▶](03_avanzados.md) |
