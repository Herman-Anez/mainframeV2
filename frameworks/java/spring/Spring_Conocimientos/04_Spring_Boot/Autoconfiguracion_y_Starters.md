# Spring_Boot/Autoconfiguracion_y_Starters.md
El problema que resolvió Spring Boot

Spring tradicional daba una flexibilidad enorme, pero configurar una aplicación sencilla requería decenas de líneas de XML o Java Config para beans de infraestructura: DataSource, EntityManagerFactory, TransactionManager, ViewResolver, MessageConverter, etc. Spring Boot introdujo dos conceptos rompedores:

    Starters: dependencias agrupadoras que traen todo el classpath necesario y autoconfiguración preparada.

    Autoconfiguración (@EnableAutoConfiguration): basada en lo que hay en el classpath, la aplicación decide qué beans crear y cómo configurarlos, siguiendo el principio "convención sobre configuración".

La anotación @SpringBootApplication

Es un atajo que combina tres anotaciones:
java

@SpringBootConfiguration  // = @Configuration en contexto Boot
@EnableAutoConfiguration  // La magia de la autoconfiguración
@ComponentScan(            // Escanea el paquete actual y subpaquetes
    excludeFilters = { @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class) }
)
public @interface SpringBootApplication {

Así que en una sola línea activas la configuración Java, el escaneo de componentes y la autoconfiguración.
Funcionamiento interno de la autoconfiguración

    @EnableAutoConfiguration importa AutoConfigurationImportSelector.

    Este selector carga todas las clases listadas en el archivo META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports (en Spring Boot 3+) o en spring.factories (versiones anteriores) del classpath.

    Cada una de esas clases es una configuración (anotada con @AutoConfiguration o @Configuration) con anotaciones condicionales.

    Anotaciones condicionales (@ConditionalOnClass, @ConditionalOnMissingBean, @ConditionalOnProperty, etc.) deciden si la configuración se aplica o no.

    Si se aplica, se definen los beans óptimos para la aplicación.

Ejemplo simplificado de lo que hace DataSourceAutoConfiguration:

    @ConditionalOnClass({ DataSource.class, EmbeddedDatabaseType.class }) → solo si hay clases JDBC en el classpath.

    @ConditionalOnMissingBean(DataSource.class) → solo si el usuario no ha definido ya un DataSource.

    Si se cumple, crea un DataSource usando las propiedades spring.datasource.*. Si no hay propiedades de conexión, Boot intenta crear una base de datos embebida (H2, Derby) si encuentra esas dependencias.

Anotaciones condicionales más poderosas
Anotación	Condición
@ConditionalOnClass	Si una clase específica está en el classpath.
@ConditionalOnMissingClass	Si una clase NO está.
@ConditionalOnBean	Si existe un bean de ese tipo.
@ConditionalOnMissingBean	Si NO existe un bean.
@ConditionalOnProperty	Si una propiedad tiene un valor determinado.
@ConditionalOnResource	Si existe un recurso (archivo).
@ConditionalOnWebApplication	Si es una aplicación web.
@ConditionalOnNotWebApplication	No web.
@ConditionalOnExpression	Expresión SpEL evaluada a true.

Estas anotaciones se pueden combinar en una misma clase de autoconfiguración para afinar la activación.
Starters: la navaja suiza del classpath

Un starter es un POM (Maven) o módulo (Gradle) que agrupa varias dependencias relacionadas entre sí, evitando que tengas que añadirlas una a una y garantizando compatibilidad de versiones. La convención de nombres es spring-boot-starter-*. Ejemplos esenciales:
Starter	Proporciona
spring-boot-starter-web	Spring MVC, Tomcat embebido, Jackson, validación.
spring-boot-starter-data-jpa	Hibernate, Spring Data JPA, Spring ORM, pool HikariCP.
spring-boot-starter-security	Spring Security, autenticación básica por defecto.
spring-boot-starter-test	JUnit Jupiter, Mockito, AssertJ, Hamcrest, Spring Test.
spring-boot-starter-actuator	Endpoints de monitoreo (health, metrics).
spring-boot-starter-thymeleaf	Thymeleaf, Spring Web.
spring-boot-starter-oauth2-client	OAuth2 client support.
spring-boot-starter-webflux	Programación reactiva con Netty.

Cada starter trae también la autoconfiguración correspondiente (en spring-boot-autoconfigure).
Cómo crear un starter personalizado

    Crea un módulo Maven con dos submódulos: auto-configuracion y starter.

    En auto-configuration: clase @AutoConfiguration con @ConditionalOn... y @Bean. Debe registrar la configuración en META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports.

    En starter: POM vacío (solo dependencias) que trae el módulo de autoconfiguración y las librerías necesarias.

    Opcional: spring-boot-configuration-processor para generar metadatos de propiedades y ayudar al IDE con el autocompletado.

Orden de las autoconfiguraciones

Las configuraciones pueden anotarse con @AutoConfigureOrder, @AutoConfigureBefore o @AutoConfigureAfter para controlar la secuencia. Esto es vital porque, por ejemplo, la configuración de Hibernate debe aplicarse después de la del DataSource.
