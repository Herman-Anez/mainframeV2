# 📁 Cuantificadores: Greedy y Lazy

## 📌 ¿Qué son los cuantificadores?

Los cuantificadores especifican cuántas veces debe aparecer el elemento inmediatamente anterior (un carácter, una clase o un grupo). Son los mecanismos para expresar repetición.

### 🔹 Lista de cuantificadores estándar

- `*` → cero o más veces (equivalente a `{0,}`)
- `+` → una o más veces (`{1,}`)
- `?` → cero o una vez (`{0,1}`)
- `{n}` → exactamente `n` veces
- `{n,}` → `n` o más veces
- `{n,m}` → entre `n` y `m` veces inclusive

### 🔹 Ejemplos básicos

```regex
a*      -> "", "a", "aa", "aaa"...
a+      -> "a", "aa", "aaa"... (pero no "")
a?      -> "" o "a"
a{3}    -> "aaa"
a{2,4}  -> "aa", "aaa", "aaaa"
```

---

## 📌 Modo por defecto: Codicioso (Greedy)

Todos los cuantificadores son codiciosos por defecto. Esto significa que intentan consumir la mayor cantidad posible de caracteres sin impedir que la expresión completa tenga éxito.

Por ejemplo, con la regex `.*` sobre el texto `"abc def ghi"`, el motor:

1. Empieza en la posición 0.
2. `.*` consume todos los caracteres hasta el final de la cadena.
3. Luego intenta continuar con el resto del patrón (si lo hubiera). Si falla, retrocede (**backtrack**) cediendo caracteres de derecha a izquierda hasta que el patrón global coincida.

### 🔹 Ejemplo clásico

```regex
a.*b
```

**Texto:** `"aabab"`

- **Proceso greedy:**
    1. `a` coincide con el primer carácter 'a'.
    2. `.*` consume el resto: `"abab"`.
    3. Intenta casar `b` al final, pero la cadena se acabó.
    4. **Backtrack:** `.*` cede el último `b`, ahora `.*` = `"aba"`, queda `b` al final. `b` coincide con ese `b` final.
    5. **Coincidencia total:** `"aabab"`.

> [!NOTE]
> Observa cómo tomó la máxima porción antes de retroceder. El resultado es la coincidencia más larga posible que satisface todo el patrón.

### 🔹 Otro ejemplo con `.+`

```regex
".+"
```

Sobre `"primero" y "segundo"`:
- **Greedy** `.+` consume desde la primera comilla hasta la última comilla, resultando en `"primero" y "segundo"`. Normalmente no es lo deseado; queremos la primera frase entrecomillada.

---

## 📌 Modo Perezoso (Lazy)

Al añadir un signo `?` después del cuantificador, se vuelve perezoso. El cuantificador perezoso intenta consumir la menor cantidad posible de caracteres para que el patrón global tenga éxito.

### 🔹 Lista de cuantificadores perezosos

- `*?` → cero o más, lo mínimo
- `+?` → una o más, lo mínimo
- `??` → cero o una, prefiere cero
- `{n,}?` → `n` o más, lo mínimo
- `{n,m}?` → entre `n` y `m`, el menor número

### 🔹 Mecanismo

El motor expande el cuantificador perezoso paso a paso: primero intenta con cero repeticiones (o la mínima), y si el resto del patrón falla, expande una repetición y lo vuelve a intentar, hasta lograr la coincidencia global o agotar las posibilidades.

### 🔹 Ejemplo (mismo caso anterior)

```regex
a.*?b
```

**Texto:** `"aabab"`

- **Primera coincidencia:**
    1. `a` coincide con el primer 'a' en la posición 0.
    2. `.*?` intenta coincidir con la mínima: cero caracteres. Ahora el cursor está justo después de ese 'a', queda `"abab"`.
    3. Intenta casar `b` con el siguiente carácter, que es 'a', falla.
    4. `.*?` se expande una vez: consume 'a'. Tenemos `"aa"` consumido (`a.*?` = `aa`). Restante: `"bab"`.
    5. Intenta `b` con el siguiente carácter: 'b' en `"bab"`, éxito.
- **Coincidencia:** `"aab"`. El motor devuelve `"aab"`, la coincidencia más corta posible.

> [!TIP]
> Si usamos la flag global, la siguiente coincidencia empezaría después: sobre `"ab"` encontraría `"ab"`.

### 🔹 Ejemplo para `.+?` en `"primero" y "segundo"`

```regex
".+?"
```

Coincide con `"primero"` (la primera comilla y la mínima cantidad de caracteres hasta la siguiente comilla). Así extraemos frases entrecomilladas individualmente.

---

## 📌 Comparativa de comportamiento

**Texto:** `<p>Hola</p> <p>Mundo</p>`

| Tipo | Regex | Coincidencia |
| :--- | :--- | :--- |
| **Greedy** | `<.*>` | `<p>Hola</p> <p>Mundo</p>` (todo, desde el primer `<` hasta el último `>`). |
| **Lazy** | `<.*?>` | `<p>`, luego `</p>`, luego `<p>`, luego `</p>`. Ideal para capturar etiquetas individuales. |

### 🔹 ¿Cuándo usar cada uno?

- **Greedy:** cuando queremos consumir todo hasta la última ocurrencia de un delimitador. Ejemplo: `^.*:` encontrará todo hasta el último `:` de la línea.
- **Lazy:** cuando queremos detenernos en la primera ocurrencia. Ejemplo: extraer contenido entre paréntesis: `\(.*?\)`.

---

## 📌 Riesgos del backtracking excesivo

Los cuantificadores anidados o combinados pueden llevar a un **backtracking catastrófico** si la cadena no coincide.

Ejemplo clásico: `(a+)+b` con entrada `"aaaaaaaaaaaaaaaaaaaaaaaaaaaaac"`. El motor explora combinaciones exponenciales. Los cuantificadores perezosos también pueden sufrir backtracking, aunque a veces reducen el problema.

> [!WARNING]
> La solución definitiva para estos casos son los **cuantificadores posesivos** o los **grupos atómicos**.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Clases de caracteres](../01_fundamentos/05_clases_de_caracteres.md) | [Índice](../README.md) | [Cuantificadores Posesivos](02_posesivos.md) |

