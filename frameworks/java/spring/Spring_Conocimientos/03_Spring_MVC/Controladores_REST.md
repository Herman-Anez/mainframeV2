
# Controladores REST

En Spring MVC, un controlador REST es aquel que devuelve datos directamente (generalmente en formato JSON o XML) en lugar de resolver un nombre de vista HTML.

## De @Controller a @RestController

La anotación `@RestController` es un atajo que combina `@Controller` y `@ResponseBody`. Al usarla, el valor de retorno de cada método se serializa automáticamente al cuerpo de la respuesta HTTP mediante un `HttpMessageConverter`.

```java
@RestController
@RequestMapping("/api/productos")
public class ProductoController {

    @GetMapping
    public List<Producto> listar() { 
        // ... lógica para listar
    }

    @GetMapping("/{id}")
    public Producto obtener(@PathVariable Long id) { 
        // ... lógica para obtener uno
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Producto crear(@RequestBody @Valid Producto producto) { 
        // ... lógica para crear
    }
}
```

## Anotaciones de Mapeo de Peticiones

Spring ofrece anotaciones compuestas para simplificar el mapeo de los métodos HTTP más comunes:

| Anotación | Equivale a |
| :--- | :--- |
| `@GetMapping` | `@RequestMapping(method = RequestMethod.GET)` |
| `@PostMapping` | `@RequestMapping(method = RequestMethod.POST)` |
| `@PutMapping` | `@RequestMapping(method = RequestMethod.PUT)` |
| `@DeleteMapping` | `@RequestMapping(method = RequestMethod.DELETE)` |
| `@PatchMapping` | `@RequestMapping(method = RequestMethod.PATCH)` |

> [!NOTE]
> Todas estas anotaciones aceptan atributos como `value` (URL), `params`, `headers`, `consumes` y `produces`.

---

## Vinculación de Parámetros (Data Binding)

Spring MVC extrae los datos de la petición y los convierte automáticamente gracias a `HandlerMethodArgumentResolver`.

- **`@PathVariable`:** Extrae valores de la plantilla de la URL (e.g., `/{id}`).
- **`@RequestParam`:** Extrae parámetros de consulta (`?nombre=valor`) o datos de formulario.
    ```java
    @GetMapping("/buscar")
    public List<Producto> buscar(@RequestParam("q") String query, 
                                 @RequestParam(defaultValue = "10") int max) { ... }
    ```
    > [!TIP]
    > Si el parámetro es opcional, puede usar `required = false` o envolverlo en un `Optional<String>`.

- **`@RequestBody`:** Convierte el cuerpo de la petición (JSON/XML) a un objeto Java usando un `HttpMessageConverter` (normalmente Jackson).
- **`@RequestHeader`:** Permite acceder a un header específico de la petición.
- **`@CookieValue`:** Extrae el valor de una cookie específica.
- **`@ModelAttribute`:** Realiza el binding de parámetros múltiples a un objeto (más común en formularios HTML que en REST puro).

---

## Manejo de Respuestas y Códigos de Estado

Existen varias formas de construir y retornar la respuesta desde un controlador:

1. **Retornar el objeto directamente:** El código HTTP por defecto es `200 OK`. Se puede usar `@ResponseStatus` a nivel de método para cambiarlo.
2. **`ResponseEntity<T>`:** Ofrece control total sobre los headers, el estado y el cuerpo.
    ```java
    @GetMapping("/{id}")
    public ResponseEntity<Producto> obtener(@PathVariable Long id) {
        Producto p = service.findById(id);
        return p != null ? ResponseEntity.ok(p) 
                         : ResponseEntity.notFound().build();
    }
    ```
3. **`HttpEntity<T>`:** Similar a `ResponseEntity`, pero también puede usarse como parámetro de entrada para acceder a los headers de la petición.

---

## Negociación de Contenido (Content Negotiation)

Spring MVC decide automáticamente qué convertidor usar basándose en:
1. El encabezado `Accept` de la petición.
2. La extensión de la URL (si está habilitado).
3. El parámetro `format`.
4. El atributo `produces` de la anotación de mapeo.

> [!IMPORTANT]
> Si se define `produces = "application/xml"`, Spring buscará un convertidor XML. Si no encuentra uno adecuado, lanzará una excepción `HttpMediaTypeNotAcceptableException`.

---

## Convertidores de Mensajes (HttpMessageConverter)

Es la interfaz que transforma objetos Java en el cuerpo de la respuesta y viceversa. Spring Boot registra automáticamente:
- **MappingJackson2HttpMessageConverter:** Para JSON (si Jackson está presente).
- **StringHttpMessageConverter:** Para `text/plain`.
- **FormHttpMessageConverter:** Para formularios.
- **Jaxb2RootElementHttpMessageConverter:** Para XML.

---

## Configuración de CORS

Puede configurarse globalmente mediante `WebMvcConfigurer` o localmente con `@CrossOrigin`:

```java
@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:4200", maxAge = 3600)
public class ApiController { ... }
```

---

## HATEOAS y Programación Reactiva

- **Spring HATEOAS:** Permite construir respuestas con hipervínculos (enlaces). Se suelen retornar objetos `EntityModel<T>` o `CollectionModel<T>`.
- **Programación Reactiva:** Con `spring-boot-starter-webflux`, los controladores pueden retornar `Mono<T>` o `Flux<T>`, permitiendo un modelo no bloqueante.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [DispatcherServlet y Flujo](./DispatcherServlet_y_Flujo.md) | [Índice](../../index.md) | [Manejo de Excepciones](./Manejo_de_Excepciones.md) |
