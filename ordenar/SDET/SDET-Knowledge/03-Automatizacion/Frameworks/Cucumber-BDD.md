# Cucumber & BDD

Cucumber permite escribir pruebas en lenguaje natural (**Gherkin**) que pueden ser entendidas por negocio y automatizadas.

## Flujo de Trabajo BDD

1.  **Definición**: El Product Owner y el equipo definen escenarios en archivos `.feature`.
2.  **Implementación**: El SDET implementa los *"step definitions"* que mapean cada paso a código.
3.  **Ejecución**: Los escenarios se ejecutan como pruebas, generando reportes que sirven como **documentación viva**.

## Sintaxis Gherkin

```gherkin
Feature: Login de usuario
  Scenario: Login exitoso
    Given que estoy en la página de login
    When ingreso "admin" como usuario y "pass" como contraseña
    And presiono el botón Login
    Then debería ver el mensaje "Bienvenido"
```

### Parametrización
- **Scenario Outline**: Permite ejecutar un mismo escenario con múltiples conjuntos de datos.
- **Data Tables**: Permite pasar estructuras de datos complejas a un solo paso.
- **Expresiones**: Los pasos se definen con expresiones regulares o *Cucumber Expressions*: `@When("ingreso {string} como usuario y {string} como contraseña")`.

## Integración y Mejores Prácticas

- **Abstracción**: Los *step definitions* deben instanciar Page Objects o clientes API. Se recomienda mantener la lógica de negocio en los steps y delegar la interacción técnica a clases especializadas.
- **Ecosistema**: Existen versiones para otros lenguajes como SpecFlow (.NET) o Behave (Python).

> [!IMPORTANT]
> **Buenas Prácticas**:
> - **Escenarios Declarativos**: No detallar secuencias de clics (imperativo), sino el comportamiento esperado (declarativo).
> - **Lenguaje Ubicuo**: Mantener un vocabulario consistente con el negocio.
> - **Uso Selectivo**: No abusar de Cucumber para todo; reservarlo para *features* de negocio críticos.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [JUnit 5 vs. TestNG](./JUnit5-TestNG.md) | [Home](../../index.md) | [Data-driven & Keyword-driven](./Data-driven-keyword.md) |