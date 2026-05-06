# Arquitectura de Spring Security

La cadena de filtros es el núcleo de Spring Security. El framework se basa en una cadena de filtros del contenedor de servlets que actúa anticipándose al `DispatcherServlet`.

## La Cadena de Filtros (Filter Chain)

Un único punto de entrada, `DelegatingFilterProxy`, se registra en el `web.xml` (o automáticamente por Spring Boot) y delega todas las peticiones a un bean llamado `springSecurityFilterChain`, que es una `FilterChainProxy`. 

Esta `FilterChainProxy` contiene una lista de cadenas de seguridad (`SecurityFilterChain`) que pueden aplicar diferentes configuraciones según la URL (por ejemplo, una para APIs REST y otra para páginas web).

## Componentes Principales del Flujo

> [!IMPORTANT]
> Entender estos componentes es vital para personalizar la seguridad en Spring.

*   **`SecurityContextHolder`**: Donde Spring Security almacena los detalles del principal autenticado. Por defecto utiliza una estrategia `ThreadLocal` para mantener el contexto ligado al hilo de la petición.
*   **`SecurityContext`**: Contiene un objeto `Authentication`.
*   **`Authentication`**: Representa el token de autenticación. Puede ser el estado previo a la autenticación (con las credenciales) o posterior (con los permisos y el principal).
    *   **principal**: Normalmente un `UserDetails`.
    *   **credentials**: La contraseña o token.
    *   **authorities**: Los roles/permisos (`GrantedAuthority`).
*   **`AuthenticationManager`**: Interfaz central que recibe un `Authentication` no autenticado y devuelve uno completamente autenticado. Su implementación principal, `ProviderManager`, itera sobre una lista de `AuthenticationProviders`.
*   **`AuthenticationProvider`**: Cada uno sabe autenticar un tipo específico de token (ej. `DaoAuthenticationProvider` para usuario/contraseña contra base de datos, `JwtAuthenticationProvider` para tokens JWT, `LdapAuthenticationProvider`, etc.).
*   **`UserDetailsService`**: Colaborador de `DaoAuthenticationProvider`. Carga un `UserDetails` (usuario, contraseña, roles) desde cualquier fuente (base de datos, memoria, LDAP). Spring Security solo pide `loadUserByUsername(String)`.

## Flujo Típico de Autenticación (Usuario/Contraseña)

1.  El filtro `UsernamePasswordAuthenticationFilter` (por defecto en `/login`) intercepta una petición POST con username y password.
2.  Crea un `UsernamePasswordAuthenticationToken` no autenticado.
3.  Llama al `AuthenticationManager` (`ProviderManager`).
4.  `ProviderManager` busca un `AuthenticationProvider` que soporte ese token. Encuentra `DaoAuthenticationProvider`.
5.  `DaoAuthenticationProvider` llama a `UserDetailsService.loadUserByUsername()` para obtener el `UserDetails`.
6.  El `PasswordEncoder` verifica la contraseña enviada contra la almacenada.
7.  Si concuerda, se crea un nuevo `UsernamePasswordAuthenticationToken` con el principal, los `GrantedAuthority` y `authenticated = true`.
8.  Se establece en el `SecurityContext` y se devuelve.
9.  En peticiones subsiguientes, el `SecurityContextPersistenceFilter` (o en sesiones, el `SecurityContextRepository`) restaura el contexto a partir de la sesión HTTP.

## Autorización: Acceso a Recursos

La autorización ocurre después de la autenticación, mediante la configuración `HttpSecurity` y en tiempo de petición:

*   **`FilterSecurityInterceptor`** (o `AuthorizationFilter` en versiones recientes): Es el último filtro de la cadena y lanza `AccessDeniedException` si el usuario no tiene los permisos requeridos.
*   La decisión se basa en los `GrantedAuthority` del `Authentication` y en las reglas expresadas en la configuración (`.hasRole("ADMIN")`, `.authenticated()`, etc.).

## Tratamiento de Excepciones

*   **`AuthenticationEntryPoint`**: Se invoca cuando un usuario no autenticado intenta acceder a un recurso protegido. En una API REST devuelve HTTP 401, en una aplicación web redirige a la página de login.
*   **`AccessDeniedHandler`**: Se ejecuta cuando un usuario autenticado no tiene permisos suficientes (HTTP 403).

## Contexto en Aplicaciones REST y Stateless

> [!NOTE]
> En aplicaciones REST modernas, es común desactivar el manejo de estado de sesión.

En REST no hay sesiones HTTP. La configuración se vuelve `SessionCreationPolicy.STATELESS`. Se reemplaza la autenticación basada en sesiones por tokens (JWT). Un filtro personalizado (por ejemplo, `JwtAuthenticationFilter`) extrae el token de la cabecera `Authorization`, lo valida y establece el `SecurityContext` para esa petición. Al ser sin sesión, el contexto no se persiste, y el filtro debe ejecutarse en cada petición.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Transacciones y @Transactional](../05_Acceso_Datos/Transacciones_y_Transactional.md) | [Índice](../../README.md) | [Configuración DSL y HttpSecurity](Configuracion_DSL.md) |

