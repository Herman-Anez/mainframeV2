Estrategias de ramas y su impacto en testing

La estrategia de branching define cómo y cuándo se ejecutan las pruebas automáticas. El SDET debe alinear la automatización con estas políticas.

    Git Flow (ramos main, develop, feature, release, hotfix)

        Ramas feature: Las pruebas unitarias y de integración deben ejecutarse en cada push a la rama. El SDET asegura que en el PR se ejecuten suites rápidas (smoke, unit, API) con feedback < 5 min.

        Ramas release: Antes de fusionar en main, se ejecuta la suite completa de regresión (incluyendo UI y rendimiento). El SDET configura el pipeline para que ejecute en paralelo y genere reportes de cobertura y estabilidad.

        Hotfix: Requieren pruebas aceleradas focalizadas en el error corregido, más una suite de humo para no romper nada.

        Inconveniente: Las ramas de larga duración (develop) pueden acumular divergencias; las pruebas pueden fallar en release al mezclar features.

    GitHub Flow (ramas feature desde main con despliegue continuo)

        Es simple: una sola rama principal (main), ramas de feature cortas, y PR hacia main.

        Testing continuo: en el PR se lanza la suite completa. El SDET configura la ejecución según el contexto: si el cambio es solo documentación, se salta la batería de tests.

        El reto es garantizar que la suite no dure más de 10-15 minutos; si es más pesada, se aplica paralelismo extremo o se dividen las suites en required (bloqueantes) y optional (informativas, que no impiden merge si fallan pero se monitorizan).

    Trunk-Based Development (rama única trunk con feature flags)

        Los desarrolladores hacen commit directo a trunk (o ramas de vida <1 día). Esto exige una calidad extrema de las pruebas automáticas.

        El SDET implementa test gating: antes de que un commit llegue al repositorio central, se ejecuta una suite pre-commit (unit + integration ligeras) en el entorno del desarrollador.

        La suite completa se ejecuta post-commit en CI, y si falla, revierte automáticamente el cambio o alerta inmediatamente.

Estrategia de pruebas por rama y entorno:

    Archivos de configuración de pruebas por entorno (test-config-dev.yml, test-config-staging.yml) se versionan en el mismo repositorio o en un repo de configuración.

    Los tests deben ser agnósticos de la rama, pero sensibles al entorno; las variables se inyectan en la pipeline.