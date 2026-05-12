# 📁 Agrupación y Captura: Grupos Atómicos

## 📌 Definición

Un **grupo atómico** es una agrupación que, una vez que ha coincidido con una parte del texto, "bloquea" esa coincidencia y no permite que el motor de búsqueda realice backtracking (retroceso) hacia su interior.

Su sintaxis es `(?> ... )`.

> [!NOTE]
> Los grupos atómicos están disponibles en motores como PCRE, Perl, Java y .NET. En Python, solo están disponibles mediante el módulo externo `regex` (el módulo estándar `re` no los soporta). JavaScript no cuenta con soporte nativo para esta funcionalidad.

---

## 📌 Comportamiento

Cuando el motor entra en un grupo atómico `(?>subexpresión)`, intenta encontrar una coincidencia para dicha subexpresión de la forma habitual. Sin embargo, si tiene éxito y sale del grupo, **descarta todos los estados internos de retroceso**.

Si el resto del patrón (lo que está fuera del grupo) falla posteriormente, el motor no intentará volver al grupo atómico para probar con menos repeticiones o alternativas diferentes; simplemente fallará la coincidencia global desde esa posición.

### 🔹 Similitud con cuantificadores posesivos
Un cuantificador posesivo (como `++` o `*+`) es funcionalmente equivalente a un grupo atómico que envuelve a un elemento cuantificado:
- `a++` es equivalente a `(?>a+)`.
- `.*+` es equivalente a `(?>.*)`.

---

## 📌 Ejemplo de funcionamiento

### 🔹 Patrón: `(?>a+)b`

**Caso 1: Texto `"aaaab"`**
1.  El motor entra en el grupo, `a+` consume las 4 letras `"a"`.
2.  Sale del grupo atómico.
3.  Intenta casar la `b` final. Como el siguiente carácter es efectivamente `b`, la coincidencia es exitosa: `"aaaab"`.

**Caso 2: Texto `"aaaa"`**
1.  `a+` consume las 4 letras `"a"`.
2.  Sale del grupo atómico.
3.  Intenta casar la `b` final, pero la cadena se ha terminado.
4.  **Resultado:** El motor falla inmediatamente. No intenta retroceder para ver si `a+` podría haber tomado solo 3 letras `"a"` para dejar paso a la `b`.

---

## 📌 Diferencia con grupos normales

Comparemos con un grupo normal `(a+)b` sobre el texto `"aaaa"`:
1.  `a+` toma las 4 letras `"a"`.
2.  Intenta casar `b`, falla.
3.  **Backtrack:** `a+` cede una `"a"`, quedándose con 3. Intenta `b`, falla.
4.  El proceso se repite (cede otra `"a"`, etc.) hasta que se agotan las posibilidades.

> [!TIP]
> En patrones muy complejos o con anidamientos de cuantificadores, eliminar estos pasos de retroceso innecesarios mediante grupos atómicos mejora drásticamente el rendimiento y evita el **backtracking catastrófico**.

---

## 📌 Usos principales

1.  **Optimización de rendimiento:** Evitar que el motor explore caminos que sabemos de antemano que no conducirán a una coincidencia exitosa.
2.  **Prevención de desastres:** Patrones como `(a+)*b` son extremadamente peligrosos con entradas largas que no coinciden. Transformarlo a `(?>a+)*b` elimina el riesgo de cuelgue por recursividad infinita.
3.  **Captura de palabras completas:** Asegurar que una vez que se toma una palabra, el motor no intente "soltar" el final de la misma para intentar casar con un prefijo de otra regla.

---

## 📌 Simulación en motores sin soporte

En JavaScript, se puede simular un grupo atómico utilizando un **lookahead positivo** y una **retroreferencia**:

```javascript
// Simulación de (?>a+)b
/(?=(a+))\1b/
```

1.  `(?=(a+))`: El lookahead captura `a+` de forma greedy pero no consume el texto.
2.  `\1`: La retroreferencia consume exactamente lo que el lookahead acaba de capturar. Como las retroreferencias son fijas, no permiten backtracking, logrando el mismo efecto que un grupo atómico.

---

## 📌 Precauciones

Un grupo atómico no debe usarse si la coincidencia global **realmente requiere** retroceder dentro de él para tener éxito. 

> [!CAUTION]
> Si utilizas un grupo atómico y el motor "bloquea" una coincidencia que impedía ver la solución global correcta, la regex fallará aunque el texto sea válido para el patrón lógico. Úsalo solo cuando estés seguro de que la subexpresión interior no necesita ser reconsiderada.

---

## 📌 Ejemplo de optimización real: Números con separadores

```regex
(?> \d{1,3} (?: , \d{3} )* ) (?: \. \d+ )?
```

Agrupar la lógica de la parte entera en un grupo atómico evita que el motor intente distribuciones alternativas de comas si la entrada es inválida (por ejemplo, si faltan dígitos al final), acelerando significativamente el fallo del patrón.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Retroreferencias](04_retroreferencias.md) | [Índice](../README.md) | [Lookahead (Aserciones)](../04_aserciones/01_lookahead.md) |
