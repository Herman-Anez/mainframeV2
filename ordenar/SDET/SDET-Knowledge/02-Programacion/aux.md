# Programación para SDET

## Lenguajes

### Java para SDET

Java sigue siendo uno de los lenguajes más demandados en entornos de testing empresarial. Un SDET que domina Java no solo sabe escribir bucles y clases; entiende cómo el lenguaje y sus características soportan la creación de frameworks robustos, paralelizables y mantenibles.

#### Sintaxis básica enfocada a testing

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

#### POO avanzado para SDET

La programación orientada a objetos es la columna vertebral de frameworks como Selenium con *Page Object Model*, pero se necesita un nivel avanzado:

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

#### Manejo de excepciones

En testing, las excepciones no son errores del sistema; a menudo son resultados esperados. El SDET debe controlarlas con maestría.

*   **Excepciones *checked* vs *unchecked***: Los frameworks de testing (TestNG, JUnit) capturan cualquier excepción y la convierten en fallo. No es necesario propagarlas siempre; a veces se atrapan para verificar un comportamiento esperado:
    ```java
    Assertions.assertThrows(NoSuchElementException.class, () -> {
        driver.findElement(By.id("inexistente"));
    });
    ```
*   **Try-catch en automatización**: Cuando se espera que una operación pueda fallar (por ejemplo, un *pop-up* que a veces no aparece), se usa `try-catch` para evitar que la prueba se detenga abruptamente.
    > [!CAUTION]
    > Un abuso de `try-catch` genera falsos positivos; se prefiere usar esperas explícitas (`WebDriverWait`) que lanzan excepciones manejables.
*   **Excepciones personalizadas**: Un SDET puede crear `TestDataException`, `EnvironmentSetupException` o `AssertionError` personalizado con mensajes claros y datos útiles para el *debugging*.
*   **Logging y manejo en hooks**: En frameworks basados en Cucumber o TestNG, los *hooks* `@After` capturan excepciones para realizar capturas de pantalla, guardar logs y limpiar el estado del entorno.

### Python para SDET

Python se ha vuelto predominante en equipos DevOps y SDET por su sintaxis clara y su ecosistema de pruebas maduro, especialmente con herramientas como `pytest` y `requests`.

#### Fundamentos de Pytest

`pytest` es más que un runner; es un framework extensible mediante plugins y *fixtures*.

*   **Instalación y ejecución**: `pip install pytest`. Ejecutar con `pytest tests/`. Descubre automáticamente archivos `test_*.py` y funciones `test_*`.
*   **Fixtures**: Son el sustituto de `@Before`/`@After`. Proporcionan datos preconfigurados y estado compartido con una limpieza segura. El *scope* puede ser `function` (por defecto), `class`, `module` o `session`.
    ```python
    @pytest.fixture(scope="function")
    def driver():
        driver = webdriver.Chrome()
        yield driver
        driver.quit()
    ```
*   **Parametrización**: Permite ejecutar la misma prueba con diferentes conjuntos de datos usando el decorador `@pytest.mark.parametrize`. Esto elimina la necesidad de bucles manuales y genera reportes individuales para cada caso.
    ```python
    @pytest.mark.parametrize("username,password,expected", [
        ("user1", "pass1", 200),
        ("user2", "wrong", 401),
    ])
    def test_login(username, password, expected):
        response = login_api(username, password)
        assert response.status_code == expected
    ```
*   **Marks (marcadores)**: Clasifican pruebas: `@pytest.mark.smoke`, `@pytest.mark.regression`. Se filtran por marcador: `pytest -m smoke`.
*   **Hooks y conftest.py**: Los archivos `conftest.py` definen fixtures a nivel de directorio y se comparten automáticamente. Los *hooks* permiten modificar el comportamiento de `pytest` (ej. capturar pantalla en fallo).
*   **Asserts avanzados**: `pytest` reescribe las aserciones para mostrar valores en fallo sin necesidad de `assertEqual`. Admite `assert a == b`, `assert result in list`, `pytest.raises`.

#### Bibliotecas de testing esenciales en Python

*   **requests + pytest**: Automatización de API. Se usa `requests` para HTTP y `pytest` para estructurar las pruebas. Se combinan *fixtures* para autenticación (obtener token) y parámetros.
    ```python
    def test_get_user(api_base_url, auth_token):
        resp = requests.get(f"{api_base_url}/users/1", headers={"Authorization": f"Bearer {auth_token}"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Juan"
    ```
