# Sintaxis básica enfocada a testing

## Conceptos clave

*   **Tipos de datos y variables**: Es esencial distinguir entre `int`, `String`, `boolean`, `List`, `Map` porque en testing se usan intensivamente para datos de prueba. Usar genéricos evita casteos.
    *   *Ejemplo al verificar el cuerpo de una API:*
        ```java
        Map<String, Object> response = RestAssured.get("/user/1").jsonPath().getMap("$");
        String name = (String) response.get("name");
        ```
*   **Estructuras de control**: `if-else`, `switch`, bucles `for` y `while`. En testing se usan menos bloques `if` que en desarrollo; se prefiere que los casos de prueba sigan un flujo lineal. Pero los bucles son fundamentales para pruebas *data-driven* con `@DataProvider` de TestNG o `@CsvSource`, `@MethodSource` de JUnit 5.
*   **Métodos y clases**: Un SDET escribe métodos que representan acciones (*login*, añadir al carrito) o verificaciones (comprobar total). Acostumbra a usar modificadores de acceso; los métodos de utilidades de pruebas suelen ser `public static` para ser reusables entre tests.
*   **Colecciones**: `ArrayList`, `HashMap`, `HashSet` son indispensables. Por ejemplo, al comparar dos listas de productos esperados y obtenidos de la UI o API, se usan operaciones como `assertThat(list, containsInAnyOrder(...))` con Hamcrest.
*   **Manejo de fechas/horas**: `java.time` (`LocalDate`, `LocalDateTime`) para evitar problemas de compatibilidad. Las pruebas deben manejar zonas horarias, formatos y aserciones con tolerancias.

---

| Anterior | Inicio | Siguiente |
| :------- | :----: | :-------- |
| ⏪ [Java para SDET](index.md) | [Índice](index.md) | [POO Avanzado](POO-avanzado.md) ⏩ |
