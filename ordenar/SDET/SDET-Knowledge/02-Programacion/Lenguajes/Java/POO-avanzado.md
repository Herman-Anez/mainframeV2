# POO avanzado para SDET

La programación orientada a objetos es la columna vertebral de frameworks como Selenium con *Page Object Model*, pero se necesita un nivel avanzado:

## Conceptos avanzados

*   **Herencia**: Se puede usar para crear una clase base `BasePage` que contenga métodos comunes como `waitForElement`, `scrollIntoView`, `jsClick`. Luego cada página hereda de ella.
    > [!WARNING]
    > La herencia profunda acopla el código; los SDETs modernos prefieren composición sobre herencia.
*   **Composición y delegación**: En lugar de heredar un `BaseTest`, se inyectan comportamientos. Por ejemplo, en un proyecto Screenplay, un actor tiene la capacidad `BrowseTheWeb` que contiene el `WebDriver`, no se hereda.
*   **Polimorfismo**: Permite escribir métodos que aceptan diferentes tipos de elementos de UI. En lugar de sobrecargar docenas de `waitForElement`, se usa una interfaz `Element` con implementaciones para Web, Mobile, etc., y el método espera el tipo genérico.
*   **Interfaces y clases abstractas**: Las interfaces permiten definir contratos como `WebDriver` o `WebElement`. Así puedes pasar un `ChromeDriver` o un `RemoteWebDriver` sin cambiar el código. Los frameworks de testing definen interfaces para reportes (`TestReporter`), gestión de logs, etc.
*   **Clases internas y estáticas**: Útiles para *builders* de datos de prueba.
    ```java
    User user = User.builder().name("Juan").age(25).build();
    ```
*   **Principio de sustitución de Liskov**: Si una clase `DashboardPage` hereda de `AuthenticatedPage`, debe poder usarse en cualquier lugar donde se espere `AuthenticatedPage` sin romper el comportamiento. Esto obliga a que las páginas no tengan aserciones ocultas que limiten su reutilización.

---

| Anterior | Inicio | Siguiente |
| :------- | :----: | :-------- |
| ⏪ [Sintaxis básica](Sintaxis-basica.md) | [Índice](index.md) | [Manejo de excepciones](Manejo-excepciones.md) ⏩ |
