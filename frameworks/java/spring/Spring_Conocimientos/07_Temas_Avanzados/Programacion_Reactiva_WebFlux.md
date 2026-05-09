# Programación Reactiva con Spring WebFlux

Spring WebFlux es el módulo de Spring para construir aplicaciones web no bloqueantes usando el estándar **Reactive Streams**. Internamente se apoya en **Project Reactor**, que proporciona dos tipos principales:

*   **Mono<T>**: Emite 0 o 1 elemento (como un `Optional` asíncrono).
*   **Flux<T>**: Emite 0 a N elementos (como un `Stream` asíncrono).

> [!NOTE]
> Estos tipos son perezosos: nada ocurre hasta que alguien se suscribe. La suscripción la realiza el framework cuando el servidor recibe una petición.

## WebFlux frente a Spring MVC

| Característica | Spring MVC | Spring WebFlux |
| :--- | :--- | :--- |
| **Modelo de hilos** | Un hilo por petición (bloqueante) | Pocos hilos en loop de eventos (no bloqueante) |
| **Pila tecnológica** | Basado en Servlet API (Tomcat, Jetty) | Basado en Netty, Undertow o Servlet 3.1+ |
| **Ecosistema** | Fácil de entender, muy maduro | Mayor escalabilidad para cargas I/O intensivas |
| **Estilo de API** | Anotaciones `@Controller` | Anotaciones o functional endpoints |

## Controladores Reactivos con Anotaciones

La programación es casi idéntica a MVC, pero los métodos retornan `Mono<T>` o `Flux<T>`.

```java
@RestController
@RequestMapping("/api/productos")
public class ProductoController {
    private final ProductoRepository repo;

    @GetMapping
    public Flux<Producto> listar() {
        return repo.findAll();
    }

    @GetMapping("/{id}")
    public Mono<ResponseEntity<Producto>> obtener(@PathVariable Long id) {
        return repo.findById(id)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<Producto> crear(@RequestBody Producto producto) {
        return repo.save(producto);
    }
}
```

> [!TIP]
> La validación con `@Valid` funciona y el framework se suscribe al flujo para enviar la respuesta sin bloquear el hilo.

## Repositorios Reactivos

Spring Data proporciona **R2DBC** (Reactive Relational Database Connectivity) para bases de datos SQL y soporte reactivo para MongoDB, Redis, etc.

### R2DBC Example

```java
public interface ProductoRepository extends ReactiveCrudRepository<Producto, Long> {
    Flux<Producto> findByNombreContaining(String nombre);
}
```

La conexión se configura mediante `spring.r2dbc.*` y requiere un driver R2DBC. Internamente, usa `DatabaseClient` que se basa en Netty para comunicación no bloqueante.

## Functional Endpoints (Router & Handler)

Alternativa a las anotaciones: configuración basada en funciones.

### Router Function

```java
@Configuration
public class ProductoRouter {
    @Bean
    public RouterFunction<ServerResponse> route(ProductoHandler handler) {
        return RouterFunctions
            .route(GET("/api/productos"), handler::listar)
            .andRoute(POST("/api/productos"), handler::crear);
    }
}
```

### Handler Function

```java
@Component
public class ProductoHandler {
    private final ProductoRepository repo;

    public Mono<ServerResponse> listar(ServerRequest req) {
        Flux<Producto> productos = repo.findAll();
        return ServerResponse.ok().body(productos, Producto.class);
    }

    public Mono<ServerResponse> crear(ServerRequest req) {
        return req.bodyToMono(Producto.class)
                .flatMap(repo::save)
                .flatMap(p -> ServerResponse.created(URI.create("/api/productos/" + p.getId())).build());
    }
}
```

Este estilo ofrece máxima transparencia y composición funcional.

## WebClient: El Cliente HTTP Reactivo

Sustituto no bloqueante de `RestTemplate`. Es reactivo y devuelve Mono/Flux.

```java
WebClient client = WebClient.create("https://api.externa.com");
Mono<Producto> producto = client.get()
    .uri("/productos/{id}", id)
    .retrieve()
    .onStatus(HttpStatus::is4xxClientError, response -> Mono.error(new RecursoNoEncontrado()))
    .bodyToMono(Producto.class);
```

Soporta programación funcional, filtros, intercambio de tokens, y balanceo de carga con Spring Cloud LoadBalancer.

## Modelo de Concurrencia y Backpressure

WebFlux ejecuta en un pequeño pool de hilos (por defecto, número de núcleos de CPU) gracias al bucle de eventos de Netty. La escritura en bases de datos se hace con drivers reactivos que usan `then`, `flatMap` para encadenar operaciones sin bloquear. 

> [!IMPORTANT]
> El concepto de **backpressure** (control de flujo) permite que el consumidor le indique al productor cuántos datos está listo para procesar, evitando sobrecargas de memoria.

## ¿Cuándo usar WebFlux?

*   Altas concurrencias con muchas conexiones simultáneas (ej. API Gateway, streaming en tiempo real).
*   Operaciones I/O intensivas (llamadas a servicios externos).
*   **Nota**: No es más rápido por operación individual; brilla en *throughput* y escalabilidad bajo carga.

## Errores Comunes

> [!CAUTION]
> *   **Bloquear dentro de una cadena reactiva**: Llamar a `Thread.sleep()` o a una API bloqueante secuestra el hilo del loop y degrada el rendimiento. Usar `subscribeOn(Schedulers.boundedElastic())` para adaptar código bloqueante.
> *   **No suscribirse**: En WebFlux, nada pasa hasta que te suscribes. Siempre devuelve el `Mono`/`Flux` al framework para que él gestione la suscripción.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Eventos de Aplicación](./Eventos_de_Aplicacion.md) | [Índice](../../index.md) | [Config Server](../08_Spring_Cloud/Config_Server.md) |

