# Circuit Breaker con Resilience4j

En sistemas distribuidos, las llamadas a servicios remotos pueden fallar o volverse lentas. El patrón **Circuit Breaker** detecta fallos acumulativos y "abre" el circuito, rechazando rápidamente las peticiones durante un tiempo. Esto evita saturar al servicio deteriorado y permite su recuperación.

## Estados del Circuito

1.  **CLOSED**: Operación normal. Se contabilizan éxitos y fallos.
2.  **OPEN**: Se superó el umbral de fallos; se rechazan todas las peticiones inmediatamente.
3.  **HALF-OPEN**: Tras un tiempo de espera, se permite un número limitado de peticiones de prueba. Si tienen éxito, vuelve a `CLOSED`; si fallan, vuelve a `OPEN`.

## Spring Cloud Circuit Breaker con Resilience4j

Spring Cloud proporciona una abstracción (`spring-cloud-circuitbreaker`) que admite múltiples implementaciones. La recomendada actualmente es **Resilience4j**, por ser ligera y reactiva.

> [!TIP]
> Dependencia necesaria: `spring-cloud-starter-circuitbreaker-resilience4j`.

### Uso declarativo con anotaciones

En un servicio, se anota el método que requiere protección:

```java
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
```

### Configuración en application.yml

```yaml
resilience4j:
  circuitbreaker:
    instances:
      productoCB:
        sliding-window-size: 10
        failure-rate-threshold: 50
        wait-duration-in-open-state: 10s
        permitted-number-of-calls-in-half-open-state: 3
```

#### Parámetros principales

*   **sliding-window-size**: número de llamadas para evaluar la tasa de fallos.
*   **failure-rate-threshold**: porcentaje de fallos que abre el circuito.
*   **wait-duration-in-open-state**: tiempo de espera antes de pasar a `HALF-OPEN`.
*   **permitted-number-of-calls-in-half-open-state**: número de llamadas de prueba permitidas.

## Fallback y Retry Combinados

Resilience4j también soporta `@Retry`, `@TimeLimiter`, `@Bulkhead` y `@RateLimiter`. Se pueden combinar con `@CircuitBreaker`:

```java
@CircuitBreaker(name = "productoCB", fallbackMethod = "fallback")
@Retry(name = "productoRetry", fallbackMethod = "fallback")
public List<Producto> listar() { ... }
```

### Configuración del Retry

```yaml
resilience4j:
  retry:
    instances:
      productoRetry:
        max-attempts: 3
        wait-duration: 500ms
```

## Circuit Breaker en el API Gateway

Spring Cloud Gateway permite aplicar circuit breaker directamente en las rutas:

```yaml
filters:
  - name: CircuitBreaker
    args:
      name: productoCB
      fallbackUri: forward:/fallback/productos
```

> [!NOTE]
> El fallback puede ser un endpoint interno que devuelva una respuesta controlada o un mensaje de error amigable.

## Eventos y Métricas

Resilience4j emite eventos (transiciones de estado, fallos, éxitos) a través de **Micrometer**. Con Spring Boot Actuator, las métricas se exponen en `/actuator/metrics` y se pueden visualizar en Prometheus/Grafana.

### Acceso programático a eventos

```java
@Autowired
private CircuitBreakerRegistry registry;

// ...
CircuitBreaker cb = registry.circuitBreaker("productoCB");
cb.getEventPublisher().onSuccess(event -> log.info("Éxito en la llamada"));
```

## Bulkhead (Compartimentos Estancos)

Aísla partes del sistema para evitar que un fallo en una dependencia consuma todos los hilos del pool de la aplicación.

```yaml
resilience4j:
  bulkhead:
    instances:
      productoBulkhead:
        max-concurrent-calls: 5
        max-wait-duration: 100ms
```

```java
@Bulkhead(name = "productoBulkhead", fallbackMethod = "fallback")
public List<Producto> listar() { ... }
```

## TimeLimiter

Limita el tiempo máximo de ejecución de una operación. Es especialmente útil en métodos asíncronos o no bloqueantes.

```java
@TimeLimiter(name = "productoTimeLimiter")
public CompletableFuture<List<Producto>> listarAsync() { ... }
```

### Configuración

```yaml
resilience4j:
  timelimiter:
    instances:
      productoTimeLimiter:
        timeout-duration: 2s
```

## Consideraciones Importantes

*   Resilience4j está diseñado para usarse con funciones funcionales o `CompletionStage`/`Mono`/`Flux`. Para código bloqueante, asegúrate de configurar los hilos apropiadamente.
*   Los **fallbacks** deben ser simples y no depender de la misma dependencia que falló.
*   Monitorear los circuit breakers con Micrometer + Grafana te permite ajustar umbrales y detectar problemas de latencia de forma proactiva.
*   El patrón no sustituye a la lógica de reintentos; se complementan. El Circuit Breaker evita llamadas cuando se sabe que el sistema está caído, mientras que el Retry maneja fallas transitorias.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [API Gateway](./API_Gateway.md) | [Índice](../../index.md) | [Internacionalización (i18n)](../09_Miscelaneos/Internacionalizacion_i18n.md) |

