# Spring_Cloud/Circuit_Breaker.md
El patrón Circuit Breaker

En sistemas distribuidos, las llamadas a servicios remotos pueden fallar o volverse lentas. El Circuit Breaker detecta fallos acumulativos y "abre" el circuito, rechazando rápidamente las peticiones durante un tiempo, evitando saturar al servicio deteriorado y dando posibilidad de recuperación.

Estados del circuito:

    CLOSED: operación normal, se contabilizan éxitos/fallos.

    OPEN: se superó el umbral de fallos, se rechazan todas las peticiones inmediatamente.

    HALF-OPEN: tras un tiempo de espera, se permite un número limitado de peticiones de prueba. Si tienen éxito, vuelve a CLOSED; si fallan, vuelve a OPEN.

Spring Cloud Circuit Breaker con Resilience4j

Spring Cloud proporciona una abstracción spring-cloud-circuitbreaker que admite múltiples implementaciones. La recomendada es Resilience4j, ligera y reactiva.

Dependencias: spring-cloud-starter-circuitbreaker-resilience4j.
Uso declarativo con anotaciones

En un servicio, se anota el método:
java

@Service
public class ProductoService {

    @CircuitBreaker(name = "productoCB", fallbackMethod = "fallbackListar")
    public List<Producto> listar() {
        // llamada a servicio externo (WebClient, RestTemplate)
        return restTemplate.getForObject("http://producto-service/api/productos", List.class);
    }

    public List<Producto> fallbackListar(Throwable t) {
        return List.of(new Producto("Producto por defecto"));
    }
}

Para habilitarlo, necesita una configuración application.yml:
yaml

resilience4j:
  circuitbreaker:
    instances:
      productoCB:
        sliding-window-size: 10
        failure-rate-threshold: 50
        wait-duration-in-open-state: 10s
        permitted-number-of-calls-in-half-open-state: 3

Parámetros principales:

    sliding-window-size: número de llamadas para evaluar la tasa de fallos.

    failure-rate-threshold: porcentaje de fallos que abre el circuito.

    wait-duration-in-open-state: tiempo de espera antes de pasar a half-open.

    permitted-number-of-calls-in-half-open-state: llamadas de prueba.

Fallback y retry combinados

Resilience4j también soporta @Retry, @TimeLimiter, @Bulkhead, @RateLimiter. Se pueden combinar con @CircuitBreaker:
java

@CircuitBreaker(name = "productoCB", fallbackMethod = "fallback")
@Retry(name = "productoRetry", fallbackMethod = "fallback")
public List<Producto> listar() { ... }

Configuración del retry:
yaml

resilience4j:
  retry:
    instances:
      productoRetry:
        max-attempts: 3
        wait-duration: 500ms

Circuit Breaker en el API Gateway

Spring Cloud Gateway permite aplicar circuit breaker directamente en las rutas:
yaml

filters:
  - name: CircuitBreaker
    args:
      name: productoCB
      fallbackUri: forward:/fallback/productos

El fallback puede ser un endpoint interno que devuelva una respuesta controlada.
Eventos y métricas

Resilience4j emite eventos (transiciones de estado, fallos, éxitos) a través de Micrometer. Con Spring Boot Actuator, las métricas se exponen en /actuator/metrics y se pueden exportar a Prometheus/Grafana.

Para acceder a los eventos programáticamente:
java

@Autowired
private CircuitBreakerRegistry registry;
...
CircuitBreaker cb = registry.circuitBreaker("productoCB");
cb.getEventPublisher().onSuccess(event -> log.info("Éxito"));

Bulkhead (compartimentos estancos)

Aísla partes del sistema para evitar que un fallo en una dependencia consuma todos los hilos del pool.
yaml

resilience4j:
  bulkhead:
    instances:
      productoBulkhead:
        max-concurrent-calls: 5
        max-wait-duration: 100ms

java

@Bulkhead(name = "productoBulkhead", fallbackMethod = "fallback")
public List<Producto> listar() { ... }

Si se alcanza el límite de llamadas concurrentes, las nuevas esperan hasta max-wait-duration y luego fallan.
TimeLimiter

Limita el tiempo de ejecución de una operación (útil en métodos asíncronos o no bloqueantes).
java

@TimeLimiter(name = "productoTimeLimiter")
public CompletableFuture<List<Producto>> listarAsync() { ... }

Configuración:
yaml

resilience4j:
  timelimiter:
    instances:
      productoTimeLimiter:
        timeout-duration: 2s

Consideraciones importantes

    Resilience4j está diseñado para usarse con funciones funcionales o CompletionStage/Mono/Flux. Para código bloqueante, asegúrate de configurar los hilos apropiadamente.

    Los fallbacks deben ser simples y no depender de la misma dependencia que falló.

    Monitorear los circuit breakers con Micrometer + Grafana te permite ajustar umbrales y detectar problemas de latencia.

    El patrón no sustituye a la lógica de reintentos; se combina. Circuit Breaker evita llamadas cuando se sabe que el sistema está caído; Retry maneja fallas transitorias.



//////////////////////////////////////////////////////////////
