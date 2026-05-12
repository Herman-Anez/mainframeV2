# Backtracking Catastrófico

En los motores de regex basados en NFA (la mayoría: Perl, PCRE, Java, Python, .NET, JS), el **backtracking** es el mecanismo que permite al motor retroceder e intentar nuevas combinaciones cuando una parte del patrón falla. Aunque es flexible, si no se controla, puede degenerar en una explosión combinatoria.

## El problema: Backtracking catastrófico

Ocurre cuando un patrón requiere un número astronómico de pasos de retroceso para determinar que no hay coincidencia, creciendo de forma exponencial con la longitud de la entrada. Esto puede causar que la aplicación se congele, consuma toda la CPU o reciba un timeout (ataque ReDoS).

> [!WARNING]
> El ejemplo clásico es `(a+)+b` aplicado a una cadena larga de "as" sin una "b" al final, como `"aaaaaaaaaaaaaaaaaaaaX"`.

### Análisis detallado del ejemplo `(a+)+b`

1.  `(a+)+` significa uno o más grupos de una o más "as".
2.  Para una cadena `"aaaa"`:
    *   El primer `a+` puede tomar 4 "as", y el cuantificador externo `+` permite repetir ese grupo 1 vez. Luego espera `b`.
    *   Si `b` no existe, el motor hace backtrack: el `+` externo cede caracteres y el `a+` interno los redistribuye.
3.  **Explosión combinatoria:** Existen múltiples formas de particionar las "as" en grupos (ej. 4 grupos de 1, 2+2, 1+1+2, etc.). El motor probará **todas** las combinaciones posibles antes de fallar.

*   Con 10 "as", el número de combinaciones es ~512.
*   Con 20 "as", ya son cientos de miles.
*   Con 30 "as", puede superar los mil millones de pasos.

## Otros patrones problemáticos comunes

*   `(a|aa)+b`: Explosión similar por alternancia redundante.
*   `.*.*=.*`: Múltiples puntos greedys anidados pueden disparar backtracking masivo.
*   `[^,]*,[^,]*,[^,]*`: Con entrada que tiene menos comas de las esperadas.
*   `(".*?"|'.*?')`: Cuando hay muchas comillas en el texto y no hay coincidencia rápida.

## Cómo identificarlos

> [!IMPORTANT]
> **Síntomas de peligro:**
> *   Regex extremadamente lentas con ciertas entradas (incluso cortas).
> *   Falla con timeout en validadores online o entornos de producción.
> *   Presencia de **cuantificadores anidados**: `(...+)+`, `(...*)*`, `(.+?)` dentro de grupos repetitivos.

### Herramientas de diagnóstico
*   **regex101.com**: El panel "debugger" muestra el número exacto de pasos. Si supera los 1000 pasos para una entrada simple, el patrón es sospechoso.

## Estrategias para prevenir y solucionar

1.  **Cuantificadores posesivos (`++`, `*+`, `?+`, `{n,m}+`):** Eliminan el backtracking dentro del cuantificador. Una vez que coinciden, no ceden caracteres.
    ```regex
    (a++)+b  # En "aaaaX" falla inmediatamente sin intentar combinaciones
    ```
2.  **Grupos atómicos (`(?>…)`):** Igual que los posesivos, pero aplicados a un grupo complejo.
    ```regex
    (?>a+)+b
    ```
3.  **Reescribir el patrón:** Eliminar anidamiento innecesario. Usar `a+b` en lugar de `(a+)+b`.
4.  **Clases negadas:** Usar `[^"]*` en lugar de `.*?` para contenido entre comillas.
5.  **Limitar cuantificadores:** Usar `{1,100}` en lugar de `+` cuando sea posible.
6.  **Anclas:** Usar `^` y `$` para forzar fallos tempranos.

## Impacto en entornos de producción

> [!CAUTION]
> Un servidor que valida entradas de usuario con una regex vulnerable puede ser blanco de un ataque **ReDoS** (Regular expression Denial of Service).
>
> En aplicaciones críticas, se deben evitar patrones complejos no acotados o usar motores de tiempo lineal como **RE2** o **Hyperscan**.

## Ejemplo práctico: Extracción de campos CSV

*   **Inseguro:** `(?:[^;]*;)+` (vulnerable si la entrada es larga y no termina en `;`).
*   **Seguro:** `[^;]*+(?:;[^;]*+)*+` (usando posesivos) o simplemente usar la función `split()` del lenguaje.

## Conclusión

El conocimiento del backtracking catastrófico es vital para la seguridad. Ante patrones complejos, siempre se debe considerar el peor escenario de entrada y utilizar herramientas de optimización para garantizar un rendimiento predecible.

---

### 📖 Temas relacionados
| Archivo | Descripción |
| :--- | :--- |
| [05_optimizacion.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/07_temas_avanzados/05_optimizacion.md) | Técnicas avanzadas de rendimiento |
| [01_recursion_y_subrutinas.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/07_temas_avanzados/01_recursion_y_subrutinas.md) | Complejidad en patrones recursivos |
| [06_motores_y_dialectos](../06_motores_y_dialectos/01_comparativa_general.md) | Motores seguros vs NFA |


---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [◀ Propiedades Unicode](03_propiedades_unicode.md) | [🏠 Inicio](../../README.md) | [Optimizacion ▶](05_optimizacion.md) |
