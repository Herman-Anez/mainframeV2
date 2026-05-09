# Seguridad a Nivel de Método

La seguridad a nivel de método proporciona una capa de defensa adicional, controlando la invocación de métodos de servicio en lugar de solo URLs. Esto es fundamental para asegurar que la lógica de negocio esté protegida independientemente de cómo se acceda a ella.

## Habilitar la Seguridad de Método

Se habilita añadiendo `@EnableMethodSecurity` (o `@EnableGlobalMethodSecurity` en versiones anteriores) en una clase de configuración.

```java
@Configuration
@EnableMethodSecurity(securedEnabled = true, prePostEnabled = true)
public class MethodSecurityConfig { }
```

*   **`securedEnabled`**: Permite el uso de `@Secured`.
*   **`prePostEnabled`**: Permite el uso de `@PreAuthorize` / `@PostAuthorize`.
*   **`jsr250Enabled`**: Habilita el soporte para `@RolesAllowed` (estándar JSR-250).

## @Secured y @RolesAllowed

`@Secured("ROLE_ADMIN")` verifica que el usuario tenga el rol indicado. No permite expresiones complejas; solo una lista de roles (usando lógica OR). `@RolesAllowed` es equivalente pero sigue el estándar JSR-250.

```java
public interface ProductoService {
    @Secured("ROLE_ADMIN")
    void eliminarProducto(Long id);
}
```

## @PreAuthorize y @PostAuthorize

Permiten usar el **Spring Security Expression Language (SpEL)** para implementar lógica de seguridad compleja.

*   **`@PreAuthorize`**: Se evalúa antes de ejecutar el método. Deniega el acceso si la expresión es falsa.
*   **`@PostAuthorize`**: Se evalúa después de la ejecución. Útil para aplicar permisos basados en el objeto retornado (`returnObject`). Si falla, el resultado no se devuelve al cliente.

### Ejemplos de Uso

```java
@PreAuthorize("hasRole('ADMIN') or hasAuthority('PRODUCTO_ESCRITURA')")
public Producto crear(Producto p) { ... }

@PreAuthorize("#id != null and @productoService.esPropietario(#id, authentication.principal.username)")
public Producto actualizarPrecio(Long id, BigDecimal precio) { ... }

@PostAuthorize("returnObject.usuario == authentication.name")
public Pedido obtenerPedido(Long id) { ... }

@PreAuthorize("hasRole('USER') and #producto.precio < 1000")
public void aplicarDescuento(Producto producto) { ... }
```

> [!NOTE]
> En las expresiones SpEL se puede acceder a:
> *   Parámetros del método con `#nombreParam`.
> *   El objeto retornado en `@PostAuthorize` con `returnObject`.
> *   Beans de Spring con `@nombreBean`.
> *   El principal (usuario) actual con `authentication`.

## @PreFilter y @PostFilter

Filtran colecciones pasadas como argumentos o devueltas por un método.

*   **`@PreFilter`**: Filtra elementos de una colección de entrada. El elemento actual se referencia con `filterObject`.
*   **`@PostFilter`**: Filtra la colección de salida.

```java
@PreFilter("filterObject.propietario == authentication.name")
public void guardarVarios(List<Documento> docs) { ... }

@PostFilter("hasPermission(filterObject, 'READ')")
public List<Documento> listarDocumentos() { ... }
```

> [!WARNING]
> Estas anotaciones pueden tener un impacto significativo en el rendimiento si se aplican sobre colecciones muy grandes.

## Consideraciones de Implementación

### Servicios vs Controladores
A menudo se aplica en la capa de servicio para mantener los controladores ligeros. Esto asegura que si la lógica de negocio se reutiliza (tareas programadas, colas de mensajería), la seguridad se aplique de forma consistente.

### Manejo de Excepciones
Cuando una expresión de seguridad falla, se lanza `AuthorizationDeniedException`. Se puede capturar globalmente con un `@ControllerAdvice` para devolver una respuesta HTTP 403 (Forbidden).

### Proxies y Auto-invocación
La seguridad de método se basa en Spring AOP (proxies). Por lo tanto:
1.  El método debe ser **público**.
2.  La llamada debe provenir de **fuera del bean** (la auto-invocación dentro de la misma clase salta el proxy y, por ende, la seguridad).

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Configuración DSL](./Configuracion_DSL.md) | [Índice](../../index.md) | [JWT y OAuth2](./JWT_y_OAuth2.md) |
