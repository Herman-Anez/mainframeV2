# Seguridad/Metodo_Security.md
Habilitar la seguridad a nivel de método

La seguridad a nivel de método proporciona una capa de defensa adicional, controlando la invocación de métodos de servicio en lugar de solo URLs. Se habilita añadiendo @EnableMethodSecurity (o @EnableGlobalMethodSecurity en versiones anteriores) en una clase de configuración.
java

@Configuration
@EnableMethodSecurity(securedEnabled = true, prePostEnabled = true)
public class MethodSecurityConfig { }

    securedEnabled permite @Secured.

    prePostEnabled permite @PreAuthorize / @PostAuthorize.

    jsr250Enabled para @RolesAllowed.

@Secured y @RolesAllowed

@Secured("ROLE_ADMIN") verifica que el usuario tenga el rol indicado. No permite expresiones; solo una lista de roles (usando lógica OR). @RolesAllowed es equivalente pero sigue el estándar JSR-250.
java

public interface ProductoService {
    @Secured("ROLE_ADMIN")
    void eliminarProducto(Long id);
}

@PreAuthorize y @PostAuthorize: la potencia de las expresiones

Permiten usar el Spring Security Expression Language (SpEL) para lógica compleja.

    @PreAuthorize: antes de ejecutar el método. Evalúa la expresión y deniega el acceso si no se cumple.

    @PostAuthorize: después de ejecutar el método. El método se ejecuta, y luego se evalúa la expresión sobre el objeto retornado (útil para permisos en base al resultado). Si falla, el resultado no se devuelve.

Ejemplos:
java

@PreAuthorize("hasRole('ADMIN') or hasAuthority('PRODUCTO_ESCRITURA')")
public Producto crear(Producto p) { ... }

@PreAuthorize("#id != null and @productoService.esPropietario(#id, authentication.principal.username)")
public Producto actualizarPrecio(Long id, BigDecimal precio) { ... }

@PostAuthorize("returnObject.usuario == authentication.name")
public Pedido obtenerPedido(Long id) { ... }

@PreAuthorize("hasRole('USER') and #producto.precio < 1000")
public void aplicarDescuento(Producto producto) { ... }

En las expresiones se puede acceder a:

    Parámetros del método con #nombreParam.

    El objeto retornado en @PostAuthorize con returnObject.

    Beans de Spring con @nombreBean (p.ej. @seguridadService).

    El principal actual con authentication.

@PreFilter y @PostFilter

Filtran colecciones pasadas como argumentos o devueltas. Muy potentes pero con impacto en rendimiento si las colecciones son grandes.

    @PreFilter: filtra elementos de una colección de entrada usando una expresión. El elemento actual se referencia con filterObject.

    @PostFilter: filtra la colección de salida.

java

@PreFilter("filterObject.propietario == authentication.name")
public void guardarVarios(List<Documento> docs) { ... }

@PostFilter("hasPermission(filterObject, 'READ')")
public List<Documento> listarDocumentos() { ... }

Seguridad en servicios y controladores

A menudo se aplica en la capa de servicio, manteniendo los controladores ligeros. Así, si la lógica de negocio se reutiliza desde otros puntos (tareas programadas, mensajería), la seguridad se aplica igual. La anotación debe estar en la interfaz o en la implementación concreta; lo habitual es en la implementación.
Manejo de excepciones de seguridad a nivel de método

Cuando una expresión de seguridad falla, se lanza AuthorizationDeniedException. Se puede capturar globalmente con un @ControllerAdvice junto con @ExceptionHandler para convertirla en una respuesta HTTP adecuada (403 Forbidden).
Consideraciones de proxy

La seguridad a nivel de método se basa en AOP (proxies). Por tanto, aplican las mismas reglas: la anotación debe estar en un método público y la llamada debe provenir de fuera del bean (no por auto-invocación). Para casos de auto-invocación, se puede extraer a otro bean o usar @EnableAspectJAutoProxy(exposeProxy = true) y llamar a través de AopContext.currentProxy().


