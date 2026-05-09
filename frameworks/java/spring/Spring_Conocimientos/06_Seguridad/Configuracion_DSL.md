g# Configuración DSL y HttpSecurity

Desde Spring Security 5.7, la forma moderna de configurar la seguridad es declarando beans de tipo `SecurityFilterChain` y usando la DSL fluida de `HttpSecurity`. Se ha abandonado el uso de la herencia (`WebSecurityConfigurerAdapter`).

## De WebSecurityConfigurerAdapter a SecurityFilterChain

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authz -> authz
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .formLogin(form -> form
                .loginPage("/login")
                .permitAll()
            )
            .logout(logout -> logout
                .logoutSuccessUrl("/")
            )
            .oauth2Login(Customizer.withDefaults());
        return http.build();
    }
}
```

## authorizeHttpRequests y la Nueva Sintaxis

A partir de Spring Security 6, se recomienda `authorizeHttpRequests` sobre `authorizeRequests`, usando `AuthorizationManager` internamente. La DSL es altamente legible:

*   **`requestMatchers("/url").permitAll()`**: Acceso libre a la URL especificada.
*   **`.hasRole("ADMIN")`**: Requiere un rol específico (el prefijo `ROLE_` se añade automáticamente).
*   **`.hasAuthority("SCOPE_read")`**: Para una autoridad exacta sin prefijos automáticos.
*   **`.hasAnyRole("ADMIN", "USER")`**: Permite múltiples roles.
*   **`.authenticated()`**: Requiere que el usuario esté autenticado, sin importar el rol.

> [!TIP]
> Se pueden encadenar marcadores específicos como `dispatcherTypeMatchers` para controlar el flujo interno de los servlets.

### Restricción por Método HTTP

```java
.requestMatchers(HttpMethod.POST, "/api/productos/**").hasRole("EDITOR")
.requestMatchers("/api/usuarios/**").hasRole("ADMIN")
```

## Configuración de Login y Logout

*   **FormLogin**: Personaliza la página de login y las URLs de procesamiento. En REST puro, se suele deshabilitar con `http.formLogin(AbstractHttpConfigurer::disable)`.
*   **HttpBasic**: Autenticación HTTP Basic. Útil para APIs internas o pruebas rápidas.
*   **OAuth2Login**: Configura el login delegado con proveedores externos (Google, GitHub, etc.), usando `spring-boot-starter-oauth2-client`.
*   **Logout**: Define la URL de logout, invalidación de sesión y eliminación de cookies.

## CORS y CSRF

*   **CORS**: Spring Security aplica una capa adicional a la configuración global de CORS de Spring MVC. Se puede personalizar con `http.cors(cors -> cors.configurationSource(...))`.
*   **CSRF**: Protección por defecto para formularios. En REST stateless con JWT, normalmente se deshabilita: `http.csrf(AbstractHttpConfigurer::disable)`. 

> [!WARNING]
> Antes de deshabilitar CSRF, considera la vulnerabilidad: si no usas cookies para autenticación, CSRF no aplica; de lo contrario, debe permanecer activo.

## Configuración de Múltiples SecurityFilterChain

Cuando coexisten una API REST y una aplicación web MVC, se pueden definir dos beans `SecurityFilterChain` con diferentes prioridades (`@Order`).

```java
@Bean
@Order(1)
public SecurityFilterChain apiFilterChain(HttpSecurity http) throws Exception {
    http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
        .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .csrf(AbstractHttpConfigurer::disable);
    return http.build();
}

@Bean
@Order(2)
public SecurityFilterChain webFilterChain(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/css/**", "/js/**").permitAll()
            .anyRequest().authenticated()
        )
        .formLogin(Customizer.withDefaults());
    return http.build();
}
```

## Personalización de Beans de Seguridad

### UserDetailsService y PasswordEncoder

```java
@Bean
public UserDetailsService userDetailsService(UserRepository userRepo) {
    return username -> userRepo.findByUsername(username)
        .map(user -> User.withUsername(user.getUsername())
                .password(user.getPassword())
                .roles(user.getRoles().toArray(String[]::new))
                .build())
        .orElseThrow(() -> new UsernameNotFoundException(username));
}

@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder();
}
```

Spring Boot detecta automáticamente un `PasswordEncoder` declarado como bean y lo inyecta en el flujo de autenticación.

### AuthenticationManager para Casos Complejos

Si necesitas exponer el `AuthenticationManager` para realizar autenticación programática en un controlador, puedes obtenerlo de la `AuthenticationConfiguration`.

```java
@Bean
public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
    return config.getAuthenticationManager();
}
```

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Arquitectura de Seguridad](./Spring_Security_Arquitectura.md) | [Índice](../../index.md) | [Seguridad a Nivel de Método](./Metodo_Security.md) |

