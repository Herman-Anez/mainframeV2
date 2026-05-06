# _Spring_Core/Profiles.md
¿Por qué perfiles?

Una misma aplicación necesita comportarse distinto en desarrollo, pruebas, producción... URLs de base de datos, nivel de logs, endpoints habilitados, beans completos (como servicios mock). La anotación @Profile y la configuración relacionada te permiten controlar la inclusión de beans y configuraciones en función del entorno activo, de forma declarativa.
Definición de un perfil en beans
java

@Configuration
@Profile("dev")
public class DevelopmentConfig {
    @Bean
    public DataSource dataSource() {
        return new EmbeddedDatabaseBuilder()
            .setType(EmbeddedDatabaseType.H2)
            .build();
    }
}

java

@Service
@Profile("prod")
public class PaymentGatewayProd implements PaymentGateway { ... }

El bean solo se registrará si el perfil dev (o prod) está activo. Si no, es como si no existiera.
Operadores en @Profile

Spring permite lógica más compleja:

    !perfil : negación. El bean se registra si el perfil no está activo.
    java

    @Profile("!prod")
    public class MockServicio { ... }

    perfil1 & perfil2 : ambos deben estar activos.

    perfil1 | perfil2 : al menos uno activo.

    Se pueden combinar con paréntesis: (dev | qa) & !cloud.

java

@Service
@Profile("dev & !mock")
public class ServicioRealSoloDevNoMock { ... }

Activación de perfiles

Se puede hacer desde varias fuentes, con el siguiente orden de precedencia:

    Línea de comandos: --spring.profiles.active=dev,mock

    Variable de entorno: SPRING_PROFILES_ACTIVE=prod

    Propiedad del sistema: -Dspring.profiles.active=prod

    Archivo application.properties: spring.profiles.active=prod

    Programáticamente al construir SpringApplication:

java

new SpringApplicationBuilder(MiApp.class)
    .profiles("dev", "mock")
    .run(args);

La propiedad spring.profiles.active acepta múltiples valores separados por coma. Además, existe spring.profiles.default que se usa si no se estableció ninguna activa.
Perfiles y archivos application-{profile}.properties

La externalización de configuración es el complemento natural de los perfiles. Cualquier archivo application-{profile}.properties (o .yml) se cargará automáticamente si ese perfil está activo, sobrescribiendo las propiedades del archivo base.

Estructura:
text

application.properties        → configuración común
application-dev.properties    → sobreescribe/agrega para dev
application-prod.properties

En producción activas prod y solo se lee el específico; las propiedades comunes se heredan. Si usas YAML, puedes definir múltiples documentos en un mismo archivo separados por --- y condición spring.config.activate.on-profile=prod.
@Profile en clases @Configuration

Si una clase @Configuration completa lleva @Profile, todos sus @Bean métodos solo se evaluarán si el perfil cuadra. Si algunos métodos llevan su propio @Profile, Spring los combina con AND.
java

@Configuration
@Profile("cloud")
public class InfraCloudConfig {
    @Bean
    public StorageService cloudStorage() { ... }

    @Bean
    @Profile("!local")
    public CacheManager remoteCache() { ... }
}

Pruebas con perfiles

En los tests, puedes activar perfiles con @ActiveProfiles:
java

@SpringBootTest
@ActiveProfiles("test")
class MiTest {
    // ...
}

Así se cargará application-test.properties y los beans anotados con @Profile("test"). Es común tener un perfil test que use bases de datos embebidas, simule servicios externos, etc.
Perfiles y beans condicionales con @Conditional

@Profile internamente es un @Conditional con una condición especial ProfileCondition. Puedes crear tus propias condiciones más complejas con @Conditional y una implementación de Condition. Por ejemplo, @ConditionalOnProperty, @ConditionalOnClass, @ConditionalOnMissingBean (propios de Spring Boot) son condiciones mucho más flexibles que @Profile para controlar la creación de beans.
Buenas prácticas con perfiles

    No abuses de perfiles: tener 30 perfiles con combinaciones extrañas se vuelve inmanejable. Prefiere propiedades externas y condiciones puntuales.

    Usa @Profile principalmente para beans completos que cambian entre entornos (gateways de pago, servicios de mensajería), no para pequeñas diferencias de configuración (eso va en properties).

    Define un perfil default para desarrollo local y perfiles explícitos para CI, QA, prod.

