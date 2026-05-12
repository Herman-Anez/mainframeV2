JUnit 5 vs TestNG

Ambos son los estándares en Java para pruebas, con características que se trasladan a Python (pytest) o C# (NUnit/xUnit). El SDET debe conocer ambos y elegir según el proyecto.

JUnit 5 (Jupiter)

    Arquitectura modular: Platform (lanzador), Jupiter (API) y Vintage (soporte JUnit 4).

    Anotaciones principales: @Test, @BeforeEach/@AfterEach, @BeforeAll/@AfterAll (con método estático).

    Parametrización: Mediante @ParameterizedTest con @ValueSource, @CsvSource, @MethodSource. Muy potente y extensible.

    Agrupación: @Tag("smoke") y filtrado con etiquetas.

    Extensiones: Mecanismo único que reemplaza a los Runners y Rules de JUnit4; permite ganchos en test lifecycle (instanciación, parámetros, interceptors). Más limpio y modular.

    Ejecución paralela: Configurable vía junit-platform.properties: junit.jupiter.execution.parallel.enabled = true. Se puede combinar con @Execution(ExecutionMode.CONCURRENT). Selenium Grid se integra para paralelismo.

    Assertions: Assertions.assertEquals, assertThrows, assertAll (ejecuta todas las aserciones y reporta fallos juntos).

TestNG

    Inspirado en JUnit pero con características avanzadas desde el inicio: paralelismo en el modelo de test, parámetros con @DataProvider, dependencias entre métodos.

    Anotaciones: @Test, @BeforeSuite, @AfterSuite, @BeforeMethod, etc. El ciclo de vida es jerárquico (suite > test > class > method).

    Paralelismo nativo: En testng.xml se puede configurar parallel="methods" o "tests" o "classes" con thread-count. TestNG gestiona los pools de hilos.

    DataProvider: Método que devuelve un array de datos (Object[][]) y se asigna al test con @Test(dataProvider = "dp"). Permite data-driven fácil. Soporta inyección de ITestContext y paralelismo incluso dentro del data provider.

    Agrupación y prioridades: Métodos con groups, dependsOnMethods, priority. Esto puede ser útil pero también crea acoplamiento; los SDET experimentados lo usan con moderación.

    Reportes: Incluye reportes HTML por defecto, aunque se suelen integrar con ExtentReports o Allure.

Comparativa para SDET:

    Para proyectos nuevos donde se valora la filosofía moderna y la extensibilidad vía extensiones, JUnit 5 es la elección.

    TestNG es preferido cuando se necesita un potente manejo de paralelismo a nivel de método con data providers y dependencias, o cuando se migra desde sistemas heredados.

