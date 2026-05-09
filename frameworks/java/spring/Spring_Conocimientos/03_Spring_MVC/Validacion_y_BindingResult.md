# Validación y BindingResult

La validación en Spring MVC se apoya en la especificación **Bean Validation** (JSR-380) para asegurar que los datos de entrada cumplan con las reglas de negocio antes de ser procesados por el controlador.

## Bean Validation (JSR-380) y Spring MVC

Spring MVC se integra con **Hibernate Validator** (la implementación de referencia) automáticamente cuando está en el classpath. Las anotaciones de validación se colocan directamente en los campos del DTO o entidad.

```java
public class ProductoDTO {
    @NotBlank(message = "El nombre es obligatorio")
    private String nombre;
    
    @Positive(message = "El precio debe ser positivo")
    private BigDecimal precio;
    
    @Size(min = 3, max = 10, message = "El SKU debe tener entre 3 y 10 caracteres")
    private String sku;
}
```

---

## Activación de la Validación

Para que Spring valide automáticamente un `@RequestBody`, se debe añadir la anotación `@Valid` (JSR-303) o `@Validated` (Spring) al parámetro del método en el controlador.

```java
@PostMapping
public ResponseEntity<Producto> crear(@Valid @RequestBody ProductoDTO dto) { 
    // ... lógica de negocio
}
```

> [!IMPORTANT]
> Si la validación falla y no se captura el error, Spring lanza una `MethodArgumentNotValidException` antes de ejecutar el método del controlador. Es fundamental manejar esta excepción en un `@ControllerAdvice`.

---

## Uso de BindingResult

Cuando se prefiere no lanzar una excepción y manejar los errores manualmente, se puede declarar un parámetro `BindingResult` inmediatamente después del objeto validado.

```java
@PostMapping
public ResponseEntity<?> crear(@Valid @RequestBody ProductoDTO dto, BindingResult result) {
    if (result.hasErrors()) {
        // Construir respuesta de error personalizada
        return ResponseEntity.badRequest().body(crearErrores(result));
    }
    // Lógica normal si no hay errores
}
```

> [!TIP]
> Esta técnica es muy útil cuando se necesita realizar comprobaciones adicionales o lógica condicional antes de reportar los errores al cliente.

---

## Validación en Servicios y Parámetros Simples

### Validación en la Capa de Servicio
Se puede validar a nivel de servicio usando `@Validated` en la clase y anotaciones en los parámetros. Esto dispara una `ConstraintViolationException`.

```java
@Service
@Validated
public class ProductoService {
    public void actualizarPrecio(@Positive double nuevoPrecio) { ... }
}
```

### Path Variables y Request Params
Para validar parámetros simples en el controlador, se anota la clase con `@Validated` y se usan las anotaciones directamente en los argumentos.

```java
@RestController
@RequestMapping("/api")
@Validated
public class BusquedaController {

    @GetMapping("/buscar")
    public List<Producto> buscar(@RequestParam @Size(min = 2) String q) { ... }
}
```

---

## Mensajes Personalizados e i18n

El atributo `message` puede referenciar claves de un archivo de propiedades para soportar internacionalización:

```java
@NotNull(message = "{producto.nombre.obligatorio}")
```

> [!NOTE]
> Spring Boot configura automáticamente un `MessageSource` que busca en `messages.properties`. Los mensajes pueden resolverse dinámicamente en el `@ControllerAdvice`.

---

## Grupos de Validaciones

Bean Validation permite definir **interfaces de grupos** para aplicar reglas distintas según el contexto (ej. creación vs. actualización). Se especifica el grupo con `@Validated(OnCreate.class)` en el controlador.

---

# Vistas y Templates

En aplicaciones que no son puramente REST, Spring MVC utiliza un sistema de resolución de vistas para renderizar contenido HTML.

## Concepto de ViewResolver y View

Cuando un controlador retorna un `String` sin `@ResponseBody`, se interpreta como el **nombre lógico** de una vista. El `DispatcherServlet` delega en los `ViewResolvers` para localizar el recurso real.

### ViewResolvers Comunes
- **InternalResourceViewResolver:** Para JSPs.
- **ThymeleafViewResolver:** Para plantillas Thymeleaf (recomendado).
- **FreeMarkerViewResolver / MustacheViewResolver:** Para otros motores.

---

## Paso de Datos a la Vista

El controlador añade atributos al objeto `Model`, que luego están disponibles en la vista.

```java
@GetMapping("/lista")
public String listar(Model model) { 
    model.addAttribute("productos", service.findAll()); 
    return "productos/lista"; 
}
```

> [!TIP]
> En Thymeleaf, se accede a estos datos con la sintaxis `${productos}`.

---

## Thymeleaf: Motor Estándar

Thymeleaf es el motor predilecto en Spring Boot por su capacidad de renderizado "natural" y su integración nativa.

- **Plantillas Prototípicas:** El HTML es válido y puede abrirse en un navegador sin servidor.
- **Fragmentos:** Permite reutilizar componentes mediante `th:fragment`.
- **Formularios:** Integración total con `th:field` y `th:errors` para mostrar resultados de validación.

---

## Redirecciones y Flash Attributes

Para seguir el patrón **POST-redirect-GET**, se utiliza el prefijo `redirect:`.

```java
@PostMapping
public String crear(@Valid Producto p, BindingResult result, RedirectAttributes ra) {
    if (result.hasErrors()) return "productos/formulario";
    service.save(p);
    ra.addFlashAttribute("success", "Producto creado correctamente");
    return "redirect:/productos";
}
```

---

## Resolución Híbrida y REST

- En un `@RestController`, todos los métodos son `@ResponseBody` por defecto.
- En un `@Controller`, se puede mezclar la devolución de vistas con respuestas JSON/XML anotando métodos específicos con `@ResponseBody`.
- Spring Boot sirve recursos estáticos automáticamente desde carpetas como `/static` o `/public`.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Manejo de Excepciones](./Manejo_de_Excepciones.md) | [Índice](../../index.md) | [Vistas y Templates](./Vistas_y_Templates.md) |

