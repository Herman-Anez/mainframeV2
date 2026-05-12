Escritura Gherkin (BDD efectivo)

Gherkin es el lenguaje de dominio específico que utiliza Cucumber (y otras herramientas BDD) para describir el comportamiento del sistema. La calidad de la automatización BDD depende directamente de lo bien escritos que estén los escenarios. El SDET es a menudo el guardián de esas prácticas.
Principios de un buen escenario

    Declarativo, no imperativo: Un escenario debe describir qué comportamiento se espera, no cómo se implementa la interacción.

        Malo (imperativo):
        gherkin

        When hago clic en el botón con ID "login"
        And escribo "admin" en el campo ID "user"

        Bueno (declarativo):
        gherkin

        When inicio sesión con credenciales válidas

    Esto oculta los detalles de la UI y permite que el paso se reutilice aunque cambie la tecnología.

    Una sola responsabilidad: Cada escenario verifica una única regla de negocio. Si falla, debe ser obvio por qué. Evitar largas secuencias de acciones mezcladas con múltiples aserciones.

    Independencia: Los escenarios no deben depender unos de otros. Deben poder ejecutarse en cualquier orden. Las dependencias crean fragilidad y falsos positivos.

    Datos relevantes y contextuales: Usar Background para pasos comunes, y Scenario Outline para ejecutar el mismo escenario con múltiples conjuntos de datos usando Examples. Ejemplo:
    gherkin

    Scenario Outline: Validación de edad mínima
      Given un usuario con fecha de nacimiento <fecha>
      When intenta registrarse
      Then el sistema <resultado>

      Examples:
        | fecha       | resultado                          |
        | 2010-01-01  | permite el registro                |
        | 2019-01-01  | muestra error "Debe ser mayor de 13" |

    Evitar incluir datos de implementación en los Examples (IDs internos). Usar lenguaje de negocio.

Roles y colaboración

    Product Owner / Negocio: Define las características y puede escribir o revisar los escenarios. El SDET facilita workshops de "Example Mapping" para refinar las reglas y convertirlas en escenarios Gherkin.

    Desarrolladores: Pueden contribuir con los pasos, asegurando que el sistema es testeable.

    SDET: Implementa los "step definitions" (el pegamento entre Gherkin y la automatización). Se encarga de que los pasos sean reutilizables y modulares, refactorizando continuamente.

Mantenimiento del vocabulario ubicuo

    Crear un glosario de términos (las palabras entre comillas en los pasos) para que todo el equipo use el mismo lenguaje. Por ejemplo, decidir si se dice "Usuario" o "Cliente", "Carrito" o "Cesta".

    Usar Data Tables para datos estructurados en lugar de listas largas de parámetros. Por ejemplo, al verificar una tabla de resultados:
    gherkin

    Then debería ver la siguiente lista de productos:
      | Nombre    | Precio |
      | Manzanas  | 2.50   |
      | Peras     | 3.00   |

Anti-patrones a evitar

    "Escenarios de tren": Escenarios con 20 pasos When-Then. Son difíciles de mantener y lentos.

    Lenguaje técnico: Insertar términos como "API", "base de datos", "clic". El Gherkin es para comunicar comportamiento de negocio.

    Escenarios triviales: No automatizar con BDD validaciones que ya cubren las pruebas unitarias. No todo necesita un archivo .feature. Cucumber es para conversaciones de negocio.

Integración con el pipeline

    Los archivos .feature se versionan junto al código de prueba. El SDET configura el runner para que falle el build si existen pasos sin implementar (@Pending).

    Los reportes Cucumber (integrándose con Allure o usando el reporte HTML de Cucumber) dan visibilidad al negocio de los escenarios que no pasan.

Ejemplo completo de ciclo de un escenario

    Negocio: "Quiero que un usuario no pueda comprar si no tiene saldo".

    Refinamiento: se crea el escenario:
    gherkin

    Scenario: Pago rechazado por saldo insuficiente
      Given un cliente con saldo "10€"
      And tiene en el carrito un producto de "15€"
      When intenta pagar
      Then el pago es rechazado
      And se muestra el mensaje "Saldo insuficiente"

    SDET desarrolla los steps: Given un cliente con saldo... que prepara datos (API o BD), When intenta pagar que invoca el endpoint de pago, y los Then que validan la respuesta.

    La prueba pasa en CI y el PO ve en el reporte el escenario verde.

