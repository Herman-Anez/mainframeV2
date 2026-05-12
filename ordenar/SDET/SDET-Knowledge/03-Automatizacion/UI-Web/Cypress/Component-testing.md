# Component Testing con Cypress

Cypress ofrece también una modalidad para pruebas de componentes, compitiendo con Jest + Testing Library pero con la ventaja de ejecutarse en un navegador real.

## ¿Qué es?

En lugar de montar toda la aplicación, se importa el componente (React, Vue, Svelte) y se monta en un entorno de prueba con su propio HTML.

## Configuración

Se instala con `cypress-react-unit-test` o similar, y se configura `cypress.config.js` con *component support*.

## Ventajas

- **Ejecución visual**: Puedes ver el componente renderizado y depurar con DevTools en un navegador real.
- **Consistencia**: Mismo lenguaje y herramientas que las pruebas E2E.
- **Realismo**: Acceso a la red y DOM real.

## Ejemplo Conceptual

```javascript
import Button from './Button';

it('emite evento click', () => {
  const onClick = cy.stub();
  cy.mount(<Button onClick={onClick} label="Enviar" />);
  cy.get('button').click();
  cy.wrap(onClick).should('have.been.calledOnce');
});
```

> [!TIP]
> Para un SDET, el testing de componentes permite verificar comportamientos aislados sin pasar por servicios externos, implementando el **"testing trophy"** que pone énfasis en integración/componentes.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Primeros Pasos](./Primeros-pasos.md) | [Home](../../../index.md) | [Playwright](../Playwright/index.md) |


