#  Ciclo de vida del software y el SDET

El SDET no se suma al final; su actividad cubre todo el ciclo de vida, particularmente en metodologías ágiles (Scrum, Kanban) y DevOps.
Fases típicas y participación

    Planificación / Refinamiento de backlog

        Revisa historias de usuario junto a Product Owner y desarrolladores.

        Aporta criterios de aceptación desde la perspectiva de prueba: condiciones de borde, escenarios negativos, requisitos de rendimiento.

        Identifica dependencias técnicas que pueden dificultar la automatización (p.ej., falta de IDs en los elementos UI) y las eleva como tareas técnicas.

        Estima el esfuerzo de automatización.

    Diseño

        Participa en las sesiones de diseño de arquitectura para sugerir puntos de prueba: exponer endpoints de health-check, habilitar logs estructurados, prever inyección de dependencias para testing, diseñar APIs con idempotencia y fácil testabilidad.

        Diseña la estrategia de pruebas para las nuevas funcionalidades: ¿qué se probará unitario, integración, UI? ¿Se necesitan pruebas de contrato?

        Define los datos de prueba necesarios y cómo se generarán.

    Desarrollo (Codificación)

        Mientras los desarrolladores programan, el SDET:

            Escribe las pruebas de API/integración en paralelo, a veces antes del código (ATDD – Acceptance Test-Driven Development).

            Configura el entorno de pruebas (docker-compose con servicios mockeados o reales).

            Prepara los scripts de carga de datos.

            Revisa el código del producto (pull request) enfocándose en la testabilidad y en las pruebas unitarias que el desarrollador incluyó.

        Integra las pruebas en el pipeline CI para que se ejecuten en cada push.

    Pruebas (Fase de verificación explícita)

        En lugar de ejecutar pruebas manuales, el SDET ejecuta y monitorea las suites automáticas.

        Analiza los resultados fallidos: si son bugs, reporta con precisión (logs, trazas, pasos para reproducir); si son falsos positivos, ajusta el script.

        Realiza pruebas exploratorias dirigidas a áreas de alto riesgo que no están automatizadas (porque no todo es automatizable).

        Ejecuta pruebas de rendimiento o de seguridad si la historia lo requiere.

    Liberación (Release) y despliegue

        Las pruebas de humo automáticas se ejecutan en el entorno de pre-producción como último filtro.

        Supervisa las métricas de negocio y errores en producción (synthetic monitoring, canary releases). Si hay un incidente, añade una prueba que lo capture para regresión futura.

    Mantenimiento y evolución

        Continuamente refactoriza el código de pruebas para mantenerlo limpio.

        Actualiza las herramientas de testing cuando hay nuevas versiones.

        Monitoriza la duración de la suite y optimiza la paralelización para mantener el feedback rápido.

Integración en DevOps: Shift-Left y Shift-Right

    Shift-Left: Mover las pruebas lo antes posible en el ciclo. Ejemplo: pruebas estáticas (linting, análisis de seguridad SAST) en el pre-commit; unitarias al hacer commit; integración en el build. El SDET ayuda a que los desarrolladores puedan ejecutar pruebas complejas localmente con un solo comando.

    Shift-Right: Probar en producción de forma controlada. El SDET implementa verificaciones sintéticas que golpean la aplicación desplegada periódicamente y disparan alertas si fallan. También participa en pruebas de caos (Chaos Engineering) y feature flags.

