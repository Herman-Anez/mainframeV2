# 📁 Agrupación y Captura: Retroreferencias

## 📌 Definición

Una **retroreferencia** (*backreference*) es una construcción que permite hacer referencia a un grupo de captura previamente encontrado dentro del mismo patrón. En lugar de repetir la lógica del patrón, la retroreferencia exige que el texto actual coincida **exactamente** con la subcadena capturada por dicho grupo.

---

## 📌 Sintaxis básica

### 🔹 Para grupos numerados
- **`\1`, `\2`, ... `\9`**: Referencia a los grupos del 1 al 9.
- **`\10` o superior**: Puede ser ambiguo. En motores como PCRE, `\10` se interpreta como el grupo 10 si este existe; de lo contrario, se interpreta como el grupo 1 seguido del carácter `"0"`.

> [!TIP]
> Para evitar ambigüedades con números de dos dígitos, se recomienda usar la notación `\g{n}` (si el motor la soporta, como en PCRE o Python `regex`).

### 🔹 Para grupos con nombre
- **Python:** `(?P=nombre)`
- **PCRE / JS / Java / .NET:** `\k<nombre>` o `\k'nombre'`

---

## 📌 Ejemplo clásico: Palabras repetidas

```regex
\b(\w+)\s+\1\b
```

Este patrón coincide con palabras duplicadas como `"hola hola"` o `"mundo mundo"`.

1.  **`(\w+)`**: Captura la primera palabra en el **Grupo 1**.
2.  **`\s+`**: Coincide con uno o más espacios.
3.  **`\1`**: Exige que el siguiente bloque de texto sea idéntico al capturado en el Paso 1.

---

## 📌 Coincidencia de comillas y delimitadores

```regex
(["'])(.*?)\1
```

Este patrón es ideal para capturar texto entre comillas, asegurando que la comilla de cierre sea la misma que la de apertura.
- En `"una frase"`, el Grupo 1 captura `"` y `\1` busca `"`.
- En `'otra frase'`, el Grupo 1 captura `'` y `\1` busca `'`.
- En `"frase mal cerrada'`, el patrón fallará porque `\1` esperará una comilla doble.

---

## 📌 Numeración en grupos anidados

Dado el patrón `((a)(b(c)))d`, las retroreferencias corresponden a:
- **`\1`** → `"abc"` (primer paréntesis de apertura)
- **`\2`** → `"a"`
- **`\3`** → `"bc"`
- **`\4`** → `"c"`

> [!IMPORTANT]
> Lo habitual es que el grupo referenciado esté a la **izquierda** de la retroreferencia. Intentar referenciar un grupo que aún no ha sido procesado (retroreferencia hacia adelante) suele fallar o tener un comportamiento indefinido según el motor.

---

## 📌 Referencias en cadenas de reemplazo

Aunque se llaman igual, las referencias en la cadena de sustitución funcionan de forma distinta:
- **Propósito:** Insertar el contenido capturado en el nuevo texto.
- **Sintaxis:**
    - **sed / Perl:** `$1`, `$2`.
    - **Python:** `\1`, `\2`.
    - **JavaScript:** `$1`, `$2`.

### 🔹 Ejemplo de inversión de palabras en Python
```python
import re
texto = "Juan Perez"
# Intercambiar palabras
resultado = re.sub(r'(\w+)\s+(\w+)', r'\2 \1', texto)
# resultado: "Perez Juan"
```

---

## 📌 Retroreferencias a grupos opcionales

Si un grupo es opcional (seguido de `?` o `*`) y no coincide con nada, la retroreferencia suele comportarse de la siguiente manera:
- **Python `re`:** La retroreferencia fallará (no coincide con nada).
- **PCRE:** La coincidencia fallará a menos que se trate de una referencia vacía permitida.
- **En general:** Es una mala práctica referenciar grupos que podrían no capturar nada, ya que el comportamiento varía entre motores.

---

## 📌 Retroreferencias vs. Subrutinas

En motores avanzados (PCRE, Perl), es importante no confundir una retroreferencia con una **subrutina** `(?1)`.
- **Retroreferencia (`\1`)**: Compara con el **texto literal** ya capturado. Exige igualdad de contenido.
- **Subrutina (`(?1)`)**: Ejecuta el **patrón** del grupo 1 nuevamente. No exige que el contenido sea el mismo, solo que cumpla la misma regla.

### 🔹 Ejemplo de diferencia
- `(\d{3})-\1`: Coincide con `123-123`, pero NO con `123-456`.
- `(\d{3})-(?1)`: Coincide con `123-123` Y con `123-456`.

---

## 📌 Número máximo de retroreferencias

La mayoría de los motores permiten hasta 99 retroreferencias. Si necesitas más de 9 grupos, utiliza la notación segura `\g{n}` para evitar que `\10` sea interpretado como el grupo 1 seguido de un cero literal.

---

## 📌 Limitaciones y riesgos

1.  **Backtracking intenso:** El uso de retroreferencias impide que el motor de regex utilice optimizaciones basadas en autómatas finitos (DFA), lo que puede llevar a un rendimiento pobre en casos complejos.
2.  **Incompatibilidad:** Los motores que se basan estrictamente en expresiones regulares matemáticas (como el DFA de awk o grep estándar) no soportan retroreferencias, ya que estas técnicamente convierten el lenguaje en uno no regular.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Grupos Nombrados](03_grupos_nombrados.md) | [Índice](../README.md) | [Grupos Atómicos](05_grupos_atomicos.md) |
