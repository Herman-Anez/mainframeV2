
Screenplay y Fluent

Screenplay (Serenity BDD, Boa Constrictor) es un patrón de diseño que modela las pruebas como un guion teatral: un actor realiza tareas para lograr objetivos y formula preguntas sobre el estado del sistema.

Componentes:

    Actor: Representa al usuario. Tiene habilidades (BrowseTheWeb, CallAnApi, InteractWithDatabase) que reciben dependencias como el driver.

    Tareas (Tasks): Acciones de alto nivel (Login, BuscarProducto) compuestas por interacciones (Click, EnterText). Son reutilizables y se encadenan.

    Preguntas (Questions): Retornan un valor del sistema (TextOfElement, ResponseStatus). Permiten ask y luego assert.

    Interacciones: Operaciones atómicas con el navegador o API (Click.on(element), Get.resource("/users")).

Ventajas: legibilidad extrema, separación de qué se hace (tareas) de cómo se hace (interacciones), y facilidad para cambiar de UI a API manteniendo las tareas de negocio.

Ejemplo simplificado:
java

Actor juan = new Actor("Juan").whoCan(BrowseTheWeb.with(driver));
juan.attemptsTo(Login.as("admin", "pass"));
String saludo = juan.asksFor(Text.of(HomePage.SALUDO));
assertThat(saludo, containsString("Bienvenido"));

Fluent Interface / Fluent Patterns:
Más que un patrón, es un estilo de codificación donde los métodos retornan el propio objeto (this) para encadenar instrucciones, logrando un código casi natural.

    Se usa en builders (UserBuilder.withName(...).withAge(...).build()).

    En aserciones con Hamcrest o AssertJ: assertThat(actual).isNotNull().startsWith("a").contains("bc");

    En peticiones API con REST Assured: given().header().when().get().then().statusCode(200);

    El patrón Screenplay es inherentemente fluido: juan.attemptsTo(Open.browser(url), Login.with(...), AddItem(...)).

El SDET utiliza fluent para que los ingenieros de QA sin perfil técnico puedan escribir pruebas en un DSL legible.