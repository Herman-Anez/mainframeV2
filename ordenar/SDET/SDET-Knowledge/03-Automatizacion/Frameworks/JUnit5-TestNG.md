# JUnit 5 vs. TestNG

Ambos son los estándares en Java para pruebas, con características que se trasladan a Python (`pytest`) o C# (`NUnit`/`xUnit`). El SDET debe conocer ambos y elegir según el proyecto.

## JUnit 5 (Jupiter)

- **Arquitectura Modular**: Platform (lanzador), Jupiter (API) y Vintage (soporte JUnit 4).
- **Anotaciones Principales**: `@Test`, `@BeforeEach`/`@AfterEach`, `@BeforeAll`/`@AfterAll`.
- **Parametrización**: Mediante `@ParameterizedTest` con `@ValueSource`, `@CsvSource`, `@MethodSource`. Muy potente y extensible.
- **Extensiones**: Mecanismo que reemplaza a los *Runners* y *Rules* de JUnit 4; permite ganchos en el ciclo de vida (instanciación, parámetros, interceptores).
- **Ejecución Paralela**: Configurable vía `junit-platform.properties`. Permite combinar con `@Execution(ExecutionMode.CONCURRENT)`.
- **Assertions**: `assertEquals`, `assertThrows`, `assertAll` (ejecuta todas las aserciones y reporta fallos juntos).

## TestNG

- **Filosofía**: Inspirado en JUnit pero con características avanzadas nativas desde el inicio.
- **Ciclo de Vida**: Jerárquico (`suite` > `test` > `class` > `method`). Anotaciones como `@BeforeSuite`, `@AfterSuite`, `@BeforeMethod`, etc.
- **Paralelismo Nativo**: Configurable en `testng.xml` (`parallel="methods/tests/classes"`) con gestión de pools de hilos.
- **DataProvider**: Método que devuelve un array de datos (`Object[][]`) y se asigna con `@Test(dataProvider = "dp")`. Permite inyección de `ITestContext`.
- **Dependencias**: Métodos con `groups`, `dependsOnMethods`, `priority`.
- **Reportes**: Incluye reportes HTML básicos, con fácil integración con Allure o ExtentReports.

## Comparativa para SDET

| Criterio | JUnit 5 | TestNG |
| :--- | :--- | :--- |
| **Modernidad** | Alta (Modular, Extensiones) | Media (Más antiguo) |
| **Paralelismo** | Configuración externa | Configuración en XML nativa |
| **Data Driven** | Basado en anotaciones | `@DataProvider` (Muy flexible) |
| **Dependencias** | No recomendado | Soportado nativamente |

> [!TIP]
> **Elección**: Para proyectos nuevos se prefiere **JUnit 5** por su extensibilidad. **TestNG** es ideal cuando se requiere un manejo complejo de paralelismo o dependencias entre tests.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Frameworks Index](./index.md) | [Home](../../index.md) | [Cucumber & BDD](./Cucumber-BDD.md) |


