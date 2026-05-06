# Seguridad/Spring_Security_Arquitectura.md
La cadena de filtros: el núcleo de Spring Security

Spring Security se basa en una cadena de filtros del contenedor de servlets, anticipándose al DispatcherServlet. Un único punto de entrada, DelegatingFilterProxy, se registra en el web.xml (o automáticamente por Spring Boot) y delega todas las peticiones a un bean llamado springSecurityFilterChain, que es una FilterChainProxy. Esta FilterChainProxy contiene una lista de cadenas de seguridad (SecurityFilterChain) que pueden aplicar diferentes configuraciones según la URL (por ejemplo, una para APIs REST y otra para páginas web).
Componentes principales del flujo de autenticación

    SecurityContextHolder: donde Spring Security almacena los detalles del principal autenticado. Por defecto utiliza una estrategia ThreadLocal para mantener el contexto ligado al hilo de la petición.

    SecurityContext: contiene un objeto Authentication.

    Authentication: representa el token de autenticación. Puede ser el estado previo a la autenticación (con las credenciales) o posterior (con los permisos y el principal).

        principal: normalmente un UserDetails.

        credentials: la contraseña o token.

        authorities: los roles/permisos (GrantedAuthority).

    AuthenticationManager: interfaz central que recibe un Authentication no autenticado y devuelve uno completamente autenticado. Su implementación principal, ProviderManager, itera sobre una lista de AuthenticationProviders.

    AuthenticationProvider: cada uno sabe autenticar un tipo específico de token (ej. DaoAuthenticationProvider para usuario/contraseña contra base de datos, JwtAuthenticationProvider para tokens JWT, LdapAuthenticationProvider, etc.).

    UserDetailsService: colaborador de DaoAuthenticationProvider. Carga un UserDetails (usuario, contraseña, roles) desde cualquier fuente (base de datos, memoria, LDAP). Spring Security solo pide loadUserByUsername(String).

Flujo típico de autenticación por usuario/contraseña

    El filtro UsernamePasswordAuthenticationFilter (por defecto en /login) intercepta una petición POST con username y password.

    Crea un UsernamePasswordAuthenticationToken no autenticado.

    Llama al AuthenticationManager (ProviderManager).

    ProviderManager busca un AuthenticationProvider que soporte ese token. Encuentra DaoAuthenticationProvider.

    DaoAuthenticationProvider llama a UserDetailsService.loadUserByUsername() para obtener el UserDetails.

    El PasswordEncoder verifica la contraseña enviada contra la almacenada.

    Si concuerda, se crea un nuevo UsernamePasswordAuthenticationToken con el principal, los GrantedAuthority y authenticated = true.

    Se establece en el SecurityContext y se devuelve.

    En peticiones subsiguientes, el SecurityContextPersistenceFilter (o en sesiones, el SecurityContextRepository) restaura el contexto a partir de la sesión HTTP.

Autorización: acceso a recursos

La autorización ocurre después de la autenticación, mediante la configuración HttpSecurity y en tiempo de petición:

    FilterSecurityInterceptor (o AuthorizationFilter en versiones recientes): es el último filtro de la cadena y lanza AccessDeniedException si el usuario no tiene los permisos requeridos.

    La decisión se basa en los GrantedAuthority del Authentication y en las reglas expresadas en la configuración (.hasRole("ADMIN"), .authenticated(), etc.).

Tratamiento de excepciones

    AuthenticationEntryPoint: se invoca cuando un usuario no autenticado intenta acceder a un recurso protegido. En una API REST devuelve HTTP 401, en una aplicación web redirige a la página de login.

    AccessDeniedHandler: se ejecuta cuando un usuario autenticado no tiene permisos suficientes (HTTP 403).

Contexto para aplicaciones REST y stateless

En REST no hay sesiones HTTP. La configuración se vuelve SessionCreationPolicy.STATELESS. Se reemplaza la autenticación basada en sesiones por tokens (JWT). Un filtro personalizado (por ejemplo, JwtAuthenticationFilter) extrae el token de la cabecera Authorization, lo valida y establece el SecurityContext para esa petición. Al ser sin sesión, el contexto no se persiste, y el filtro debe ejecutarse en cada petición.
