# Detox

Detox es un framework de pruebas end-to-end específico para React Native, aunque también soporta apps nativas. Su diferenciador es el enfoque **"gray box"**: ejecuta la aplicación y las pruebas en el mismo contexto, permitiendo sincronización automática.

## Principios

- **Sincronización Automática**: Detox monitoriza el bucle de eventos de la app (JS y nativo) y espera hasta que esté inactivo antes de ejecutar el siguiente comando. Esto elimina prácticamente la necesidad de `sleep()` o *waits* manuales.
- **Arquitectura**: El cliente (Node.js) se comunica con el Detox Server que corre en el dispositivo. No usa WebDriver ni HTTP para los comandos; utiliza una conexión de alto rendimiento.

## Implementación

Los tests se escriben en JavaScript/TypeScript con un DSL similar a Cypress.

```javascript
describe('Login', () => {
  it('should login successfully', async () => {
    await element(by.id('username')).typeText('admin');
    await element(by.id('password')).typeText('pass');
    await element(by.text('Login')).tap();
    await expect(element(by.text('Bienvenido'))).toBeVisible();
  });
});
```

> [!CAUTION]
> **Limitaciones**: Sólo para iOS y Android (no para web). La aplicación debe integrar la librería Detox en tiempo de compilación. No es para apps híbridas generales; está muy enfocado en React Native.

> [!TIP]
> El SDET elige **Appium** para cross-platform tradicional y gestos complejos; **Detox** cuando se trabaja con React Native y se requiere máxima estabilidad.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Appium](./Appium.md) | [Home](../../index.md) | [Frameworks de Ejecución](../../Frameworks/index.md) |