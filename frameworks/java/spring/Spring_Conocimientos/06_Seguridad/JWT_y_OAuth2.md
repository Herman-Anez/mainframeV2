# JWT y OAuth2 en Spring Security

OAuth2 es el estándar de facto para la delegación de acceso, permitiendo que las aplicaciones obtengan acceso limitado a las cuentas de usuario en un servicio HTTP.

## OAuth2: Roles y Flujos

En el ecosistema de OAuth2, existen cuatro protagonistas principales:

*   **Resource Owner**: El usuario final.
*   **Client**: La aplicación que desea acceder a los recursos del usuario.
*   **Authorization Server**: El servidor que emite los tokens tras validar la identidad del usuario.
*   **Resource Server**: La API que protege los recursos y acepta tokens válidos.

### Flujos (Grants) más Comunes

1.  **Authorization Code (con PKCE)**: El flujo recomendado para aplicaciones web y móviles. Incluye redirección, consentimiento del usuario y canje de un código por un token.
2.  **Client Credentials**: Utilizado para la comunicación directa entre servicios (máquina a máquina).
3.  **Refresh Token**: Permite obtener nuevos access tokens sin que el usuario deba volver a autenticarse.

---

## JSON Web Tokens (JWT)

Un JWT es un estándar abierto (RFC 7519) que define una forma compacta y autónoma de transmitir información entre partes como un objeto JSON.

### Estructura de un JWT
Se compone de tres partes codificadas en Base64 y separadas por puntos (`header.payload.signature`):

*   **Header**: Contiene el tipo de token y el algoritmo de firma (ej. HS256, RS256).
*   **Payload**: Contiene los *claims* (datos del usuario, fecha de expiración, roles, scopes).
*   **Signature**: Utilizada para verificar que el remitente del JWT es quien dice ser y para asegurar que el mensaje no fue alterado.

> [!NOTE]
> Los JWT son ideales para arquitecturas distribuidas y stateless, ya que el servidor no necesita almacenar el estado de la sesión.

---

## Spring Security como Resource Server

Configurar un Resource Server para validar tokens JWT es directo con `spring-boot-starter-oauth2-resource-server`.

### Configuración vía Propiedades

```properties
spring.security.oauth2.resourceserver.jwt.issuer-uri=https://auth-server.com/realms/mi-realm
```

### Configuración Programática

```java
@Bean
public SecurityFilterChain resourceServerFilter(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/api/public").permitAll()
            .anyRequest().authenticated()
        )
        .oauth2ResourceServer(oauth2 -> oauth2.jwt(
            jwt -> jwt.jwtAuthenticationConverter(jwtAuthenticationConverter())
        ));
    return http.build();
}
```

### Conversión de JWT a Authentication
Por defecto, Spring mapea los *scopes* a autoridades con el prefijo `SCOPE_`. Para usar roles personalizados:

```java
@Bean
public JwtAuthenticationConverter jwtAuthenticationConverter() {
    JwtGrantedAuthoritiesConverter grantedAuthoritiesConverter = new JwtGrantedAuthoritiesConverter();
    grantedAuthoritiesConverter.setAuthoritiesClaimName("roles");
    grantedAuthoritiesConverter.setAuthorityPrefix("ROLE_");
    
    JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
    converter.setJwtGrantedAuthoritiesConverter(grantedAuthoritiesConverter);
    return converter;
}
```

---

## Authorization Server

Para emitir tokens propios, se utiliza el proyecto **Spring Authorization Server**.

```java
@Bean
public RegisteredClientRepository registeredClientRepository() {
    RegisteredClient client = RegisteredClient.withId(UUID.randomUUID().toString())
        .clientId("mi-cliente")
        .clientSecret("{noop}secret")
        .authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
        .authorizationGrantType(AuthorizationGrantType.REFRESH_TOKEN)
        .redirectUri("http://localhost:8080/login/oauth2/code/mi-cliente")
        .scope("openid").scope("profile")
        .clientSettings(ClientSettings.builder().requireAuthorizationConsent(true).build())
        .build();
    return new InMemoryRegisteredClientRepository(client);
}
```

> [!TIP]
> En entornos de producción, es común delegar esta responsabilidad a soluciones como Keycloak, Auth0 o Okta.

---

## Implementación de Autenticación Local con JWT

Si decides generar tus propios tokens sin un Authorization Server completo:

1.  **AuthenticationController**: Valida credenciales y devuelve el JWT generado.
2.  **JwtAuthenticationFilter**: Un filtro que extiende de `OncePerRequestFilter` para procesar el token en cada petición.

### Ejemplo de Filtro JWT

```java
public class JwtTokenFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {
        String header = request.getHeader("Authorization");
        if (header != null && header.startsWith("Bearer ")) {
            String token = header.substring(7);
            String username = JwtUtils.getUsername(token);
            if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
                UserDetails userDetails = userDetailsService.loadUserByUsername(username);
                UsernamePasswordAuthenticationToken auth =
                    new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
                auth.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                SecurityContextHolder.getContext().setAuthentication(auth);
            }
        }
        chain.doFilter(request, response);
    }
}
```

### Registro del Filtro

```java
http.addFilterBefore(jwtTokenFilter, UsernamePasswordAuthenticationFilter.class);
```

---

## OAuth2 Client (Login Social)

Para habilitar login con Google o GitHub basta con añadir el starter `spring-boot-starter-oauth2-client` y configurar las credenciales:

```properties
spring.security.oauth2.client.registration.google.client-id=TU_CLIENT_ID
spring.security.oauth2.client.registration.google.client-secret=TU_CLIENT_SECRET
```

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Seguridad a Nivel de Método](./Metodo_Security.md) | [Índice](../../index.md) | [Batch y Tareas Programadas](../07_Temas_Avanzados/Batch_y_Tareas_Programadas.md) |

