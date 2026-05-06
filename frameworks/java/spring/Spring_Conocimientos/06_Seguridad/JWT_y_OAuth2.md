
# Seguridad/JWT_y_OAuth2.md
OAuth2: roles y flujos

OAuth2 es el estándar de facto para delegación de acceso. Sus protagonistas:

    Resource Owner (el usuario).

    Client (la aplicación que quiere acceder).

    Authorization Server (emite tokens).

    Resource Server (la API protegida).

Flujos más usados:

    Authorization Code (con PKCE): para aplicaciones web y móviles. El cliente redirige al servidor de autorización, el usuario autentica y consiente, se devuelve un código que el cliente canjea por un token.

    Client Credentials: para comunicación máquina a máquina.

    Refresh Token: para renovar access tokens sin molestar al usuario.

JSON Web Tokens (JWT)

Un token JWT (JSON Web Token) es una cadena codificada en Base64 que contiene tres partes:
header.payload.signature

    Header: algoritmo de firma (HS256, RS256).

    Payload: claims (sub, iss, exp, roles, scopes, etc.).

    Signature: garantiza integridad y autenticidad.

Ventajas: autocontenido, no requiere almacenamiento en el servidor, ideal para servicios distribuidos y stateless.
Spring Security como Resource Server

Con Spring Boot y el starter spring-boot-starter-oauth2-resource-server, configurar un resource server JWT es trivial:
properties

spring.security.oauth2.resourceserver.jwt.issuer-uri=https://auth-server.com/realms/mi-realm

O manualmente:
java

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

Spring Security valida automáticamente la firma, la expiración, el issuer, etc. usando las propiedades o un JwtDecoder.
Conversión de JWT a Authentication

Por defecto, el framework mapea los scopes del JWT a GrantedAuthority con prefijo SCOPE_. Si tu token tiene roles personalizados, puedes definir un JwtAuthenticationConverter:
java

@Bean
public JwtAuthenticationConverter jwtAuthenticationConverter() {
    JwtGrantedAuthoritiesConverter grantedAuthoritiesConverter = new JwtGrantedAuthoritiesConverter();
    grantedAuthoritiesConverter.setAuthoritiesClaimName("roles");
    grantedAuthoritiesConverter.setAuthorityPrefix("ROLE_");
    JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
    converter.setJwtGrantedAuthoritiesConverter(grantedAuthoritiesConverter);
    return converter;
}

Authorization Server con Spring Authorization Server

Para emitir tokens JWT, Spring proporciona el proyecto spring-authorization-server. Se configura con un RegisteredClientRepository y una AuthorizationServerSettings:
java

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

Pero para muchos escenarios, se usa Keycloak, Okta o Auth0 como servidores de autorización externos.
Implementación completa de login con JWT en un cliente

No siempre necesitas un authorization server propio. Si implementas autenticación local generando tus propios JWT:

    AuthenticationController: recibe credenciales, valida con AuthenticationManager, genera un JWT (usando librería jjwt o nimbus-jose-jwt) y lo devuelve al cliente.

    JwtAuthenticationFilter (heredado de OncePerRequestFilter): lee el token de la cabecera Authorization: Bearer ..., lo parsea, valida firma/expiración, carga el usuario (opcional) y establece el SecurityContext.

    Configurar el filtro en la cadena antes de los filtros de autorización.

Ejemplo de filtro simplificado:
java

public class JwtTokenFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {
        String header = request.getHeader("Authorization");
        if (header != null && header.startsWith("Bearer ")) {
            String token = header.substring(7);
            // validar token y extraer claims
            String username = JwtUtils.getUsername(token);
            if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
                // cargar UserDetails y crear Authentication
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

Y en la configuración:
java

http.addFilterBefore(jwtTokenFilter, UsernamePasswordAuthenticationFilter.class);

OAuth2 Client (login social)

Con spring-boot-starter-oauth2-client y propiedades:
properties

spring.security.oauth2.client.registration.google.client-id=...
spring.security.oauth2.client.registration.google.client-secret=...

Spring Security expone automáticamente /oauth2/authorization/google y gestiona la redirección, el canje del código y la creación del OAuth2AuthenticationToken. Se puede personalizar el OAuth2UserService para mapear a tu propio modelo de usuario.
