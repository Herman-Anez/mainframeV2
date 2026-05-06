# Seguridad/Configuracion_DSL.md
De WebSecurityConfigurerAdapter a SecurityFilterChain

Desde Spring Security 5.7, la forma moderna de configurar la seguridad es declarando beans de tipo SecurityFilterChain y usando la DSL fluida de HttpSecurity. Adiós a la herencia.
java

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

authorizeHttpRequests y la nueva sintaxis

A partir de Spring Security 6, se recomienda authorizeHttpRequests sobre authorizeRequests, usando AuthorizationManager internamente. La DSL es muy legible:

    requestMatchers("/url").permitAll(): acceso libre.

    .hasRole("ADMIN"): requiere rol (prefijo ROLE_ automático).

    .hasAuthority("SCOPE_read"): para authority exacta.

    .hasAnyRole("ADMIN", "USER"): múltiples roles.

    .authenticated(): solo requiere autenticado.

    Se pueden encadenar marcadores específicos como dispatcherTypeMatchers, etc.

Ejemplo de restricción por método HTTP y patrón:
java

.requestMatchers(HttpMethod.POST, "/api/productos/**").hasRole("EDITOR")
.requestMatchers("/api/usuarios/**").hasRole("ADMIN")

Configuración de login y logout

    FormLogin: personaliza la página de login y las URLs de procesamiento. En REST puro, se suele deshabilitar con http.formLogin(AbstractHttpConfigurer::disable).

    HttpBasic: autenticación HTTP Basic. Útil para APIs internas o pruebas.

    OAuth2Login: configura el login delegado con Google, GitHub, etc., usando spring-boot-starter-oauth2-client.

    Logout: define la URL de logout, invalidación de sesión, eliminación de cookies.

CORS y CSRF

    CORS: Spring Security aplica una capa adicional a la configuración global de CORS de Spring MVC. Se puede personalizar con http.cors(cors -> cors.configurationSource(...)).

    CSRF: protección por defecto para formularios. En REST stateless con JWT, normalmente se deshabilita: http.csrf(AbstractHttpConfigurer::disable). Pero antes de deshabilitarlo, considera la vulnerabilidad: si no usas cookies para autenticación, CSRF no aplica.

Configuración de múltiples SecurityFilterChain

Cuando coexisten una API REST y una aplicación web MVC, se pueden definir dos SecurityFilterChain beans con diferentes prioridades (@Order). Por ejemplo, una cadena para /api/** sin estado y otra para el resto con login de formulario.
java

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

Personalización del UserDetailsService y PasswordEncoder
java

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

Spring Boot detecta un PasswordEncoder y lo inyecta automáticamente.
Configuración de AuthenticationManager para casos complejos

Si necesitas exponer el AuthenticationManager (por ejemplo, para autenticar programáticamente en un controlador), puedes definirlo como bean. Con Spring Boot, AuthenticationConfiguration lo expone:
java

@Bean
public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
    return config.getAuthenticationManager();
}
