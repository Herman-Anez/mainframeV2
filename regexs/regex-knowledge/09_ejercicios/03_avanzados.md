# 09 - Ejercicios Avanzados de Regex

> [!IMPORTANT]
> **Instrucciones:**
> Estos problemas requieren dominio de temas como recursión, grupos atómicos, posesivos, propiedades Unicode, backtracking catastrófico y optimización. Las regex deben ser eficientes y correctas.

## 1. Validar paréntesis balanceados con recursión
Escribe una regex que verifique si una cadena contiene una expresión con paréntesis correctamente balanceados (puede haber texto dentro y fuera). Por ejemplo: `a(b(c)d)e` es válido, `a(b(c)d` no lo es. La recursión debe aplicarse sobre el patrón completo. (Usa PCRE, PHP, Perl o Python regex)

```text
Test: "(a(b)c)"   -> válido
Test: "((a)"      -> inválido
Test: "())"       -> inválido
```

## 2. Prevenir backtracking catastrófico en (a+)+b
Transforma el patrón `(a+)+b` en una versión que no sufra backtracking exponencial cuando se enfrenta a una cadena larga de "a"s sin "b" al final. Usa cuantificadores posesivos o grupos atómicos.

```text
Entrada de prueba: "aaaaaaaaaaaaaaaaaaaaX"
```
> [!NOTE]
> Explica por qué la versión original fallaría estrepitosamente y cómo la nueva lo evita.

## 3. Tokenizar un texto en palabras según propiedades Unicode
Exclusivamente con propiedades Unicode, extrae todas las palabras de un texto multilingüe. Una palabra se define como una secuencia de caracteres de categoría Letra (`\p{L}`). Debe ignorar números y puntuación.

```text
Test: "Hola, ¿cómo estás? 123 números и русский текст"
Resultado esperado: ["Hola", "cómo", "estás", "русский", "текст"]
```

## 4. Reemplazar comillas tipográficas conservando el contenido
Dado un texto con comillas latinas («...») y comillas inglesas (“...”), escribe un patrón que capture el texto interior y permita reemplazar ambos estilos por comillas dobles estándar, preservando el contenido. Utiliza grupos con nombre o retroreferencias para manejar el cierre correcto.

```text
Entrada: «Hola» y “mundo”
Salida (tras reemplazo): "Hola" y "mundo"
```

## 5. Validar un número de tarjeta de crédito (Visa, MasterCard, American Express) con una sola regex
Utiliza lookaheads para distinguir los formatos de inicio:

* **Visa:** empieza con 4, longitud 16.
* **MasterCard:** empieza con 51-55 o 2221-2720, longitud 16.
* **American Express:** empieza con 34 o 37, longitud 15.

> [!NOTE]
> No es necesario aplicar el algoritmo de Luhn.

```text
Test: "4111111111111111" -> Visa
Test: "5105105105105100" -> MasterCard
Test: "371449635398431" -> American Express
Test: "1234567812345670" -> no válido
```

## 6. Modo verboso: reescribe un patrón complejo con comentarios
Toma el siguiente patrón para validar un código postal español (5 dígitos) y una extensión opcional de 4 dígitos tras guión, con espacios opcionales: `^\d{5}\s*-?\s*(\d{4})?$`. Reescríbelo en modo verboso (con flag x o comentarios) explicando cada parte.

## 7. Extraer todas las claves JSON de primer nivel
Dada una cadena JSON simple (sin anidamiento de objetos), extrae las claves de las propiedades de primer nivel. Por ejemplo: `{"nombre":"Juan","edad":30,"ciudad":"Madrid"}` debería capturar nombre, edad, ciudad. Asume un formato sin espacios alrededor de comillas y dos puntos.

```text
Test: '{"nombre":"Juan","edad":30,"ciudad":"Madrid"}'
Capturas: "nombre", "edad", "ciudad"
```

## 8. Encontrar todas las palabras que contienen al menos dos vocales consecutivas
Usando clases de caracteres y cuantificadores, identifica palabras completas que tengan dos o más vocales seguidas (mayúsculas/minúsculas, considerando también vocales acentuadas: áéíóúü). No importa el resto de la palabra.

```text
Test: "El caos y la poesía en el cielo"
Debe coincidir: "caos", "poesía", "cielo"
```

## 9. Simular un grupo atómico en JavaScript
JavaScript no soporta grupos atómicos. Escribe un patrón equivalente para `(?>a+)b` utilizando lookahead y retroreferencia. Demuestra que funciona con la entrada "aaab" y que no funciona con "aaaa".

> [!TIP]
> Explicación: usa `(?=(a+))\1b`

