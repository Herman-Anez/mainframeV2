# Temas_Avanzados/Programacion_Reactiva_WebFlux.md
Fundamentos reactivos con Project Reactor

Spring WebFlux es el módulo de Spring para construir aplicaciones web no bloqueantes usando el estándar Reactive Streams. Internamente se apoya en Project Reactor, que proporciona dos tipos principales:

    Mono<T>: emite 0 o 1 elemento (como un Optional asíncrono).

    Flux<T>: emite 0 a N elementos (como un Stream asíncrono).

Estos tipos son perezosos: nada ocurre hasta que alguien se suscribe. La suscripción la realiza el framework cuando el servidor recibe una petición.
WebFlux frente a Spring MVC
Spring MVC	Spring WebFlux
Modelo de hilos: un hilo por petición (bloqueante)	Modelo de hilos: pocos hilos en loop de eventos (no bloqueante)
Basado en Servlet API (Tomcat, Jetty)	Basado en Netty, Undertow o Servlet 3.1+ (con soporte no bloqueante)
Fácil de entender, ecosistema maduro	Mayor escalabilidad para cargas I/O intensivas
Anotaciones @Controller iguales	Puede usar anotaciones o functional endpoints
Controladores reactivos con anotaciones

La programación es casi idéntica a MVC, pero los métodos retornan Mono<T> o Flux<T>.
java

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

La validación con @Valid funciona y el framework se suscribe al flujo para enviar la respuesta sin bloquear el hilo.
Repositorios reactivos

Spring Data proporciona R2DBC (Reactive Relational Database Connectivity) para bases de datos SQL y reactive MongoDB, Redis, etc.

R2DBC:
java

public interface ProductoRepository extends ReactiveCrudRepository<Producto, Long> {
    Flux<Producto> findByNombreContaining(String nombre);
}

La conexión se configura mediante spring.r2dbc.* y requiere un driver R2DBC (por ejemplo, PostgreSQL). Internamente, usa DatabaseClient que se basa en Netty para comunicación no bloqueante.
Functional Endpoints (RouterFunction & HandlerFunction)

Alternativa a las anotaciones: configuración basada en funciones.
java

@Configuration
public class ProductoRouter {
    @Bean
    public RouterFunction<ServerResponse> route(ProductoHandler handler) {
        return RouterFunctions
            .route(GET("/api/productos"), handler::listar)
            .andRoute(POST("/api/productos"), handler::crear);
    }
}

java

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

Este estilo ofrece máxima transparencia y composición funcional.
WebClient: el cliente HTTP reactivo

Sustituto no bloqueante de RestTemplate. Es reactivo y devuelve Mono/Flux.
java

WebClient client = WebClient.create("https://api.externa.com");
Mono<Producto> producto = client.get()
    .uri("/productos/{id}", id)
    .retrieve()
    .onStatus(HttpStatus::is4xxClientError, response -> Mono.error(new RecursoNoEncontrado()))
    .bodyToMono(Producto.class);

Soporta programación funcional, filtros, intercambio de tokens, y balanceo de carga con Spring Cloud LoadBalancer.
Modelo de concurrencia y backpressure

WebFlux ejecuta en un pequeño pool de hilos (por defecto, número de núcleos de CPU) gracias al bucle de eventos de Netty. La escritura en bases de datos se hace con drivers reactivos que usan then, flatMap para encadenar operaciones sin bloquear. El concepto de backpressure (control de flujo) permite que el consumidor le indique al productor cuántos datos está listo para procesar, evitando sobrecargas de memoria.
¿Cuándo usar WebFlux?

    Altas concurrencias con muchas conexiones simultáneas (ej. API Gateway, streaming en tiempo real).

    Operaciones I/O intensivas (llamadas a servicios externos).

    No es más rápido por operación individual; brilla en throughput y escalabilidad bajo carga.

Errores comunes

    Bloquear dentro de una cadena reactiva (ej. llamar a Thread.sleep() o a una API bloqueante). Esto secuestra el hilo del loop y degrada el rendimiento. Usar subscribeOn(Schedulers.boundedElastic()) para adaptar código bloqueante.

    No suscribirse explícitamente; siempre devolver el Mono/Flux al framework.