*   **Selenium / Playwright con pytest**: Se usan *fixtures* para el navegador. Playwright suele ser la opción moderna por su velocidad y trazabilidad.
*   **Mocking con `unittest.mock`**: Para simular respuestas de bases de datos o servicios externos sin depender de ellos. `patch` reemplaza objetos durante una prueba.
*   **Factory Boy**: Crea instancias de objetos (modelos de base de datos, datos de entrada) con valores aleatorios o predefinidos, ideal para *data-driven testing*.
*   **Faker**: Genera datos realistas (nombres, emails, direcciones) para pruebas. Se combina con Factory Boy.
*   **Cobertura**: `pytest-cov` mide la cobertura de código. El SDET lo integra en CI para establecer umbrales (p.ej., 80% de líneas).

### TypeScript y JavaScript para SDET

El *stack* JavaScript/TypeScript domina las herramientas de testing modernas, especialmente en el ecosistema *frontend* y pruebas *end-to-end* con herramientas como Cypress, Playwright y Jest.

#### Asincronía en JavaScript

La naturaleza asíncrona de JavaScript es crítica al automatizar interacciones con el navegador y APIs. Entenderla evita pruebas erráticas.

*   **Callbacks a Promesas**: Las APIs modernas de navegador (`fetch`) están basadas en promesas. Cypress y Playwright gestionan internamente las esperas automáticas, pero al escribir tests se necesita encadenar `.then()` o usar `async/await`.
*   **Async/await**: Es el estilo preferido. Hace que el código de prueba parezca síncrono.
    ```typescript
    test('debe mostrar el usuario', async () => {
        const response = await request.get('/api/user/1');
        expect(response.status()).toBe(200);
    });
    ```
*   **Manejo en Playwright**: Todos los métodos de interacción (`page.click()`, `page.fill()`) retornan promesas. Usar `await` garantiza que la acción se completa antes de la siguiente instrucción.
*   **Esperas explícitas y *race conditions***: Aunque las herramientas tienen auto-esperas, a veces se requiere `page.waitForSelector()` o `page.waitForResponse()`. El SDET debe saber cuándo usar `Promise.all()` para ejecutar acciones paralelas (ej. hacer clic y esperar navegación).
*   **Testing de código asíncrono con Jest**: Jest requiere devolver la promesa o usar `async/await` con `expect`. Si no, la prueba puede finalizar antes de las aserciones y dar falsos positivos.

#### Testing con Jest

Jest es el framework unitario/de integración por excelencia en proyectos React, Angular, Vue y Node.

*   **Configuración**: Viene preconfigurado en CRA (*Create React App*) y Vite. Soporta TypeScript con `ts-jest`. El SDET configura `jest.config.js` para definir raíces de pruebas, patrones de archivos, *coverage* y *mocks* globales.
*   **Matchers poderosos**: `toBe`, `toEqual` (comparación profunda), `toContain`, `toMatchObject`, `toThrow`. Jest extiende las posibilidades con `jest-extended`.
*   **Mocks y espías**: `jest.fn()` crea funciones simuladas. `jest.spyOn(object, method)` espía llamadas. Útil para simular módulos completos con `jest.mock('./module')`. En pruebas de componentes, se mockean APIs y librerías externas.
*   **Timers**: Con `jest.useFakeTimers()` se controlan `setTimeout` y `setInterval`. Permite simular el paso del tiempo y evitar esperas reales en pruebas de *timeouts* o animaciones.
*   **Pruebas de componentes UI**: Con *React Testing Library* (o *Vue Test Utils*) se monta el componente, se simulan eventos y se verifican salidas en el DOM, siguiendo el enfoque de testing centrado en el usuario.
*   **Snapshots**: Capturan la salida de un componente en un archivo para detectar cambios inesperados.
    > [!WARNING]
    > Un *snapshot* grande y opaco da falsa seguridad. Se deben usar con moderación y combinarse con aserciones específicas.

## Patrones de diseño para frameworks de automatización

Los patrones no son recetas dogmáticas, sino soluciones probadas a problemas recurrentes. Un SDET aplica patrones para construir frameworks flexibles y legibles.

### Singleton y Factory en Testing

