# Contract Testing con Pact

En arquitecturas de microservicios, las pruebas de integración completas son frágiles y pesadas. Las pruebas de contrato impulsadas por el consumidor aseguran que los servicios se comuniquen correctamente sin desplegar todo el ecosistema.

## Pact Framework

### Consumer Driven Contracts
El equipo que consume una API define un contrato (ej. *"cuando GET /users/1, espero un 200 y un JSON con name y email"*). Pact simula un servidor local para que el consumidor verifique su cliente contra ese mock. Luego se publica el contrato en el **Pact Broker**.

### Provider Verification
El servicio proveedor descarga los contratos de sus consumidores y verifica que su implementación real satisface todos ellos.

## Flujo de Trabajo

1.  **Consumer Test**: Se define la interacción esperada usando `PactConsumerBuilder` (Java) o `@Pact` (JS/Python). Se simula el provider y se prueba el cliente.
2.  **Publicación**: Se genera un archivo de contrato (JSON) y se sube al broker (o se comparte vía carpeta).
3.  **Verificación**: En el pipeline del provider, se ejecuta la verificación contra el endpoint real (o versiones locales). Pact provee librerías para arrancar el servicio y ejecutar las pruebas de contrato.

## Beneficios

- **Feedback Temprano**: Detecta fallos de integración antes de desplegar.
- **Desacoplamiento**: No requiere que todos los servicios estén arriba para probar uno solo.
- **Despliegues Independientes**: Mayor confianza al liberar nuevas versiones del proveedor.

> [!TIP]
> **Rol del SDET**: Configurar la infraestructura de Pact Broker, integrar las verificaciones en CI y fomentar esta práctica en los equipos.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [GraphQL Testing](./GraphQL-testing.md) | [Home](../../index.md) | [Appium](../../Mobile/index.md) |