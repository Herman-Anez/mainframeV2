El módulo 03-Automatizacion es el corazón práctico del SDET. Abarca desde la automatización de interfaces de usuario hasta la validación de contratos entre microservicios. Desgloso cada archivo con la profundidad que necesita un profesional que diseñará e implementará soluciones, no solo scripts.
Automatización UI-Web

La capa de presentación sigue siendo crítica para pruebas de extremo a extremo. Las tres herramientas aquí cubiertas resuelven el problema de formas distintas, y el SDET elige la más adecuada al contexto.
Selenium WebDriver

Selenium es el veterano estándar abierto, ampliamente integrado en múltiples lenguajes. Conocer sus fundamentos sigue siendo imprescindible.
WebDriver-basics

¿Qué es WebDriver?
Es una interfaz de control de navegadores. No es una herramienta, sino una especificación W3C que los navegadores implementan mediante drivers (chromedriver, geckodriver, etc.). El script envía comandos HTTP al driver, que los traduce en acciones sobre el navegador real.

    Arquitectura:
    text

    Código de prueba (Java, Python...) → Cliente WebDriver → Driver (ejecutable) → Navegador

    Configuración básica:
    En Java con Selenium 4:
    java

    WebDriver driver = new ChromeDriver();
    driver.get("https://example.com");
    String title = driver.getTitle();
    driver.quit();

        WebDriverManager de Boni García elimina la descarga manual de drivers.

        En Selenium 4 se añaden capacidades relativas de Actions, DevTools (Chrome DevTools Protocol) y localizadores mejorados.

    Localizadores (Selectores):
    By.id, By.name, By.className, By.tagName, By.linkText/partialLinkText, By.cssSelector, By.xpath.

        Prioridad: IDs únicos > selectores CSS robustos > XPaths fiables (evitar XPaths absolutos).

        XPath posee funciones como contains(), starts-with(), ejes (following-sibling) útiles en estructuras complejas, pero más lentos que CSS.

    Gestión del navegador:
    driver.manage().window().maximize();
    driver.navigate().back()/forward()/refresh();
    driver.switchTo().frame() / alert() / window(handle).

    Cierre y ciclo de vida: driver.close() cierra la pestaña actual y driver.quit() cierra todas y finaliza el driver. En pruebas siempre usar quit() al finalizar.

Waits-esperas

Las esperas son el mecanismo más crítico para evitar flaky tests. Selenium ejecuta comandos tan rápido como el código; si la UI no ha cargado el elemento, lanza NoSuchElementException.

    Esperas implícitas:
    driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
    Se configura una sola vez y aplica a todas las búsquedas de elementos. Si el driver no encuentra el elemento de inmediato, espera un tiempo máximo antes de lanzar la excepción.

        Desventaja: No es flexible; a veces se necesita esperar a que un elemento sea clickable o visible, no solo a que exista en el DOM. Combinar implícitas con explícitas puede causar comportamientos extraños.

    Esperas explícitas (la práctica recomendada por Selenium):
    Con WebDriverWait y ExpectedConditions se espera una condición concreta con un timeout dado.
    java

    WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    WebElement element = wait.until(ExpectedConditions.elementToBeClickable(By.id("submit")));
    element.click();

        Condiciones predefinidas: visibilityOf, presenceOfElementLocated, invisibilityOf, textToBe, etc.

        Permite ignorar excepciones específicas durante la espera.

        Son dinámicas: si la condición se cumple antes, la ejecución continúa.

    Esperas fluidas (FluentWait):
    Variante más configurable: se define el tiempo máximo, frecuencia de sondeo y qué excepciones ignorar. Útil cuando un elemento puede tardar debido a animaciones o peticiones AJAX.

Principio del SDET: Las esperas explícitas encapsuladas dentro de los Page Objects garantizan robustez y ocultan la complejidad.
PageObjectModel

Es el patrón de diseño más adoptado para automatización de UI. Cada página web se modela como una clase; los elementos son campos y las acciones son métodos que retornan otras páginas.

    Principios:

        No exponer WebDriver ni By al test.

        Los métodos públicos representan la funcionalidad de la página (login, buscar).

        Si una acción navega a otra página, el método retorna la instancia de esa nueva página.

        No contener aserciones en los Page Objects (eso va en los tests o en capas adicionales); separar lógica de validación.

    Implementación con Page Factory:
    Selenium ofrece PageFactory que inicializa los elementos anotados con @FindBy.
    java

    public class LoginPage {
        @FindBy(id = "username")
        WebElement username;
        @FindBy(id = "password")
        WebElement password;
        @FindBy(id = "loginBtn")
        WebElement loginButton;

        public LoginPage(WebDriver driver) {
            PageFactory.initElements(driver, this);
        }

        public HomePage loginAs(String user, String pass) {
            username.sendKeys(user);
            password.sendKeys(pass);
            loginButton.click();
            return new HomePage(driver);
        }
    }

        Pros: Código declarativo y menos boilerplate.

        Contras: El lazy initialization puede esconder problemas; es más frágil con proxies. Muchos SDETs prefieren inicializar los By explícitamente y usar driver.findElement(…) directamente con esperas.

