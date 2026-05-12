Workflows y acciones para testing

Un workflow se compone de uno o más jobs con pasos que ejecutan acciones (scripts, comandos, o acciones reutilizables). El SDET lo ve como la herramienta para ejecutar baterías de test automáticas en cada push, PR y programación.

Estructura de un workflow de pruebas típico:
yaml

name: Test Suite
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 6 * * 1-5'  # ejecución diaria a las 6 AM

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

Características destacadas para el SDET:

    Matrix strategy: permite ejecutar tests en combinaciones de sistema operativo, versión de lenguaje, navegador. Ideal para cross-browser y cross-platform con un solo job.

    Service containers: bases de datos, Selenium Hub, wiremock. Se definen directamente en el workflow, facilitando entornos de integración reales sin necesidad de hosts externos.

    Caching: actions/cache para dependencias (Maven, npm) acelera las ejecuciones.

    Artifacts y reports: actions/upload-artifact permite guardar reportes, logs, screenshots para su revisión en caso de fallo.

    Reusabilidad: se pueden escribir acciones compuestas y workflows reusables que encapsulan pasos comunes (ej. "run-api-tests" que recibe como input el entorno).

    Condiciones y gates: con if se pueden ejecutar pruebas de rendimiento solo en horarios específicos, o saltar suites si el commit solo cambia documentación.

Consideraciones de seguridad:

    Los secretos (secrets.BROWSERSTACK_KEY) se configuran en GitHub y se evita exponerlos en logs.

    Los workflows que vienen de forks de PR pueden no tener acceso a secretos; se debe diseñar la suite para que no dependa de datos confidenciales en esos casos, o usar pull_request_target con precaución.

Para el SDET, Actions facilita la integración temprana de pruebas; permite que cualquier desarrollador pueda ver el resultado de los tests directamente en el PR, fomentando la propiedad compartida de calidad.