# Recursión y Subrutinas

La recursión permite que un patrón se llame a sí mismo, de forma similar a una función recursiva en programación. Esto habilita el emparejamiento de estructuras anidadas arbitrariamente, como paréntesis balanceados, etiquetas HTML anidadas o bloques de código, algo imposible con expresiones regulares clásicas (que solo reconocen lenguajes regulares). La recursión es una extensión presente en PCRE, Perl y el módulo regex de Python.

## Sintaxis de recursión

*   **`(?R)` o `(?0)`**: llama recursivamente al patrón completo.
*   **`(?1)`, `(?2)`, etc.**: llama al patrón del grupo de captura número 1, 2, etc.
*   **`(?&nombre)`**: llama al patrón del grupo con nombre (subrutina, similar a re-ejecutar el subpatrón).
*   **`(?P>nombre)`**: sintaxis alternativa en Python (regex).

> [!NOTE]
> No confundir con las retroreferencias: una retroreferencia (`\1`) exige que el texto coincida exactamente con la captura previa. La recursión/subrutina re-ejecuta el patrón del grupo, permitiendo nueva coincidencia con estructura pero no forzando igualdad literal.

## Ejemplo: paréntesis balanceados con `(?R)`

Patrón para validar y capturar contenido entre paréntesis con anidamiento ilimitado:

```regex
\( (?: [^()]++ | (?R) )* \)
```

*   `\(` y `\)` delimitan el bloque.
*   `[^()]++` consume uno o más caracteres que no son paréntesis (cuantificador posesivo para eficiencia).
*   `| (?R)` recursivamente aplica todo el patrón de nuevo cuando encuentra otro paréntesis anidado.
*   `(?: ... )*` repite la alternancia cero o más veces.

**Aplicado sobre `"(a (b) c)"`:**
Encuentra `(a (b) c)`, capturando todo correctamente. La recursión maneja `(b)` internamente.

## Recursión a grupos específicos

Si solo queremos repetir un subpatrón sin recursión completa:

```regex
(?<word>\w+) \s+ (?&word)
```

Busca una palabra, espacio, y la misma palabra después (similar a una retroreferencia, pero sin capturar previamente: aquí `(?&word)` re-ejecuta `\w+`, no fuerza igualdad de texto). Para forzar igualdad usaríamos `\k<word>` (retroreferencia), no `(?&word)`.

Para forzar igual estructura: `(?<tag>h[1-6])>.*?</(?&tag)>` casaría con `<h1>...</h1>` pero también con `<h1>...</h2>` si no usamos retroreferencia. La recursión sola no impone igualdad de texto, solo re-aplica el patrón. Para igualdad combinar con retroreferencia o capturar antes y comparar.

## Subrutinas (recursión a grupos)

Una subrutina es una llamada a un grupo con nombre que ya ha aparecido antes (o después) en el patrón. Es como un "subprograma" de regex.

```regex
(?<number>\d+(?:\.\d+)?) \s+ (?&number)
```

Coincide con un número, espacio, y otro número con el mismo formato (pero posibles valores diferentes). Si queremos mismo valor: `(?<n>\d+.\d+)\s+\k<n>`.

### Ejemplo complejo: etiquetas HTML emparejadas (contexto simple)

```regex
<(?<tag>[a-z]+)>
  (?: [^<]++ | (?R) )*
</\k<tag>>
```

1.  Captura el nombre de etiqueta en `tag`.
2.  Contenido: caracteres que no son `<` o recursión completa (para etiquetas anidadas).
3.  Cierre con retroreferencia `\k<tag>` para asegurar misma etiqueta.

## Soporte en motores

*   **PCRE (PHP, Apache):** `(?R)`, `(?1)`, `(?&name)` completamente soportados.
*   **Perl:** `(?R)`, `(?1)`, `(?&name)` (moderno).
*   **Python regex:** soporta `(?R)`, `(?0)`, `(?1)`, `(?&name)`. El módulo estándar `re` no.
*   **Java, .NET, JavaScript:** no soportan recursión nativa. .NET usa grupos balanceados como alternativa. JavaScript no tiene alternativa directa.

## Consideraciones importantes

> [!WARNING]
> *   **Profundidad y stack:** la recursión consume pila; niveles muy profundos pueden causar error de stack overflow.
> *   **Rendimiento:** la recursión es potente pero puede ser lenta en estructuras grandes. Combinar con posesivos y grupos atómicos mejora.
> *   **No es mágica:** no cubre todos los casos de parseo (por ejemplo, HTML arbitrario requiere un parser real). Útil para formatos con anidamiento conocido.

## Equivalencia sin recursión (grupos balanceados .NET)

En .NET, los grupos balanceados sustituyen la recursión con una pila explícita (ver sección .NET en motores). La idea es contar aperturas/cierres sin necesidad de llamada recursiva.

---

### 📖 Temas relacionados
| Archivo | Descripción |
| :--- | :--- |
| [02_condicionales.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/07_temas_avanzados/02_condicionales.md) | Uso de lógica condicional en patrones |
| [04_backtracking_catastrofico.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/07_temas_avanzados/04_backtracking_catastrofico.md) | Riesgos de rendimiento y cómo evitarlos |
| [06_motores_y_dialectos](../06_motores_y_dialectos/01_comparativa_general.md) | Soporte según el lenguaje |


---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| ➖ | [🏠 Inicio](../../README.md) | [Condicionales ▶](02_condicionales.md) |
