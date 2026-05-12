# 📁 Fundamentos: Anclas y Límites

## 📌 Concepto: anclas y límites

Son posiciones dentro de la cadena que no consumen caracteres, sino que afirman que en ese punto se cumple una condición. Su función es delimitar dónde debe ocurrir una coincidencia sin añadir caracteres al resultado.

## 📌 `^` - Inicio

- **Modo normal (flag m inactivo):** Coincide con el inicio de la cadena.
- **Modo multilínea (m):** Coincide con el inicio de cada línea (después de cada `\n` o al inicio de la cadena).

```regex
^a → en "abc\naaa" sin flag m: coincide solo con el primer 'a'.
Con flag m: coincide con el primer 'a' de "abc" y el primer 'a' de "aaa".
```

> [!NOTE]
> El ancla no consume el salto de línea.

## 📌 `$` - Final

- **Normal:** Final de la cadena o justo antes de un `\n` al final de la cadena (varía según motor; PCRE: justo antes del salto final si existe).
- **Multilínea:** Final de cada línea (antes de `\n` o final de cadena).

```regex
a$ → "abc\naaa", con flag m, coincide con el 'a' final de "aaa" y con el 'a' de "abc".
```

> [!TIP]
> Para final absoluto sin importar el motor, es mejor usar `\z`.

## 📌 `\A` - Inicio absoluto

Coincide únicamente con el comienzo de la cadena, sin importar el flag multilínea.

```regex
\Aabc → "abc\ndef", con o sin m, solo al principio.
```

## 📌 `\z` y `\Z` - Final absoluto

- **`\z` (minúscula):** Final absoluto de la cadena, sin excepciones.
- **`\Z` (mayúscula):** Final de la cadena o justo antes de un salto de línea al final de la cadena.

> [!WARNING]
> En Python `re`, `\Z` funciona como final absoluto. Verifique siempre el comportamiento de su motor específico.

```regex
abc\z → "abc\n" NO coincidirá (porque hay \n luego).
abc\Z → Puede coincidir con "abc" y "abc\n" según motor.
```

## 📌 `\b` - Límite de palabra (word boundary)

Coincide en una posición entre un carácter de palabra (`\w` = `[a-zA-Z0-9_]`) y uno no palabra (`\W`) o entre un no palabra y uno palabra. También coincide al inicio de cadena si el primer carácter es `\w`, y al final si el último es `\w`.

Sirve para aislar palabras completas.

```regex
\bgato\b → busca la palabra "gato" como palabra entera.
"No es un gato, es un gato." coincide con las dos.
```

> [!IMPORTANT]
> `\b` depende de la definición de `\w`. Si `\w` incluye guion bajo, `\b` lo considerará parte de palabra.

## 📌 `\B` - No límite de palabra

Coincide en cualquier posición donde `\b` no coincide. Se usa para patrones que deben estar en medio de palabras.

```regex
\Bton\B → encuentra "ton" dentro de "tonelada" o "ratón" pero no si "ton" es palabra aislada.
```

## 📌 Combinación de anclas

Las anclas no consumen caracteres, por lo que podemos tener varias juntas. Por ejemplo, `^\b` exige que al inicio haya un límite de palabra (es decir, que el primer carácter tras el inicio sea `\w`).

## 📌 Uso incorrecto como caracteres dentro de clase

Dentro de `[...]`, `^` **NO** funciona como ancla, sino como negación de la clase (sólo si es el primer carácter). `$` y `\b` pierden su significado dentro de la clase y se tratan como literales.

> [!WARNING]
> Evitar escribir anclas dentro de clases sin sentido: `[$]` es simplemente un símbolo de dólar literal.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Literales y Escape](03_literales_y_escape.md) | [Índice](../README.md) | [Clases de Caracteres](05_clases_de_caracteres.md) |
