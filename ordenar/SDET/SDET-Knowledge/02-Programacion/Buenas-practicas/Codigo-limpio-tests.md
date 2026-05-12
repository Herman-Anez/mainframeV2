# Código limpio en tests

Un test automatizado es documentación viva. Debe ser autoexplicativo, pequeño y centrado.

## Principios fundamentales

*   **Nombrado expresivo**: El nombre de la prueba debe describir el escenario, el resultado esperado y a veces las condiciones. Patrones: `test[Metodo][Estado][Comportamiento]`. Ejemplo: `testLoginWithIncorrectPasswordReturns401`. En Cucumber, los escenarios describen la intención del negocio.
*   **Estructura AAA (Arrange, Act, Assert)**: Separar claramente preparación, acción y verificación. A veces se añade un paso Act compuesto. Un test de 10 líneas con AAA es más fácil de depurar que uno de 30 con lógica enredada.
*   **Principio DAMP (Descriptive And Meaningful Phrases) vs DRY**: En testing, no es obligatorio eliminar toda duplicación si eso perjudica la legibilidad. Es preferible repetir un par de líneas de setup si cada prueba mantiene su propia claridad. La abstracción prematura genera confusión. Se busca equilibrio: usar fixtures, builders y métodos helper para las preparaciones complejas, pero manteniendo los tests lo suficientemente lineales.
*   **Un test, un concepto**: Cada test debe verificar un único comportamiento. Si falla, la causa es obvia. Evitar múltiples assert no relacionados. Si una prueba requiere varias aserciones, que sean sobre el mismo objeto o flujo.
*   **Evitar lógica en tests**: Los `if`, `while`, `try-catch` deben ser mínimos. Si aparece lógica condicional, probablemente falta una prueba con diferentes datos parametrizados.
*   **Constantes y datos claros**: Usar variables descriptivas en lugar de números mágicos o textos largos. Ejemplo: `final String MENSAJE_ERROR = "Usuario no encontrado";` y luego `assertThat(errorMessage, is(MENSAJE_ERROR));`.
*   **Comentarios**: Los tests deben ser tan legibles que no necesiten comentarios. Si un comentario es necesario para explicar por qué se hace algo extraño, es aceptable. No comentar lo obvio.

---

| Anterior | Inicio | Siguiente |
| :------- | :----: | :-------- |
| ⏪ [Buenas prácticas](index.md) | [Índice](index.md) | [SOLID en testing](SOLID-para-testing.md) ⏩ |
