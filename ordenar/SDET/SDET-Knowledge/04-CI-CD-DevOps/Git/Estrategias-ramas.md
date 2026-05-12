# Estrategias de ramas y su impacto en testing

La estrategia de branching define cómo y cuándo se ejecutan las pruebas automáticas. El SDET debe alinear la automatización con estas políticas para garantizar un flujo de entrega continuo y estable.

## Metodologías Comunes

### 1. Git Flow
Estructura basada en ramas `main`, `develop`, `feature`, `release` y `hotfix`.

*   **Ramas feature:** Las pruebas unitarias y de integración deben ejecutarse en cada push. El SDET asegura que en el PR se ejecuten suites rápidas (*smoke*, unit, API) con feedback < 5 min.
*   **Ramas release:** Antes de fusionar en `main`, se ejecuta la suite completa de regresión (incluyendo UI y rendimiento).
*   **Hotfix:** Requieren pruebas aceleradas focalizadas en el error corregido, más una suite de humo para evitar regresiones.
> [!WARNING]
> Las ramas de larga duración (`develop`) pueden acumular divergencias; las pruebas pueden fallar en release al mezclar múltiples características.

### 2. GitHub Flow
Ramas `feature` cortas desde `main` con despliegue continuo.

*   **Testing continuo:** En el PR se lanza la suite completa. El SDET configura la ejecución según el contexto: si el cambio es solo documentación, se salta la batería de tests.
*   **El reto:** Garantizar que la suite no dure más de 10-15 minutos. Si es más pesada, se aplica paralelismo extremo o se dividen las suites en:
    *   **Required:** Bloqueantes para el merge.
    *   **Optional:** Informativas, monitorizan estabilidad sin bloquear el flujo.

### 3. Trunk-Based Development
Rama única (`trunk`) con uso intensivo de *feature flags*.

*   Los desarrolladores hacen commit directo a `trunk` (o ramas de vida <1 día). Esto exige una calidad extrema de las pruebas automáticas.
*   **Test gating:** Antes de que un commit llegue al repositorio central, se ejecuta una suite pre-commit (unit + integración ligeras) en el entorno local.
*   La suite completa se ejecuta post-commit en CI; si falla, se revierte automáticamente el cambio o se alerta inmediatamente.

## Estrategia de pruebas por rama y entorno

*   **Configuración por entorno:** Archivos como `test-config-dev.yml` o `test-config-staging.yml` se versionan en el mismo repositorio o en uno dedicado a configuración.
*   **Agnosticismo de ramas:** Los tests deben ser independientes de la rama pero sensibles al entorno; las variables necesarias se inyectan directamente en la pipeline de CI/CD.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Comandos esenciales](./Comandos-esenciales.md) | [Home](../../../index.md) | [Jenkins](../Jenkins/index.md) |