Evolución del POM:

    Component Objects: Dividir una página en componentes reutilizables (header, tabla, modal).

    Screenplay: Abstracción mayor que separa actores, tareas y preguntas; el Page Object se reduce a una fuente de localizadores y no contiene lógica de navegación.

Cypress

Cypress es un framework de testing de frontend basado en JavaScript que se ejecuta dentro del mismo bucle de eventos que la aplicación, lo que le da velocidad y control.
Primeros-pasos

    Instalación: npm install cypress --save-dev y se abre con npx cypress open. La estructura de proyecto se genera automáticamente.

    Primer test:
    javascript

    describe('Login', () => {
      it('debería loguearse con credenciales válidas', () => {
        cy.visit('/login');
        cy.get('#username').type('admin');
        cy.get('#password').type('pass');
        cy.get('button[type=submit]').click();
        cy.url().should('include', '/dashboard');
        cy.contains('Bienvenido').should('be.visible');
      });
    });

    Arquitectura única: Cypress no usa WebDriver; se comunica directamente con el navegador mediante inyección de un iframe. Esto le da acceso al DOM, a la red y a las APIs del navegador de manera síncrona (de cara al tester), mediante su motor de reintentos automáticos.

    Aserciones automáticas: Cypress reintenta automáticamente los comandos cy.get, cy.contains y las aserciones hasta que se cumplan o expire el tiempo por defecto, eliminando la necesidad de waits explícitos en la mayoría de casos.

    Manejo de red: cy.intercept() permite espiar, stubear o modificar peticiones HTTP/XHR en tiempo real, ideal para pruebas de integración de frontend sin depender del backend real.

    Limitaciones: No soporta múltiples pestañas ni navegadores distintos a los basados en Chromium, Firefox o Electron; no puede ejecutar pruebas en Safari nativo. Para escenarios multi-pestaña o cross-browser completo se prefiere Playwright.

Component-testing

Cypress ofrece también una modalidad para pruebas de componentes, compitiendo con Jest + Testing Library pero con la ventaja de ejecutarse en un navegador real.

    ¿Qué es? En lugar de montar toda la aplicación, se importa el componente (React, Vue, Svelte) y se monta en un entorno de prueba con su propio HTML.

    Configuración: Se instala con cypress-react-unit-test o similar, y se configura cypress.config.js con component support.

    Ventajas:

        Ejecución visual en el navegador (puedes ver el componente renderizado y depurar con DevTools).

        Mismo lenguaje y herramientas que las pruebas E2E.

        Acceso a la red y DOM real.

    Ejemplo conceptual:
    javascript

    import Button from './Button';
    it('emite evento click', () => {
      const onClick = cy.stub();
      cy.mount(<Button onClick={onClick} label="Enviar" />);
      cy.get('button').click();
      cy.wrap(onClick).should('have.been.calledOnce');
    });

    Para un SDET, el testing de componentes permite verificar comportamientos aislados sin pasar por servicios externos, implementando el "testing trophy" que pone énfasis en integración/componentes.

Playwright

Playwright, también de Microsoft, es un framework de automatización cross-browser (Chromium, Firefox, WebKit) con una API moderna y asíncrona.
Codegen-grabacion

Playwright viene con codegen, una herramienta de generación de código por interacción. El SDET puede usarla para acelerar la creación de localizadores o esqueleto de pruebas, no como sustituto de la ingeniería.

    Uso: npx playwright codegen https://example.com abre una ventana del navegador y un inspector. Cada clic o entrada de texto se convierte en código Playwright que se puede copiar directamente.

    Beneficios:

        Genera selectores resilientes (basados en roles de accesibilidad, texto, IDs) en lugar de XPaths frágiles.

        Captura aserciones básicas (como page.waitForSelector).

        Ayuda a explorar la estructura de la app rápidamente.

    Buenas prácticas: No confiar ciegamente; el código generado debe ser refactorizado en Page Objects y combinado con fixtures. También puede usarse para grabar flujos y luego parametrizarlos.