## 10. Optimizar una regex para logs de Apache
Dado un patrón típico para analizar una línea de log de Apache: `^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d{3}) (\d+|- )`, sugiere mejoras de rendimiento utilizando cuantificadores posesivos o grupos atómicos donde sea posible, y explica por qué podrían reducir el backtracking en caso de líneas mal formadas.

---

# 💡 Soluciones

## Soluciones – Ejercicios Básicos

1. **Buscar la palabra "gato"**
   * **Regex:** `/\bgato\b/gi`
   * **Explicación:** `\b` límite de palabra, `gato` literal, bandera `i` para insensibilidad y `g` global.

2. **Código de área**
   * **Regex:** `/\(\d{3}\) /`
   * **Explicación:** `\(` `\d{3}` `\)` coincide con paréntesis y tres dígitos, seguido de espacio literal.

3. **Palabras terminadas en "ción"**
   * **Regex:** `/\w+ción\b/gi` (si `\w` soporta acentos y ñ con Unicode) o `/[a-zA-Záéíóúüñ]+ción\b/gi`.
   * **Explicación:** `\w+` una o más letras/dígitos/guion bajo, luego "ción", límite de palabra.

4. **Fecha DD/MM/AAAA**
   * **Regex:** `/^(0[1-9]|[12]\d|3[01])\/(0[1-9]|1[0-2])\/\d{4}$/`
   * **Explicación:** Día: 01-31, mes: 01-12, año: 4 dígitos. Los separadores son barras.

5. **Vocales**
   * **Regex:** `/[aeiou]/gi`
   * **Explicación:** Clase con las cinco vocales. `g` global, `i` case-insensitive.

6. **Múltiples espacios**
   * **Patrón de búsqueda:** `/\s+/g`
   * **Cadena de reemplazo:** un espacio `" "`.
   * **Explicación:** `\s+` uno o más caracteres de espacio.

7. **Nombre de usuario**
   * **Regex:** `/^[a-zA-Z0-9]{4,16}$/`
   * **Explicación:** Clase alfanumérica, cuantificador de 4 a 16. `^` y `$` para toda la cadena.

8. **Extensión de archivo**
   * **Regex:** /\.([a-zA-Z]+)$/
   * **Explicación:** Busca un punto literal seguido de una o más letras hasta el final de la cadena. El grupo 1 contiene la extensión.

9. **Líneas que empiezan con "Error"**
   * **Regex:** `/^Error\b.*/gim`
   * **Explicación:** `^` inicio de línea (con flag `m`), `Error` literal, `\b` límite de palabra, luego cualquier cosa. Flags: `g` global, `i` ignore case, `m` multilínea.

10. **Número decimal simple**
    * **Regex:** `/^-?\d+(\.\d+)?$/`
    * **Explicación:** `-?` signo opcional. `\d+` entero obligatorio. `(\.\d+)?` parte decimal opcional con punto y al menos un dígito.

---

## Soluciones – Ejercicios Intermedios

1. **Texto en <strong>**
   * **Regex:** `/<strong>(.*?)<\/strong>/gi`
   * **Explicación:** `.*?` perezoso captura contenido en el grupo 1. Flags global e ignore case.

2. **Validar email (mejorado)**
   * **Regex:**
   ```regex
   /^[a-zA-Z0-9]+(?:[._%+-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*(?:\.[a-zA-Z]{2,})+$/
   ```
   * **Explicación:** La parte local empieza con alfanumérico, luego permite separadores únicos entre bloques alfanuméricos. El dominio valida segmentos sin guiones al inicio/fin, y TLD de al menos 2 letras.

3. **Palabras no precedidas por @**
   * **Regex:** `/(?<!@)\b[a-zA-Z]+\b/g`
   * **Explicación:** Lookbehind negativo `(?<!@)` asegura que no haya `@` justo antes. `\b...\b` palabra de letras.

4. **Nombre de archivo sin extensión**
   * **Regex:** `/^(.+)\.([^.]+)$/` (aplicado con match y grupo 1).
   * **O usando lookahead:** `/.+(?=\.)/`.
   * **Explicación:** Captura todo hasta el último punto. Grupo 1 contiene el nombre.

5. **Contraseña segura**
   * **Regex:** `/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/`
   * **Explicación:** Cuatro lookaheads que verifican presencia de cada categoría. `.{8,}` consume la cadena.

6. **Teléfono internacional**
   * **Regex:**
   ```regex
   /^\+(\d+)\D*\(?(\d+)\)?\D*(\d+)\D*(\d+)$/
   ```
   * **Explicación:** Luego concatenar grupo 3 y 4 para el número local.

