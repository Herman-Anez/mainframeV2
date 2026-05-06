#  Configuración: Java vs. XML (evolución, comparación y mejores prácticas)
El viaje desde XML puro hasta Java config

Etapa 1 (2004-2008) : XML era la única opción. Archivos <beans> con <bean id=".." class="..">. Ventaja: configuración explícita y centralizada, fácil de cambiar sin recompilar. Desventaja: verbosidad, sin chequeo de tipos en tiempo de compilación, complejo para grandes proyectos.

Etapa 2 (2008-2012) : surgen anotaciones como @Autowired, @Component y @Transactional. Empieza a convivir XML con escaneo de componentes. El XML queda para beans de infraestructura.

Etapa 3 (2013-presente) : @Configuration + @Bean permiten escribir configuración en Java puro, con comprobación de tipos y refactorización segura. Spring Boot prácticamente elimina el XML obligatorio, salvo integraciones heredadas. Hoy es el estándar.
Comparación detallada con ejemplos equivalentes

Definir un DataSource y un JdbcTemplate

XML:
xml

<bean id="dataSource" class="com.zaxxer.hikari.HikariDataSource"
      destroy-method="close">
    <property name="jdbcUrl" value="${db.url}"/>
    <property name="username" value="${db.user}"/>
    <property name="password" value="${db.pass}"/>
</bean>

<bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">
    <constructor-arg ref="dataSource"/>
</bean>

Configuración Java:
java

@Configuration
@PropertySource("classpath:datasource.properties")
public class DbConfig {
    @Value("${db.url}") private String url;
    @Value("${db.user}") private String user;
    @Value("${db.pass}") private String pass;

    @Bean(destroyMethod = "close")
    public DataSource dataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(url);
        config.setUsername(user);
        config.setPassword(pass);
        return new HikariDataSource(config);
    }

    @Bean
    public JdbcTemplate jdbcTemplate(DataSource ds) {
        return new JdbcTemplate(ds);
    }
}

Ventajas de Java Config:

    Refactorización y autocompletado del IDE.

    Validación de tipos en compilación.

    Capacidad de lógica condicional (if, profile, @Conditional).

    Mejor integración con el ecosistema moderno.

Condicionalidad y perfiles

En XML, los perfiles se aplican con beans profile="dev" dentro del archivo. En Java config, con @Profile a nivel de clase o método.
java

@Configuration
@Profile("prod")
public class ProductionConfig { ... }

Además, con @Conditional (y derivados como @ConditionalOnClass, @ConditionalOnMissingBean, etc. en Boot), se puede activar una configuración en función de la presencia de clases, beans o propiedades.
Mezclar XML y Java Config

Todavía hay proyectos que necesitan importar XML existente. Se hace con @ImportResource:
java

@Configuration
@ImportResource("classpath:old-config.xml")
public class HybridConfig { }

Y a la inversa, desde XML se puede incluir una clase de configuración con <bean class="com.example.AppConfig"/>.
Buenas prácticas actuales

    Usa siempre configuración basada en Java (@Configuration).

    Mantén las clases de configuración pequeñas y cohesivas (p.ej. SecurityConfig, PersistenceConfig, WebConfig).

    Externaliza valores con @ConfigurationProperties en lugar de dispersar @Value: agrupa propiedades por prefijo en un POJO.
