# 📁 Agrupación y Captura: Grupos sin Captura

## 📌 Definición

Un **grupo sin captura** permite agrupar una parte de la expresión regular sin almacenar el texto coincidente en la memoria del motor. Su sintaxis es `(?: ... )`.

Este tipo de grupo sirve únicamente para:
1. Aplicar cuantificadores a un bloque de caracteres.
2. Definir una alternancia encapsulada.
3. Atomizar una parte del patrón sin generar una referencia de captura (índice numérico).

### 🔹 Ejemplo

```regex
(?:https?:\/\/)?(?:www\.)?example\.com
```

En este caso, los grupos no capturan el protocolo ni el subdominio, pero permiten que ambos bloques sean opcionales de forma independiente mediante el cuantificador `?`.

---

## 📌 Ventajas frente a los grupos de captura

1.  **Eficiencia:** Al no tener que almacenar la subcadena en memoria para un uso posterior, se ahorra memoria y se reduce el tiempo de procesamiento.
2.  **Claridad:** Indica explícitamente a otros desarrolladores que esa subcoincidencia no se utilizará posteriormente en el código o en retroreferencias.
3.  **Evita interferencias de numeración:** Si ya tienes varios grupos de captura y necesitas añadir una agrupación adicional sin alterar los índices existentes (Grupo 1, 2, 3...), el grupo sin captura es la solución ideal.

> [!TIP]
> Si tienes la regex `(\d{4})-(\d{2})-(\d{2})` y decides hacer el separador opcional, puedes usar `(\d{4})(?:-(\d{2}))?`. De este modo, el año sigue siendo el **Grupo 1** y el mes el **Grupo 2**, sin que el guion "robe" un índice de captura.

---

## 📌 Sintaxis y uso

- **`(?:patrón)`**: Agrupa el contenido de `patrón` sin capturarlo.
- **Cuantificadores:** Se pueden aplicar normalmente. Ejemplo: `(?:abc)+` coincide con una o más repeticiones de la secuencia `"abc"`.
- **Alternancia:** `(?:gato|perro)` funciona igual que `gato|perro`, pero permite delimitar claramente el alcance de la alternancia dentro de una expresión más larga.

---

## 📌 Comparación con grupos de captura

Dado el texto `"rojo verde azul"`:

- **Con captura mixta:** `((?:r|v)\w+)`
  Captura palabras que empiezan con 'r' o 'v'. El grupo externo (paréntesis normales) captura toda la palabra (ej. `"rojo"`), mientras que el grupo interno `(?:r|v)` es sin captura. El **Grupo 1** será la palabra completa y no habrá Grupo 2.
  
- **Solo con captura:** `(r|v)(\w+)`
  Generaría dos capturas: la letra inicial en el **Grupo 1** (`"r"`) y el resto de la palabra en el **Grupo 2** (`"ojo"`).

---

## 📌 Grupos sin captura y modificadores de modo

En algunos motores de regex avanzados (PCRE, Java, .NET), se pueden incluir modificadores de comportamiento (flags) de forma localizada mediante la sintaxis `(?flags:...)`. Esto actúa como un grupo sin captura que aplica un modo específico solo a su contenido.

### 🔹 Ejemplo: Búsqueda insensible a mayúsculas
```regex
(?i:abc)
```
Coincidirá con `"ABC"`, `"Abc"`, `"abc"`, etc., sin afectar al resto del patrón externo.

> [!NOTE]
> El soporte varía según el lenguaje. Python `re` no soporta modificadores locales dentro de grupos, aunque sí admite `(?i)` al inicio del patrón para afectar a toda la expresión.

---

## 📌 Ejemplo práctico: Extracción de fecha

```regex
(\d{4})(?:[-/.])(\d{2})(?:[-/.])(\d{2})
```

Este patrón coincide con fechas como `2024-12-25`, `2024/12/25` o `2024.12.25`.
- **Grupo 1:** Año.
- **Grupo 2:** Mes.
- **Grupo 3:** Día.
- Los separadores están en grupos sin captura porque no necesitamos extraerlos individualmente, solo validar su presencia.

---

## 📌 Cuándo NO usar grupos sin captura

Si posteriormente necesitas acceder a la subcadena capturada para:
- Realizar reemplazos mediante `$1`, `\1`, etc.
- Procesar partes específicas del texto en tu lenguaje de programación.

En estos casos, **debes** utilizar paréntesis de captura normales `(...)`. Los grupos sin captura son totalmente invisibles para las funciones de extracción y retroreferencias.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Captura Básica](01_captura_basica.md) | [Índice](../README.md) | [Grupos Nombrados](03_grupos_nombrados.md) |
