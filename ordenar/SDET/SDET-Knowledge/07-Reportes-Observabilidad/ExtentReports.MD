ExtentReports

ExtentReports (de AventStack) es una librería de reportes completamente implementada en Java/.NET/Node.js que genera un dashboard HTML rico, sin necesidad de una herramienta externa de generación. Ofrece control total desde el código de pruebas, permitiendo al SDET personalizar el reporte y adjuntar información en tiempo de ejecución.

Concepto fundamental
A diferencia de Allure (que procesa JSON post-ejecución), ExtentReports escribe el reporte HTML directamente mientras las pruebas se ejecutan, lo que lo hace muy sencillo de integrar pero limita el post-procesamiento. Cada evento (inicio de test, paso, log, captura) se registra mediante la API de Extent.

Configuración con TestNG y Selenium (Java)

    Dependencias: extentreports y un adaptador para el runner (se puede implementar un listener de TestNG o JUnit5).

    Crear un ExtentReports y un reporter (ej. ExtentSparkReporter).
    java

    ExtentSparkReporter spark = new ExtentSparkReporter("test-output/SparkReport.html");
    spark.config().setTheme(Theme.STANDARD);
    spark.config().setDocumentTitle("Suite de Regresión");
    spark.config().setReportName("API + UI Tests");

    ExtentReports extent = new ExtentReports();
    extent.attachReporter(spark);
    extent.setSystemInfo("Entorno", "Staging");
    extent.setSystemInfo("SO", System.getProperty("os.name"));

    Usar ExtentTest para cada caso de prueba, asignando categorías, autores, dispositivos.
    java

    @Test
    public void loginTest() {
        ExtentTest test = extent.createTest("Login con usuario válido")
                .assignCategory("Regresión")
                .assignAuthor("SDET Team");
        test.info("Iniciando prueba de login");
        try {
            loginPage.login("user", "pass");
            Assert.assertEquals(driver.getTitle(), "Dashboard");
            test.pass("Login exitoso");
            test.addScreenCaptureFromPath(captura);
        } catch (AssertionError e) {
            test.fail("Fallo en login: " + e.getMessage());
            test.addScreenCaptureFromPath(captura);
            throw e;
        }
    }

    Al final de la suite: extent.flush(); (escribe el HTML a disco).

Integración vía Listeners (más limpio)

    Con TestNG se implementa ITestListener y se invocan ExtentTest en onTestStart, onTestSuccess, onTestFailure.

    Así se evita código repetitivo en cada prueba. En onTestFailure se pueden agregar capturas de pantalla automáticamente.

ExtentReports vs Allure:

    ExtentReports es totalmente autónomo; no requiere línea de comandos externa, perfecto para proyectos pequeños o donde no se puede instalar Allure. La configuración es en código y el reporte se genera al vuelo.

    Allure tiene una presentación más pulida, con timeline, categorías automáticas de defectos (producto vs test), y almacena históricos por build sin almacenar HTML completos (solo JSON, y regenera). ExtentReports guarda HTMLs independientes; para histórico se necesita un mecanismo externo (por ejemplo, subir a un servidor).

    En entornos empresariales, Allure tiende a ser preferido por su facilidad de integración en pipelines y su rica UI. ExtentReports es excelente cuando se necesita una solución rápida y se quiere control absoluto desde el código.

Adjuntos y red: ExtentReports también puede incrustar imágenes en base64, logs de red (para pruebas de API), tablas personalizadas y cualquier HTML.

Uso en otros lenguajes: Existen versiones para .NET (ExtentReports.Core), Python y Node.js, aunque en esos ecosistemas Allure o ReportPortal suelen ser más populares.