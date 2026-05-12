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