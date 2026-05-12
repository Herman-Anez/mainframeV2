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