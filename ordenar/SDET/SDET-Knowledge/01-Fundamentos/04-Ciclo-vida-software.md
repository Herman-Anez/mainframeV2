# Ciclo de vida del software y el SDET

El SDET no se suma al final; su actividad cubre todo el ciclo de vida, particularmente en metodologías ágiles (Scrum, Kanban) y DevOps.

## Fases típicas y participación

### 1. Planificación / Refinamiento de backlog
*   Revisa historias de usuario junto a Product Owner y desarrolladores.
*   Aporta criterios de aceptación desde la perspectiva de prueba: condiciones de borde, escenarios negativos, requisitos de rendimiento.
*   Identifica dependencias técnicas que pueden dificultar la automatización y las eleva como tareas técnicas.
*   Estima el esfuerzo de automatización.

### 2. Diseño
*   Participa en las sesiones de diseño de arquitectura para sugerir puntos de prueba: exponer endpoints de *health-check*, habilitar logs estructurados, prever inyección de dependencias para testing, diseñar APIs con idempotencia.
*   Diseña la estrategia de pruebas para las nuevas funcionalidades: ¿qué se probará unitario, integración, UI? ¿Se necesitan pruebas de contrato?
*   Define los datos de prueba necesarios y cómo se generarán.

### 3. Desarrollo (Codificación)
Mientras los desarrolladores programan, el SDET:
*   Escribe las pruebas de API/integración en paralelo, a veces antes del código (**ATDD** – *Acceptance Test-Driven Development*).
*   Configura el entorno de pruebas (*docker-compose* con servicios mockeados o reales).
*   Prepara los scripts de carga de datos.
*   Revisa el código del producto (*pull request*) enfocándose en la testabilidad.
*   Integra las pruebas en el pipeline CI para que se ejecuten en cada push.

### 4. Pruebas (Fase de verificación explícita)
*   En lugar de ejecutar pruebas manuales, el SDET ejecuta y monitorea las suites automáticas.
*   Analiza los resultados fallidos: si son bugs, reporta con precisión; si son falsos positivos, ajusta el script.
*   Realiza pruebas exploratorias dirigidas a áreas de alto riesgo no automatizables.
*   Ejecuta pruebas de rendimiento o de seguridad si la historia lo requiere.

### 5. Liberación (Release) y despliegue
*   Las pruebas de humo automáticas se ejecutan en el entorno de pre-producción como último filtro.
*   Supervisa las métricas de negocio y errores en producción (*synthetic monitoring*, *canary releases*). Si hay un incidente, añade una prueba que lo capture para regresión futura.

### 6. Mantenimiento y evolución
*   Continuamente refactoriza el código de pruebas para mantenerlo limpio.
*   Actualiza las herramientas de testing cuando hay nuevas versiones.
*   Monitoriza la duración de la suite y optimiza la paralelización para mantener el feedback rápido.

## Integración en DevOps

> [!TIP]
> **Shift-Left**: Mover las pruebas lo antes posible en el ciclo. Ejemplo: pruebas estáticas (linting, SAST) en el pre-commit y unitarias en el build. El SDET ayuda a que los desarrolladores puedan ejecutar pruebas complejas localmente.

> [!NOTE]
> **Shift-Right**: Probar en producción de forma controlada. El SDET implementa verificaciones sintéticas que golpean la aplicación desplegada y participa en pruebas de caos (*Chaos Engineering*) y *feature flags*.

---

| Anterior | Inicio | Siguiente |
| :------- | :----: | :-------- |
| ⏪ [Pirámide de Testing](03-Piramide-testing.md) | [Índice](01-Que-es-SDET.md) | [Técnicas de diseño de pruebas](05-Tecnicas-diseno-pruebas.md) ⏩ |

