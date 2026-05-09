# Spring Boot Actuator y Métricas

**Spring Boot Actuator** es un subproyecto que proporciona funcionalidades listas para producción que nos permiten monitorizar y gestionar nuestra aplicación. A través de endpoints HTTP o JMX, podemos obtener información sobre el estado de salud, métricas, tráfico, configuración y más.

---

## ¿Qué es Actuator?

Para habilitarlo en un proyecto, basta con añadir el starter correspondiente:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

### Endpoints Más Relevantes

| Endpoint | Descripción |
| :--- | :--- |
| `health` | Muestra el estado de salud de la aplicación y sus dependencias (BD, disco, etc.). |
| `info` | Expone información personalizada (versión, descripción de la app). |
| `metrics` | Métricas detalladas (uso de memoria, CPU, peticiones HTTP). |
| `env` | Expone las propiedades del `Environment` de Spring. |
| `loggers` | Permite consultar y modificar niveles de log en tiempo real. |
| `beans` | Lista completa de todos los beans registrados en el contexto. |
| `mappings` | Lista de todas las rutas `@RequestMapping` y sus controladores. |

> [!WARNING]
> Por motivos de seguridad, por defecto solo el endpoint `/health` está expuesto vía HTTP. Para habilitar otros en desarrollo, usa: `management.endpoints.web.exposure.include=*`.

---

## Configuración de Actuadores

La configuración se realiza habitualmente en el archivo `application.properties`:

```properties
# Exponer endpoints específicos
management.endpoints.web.exposure.include=health,info,metrics

# Mostrar detalles de salud solo a usuarios autorizados
management.endpoint.health.show-details=when-authorized

# Habilitar liveness y readiness probes (ideal para Kubernetes)
management.endpoint.health.probes.enabled=true

# Cambiar el puerto de gestión para separar el tráfico de negocio del de monitoreo
management.server.port=8081
```

---

## Health Indicators

El endpoint `/health` agrega el estado de múltiples `HealthIndicator`. Spring Boot autodetecta y configura indicadores para: **DataSource, Redis, MongoDB, RabbitMQ, DiskSpace**, etc.

### Creación de un Indicador Personalizado

Si necesitas monitorizar un servicio externo o una condición de negocio específica:

```java
@Component
public class ServicioExternoHealth implements HealthIndicator {
    @Override
    public Health health() {
        boolean disponible = checkServicio();
        if (disponible) {
            return Health.up()
                .withDetail("latencia", 120)
                .build();
        }
        return Health.down()
            .withDetail("error", "timeout")
            .build();
    }
}
```

---

## Métricas con Micrometer

Actuator utiliza **Micrometer**, una fachada de métricas que permite exportar datos a diversos sistemas de monitorización como **Prometheus, Datadog, New Relic o Graphite**.

### Métricas Automáticas
Spring Boot recolecta automáticamente:
- **JVM**: Memoria, recolección de basura (GC), hilos.
- **Sistema**: Uso de CPU, carga media.
- **HTTP**: Peticiones totales, tiempos de respuesta, códigos de estado.
- **DataSource**: Conexiones activas, hilos en espera.

### Métricas Personalizadas
Puedes inyectar un `MeterRegistry` para registrar tus propios contadores o timers:

```java
@RestController
public class PedidoController {
    private final Counter pedidosCreados;

    public PedidoController(MeterRegistry registry) {
        this.pedidosCreados = registry.counter("pedidos.creados.total");
    }

    @PostMapping("/pedidos")
    public void crear() {
        // ... lógica
        pedidosCreados.increment();
    }
}
```

> [!TIP]
> Utiliza la anotación `@Timed` en métodos de controladores o servicios para medir automáticamente el tiempo de ejecución y la frecuencia de invocación.

---

## Seguridad en Actuator

Dado que Actuator expone información sensible sobre la infraestructura, es crítico proteger sus endpoints.

- **Con Spring Security**: Se deben restringir las rutas `/actuator/**` para que solo usuarios con un rol específico (ej. `ROLE_ACTUATOR`) puedan acceder.
- **Separación de Puertos**: Configurar `management.server.port` en un puerto distinto al de la aplicación permite aplicar reglas de firewall a nivel de red.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Perfiles y Propiedades](./Perfiles_y_Propiedades.md) | [Índice](../../index.md) | [Testing](./Testing.md) |

