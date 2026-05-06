# Spring_Cloud/API_Gateway.md
El patrón API Gateway

En microservicios, un API Gateway es el punto de entrada único que encamina las peticiones a los servicios internos, aplica políticas de seguridad, límites, transformación de protocolo y agregación. Aísla al cliente de la complejidad interna.
Spring Cloud Gateway

Es el gateway oficial (reactivo, no bloqueante) construido sobre Spring WebFlux. Alternativa a Netflix Zuul (obsoleto). Se configura con spring-cloud-starter-gateway.
yaml

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

El prefijo lb:// indica balanceo de carga a través del Service Discovery (Eureka). Los predicates determinan si la ruta aplica; los filters modifican la petición/respuesta.
Predicados (predicates)

Factores que determinan si una ruta coincide. Spring Cloud Gateway incluye muchos incorporados:

    Path: /api/productos/**

    Host: *.mitienda.com

    Method: GET,POST

    Header: X-Request-Id con expresión regular

    Query param: foo=bar

    Cookie: sessionId=regex

    Before/After/Between: horarios

    Weight: para distribución ponderada (canary releases)

Ejemplo de combinación:
yaml

predicates:
  - Path=/api/**
  - Method=GET
  - Header=X-Api-Version, v2

Filtros

Los filtros permiten modificar la petición entrante y la respuesta saliente. Existen filtros predefinidos y se pueden crear filtros personalizados.

Filtros comunes de Gateway:

    AddRequestHeader / AddResponseHeader: añade encabezados.

    AddRequestParameter: añade query params.

    PrefixPath / StripPrefix: manipula la ruta.

    RewritePath: reescribe la ruta con regex.

    CircuitBreaker: integra Resilience4j (circuit breaker).

    RequestRateLimiter: limitación de velocidad con Redis.

    Retry: lógica de reintentos.

    DedupeResponseHeader: elimina cabeceras duplicadas.

Ejemplo con circuit breaker:
yaml

filters:
  - CircuitBreaker=name=productoCB, fallbackUri=forward:/fallback/productos

Filtros personalizados

Implementando GatewayFilterFactory:
java

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

Luego se usa en las rutas con - Logging.
Global Filters

Afectan a todas las rutas. Se implementan con GlobalFilter. Por ejemplo, autenticación JWT global, métricas, logging global.
Configuración programática

En lugar de YAML, se pueden definir rutas con la API de Java:
java

@Bean
public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
    return builder.routes()
        .route("producto-service", r -> r.path("/api/productos/**")
            .filters(f -> f.stripPrefix(1))
            .uri("lb://producto-service"))
        .build();
}

Integración con Spring Security

El Gateway puede integrar autenticación OAuth2, validando tokens JWT y propagando la identidad a los servicios posteriores. Con spring-boot-starter-oauth2-resource-server y configurando el gateway como resource server, se pueden proteger rutas de manera centralizada.
Limitación de velocidad (Rate Limiting)

Usa RequestRateLimiter con Redis. Se define un KeyResolver (por IP, por usuario, etc.):
java

@Bean
public KeyResolver userKeyResolver() {
    return exchange -> Mono.just(exchange.getRequest().getRemoteAddress().getAddress().getHostAddress());
}

Configuración:
yaml

filters:
  - name: RequestRateLimiter
    args:
      redis-rate-limiter.replenishRate: 10
      redis-rate-limiter.burstCapacity: 20

Resiliencia y tolerancia a fallos

El Gateway puede integrar Resilience4J (circuit breaker, retry, timeout) directamente en las rutas para fallos en los servicios backend, como veremos después.
Comparativa con otras soluciones

    Zuul 1.x: bloqueante, no recomendado para nuevas aplicaciones.

    Spring Cloud Gateway: reactivo, más ligero.

    Kong, Traefik, Nginx: soluciones externas; Spring Cloud Gateway es perfecto para ecosistema Spring Boot.