Testing-paralelo

Playwright fue diseñado con la paralelización como prioridad de primer nivel, superando a Selenium Grid en simplicidad.

    Modelo de Browser Context: En lugar de múltiples instancias de navegador, Playwright crea múltiples contextos de navegador, cada uno aislado (cookies, localStorage, sesiones). Crear un contexto es casi tan barato como una pestaña. Esto permite ejecutar cientos de pruebas en paralelo dentro del mismo proceso.

    Configuración: En playwright.config.ts se define workers: 4 (o 'auto'). Playwright lanza automáticamente múltiples workers (procesos) que ejecutan pruebas en paralelo.

    Aislamiento total: Cada worker puede tener su propio navegador o compartir uno, pero los contextos garantizan que las pruebas no se interfieran.

    Ejemplos de paralelización:

        Pruebas independientes en diferentes archivos se distribuyen automáticamente.

        Se pueden configurar diferentes proyectos (projects) para combinar navegador y viewport, y Playwright ejecutará todos en paralelo.

    Sharding: Para CI a gran escala, Playwright soporta sharding (dividir la suite entre múltiples máquinas) con un simple parámetro.

    Ventaja para SDET: Reduce drásticamente el tiempo de ejecución de la suite completa, un habilitador clave de la integración continua real.

Automatización API

Un SDET concentra gran parte de su estrategia de pruebas en la capa de servicios, porque es más rápida y estable que la UI.
REST Assured

Es la librería Java dominante para probar APIs REST. Usa un DSL fluido (given-when-then) que sigue el estilo BDD y facilita validar códigos de estado, cabeceras, cuerpos (JSON, XML) y tiempos.

Conceptos clave:

    Estructura: given() especifica cabeceras, parámetros, body. when() indica el método HTTP y la URL. then() realiza las validaciones.
    java

    given()
        .contentType(ContentType.JSON)
        .body(requestBody)
    .when()
        .post("/users")
    .then()
        .statusCode(201)
        .body("id", notNullValue())
        .body("name", equalTo("Juan"));

    Configuración base: RestAssured.baseURI = "http://api.example.com"; con RequestSpecification y ResponseSpecification reusables para autenticación, logging.

    Extracción de datos: Para encadenar pruebas, se extraen valores con extract().path("token") o usando JsonPath/GPath.

    Serialización/Deserialización: REST Assured integra Jackson/Gson para mapear automáticamente objetos Java a JSON y viceversa, facilitando pruebas tipadas.

    Autenticación: Soporta basic, OAuth2, form, digest. Se puede manejar de forma declarativa en la especificación de petición.

    Validación de esquemas: then().body(matchesJsonSchemaInClasspath("user-schema.json")).

    Manejo de logs: given().log().all() para depurar.

    Para SDET: Permite construir frameworks de prueba de API mantenibles usando especificaciones y herencia de configuraciones por entorno.

Postman & Newman

Aunque el SDET tiende a usar código, Postman/Newman sigue siendo necesario para equipos donde la colaboración con QA menos técnicos es vital.

Postman:

    Colecciones: agrupan peticiones. Variables en diferentes ámbitos (global, colección, entorno).

    Scripts pre-request y tests en JavaScript: se puede programar lógica de prueba y encadenamiento.

    Integración con monitores y versionamiento.

Newman:

    CLI que ejecuta colecciones de Postman sin interfaz gráfica.

    Uso: newman run mi-coleccion.json -e entorno.json --reporters cli,junit

    Permite integrar colecciones como prueba de humo en pipelines CI/CD, aunque con limitaciones en mantenibilidad cuando crece la complejidad.

    Rol del SDET: Puede generar colecciones desde definiciones OpenAPI; usarlas como punto de partida para migrar a REST Assured o código más robusto. También definir estándares para que los QA escriban colecciones que Newman ejecute en CI.

GraphQL-testing

GraphQL requiere un enfoque diferente: una sola URL, consultas flexibles y validación de esquema.

Características de las pruebas GraphQL:

    Las peticiones son POST a /graphql con un query en el body, variables opcionales.

    La respuesta siempre tiene código 200, pero puede contener errors o datos parciales.

    La validación no es solo de status, sino de estructura: que los datos vengan con los campos solicitados; también se verifican errores de negocio.