#### Singleton

Asegura que una clase tenga una única instancia y provee un punto de acceso global. En testing se usa controvertidamente para los drivers `WebDriver`, porque compartir el mismo driver entre pruebas en paralelo causa interferencias. El patrón correcto es Singleton por thread o inyección de dependencia con container.

> [!IMPORTANT]
> El patrón correcto para pruebas en paralelo es Singleton por thread o inyección de dependencia con container para evitar interferencias.

##### Ejemplo clásico
`WebDriverManager` que devuelve el mismo driver para toda la clase de prueba (no para ejecución paralela).

```java
public class DriverManager {
    private static ThreadLocal<WebDriver> driver = new ThreadLocal<>();
    public static WebDriver getDriver() {
        if (driver.get() == null) {
            driver.set(new ChromeDriver());
        }
        return driver.get();
    }
}
```

En Python, se puede implementar con módulos (el módulo es singleton) o con `@singleton` decorator. En la práctica, los frameworks modernos como Selenide o Playwright manejan esto internamente; el SDET rara vez necesita un singleton manual.

#### Factory (Método de fábrica / Abstract Factory)

Crea objetos sin especificar la clase concreta. Magnífico para:

*   Crear drivers según parámetros (Chrome, Firefox, Remote) sin que el test conozca la implementación.
*   Generar datos de prueba con fábricas que devuelven objetos `User`, `Product` con valores válidos, aleatorios o concretos. Se combina con el patrón Builder para legibilidad.

```java
public class UserFactory {
    public static User createDefaultUser() {
        return User.builder().name("Test").email("test@test.com").build();
    }
    public static User createAdminUser() { ... }
}
```

En testing de APIs, una `ResponseFactory` convierte respuestas crudas en objetos de dominio para aserciones tipadas.

### Screenplay y Fluent Interface

**Screenplay** (Serenity BDD, Boa Constrictor) es un patrón de diseño que modela las pruebas como un guion teatral: un **actor** realiza **tareas** para lograr objetivos y formula **preguntas** sobre el estado del sistema.

#### Componentes de Screenplay

*   **Actor**: Representa al usuario. Tiene **habilidades** (`BrowseTheWeb`, `CallAnApi`, `InteractWithDatabase`) que reciben dependencias como el driver.
*   **Tareas (Tasks)**: Acciones de alto nivel (`Login`, `BuscarProducto`) compuestas por **interacciones** (`Click`, `EnterText`). Son reutilizables y se encadenan.
*   **Preguntas (Questions)**: Retornan un valor del sistema (`TextOfElement`, `ResponseStatus`). Permiten `ask` y luego `assert`.
*   **Interacciones**: Operaciones atómicas con el navegador o API (`Click.on(element)`, `Get.resource("/users")`).

> [!TIP]
> Las ventajas principales son la legibilidad extrema, la separación de *qué* se hace (tareas) de *cómo* se hace (interacciones), y la facilidad para cambiar de UI a API manteniendo las tareas de negocio.

#### Ejemplo simplificado (Java)

```java
Actor juan = new Actor("Juan").whoCan(BrowseTheWeb.with(driver));
juan.attemptsTo(Login.as("admin", "pass"));
String saludo = juan.asksFor(Text.of(HomePage.SALUDO));
assertThat(saludo, containsString("Bienvenido"));
```

#### Fluent Interface / Fluent Patterns

Más que un patrón, es un estilo de codificación donde los métodos retornan el propio objeto (`this`) para encadenar instrucciones, logrando un código casi natural.

*   Se usa en **builders**: `UserBuilder.withName(...).withAge(...).build()`.
*   En **aserciones** con Hamcrest o AssertJ: `assertThat(actual).isNotNull().startsWith("a").contains("bc");`.
*   En **peticiones API** con REST Assured: `given().header().when().get().then().statusCode(200);`.
*   El patrón Screenplay es inherentemente fluido: `juan.attemptsTo(Open.browser(url), Login.with(...), AddItem(...));`.

> [!NOTE]
> El SDET utiliza *fluent* para que los ingenieros de QA sin perfil técnico puedan escribir pruebas en un DSL (*Domain Specific Language*) legible.

## Buenas prácticas en programación para Testing

Escribir pruebas es programar; las mismas reglas de calidad aplican.

### Código limpio en tests