7. **Intercambiar fecha MM/DD/AAAA**
   * **Patrón:** `/(\d{2})\/(\d{2})\/(\d{4})/`
   * **Cadena de reemplazo:** `$2/$1/$3`
   * **Explicación:** Grupo 1: mes, Grupo 2: día, Grupo 3: año. Se invierten 1 y 2.

8. **Palabra repetida consecutiva**
   * **Regex:** `/\b(\w+)\s+\1\b/g`
   * **Explicación:** `(\w+)` captura palabra. `\s+` espacios. `\1` exige la misma palabra. `\b` límites aseguran palabra completa.

9. **Cadena sin "prohibido"**
   * **Regex:** `/^(?!.*prohibido).*$/` (o con flags `i` si no importa mayúsculas).
   * **Explicación:** El lookahead negativo `(?!.*prohibido)` falla si en cualquier lugar aparece "prohibido".

10. **Hashtags limpios**
    * **Regex:** `/#\w+\b/g`
    * **Explicación:** `#\w+` hashtag. El `\b` al final impide que caracteres extra como `,` se incluyan (porque `,` no es parte de `\w`).

---

## Soluciones – Ejercicios Avanzados

1. **Paréntesis balanceados con recursión**
   * **Regex (PCRE/Python regex):**
   ```regex
   /^(?:[^()]* \((?: (?: [^()]++ | (?R) )* )\) [^()]* )+$/x
   ```
   * **Explicación:** Desde el inicio, permite texto sin paréntesis, luego `\(`, dentro un grupo atómico que repite caracteres no paréntesis o recursión, y cierra `\)`. `[^()]++` es posesivo para eficiencia.

2. **Prevenir backtracking catastrófico**
   * **Regex original:** `(a+)+b`
   * **Regex optimizada:** `(a++)+b` o `(?>a+)+b` o simplemente `a+b` (si no es necesario el anidamiento).
   * **Explicación:** Con `a++` el cuantificador no cede caracteres, eliminando el retroceso exponencial. Al aplicarlo sobre "aaaa...X" falla inmediatamente porque tras consumir todas las "a"s no hay "b" y no intenta redistribuir.

3. **Tokenizar con propiedades Unicode**
   * **Regex:** `/\p{L}+/gu` en JavaScript, o en Python regex: `\p{L}+`.
   * **Explicación:** `\p{L}` cualquier letra Unicode. Flag `u` y `g` dan todas las secuencias de letras.

4. **Comillas tipográficas a comillas rectas**
   * **Patrón:** `/«([^«»]+)»|“([^“”]+)”/`
   * **Reemplazo:** `"$1$2"`.
   * **Explicación:** Se puede usar un solo grupo con nombre y condicional (en motores que lo permitan), pero con alternancia simple y dos grupos es fácil: la coincidencia tendrá grupo 1 o grupo 2. En sustitución `"$1$2"` (uno estará vacío).

5. **Tarjeta de crédito**
   * **Regex:**
   ```regex
   /^(?:(?=4)\d{16}|(?=5[1-5]|222[1-9]|22[3-9]|2[3-6]|27[0-1]|2720)\d{16}|(?=3[47])\d{15})$/
   ```
   * **Explicación:** Ajuste para MasterCard: comienzo 51-55 o 2221-2720.

6. **Modo verboso**
   ```python
   pattern = re.compile(r"""
       ^
       \d{5}      # código postal base
       \s* -? \s* # separador flexible
       (\d{4})?   # extensión opcional
       $
   """, re.VERBOSE)
   ```

7. **Claves JSON de primer nivel**
   * **Regex:** `/"([^"]+)":/g`
   * **Explicación:** Busca comilla, captura uno o más caracteres no comilla, luego comilla y dos puntos. Grupo 1 contiene la clave.

8. **Palabras con al menos dos vocales consecutivas**
   * **Regex (con vocales acentuadas):** `/\b\w*[aeiouáéíóúü]{2}\w*\b/gi`
   * **Explicación:** `\b\w*` inicio de palabra, luego dos vocales seguidas, luego resto de palabra.

9. **Simular grupo atómico en JavaScript**
   * **Regex:** `/(?=(a+))\1b/`
   * **Explicación:** En "aaab" devuelve match. En "aaaa" no hay match.

10. **Optimizar Apache log regex**
    * **Patrón original:** `^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d{3}) (\d+|- )`
    * **Mejoras:**
      ```text
      ^(\S++) (\S++) (\S++) \[([^][]*+)\] "([^"]*+)" (\d{3}) (\d++|-)
      ```
    * **Explicación:** Cada `++` y `*+` evita que, en caso de fallo más adelante, el motor intente reducir la captura y redistribuir, evitando backtracking innecesario en líneas incompletas.

---

| [Anterior (Intermedios)](02_intermedios.md) | [Inicio](../../index.md) |
