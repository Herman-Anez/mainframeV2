# Spring_MVC/Manejo_de_Excepciones.md
Gestión centralizada de excepciones en @ControllerAdvice

En lugar de esparcir try/catch en cada controlador, Spring permite definir clases globales con @ControllerAdvice (o @RestControllerAdvice, que es @ControllerAdvice + @ResponseBody). Los métodos anotados con @ExceptionHandler capturan excepciones específicas.
java

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(RecursoNoEncontradoException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorDTO manejarNoEncontrado(RecursoNoEncontradoException ex) {
        return new ErrorDTO(404, ex.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public List<ErrorValidacionDTO> manejarValidacion(MethodArgumentNotValidException ex) {
        return ex.getBindingResult().getFieldErrors().stream()
                .map(e -> new ErrorValidacionDTO(e.getField(), e.getDefaultMessage()))
                .collect(Collectors.toList());
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorDTO manejarGeneral(Exception ex) {
        // logging del stacktrace real
        logger.error("Error no esperado", ex);
        return new ErrorDTO(500, "Error interno del servidor");
    }
}

Jerarquía de manejo de excepciones

Spring busca el manejador más específico:

    @ExceptionHandler dentro del propio controlador (mayor prioridad).

    @ExceptionHandler en clases con @ControllerAdvice aplicables (pueden ser globales, por paquete, o por anotación).

    Implementaciones de HandlerExceptionResolver (resolvers globales).

    Si no se captura, se propaga al contenedor servlet, que responde con una página de error predeterminada (o se puede personalizar con ErrorController).

HandlerExceptionResolver y sus implementaciones

HandlerExceptionResolver es la interfaz de bajo nivel. La resolución ocurre en el DispatcherServlet antes de llegar a los filtros de error. Implementaciones por defecto:

    ExceptionHandlerExceptionResolver: invoca los métodos @ExceptionHandler de @ControllerAdvice y controladores. Es el más potente y se configura automáticamente al detectar anotaciones.

    ResponseStatusExceptionResolver: busca la anotación @ResponseStatus en la excepción y establece el código de estado.

    DefaultHandlerExceptionResolver: convierte excepciones estándar de Spring MVC (NoHandlerFoundException, HttpMediaTypeNotSupportedException, etc.) a códigos HTTP.

    SimpleMappingExceptionResolver: mapea nombres de excepción a vistas de error (configuración XML/Java), para MVC no REST.

Se pueden agregar resolvers personalizados o ajustar el orden con WebMvcConfigurer.configureHandlerExceptionResolvers.
Lanzar excepciones con ResponseStatusException

Para evitar crear clases de excepción personalizadas, Spring ofrece ResponseStatusException, que se puede lanzar directamente y será capturada por ResponseStatusExceptionResolver:
java

@GetMapping("/{id}")
public Producto obtener(@PathVariable Long id) {
    throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Producto no encontrado");
}

El cuerpo por defecto contendrá el mensaje y el status. Para un formato más rico, es mejor usar un @ControllerAdvice con DTO.
Errores en filtros y antes del DispatcherServlet

Las excepciones que ocurren en los filtros (fuera del alcance del DispatcherServlet) no son manejadas por los mecanismos anteriores. Para capturarlas y devolver una respuesta JSON consistente, se puede usar un ErrorController implementando ErrorController (Spring Boot provee BasicErrorController). Personalizarlo permite tener respuestas de error uniformes aunque la petición nunca llegue al controlador.
Response con detalles en errores de validación

Volviendo al ejemplo de MethodArgumentNotValidException: el BindingResult contiene todos los errores de campo (rechazos de @NotNull, @Size, etc.), que podemos serializar en una lista de errores estructurados. Es una práctica recomendada devolver una respuesta legible por el cliente frontend.
