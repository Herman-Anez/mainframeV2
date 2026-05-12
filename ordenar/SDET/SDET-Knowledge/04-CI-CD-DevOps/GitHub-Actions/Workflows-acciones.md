# Workflows y acciones para testing

Un **workflow** en GitHub Actions se compone de uno o más *jobs* con pasos que ejecutan acciones (scripts, comandos o acciones reutilizables). Para un SDET, es la herramienta ideal para orquestar baterías de pruebas automáticas en cada `push`, `pull_request` o de forma programada.

## Estructura de un workflow de pruebas típico

```yaml
name: Test Suite
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 6 * * 1-5'  # Ejecución diaria de lunes a viernes a las 6 AM

env:
  NODE_VERSION: 18

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run test:unit
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        if: success()

  integration-and-api-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - run: mvn -B verify -Pintegration

  e2e-tests:
    needs: integration-and-api-tests
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        browser: [chromium, firefox, webkit]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      - run: npx playwright install --with-deps ${{ matrix.browser }}
      - run: npx playwright test --project=${{ matrix.browser }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report-${{ matrix.browser }}
          path: playwright-report/
```

## Características destacadas para el SDET

*   **Matrix Strategy**: Permite ejecutar tests en combinaciones de sistema operativo, versión de lenguaje o navegadores.
    > [!TIP]
    > Es ideal para garantizar compatibilidad *cross-browser* y *cross-platform* con un solo job.
*   **Service Containers**: Bases de datos, Selenium Hub o Wiremock se definen directamente en el workflow, facilitando entornos de integración reales sin infraestructura externa.
*   **Caching**: El uso de `actions/cache` para dependencias (Maven, npm) acelera significativamente las ejecuciones.
*   **Artifacts y Reports**: `actions/upload-artifact` permite guardar reportes, logs y screenshots para su revisión tras un fallo.
*   **Reusabilidad**: Se pueden crear acciones compuestas y workflows reusables para encapsular pasos comunes (ej. "run-api-tests" con inputs de entorno).
*   **Condiciones y Gates**: Mediante `if`, se pueden filtrar ejecuciones (ej. saltar suites si el commit solo afecta a la documentación).

## Consideraciones de Seguridad

1.  **Secretos**: Las credenciales (`secrets.BROWSERSTACK_KEY`) se configuran en GitHub y nunca se exponen en los logs.
2.  **Pull Requests de Forks**: Los workflows de forks externos pueden tener acceso limitado a secretos por seguridad. Se debe diseñar la suite para manejar estos casos o usar `pull_request_target` con extrema precaución.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [GitHub Actions para SDET](./index.md) | [Home](../../../index.md) | [Docker para Testing](../Docker/index.md) |