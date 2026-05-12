Allure Framework

Allure es un framework de reportes flexible y multi-lenguaje que se integra con la mayoría de los runners de pruebas (JUnit5, TestNG, pytest, Cucumber, Mocha, etc.). Genera un informe web rico en información, con gráficos de tendencias, línea de tiempo, severidad, pasos anidados y adjuntos.

Arquitectura de Allure

    Adaptadores (bindings): Durante la ejecución de las pruebas, una librería específica del lenguaje escribe resultados crudos en formato JSON (allure-results). Por ejemplo, en Java con allure-junit5 o allure-testng, en Python con allure-pytest.

    Generador de reportes: Una herramienta de línea de comandos (allure) o un plugin de Maven/Gradle toma los resultados JSON y los transforma en un sitio HTML estático (allure-report). Este HTML puede servirse localmente (allure open) o publicarse en un servidor web.

Integración con pruebas

    Java + TestNG con Allure:
    Agregar dependencia io.qameta.allure:allure-testng y anotar métodos de prueba o usar steps programáticos.
    java

    @Test
    @Feature("Login")
    @Story("US-123 Login exitoso")
    @Severity(SeverityLevel.CRITICAL)
    public void testLoginCorrecto() {
        Allure.step("Abrir página de login", () -> loginPage.open());
        Allure.step("Ingresar credenciales", () -> {
            loginPage.typeUsername("admin");
            loginPage.typePassword("pass");
        });
        Allure.step("Hacer clic en Login", () -> loginPage.clickLogin());
        Allure.step("Verificar bienvenida", () -> {
            assertEquals("Bienvenido", homePage.getWelcomeMessage());
        });
        // Adjuntar evidencia
        Allure.addAttachment("Captura de pantalla", new ByteArrayInputStream(screenshot));
    }

        @Feature, @Story: Agrupan pruebas en epics e historias.

        @Severity: para priorizar la revisión de fallos (Blocker, Critical, Normal, Minor, Trivial).

        Allure.step(description, lambda): crea un paso dentro del test. Si falla, muestra exactamente en qué paso ocurrió.

    Python + pytest:
    Instalar allure-pytest y ejecutar: pytest --alluredir=./allure-results.
    Las aserciones se capturan automáticamente. Se pueden añadir steps mediante allure.step('...') y adjuntos con allure.attach(body, name, attachment_type).
    python

    import allure
    def test_registro():
        with allure.step("Navegar a registro"):
            login.go_to_registration()
        with allure.step("Llenar formulario"):
            registration.fill_email("test@test.com")
        with allure.step("Enviar"):
            registration.submit()
        # Adjunto de respuesta API
        allure.attach(response.text, "Respuesta", allure.attachment_type.JSON)

    Integración con Cucumber: usando allure-cucumber-jvm, los escenarios y sus pasos se reflejan automáticamente. Se pueden añadir @Severity, @Feature en los features/escenarios.

Generación del reporte en CI/CD

    Maven: mvn io.qameta.allure:allure-maven:report (la carpeta allure-results debe existir).

    CLI: allure generate allure-results --clean -o allure-report y luego allure open allure-report.

    Jenkins: usando el plugin Allure Jenkins Plugin. Después de ejecutar las pruebas, se archiva la carpeta allure-results y el plugin genera el reporte automáticamente, mostrando la tendencia histórica en la página del trabajo.

    GitHub Actions: se puede usar peaceiris/actions-gh-pages para publicar allure-report en GitHub Pages después de la ejecución:
    yaml

    - name: Generate report
      uses: simple-elf/allure-report-action@v1
      with:
        allure_results: allure-results
        allure_history: allure-history
    - name: Deploy report
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: allure-history

Características avanzadas:

    Retries: Las repeticiones de test (flaky tests) se agrupan correctamente; Allure muestra el historial de ejecuciones del mismo caso en el reporte.

    Entornos: Se puede inyectar información del entorno (URL, sistema operativo) con -Denvironment o creando un archivo environment.properties en allure-results.

    Línea de tiempo: Muestra visualmente la ejecución concurrente de pruebas, útil para identificar cuellos de botella en paralelismo.

    Integración con sistemas de ticketing: los links de @Issue, @TmsLink permiten enlazar el reporte con Jira, TestRail.

Para el SDET: Allure proporciona un solo lugar para inspeccionar todas las ejecuciones, habilitando un análisis rápido de regresiones y facilitando la comunicación con negocio.