Herramientas y scripts:

    Con REST Assured: se puede enviar una cadena de consulta y validar usando JsonPath.
    java

    String query = "{ user(id: 1) { name email } }";
    given()
        .body(new GraphQLQuery(query))
    .when()
        .post("/graphql")
    .then()
        .body("data.user.name", equalTo("Juan"))
        .body("data.user.email", notNullValue());

    Para un testing más especializado, se pueden usar clientes como com.graphql-java-tools o simplemente construir la carga útil.

    Validación de esquema: Se puede obtener el esquema mediante introspección y validar las respuestas contra él, o usar pruebas de contrato.

Desafíos: Manejo de variables, mutaciones, carga de archivos. El SDET debe entender la semántica de errores (errores de sistema vs de negocio) para aserciones correctas.
Contract-testing-Pact

En arquitecturas de microservicios, las pruebas de integración completas son frágiles y pesadas. Las pruebas de contrato impulsadas por el consumidor aseguran que los servicios se comuniquen correctamente sin desplegar todo el ecosistema.

Pact Framework:

    Consumer Driven Contracts: El equipo que consume una API define un contrato (ej. "cuando GET /users/1, espero un 200 y un JSON con name y email"). Pact simula un servidor local para que el consumidor verifique su cliente contra ese mock. Luego se publica el contrato en el Pact Broker.

    Provider verification: El servicio proveedor descarga los contratos de sus consumidores y verifica que su implementación real satisface todos ellos.

    Flujo:

        Consumer test: Se define interacción esperada usando PactConsumerBuilder (Java) o @Pact (JS/Python). Se simula el provider y se prueba el cliente.

        Se genera un archivo de contrato (JSON) y se sube al broker (o se comparte vía carpeta).

        En el pipeline del provider: se ejecuta la verificación contra el endpoint real (o versiones locales). Pact provee librerías para arrancar el servicio y ejecutar las pruebas de contrato.

    Beneficios: Feedback temprano, desacoplamiento, despliegues independientes.

    Rol del SDET: Configurar la infraestructura de Pact Broker, integrar las verificaciones en CI y fomentar esta práctica en los equipos.

Automatización Mobile

Las pruebas móviles añaden fragmentación de dispositivos, gestos táctiles y conexiones de red. Dos herramientas representan los enfoques predominantes.
Appium

Es el equivalente a Selenium para móviles: permite escribir pruebas contra aplicaciones iOS, Android (nativas, web, híbridas) usando la misma API WebDriver.

Arquitectura:

    Appium Server (escrito en Node) recibe comandos HTTP y los traduce a frameworks de automatización nativos: UIAutomator2 / Espresso para Android, XCUITest para iOS.

    Cliente en cualquier lenguaje (Java, Python) usando la librería apropiada.

Conceptos fundamentales:

    Desired Capabilities: conjunto de pares clave-valor que indican el dispositivo, plataforma, app, etc. Ejemplo Android:
    java

    DesiredCapabilities caps = new DesiredCapabilities();
    caps.setCapability("platformName", "Android");
    caps.setCapability("appium:deviceName", "emulator-5554");
    caps.setCapability("appium:app", "/ruta/app.apk");
    caps.setCapability("appium:automationName", "UiAutomator2");
    AndroidDriver driver = new AndroidDriver(new URL("http://localhost:4723"), caps);

    Localización: Similar a Selenium, pero con selectores específicos como AccessibilityId, XPath nativo, UIAutomator (Android) y predicates (iOS). La AccessibilityId es el más robusto.

    Gestos: Appium provee APIs para tap, swipe, scroll, pinch, drag and drop mediante la clase TouchAction (deprecada en versiones nuevas) o mediante W3C Actions con punteros táctiles. Ejemplo swipe:
    java

    driver.executeScript("mobile: swipeGesture", ImmutableMap.of(
        "left", 100, "top", 500, "width", 200, "height", 200, "direction", "up"
    ));

    Contextos: En apps híbridas (webviews) se cambia entre contexto nativo y web con driver.getContextHandles() y driver.context().

    Ejecución en paralelo: Appium permite múltiples sesiones en un mismo servidor o usar Selenium Grid con nodos Appium. Combinado con TestNG/JUnit y dispositivos en la nube (Sauce Labs, BrowserStack) se logran pruebas masivas.

    Retos: Configuración de dispositivos/emuladores, latencia, esperas no fiables. Los SDETs aplican esperas explícitas y Page Objects móviles para mitigarlo.

Detox

Detox es un framework de pruebas end-to-end específico para React Native, aunque también soporta apps nativas. Su diferenciador es la "gray box": ejecuta la aplicación y las pruebas en el mismo contexto, permitiendo sincronización automática.

