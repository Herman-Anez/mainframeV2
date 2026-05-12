# 📁 Cuantificadores: Posesivos

## 📌 Definición y sintaxis

Los cuantificadores posesivos son una extensión presente en algunos motores (PCRE, Java, .NET, Perl, módulo `regex` de Python). Se forman añadiendo un `+` después del cuantificador normal.

### 🔹 Lista de cuantificadores posesivos

- `*+` → cero o más, posesivo
- `++` → una o más, posesivo
- `?+` → cero o una, posesivo
- `{n,}+` → `n` o más, posesivo
- `{n,m}+` → entre `n` y `m`, posesivo

---

## 📌 Comportamiento

Un cuantificador posesivo consume la máxima cantidad posible de caracteres, igual que el greedy, pero con una diferencia crucial: **nunca retrocede (backtrack)**. Una vez que toma una porción, no la devuelve aunque eso impida que el resto del patrón coincida.

Esto significa que si el resto de la expresión falla, el motor no intentará ceder caracteres del cuantificador posesivo; simplemente fallará esa rama de la búsqueda y continuará probando desde otras posiciones (backtrack global), pero sin reajustar el interior del cuantificador.

### 🔹 Ejemplo: `a++b`

**Sobre `"aaaab"`:**
1. `a++` consume todas las as (4 as).
2. Luego intenta coincidir `b`, pero el carácter siguiente es `b` → éxito, coincide `"aaaab"`.

**Sobre `"aaaa"`:**
1. `a++` come todas las as (4 as).
2. Luego intenta `b`, pero no hay más caracteres. Como el cuantificador es posesivo, no retrocede para ceder as.
3. **Fallo global inmediato.**

> [!NOTE]
> Con un greedy normal `a+b`, el motor cedería una `a`, probaría `b`, cedería otra, etc., generando backtracking que finalmente falla igual, pero con un coste computacional mucho mayor.

---

## 📌 Ventajas

1. **Eficiencia y prevención de backtracking catastrófico:** Al eliminar estados de retroceso interiores, se reduce drásticamente el número de intentos. Es una herramienta de optimización.
2. **Seguridad:** En patrones complejos donde sabemos que no queremos que el cuantificador ceda, el posesivo garantiza que no habrá retroceso, evitando bucles infinitos o cuellos de botella.

### 🔹 Caso de uso típico: cuantificadores anidados

El patrón `(?:a+)*b` sobre `"aaaaaaaaaaaaaaac"` sufre backtracking exponencial. Si usamos un grupo atómico o cuantificadores posesivos en el interior `(?:a++)*b` (o `(?>a+)*b`), el motor falla mucho más rápido porque no retrocede dentro de `a+` para intentar distribuciones alternativas.

---

## 📌 Soporte en motores

| Motor | Soporte | Observaciones |
| :--- | :---: | :--- |
| **PCRE / PHP** | ✅ | Soportado nativamente (`*+`, `++`, etc.). |
| **Perl / Java / .NET** | ✅ | Soportado nativamente. |
| **Python (re)** | ❌ | El módulo `re` estándar **NO** lo soporta. |
| **Python (regex)** | ✅ | El módulo externo `regex` (PyPI) sí los soporta. |
| **JavaScript** | ❌ | No hay sintaxis disponible nativamente. |

---

## 📌 Simulación en motores que no los soportan

Si necesitas un comportamiento posesivo en JS o Python `re`, puedes usar un grupo atómico (si está disponible) o una construcción de lookahead:

Para `a++b` sin posesivo, la equivalencia sería `(?=a+)\1b`, pero solo en motores con retroreferencias.

> [!TIP]
> En JavaScript, un truco para simular `a++b` podría ser `(?=(a+))\1b`. El lookahead captura las as y la retroreferencia las consume sin posibilidad de retroceder en el grupo externo, imitando parcialmente el comportamiento posesivo.

---

## 📌 Precauciones

Los cuantificadores posesivos pueden cambiar la semántica. Si la coincidencia global podría lograrse cediendo caracteres del cuantificador, un posesivo lo impedirá. Solo deben usarse cuando sabemos que no se necesita tal cesión.

**Ejemplo de patrón inadecuado:**
`".*+"` nunca coincidiría con `"hola"` porque `.*+` consumiría todo hasta el final, incluyendo la comilla de cierre, y luego no podría retroceder para que la comilla final case. Mientras que el greedy `".*"` sí lo haría.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Greedy vs Lazy](01_greedy_lazy.md) | [Índice](../README.md) | [Ejemplos Prácticos](03_ejemplos_practicos.md) |

