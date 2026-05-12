# SOLID aplicado al código de testing

Los cinco principios SOLID se pueden reinterpretar para el diseño de pruebas y frameworks de automatización.

## Los cinco principios

*   **S – Single Responsibility (Responsabilidad única)**: Cada clase de prueba o suite debe tener un motivo para cambiar. No mezclar pruebas de login con pruebas de reportes en la misma clase. A nivel de framework, una clase PageObject solo debe representar la página y sus elementos, no contener lógica de negocio compleja (eso va en tareas Screenplay).
*   **O – Open/Closed (Abierto para extensión, cerrado para modificación)**: Un framework debe permitir añadir nuevas páginas, componentes o drivers sin modificar las clases existentes. Se logra con herencia (`BasePage`), pero mejor aún con composición y plugins. Por ejemplo, añadir un nuevo tipo de reporte (Reporte en PDF) implementando una interfaz `TestReporter` sin tocar el código que ejecuta pruebas.
*   **L – Liskov Substitution (Sustitución de Liskov)**: Las subclases deben poder reemplazar a sus clases base sin alterar la corrección. En Page Objects: si `CheckoutPage` hereda de `CartPage`, debe poder usarse en cualquier lugar donde se espera `CartPage`. Eso implica no lanzar excepciones inesperadas ni cambiar contratos. A menudo se viola al heredar y redefinir métodos dejando vacíos los heredados; mejor usar composición.
*   **I – Interface Segregation (Segregación de interfaces)**: No forzar a un cliente a depender de métodos que no usa. En el contexto de un actor (Screenplay), define habilidades pequeñas: `BrowseTheWeb`, `ConsumeAPI`, `AccessDatabase`. Un actor que solo necesita la web no debe depender de métodos de base de datos.
*   **D – Dependency Inversion (Inversión de dependencias)**: Los módulos de alto nivel (tests) no deben depender de módulos de bajo nivel (implementaciones concretas de `WebDriver`, `database driver`). Ambos deben depender de abstracciones. Por eso se inyecta un `WebDriver` o `DriverFactory` como parámetro, en vez de instanciarlo dentro del test. Esto permite cambiar fácilmente el navegador, entorno y ejecución local vs remota.

> [!TIP]
> Aplicar SOLID evita que un proyecto de automatización se convierta en un monolito inmantenible tras un año de crecimiento.

---

| Anterior | Inicio | Siguiente |
| :------- | :----: | :-------- |
| ⏪ [Código limpio](Codigo-limpio-tests.md) | [Índice](index.md) | [Patrones de diseño](../Patrones-diseno/index.md) ⏩ |
