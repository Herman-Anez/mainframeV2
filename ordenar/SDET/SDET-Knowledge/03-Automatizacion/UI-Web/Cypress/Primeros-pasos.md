# Primeros Pasos con Cypress

## Instalación

```bash
npm install cypress --save-dev
npx cypress open
```

La estructura del proyecto se genera automáticamente al abrirlo por primera vez.

## Primer Test

```javascript
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
```

## Características Clave

### Arquitectura Única
Cypress no usa WebDriver; se comunica directamente con el navegador mediante inyección de un `iframe`. Esto le da acceso al DOM, a la red y a las APIs del navegador de manera síncrona (de cara al tester), mediante su motor de reintentos automáticos.

### Aserciones Automáticas
Cypress reintenta automáticamente los comandos `cy.get`, `cy.contains` y las aserciones hasta que se cumplan o expire el tiempo por defecto, eliminando la necesidad de *waits* explícitos en la mayoría de casos.

### Manejo de Red
`cy.intercept()` permite espiar, *stubear* o modificar peticiones HTTP/XHR en tiempo real, ideal para pruebas de integración de frontend sin depender del backend real.

> [!WARNING]
> **Limitaciones**: No soporta múltiples pestañas ni navegadores distintos a los basados en Chromium, Firefox o Electron; no puede ejecutar pruebas en Safari nativo. Para escenarios multi-pestaña o cross-browser completo se prefiere Playwright.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Cypress Index](./index.md) | [Home](../../../index.md) | [Component Testing](./Component-testing.md) |