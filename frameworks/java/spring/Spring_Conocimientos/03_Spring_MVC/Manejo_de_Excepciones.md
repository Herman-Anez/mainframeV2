# Manejo de Excepciones en Spring MVC

Spring MVC ofrece mecanismos potentes para centralizar el manejo de errores, evitando el uso repetitivo de bloques `try/catch` en los controladores.

## Gestión Centralizada con @ControllerAdvice

La anotación `@ControllerAdvice` (o `@RestControllerAdvice` para APIs REST) permite definir una clase global que captura excepciones lanzadas por cualquier controlador.

Los métodos anotados con `@ExceptionHandler` se encargan de procesar excepciones específicas.

```java
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
        // Log del stacktrace real
        logger.error("Error no esperado", ex);
        return new ErrorDTO(500, "Error interno del servidor");
    }
}
```

---

## Jerarquía de Manejo de Excepciones

Spring busca el manejador más específico siguiendo este orden de prioridad:

1. **`@ExceptionHandler` local:** Dentro del propio controlador donde ocurrió el error.
2. **`@ExceptionHandler` global:** En clases anotadas con `@ControllerAdvice`.
3. **`HandlerExceptionResolver`:** Implementaciones globales de bajo nivel.
4. **Contenedor Servlet:** Si nadie captura la excepción, se propaga al servidor (e.g., Tomcat), que muestra una página de error por defecto.

---

## HandlerExceptionResolver

Es la interfaz de bajo nivel que utiliza el `DispatcherServlet` para resolver excepciones. Implementaciones por defecto:

- **ExceptionHandlerExceptionResolver:** Es el más potente. Procesa las anotaciones `@ExceptionHandler`.
- **ResponseStatusExceptionResolver:** Busca la anotación `@ResponseStatus` en las clases de excepción personalizadas.
- **DefaultHandlerExceptionResolver:** Convierte excepciones estándar de Spring MVC (como `NoHandlerFoundException`) en códigos HTTP adecuados.
- **SimpleMappingExceptionResolver:** Mapea nombres de excepción a nombres de vista (útil en aplicaciones MVC tradicionales, no REST).

> [!TIP]
> Se pueden agregar resolvers personalizados o ajustar su orden de ejecución mediante `WebMvcConfigurer.configureHandlerExceptionResolvers`.

---

## Uso de ResponseStatusException

Spring permite lanzar excepciones rápidas sin necesidad de crear clases personalizadas mediante `ResponseStatusException`:

```java
@GetMapping("/{id}")
public Producto obtener(@PathVariable Long id) {
    throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Producto no encontrado");
}
```

> [!IMPORTANT]
> Aunque es útil para casos simples, para APIs profesionales se recomienda usar `@ControllerAdvice` con un DTO de error estructurado para mantener la consistencia en las respuestas.

---

## Errores en Filtros y Pre-Dispatcher

Las excepciones que ocurren en los **filtros** (fuera del alcance de Spring MVC) no son capturadas por `@ControllerAdvice`. 

Para estos casos, Spring Boot provee un `BasicErrorController`. Si necesitas personalizar la respuesta para errores de bajo nivel (como un error de autenticación en un filtro de seguridad), puedes implementar tu propio `ErrorController`.

---

## Detalles en Errores de Validación

Cuando falla una validación (e.g., `@NotNull`, `@Size`), se lanza una `MethodArgumentNotValidException`. Esta excepción contiene un objeto `BindingResult` con todos los errores de campo. 

Es una buena práctica extraer estos errores y devolverlos en una lista legible para que el cliente (frontend) pueda informar al usuario exactamente qué falló.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Controladores REST](./Controladores_REST.md) | [Índice](../../README.md) | [Validación y Binding](./Validacion_y_BindingResult.md) |

