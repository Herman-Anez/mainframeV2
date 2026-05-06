# API Gateway en Spring Cloud

En microservicios, un **API Gateway** es el punto de entrada único que encamina las peticiones a los servicios internos, aplica políticas de seguridad, límites, transformación de protocolo y agregación. Aísla al cliente de la complejidad interna.

## Spring Cloud Gateway

Es el gateway oficial (reactivo, no bloqueante) construido sobre Spring WebFlux. Es la alternativa recomendada a Netflix Zuul (obsoleto). Se configura con la dependencia `spring-cloud-starter-gateway`.

### Configuración vía YAML

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: producto-service
          uri: lb://producto-service
          predicates:
            - Path=/api/productos/**
          filters:
            - StripPrefix=1
        - id: pedido-service
          uri: lb://pedido-service
          predicates:
            - Path=/api/pedidos/**
          filters:
            - StripPrefix=1
```

> [!NOTE]
> El prefijo `lb://` indica balanceo de carga a través del **Service Discovery** (Eureka). Los *predicates* determinan si la ruta aplica; los *filters* modifican la petición o respuesta.

## Predicados (Predicates)

Son los factores que determinan si una ruta coincide. Spring Cloud Gateway incluye muchos incorporados:

*   **Path**: `/api/productos/**`
*   **Host**: `*.mitienda.com`
*   **Method**: `GET, POST`
*   **Header**: `X-Request-Id` con expresión regular.
*   **Query param**: `foo=bar`
*   **Cookie**: `sessionId=regex`
*   **Before/After/Between**: horarios específicos.
*   **Weight**: para distribución ponderada (*canary releases*).

### Ejemplo de combinación

```yaml
predicates:
  - Path=/api/**
  - Method=GET
  - Header=X-Api-Version, v2
```

## Filtros

Los filtros permiten modificar la petición entrante y la respuesta saliente. Existen filtros predefinidos y se pueden crear filtros personalizados.

### Filtros comunes de Gateway

*   **AddRequestHeader / AddResponseHeader**: añade encabezados.
*   **AddRequestParameter**: añade query params.
*   **PrefixPath / StripPrefix**: manipula la ruta.
*   **RewritePath**: reescribe la ruta con regex.
*   **CircuitBreaker**: integra Resilience4j.
*   **RequestRateLimiter**: limitación de velocidad con Redis.
*   **Retry**: lógica de reintentos.
*   **DedupeResponseHeader**: elimina cabeceras duplicadas.

### Ejemplo con Circuit Breaker

```yaml
filters:
  - CircuitBreaker=name=productoCB, fallbackUri=forward:/fallback/productos
```

## Filtros Personalizados

Para crear un filtro propio, se implementa `GatewayFilterFactory`:

```java
@Component
public class LoggingGatewayFilterFactory extends AbstractGatewayFilterFactory<LoggingGatewayFilterFactory.Config> {
    
    public LoggingGatewayFilterFactory() { super(Config.class); }

    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            System.out.println("Request: " + exchange.getRequest().getURI());
            return chain.filter(exchange).then(Mono.fromRunnable(() ->
                System.out.println("Response: " + exchange.getResponse().getStatusCode())));
        };
    }

    public static class Config { /* propiedades configurables */ }
}
```

Luego se usa en las rutas con `- Logging`.

### Global Filters

Afectan a todas las rutas de manera automática. Se implementan mediante la interfaz `GlobalFilter`. Son ideales para:
*   Autenticación JWT global.
*   Recolección de métricas.
*   Logging centralizado.

## Configuración Programática

En lugar de YAML, se pueden definir rutas mediante la API de Java:

```java
@Bean
public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
    return builder.routes()
        .route("producto-service", r -> r.path("/api/productos/**")
            .filters(f -> f.stripPrefix(1))
            .uri("lb://producto-service"))
        .build();
}
```

## Integración con Spring Security

El Gateway puede integrar autenticación OAuth2, validando tokens JWT y propagando la identidad a los servicios posteriores. Con `spring-boot-starter-oauth2-resource-server` y configurando el gateway como resource server, se pueden proteger rutas de manera centralizada.

## Limitación de Velocidad (Rate Limiting)

Utiliza `RequestRateLimiter` con Redis. Se debe definir un `KeyResolver` (por IP, por usuario, etc.):

```java
@Bean
public KeyResolver userKeyResolver() {
    return exchange -> Mono.just(exchange.getRequest().getRemoteAddress().getAddress().getHostAddress());
}
```

### Configuración en YAML

```yaml
filters:
  - name: RequestRateLimiter
    args:
      redis-rate-limiter.replenishRate: 10
      redis-rate-limiter.burstCapacity: 20
```

## Resiliencia y Tolerancia a Fallos

El Gateway puede integrar **Resilience4J** (circuit breaker, retry, timeout) directamente en las rutas para gestionar fallos en los servicios backend.

## Comparativa con otras soluciones

*   **Zuul 1.x**: bloqueante, no recomendado para nuevas aplicaciones.
*   **Spring Cloud Gateway**: reactivo, más moderno y ligero.
*   **Kong, Traefik, NGINX**: soluciones externas; Spring Cloud Gateway es la opción nativa ideal para el ecosistema Spring Boot.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Temas Avanzados](../07_Temas_Avanzados/Programacion_Reactiva_WebFlux.md) | [Índice](../../README.md) | [Circuit Breaker](Circuit_Breaker.md) |


