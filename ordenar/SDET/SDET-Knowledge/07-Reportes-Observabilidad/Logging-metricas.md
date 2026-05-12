Logging y Métricas (Observabilidad)

Los reportes de pruebas responden "¿qué falló en esta ejecución?". La observabilidad en testing responde "¿cómo está evolucionando la calidad del producto y la salud de la suite de pruebas a lo largo del tiempo?". Un SDET integra logging estructurado, métricas de ejecución y correlación con el sistema bajo prueba.
Logging estructurado en el código de pruebas

Las pruebas automatizadas deben generar logs que permitan depurar fallos intermitentes y correlacionar eventos entre la prueba y la aplicación.

    Configuración con Log4j2 / SLF4J (Java):
    xml

    <Logger name="com.ejemplo.tests" level="DEBUG" additivity="false">
        <AppenderRef ref="Console"/>
        <AppenderRef ref="File"/>
    </Logger>

    Durante la prueba:
    java

    private static final Logger log = LoggerFactory.getLogger(MiTest.class);
    log.info("Preparando datos de usuario: {}", userId);

    Buenas prácticas de logging:

        Usar identificadores de correlación (traceId, testCaseId) en ambos lados (app y prueba). El test genera un ID único al inicio y lo pasa en las peticiones (ej. cabecera X-Correlation-ID). Así, los logs del backend pueden ser enlazados con la ejecución de la prueba específica.

        No saturar los logs de la aplicación; en entornos de prueba se puede activar un nivel DEBUG, pero filtrar por ese ID.

        Capturar parámetros de entrada y puntos de verificación. Un log antes de cada assert facilita el análisis post-mortem.

    En Python (logging):
    python

    import logging
    logger = logging.getLogger(__name__)
    logger.info("Iniciando prueba de login con usuario %s", user)

Muchos frameworks de testing (pytest, TestNG) tienen hooks para capturar los logs de las pruebas automáticamente y adjuntarlos al reporte.
Captura automática de evidencias en fallos

Es imprescindible que, ante un fallo, el sistema de pruebas recolecte toda la evidencia posible sin intervención manual.

Estrategias:

    WebDriver + Screenshots: En hooks onTestFailure (TestNG) o @AfterEach con condición (JUnit5 TestInfo), tomar captura de pantalla, guardar el DOM (page source) y las logs del navegador. En Cypress, esto se hace automáticamente.

    API testing: En fallo, adjuntar la petición completa (URL, headers, body), respuesta completa (status, body) y timestamp. Con REST Assured, usando filtros de logging: given().filter(RestAssured.replaceFiltersWith(new RequestLoggingFilter())); y luego en el fallo capturarlo.

    Logs de base de datos: tras una operación, el test puede consultar tablas de auditoría y adjuntar los registros al reporte si falla.

    Herramientas: Allure y ExtentReports tienen soporte nativo para addAttachment. El código del listener se encarga de agregarlos.

Procesamiento de flaky tests:
Un dashboard de métricas debe permitir identificar pruebas inestables. Se puede etiquetar un test con @Flaky y utilizar un sistema que, en lugar de fallar el build, aísle la prueba en un grupo separado y genere una alerta.
Métricas de ejecución de pruebas con Prometheus + Grafana

Más allá del reporte puntual, el SDET recopila series de tiempo de las ejecuciones de pruebas para visualizar tendencias.

¿Qué métricas recolectar?

    Duración total de la suite.

    Número de pruebas ejecutadas, pasadas, fallidas, omitidas.

    Tasa de fallos por entorno y por rama.

    Cobertura de código (líneas, ramas) – línea de tiempo.

Implementación:

    Las herramientas de CI (Jenkins, GitHub Actions) ya exponen algunas métricas. Pero se puede enriquecer con un script que, al finalizar la suite, envíe métricas a un Pushgateway de Prometheus.

    Ejemplo en Java: usar io.prometheus:simpleclient y un CollectorRegistry.

    Con pytest: plugin pytest-prometheus o simplemente parsear los XML de JUnit y enviar métricas vía script.

    Con k6 (rendimiento) las métricas se envían a cualquier backend.

Dashboard en Grafana:

    Paneles de tendencia: tiempo de ejecución último mes.

    Paneles de flaky tests: porcentaje de tests que fallan esporádicamente.

    Mapa de calor de fallos por etapa/entorno.

Esto permite detectar degradaciones de rendimiento de la suite y tomar decisiones como cuarentenar pruebas o añadir recursos.
ReportPortal: una plataforma integral

ReportPortal.io es una solución open-source que unifica reportes multi-lenguaje (JUnit, TestNG, pytest, Cucumber, etc.) en un solo lugar, con análisis de fallos, dashboards y comparaciones.

Ventajas para el SDET:

    Centraliza resultados de múltiples equipos y proyectos.

    Análisis automático de fallos: agrupa fallos similares mediante el mensaje de error, reduciendo el ruido.

    Visualización de logs y adjuntos.

    Permite ver la ejecución en tiempo real (WebSocket).

    Histórico infinito sin necesidad de mantener HTML estáticos.

Se integra con CI mediante un agente que envía los resultados (en formato estándar como el XML de JUnit) a la instancia de ReportPortal.
Correlación con logs de la aplicación (Observabilidad de verdad)

Para cerrar el círculo, el SDET participa en la instrumentación de la aplicación para que, durante las pruebas, los logs del sistema se puedan correlacionar con el caso de prueba.

    Tracing distribuido: En microservicios, se usa un traceparent o X-B3-TraceId. El test lo inyecta y luego se puede consultar en Jaeger o Zipkin. Así, cuando un test de API falla, se puede ver exactamente la traza de ese flujo.

    Integración con Elasticsearch/Kibana: Los logs de la aplicación se indexan con el testExecutionId. Tras la ejecución, un script extrae esos logs y los adjunta al reporte, o permite al analista buscar en Kibana con ese ID.

Beneficio: Acorta drásticamente el tiempo de diagnóstico de fallos en entornos complejos.

En resumen, un sistema de reportes y observabilidad maduro transforma los datos crudos de las ejecuciones en conocimiento accionable, permitiendo al equipo reaccionar rápido y mantener la confianza en la automatización.

Si deseas que amplíe con ejemplos concretos de configuración de ReportPortal en Kubernetes, o cómo montar un dashboard de flaky tests en Grafana, estoy a tu disposición.