Principios:

    Sincronización Automática: Detox monitoriza el bucle de eventos de la app (JS y nativo) y espera hasta que esté inactivo antes de ejecutar el siguiente comando. Esto elimina prácticamente la necesidad de sleep() o waits manuales.

    Arquitectura: Cliente (Node) se comunica con Detox Server que corre en el dispositivo. No usa WebDriver ni HTTP para los comandos; utiliza una conexión de alto rendimiento.

    Pruébalo: Los tests se escriben en JavaScript/TypeScript con un DSL similar a Cypress.
    javascript

    describe('Login', () => {
      it('should login successfully', async () => {
        await element(by.id('username')).typeText('admin');
        await element(by.id('password')).typeText('pass');
        await element(by.text('Login')).tap();
        await expect(element(by.text('Bienvenido'))).toBeVisible();
      });
    });

    Limitaciones: Sólo para iOS y Android (no para web). La aplicación debe integrar la librería Detox en tiempo de compilación (para el mecanismo de sincronización). No es para apps híbridas generales; está muy enfocado en React Native.

El SDET elige Appium para cross-platform tradicional y gestos complejos; Detox cuando se trabaja con React Native y se requiere máxima estabilidad.
Frameworks de ejecución de pruebas

Estos frameworks organizan, ejecutan y reportan las pruebas, independientemente de la herramienta de automatización subyacente.
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

Cucumber-BDD

Cucumber permite escribir pruebas en lenguaje natural (Gherkin) que pueden ser entendidas por negocio y automatizadas.

Flujo de trabajo BDD:

    Product Owner y equipo definen escenarios en archivos .feature.

    El SDET implementa los "step definitions" que mapean cada paso a código.

    Los escenarios se ejecutan como pruebas, generando reportes que sirven como documentación viva.

Sintaxis Gherkin:
text

Feature: Login de usuario
  Scenario: Login exitoso
    Given que estoy en la página de login
    When ingreso "admin" como usuario y "pass" como contraseña
    And presiono el botón Login
    Then debería ver el mensaje "Bienvenido"

Pasos parametrizados con Data Tables y Scenario Outline:

    Scenario Outline permite ejecutar un mismo escenario con múltiples conjuntos de datos.

    Los pasos se definen con expresiones regulares o Cucumber Expressions: @When("ingreso {string} como usuario y {string} como contraseña").

Integración con Selenium/API: Los step definitions instancian Page Objects o clientes API. Se recomienda mantener la lógica de negocio en los steps y delegar la interacción a clases especializadas.

Leaner Cucumber (SpecFlow en .NET, Behave en Python): El enfoque es el mismo.

Buenas prácticas:

    Escenarios atómicos y declarativos, no secuencias de clics detalladas (imperativos).

    Mantener un lenguaje ubicuo y consistente.

    No abusar de Cucumber para todo; combinar con pruebas unitarias y de API. Cucumber es para features de negocio críticos.

Data-driven y Keyword-driven

Son dos enfoques históricos importantes para construir frameworks de automatización.

Data-driven Testing:
Las pruebas obtienen los datos de entrada y resultados esperados desde fuentes externas (Excel, CSV, base de datos), y la misma lógica de prueba se ejecuta para cada fila.

    Implementación: con TestNG DataProvider, JUnit5 parametrized tests, pytest parametrize, etc. El SDET lee el archivo de datos, lo transforma en un iterador y ejecuta.

    Ventaja: añadir un nuevo caso es solo añadir una fila sin programar.

    Desafío: la lógica de prueba debe ser suficientemente genérica; los datos deben cubrir todas las variantes.

Keyword-driven Testing:
Cada acción se representa como una "palabra clave" (keyword) que se mapea a código. Los casos de prueba son secuencias de keywords en una tabla.

    Ejemplo de tabla Excel:
    Keyword	Locator	Value
    openBrowser	Chrome	
    navigate	https://...	
    input	id=user	admin
    click	id=login	
    verifyText	id=welcome	Bienvenido

    Un motor lee la tabla y mediante reflection o diccionario invoca los métodos correspondientes.

    Herramientas: Robot Framework es el exponente más conocido. Selenium IDE también genera keywords.

    El SDET actual suele evitar construir un motor keyword-driven desde cero porque las capas de abstracción modernas (Screenplay, BDD) ofrecen mejor mantenibilidad; sin embargo, Robot Framework es apropiado en entornos donde los testers no programan pero necesitan automatizar.

Conclusión:
Para un SDET, los frameworks de ejecución (JUnit/TestNG) y el patrón BDD/Cucumber son herramientas diarias. Las técnicas data-driven forman parte natural de la parametrización, mientras que keyword-driven se reserva para contextos muy específicos con herramientas como Robot Framework.

