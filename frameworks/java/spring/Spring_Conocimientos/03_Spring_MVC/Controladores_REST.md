
# Spring_MVC/Controladores_REST.md
De @Controller a @RestController

Un controlador REST es un controlador que devuelve datos (generalmente JSON o XML) en lugar de un nombre de vista. La anotación @RestController es un atajo que combina @Controller y @ResponseBody. Con @ResponseBody, el valor de retorno del método se serializa directamente al cuerpo de la respuesta HTTP mediante HttpMessageConverter.
java

@RestController
@RequestMapping("/api/productos")
public class ProductoController {

    @GetMapping
    public List<Producto> listar() { ... }

    @GetMapping("/{id}")
    public Producto obtener(@PathVariable Long id) { ... }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Producto crear(@RequestBody @Valid Producto producto) { ... }
}

Anotaciones de mapeo de peticiones

Spring ofrece antaciones compuestas para los métodos HTTP más comunes:
Anotación	Equivale a
@GetMapping	@RequestMapping(method = RequestMethod.GET)
@PostMapping	@RequestMapping(method = RequestMethod.POST)
@PutMapping	@RequestMapping(method = RequestMethod.PUT)
@DeleteMapping	@RequestMapping(method = RequestMethod.DELETE)
@PatchMapping	@RequestMapping(method = RequestMethod.PATCH)

Todas aceptan atributos como value (URL), params, headers, consumes, produces.
Vinculación de parámetros (Data Binding avanzado)

Spring MVC extrae los datos de la petición y los convierte automáticamente gracias a HandlerMethodArgumentResolver.

    @PathVariable: de la plantilla de la URL. @GetMapping("/{id}") con @PathVariable Long id.

    @RequestParam: de parámetros de consulta o datos de formulario (?nombre=valor).
    java

    @GetMapping("/buscar")
    public List<Producto> buscar(@RequestParam("q") String query, 
                                 @RequestParam(defaultValue = "10") int max) { ... }

    Si el parámetro es opcional, usar required = false o Optional<String>.

    @RequestBody: convierte el cuerpo de la petición (JSON, XML) a un objeto Java usando HttpMessageConverter (normalmente Jackson).

    @RequestHeader: extrae un header específico.

    @CookieValue: extrae el valor de una cookie.

    @ModelAttribute: para binding de parámetros múltiples a un objeto (menos común en REST puro, más en formularios).

    Objetos complejos: Si el método tiene un parámetro de tipo POJO sin anotaciones, Spring lo trata como un @ModelAttribute, haciendo binding de parámetros por nombre de propiedad.

Manejo de respuestas y códigos de estado

La respuesta se puede construir de varias formas:

    Retornar directamente el objeto (con @ResponseBody o en un @RestController). El código HTTP por defecto es 200 OK. Para otros códigos se usa @ResponseStatus a nivel de método o excepción.

    ResponseEntity<T>: da control total sobre headers, status y cuerpo.
    java

    @GetMapping("/{id}")
    public ResponseEntity<Producto> obtener(@PathVariable Long id) {
        Producto p = service.findById(id);
        return p != null ? ResponseEntity.ok(p) 
                         : ResponseEntity.notFound().build();
    }

    ResponseEntity tiene métodos estáticos: ok(), created(URI), noContent(), badRequest(), status(HttpStatus), etc.

    HttpServletResponse: en el propio parámetro del método, se puede escribir directamente (no recomendado para REST moderno).

    HttpEntity<T>: similar a ResponseEntity pero también puede usarse como parámetro de entrada con HttpEntity<Producto> (accede a headers y cuerpo de la petición).

Negociación de contenido (Content Negotiation)

Spring MVC decide automáticamente qué converter usar basándose en:

    El header Accept de la petición.

    La extensión de la URL (si está configurado).

    El parámetro format (si está configurado).

    El atributo produces de las anotaciones de mapeo.

Ejemplo: si produces = "application/xml", Spring usará un converter de XML (si está disponible, p.ej. jackson-dataformat-xml). Si no hay converter adecuado, lanza HttpMediaTypeNotAcceptableException.
Convertidores de mensajes (HttpMessageConverter)

Interfaz que transforma entre objetos Java y el cuerpo de peticiones/respuestas. Spring Boot registra automáticamente:

    MappingJackson2HttpMessageConverter (JSON) si Jackson está en el classpath.

    StringHttpMessageConverter (text/plain).

    FormHttpMessageConverter (formularios).

    Jaxb2RootElementHttpMessageConverter (XML) si JAXB está disponible, pero normalmente se prefiere el jackson XML converter.

Se pueden añadir o personalizar mediante configureMessageConverters() o extendMessageConverters() en WebMvcConfigurer.
Configuración de CORS en controladores

A nivel global con WebMvcConfigurer.addCorsMappings, o a nivel de controlador/método con @CrossOrigin.
java

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:4200", maxAge = 3600)
public class ApiController { ... }

HATEOAS y enlaces

Spring HATEOAS permite construir respuestas REST con hipervínculos. Aunque es avanzado, los controladores pueden devolver EntityModel<T> o CollectionModel<T> para añadir enlaces. Spring Boot con spring-boot-starter-hateoas proporciona autoconfiguración.
Programación reactiva en REST

Con spring-boot-starter-webflux y @RestController (o en WebFlux), los métodos pueden retornar Mono<T> o Flux<T>. Spring maneja la suscripción. Cambia el paradigma a no bloqueante.
