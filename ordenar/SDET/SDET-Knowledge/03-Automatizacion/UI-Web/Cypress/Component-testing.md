Component-testing

Cypress ofrece también una modalidad para pruebas de componentes, compitiendo con Jest + Testing Library pero con la ventaja de ejecutarse en un navegador real.

    ¿Qué es? En lugar de montar toda la aplicación, se importa el componente (React, Vue, Svelte) y se monta en un entorno de prueba con su propio HTML.

    Configuración: Se instala con cypress-react-unit-test o similar, y se configura cypress.config.js con component support.

    Ventajas:

        Ejecución visual en el navegador (puedes ver el componente renderizado y depurar con DevTools).

        Mismo lenguaje y herramientas que las pruebas E2E.

        Acceso a la red y DOM real.

    Ejemplo conceptual:
    javascript

    import Button from './Button';
    it('emite evento click', () => {
      const onClick = cy.stub();
      cy.mount(<Button onClick={onClick} label="Enviar" />);
      cy.get('button').click();
      cy.wrap(onClick).should('have.been.calledOnce');
    });

    Para un SDET, el testing de componentes permite verificar comportamientos aislados sin pasar por servicios externos, implementando el "testing trophy" que pone énfasis en integración/componentes.

