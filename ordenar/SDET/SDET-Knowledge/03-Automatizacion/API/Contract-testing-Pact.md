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