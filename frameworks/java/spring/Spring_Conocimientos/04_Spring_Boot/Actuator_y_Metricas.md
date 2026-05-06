# Spring_Boot/Actuator_y_Metricas.md
¿Qué es Actuator?

Spring Boot Actuator expone una serie de endpoints HTTP y JMX que permiten monitorizar y gestionar una aplicación en producción: estado de salud, métricas, variables de entorno, configuración, trazas, mapeos de peticiones, etc. Para habilitarlo se añade el starter spring-boot-starter-actuator.
Endpoints más relevantes
Endpoint	Descripción
health	Estado de la aplicación y sus dependencias (DB, disco, etc.).
info	Información arbitraria (versión, descripción).
metrics	Métricas como uso de memoria, peticiones HTTP, tiempo de respuesta.
env	Propiedades del Environment.
loggers	Configuración de niveles de logs en tiempo real.
heapdump	Vuelca la memoria del heap (requiere JVM HotSpot).
threaddump	Vuelca los hilos.
mappings	Todos los endpoints de Spring MVC.
beans	Lista todos los beans del contexto.
conditions	Evaluación de autoconfiguraciones (positivos y negativos).

Por defecto, solo health está expuesto vía HTTP; los demás se pueden habilitar configurando management.endpoints.web.exposure.include=* (o una lista específica) para desarrollo, pero en producción se debe ser restrictivo y combinar con seguridad.
Configuración de actuadores
properties

management.endpoints.web.exposure.include=health,info,metrics
management.endpoint.health.show-details=when-authorized
management.endpoint.health.probes.enabled=true   # Para Kubernetes probes
management.server.port=8081                       # Puerto separado para gestión

Los endpoints pueden ser accedidos mediante /actuator/health, etc. (prefijo configurable).
Health indicators

El endpoint health agrega el estado de múltiples HealthIndicator. Spring Boot proporciona indicadores automáticos para: DataSource, Redis, MongoDB, DiskSpace, RabbitMQ, etc. Cada uno reporta UP, DOWN, o UNKNOWN. Puedes crear indicadores personalizados:
java

@Component
public class ServicioExternoHealth implements HealthIndicator {
    @Override
    public Health health() {
        // lógica para comprobar un servicio externo
        boolean disponible = check();
        if (disponible) {
            return Health.up().withDetail("latencia", 120).build();
        }
        return Health.down().withDetail("error", "timeout").build();
    }
}

Métricas con Micrometer

Actuator usa Micrometer como fachada de métricas. Se pueden exportar a múltiples sistemas: Prometheus, Datadog, Graphite, New Relic, etc. Basta añadir el registro adecuado (micrometer-registry-prometheus) y las métricas se publican en el formato correspondiente.

Métricas automáticas incluyen:

    JVM (memoria, GC, threads).

    Sistema (CPU, load average).

    Peticiones HTTP (http.server.requests con tag uri, status).

    Tiempos de ejecución de métodos @Timed.

    Conexiones de base de datos.

Métricas personalizadas

Puedes inyectar MeterRegistry y registrar contadores, timers, gauges.
java

@RestController
public class PedidoController {
    private final Counter pedidosCreados;

    public PedidoController(MeterRegistry registry) {
        pedidosCreados = registry.counter("pedidos.creados.total");
    }

    @PostMapping("/pedidos")
    public Pedido crear() {
        Pedido p = /* ... */;
        pedidosCreados.increment();
        return p;
    }
}

También se puede utilizar @Timed en métodos (requiere @EnableAspectJAutoProxy y un TimedAspect bean) para medir tiempos y contar invocaciones.
Info endpoint

Se puede crear un InfoContributor para añadir información personalizada, o simplemente definir propiedades:
properties

info.app.name=MiApp
info.app.version=1.0.0

java

@Component
public class BuildInfoContributor implements InfoContributor {
    @Override
    public void contribute(Info.Builder builder) {
        builder.withDetail("buildTime", Instant.now());
    }
}

Seguridad en Actuator

Combinado con Spring Security, se pueden restringir los endpoints. Lo típico es que /actuator/health esté sin autenticación (para probes de k8s) y el resto requiera un rol ACTUATOR.