Un test automatizado es documentación viva. Debe ser autoexplicativo, pequeño y centrado.

#### Principios fundamentales

*   **Nombrado expresivo**: El nombre de la prueba debe describir el escenario, el resultado esperado y a veces las condiciones. Patrones: `test[Metodo][Estado][Comportamiento]`. Ejemplo: `testLoginWithIncorrectPasswordReturns401`. En Cucumber, los escenarios describen la intención del negocio.
*   **Estructura AAA (Arrange, Act, Assert)**: Separar claramente preparación, acción y verificación. A veces se añade un paso Act compuesto. Un test de 10 líneas con AAA es más fácil de depurar que uno de 30 con lógica enredada.
*   **Principio DAMP (Descriptive And Meaningful Phrases) vs DRY**: En testing, no es obligatorio eliminar toda duplicación si eso perjudica la legibilidad. Es preferible repetir un par de líneas de setup si cada prueba mantiene su propia claridad. La abstracción prematura genera confusión. Se busca equilibrio: usar fixtures, builders y métodos helper para las preparaciones complejas, pero manteniendo los tests lo suficientemente lineales.
*   **Un test, un concepto**: Cada test debe verificar un único comportamiento. Si falla, la causa es obvia. Evitar múltiples assert no relacionados. Si una prueba requiere varias aserciones, que sean sobre el mismo objeto o flujo.
*   **Evitar lógica en tests**: Los `if`, `while`, `try-catch` deben ser mínimos. Si aparece lógica condicional, probablemente falta una prueba con diferentes datos parametrizados.
*   **Constantes y datos claros**: Usar variables descriptivas en lugar de números mágicos o textos largos. Ejemplo: `final String MENSAJE_ERROR = "Usuario no encontrado";` y luego `assertThat(errorMessage, is(MENSAJE_ERROR));`.
*   **Comentarios**: Los tests deben ser tan legibles que no necesiten comentarios. Si un comentario es necesario para explicar por qué se hace algo extraño, es aceptable. No comentar lo obvio.

### SOLID aplicado al código de testing

Los cinco principios SOLID se pueden reinterpretar para el diseño de pruebas y frameworks de automatización.

#### Los cinco principios

*   **S – Single Responsibility (Responsabilidad única)**: Cada clase de prueba o suite debe tener un motivo para cambiar. No mezclar pruebas de login con pruebas de reportes en la misma clase. A nivel de framework, una clase PageObject solo debe representar la página y sus elementos, no contener lógica de negocio compleja (eso va en tareas Screenplay).
*   **O – Open/Closed (Abierto para extensión, cerrado para modificación)**: Un framework debe permitir añadir nuevas páginas, componentes o drivers sin modificar las clases existentes. Se logra con herencia (`BasePage`), pero mejor aún con composición y plugins. Por ejemplo, añadir un nuevo tipo de reporte (Reporte en PDF) implementando una interfaz `TestReporter` sin tocar el código que ejecuta pruebas.
*   **L – Liskov Substitution (Sustitución de Liskov)**: Las subclases deben poder reemplazar a sus clases base sin alterar la corrección. En Page Objects: si `CheckoutPage` hereda de `CartPage`, debe poder usarse en cualquier lugar donde se espera `CartPage`. Eso implica no lanzar excepciones inesperadas ni cambiar contratos. A menudo se viola al heredar y redefinir métodos dejando vacíos los heredados; mejor usar composición.
*   **I – Interface Segregation (Segregación de interfaces)**: No forzar a un cliente a depender de métodos que no usa. En el contexto de un actor (Screenplay), define habilidades pequeñas: `BrowseTheWeb`, `ConsumeAPI`, `AccessDatabase`. Un actor que solo necesita la web no debe depender de métodos de base de datos.
*   **D – Dependency Inversion (Inversión de dependencias)**: Los módulos de alto nivel (tests) no deben depender de módulos de bajo nivel (implementaciones concretas de `WebDriver`, `database driver`). Ambos deben depender de abstracciones. Por eso se inyecta un `WebDriver` o `DriverFactory` como parámetro, en vez de instanciarlo dentro del test. Esto permite cambiar fácilmente el navegador, entorno y ejecución local vs remota.

> [!TIP]
> Aplicar SOLID evita que un proyecto de automatización se convierta en un monolito inmantenible tras un año de crecimiento.
