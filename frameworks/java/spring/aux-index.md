
/1//////////////////////////////////////////////
00 - ¿Qué es Spring? La filosofía y el ecosistema

Spring no es simplemente un conjunto de utilidades. Es un marco de trabajo completo que redefine cómo se construye software empresarial en Java. Para entenderlo a fondo hay que responder a tres preguntas: ¿por qué surgió?, ¿qué problema resuelve realmente? y ¿cómo está diseñado?
El problema original: J2EE pesado

A principios de los 2000, desarrollar aplicaciones empresariales con J2EE (antecesor de Jakarta EE) implicaba un infierno de configuración XML, obligatoriedad de heredar de clases del servidor de aplicaciones (EjBs), interfaces remotas, despliegues larguísimos y código fuertemente acoplado. Spring nació en 2003 de la mano de Rod Johnson como una reacción contra esa complejidad, basándose en las ideas de su libro *Expert One-on-One J2EE Design and Development*.
Principios fundamentales de Spring

    Contenedor ligero: no necesitas un servidor de aplicaciones pesado; Spring puede ejecutarse en un simple Tomcat o incluso en un entorno standalone. Gestiona el ciclo de vida de los objetos (beans) sin imponer contratos como EJBObject o interfaces específicas.

    No invasivo: las clases de tu dominio o servicio no tienen que extender clases de Spring ni implementar interfaces del framework (salvo alguna interfaz opcional para conveniencia). Solo se usan anotaciones que son puras marcas o importaciones de javax.inject / Jakarta.

    Configuración por convención y anotaciones: en lugar de una montaña de XML, hoy se utiliza principalmente configuración por código Java y anotaciones, complementada con la autoconfiguración de Spring Boot.

    Modularidad: Spring se compone de una veintena de módulos que puedes usar o ignorar. El núcleo (spring-core, spring-beans, spring-context) es obligatorio; el resto se añade según necesidad.

Arquitectura general de Spring

Se organiza en capas:

    Core Container (spring-core, spring-beans, spring-context, spring-expression): el contenedor IoC, el lenguaje SpEL, manejo de beans, etc.

    AOP and Instrumentation (spring-aop, spring-aspects): programación orientada a aspectos.

    Data Access/Integration (spring-jdbc, spring-tx, spring-orm, spring-jms): abstracción sobre JDBC, JPA, transacciones y mensajería.

    Web (spring-web, spring-webmvc, spring-websocket, spring-webflux): soporte para MVC, WebSocket y reactivo.

    Test (spring-test): utilidades para pruebas unitarias y de integración.

Sobre estos bloques se construye el ecosistema Spring Boot (que empaqueta y autoconfigura todo), Spring Data, Spring Security, Spring Cloud, etc.
¿Qué no es Spring?

    No es un servidor de aplicaciones, aunque puede reemplazar gran parte de su funcionalidad.

    No es solo un framework de inyección de dependencias; DI es solo el pegamento.

    No obliga a usar solo su forma de hacer las cosas; puedes combinar XML y anotaciones, usar solo partes del ecosistema.

En resumen: Spring es una plataforma de productividad para Java empresarial que proporciona infraestructura, abstracciones y una filosofía de diseño limpia.
01 - IoC y DI: el corazón del desacoplamiento
La inversión de control (IoC) como principio

En un programa tradicional, tu código controla el flujo: instancia objetos, llama a métodos, decide cuándo finalizar. La inversión de control entrega ese control a un framework. No es un patrón exclusivo de Spring; los servlets, los event listeners o los callbacks ya lo implementan.

En Spring, IoC toma la forma de un contenedor que crea y ensambla tus objetos (beans). Tú escribes clases "inocentes" que declaran sus dependencias, y el contenedor se las suministra en tiempo de ejecución. Esto es el Hollywood Principle: "No nos llames; nosotros te llamaremos".
Inyección de dependencias (DI) – La implementación concreta

DI es la técnica principal con la que Spring logra IoC. Consiste en que una clase no instancia sus dependencias (no hace new Servicio()), sino que las recibe desde el exterior.

Formas de DI en Spring:
1. Inyección por constructor (recomendada)
java

@Service
public class PedidoService {
    private final PedidoRepository repository;
    private final NotificacionService notificacion;

    public PedidoService(PedidoRepository repository, 
                         NotificacionService notificacion) {
        this.repository = repository;
        this.notificacion = notificacion;
    }
}

    Ventajas: el objeto siempre está completamente inicializado, permite final (inmutabilidad), las dependencias son explícitas y obligatorias. Facilita el testing (no necesitas campo @Autowired ni MockBean).

    Inconvenientes: si hay muchas dependencias, el constructor puede tener demasiados parámetros (síntoma de que la clase necesita un refactor).

2. Inyección por setter
java

@Service
public class PedidoService {
    private PedidoRepository repository;
    
    @Autowired
    public void setRepository(PedidoRepository repository) {
        this.repository = repository;
    }
}

    Se usa cuando la dependencia es opcional o se necesita reconfigurar después de la construcción. Menos recomendada porque el objeto puede existir en un estado temporal sin la dependencia.

3. Inyección por campo (@Autowired en atributo)
java

@Autowired
private PedidoRepository repository;

    Es la más legible pero tiene graves desventajas: oculta las dependencias (no sabes qué necesita la clase sin mirar los campos), dificulta las pruebas unitarias sin Spring (necesitas usar reflexión o @InjectMocks), impide final y rompe la encapsulación.

Cómo resuelve Spring las dependencias

El proceso de autowiring sigue estos pasos cuando encuentra @Autowired:

    Por tipo: busca un bean que coincida con el tipo declarado (si es una interfaz, busca la implementación única).

    Si encuentra exactamente uno, lo inyecta.

    Si encuentra varios candidatos del mismo tipo, busca un calificador:

        @Primary: el bean marcado con @Primary tendrá preferencia.

        @Qualifier("nombre"): especifica el bean por su nombre lógico.

    Si no hay ninguna coincidencia, por defecto lanza una excepción en tiempo de arranque (NoSuchBeanDefinitionException), a menos que required = false en @Autowired(required = false) o que la inyección sea dentro de un Optional<T> o @Nullable.

java

@Autowired
@Qualifier("emailService")
private NotificacionService notificacion; // inyecta el bean con nombre "emailService"

También se puede usar @Resource (JSR-250) que inyecta por nombre por defecto, o @Inject (JSR-330) que es funcionalmente equivalente a @Autowired sin required.
Laziness y dependencias circulares

Spring intenta crear los beans en orden para satisfacer las dependencias. Si hay una dependencia circular irresoluble (A → B → A), el contexto no puede levantarse. Sin embargo, se puede romper con @Lazy en uno de los puntos de inyección, lo que hace que Spring inyecte un proxy en lugar del bean real, que se resolverá solo en el primer acceso.
java

@Component
public class A {
    private final B b;
    public A(@Lazy B b) { this.b = b; }
}

También existen mecanismos como ObjectFactory, Provider<T> y ObjectProvider para obtener el bean bajo demanda (dependencia de tipo "lookup"):
java

@Autowired
private ObjectProvider<ServicioCostoso> servicioProvider;
...
ServicioCostoso s = servicioProvider.getIfAvailable();

IoC no es solo DI

Spring también ofrece Eventos y Listeners como variante de IoC: un componente publica un evento y no sabe quién lo recibe; los consumidores reaccionan sin acoplamiento directo. Igualmente con la programación orientada a aspectos (AOP): el código transversal se ejecuta sin que la clase invocada lo sepa.
02 - Contenedor y Beans: el motor interno
BeanFactory vs ApplicationContext

    BeanFactory: es la interfaz raíz, proporciona las capacidades básicas: crear, obtener y mantener beans. Pereza (lazy load por defecto). Sin funcionalidades de internacionalización, eventos, etc. Rara vez se usa directamente.

    ApplicationContext: hereda de BeanFactory y añade:

        Carga automática de bean post-processors y beans de configuración (incluye BeanFactoryPostProcessor).

        Publicación de eventos (ApplicationEventPublisher).

        Acceso a mensajes y recursos (MessageSource, cargar archivos .properties i18n).

        Soporte para múltiples fuentes de configuración (web, xml, anotaciones).

        Registro automático de BeanPostProcessor.

En la práctica siempre usamos ApplicationContext. Spring Boot crea un AnnotationConfigApplicationContext o un AnnotationConfigServletWebServerApplicationContext.
BeanDefinition y el registro de beans

Cuando Spring arranca, no almacena directamente instancias de beans, sino sus definiciones en una estructura BeanDefinition. Una BeanDefinition contiene:

    Nombre del bean (id).

    Nombre de la clase (className).

    Ámbito (scope: singleton, prototype...).

    Dependencias (nombres de otros beans).

    Modo de inicialización (lazy o eager).

    Métodos de callback (init/destroy).

    Si es abstracto, primario, etc.

Estas definiciones se cargan a través de un BeanDefinitionReader (para XML sería XmlBeanDefinitionReader, para anotaciones AnnotatedBeanDefinitionReader) y se almacenan en un BeanDefinitionRegistry (normalmente el mismo ApplicationContext).

Ejemplo de configuración programática:
java

AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext();
ctx.register(AppConfig.class); // registra una clase @Configuration
ctx.refresh(); // aquí se procesan las definiciones y se instancian los beans

Component Scanning: cómo encuentra Spring tus beans

@ComponentScan indica los paquetes base donde buscar clases anotadas con estereotipos (@Component, @Service, @Repository, @Controller). Spring escanea el classpath y crea una BeanDefinition por cada clase encontrada que cumpla con los filtros.

Puedes afinar con:

    basePackages o basePackageClasses para evitar escanear todo.

    includeFilters y excludeFilters con expresiones como @ComponentScan.Filter(type=FilterType.REGEX, pattern=".*Test") o FilterType.ASSIGNABLE_TYPE.

Estereotipos: @Service, @Repository y @Controller son especializaciones de @Component que añaden semántica. En particular @Repository habilita la traducción de excepciones de persistencia a la jerarquía DataAccessException de Spring.
Inicialización perezosa vs ansiosa (Eager)

Por defecto, los beans singleton se crean en el arranque (eager), lo que ayuda a detectar fallos de configuración rápidamente. Se puede marcar un bean con @Lazy para que se cree solo cuando sea requerido.

A nivel global: en Spring Boot, spring.main.lazy-initialization=true hace que todos los beans sean perezosos.
Configuración Java: @Configuration y @Bean

Una clase @Configuration es una forma elegante de definir beans mediante métodos anotados con @Bean. El contenedor llamará a esos métodos y registrará el objeto devuelto. Importante:

    proxyBeanMethods = true (por defecto) : Spring crea un proxy de la clase de configuración mediante CGLIB para interceptar las llamadas a los métodos @Bean. Así, si dentro de un método @Bean se invoca a otro método @Bean, se devuelve la instancia única del contenedor en lugar de crear una nueva, respetando el ámbito singleton.

    proxyBeanMethods = false (modo ligero, "Lite mode") : no se genera proxy; las llamadas entre métodos @Bean invocan directamente el método Java, creando un nuevo objeto cada vez. Es más rápido y útil cuando no hay dependencia entre los beans definidos.

java

@Configuration(proxyBeanMethods = false)
public class AppConfig {
    @Bean
    public DataSource dataSource() {
        return ...; // único
    }
    @Bean 
    public JdbcTemplate jdbcTemplate() {
        return new JdbcTemplate(dataSource()); // si proxyBeanMethods=true, dataSource() devuelve el bean singleton
    }
}

Internacionalización, Eventos y Recursos

ApplicationContext extiende MessageSource. Si defines un bean messageSource, Spring lo utiliza para resolver mensajes multi-idioma con getMessage(String code, Object[] args, Locale). Ideal para mensajes de validación o UI.

Los eventos de aplicación (ApplicationEvent y @EventListener) permiten comunicación desacoplada entre componentes. El publicador no conoce a los suscriptores.

La interfaz ResourceLoader del contexto permite cargar archivos con prefijos: classpath:, file:, http:, etc.
03 - Configuración: Java vs. XML (evolución, comparación y mejores prácticas)
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

04 - Ciclo de vida del Bean: paso a paso con internals

Comprender el ciclo de vida es indispensable para personalizar el comportamiento del contenedor y para entender cómo funcionan las transacciones, aspectos y la seguridad.
Fases completas del ciclo de vida (arranque de un bean singleton)

Imagina que Spring está arrancando y decide instanciar un bean MiServicio. El proceso detallado es:

    Instanciación del objeto

        Se llama al constructor (o al método estático de fábrica) usando la información de BeanDefinition. El objeto es "crudo", sin dependencias.

    Inyección de propiedades (dependencias)

        Spring inyecta las dependencias vía setters o directamente en campos anotados con @Autowired, @Value, @Inject, etc. Esto lo hacen BeanPostProcessors específicos como AutowiredAnnotationBeanPostProcessor y CommonAnnotationBeanPostProcessor.

    Ejecución de interfaces Aware

        Si el bean implementa ciertas interfaces Aware, se invocan sus métodos en este orden típico:

            BeanNameAware.setBeanName(String name)

            BeanClassLoaderAware.setBeanClassLoader(ClassLoader)

            BeanFactoryAware.setBeanFactory(BeanFactory) (si es un BeanFactory)

            ApplicationContextAware.setApplicationContext(ApplicationContext) (solo en contexto ApplicationContext)

        De esta forma, el bean puede obtener referencias al entorno de Spring sin buscar el contexto por fuera.

    BeanPostProcessor – Antes de inicialización

        Para cada BeanPostProcessor registrado, se ejecuta postProcessBeforeInitialization(bean, beanName). Aquí se puede modificar el bean, envolverlo en un proxy temprano, o hacer cualquier lógica transversal (p.ej., en Spring AOP se marcan los beans candidatos a ser proxy, aunque el proxy real se crea después).

        Ejemplo común: InitDestroyAnnotationBeanPostProcessor busca métodos @PostConstruct pero su ejecución real ocurrirá en el siguiente paso, no aquí; esta fase es más de preparación.

    Inicialización del bean
    Se ejecutan los métodos de inicialización en el siguiente orden de prioridad:
    a. Método anotado con @PostConstruct (detectado por el CommonAnnotationBeanPostProcessor que se ejecutó antes).
    b. afterPropertiesSet() de la interfaz InitializingBean.
    c. Método init-method personalizado definido en @Bean(initMethod = "nombre") o en XML.

    Durante esta fase el bean puede configurarse a sí mismo, validar dependencias o iniciar recursos.

    BeanPostProcessor – Después de inicialización

        Se ejecuta postProcessAfterInitialization(bean, beanName). Esta es la etapa donde normalmente se generan los proxies (AOP, transacciones, seguridad). Si el bean necesita ser envuelto en un proxy, el AbstractAutoProxyCreator (un BeanPostProcessor) reemplaza la instancia original por un proxy CGLIB o JDK. Por eso si llamas a un método interno dentro del mismo bean, la anotación @Transactional no se aplica: porque la llamada no pasa por el proxy.

    El bean está listo para ser usado

        El bean se almacena en el contenedor singleton (en un ConcurrentHashMap). Cualquier otra dependencia que lo necesite recibirá el bean ya completamente vestido.

    Destrucción del bean (al cerrar el contexto)

        Métodos anotados con @PreDestroy.

        destroy() de DisposableBean interface.

        Método destroy-method personalizado de @Bean o XML.

        Los DestructionAwareBeanPostProcessor pueden ejecutar lógica previa.

Diagrama resumido (texto)
text

[Constructor o Fábrica] --> [Inyección de Deps] --> [Aware: BenaName, ApplicationContext, etc.]
--> [BeanPostProcessor::before] --> [@PostConstruct / afterPropertiesSet / init-method]
--> [BeanPostProcessor::after] (proxies creados aquí) --> [Bean listo]
--> [Al cerrar: @PreDestroy / destroy()]

Extensiones poderosas: BeanFactoryPostProcessor y BeanDefinitionRegistryPostProcessor

Antes de que ningún bean sea instanciado, el contenedor permite modificar las propias definiciones de los beans. Los BeanFactoryPostProcessor trabajan con el BeanFactory (en realidad ConfigurableListableBeanFactory). Los BeanDefinitionRegistryPostProcessor pueden incluso registrar nuevas definiciones de beans.

El caso más famoso es ConfigurationClassPostProcessor, que procesa todas las clases @Configuration, @ComponentScan y @Import para registrar las definiciones correspondientes.

Ejemplo: modificar una propiedad tras la lectura del Classpath
java

@Component
public class CustomBeanFactoryPostProcessor implements BeanFactoryPostProcessor {
    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) {
        BeanDefinition bd = beanFactory.getBeanDefinition("dataSource");
        bd.getPropertyValues().add("maxPoolSize", 20);
    }
}

Ejemplo práctico de un BeanPostProcessor personalizado

Supón que quieres medir el tiempo de ejecución de todos los métodos de los beans de un paquete.
java

@Component
public class TimingBeanPostProcessor implements BeanPostProcessor {
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        if (bean.getClass().getPackageName().startsWith("com.empresa.servicio")) {
            return Proxy.newProxyInstance(
                bean.getClass().getClassLoader(),
                bean.getClass().getInterfaces(),
                (proxy, method, args) -> {
                    long start = System.nanoTime();
                    Object result = method.invoke(bean, args);
                    long time = System.nanoTime() - start;
                    System.out.println(method.getName() + ": " + time + " ns");
                    return result;
                });
        }
        return bean; // si no, devuelve el bean sin tocar
    }
}

Este processor envuelve el bean en un proxy JDK justo después de la inicialización, añadiendo el comportamiento de medición.
¿Por qué es vital este entendimiento?

    Te permite implementar cross-cutting concerns sin necesidad de AOP declarativa para casos específicos.

    Explica por qué funciona @Transactional: un BeanPostProcessor crea el proxy que maneja la transacción alrededor del método real.

    Depuración de problemas de beans: si una dependencia se resuelve mal, sabrás en qué fase mirar.



//////////////////////////////////////////////////////////////

/2//////////////////////////////////////////////
01_Spring_Core/Scopes_y_Proxies.md
El concepto de Scope (ámbito) en Spring

El scope define el ciclo de vida y visibilidad de un bean. Responde a cuántas instancias del bean se crean, cuándo se crean y cuándo se destruyen. Spring no solo maneja los típicos singleton y prototype, sino que ofrece una gama de ámbitos específicos para aplicaciones web.
1. Singleton (por defecto)

Una única instancia por contenedor Spring IoC. Ésta se crea, por defecto, en la fase de arranque (eager loading) y se sirve para todas las inyecciones. Es el scope más eficiente en memoria y el estándar para servicios sin estado.
java

@Service // Por defecto singleton
public class UsuarioService { }

O de manera explícita:
java

@Bean
@Scope(ConfigurableBeanFactory.SCOPE_SINGLETON) // "singleton"
public UsuarioService usuarioService() { return new UsuarioService(); }

El bean singleton se almacena en un mapa concurrente dentro del contenedor. Cuidado con el estado mutable: si un singleton guarda datos de petición, se mezclarán entre distintos usuarios. Para estado propio de la petición, hay que utilizar scopes web o almacenar los datos en objetos no gestionados (pass-by-value).
2. Prototype

Una nueva instancia por cada solicitud del bean. Si inyectas un bean prototype en un bean singleton, esa inyección ocurre una única vez; no se crea una nueva instancia cada vez que se invoca un método del singleton. Esto es la principal fuente de confusión.
java

@Component
@Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE) // "prototype"
public class PrototipoService { }

Problema típico:
java

@Component
public class Gestor {
    @Autowired
    private PrototipoService protoService; // Se inyecta una única instancia en toda la vida del Gestor
}

Soluciones para obtener una instancia fresca cada vez:

    Inyectar ObjectProvider<PrototipoService> y llamar a getIfAvailable().

    Inyectar ApplicationContext y obtenerlo programáticamente (context.getBean(PrototipoService.class)), aunque eso acopla al contenedor.

    Usar @Lookup sobre un método abstracto que devuelva el tipo prototype: Spring generará una subclase (a través de CGLIB) que devolverá un nuevo bean cada vez.

java

@Component
public class Gestor {
    @Lookup
    public PrototipoService obtenerPrototipoService() { return null; } // Spring sobreescribe el método
}

    Configurar un proxy en el scope prototype para que cada invocación a sus métodos cree una nueva instancia (ver más abajo).

Los beans prototype dejan de ser gestionados después de la creación: Spring no destruye sus métodos @PreDestroy (salvo que se registre un DestructionAwareBeanPostProcessor personalizado). Tú eres responsable de liberar sus recursos.
3. Request (ámbito web)

Una instancia por petición HTTP. Se crea al iniciar la petición y se destruye al terminarla. Permite almacenar datos del ciclo de la solicitud, como el usuario autenticado, sin necesidad de pasar HttpServletRequest por todos los métodos.
java

@Component
@RequestScope // equivalente a @Scope(value = WebApplicationContext.SCOPE_REQUEST)
public class DatosRequest {
    private String usuario;
    // getters/setters
}

Detrás de escena: Spring no crea un bean “real” de ámbito request, sino un proxy que se inyecta en otros beans (p.ej. un controlador singleton). Cada vez que se invoca un método del proxy dentro de una petición HTTP, el proxy delega en la instancia correcta (que está almacenada en un mapa dentro del RequestAttributes). Este mecanismo es crucial porque no se puede inyectar un bean de vida corta directamente en un bean de vida larga (el singleton viviría eternamente).

Necesidad de @Scope con proxy:
Si inyectas DatosRequest en un controller singleton, Spring necesita envolverlo en un proxy. Por defecto, con @RequestScope, Spring Boot habilita automáticamente el proxy (lo crea mediante CGLIB o JDK). Si usas la anotación genérica @Scope("request") necesitas activar explícitamente el modo proxy:
java

@Bean
@Scope(value = WebApplicationContext.SCOPE_REQUEST, proxyMode = ScopedProxyMode.TARGET_CLASS)
public DatosRequest datosRequest() { return new DatosRequest(); }

proxyMode puede ser:

    ScopedProxyMode.TARGET_CLASS → proxy CGLIB (necesita clase no final).

    ScopedProxyMode.INTERFACES → proxy JDK si la clase implementa una interfaz adecuada.

    ScopedProxyMode.NO → no proxy (solo válido si el bean se inyecta en otro bean del mismo ámbito o si se obtiene bajo demanda).

4. Session (ámbito web)

Una instancia por sesión HTTP. Mantiene estado a lo largo de todas las peticiones de un mismo usuario. Muy útil para carritos de compra, preferencias de usuario, etc.
java

@Component
@SessionScope // @Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = TARGET_CLASS)
public class CarritoBean { ... }

La sesión vive mientras el HttpSession exista. Al destruirse la sesión, el bean también se destruye. De nuevo, el proxy hace posible la inyección en beans singleton.

Peligro: en aplicaciones REST sin estado, @SessionScope puede causar efectos no deseados si el cliente no envía cookies de sesión. En esos casos, se desactiva el soporte de sesiones o se usa un @RequestScope apoyado en tokens JWT para guardar estado puntual.
5. Application (ámbito web)

Una única instancia por ServletContext. Es como un singleton global a toda la aplicación web (en un clúster, cada nodo tiene su instancia). Poco usado, pero disponible para recursos compartidos por todas las sesiones y peticiones, como un catálogo en memoria que no cambia.
java

@Component
@ApplicationScope // @Scope(value = WebApplicationContext.SCOPE_APPLICATION, proxyMode = TARGET_CLASS)
public class ConfiguracionGlobalBean { ... }

6. WebSocket (ámbito web)

Una instancia por ciclo de vida de una conexión WebSocket. Muy específico para almacenar estado durante una conversación WebSocket. Necesita también proxy.
java

@Component
@Scope(scopeName = "websocket", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class ChatBean { ... }

Cómo funcionan los proxies de ámbito

Cuando inyectas un bean de scope corto (request, session, etc.) en uno largo (singleton), Spring no puede colocar la instancia real porque ésta aún no existe en el momento del arranque del contenedor. La solución es un proxy (generado por CGLIB/JDK) que implementa la misma interfaz o extiende la clase y se registra en el lugar del bean original. Cada vez que se ejecuta un método del proxy, éste:

    Determina el ámbito correspondiente (request, session...).

    Busca la instancia real en el contenedor del ámbito (p.ej., la sesión HTTP).

    Si no existe, la crea y la almacena.

    Delega la llamada al método en la instancia real.

    Al finalizar el ámbito, el bean real se destruye.

El proxy vive tanto como el bean donde fue inyectado (por ejemplo, toda la vida del singleton). Pero cada hilo que lo invoca recibe la instancia adecuada a su contexto. Esta magia es la que permite escribir aplicaciones web sin preocuparse explícitamente por los límites de los ámbitos.
Cuándo usar cada scope

    Singleton: para lógica de negocio sin estado, repositorios, servicios utilitarios, etc.

    Prototype: cuando cada uso necesita su propia copia (por ejemplo, objetos que acumulan estado mutable durante un proceso, o cuando la creación tiene lógica condicional).

    Request: información vinculada a una sola petición HTTP, como el ID de usuario extraído de un token JWT o metadatos de la llamada.

    Session: estado persistente del usuario (carrito, preferencias de visualización). Solo en aplicaciones con sesiones HTTP.

    Application: es tan amplio que casi ningún caso práctico lo necesita; mejor usar un singleton común.

01_Spring_Core/BeanPostProcessor_y_Aware_Interfaces.md
El secreto para extender el contenedor: BeanPostProcessor

Un BeanPostProcessor permite ejecutar lógica antes y después de la inicialización de cada bean. No solo es un mecanismo para observar, sino para modificar o envolver beans. Todos los comportamientos transversales (inyección de dependencias, proxies transaccionales, seguridad, programación de tareas) se implementan a través de ellos.

La interfaz tiene dos métodos:
java

public interface BeanPostProcessor {
    @Nullable
    default Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        return bean;
    }

    @Nullable
    default Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        return bean;
    }
}

    postProcessBeforeInitialization: se ejecuta después de la inyección de dependencias pero antes de los callbacks de inicialización (@PostConstruct, afterPropertiesSet, etc.).

    postProcessAfterInitialization: se ejecuta después de los callbacks de inicialización. Aquí es donde típicamente se crean los proxies (transacciones, seguridad, aspectos).

Ambos pueden devolver el mismo bean o uno diferente (un wrapper). Si devuelves null, el bean no se registrará.

Ejemplo básico: logging de beans
java

@Component
public class LoggingBeanPostProcessor implements BeanPostProcessor {
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) {
        if (bean.getClass().getPackageName().startsWith("com.miempresa")) {
            System.out.println("Bean a punto de inicializarse: " + beanName);
        }
        return bean;
    }
}

BeanFactoryPostProcessor vs BeanPostProcessor

No confundir estas dos interfaces:

    BeanFactoryPostProcessor: opera sobre las definiciones de los beans (antes de que se creen). Puede modificar propiedades de BeanDefinition, añadir nuevos beans, etc. El ejemplo más famoso es ConfigurationClassPostProcessor, que procesa las anotaciones @Configuration, @ComponentScan, etc.

    BeanPostProcessor: opera sobre instancias de beans ya creadas.

Ambos son extensiones muy potentes y se aplican a todos los beans, por lo que hay que filtrar cuidadosamente para no dañar infraestructura interna.
Ejemplos reales de BeanPostProcessor en Spring

    AutowiredAnnotationBeanPostProcessor: procesa @Autowired y @Value.

    CommonAnnotationBeanPostProcessor: maneja @PostConstruct, @PreDestroy, @Resource.

    AbstractAutoProxyCreator (como InfrastructureAdvisorAutoProxyCreator): crea los proxies AOP para @Transactional, @Cacheable, etc., en postProcessAfterInitialization.

    ServletContextAwareProcessor y similares: invocan las interfaces Aware.

Crear un BeanPostProcessor personalizado

Imagina que quieres medir el tiempo de ejecución de todos los métodos de los beans de un paquete sin usar AOP. Puedes crear un proxy en postProcessAfterInitialization:
java

@Component
public class PerformanceBeanPostProcessor implements BeanPostProcessor {

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        if (bean.getClass().getPackageName().startsWith("com.empresa.servicio")) {
            return Proxy.newProxyInstance(
                    bean.getClass().getClassLoader(),
                    bean.getClass().getInterfaces(),
                    (proxy, method, args) -> {
                        long start = System.nanoTime();
                        Object result = method.invoke(bean, args);
                        System.out.println(method.getName() + ": " + (System.nanoTime() - start) + " ns");
                        return result;
                    });
        }
        return bean;
    }
}

Interfaces Aware: darle al bean acceso al contenedor

Un bean puede querer conocer su nombre, el ApplicationContext o el BeanFactory. Spring lo consigue mediante interfaces “Aware”. Cuando el contenedor detecta que un bean implementa alguna de estas interfaces, inyecta la dependencia correspondiente en el momento adecuado.

Principales interfaces Aware:
Interfaz	Descripción	Método
BeanNameAware	Recibe su nombre dentro del contenedor	setBeanName(String name)
BeanFactoryAware	Accede al BeanFactory que lo contiene	setBeanFactory(BeanFactory factory)
ApplicationContextAware	El contexto completo	setApplicationContext(ApplicationContext ctx)
MessageSourceAware	Para resolución de mensajes i18n	setMessageSource(MessageSource ms)
ApplicationEventPublisherAware	Para publicar eventos	setApplicationEventPublisher(ApplicationEventPublisher pub)
EnvironmentAware	Acceso al Environment (propiedades, perfiles)	setEnvironment(Environment env)
ResourceLoaderAware	Para cargar recursos del classpath, etc.	setResourceLoader(ResourceLoader loader)
ServletContextAware (web)	El ServletContext de la aplicación web	setServletContext(ServletContext context)

Ejemplo: un bean que necesita publicar eventos sin inyectar el publicador (aunque siempre es preferible la inyección):
java

@Component
public class MiComponente implements ApplicationEventPublisherAware {
    private ApplicationEventPublisher publisher;

    @Override
    public void setApplicationEventPublisher(ApplicationEventPublisher publisher) {
        this.publisher = publisher;
    }
    // ...
}

¿Son buenas prácticas? En general, preferimos la inyección de dependencias explícita (@Autowired o constructor). Las interfaces Aware acoplan tu código al framework más de lo necesario, pero son útiles en casos de infraestructura o cuando se está desarrollando una librería que necesita interactuar con Spring sin recibir inyecciones tradicionales.
Orden de ejecución combinado

El contenedor sigue un orden preciso cuando crea un bean:

    Instanciación (constructor o factory method).

    Inyección de dependencias (campo/setter) – manejada por AutowiredAnnotationBeanPostProcessor.

    Llamada a Aware interfaces en orden: BeanNameAware → BeanClassLoaderAware → BeanFactoryAware → ApplicationContextAware → otros.

    BeanPostProcessor.postProcessBeforeInitialization(...) (puede modificar el bean).

    Inicialización: @PostConstruct → afterPropertiesSet() → init-method personalizado.

    BeanPostProcessor.postProcessAfterInitialization(...) (creación de proxies, aspectos).

    El bean ya está listo para su uso.

Conocer este orden te permite depurar problemas de inyección, proxies o valores null en métodos init.
01_Spring_Core/Profiles.md
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

01_Spring_Core/SpEL.md
El lenguaje de expresiones de Spring

SpEL (Spring Expression Language) permite evaluar expresiones en tiempo real sobre un contexto de objetos. Integrado profundamente en el framework, es el motor oculto tras @Value, las condiciones de seguridad @PreAuthorize, las claves de caché @Cacheable(key=...), los filtros de Spring Integration, etc.
Sintaxis básica

Todo va entre #{}. Puedes incluir literales, operadores, acceso a propiedades, invocación de métodos, colecciones, operadores seguros, etc.
java

@Value("#{ 2 + 3 }")
private int suma; // 5

@Value("#{ T(java.lang.Math).random() * 100.0 }")
private double numeroAleatorio;

@Value("#{ sistemaProperties['user.home'] }")
private String homeDir;

@Value("#{ miBeanDelContexto.propiedad }")
private String valorDeOtroBean;

Operadores y tipos

    Aritméticos: +, -, *, /, %.

    Comparación: ==, !=, <, >, <=, >=, lt, gt, eq, etc.

    Lógicos: and, or, not.

    Condicional ternario: expression ? valorSiTrue : valorSiFalse.

    Elvis: nombre ?: 'Anónimo' (si null, usa el valor por defecto).

    Safe navigation: objeto?.propiedad (si objeto es null, devuelve null sin lanzar NullPointerException).

    Expresiones regulares: 'texto' matches '\\w+'.

    Tipo T: T(paquete.Clase). Accede a métodos estáticos y constantes.

Acceso al contexto y beans

En una expresión puedes acceder a beans por su nombre con @nombreBean y al Environment mediante environment['clave'] o systemProperties, systemEnvironment como objetos predefinidos.
java

@Value("#{ @pedidoService.findById(#id) }") // Referencia a otro bean y su método
private Pedido obtenerPedido(Long id);

En @PreAuthorize de seguridad:
java

@PreAuthorize("hasRole('ADMIN') or #usuario.id == authentication.principal.id")
public void actualizarPerfil(Usuario usuario) { ... }

Uso en anotaciones de caché
java

@Cacheable(value = "productos", key = "#nombre.toUpperCase()")
public Producto buscar(String nombre) { ... }

Uso en Spring Integration y otras áreas

    Filtros de mensajes: @Filter(inputChannel="...", expression="#payload.importe > 1000").

    Transformadores: @Transformer(expression = "payload.nombre.toUpperCase()").

StandardEvaluationContext y evaluación programática

Puedes evaluar SpEL manualmente para tus propias necesidades:
java

ExpressionParser parser = new SpelExpressionParser();
Expression exp = parser.parseExpression("nombre.length() > 5");
StandardEvaluationContext context = new StandardEvaluationContext(objeto);
context.setVariable("descuento", 0.1);
Boolean result = exp.getValue(context, Boolean.class);

El contexto se puede nutrir con variables, funciones y root objects.
Buenas prácticas y precauciones

    Rendimiento: las expresiones SpEL se compilan en árboles de sintaxis abstracta la primera vez, pero evaluarlas repetidamente en tiempo real tiene costo. Se recomienda compilar una vez y reutilizar el objeto Expression.

    Legibilidad: no abuses de SpEL en @Value para lógica muy compleja. Si una expresión se vuelve difícil de leer, extrae la lógica a un método Java.

    Seguridad: por defecto, SpEL no evalúa código arbitrario, pero en versiones muy antiguas era un vector de ataque. Siempre mantén las dependencias actualizadas.

    Compatibilidad: en application.properties, no se puede usar SpEL para definir propiedades (solo @Value al inyectarlas).

//////////////////////////////////////////////////////////////

/3//////////////////////////////////////////////
03_Spring_MVC/DispatcherServlet_y_Flujo.md
El corazón de Spring MVC: DispatcherServlet

DispatcherServlet es el Front Controller del patrón MVC. Recibe todas las peticiones HTTP, las distribuye a los controladores adecuados y gestiona todo el ciclo de vida de la respuesta. Sus responsabilidades principales:

    Recibir la petición.

    Determinar qué controlador y método manejan la solicitud (handler mapping).

    Ejecutar el handler (controlador).

    Resolver la vista lógica o generar la respuesta REST.

    Manejar excepciones.

    Aplicar interceptores.

Spring Boot registra y configura automáticamente un DispatcherServlet cuando detecta el starter spring-boot-starter-web. En un entorno tradicional, se configura en el web.xml o mediante la interfaz WebApplicationInitializer.
Roles de los beans estratégicos en Spring MVC

El DispatcherServlet utiliza una serie de beans especializados para delegar las tareas. Estos se definen en el contexto de la aplicación web (el WebApplicationContext, hijo del contexto raíz).

    HandlerMapping: Mapea una petición entrante a un handler (típicamente un método de controlador). Varias implementaciones:

        RequestMappingHandlerMapping: maneja las anotaciones @RequestMapping, @GetMapping, etc. Es la principal y está habilitada por defecto en Spring Boot.

        BeanNameUrlHandlerMapping: mapea por nombre de bean si coincide con un patrón de URL (casi en desuso).

        SimpleUrlHandlerMapping: configuraciones explícitas de URLs a beans.

    El proceso de búsqueda es secuencial: se recorre la lista de HandlerMapping en orden hasta que uno devuelve un handler no nulo.

    HandlerAdapter: Ejecuta el handler encontrado. Como los handlers pueden ser de distintos tipos (métodos anotados, controladores que implementan Controller, etc.), el HandlerAdapter sabe cómo invocarlos.

        RequestMappingHandlerAdapter: invoca métodos anotados con @RequestMapping. Se encarga de la conversión de parámetros, manejo de @ResponseBody, binding, validación, etc.

        HttpRequestHandlerAdapter, SimpleControllerHandlerAdapter para otros tipos.

    HandlerExceptionResolver: Maneja excepciones no capturadas que se propagan desde los handlers. Se verá en detalle más adelante.

    ViewResolver: Traduce el nombre lógico de una vista (String devuelto por el controlador) a un objeto View (JSP, Thymeleaf, etc.). En REST no se usa, porque el método está anotado con @ResponseBody.

    LocaleResolver, ThemeResolver, FlashMapManager: Para internacionalización, temas y atributos flash (redirecciones).

Ciclo de vida detallado de una petición

Suponiendo una petición GET /usuarios/5 con header Accept: text/html.

    Filtros previos (Filter chain) : Antes de llegar al DispatcherServlet, la petición pasa por los filtros de la cadena estándar (Spring Security, filtros personalizados, etc.). El DispatcherServlet se registra como un servlet y se invoca su service().

    Búsqueda del handler: DispatcherServlet consulta cada HandlerMapping registrado. RequestMappingHandlerMapping encuentra que el método getUsuario(Long id) en UsuarioController mapea con GET /usuarios/{id}. Retorna un HandlerExecutionChain que contiene el handler (un HandlerMethod que encapsula el controlador y método) y una lista de interceptores aplicables.

    Ejecución de interceptores (preHandle) : Si la cadena tiene interceptores, se ejecuta preHandle de cada uno en orden. Si alguno devuelve false, se corta la petición y se puede enviar una respuesta temprana.

    Determinación del HandlerAdapter: Se busca un HandlerAdapter que soporte el handler. RequestMappingHandlerAdapter es el adecuado.

    Ejecución del HandlerAdapter:

        Resolución de argumentos: mediante HandlerMethodArgumentResolvers, convierte los parámetros de la petición en los argumentos del método. Por ejemplo, @PathVariable("id") Long id, @RequestParam, @RequestBody, etc. Hay decenas de resolvers predefinidos.

        Llamada al método del controlador: se invoca usuarioController.getUsuario(5L).

        Procesamiento del retorno: mediante HandlerMethodReturnValueHandler. Si el método devuelve un String ("usuario/detalle") y la clase NO tiene @ResponseBody, se interpreta como nombre de vista. Si tiene @ResponseBody, se convierte el objeto a JSON mediante HttpMessageConverter.

    Post-ejecución de interceptores (postHandle) : Después de que el handler se ejecutó pero antes de renderizar la vista, se llama a postHandle. Permite modificar el modelo.

    Resolución de vista (si es necesario) : Si el handler devuelve un nombre de vista lógico, el ViewResolver seleccionado (ej. ThymeleafViewResolver) lo resuelve a una plantilla concreta (/templates/usuario/detalle.html). Se crea el objeto View.

    Renderizado de la vista: La vista se fusiona con el modelo (el ModelAndView o los atributos añadidos) y se escribe la respuesta en el HttpServletResponse.

    Finalización (afterCompletion) : Se llama a afterCompletion de los interceptores, incluso si hubo excepción, similar a un finally. Perfecto para limpiar recursos.

Interceptores vs Filtros

    Filtros: son parte del contenedor Servlet, no conocen detalles de Spring MVC. Útiles para logging, compresión, CORS, seguridad pre-triaje.

    Interceptores (HandlerInterceptor): tienen acceso al handler, modelo y vista, y se ejecutan dentro del contexto del DispatcherServlet. Ideal para añadir atributos comunes al modelo, verificar permisos tras el binding, medir tiempos, etc.

Configuración en Spring Boot

Boot autoconfigura DispatcherServlet, RequestMappingHandlerMapping, RequestMappingHandlerAdapter, ViewResolvers (si hay Thymeleaf, el resolver correspondiente), HandlerExceptionResolver, etc. Se puede personalizar implementando WebMvcConfigurer (sin anular @EnableWebMvc):
java

@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new MiInterceptor()).addPathPatterns("/api/**");
    }
    @Override
    public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
        converters.add(new MappingJackson2HttpMessageConverter());
    }
}

03_Spring_MVC/Controladores_REST.md
De @Controller a @RestController

Un controlador REST es un controlador que devuelve datos (generalmente JSON o XML) en lugar de un nombre de vista. La anotación @RestController es un atajo que combina @Controller y @ResponseBody. Con @ResponseBody, el valor de retorno del método se serializa directamente al cuerpo de la respuesta HTTP mediante HttpMessageConverter.
java

@RestController
@RequestMapping("/api/productos")
public class ProductoController {

    @GetMapping
    public List<Producto> listar() { ... }

    @GetMapping("/{id}")
    public Producto obtener(@PathVariable Long id) { ... }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Producto crear(@RequestBody @Valid Producto producto) { ... }
}

Anotaciones de mapeo de peticiones

Spring ofrece antaciones compuestas para los métodos HTTP más comunes:
Anotación	Equivale a
@GetMapping	@RequestMapping(method = RequestMethod.GET)
@PostMapping	@RequestMapping(method = RequestMethod.POST)
@PutMapping	@RequestMapping(method = RequestMethod.PUT)
@DeleteMapping	@RequestMapping(method = RequestMethod.DELETE)
@PatchMapping	@RequestMapping(method = RequestMethod.PATCH)

Todas aceptan atributos como value (URL), params, headers, consumes, produces.
Vinculación de parámetros (Data Binding avanzado)

Spring MVC extrae los datos de la petición y los convierte automáticamente gracias a HandlerMethodArgumentResolver.

    @PathVariable: de la plantilla de la URL. @GetMapping("/{id}") con @PathVariable Long id.

    @RequestParam: de parámetros de consulta o datos de formulario (?nombre=valor).
    java

    @GetMapping("/buscar")
    public List<Producto> buscar(@RequestParam("q") String query, 
                                 @RequestParam(defaultValue = "10") int max) { ... }

    Si el parámetro es opcional, usar required = false o Optional<String>.

    @RequestBody: convierte el cuerpo de la petición (JSON, XML) a un objeto Java usando HttpMessageConverter (normalmente Jackson).

    @RequestHeader: extrae un header específico.

    @CookieValue: extrae el valor de una cookie.

    @ModelAttribute: para binding de parámetros múltiples a un objeto (menos común en REST puro, más en formularios).

    Objetos complejos: Si el método tiene un parámetro de tipo POJO sin anotaciones, Spring lo trata como un @ModelAttribute, haciendo binding de parámetros por nombre de propiedad.

Manejo de respuestas y códigos de estado

La respuesta se puede construir de varias formas:

    Retornar directamente el objeto (con @ResponseBody o en un @RestController). El código HTTP por defecto es 200 OK. Para otros códigos se usa @ResponseStatus a nivel de método o excepción.

    ResponseEntity<T>: da control total sobre headers, status y cuerpo.
    java

    @GetMapping("/{id}")
    public ResponseEntity<Producto> obtener(@PathVariable Long id) {
        Producto p = service.findById(id);
        return p != null ? ResponseEntity.ok(p) 
                         : ResponseEntity.notFound().build();
    }

    ResponseEntity tiene métodos estáticos: ok(), created(URI), noContent(), badRequest(), status(HttpStatus), etc.

    HttpServletResponse: en el propio parámetro del método, se puede escribir directamente (no recomendado para REST moderno).

    HttpEntity<T>: similar a ResponseEntity pero también puede usarse como parámetro de entrada con HttpEntity<Producto> (accede a headers y cuerpo de la petición).

Negociación de contenido (Content Negotiation)

Spring MVC decide automáticamente qué converter usar basándose en:

    El header Accept de la petición.

    La extensión de la URL (si está configurado).

    El parámetro format (si está configurado).

    El atributo produces de las anotaciones de mapeo.

Ejemplo: si produces = "application/xml", Spring usará un converter de XML (si está disponible, p.ej. jackson-dataformat-xml). Si no hay converter adecuado, lanza HttpMediaTypeNotAcceptableException.
Convertidores de mensajes (HttpMessageConverter)

Interfaz que transforma entre objetos Java y el cuerpo de peticiones/respuestas. Spring Boot registra automáticamente:

    MappingJackson2HttpMessageConverter (JSON) si Jackson está en el classpath.

    StringHttpMessageConverter (text/plain).

    FormHttpMessageConverter (formularios).

    Jaxb2RootElementHttpMessageConverter (XML) si JAXB está disponible, pero normalmente se prefiere el jackson XML converter.

Se pueden añadir o personalizar mediante configureMessageConverters() o extendMessageConverters() en WebMvcConfigurer.
Configuración de CORS en controladores

A nivel global con WebMvcConfigurer.addCorsMappings, o a nivel de controlador/método con @CrossOrigin.
java

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:4200", maxAge = 3600)
public class ApiController { ... }

HATEOAS y enlaces

Spring HATEOAS permite construir respuestas REST con hipervínculos. Aunque es avanzado, los controladores pueden devolver EntityModel<T> o CollectionModel<T> para añadir enlaces. Spring Boot con spring-boot-starter-hateoas proporciona autoconfiguración.
Programación reactiva en REST

Con spring-boot-starter-webflux y @RestController (o en WebFlux), los métodos pueden retornar Mono<T> o Flux<T>. Spring maneja la suscripción. Cambia el paradigma a no bloqueante.
03_Spring_MVC/Manejo_de_Excepciones.md
Gestión centralizada de excepciones en @ControllerAdvice

En lugar de esparcir try/catch en cada controlador, Spring permite definir clases globales con @ControllerAdvice (o @RestControllerAdvice, que es @ControllerAdvice + @ResponseBody). Los métodos anotados con @ExceptionHandler capturan excepciones específicas.
java

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(RecursoNoEncontradoException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorDTO manejarNoEncontrado(RecursoNoEncontradoException ex) {
        return new ErrorDTO(404, ex.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public List<ErrorValidacionDTO> manejarValidacion(MethodArgumentNotValidException ex) {
        return ex.getBindingResult().getFieldErrors().stream()
                .map(e -> new ErrorValidacionDTO(e.getField(), e.getDefaultMessage()))
                .collect(Collectors.toList());
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorDTO manejarGeneral(Exception ex) {
        // logging del stacktrace real
        logger.error("Error no esperado", ex);
        return new ErrorDTO(500, "Error interno del servidor");
    }
}

Jerarquía de manejo de excepciones

Spring busca el manejador más específico:

    @ExceptionHandler dentro del propio controlador (mayor prioridad).

    @ExceptionHandler en clases con @ControllerAdvice aplicables (pueden ser globales, por paquete, o por anotación).

    Implementaciones de HandlerExceptionResolver (resolvers globales).

    Si no se captura, se propaga al contenedor servlet, que responde con una página de error predeterminada (o se puede personalizar con ErrorController).

HandlerExceptionResolver y sus implementaciones

HandlerExceptionResolver es la interfaz de bajo nivel. La resolución ocurre en el DispatcherServlet antes de llegar a los filtros de error. Implementaciones por defecto:

    ExceptionHandlerExceptionResolver: invoca los métodos @ExceptionHandler de @ControllerAdvice y controladores. Es el más potente y se configura automáticamente al detectar anotaciones.

    ResponseStatusExceptionResolver: busca la anotación @ResponseStatus en la excepción y establece el código de estado.

    DefaultHandlerExceptionResolver: convierte excepciones estándar de Spring MVC (NoHandlerFoundException, HttpMediaTypeNotSupportedException, etc.) a códigos HTTP.

    SimpleMappingExceptionResolver: mapea nombres de excepción a vistas de error (configuración XML/Java), para MVC no REST.

Se pueden agregar resolvers personalizados o ajustar el orden con WebMvcConfigurer.configureHandlerExceptionResolvers.
Lanzar excepciones con ResponseStatusException

Para evitar crear clases de excepción personalizadas, Spring ofrece ResponseStatusException, que se puede lanzar directamente y será capturada por ResponseStatusExceptionResolver:
java

@GetMapping("/{id}")
public Producto obtener(@PathVariable Long id) {
    throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Producto no encontrado");
}

El cuerpo por defecto contendrá el mensaje y el status. Para un formato más rico, es mejor usar un @ControllerAdvice con DTO.
Errores en filtros y antes del DispatcherServlet

Las excepciones que ocurren en los filtros (fuera del alcance del DispatcherServlet) no son manejadas por los mecanismos anteriores. Para capturarlas y devolver una respuesta JSON consistente, se puede usar un ErrorController implementando ErrorController (Spring Boot provee BasicErrorController). Personalizarlo permite tener respuestas de error uniformes aunque la petición nunca llegue al controlador.
Response con detalles en errores de validación

Volviendo al ejemplo de MethodArgumentNotValidException: el BindingResult contiene todos los errores de campo (rechazos de @NotNull, @Size, etc.), que podemos serializar en una lista de errores estructurados. Es una práctica recomendada devolver una respuesta legible por el cliente frontend.
03_Spring_MVC/Validacion_y_BindingResult.md
Bean Validation (JSR-380) y su integración con Spring MVC

Spring MVC se integra con Hibernate Validator (implementación de referencia) automáticamente cuando está en el classpath. Las anotaciones de validación (@NotNull, @Size, @Email, @Pattern, etc.) se colocan en los campos del DTO o entidad que se recibe.
java

public class ProductoDTO {
    @NotBlank(message = "El nombre es obligatorio")
    private String nombre;
    
    @Positive(message = "El precio debe ser positivo")
    private BigDecimal precio;
    
    @Size(min = 3, max = 10, message = "El SKU debe tener entre 3 y 10 caracteres")
    private String sku;
}

Activación de la validación en los controladores

Para que Spring valide automáticamente un @RequestBody, se debe añadir @Valid (o @Validated de Spring) al parámetro.
java

@PostMapping
public ResponseEntity<Producto> crear(@Valid @RequestBody ProductoDTO dto) { ... }

Si la validación falla, Spring lanza MethodArgumentNotValidException antes de que se ejecute el método del controlador. Por eso es crucial tener un @ControllerAdvice que la maneje.
Uso de BindingResult para capturar errores manualmente

Cuando no se quiere lanzar una excepción, se puede declarar un parámetro BindingResult justo después del objeto validado. Spring no lanzará la excepción y tú decides cómo actuar.
java

@PostMapping
public ResponseEntity<?> crear(@Valid @RequestBody ProductoDTO dto, BindingResult result) {
    if (result.hasErrors()) {
        // Construir respuesta de error personalizada
        return ResponseEntity.badRequest().body(crearErrores(result));
    }
    // lógica normal
}

Esta técnica es útil cuando se necesita lógica condicional adicional antes de reportar errores.
Validación a nivel de servicio con @Validated

Spring también permite validar parámetros de métodos de servicios con @Validated a nivel de clase y anotaciones de Bean Validation en los parámetros. Esto dispara ConstraintViolationException. Para capturarla globalmente, un @ControllerAdvice puede manejar ConstraintViolationException y construir la respuesta apropiada.
java

@Service
@Validated
public class ProductoService {
    public void actualizarPrecio(@Positive double nuevoPrecio) { ... }
}

Validación de path variables y request params

Para validar parámetros simples (no cuerpos), se puede anotar el controlador con @Validated y usar anotaciones de validación directamente en los parámetros.
java

@RestController
@RequestMapping("/api")
@Validated
public class BusquedaController {

    @GetMapping("/buscar")
    public List<Producto> buscar(@RequestParam @Size(min = 2) String q) { ... }
}

Si falla, se lanza ConstraintViolationException (no MethodArgumentNotValidException), que debe capturarse de forma diferenciada en el @ControllerAdvice.
Mensajes de validación personalizados y i18n

El valor de message puede referenciar una clave del MessageSource para soportar múltiples idiomas:
java

@NotNull(message = "{producto.nombre.obligatorio}")

Se debe tener un bean messageSource configurado (Spring Boot lo hace automáticamente con messages.properties). En el @ControllerAdvice, al construir los errores, se pueden resolver los mensajes mediante el MessageSource inyectado.
Grupos de validación

Bean Validation permite definir interfaces de grupos para aplicar distintas reglas en diferentes casos de uso (creación vs actualización). Se especifica el grupo con @Validated(OnCreate.class) en el controlador. Es una funcionalidad avanzada pero a tener en cuenta.
03_Spring_MVC/Vistas_y_Templates.md
El concepto de ViewResolver y View

Cuando un método controlador retorna un String sin @ResponseBody, ese string es el nombre lógico de la vista. El DispatcherServlet consulta a los ViewResolvers registrados para convertir ese nombre en un objeto View real (JSP, HTML con Thymeleaf, Freemarker, etc.).
ViewResolvers más comunes

    InternalResourceViewResolver: para JSP. Prefijo y sufijo configurables (/WEB-INF/views/ y .jsp). Si la vista lógica es "usuarios/lista", busca /WEB-INF/views/usuarios/lista.jsp.

    ThymeleafViewResolver: si Thymeleaf está presente. Resuelve nombres de plantilla como "usuarios/lista" a templates/usuarios/lista.html. Soporta Spring Expression Language (SpEL) dentro del HTML.

    FreeMarkerViewResolver, MustacheViewResolver, etc.

En una aplicación Spring Boot, si usas spring-boot-starter-thymeleaf, no necesitas configurar nada; el ThymeleafViewResolver se registra automáticamente y espera las plantillas en src/main/resources/templates/.
Paso de datos del controlador a la vista

El controlador añade atributos al modelo. Esto se hace de varias formas:

    Model como parámetro: public String listar(Model model) { model.addAttribute("productos", lista); return "productos/lista"; }

    ModelAndView como retorno.

    @ModelAttribute a nivel de método en el controlador (se añade automáticamente a todos los métodos del controlador). Útil para datos de formularios o menús.

    model.addAttribute sin nombre (se deduce del tipo).

En la vista, con Thymeleaf accedes así: ${productos} o iteraciones th:each="p : ${productos}". Con JSP, mediante Expression Language ${productos}.
Thymeleaf como motor de plantillas estándar

Thymeleaf es el motor recomendado en Spring Boot por su sintaxis natural y su integración con Spring Security, i18n, etc. Características destacadas:

    Plantillas prototípicas: se pueden abrir en navegador sin servidor porque usan atributos en lugar de etiquetas JSP.

    Expression utilitarias: #strings, #dates, #numbers.

    Formularios: th:object, th:field, th:errors ligados al binding de Spring para mostrar errores de validación.

    Fragmentos y layouts: mediante th:fragment y th:replace se crean layouts reutilizables.

    Soporte de SpEL para seguridad: sec:authorize de Spring Security integrado.

Redirecciones y flash attributes

El patrón POST-redirect-GET es común para evitar el doble envío de formularios.

    El controlador retorna "redirect:/productos". Spring lo interpreta como una redirección y se invoca RedirectView.

    Para pasar datos a la siguiente petición, como mensajes de éxito, se usan flash attributes: RedirectAttributes.addFlashAttribute("mensaje", "Creado exitosamente"). Estos sobreviven a la redirección y se borran tras mostrarse.

java

@PostMapping
public String crear(@Valid Producto p, BindingResult result, RedirectAttributes ra) {
    if (result.hasErrors()) return "productos/formulario";
    service.save(p);
    ra.addFlashAttribute("success", "Producto creado");
    return "redirect:/productos";
}

REST y ¿vistas?

En servicios REST puros no se devuelven vistas. Sin embargo, puede haber endpoints híbridos que devuelvan HTML para documentación (Swagger UI) o que sirvan una SPA. Spring Boot maneja recursos estáticos desde static/, public/, META-INF/resources/. La configuración de vistas no interfiere.
Resolución de vistas y negociación de contenido en REST

Si un método devuelve un objeto y no tiene @ResponseBody, pero la petición tiene encabezados que indican que acepta JSON, el HttpMessageConverter puede tomar el control. En la práctica, si el controlador tiene @RestController todo es @ResponseBody. En un @Controller puro, para que el valor retornado se interprete como JSON debe estar anotado con @ResponseBody en el método.


//////////////////////////////////////////////////////////////

/4//////////////////////////////////////////////
04_Spring_Boot/Autoconfiguracion_y_Starters.md
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
04_Spring_Boot/Estructura_Proyecto_Spring_Boot.md
Estructura recomendada de directorios

Spring Boot no fuerza una estructura, pero hay una ampliamente aceptada que sigue el estándar Maven/Gradle:
text

mi-proyecto/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── empresa/
│   │   │           └── miapp/
│   │   │               ├── MiAppApplication.java   (clase principal)
│   │   │               ├── controlador/
│   │   │               ├── servicio/
│   │   │               ├── repositorio/
│   │   │               ├── modelo/
│   │   │               ├── dto/
│   │   │               ├── configuracion/
│   │   │               └── excepcion/
│   │   └── resources/
│   │       ├── static/                 (contenido estático: css, js, imágenes)
│   │       ├── templates/              (plantillas Thymeleaf, Freemarker)
│   │       ├── application.properties  (o application.yml)
│   │       └── data.sql / schema.sql   (opcional, para inicializar BD)
│   └── test/
│       ├── java/
│       │   └── com/empresa/miapp/
│       │       ├── integracion/
│       │       ├── unidad/
│       │       └── MiAppApplicationTests.java
│       └── resources/
│           └── application-test.properties
├── pom.xml (o build.gradle)
└── README.md

    static/: servido directamente por Spring Boot (recursos estáticos). Ruta raíz /.

    templates/: plantillas del motor de vistas (Thymeleaf, etc.). No accesibles directamente.

    application.properties o .yml: configuración por defecto. Se puede dividir por perfiles.

    data.sql y schema.sql: si existen, Spring Boot los ejecuta al iniciar la base de datos embebida, a menos que se desactive.

La clase principal y SpringApplication
java

@SpringBootApplication
public class MiAppApplication {
    public static void main(String[] args) {
        SpringApplication.run(MiAppApplication.class, args);
    }
}

SpringApplication.run() arranca el contexto de Spring, el servidor embebido (si es web) y todo lo demás. Se puede personalizar mediante SpringApplication builder:
java

new SpringApplicationBuilder(MiAppApplication.class)
    .bannerMode(Banner.Mode.OFF)
    .profiles("dev")
    .run(args);

Empaquetado y ejecución

Spring Boot ofrece el plugin spring-boot-maven-plugin que genera un fat jar (JAR autocontenido con todas las dependencias, el servidor embebido y un cargador de clases especial). Se ejecuta con:
bash

mvn clean package
java -jar target/mi-app.jar

El plugin también permite ejecutar directamente con mvn spring-boot:run para desarrollo ágil.
Convenciones en el package scanning

El @ComponentScan implícito en @SpringBootApplication escanea el paquete donde reside la clase principal y todos sus subpaquetes. Por eso se recomienda ubicar la aplicación en el paquete raíz (com.empresa.miapp). Si necesitas escanear otros paquetes, puedes usar scanBasePackages en la anotación.
Recursos estáticos y caché

Por defecto, Spring Boot sirve recursos estáticos desde classpath:/static/, classpath:/public/, classpath:/resources/, classpath:/META-INF/resources/. Puedes personalizar con spring.web.resources.static-locations. El mapeo de URL raíz es /. Para control de caché: spring.web.resources.cache.cachecontrol.max-age.
El servidor embebido

Spring Boot incluye Tomcat por defecto en spring-boot-starter-web. Pero puedes cambiarlo a Jetty o Undertow excluyendo Tomcat y añadiendo el starter correspondiente. La configuración del servidor se realiza mediante propiedades server.* (puerto, SSL, compression, etc.). El servidor se inicia desde ServletWebServerApplicationContext.
04_Spring_Boot/Actuator_y_Metricas.md
¿Qué es Actuator?

Spring Boot Actuator expone una serie de endpoints HTTP y JMX que permiten monitorizar y gestionar una aplicación en producción: estado de salud, métricas, variables de entorno, configuración, trazas, mapeos de peticiones, etc. Para habilitarlo se añade el starter spring-boot-starter-actuator.
Endpoints más relevantes
Endpoint	Descripción
health	Estado de la aplicación y sus dependencias (DB, disco, etc.).
info	Información arbitraria (versión, descripción).
metrics	Métricas como uso de memoria, peticiones HTTP, tiempo de respuesta.
env	Propiedades del Environment.
loggers	Configuración de niveles de logs en tiempo real.
heapdump	Vuelca la memoria del heap (requiere JVM HotSpot).
threaddump	Vuelca los hilos.
mappings	Todos los endpoints de Spring MVC.
beans	Lista todos los beans del contexto.
conditions	Evaluación de autoconfiguraciones (positivos y negativos).

Por defecto, solo health está expuesto vía HTTP; los demás se pueden habilitar configurando management.endpoints.web.exposure.include=* (o una lista específica) para desarrollo, pero en producción se debe ser restrictivo y combinar con seguridad.
Configuración de actuadores
properties

management.endpoints.web.exposure.include=health,info,metrics
management.endpoint.health.show-details=when-authorized
management.endpoint.health.probes.enabled=true   # Para Kubernetes probes
management.server.port=8081                       # Puerto separado para gestión

Los endpoints pueden ser accedidos mediante /actuator/health, etc. (prefijo configurable).
Health indicators

El endpoint health agrega el estado de múltiples HealthIndicator. Spring Boot proporciona indicadores automáticos para: DataSource, Redis, MongoDB, DiskSpace, RabbitMQ, etc. Cada uno reporta UP, DOWN, o UNKNOWN. Puedes crear indicadores personalizados:
java

@Component
public class ServicioExternoHealth implements HealthIndicator {
    @Override
    public Health health() {
        // lógica para comprobar un servicio externo
        boolean disponible = check();
        if (disponible) {
            return Health.up().withDetail("latencia", 120).build();
        }
        return Health.down().withDetail("error", "timeout").build();
    }
}

Métricas con Micrometer

Actuator usa Micrometer como fachada de métricas. Se pueden exportar a múltiples sistemas: Prometheus, Datadog, Graphite, New Relic, etc. Basta añadir el registro adecuado (micrometer-registry-prometheus) y las métricas se publican en el formato correspondiente.

Métricas automáticas incluyen:

    JVM (memoria, GC, threads).

    Sistema (CPU, load average).

    Peticiones HTTP (http.server.requests con tag uri, status).

    Tiempos de ejecución de métodos @Timed.

    Conexiones de base de datos.

Métricas personalizadas

Puedes inyectar MeterRegistry y registrar contadores, timers, gauges.
java

@RestController
public class PedidoController {
    private final Counter pedidosCreados;

    public PedidoController(MeterRegistry registry) {
        pedidosCreados = registry.counter("pedidos.creados.total");
    }

    @PostMapping("/pedidos")
    public Pedido crear() {
        Pedido p = /* ... */;
        pedidosCreados.increment();
        return p;
    }
}

También se puede utilizar @Timed en métodos (requiere @EnableAspectJAutoProxy y un TimedAspect bean) para medir tiempos y contar invocaciones.
Info endpoint

Se puede crear un InfoContributor para añadir información personalizada, o simplemente definir propiedades:
properties

info.app.name=MiApp
info.app.version=1.0.0

java

@Component
public class BuildInfoContributor implements InfoContributor {
    @Override
    public void contribute(Info.Builder builder) {
        builder.withDetail("buildTime", Instant.now());
    }
}

Seguridad en Actuator

Combinado con Spring Security, se pueden restringir los endpoints. Lo típico es que /actuator/health esté sin autenticación (para probes de k8s) y el resto requiera un rol ACTUATOR.
04_Spring_Boot/Testing.md
Enfoque de testing en Spring Boot

Spring Boot facilita tanto pruebas unitarias (aisladas, sin contexto) como pruebas de integración (con contexto de Spring y/o bases de datos reales). Su starter spring-boot-starter-test trae: JUnit Jupiter, Mockito, AssertJ, Hamcrest, Spring Test, y más.
Pruebas unitarias con Mockito

No se levanta el contexto Spring; se mockean dependencias.
java

@ExtendWith(MockitoExtension.class)
class ProductoServiceTest {
    @Mock
    ProductoRepository repo;
    @InjectMocks
    ProductoService service;

    @Test
    void buscarPorId_debeRetornarProducto() {
        Producto esperado = new Producto(1L, "Teclado");
        when(repo.findById(1L)).thenReturn(Optional.of(esperado));

        Producto resultado = service.buscarPorId(1L);
        assertThat(resultado.getNombre()).isEqualTo("Teclado");
    }
}

Pruebas de integración con @SpringBootTest

@SpringBootTest levanta el contexto completo (o parcial). Por defecto, busca la clase @SpringBootApplication hacia arriba en el paquete. Útil para pruebas end-to-end de capas completas. Se puede arrancar un servidor real en un puerto aleatorio con webEnvironment = DEFINED_PORT / RANDOM_PORT.
java

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class MiApiIntegrationTest {
    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void obtenerProductos() {
        ResponseEntity<String> response = restTemplate.getForEntity("/api/productos", String.class);
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
    }
}

Slices de contexto (testing ligero de capas)

Para no levantar todo el contexto y acelerar las pruebas, Boot ofrece anotaciones de "slice":
Anotación	Carga solo	Típico use case
@WebMvcTest	Capa web (controladores), sin servicios ni repos. Mock de dependencias con @MockBean.	Probar controladores REST.
@DataJpaTest	Entidades, repositorios, DataSource embebido. Transaccional y rollback por defecto.	Probar repositorios y queries.
@JsonTest	Solo Jackson (serialización).	Probar DTOs JSON.
@RestClientTest	RestTemplate y componentes de llamada REST.	Probar clientes REST.
@JdbcTest	Solo JDBC (sin JPA).	Probar consultas directas.

Ejemplo @WebMvcTest:
java

@WebMvcTest(ProductoController.class)
class ProductoControllerTest {
    @Autowired
    private MockMvc mvc;
    @MockBean
    private ProductoService service;

    @Test
    void listarDebeRetornarOk() throws Exception {
        when(service.listar()).thenReturn(List.of(new Producto()));
        mvc.perform(get("/api/productos"))
           .andExpect(status().isOk())
           .andExpect(content().contentType(MediaType.APPLICATION_JSON));
    }
}

Nota: @WebMvcTest desactiva la autoconfiguración completa de datos y seguridad, aunque puedes incluir filtros concretos.
Mocking y sobrescritura de beans en tests

    @MockBean: reemplaza un bean en el contexto por un mock de Mockito. Útil para simular dependencias externas.

    @SpyBean: envuelve el bean real con un spy, permitiendo verificar llamadas.

    @TestConfiguration + @Bean: define beans adicionales o sustituye beans para ese test específico (dentro de la clase de test o en una inner class).

    @SpringBootTest(classes = ...) o @Import para cargar solo configuraciones específicas.

Base de datos en pruebas

@DataJpaTest configura automáticamente una base de datos embebida en memoria (H2). Las transacciones se revierten al final de cada test. Puedes usar el parámetro @AutoConfigureTestDatabase(replace = Replace.NONE) para conectar a una base de datos real (p.ej. PostgreSQL en un contenedor).

Para pruebas de integración con una base de datos real, el enfoque moderno es Testcontainers: levanta una instancia Docker de PostgreSQL, MySQL, etc., y la inyecta mediante configuraciones dinámicas (@DynamicPropertySource) o usando el módulo Spring Boot de Testcontainers.
Pruebas con @SpringBootTest y control transaccional

Por defecto, @SpringBootTest no es transaccional (a diferencia de @DataJpaTest). Para pruebas que usan HTTP (TestRestTemplate), ejecutan en hilos separados, por lo que la transacción no se comparte. En esos casos hay que limpiar manualmente o usar @Transactional (solo si las peticiones no cruzan hilos).
Pruebas con configuración externa

Puedes usar @ActiveProfiles("test") y un archivo application-test.properties para definir propiedades específicas. También @TestPropertySource para añadir propiedades en línea.
04_Spring_Boot/Perfiles_y_Propiedades.md
Externalización de la configuración

Spring Boot permite casi todas las propiedades de la aplicación (URL de base de datos, puerto, claves API, etc.) fuera del código, en archivos de propiedades, variables de entorno, argumentos de línea de comandos, o servidores de configuración. Esto sigue las reglas de The Twelve-Factor App.
Fuentes de propiedades y orden de prioridad

Spring Boot lee las propiedades desde 17 fuentes diferentes (ordenadas de mayor a menor prioridad):

    Argumentos de línea de comandos (--server.port=9090)

    Propiedades de Java System (System.getProperties())

    Variables de entorno (export SERVER_PORT=9090)

    Archivos application.properties / .yml

        application-{profile}.properties dentro del classpath (o spring.config.additional-location).

    @PropertySource en clases @Configuration
    ... etc. La lista exacta está en la documentación.

La sobreescritura sigue ese orden: un argumento de línea de comandos vence a una variable de entorno, que vence a un archivo de perfil.
Archivos application.properties y application.yml

Spring Boot soporta ambos formatos. YAML es más legible para estructuras jerárquicas, pero ambos son equivalentes.

properties:
properties

server.port=8080
spring.datasource.url=jdbc:mysql://localhost/midb

yml:
yaml

server:
  port: 8080
spring:
  datasource:
    url: jdbc:mysql://localhost/midb

Perfiles (profiles)

Los perfiles permiten tener múltiples conjuntos de configuración para distintos entornos (dev, test, prod). Se activan con spring.profiles.active=dev (en variable de entorno, línea de comandos, o en el application.properties principal). Los archivos específicos de perfil se nombran application-{profile}.properties o .yml. Si un perfil está activo, sus propiedades se superponen a las del archivo base.

Ejemplo:
application.properties define puerto 8080.
application-prod.properties define puerto 80 y datasource de producción.
Al activar prod, el puerto se sobrescribe a 80.

Los documentos multi-perfil en YAML permiten agrupar configuraciones:
yaml

# application.yml
server:
  port: 8080
---
spring:
  config:
    activate:
      on-profile: dev
server:
  port: 9090
---
spring:
  config:
    activate:
      on-profile: prod
server:
  port: 80

@Value y @ConfigurationProperties

    @Value("${clave}"): inyecta un valor simple, con posibilidad de valor por defecto (${clave:defecto}). Útil para una o pocas propiedades. Pero no ofrece chequeo de tipos ni auto-completado en IDE.

    @ConfigurationProperties: mapea un prefijo de propiedades a un bean Java, con binding relajado (camelCase, kebab-case, snake_case). Más seguro y escalable.

java

@ConfigurationProperties(prefix = "app.pedidos")
@Component
public class PedidosProperties {
    private int maxItems = 10;    // valor por defecto
    private Duration timeout;
    private List<String> estadosValidos;
    // getters y setters
}

properties

app.pedidos.max-items=20
app.pedidos.timeout=5s
app.pedidos.estados-validos=CREADO,ENVIADO

Para activar el autocompletado en el IDE, añade la dependencia spring-boot-configuration-processor (optional). Además, se pueden anidar clases POJO para mapear estructuras complejas.
Relajación del binding

@ConfigurationProperties soporta nombres de propiedades en distintos formatos:

    app.pedidos.max-items

    app.pedidos.maxItems

    app.pedidos.max_items

    APP_PEDIDOS_MAXITEMS (variable de entorno)

Todos se mapean a la misma propiedad maxItems.
Placeholders y SpEL en propiedades

Se pueden referenciar otras propiedades o usar expresiones SpEL limitadas en los valores:
properties

app.url-base=http://localhost:${server.port}
app.descripcion=La aplicación ${info.app.name} escuchando en ${app.url-base}

Configuración externa en producción: variables de entorno y Config Server

En entornos como Kubernetes o plataformas de nube, las propiedades se inyectan mediante variables de entorno (p.ej. SPRING_DATASOURCE_URL). Spring Boot convierte automáticamente variables mayúsculas con guiones bajos al formato de propiedad.

Para aplicaciones distribuidas, Spring Cloud Config Server centraliza la configuración y permite actualizarla en caliente (con @RefreshScope). El listado de fuentes se amplía para incluir la configuración remota con prioridad adecuada.
Validación de propiedades

Se puede utilizar Bean Validation en el POJO de @ConfigurationProperties para validar en el arranque. Si se añade @Validated a la clase y @NotNull, @Min, etc. en los campos, si la validación falla la aplicación no arranca, lo cual es deseable para evitar errores tardíos.
java

@Validated
@ConfigurationProperties(prefix = "app.pedidos")
public class PedidosProperties {
    @Min(1)
    private int maxItems;
    ...
}

//////////////////////////////////////////////////////////////

/5//////////////////////////////////////////////
05_Acceso_Datos/JDBC_Template.md
El dolor que resuelve: JDBC crudo

JDBC es potente pero requiere código repetitivo: abrir conexiones, preparar sentencias, recorrer ResultSet, cerrar recursos en finally anidados y manejar la omnipresente SQLException. Spring elimina esa fricción con JdbcTemplate, que sigue el patrón Template Method: el recurso se abre y cierra automáticamente, y tu código se centra en la lógica SQL y el mapeo.
Configuración del DataSource

Todo comienza con un DataSource. Spring Boot lo autoconfigura a partir de las propiedades spring.datasource.*. Si no hay propiedades, intenta una base de datos embebida (H2) si encuentra el driver. En configuración manual:
java

@Bean
public DataSource dataSource() {
    HikariConfig config = new HikariConfig();
    config.setJdbcUrl("jdbc:mysql://localhost/midb");
    config.setUsername("user");
    config.setPassword("pass");
    return new HikariDataSource(config);
}

@Bean
public JdbcTemplate jdbcTemplate(DataSource ds) {
    return new JdbcTemplate(ds);
}

Spring Boot incluye HikariCP como pool por defecto, el más rápido.
Operaciones básicas con JdbcTemplate

Una vez inyectado JdbcTemplate, los métodos principales son:

    queryForObject(String sql, Class<T> tipo, Object... args) : para un solo valor (ej. Integer count). Lanza EmptyResultDataAccessException si no hay resultados.

    queryForList(String sql, Class<T> tipo, Object... args) : lista de valores únicos.

    query(String sql, RowMapper<T> rowMapper, Object... args) : lista de objetos mapeados.

    queryForMap(String sql, Object... args) : un solo registro como Map<String,Object>.

    update(String sql, Object... args) : INSERT, UPDATE, DELETE. Devuelve el número de filas afectadas.

    batchUpdate(String sql, List<Object[]> batchArgs) : múltiples actualizaciones en lote.

    execute(String sql) : para DDL o ejecución genérica.

RowMapper: el puente entre ResultSet y objetos

Interfaz funcional clave:
java

public class ProductoRowMapper implements RowMapper<Producto> {
    @Override
    public Producto mapRow(ResultSet rs, int rowNum) throws SQLException {
        Producto p = new Producto();
        p.setId(rs.getLong("id"));
        p.setNombre(rs.getString("nombre"));
        p.setPrecio(rs.getBigDecimal("precio"));
        return p;
    }
}

Se puede usar lambda: (rs, rowNum) -> new Producto(...). Spring proporciona BeanPropertyRowMapper<Producto>(Producto.class) que mapea por nombres de columna (si coinciden), pero tiene limitaciones (no soporta conversiones complejas, ligeramente más lento).
Ejemplo de consulta con parámetros
java

public Optional<Producto> findById(Long id) {
    try {
        Producto p = jdbcTemplate.queryForObject(
            "SELECT id, nombre, precio FROM productos WHERE id = ?",
            new ProductoRowMapper(), id);
        return Optional.of(p);
    } catch (EmptyResultDataAccessException e) {
        return Optional.empty();
    }
}

NamedParameterJdbcTemplate

En lugar de ?, puedes usar parámetros con nombre (:id). Requiere un NamedParameterJdbcTemplate, que internamente delega en el JdbcTemplate estándar.
java

String sql = "SELECT * FROM productos WHERE nombre = :nombre AND precio < :precio";
Map<String, Object> params = Map.of("nombre", "Teclado", "precio", new BigDecimal(100));
List<Producto> productos = namedJdbcTemplate.query(sql, params, new ProductoRowMapper());

Muy práctico cuando hay muchos parámetros y mejora la legibilidad.
ResultSetExtractor y RowCallbackHandler

    ResultSetExtractor: para procesar el ResultSet completo dentro de una sola callback (ej. construir estructura jerárquica a partir de múltiples filas). Se usa con query(sql, ResultSetExtractor).

    RowCallbackHandler: para procesar fila a fila sin devolver nada (no acumula resultados). Ideal para volcados o streamings.

Gestión de excepciones

JDBC lanza SQLException y sus derivados. JdbcTemplate traduce automáticamente estas excepciones a la jerarquía de DataAccessException de Spring, que son unchecked y más informativas: DataIntegrityViolationException, DuplicateKeyException, BadSqlGrammarException, etc. Esta traducción se realiza mediante un SQLExceptionTranslator configurable.
Operaciones por lotes (batch)

Para insertar miles de registros eficientemente:
java

List<Object[]> batch = productos.stream()
    .map(p -> new Object[]{p.getNombre(), p.getPrecio()})
    .collect(toList());
jdbcTemplate.batchUpdate("INSERT INTO productos (nombre, precio) VALUES (?,?)", batch);

batchUpdate permite también indicar el tamaño de lote y manejar devoluciones de claves generadas mediante PreparedStatement con KeyHolder.
Recuperación de claves generadas
java

KeyHolder keyHolder = new GeneratedKeyHolder();
jdbcTemplate.update(connection -> {
    PreparedStatement ps = connection.prepareStatement(
        "INSERT INTO productos (nombre, precio) VALUES (?,?)", 
        Statement.RETURN_GENERATED_KEYS);
    ps.setString(1, p.getNombre());
    ps.setBigDecimal(2, p.getPrecio());
    return ps;
}, keyHolder);
Long nuevoId = keyHolder.getKey().longValue();

Llamada a stored procedures y funciones

Se puede usar JdbcTemplate.call(...) con CallableStatementCreator y CallableStatementCallback, pero hay alternativas más modernas como SimpleJdbcCall:
java

SimpleJdbcCall jdbcCall = new SimpleJdbcCall(jdbcTemplate)
    .withProcedureName("actualizar_stock")
    .declareParameters(
        new SqlParameter("p_id", Types.INTEGER),
        new SqlParameter("p_cantidad", Types.INTEGER));
Map<String, Object> inParams = Map.of("p_id", id, "p_cantidad", cantidad);
jdbcCall.execute(inParams);

Sin embargo, Spring Data JPA o JDBC simplifican aún más esto.
Cuándo usar JdbcTemplate frente a JPA

    Si necesitas control absoluto sobre el SQL y rendimiento máximo.

    En aplicaciones pequeñas o consultas muy específicas donde un ORM es excesivo.

    Cuando el modelo de datos no encaja bien con entidades JPA.

    Para migraciones o tareas batch.

Spring ofrece también Spring Data JDBC, que combina el estilo de repositorios de Spring Data con JdbcTemplate pero sin JPA ni mapeo complejo.
05_Acceso_Datos/JPA_y_Hibernate_Integracion.md
JPA: estándar, Hibernate: implementación

JPA (Jakarta Persistence API) es la especificación estándar para ORM en Java. Hibernate es la implementación más popular. Spring Boot elige Hibernate automáticamente si está en el classpath (starter spring-boot-starter-data-jpa).
Configuración sin Spring Boot

En Spring puro, configurar JPA implica:
java

@Bean
public LocalContainerEntityManagerFactoryBean entityManagerFactory(DataSource ds) {
    LocalContainerEntityManagerFactoryBean emf = new LocalContainerEntityManagerFactoryBean();
    emf.setDataSource(ds);
    emf.setPackagesToScan("com.empresa.modelo");
    emf.setJpaVendorAdapter(new HibernateJpaVendorAdapter());
    emf.setJpaProperties(hibernateProperties());
    return emf;
}

@Bean
public PlatformTransactionManager transactionManager(EntityManagerFactory emf) {
    return new JpaTransactionManager(emf);
}

Spring Boot autoconfigura todo esto con un simple spring.jpa.* en las propiedades.
El EntityManager y su ciclo de vida

El EntityManager es el objeto central de JPA que gestiona las entidades. Spring, a través de la anotación @PersistenceContext, inyecta un EntityManager con ámbito de transacción. En realidad inyecta un proxy que comparte el EntityManager real (que es de ámbito de transacción y no es thread-safe).
java

@Repository
public class ProductoDao {
    @PersistenceContext
    private EntityManager em;

    public Producto findById(Long id) {
        return em.find(Producto.class, id);
    }
}

Entidades: anotaciones esenciales
java

@Entity
@Table(name = "productos")
public class Producto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 200)
    private String nombre;

    @Enumerated(EnumType.STRING)
    private Categoria categoria;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "fabricante_id")
    private Fabricante fabricante;
    // getters/setters
}

Estrategias de generación de ID: AUTO, IDENTITY, SEQUENCE, TABLE. Lo más común es IDENTITY (autoincrement) o SEQUENCE en bases de datos que lo soportan (PostgreSQL, Oracle).
Mapeo de relaciones

    @OneToOne, @OneToMany, @ManyToOne, @ManyToMany.

    Importante: FetchType.LAZY para evitar cargas innecesarias (el valor por defecto en @ManyToOne es EAGER, así que hay que cambiarlo).

    Cuidado con @OneToMany sin mappedBy: por defecto crea tabla intermedia. Generalmente se define mappedBy en el lado no propietario.

    LazyInitializationException: ocurre cuando se accede a una relación lazy fuera de la transacción. Para evitarlo: usar JOIN FETCH en consultas, mantener transacción abierta (con @Transactional sobre el método) o usar DTOs.

Hibernate como motor: propiedades clave
properties

spring.jpa.show-sql=true
spring.jpa.hibernate.ddl-auto=validate  # none, update, create, create-drop
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.properties.hibernate.default_schema=public

ddl-auto en producción debe ser validate o none. update puede generar cambios destructivos. Mejor usar Flyway o Liquibase.
Contexto de persistencia y caché de primer nivel

Dentro de una transacción, el EntityManager mantiene un contexto de persistencia (caché de primer nivel) que garantiza que una misma entidad por ID devuelva la misma instancia. Las modificaciones se detectan al hacer flush (antes del commit) mediante el mecanismo de dirty checking, comparando el estado actual con una instantánea del momento de carga. No es necesario llamar a update() explícito; si la entidad está managed y la transacción se completa, Hibernate sincroniza los cambios.
Operaciones con EntityManager

    persist(entity): guarda una nueva entidad.

    merge(entity): actualiza una entidad detached (o crea si no existe).

    remove(entity): elimina una entidad managed.

    find(Class, id): busca por clave primaria.

    createQuery(jpql): consultas JPQL.

    createNativeQuery(sql): consultas nativas.

    flush(): sincroniza con la base de datos sin hacer commit.

Spring Data JPA encapsula todo esto, pero conocer el EntityManager es vital para casos complejos o cuando se requieren consultas dinámicas.
Errores frecuentes

    N+1 queries: al recorrer una colección de entidades que tienen una relación lazy y no se ha hecho fetch, se ejecuta una consulta adicional por cada entidad. Solución: JOIN FETCH en JPQL o @EntityGraph.

    Entidades detachadas: si intentas persistir una entidad que ya tiene ID pero no está managed, puede lanzar PersistentObjectException.

    Transaccionalidad: olvidar @Transactional en el servicio que orquesta múltiples operaciones.

05_Acceso_Datos/Spring_Data_JPA.md
El paradigma: repositorios sin implementación

Spring Data JPA genera automáticamente la implementación de las interfaces de repositorio en tiempo de ejecución. Solo defines la interfaz y, mediante query derivation o consultas anotadas, obtienes el código necesario.
java

public interface ProductoRepository extends JpaRepository<Producto, Long> {
    List<Producto> findByNombreIgnoreCase(String nombre);
    Optional<Producto> findByNombreAndFabricante(String nombre, Fabricante f);
}

En tiempo de arranque, Spring crea un proxy que implementa ProductoRepository y todos los métodos de JpaRepository (CRUD básico, paginación, ordenación, batch).
Query Methods (consulta derivada del nombre)

El mecanismo clave: el nombre del método se analiza y se traduce a una consulta JPQL/Criteria.

Palabras clave más comunes:
Palabra	Ejemplo	JPQL equivalente
find...By, read...By, get...By	findByNombre	where x.nombre = ?1
...Containing / ...Contains	findByNombreContaining(String)	where x.nombre like %?1%
...StartingWith	findByNombreStartingWith	like ?1%
...Between	findByPrecioBetween	where x.precio between ?1 and ?2
...In	findByCategoriaIn	where x.categoria in ?1
...OrderBy	findByNombreOrderByPrecioDesc	order by x.precio desc
...And, ...Or	findByNombreAndPrecio	where x.nombre = ?1 and x.precio = ?2
...True / ...False	findByActivoTrue	where x.activo = true
...First / ...Top	findFirst5ByNombre	limita resultados

Se puede usar Pageable y Sort como parámetro adicional. Retornar Page, List, Stream, opcional con Optional.
java

Page<Producto> findByPrecioGreaterThan(BigDecimal precio, Pageable pageable);

@Query personalizada con JPQL

Cuando los nombres se vuelven muy largos o necesitas joins complejos:
java

@Query("SELECT p FROM Producto p JOIN FETCH p.fabricante WHERE p.nombre LIKE %:nombre%")
List<Producto> buscarPorNombreConFabricante(@Param("nombre") String nombre);

También se pueden hacer updates/delete:
java

@Modifying
@Transactional
@Query("UPDATE Producto p SET p.precio = p.precio * :factor WHERE p.categoria = :cat")
int actualizarPrecioPorCategoria(@Param("factor") BigDecimal factor, @Param("cat") Categoria cat);

@Modifying indica que no es SELECT y necesita @Transactional.
@EntityGraph para controlar carga EAGER/LAZY

Para evitar el problema N+1 sin escribir JPQL, se pueden definir @EntityGraph y referenciarlo en el método:
java

@Entity
@NamedEntityGraph(name = "Producto.fabricante", 
    attributeNodes = @NamedAttributeNode("fabricante"))
public class Producto { ... }

// En repositorio:
@EntityGraph("Producto.fabricante")
List<Producto> findAll();

También se puede definir de forma ad-hoc con @EntityGraph(attributePaths = {"fabricante"}).
Auditoría y campos automáticos

Spring Data JPA proporciona anotaciones para auditoría:

    @CreatedDate, @LastModifiedDate (en java.time.Instant o LocalDateTime).

    @CreatedBy, @LastModifiedBy (con Spring Security integrado).

    Se habilita con @EnableJpaAuditing en alguna configuración.

java

@EntityListeners(AuditingEntityListener.class)
@Entity
public class Producto {
    @CreatedDate
    private Instant fechaCreacion;
    @LastModifiedDate
    private Instant fechaModificacion;
}

Proyecciones y DTOs

En lugar de devolver la entidad completa, se pueden definir interfaces de proyección:
java

public interface ProductoResumen {
    String getNombre();
    BigDecimal getPrecio();
}

// En repositorio:
List<ProductoResumen> findByCategoria(Categoria cat);

Spring solo selecciona las columnas necesarias. También hay proyecciones de cierre abierto (expresiones SpEL) o basadas en DTOs con constructor.
Especificaciones (Specification) y Query by Example

Para consultas dinámicas, JpaSpecificationExecutor permite construir criterios con Specification:
java

public interface ProductoRepository extends JpaRepository<Producto, Long>, 
        JpaSpecificationExecutor<Producto> {}

java

Specification<Producto> spec = (root, query, cb) -> cb.and(
    cb.like(root.get("nombre"), "%" + nombre + "%"),
    cb.greaterThan(root.get("precio"), 10)
);
List<Producto> productos = repo.findAll(spec);

Query by Example permite consultar a partir de una instancia de la entidad con campos no nulos. Simple pero limitado a igualdades exactas.
Paginación, ordenación y streaming

    Page<T>: contiene el contenido, número de página, total páginas, etc.

    Slice<T>: solo sabe si hay siguiente (más eficiente sin count).

    Stream<T>: un stream de resultados que debe cerrarse dentro de una transacción (@Transactional). Bueno para procesar grandes volúmenes con Java 8 streams.

05_Acceso_Datos/Transacciones_y_Transactional.md
Modelo de transacciones de Spring

Spring abstrae las transacciones con PlatformTransactionManager. Independientemente de que uses JDBC, JPA o JMS, el manejo declarativo es el mismo. La anotación @Transactional envuelve el método en un proxy AOP que crea/únete a una transacción según la configuración.
@Transactional en profundidad
java

@Transactional(
    propagation = Propagation.REQUIRED,
    isolation = Isolation.READ_COMMITTED,
    timeout = 30,
    readOnly = false,
    rollbackFor = { RuntimeException.class },
    noRollbackFor = { MiExcepcionControlada.class }
)
public void procesarPedido() { ... }

Propagación: define cómo se comporta el método si ya existe una transacción.
Valor	Comportamiento
REQUIRED (defecto)	Usa la transacción existente o crea una nueva.
REQUIRES_NEW	Siempre crea una nueva transacción, suspendiendo la actual.
MANDATORY	Debe existir una transacción; si no, lanza excepción.
SUPPORTS	Ejecuta en transacción si existe, si no, no.
NOT_SUPPORTED	Siempre ejecuta sin transacción, suspendiendo la existente.
NEVER	No debe existir transacción; si hay, lanza excepción.
NESTED	Ejecuta en un savepoint anidado (solo con JDBC).

Isolation: nivel de aislamiento SQL (READ_UNCOMMITTED, READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE). Normalmente READ_COMMITTED es suficiente.

readOnly: optimiza el rendimiento indicando que solo hay lecturas (el EntityManager no necesita hacer dirty checking).

rollbackFor / noRollbackFor: por defecto, solo se hace rollback con RuntimeException y Error. Si una excepción checked debe causar rollback, se especifica.
El proxy transaccional: cómo funciona internamente

    Spring crea un proxy alrededor del bean.

    Cuando se invoca un método anotado con @Transactional desde fuera del bean, el proxy intercepta la llamada.

    Antes de ejecutar el método, consulta al TransactionManager para comenzar o unirse a una transacción.

    Ejecuta el método real.

    Si el método lanza una excepción que cumple con rollbackFor, el TransactionManager hace rollback.

    Si todo sale bien, hace commit.

    Si la excepción es de las que no causan rollback, hace commit después de la excepción (poco común).

El problema de la auto-invocación: si desde dentro del mismo bean se llama a this.metodoTransaccional(), no pasa por el proxy y la anotación se ignora. Soluciones: autowirearse uno mismo, usar AopContext.currentProxy(), o refactorizar a otro bean.
@Transactional en repositorios y servicios

La práctica recomendada es poner @Transactional a nivel de servicio o caso de uso. Los repositorios de Spring Data JPA ya heredan @Transactional(readOnly = true) en SimpleJpaRepository para métodos de consulta, y los métodos de modificación (save, delete) tienen @Transactional por defecto, pero usualmente se requiere una transacción que cubra todo el flujo de negocio.
Transacciones y bases de datos distribuidas / JTA

Con un solo DataSource, se usa DataSourceTransactionManager o JpaTransactionManager. Para múltiples recursos (dos bases de datos, JMS, etc.) se necesita un gestor de transacciones distribuidas (JTA), como Atomikos o Bitronix, o delegar en el servidor de aplicaciones. Spring Boot simplifica la configuración con spring-boot-starter-jta-atomikos.
Manejo de transacciones largas y con patrones conversacionales

Spring soporta transacciones largas usando @Transactional y sesiones extendidas, pero la tendencia es usar arquitecturas que eviten mantener la transacción abierta a través de múltiples peticiones HTTP. En su lugar, se usa @Transactional en cada petición y se trabaja con entidades detachadas, volviendo a fusionarlas (merge) si es necesario.
Testing de transacciones

En pruebas con @DataJpaTest o @SpringBootTest, se puede usar @Transactional para que las operaciones de un test se reviertan automáticamente al final. Sin embargo, cuando se usa TestRestTemplate en @SpringBootTest(webEnvironment = RANDOM_PORT), la petición HTTP corre en un hilo separado, por lo que no comparte la transacción del test. En ese caso, se debe limpiar manualmente o usar @Transactional(propagation = NOT_SUPPORTED) y luego borrar datos.
05_Acceso_Datos/Consultas_Nativas_y_Procedure.md
Cuándo usar consultas nativas

Aunque JPQL cubre la mayoría de casos, a veces es necesario SQL nativo para:

    Utilizar características específicas del motor (funciones de ventana, operadores espaciales, FOR UPDATE, hints de optimizador).

    Invocar procedimientos almacenados complejos.

    Realizar operaciones masivas de actualización con condiciones especiales.

    Consultas con joins complejos donde JPQL no rinde o se vuelve ilegible.

Spring Data JPA y JPA proveen mecanismos para ejecutar SQL nativo manteniendo el mapeo de resultados.
@Query con nativeQuery = true
java

public interface ProductoRepository extends JpaRepository<Producto, Long> {
    @Query(value = "SELECT * FROM productos WHERE nombre ILIKE CONCAT('%', :nombre, '%')", 
           nativeQuery = true)
    List<Producto> buscarPorNombreSimilar(@Param("nombre") String nombre);
}

El resultado se mapea a la entidad Producto (o una proyección) si las columnas coinciden. También se puede retornar Object[] o List<Object[]> para casos sin mapeo.
Proyecciones con consulta nativa

Con una interfaz de proyección:
java

public interface ProductoCantidad {
    String getCategoria();
    Long getCantidad();
}

@Query(value = "SELECT categoria, COUNT(*) as cantidad FROM productos GROUP BY categoria", nativeQuery = true)
List<ProductoCantidad> contarPorCategoria();

Si el SQL devuelve columnas con nombres diferentes, se puede usar alias (SELECT cat as categoria).
Mapeo a DTO con @SqlResultSetMapping

Cuando se necesita un DTO (clase concreta) en lugar de interfaz, se puede usar @SqlResultSetMapping:
java

@SqlResultSetMapping(
    name = "productoResumenMapping",
    classes = @ConstructorResult(
        targetClass = ProductoResumenDTO.class,
        columns = {
            @ColumnResult(name = "nombre", type = String.class),
            @ColumnResult(name = "precio_medio", type = Double.class)
        }
    )
)
@Entity
public class Producto { ... }

// Luego en el repositorio:
@Query(value = "SELECT nombre, AVG(precio) as precio_medio FROM productos GROUP BY nombre", nativeQuery = true)
@SqlResultSetMapping(name = "productoResumenMapping")  // redundante si ya se mapea en la entidad
List<ProductoResumenDTO> resumenPrecios();

En la práctica, se prefiere @NamedNativeQuery declarado en la entidad y luego invocarlo con EntityManager.createNamedQuery.
Ejecución dinámica de SQL nativo con EntityManager

Cuando la consulta se construye en tiempo de ejecución (cuidado con SQL injection), se puede usar EntityManager.createNativeQuery directamente en el repositorio o un DAO.
java

@Repository
public class ProductoCustomRepository {
    @PersistenceContext
    private EntityManager em;

    @SuppressWarnings("unchecked")
    public List<Producto> buscarConFiltros(Map<String, Object> filtros) {
        StringBuilder sql = new StringBuilder("SELECT * FROM productos WHERE 1=1");
        Map<String, Object> params = new HashMap<>();
        if (filtros.containsKey("nombre")) {
            sql.append(" AND nombre LIKE :nombre");
            params.put("nombre", "%" + filtros.get("nombre") + "%");
        }
        Query query = em.createNativeQuery(sql.toString(), Producto.class);
        params.forEach(query::setParameter);
        return query.getResultList();
    }
}

Llamada a procedimientos almacenados con @Procedure

Spring Data JPA permite invocar procedimientos almacenados mediante la anotación @Procedure en métodos del repositorio.
java

@Procedure("nombre_procedimiento")
void ejecutarProcedimiento(@Param("param1") String param1);

Si el procedimiento retorna un conjunto de resultados, se puede declarar el tipo de retorno List<T>. También se puede usar @Query con nativeQuery = true y CALL para procedimientos que no se adaptan a los parámetros.

Alternativa vía EntityManager:
java

StoredProcedureQuery sp = em.createStoredProcedureQuery("calcular_ventas");
sp.registerStoredProcedureParameter("anio", Integer.class, ParameterMode.IN);
sp.setParameter("anio", 2025);
sp.execute();
List<Object[]> resultados = sp.getResultList();

Actualizaciones masivas con SQL nativo

@Modifying también funciona con nativeQuery = true:
java

@Modifying
@Transactional
@Query(value = "UPDATE productos SET precio = precio * 1.1 WHERE categoria = :cat", nativeQuery = true)
int aplicarInflacion(@Param("cat") String categoria);

Ojo: al ser nativo, no se aplican las reglas de cascada JPA ni se actualizan entidades en memoria, por lo que debe ir seguido de una recarga si la sesión se mantiene.
Consideraciones de seguridad y portabilidad

    Las consultas nativas atan la aplicación a un dialecto de base de datos concreto.

    Mayor riesgo de SQL injection si se concatenan parámetros. Siempre usar parámetros enlazados (setParameter).

    No pasan por la caché de segundo nivel de Hibernate.

    Las consultas nativas no son validadas en tiempo de arranque (salvo que se habilite spring.jpa.properties.hibernate.query.fail_on_pagination_over_collection_fetch), así que los errores sintácticos aparecen en tiempo de ejecución.



//////////////////////////////////////////////////////////////

/6//////////////////////////////////////////////
06_Seguridad/Spring_Security_Arquitectura.md
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
06_Seguridad/Configuracion_DSL.md
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

06_Seguridad/JWT_y_OAuth2.md
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
06_Seguridad/Metodo_Security.md
Habilitar la seguridad a nivel de método

La seguridad a nivel de método proporciona una capa de defensa adicional, controlando la invocación de métodos de servicio en lugar de solo URLs. Se habilita añadiendo @EnableMethodSecurity (o @EnableGlobalMethodSecurity en versiones anteriores) en una clase de configuración.
java

@Configuration
@EnableMethodSecurity(securedEnabled = true, prePostEnabled = true)
public class MethodSecurityConfig { }

    securedEnabled permite @Secured.

    prePostEnabled permite @PreAuthorize / @PostAuthorize.

    jsr250Enabled para @RolesAllowed.

@Secured y @RolesAllowed

@Secured("ROLE_ADMIN") verifica que el usuario tenga el rol indicado. No permite expresiones; solo una lista de roles (usando lógica OR). @RolesAllowed es equivalente pero sigue el estándar JSR-250.
java

public interface ProductoService {
    @Secured("ROLE_ADMIN")
    void eliminarProducto(Long id);
}

@PreAuthorize y @PostAuthorize: la potencia de las expresiones

Permiten usar el Spring Security Expression Language (SpEL) para lógica compleja.

    @PreAuthorize: antes de ejecutar el método. Evalúa la expresión y deniega el acceso si no se cumple.

    @PostAuthorize: después de ejecutar el método. El método se ejecuta, y luego se evalúa la expresión sobre el objeto retornado (útil para permisos en base al resultado). Si falla, el resultado no se devuelve.

Ejemplos:
java

@PreAuthorize("hasRole('ADMIN') or hasAuthority('PRODUCTO_ESCRITURA')")
public Producto crear(Producto p) { ... }

@PreAuthorize("#id != null and @productoService.esPropietario(#id, authentication.principal.username)")
public Producto actualizarPrecio(Long id, BigDecimal precio) { ... }

@PostAuthorize("returnObject.usuario == authentication.name")
public Pedido obtenerPedido(Long id) { ... }

@PreAuthorize("hasRole('USER') and #producto.precio < 1000")
public void aplicarDescuento(Producto producto) { ... }

En las expresiones se puede acceder a:

    Parámetros del método con #nombreParam.

    El objeto retornado en @PostAuthorize con returnObject.

    Beans de Spring con @nombreBean (p.ej. @seguridadService).

    El principal actual con authentication.

@PreFilter y @PostFilter

Filtran colecciones pasadas como argumentos o devueltas. Muy potentes pero con impacto en rendimiento si las colecciones son grandes.

    @PreFilter: filtra elementos de una colección de entrada usando una expresión. El elemento actual se referencia con filterObject.

    @PostFilter: filtra la colección de salida.

java

@PreFilter("filterObject.propietario == authentication.name")
public void guardarVarios(List<Documento> docs) { ... }

@PostFilter("hasPermission(filterObject, 'READ')")
public List<Documento> listarDocumentos() { ... }

Seguridad en servicios y controladores

A menudo se aplica en la capa de servicio, manteniendo los controladores ligeros. Así, si la lógica de negocio se reutiliza desde otros puntos (tareas programadas, mensajería), la seguridad se aplica igual. La anotación debe estar en la interfaz o en la implementación concreta; lo habitual es en la implementación.
Manejo de excepciones de seguridad a nivel de método

Cuando una expresión de seguridad falla, se lanza AuthorizationDeniedException. Se puede capturar globalmente con un @ControllerAdvice junto con @ExceptionHandler para convertirla en una respuesta HTTP adecuada (403 Forbidden).
Consideraciones de proxy

La seguridad a nivel de método se basa en AOP (proxies). Por tanto, aplican las mismas reglas: la anotación debe estar en un método público y la llamada debe provenir de fuera del bean (no por auto-invocación). Para casos de auto-invocación, se puede extraer a otro bean o usar @EnableAspectJAutoProxy(exposeProxy = true) y llamar a través de AopContext.currentProxy().


//////////////////////////////////////////////////////////////

/7//////////////////////////////////////////////
07_Temas_Avanzados/Eventos_de_Aplicacion.md
El sistema de eventos de Spring

Spring proporciona un mecanismo de publicación/suscripción de eventos dentro del ApplicationContext. Permite que un componente publique un evento y que otros componentes reaccionen sin acoplamiento directo, una implementación más del principio de Inversión de Control.

Piezas clave:

    ApplicationEvent: clase base para definir eventos. Desde Spring 4.2 ya no es obligatorio extenderla; cualquier objeto puede ser un evento.

    ApplicationEventPublisher: interfaz que posee el ApplicationContext (y cualquier bean que la implemente) para publicar eventos.

    Listener / @EventListener: método que recibe el evento y reacciona. Puede anotarse directamente en un bean.

Publicación de eventos

Inyectamos el publicador:
java

@Component
public class PedidoService {
    private final ApplicationEventPublisher publisher;
    // ...

    public void procesarPedido(Pedido pedido) {
        // lógica de negocio
        publisher.publishEvent(new PedidoCreadoEvent(this, pedido));
    }
}

PedidoCreadoEvent es una clase simple que hereda de ApplicationEvent o, más moderno, simplemente un POJO (sin extender nada) y se puede publicar así desde Spring 4.2+:
java

public class PedidoCreadoEvent {
    private final Pedido pedido;
    public PedidoCreadoEvent(Pedido pedido) { this.pedido = pedido; }
    public Pedido getPedido() { return pedido; }
}

Y la publicación sería publisher.publishEvent(new PedidoCreadoEvent(pedido)).
Recepción de eventos con @EventListener

Cualquier bean puede contener un método anotado con @EventListener. Spring lo registra automáticamente.
java

@Component
public class NotificacionListener {

    @EventListener
    public void manejarPedidoCreado(PedidoCreadoEvent event) {
        // enviar email de confirmación
        notificar(event.getPedido());
    }
}

Se pueden escuchar múltiples tipos de eventos con distintos métodos, o un mismo método puede escuchar varios usando la condición classes o genéricos.
Eventos transaccionales

Con @TransactionalEventListener, la escucha se vincula a las fases de una transacción:
Fase	Descripción
AFTER_COMMIT (defecto)	Se ejecuta si la transacción se completa exitosamente.
AFTER_ROLLBACK	Se ejecuta si la transacción falla.
AFTER_COMPLETION	Después de commit o rollback.
BEFORE_COMMIT	Antes de que la transacción se confirme.
java

@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void manejarPedidoCreadoCommit(PedidoCreadoEvent event) {
    // solo se ejecuta si la transacción fue exitosa
}

Importante: @TransactionalEventListener solo funciona si el evento se publicó dentro de una transacción activa y el listener está en el mismo ApplicationContext (o contexto con propagación de transacciones). Es una herramienta poderosa para evitar efectos secundarios si la transacción falla (ej. no enviar email si el pedido no se persistió).
Eventos asíncronos

Para no bloquear al publicador, se puede ejecutar el listener de forma asíncrona. Basta con añadir @Async al método listener y habilitar el soporte asíncrono con @EnableAsync.
java

@Component
@EnableAsync
public class AsyncNotificacionListener {

    @Async
    @EventListener
    public void manejarPedidoCreadoAsync(PedidoCreadoEvent event) {
        // este código se ejecuta en un pool de hilos separado
    }
}

Precauciones:

    La transacción del publicador no se propaga al hilo asíncrono.

    Los eventos asíncronos pueden perderse si la aplicación se cae antes de que se procesen; para garantías de entrega se necesita un message broker.

    No combinar @Async con @TransactionalEventListener en el mismo listener.

Programación reactiva con eventos

También se pueden publicar eventos y escucharlos usando @EventListener en entornos reactivos, pero el sistema de eventos estándar es bloqueante. Para aplicaciones WebFlux, se recomienda usar ApplicationEventMulticaster configurable o la integración con Project Reactor mediante Sinks.Many.
Orden y herencia

Se puede controlar el orden de ejecución de varios listeners con @Order. Además, un listener para una superclase también recibe eventos de las subclases, gracias a la resolución de tipos.
Eventos de contexto (built-in)

Spring dispara varios eventos del ciclo de vida del contexto: ContextRefreshedEvent, ContextStartedEvent, ContextStoppedEvent, ContextClosedEvent, RequestHandledEvent. Podemos escucharlos para inicializar recursos o gracia al apagar.
java

@Component
public class StartupListener {
    @EventListener(ContextRefreshedEvent.class)
    public void onRefresh() {
        // Cache warmup, etc.
    }
}

07_Temas_Avanzados/Cache.md
Abstracción de caché de Spring

Desde Spring 3.1, la capa de caché permite añadir comportamiento de almacenamiento temporal a métodos con anotaciones declarativas, sin acoplarse a una implementación concreta (EhCache, Caffeine, Redis, Hazelcast, etc.). Solo necesitas configurar un CacheManager y anotar los métodos.
@Cacheable – El pilar del caché

El resultado de un método se almacena en un caché (por nombre) usando la clave generada. En invocaciones posteriores con la misma clave, se devuelve el valor cacheado sin ejecutar el método.
java

@Service
public class ProductoService {
    @Cacheable("productos")
    public Producto findById(Long id) {
        // consulta costosa a BD
    }
}

    value / cacheNames: nombre(s) del caché donde almacenar.

    key: expresión SpEL para personalizar la clave. Por defecto se genera considerando todos los parámetros.

    keyGenerator: bean personalizado para generación de claves.

    condition: expresión SpEL que debe cumplirse para que se almacene en caché (p.ej. #id > 10).

    unless: expresión SpEL que si es verdadera excluye el almacenamiento (útil para no cachear resultados nulos: #result == null).

    sync: si es true, bloquea el acceso concurrente al mismo método para evitar que múltiples hilos computen el mismo valor a la vez (requiere que el CacheManager soporte sincronización, p.ej. Caffeine).

java

@Cacheable(value = "productos", key = "#id", unless = "#result == null")
public Producto findById(Long id) { ... }

@CacheEvict – Eliminación de entradas

Elimina una o todas las entradas de un caché. Se ejecuta después de la invocación del método (o antes con beforeInvocation = true).
java

@CacheEvict(value = "productos", key = "#id")
public void actualizarProducto(Long id, ProductoDTO dto) { ... }

@CacheEvict(value = "productos", allEntries = true)
public void limpiarCacheProductos() { ... }

@CachePut – Actualización sin omitir la ejecución

Similar a @Cacheable, pero siempre ejecuta el método y actualiza el caché con el resultado. Útil para refrescar entradas sin saltarse la lógica.
java

@CachePut(value = "productos", key = "#producto.id")
public Producto guardar(Producto producto) { return repo.save(producto); }

@Caching – Agrupar múltiples operaciones

Permite combinar varias anotaciones de caché en un solo método:
java

@Caching(
    cacheable = @Cacheable("productos"),
    evict = { @CacheEvict("catalogo", allEntries = true) }
)
public Producto crear(Producto p) { ... }

Configuración del CacheManager

Spring Boot autoconfigura un CacheManager según las dependencias:

    Caffeine (recomendada para caché local) con spring-boot-starter-cache.

    Redis con spring-boot-starter-data-redis.

    EhCache 3, Hazelcast, etc.

Con Caffeine, basta añadir la dependencia y configurar en application.properties:
properties

spring.cache.type=caffeine
spring.cache.caffeine.spec=maximumSize=500,expireAfterAccess=600s

Si necesitas múltiples caches con configuraciones distintas, defines un CacheManager bean:
java

@Bean
public CacheManager cacheManager() {
    CaffeineCacheManager cacheManager = new CaffeineCacheManager();
    cacheManager.setCaffeine(Caffeine.newBuilder()
        .expireAfterWrite(30, TimeUnit.MINUTES)
        .maximumSize(1000));
    return cacheManager;
}

Para caches con TTL diferentes, se puede crear un SimpleCacheManager con varios CaffeineCache.
Configuración avanzada: KeyGenerator y CacheResolver

    KeyGenerator: cuando la lógica de clave por defecto no es suficiente (parámetros complejos sin toString() específico). Se implementa la interfaz y se referencia con @Cacheable(keyGenerator = "miGenerador").

    CacheResolver: determina el(los) caché(s) en tiempo de ejecución, perfecto para sistemas multi-tenant. Puede elegir el caché según el inquilino.

Cacheo a nivel de anotaciones personalizadas

Puedes crear tu propia anotación estereotipada que agrupe las anotaciones de caché:
java

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Cacheable(value = "productos", key = "#id")
public @interface CachearProducto { }

Sincronización y concurrencia

Con sync = true en @Cacheable, Spring delega en el Cache subyacente el bloqueo. Por ejemplo, Caffeine soporta ConcurrentMap con sincronización a nivel de entrada. Esto evita el efecto "cache stampede" cuando muchos hilos intentan computar la misma clave simultáneamente.
Cache con Spring WebFlux (reactivo)

En WebFlux no se puede usar el CacheManager bloqueante estándar. Reactor añade CacheMono y CacheFlux para operaciones reactivas, pero no hay integración directa con @Cacheable. El uso de caché en contexto reactivo suele ser manual o con Mono.cache().
07_Temas_Avanzados/Programacion_Reactiva_WebFlux.md
Fundamentos reactivos con Project Reactor

Spring WebFlux es el módulo de Spring para construir aplicaciones web no bloqueantes usando el estándar Reactive Streams. Internamente se apoya en Project Reactor, que proporciona dos tipos principales:

    Mono<T>: emite 0 o 1 elemento (como un Optional asíncrono).

    Flux<T>: emite 0 a N elementos (como un Stream asíncrono).

Estos tipos son perezosos: nada ocurre hasta que alguien se suscribe. La suscripción la realiza el framework cuando el servidor recibe una petición.
WebFlux frente a Spring MVC
Spring MVC	Spring WebFlux
Modelo de hilos: un hilo por petición (bloqueante)	Modelo de hilos: pocos hilos en loop de eventos (no bloqueante)
Basado en Servlet API (Tomcat, Jetty)	Basado en Netty, Undertow o Servlet 3.1+ (con soporte no bloqueante)
Fácil de entender, ecosistema maduro	Mayor escalabilidad para cargas I/O intensivas
Anotaciones @Controller iguales	Puede usar anotaciones o functional endpoints
Controladores reactivos con anotaciones

La programación es casi idéntica a MVC, pero los métodos retornan Mono<T> o Flux<T>.
java

@RestController
@RequestMapping("/api/productos")
public class ProductoController {
    private final ProductoRepository repo;

    @GetMapping
    public Flux<Producto> listar() {
        return repo.findAll();
    }

    @GetMapping("/{id}")
    public Mono<ResponseEntity<Producto>> obtener(@PathVariable Long id) {
        return repo.findById(id)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<Producto> crear(@RequestBody Producto producto) {
        return repo.save(producto);
    }
}

La validación con @Valid funciona y el framework se suscribe al flujo para enviar la respuesta sin bloquear el hilo.
Repositorios reactivos

Spring Data proporciona R2DBC (Reactive Relational Database Connectivity) para bases de datos SQL y reactive MongoDB, Redis, etc.

R2DBC:
java

public interface ProductoRepository extends ReactiveCrudRepository<Producto, Long> {
    Flux<Producto> findByNombreContaining(String nombre);
}

La conexión se configura mediante spring.r2dbc.* y requiere un driver R2DBC (por ejemplo, PostgreSQL). Internamente, usa DatabaseClient que se basa en Netty para comunicación no bloqueante.
Functional Endpoints (RouterFunction & HandlerFunction)

Alternativa a las anotaciones: configuración basada en funciones.
java

@Configuration
public class ProductoRouter {
    @Bean
    public RouterFunction<ServerResponse> route(ProductoHandler handler) {
        return RouterFunctions
            .route(GET("/api/productos"), handler::listar)
            .andRoute(POST("/api/productos"), handler::crear);
    }
}

java

@Component
public class ProductoHandler {
    private final ProductoRepository repo;

    public Mono<ServerResponse> listar(ServerRequest req) {
        Flux<Producto> productos = repo.findAll();
        return ServerResponse.ok().body(productos, Producto.class);
    }

    public Mono<ServerResponse> crear(ServerRequest req) {
        return req.bodyToMono(Producto.class)
                .flatMap(repo::save)
                .flatMap(p -> ServerResponse.created(URI.create("/api/productos/" + p.getId())).build());
    }
}

Este estilo ofrece máxima transparencia y composición funcional.
WebClient: el cliente HTTP reactivo

Sustituto no bloqueante de RestTemplate. Es reactivo y devuelve Mono/Flux.
java

WebClient client = WebClient.create("https://api.externa.com");
Mono<Producto> producto = client.get()
    .uri("/productos/{id}", id)
    .retrieve()
    .onStatus(HttpStatus::is4xxClientError, response -> Mono.error(new RecursoNoEncontrado()))
    .bodyToMono(Producto.class);

Soporta programación funcional, filtros, intercambio de tokens, y balanceo de carga con Spring Cloud LoadBalancer.
Modelo de concurrencia y backpressure

WebFlux ejecuta en un pequeño pool de hilos (por defecto, número de núcleos de CPU) gracias al bucle de eventos de Netty. La escritura en bases de datos se hace con drivers reactivos que usan then, flatMap para encadenar operaciones sin bloquear. El concepto de backpressure (control de flujo) permite que el consumidor le indique al productor cuántos datos está listo para procesar, evitando sobrecargas de memoria.
¿Cuándo usar WebFlux?

    Altas concurrencias con muchas conexiones simultáneas (ej. API Gateway, streaming en tiempo real).

    Operaciones I/O intensivas (llamadas a servicios externos).

    No es más rápido por operación individual; brilla en throughput y escalabilidad bajo carga.

Errores comunes

    Bloquear dentro de una cadena reactiva (ej. llamar a Thread.sleep() o a una API bloqueante). Esto secuestra el hilo del loop y degrada el rendimiento. Usar subscribeOn(Schedulers.boundedElastic()) para adaptar código bloqueante.

    No suscribirse explícitamente; siempre devolver el Mono/Flux al framework.

07_Temas_Avanzados/Batch_y_Tareas_Programadas.md
Spring Batch: procesamiento de grandes volúmenes

Spring Batch es un framework para el desarrollo de procesos batch robustos, con reinicio, trazabilidad, control de transacciones escalonado y estadísticas. Una tarea batch se define como un Job compuesto de uno o más Step.

Conceptos básicos:

    Job: una unidad de trabajo completa, compuesto de pasos.

    Step: fase independiente (p.ej. leer, procesar, escribir).

    ItemReader: lee elementos uno a uno de una fuente (BD, archivo plano, XML).

    ItemProcessor: transforma un elemento leído.

    ItemWriter: escribe un lote de elementos (BD, archivo).

    Tasklet: alternativa al chunk para acciones simples (ej. mover archivos, enviar correos).

    JobRepository: almacena metadatos del estado del job y pasos (en BD). Permite reanudar tras fallos.

    JobLauncher: interfaz para lanzar jobs.

Configuración de un Job simple (lectura de CSV a BD)
java

@Configuration
@EnableBatchProcessing
public class BatchConfig {

    @Autowired JobBuilderFactory jobs;
    @Autowired StepBuilderFactory steps;

    @Bean
    public FlatFileItemReader<Producto> reader() {
        return new FlatFileItemReaderBuilder<Producto>()
            .name("productoItemReader")
            .resource(new ClassPathResource("productos.csv"))
            .delimited()
            .names(new String[]{"nombre", "precio"})
            .fieldSetMapper(fieldSet -> {
                Producto p = new Producto();
                p.setNombre(fieldSet.readString("nombre"));
                p.setPrecio(fieldSet.readBigDecimal("precio"));
                return p;
            })
            .linesToSkip(1)
            .build();
    }

    @Bean
    public JdbcBatchItemWriter<Producto> writer(DataSource dataSource) {
        return new JdbcBatchItemWriterBuilder<Producto>()
            .dataSource(dataSource)
            .sql("INSERT INTO productos (nombre, precio) VALUES (:nombre, :precio)")
            .beanMapped()
            .build();
    }

    @Bean
    public Step importStep(FlatFileItemReader<Producto> reader, JdbcBatchItemWriter<Producto> writer) {
        return steps.get("importStep")
            .<Producto, Producto>chunk(10)  // chunk size
            .reader(reader)
            .processor(processor())
            .writer(writer)
            .build();
    }

    @Bean
    public Job importJob(Step importStep, JobCompletionNotificationListener listener) {
        return jobs.get("importJob")
            .incrementer(new RunIdIncrementer())
            .listener(listener)
            .start(importStep)
            .build();
    }

    @Bean
    public ItemProcessor<Producto, Producto> processor() {
        return p -> { 
            p.setNombre(p.getNombre().toUpperCase());
            return p;
        };
    }
}

Chunk-oriented processing

El Step de tipo chunk lee elementos uno a uno con el ItemReader, los acumula en un buffer del tamaño del chunk, los pasa al ItemProcessor (opcional) y luego escribe el chunk completo con el ItemWriter. Si falla, puede reintentar el chunk o marcar el step como fallido.
Tasklets para pasos simples

Cuando no hay necesidad de procesar elementos, se usa un Tasklet:
java

@Bean
public Step cleanupStep() {
    return steps.get("cleanupStep")
        .tasklet((contribution, chunkContext) -> {
            // limpiar archivos temporales
            return RepeatStatus.FINISHED;
        })
        .build();
}

Job scheduling: lanzamiento bajo demanda

Spring Batch no incluye un planificador, pero se integra fácilmente con Spring @Scheduled o herramientas externas como Quartz. En una aplicación Boot, se puede lanzar con JobLauncher desde un controlador o una tarea programada.
java

@RestController
public class BatchController {
    @Autowired JobLauncher jobLauncher;
    @Autowired Job importJob;

    @PostMapping("/batch/import")
    public String lanzar() throws Exception {
        JobExecution exec = jobLauncher.run(importJob, new JobParametersBuilder()
            .addLong("time", System.currentTimeMillis())
            .toJobParameters());
        return "Batch lanzado: " + exec.getStatus();
    }
}

Spring Boot y Batch

El starter spring-boot-starter-batch autoconfigura JobLauncher, JobRepository (necesitarás una base de datos) y habilita @EnableBatchProcessing. Boot puede ejecutar jobs al arrancar si se configura spring.batch.job.enabled=true y se definen beans de Job.
Tareas programadas con @Scheduled

Spring proporciona un planificador ligero para ejecutar métodos periódicamente.

Habilitar con @EnableScheduling en alguna configuración.
java

@Configuration
@EnableScheduling
public class SchedulingConfig { }

Luego en cualquier bean:
java

@Component
public class ReporteProgramado {
    @Scheduled(fixedDelay = 60000) // 60 seg después de que termine la ejecución anterior
    public void generarReporte() { ... }

    @Scheduled(fixedRate = 60000)  // cada 60 seg, independientemente del tiempo de ejecución
    public void refrescarDatos() { ... }

    @Scheduled(cron = "0 0 2 * * ?") // a las 2 AM diario
    public void limpiarLogs() { ... }
}

Opciones:

    fixedDelay: intervalo en ms entre el final de una ejecución y el inicio de la siguiente.

    fixedRate: intervalo entre inicios de ejecución (puede solaparse si la tarea tarda más que el rate; evitar con @Async o manejo de concurrencia).

    initialDelay: retardo antes de la primera ejecución.

    cron: expresión cron (segundos, minutos, horas, día del mes, mes, día de la semana).

    zone: zona horaria para cron.

    timeUnit (a partir de Spring Boot 3.x): permite cambiar la unidad de tiempo.

Ejecución asíncrona de tareas programadas

Por defecto, las tareas @Scheduled se ejecutan en un único hilo (el TaskScheduler). Si una tarea se bloquea, las demás esperan. Para paralelismo, se puede configurar un TaskScheduler con pool:
java

@Bean
public TaskScheduler taskScheduler() {
    ThreadPoolTaskScheduler scheduler = new ThreadPoolTaskScheduler();
    scheduler.setPoolSize(5);
    return scheduler;
}

O marcar la tarea con @Async y habilitar @EnableAsync.
Consideraciones en tareas programadas

    En entornos clusterizados, las tareas programadas en cada nodo se ejecutarán simultáneamente a menos que se use un ejecutor distribuido (como ShedLock, Quartz con JDBC). Para evitar duplicados, se puede usar @SchedulerLock de ShedLock.

    Excepciones no capturadas detienen la ejecución futura de esa tarea con fixedDelay (si la instancia no está ya en ejecución). Es recomendable envolver la lógica en try/catch si se desea que continúe.

    Spring Boot expone el endpoint /actuator/scheduledtasks (Actuator) para ver las tareas programadas y sus expresiones cron.


//////////////////////////////////////////////////////////////

/8//////////////////////////////////////////////
## 08_Spring_Cloud/Service_Discovery_Eureka.md

### El problema del descubrimiento de servicios

En una arquitectura de microservicios, los servicios se despliegan en múltiples instancias, con direcciones IP y puertos dinámicos (contenedores, escalado automático). La configuración estática de endpoints se vuelve inviable. **Service Discovery** resuelve esto proporcionando un registro central donde los servicios se registran y consultan la ubicación de sus dependencias.

### Spring Cloud Netflix Eureka

Eureka es un componente del stack Netflix OSS integrado en Spring Cloud. Consta de:

- **Eureka Server**: el registro central.
- **Eureka Client**: cada microservicio que se registra y descubre otros.

### Implementación del Eureka Server

1. Añade `spring-cloud-starter-netflix-eureka-server`.
2. Anota la aplicación con `@EnableEurekaServer`.

```java
@SpringBootApplication
@EnableEurekaServer
public class EurekaServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServerApplication.class, args);
    }
}

    Configura application.yml:

yaml

server:
  port: 8761
eureka:
  client:
    register-with-eureka: false   # no se registra a sí mismo
    fetch-registry: false

¡El servidor ya está listo! Se accede a un dashboard en http://localhost:8761.
Eureka Client (microservicio)

Añade spring-cloud-starter-netflix-eureka-client a cada microservicio. Con spring.application.name se asigna el nombre lógico del servicio.
yaml

spring:
  application:
    name: producto-service
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka

Al iniciar, el cliente se registra. Opcional: eureka.instance.prefer-ip-address=true para registrar la IP en lugar del hostname (mejor en contenedores).
Descubrimiento en el código: RestTemplate + @LoadBalanced

Spring Cloud integra el descubrimiento con balanceo de carga del lado cliente usando Spring Cloud LoadBalancer (sucesor de Ribbon). Exponemos un RestTemplate con @LoadBalanced:
java

@Bean
@LoadBalanced
public RestTemplate restTemplate() {
    return new RestTemplate();
}

Ahora, en cualquier petición HTTP, usamos el nombre lógico del servicio:
java

restTemplate.getForObject("http://producto-service/api/productos", List.class);

La librería intercepta la petición, consulta a Eureka por las instancias de producto-service, elige una (round-robin por defecto) y traduce el nombre lógico a http://IP:puerto.
Alternativa moderna: WebClient reactivo con balanceo
java

@Bean
@LoadBalanced
public WebClient.Builder loadBalancedWebClientBuilder() {
    return WebClient.builder();
}
// Uso:
WebClient client = loadBalancedWebClientBuilder().build();
Mono<List<Producto>> productos = client.get()
    .uri("http://producto-service/api/productos")
    .retrieve()
    .bodyToFlux(Producto.class).collectList();

Salud y autorenovación

El Eureka client envía latidos (heartbeats) cada 30 segundos por defecto. Si el server no los recibe, la instancia se saca del registro. Se puede afinar con:
yaml

eureka:
  instance:
    lease-renewal-interval-in-seconds: 10
    lease-expiration-duration-in-seconds: 30

Zonas y alta disponibilidad

Para tolerancia a fallos del servidor Eureka, se despliegan múltiples servidores peer-to-peer que replican el registro. Cada servidor es cliente de los demás.
yaml

# server1
eureka:
  client:
    service-url:
      defaultZone: http://server2:8762/eureka,http://server3:8763/eureka

Los clientes pueden apuntar a todos los servidores en la lista, y Spring Cloud selecciona uno disponible.
Eureka vs. otras soluciones

    Eureka: AP (disponibilidad y tolerancia a particiones) en el teorema CAP, ideal para consistencia eventual y alta disponibilidad del registro.

    Consul: CP, con chequeos de salud más ricos y KV store.

    Kubernetes Service Discovery: en Kubernetes, se puede prescindir de Eureka y usar DiscoveryClient para Kubernetes.

Spring Cloud Commons abstrae el descubrimiento; cambiar de Eureka a Consul o Kubernetes solo requiere cambiar dependencias sin tocar el código de negocio.
08_Spring_Cloud/Config_Server.md
La necesidad de configuración externa centralizada

Los microservicios tienen propiedades (URLs de bases de datos, secretos, parámetros de negocio) que varían por entorno y deben gestionarse sin recompilar. Spring Cloud Config Server centraliza esta configuración en un backend versionado (Git, SVN, Vault) y la sirve a los servicios.
Config Server

Añade spring-cloud-config-server y anota con @EnableConfigServer.
java

@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}

Configuración application.yml:
yaml

server:
  port: 8888
spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/mi-organizacion/config-repo
          default-label: main
          clone-on-start: true

El servidor clona el repositorio Git y sirve las propiedades bajo /{application}/{profile} (ej. /producto-service/dev). El cliente consulta esta URL al arrancar y fusiona las propiedades.
Config Client

Los microservicios añaden spring-cloud-starter-config y un archivo bootstrap.properties (o application.properties) con la ubicación:
properties

spring.application.name=producto-service
spring.config.import=optional:configserver:http://localhost:8888

En el repositorio Git, un archivo producto-service-dev.yml contendrá las propiedades para ese perfil. El servidor las entrega, y el cliente las integra en su Environment antes de la inicialización de beans.
Refresco de configuración en caliente

Los cambios en Git no se propagan automáticamente a los clientes en ejecución. Spring Cloud ofrece:

    Actuator /refresh: el cliente debe invocar POST /actuator/refresh para recargar propiedades anotadas con @RefreshScope. Solo se actualizan beans marcados con @RefreshScope (normalmente servicios que leen propiedades).

java

@Service
@RefreshScope
public class ConfiguracionServicio {
    @Value("${mi.propiedad}")
    private String propiedad;
}

Al llamar a /refresh, el bean se reinicializa con los nuevos valores sin reiniciar la aplicación.

    Spring Cloud Bus: propaga eventos de refresco a todos los clientes mediante un broker de mensajería (RabbitMQ, Kafka). Con un solo POST /actuator/busrefresh en cualquier cliente, todos los demás reciben la notificación.

Cifrado y secretos

El Config Server puede cifrar valores en reposo usando claves simétricas o asimétricas. Los valores en los archivos de configuración pueden estar prefijados con {cipher}:
yaml

spring:
  datasource:
    password: '{cipher}AQBt...'

El servidor descifra antes de enviar a los clientes. La clave se configura con encrypt.key (simétrica). Para mayor seguridad, se puede integrar Vault como backend.
Estrategias de repositorio y composición

    Repositorio compuesto: múltiples fuentes de configuración (Git + Vault + base de datos).

    Patrones de búsqueda: soporta {application}, {profile}, {label}. Permite configuración global con archivos application*.yml.

    Sobrescritura local: las propiedades locales del cliente (application.yml) pueden anular las remotas según la prioridad.

Config Server en producción

    Se integra con Eureka para alta disponibilidad (los clientes usan el nombre lógico config-server en lugar de la URL fija).

    Autenticación HTTP básica con Spring Security.

    Aplicaciones nativas de Spring Cloud: spring-cloud-config-server + spring-cloud-starter-netflix-eureka-client.

08_Spring_Cloud/API_Gateway.md
El patrón API Gateway

En microservicios, un API Gateway es el punto de entrada único que encamina las peticiones a los servicios internos, aplica políticas de seguridad, límites, transformación de protocolo y agregación. Aísla al cliente de la complejidad interna.
Spring Cloud Gateway

Es el gateway oficial (reactivo, no bloqueante) construido sobre Spring WebFlux. Alternativa a Netflix Zuul (obsoleto). Se configura con spring-cloud-starter-gateway.
yaml

spring:
  cloud:
    gateway:
      routes:
        - id: producto-service
          uri: lb://producto-service
          predicates:
            - Path=/api/productos/**
          filters:
            - StripPrefix=1
        - id: pedido-service
          uri: lb://pedido-service
          predicates:
            - Path=/api/pedidos/**
          filters:
            - StripPrefix=1

El prefijo lb:// indica balanceo de carga a través del Service Discovery (Eureka). Los predicates determinan si la ruta aplica; los filters modifican la petición/respuesta.
Predicados (predicates)

Factores que determinan si una ruta coincide. Spring Cloud Gateway incluye muchos incorporados:

    Path: /api/productos/**

    Host: *.mitienda.com

    Method: GET,POST

    Header: X-Request-Id con expresión regular

    Query param: foo=bar

    Cookie: sessionId=regex

    Before/After/Between: horarios

    Weight: para distribución ponderada (canary releases)

Ejemplo de combinación:
yaml

predicates:
  - Path=/api/**
  - Method=GET
  - Header=X-Api-Version, v2

Filtros

Los filtros permiten modificar la petición entrante y la respuesta saliente. Existen filtros predefinidos y se pueden crear filtros personalizados.

Filtros comunes de Gateway:

    AddRequestHeader / AddResponseHeader: añade encabezados.

    AddRequestParameter: añade query params.

    PrefixPath / StripPrefix: manipula la ruta.

    RewritePath: reescribe la ruta con regex.

    CircuitBreaker: integra Resilience4j (circuit breaker).

    RequestRateLimiter: limitación de velocidad con Redis.

    Retry: lógica de reintentos.

    DedupeResponseHeader: elimina cabeceras duplicadas.

Ejemplo con circuit breaker:
yaml

filters:
  - CircuitBreaker=name=productoCB, fallbackUri=forward:/fallback/productos

Filtros personalizados

Implementando GatewayFilterFactory:
java

@Component
public class LoggingGatewayFilterFactory extends AbstractGatewayFilterFactory<LoggingGatewayFilterFactory.Config> {
    
    public LoggingGatewayFilterFactory() { super(Config.class); }

    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            System.out.println("Request: " + exchange.getRequest().getURI());
            return chain.filter(exchange).then(Mono.fromRunnable(() ->
                System.out.println("Response: " + exchange.getResponse().getStatusCode())));
        };
    }

    public static class Config { /* propiedades configurables */ }
}

Luego se usa en las rutas con - Logging.
Global Filters

Afectan a todas las rutas. Se implementan con GlobalFilter. Por ejemplo, autenticación JWT global, métricas, logging global.
Configuración programática

En lugar de YAML, se pueden definir rutas con la API de Java:
java

@Bean
public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
    return builder.routes()
        .route("producto-service", r -> r.path("/api/productos/**")
            .filters(f -> f.stripPrefix(1))
            .uri("lb://producto-service"))
        .build();
}

Integración con Spring Security

El Gateway puede integrar autenticación OAuth2, validando tokens JWT y propagando la identidad a los servicios posteriores. Con spring-boot-starter-oauth2-resource-server y configurando el gateway como resource server, se pueden proteger rutas de manera centralizada.
Limitación de velocidad (Rate Limiting)

Usa RequestRateLimiter con Redis. Se define un KeyResolver (por IP, por usuario, etc.):
java

@Bean
public KeyResolver userKeyResolver() {
    return exchange -> Mono.just(exchange.getRequest().getRemoteAddress().getAddress().getHostAddress());
}

Configuración:
yaml

filters:
  - name: RequestRateLimiter
    args:
      redis-rate-limiter.replenishRate: 10
      redis-rate-limiter.burstCapacity: 20

Resiliencia y tolerancia a fallos

El Gateway puede integrar Resilience4J (circuit breaker, retry, timeout) directamente en las rutas para fallos en los servicios backend, como veremos después.
Comparativa con otras soluciones

    Zuul 1.x: bloqueante, no recomendado para nuevas aplicaciones.

    Spring Cloud Gateway: reactivo, más ligero.

    Kong, Traefik, Nginx: soluciones externas; Spring Cloud Gateway es perfecto para ecosistema Spring Boot.

08_Spring_Cloud/Circuit_Breaker.md
El patrón Circuit Breaker

En sistemas distribuidos, las llamadas a servicios remotos pueden fallar o volverse lentas. El Circuit Breaker detecta fallos acumulativos y "abre" el circuito, rechazando rápidamente las peticiones durante un tiempo, evitando saturar al servicio deteriorado y dando posibilidad de recuperación.

Estados del circuito:

    CLOSED: operación normal, se contabilizan éxitos/fallos.

    OPEN: se superó el umbral de fallos, se rechazan todas las peticiones inmediatamente.

    HALF-OPEN: tras un tiempo de espera, se permite un número limitado de peticiones de prueba. Si tienen éxito, vuelve a CLOSED; si fallan, vuelve a OPEN.

Spring Cloud Circuit Breaker con Resilience4j

Spring Cloud proporciona una abstracción spring-cloud-circuitbreaker que admite múltiples implementaciones. La recomendada es Resilience4j, ligera y reactiva.

Dependencias: spring-cloud-starter-circuitbreaker-resilience4j.
Uso declarativo con anotaciones

En un servicio, se anota el método:
java

@Service
public class ProductoService {

    @CircuitBreaker(name = "productoCB", fallbackMethod = "fallbackListar")
    public List<Producto> listar() {
        // llamada a servicio externo (WebClient, RestTemplate)
        return restTemplate.getForObject("http://producto-service/api/productos", List.class);
    }

    public List<Producto> fallbackListar(Throwable t) {
        return List.of(new Producto("Producto por defecto"));
    }
}

Para habilitarlo, necesita una configuración application.yml:
yaml

resilience4j:
  circuitbreaker:
    instances:
      productoCB:
        sliding-window-size: 10
        failure-rate-threshold: 50
        wait-duration-in-open-state: 10s
        permitted-number-of-calls-in-half-open-state: 3

Parámetros principales:

    sliding-window-size: número de llamadas para evaluar la tasa de fallos.

    failure-rate-threshold: porcentaje de fallos que abre el circuito.

    wait-duration-in-open-state: tiempo de espera antes de pasar a half-open.

    permitted-number-of-calls-in-half-open-state: llamadas de prueba.

Fallback y retry combinados

Resilience4j también soporta @Retry, @TimeLimiter, @Bulkhead, @RateLimiter. Se pueden combinar con @CircuitBreaker:
java

@CircuitBreaker(name = "productoCB", fallbackMethod = "fallback")
@Retry(name = "productoRetry", fallbackMethod = "fallback")
public List<Producto> listar() { ... }

Configuración del retry:
yaml

resilience4j:
  retry:
    instances:
      productoRetry:
        max-attempts: 3
        wait-duration: 500ms

Circuit Breaker en el API Gateway

Spring Cloud Gateway permite aplicar circuit breaker directamente en las rutas:
yaml

filters:
  - name: CircuitBreaker
    args:
      name: productoCB
      fallbackUri: forward:/fallback/productos

El fallback puede ser un endpoint interno que devuelva una respuesta controlada.
Eventos y métricas

Resilience4j emite eventos (transiciones de estado, fallos, éxitos) a través de Micrometer. Con Spring Boot Actuator, las métricas se exponen en /actuator/metrics y se pueden exportar a Prometheus/Grafana.

Para acceder a los eventos programáticamente:
java

@Autowired
private CircuitBreakerRegistry registry;
...
CircuitBreaker cb = registry.circuitBreaker("productoCB");
cb.getEventPublisher().onSuccess(event -> log.info("Éxito"));

Bulkhead (compartimentos estancos)

Aísla partes del sistema para evitar que un fallo en una dependencia consuma todos los hilos del pool.
yaml

resilience4j:
  bulkhead:
    instances:
      productoBulkhead:
        max-concurrent-calls: 5
        max-wait-duration: 100ms

java

@Bulkhead(name = "productoBulkhead", fallbackMethod = "fallback")
public List<Producto> listar() { ... }

Si se alcanza el límite de llamadas concurrentes, las nuevas esperan hasta max-wait-duration y luego fallan.
TimeLimiter

Limita el tiempo de ejecución de una operación (útil en métodos asíncronos o no bloqueantes).
java

@TimeLimiter(name = "productoTimeLimiter")
public CompletableFuture<List<Producto>> listarAsync() { ... }

Configuración:
yaml

resilience4j:
  timelimiter:
    instances:
      productoTimeLimiter:
        timeout-duration: 2s

Consideraciones importantes

    Resilience4j está diseñado para usarse con funciones funcionales o CompletionStage/Mono/Flux. Para código bloqueante, asegúrate de configurar los hilos apropiadamente.

    Los fallbacks deben ser simples y no depender de la misma dependencia que falló.

    Monitorear los circuit breakers con Micrometer + Grafana te permite ajustar umbrales y detectar problemas de latencia.

    El patrón no sustituye a la lógica de reintentos; se combina. Circuit Breaker evita llamadas cuando se sabe que el sistema está caído; Retry maneja fallas transitorias.



//////////////////////////////////////////////////////////////

///////////////////////////////////////////////
09_Miscelaneos/Internacionalizacion_i18n.md
El desafío de las aplicaciones multidioma

Una aplicación global debe presentar mensajes, etiquetas, formatos de fecha/número y validaciones en el idioma y la región del usuario. Spring proporciona un soporte sólido para i18n (internacionalización) y l10n (localización) mediante la abstracción MessageSource y la resolución de Locale.
MessageSource: la fábrica de mensajes

MessageSource es una interfaz que permite obtener mensajes por código y Locale. Spring define tres implementaciones principales:

    ResourceBundleMessageSource: carga bundles .properties desde el classpath. Sin caché configurable (lee cada vez por defecto, aunque internamente usa ResourceBundle con caché de la JVM).

    ReloadableResourceBundleMessageSource: similar, pero soporta recarga en caliente sin reiniciar la aplicación. Ideal para desarrollo o cuando los bundles están externos.

    StaticMessageSource: para mensajes programáticos, útil en tests.

Spring Boot autoconfigura un MessageSource buscando archivos messages*.properties en la raíz del classpath. La configuración por defecto:
properties

spring.messages.basename=messages
spring.messages.encoding=UTF-8
spring.messages.cache-duration=3600   # segundos, para producción

Se pueden definir múltiples basenames: messages, errors.

Los archivos se nombran con el sufijo del locale: messages_es.properties, messages_en.properties, messages_fr.properties. Si no encuentra el código en el locale exacto, busca en el idioma base y luego en el archivo sin sufijo.
Resolución de mensajes en código Java

Inyectamos MessageSource y solicitamos un mensaje con un Locale:
java

@Autowired
private MessageSource messageSource;

public String saludo(Locale locale) {
    return messageSource.getMessage("saludo.bienvenida", null, locale);
}

Si el mensaje requiere parámetros:
properties

# messages_es.properties
pedido.confirmacion=Pedido {0} confirmado con total de {1,number,currency}

java

String mensaje = messageSource.getMessage(
    "pedido.confirmacion",
    new Object[]{pedido.getId(), pedido.getTotal()},
    locale);

Podemos manejar mensajes de error con argumentos y DefaultMessageSourceResolvable.
Resolución del Locale

Spring necesita determinar el Locale del usuario. El DispatcherServlet utiliza un LocaleResolver:

    AcceptHeaderLocaleResolver (defecto): analiza el header Accept-Language de la petición HTTP. Stateless, ideal para APIs.

    SessionLocaleResolver: almacena el locale en la sesión HTTP. Útil cuando el usuario puede cambiar de idioma manualmente.

    CookieLocaleResolver: persiste el locale en una cookie, sobrevive entre sesiones.

    FixedLocaleResolver: fuerza un locale fijo (por ejemplo, para un backend interno).

Spring Boot, por defecto, usa AcceptHeaderLocaleResolver. Para permitir al usuario cambiar de idioma, se configura un SessionLocaleResolver junto con un LocaleChangeInterceptor:
java

@Bean
public LocaleResolver localeResolver() {
    SessionLocaleResolver resolver = new SessionLocaleResolver();
    resolver.setDefaultLocale(Locale.forLanguageTag("es"));
    return resolver;
}

@Bean
public LocaleChangeInterceptor localeChangeInterceptor() {
    LocaleChangeInterceptor interceptor = new LocaleChangeInterceptor();
    interceptor.setParamName("lang");
    return interceptor;
}

@Override
public void addInterceptors(InterceptorRegistry registry) {
    registry.addInterceptor(localeChangeInterceptor);
}

Ahora, una petición GET /productos?lang=en cambia el locale para esa sesión.
i18n en plantillas Thymeleaf

Thymeleaf integra el MessageSource mediante la expresión #{…}:
html

<h1 th:text="#{titulo.productos}">Productos</h1>
<p th:text="#{pedido.confirmado(${pedido.id}, ${pedido.total})}">Pedido confirmado</p>

Para fechas y números, Thymeleaf usa #dates.format y #numbers.formatDecimal con el Locale del contexto automáticamente.
i18n en REST y validación

Las anotaciones de Bean Validation también se pueden internacionalizar. En los archivos de validación (messages_es.properties) definimos:
properties

producto.nombre.obligatorio=El nombre del producto es obligatorio
precio.positivo=El precio debe ser positivo

Las anotaciones usan {producto.nombre.obligatorio} como valor de message. Spring MVC, al fallar la validación, resuelve esos mensajes usando el MessageSource y el Locale de la petición.

En un @ControllerAdvice personalizado, también podemos inyectar MessageSource para construir mensajes de error localizados:
java

@ExceptionHandler(RecursoNoEncontradoException.class)
public ResponseEntity<ErrorDTO> manejarNoEncontrado(RecursoNoEncontradoException ex, Locale locale) {
    String mensaje = messageSource.getMessage("error.recurso_no_encontrado", new Object[]{ex.getId()}, locale);
    return ResponseEntity.status(404).body(new ErrorDTO(mensaje));
}

Internacionalización de valores en @ConfigurationProperties

No directamente. Las propiedades de configuración no están pensadas para i18n. Usa mensajes en las vistas o respuestas API.
Buenas prácticas

    Centraliza los mensajes en archivos .properties con nombres descriptivos.

    Usa ReloadableResourceBundleMessageSource en desarrollo.

    Evita mensajes largos con lógica de negocio en las plantillas; mantenlos simples.

    Para aplicaciones con muchos idiomas, considera servicios externos de traducción o un CMS.

09_Miscelaneos/Websockets_y_STOMP.md
WebSockets: comunicación full-duplex

El protocolo WebSocket permite un canal de comunicación persistente y bidireccional entre el cliente (navegador) y el servidor, superando las limitaciones de HTTP (petición-respuesta). Es ideal para notificaciones en tiempo real, chats, dashboards en vivo.

Spring proporciona soporte tanto para WebSockets crudos como para la capa de subprotocolo STOMP (Simple Text Oriented Messaging Protocol), que añade encaminamiento de mensajes mediante destinos (similar a tópicos y colas de mensajería).
Habilitar WebSocket en Spring

Dependencia: spring-boot-starter-websocket.

Configuración básica con STOMP:
java

@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic", "/queue"); // prefijos para destinos del broker
        registry.setApplicationDestinationPrefixes("/app"); // prefijo para mensajes del cliente al servidor
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws")
                .setAllowedOriginPatterns("*")
                .withSockJS(); // habilita fallback SockJS
    }
}

    Broker simple (/topic, /queue): es un broker en memoria que reenvía mensajes a los clientes suscritos.

    /app: prefijo para los destinos de los métodos @MessageMapping (mensajes que llegan del cliente).

    SockJS: emula WebSocket en navegadores antiguos usando long polling.

Controlador de mensajes STOMP

Similar a @Controller MVC pero con anotaciones propias:
java

@Controller
public class ChatController {

    @MessageMapping("/chat.enviar")
    @SendTo("/topic/mensajes")
    public Mensaje enviar(Mensaje mensaje) {
        // se puede persistir aquí
        return mensaje; // se reenvía a todos los suscritos a /topic/mensajes
    }

    @MessageMapping("/chat.privado")
    public void privado(Mensaje msg, Principal principal) {
        // Enviar a un usuario específico (destino /queue/privado-{username})
        simpMessagingTemplate.convertAndSendToUser(msg.getDestinatario(), "/queue/privado", msg);
    }
}

    @MessageMapping("/ruta"): escucha mensajes enviados por clientes a /app/ruta.

    @SendTo: define a qué destino broker se envía el valor de retorno del método (broadcast).

    Principal: disponible si la sesión está autenticada.

Envío de mensajes desde el servidor

Inyectamos SimpMessagingTemplate:
java

@Autowired
private SimpMessagingTemplate messagingTemplate;

public void notificarCambio(Evento evento) {
    messagingTemplate.convertAndSend("/topic/eventos", evento);
}

public void notificarUsuario(String username, Notificacion notif) {
    messagingTemplate.convertAndSendToUser(username, "/queue/notificaciones", notif);
}

convertAndSendToUser envía a un destino único por usuario: internamente se resuelve a /user/{username}/queue/notificaciones. El cliente debe suscribirse a /user/queue/notificaciones.
Autenticación y autorización en STOMP

Spring Security se integra con WebSocket. Se puede interceptar el handshake HTTP para extraer credenciales y luego aplicar seguridad a los destinos:
java

@Configuration
public class WebSocketSecurityConfig implements WebSocketMessageBrokerConfigurer {
    @Override
    public void configureClientInboundChannel(ChannelRegistration registration) {
        registration.interceptors(new ChannelInterceptor() {
            @Override
            public Message<?> preSend(Message<?> message, MessageChannel channel) {
                StompHeaderAccessor accessor = MessageHeaderAccessor.getAccessor(message, StompHeaderAccessor.class);
                if (StompCommand.CONNECT.equals(accessor.getCommand())) {
                    // autenticar vía token en headers
                }
                return message;
            }
        });
    }
}

Y autorización con @PreAuthorize en métodos @MessageMapping.
Broker externo: RabbitMQ o ActiveMQ

Para aplicaciones en cluster, el broker simple no es suficiente porque no replica mensajes entre instancias. Spring permite conectar un broker STOMP externo (RabbitMQ, ActiveMQ) que haga de relay:
java

@Override
public void configureMessageBroker(MessageBrokerRegistry registry) {
    registry.enableStompBrokerRelay("/topic", "/queue")
            .setRelayHost("localhost")
            .setRelayPort(61613)
            .setClientLogin("guest")
            .setClientPasscode("guest");
}

Ahora el broker externo maneja las suscripciones y la distribución, mientras los controladores siguen funcionando igual.
Cliente JavaScript (STOMP.js)
javascript

const socket = new SockJS('/ws');
const stompClient = Stomp.over(socket);
stompClient.connect({}, function(frame) {
    stompClient.subscribe('/topic/mensajes', function(mensaje) {
        // JSON.parse(mensaje.body)
    });
    stompClient.send("/app/chat.enviar", {}, JSON.stringify({texto: "Hola"}));
});

Serialización y mensajes

Spring usa un MessageConverter para convertir entre objetos Java y el cuerpo del mensaje STOMP. Por defecto, MappingJackson2MessageConverter con JSON, configurable.
Consideraciones de escalabilidad y estado

    Los clientes mantienen una sesión con el servidor. En un cluster, el broker externo permite compartir suscripciones.

    El fallback SockJS puede crear múltiples peticiones HTTP; hay que dimensionar el pool de hilos.

    Cuida el envío masivo: para miles de usuarios, el broker externo es obligatorio.

    Las sesiones WebSocket no comparten el HttpSession automáticamente; se puede configurar un HandshakeInterceptor para transferir el usuario autenticado.

09_Miscelaneos/Integracion_JMS_y_Kafka.md
Mensajería asíncrona en Spring

Spring ofrece abstracciones para los dos estándares de mensajería más extendidos: JMS (Java Message Service) para brokers tradicionales como ActiveMQ o Artemis, y Apache Kafka para streaming de eventos de alto rendimiento.

Aunque los detalles difieren, el patrón es similar: un Template para enviar mensajes y un Listener anotado para recibirlos.
Integración JMS
Configuración con Spring Boot

Starter: spring-boot-starter-artemis (o -activemq). Boot autoconfigura una ConnectionFactory y un JmsTemplate a partir de las propiedades:
properties

spring.artemis.mode=native
spring.artemis.broker-url=tcp://localhost:61616
spring.artemis.user=admin
spring.artemis.password=admin

O con ActiveMQ:
properties

spring.activemq.broker-url=tcp://localhost:61616
spring.activemq.user=admin
spring.activemq.password=admin

Envío de mensajes con JmsTemplate
java

@Autowired
private JmsTemplate jmsTemplate;

public void enviarPedido(Pedido pedido) {
    jmsTemplate.convertAndSend("cola.pedidos", pedido);
}

convertAndSend utiliza un MessageConverter (por defecto MappingJackson2MessageConverter si Jackson está presente) para serializar a JSON.

Si necesitas control fino (headers, propiedades JMS), puedes crear un Message con JmsTemplate.send().
Recepción con @JmsListener
java

@Component
public class PedidoListener {

    @JmsListener(destination = "cola.pedidos")
    public void recibirPedido(Pedido pedido) {
        // procesar pedido
    }
}

Para lecturas transaccionales, añade @Transactional al método (si hay un JmsTransactionManager o JtaTransactionManager). También se puede configurar concurrency para paralelismo:
java

@JmsListener(destination = "cola.pedidos", concurrency = "3-10")

Configuración avanzada de JMS

    Destinos dinámicos: usar "dynamicQueues/..." en Artemis.

    Mensajes de texto plano: cambiar MessageConverter por SimpleMessageConverter.

    Dead Letter Queue: configurar en el broker.

    Pub/Sub con tópicos: jmsTemplate.setPubSubDomain(true) y destino tema.nombre.

Integración Apache Kafka
Dependencias y configuración

Starter: spring-kafka. Spring Boot autoconfigura KafkaTemplate y consumer factories.

Propiedades base:
properties

spring.kafka.bootstrap-servers=localhost:9092
spring.kafka.consumer.group-id=pedidos-group
spring.kafka.consumer.key-deserializer=org.apache.kafka.common.serialization.StringDeserializer
spring.kafka.consumer.value-deserializer=org.springframework.kafka.support.serializer.JsonDeserializer
spring.kafka.producer.key-serializer=org.apache.kafka.common.serialization.StringSerializer
spring.kafka.producer.value-serializer=org.springframework.kafka.support.serializer.JsonSerializer

Productor con KafkaTemplate
java

@Autowired
private KafkaTemplate<String, Pedido> kafkaTemplate;

public void enviarPedido(Pedido pedido) {
    kafkaTemplate.send("topic-pedidos", pedido.getId().toString(), pedido)
        .addCallback(
            result -> log.info("Enviado: {}", result.getProducerRecord().value()),
            ex -> log.error("Error", ex)
        );
}

Se envía con una clave para particionamiento. El serializador JSON maneja el objeto.
Consumidor con @KafkaListener
java

@Component
public class PedidoConsumer {

    @KafkaListener(topics = "topic-pedidos", groupId = "pedidos-group")
    public void escuchar(Pedido pedido) {
        // procesar pedido
    }
}

Spring gestiona el offset commit automáticamente (por defecto enable.auto.commit=true, se commit tras el procesamiento). Para control manual, usar Acknowledgment en el parámetro y spring.kafka.consumer.enable-auto-commit=false.
Manejo de errores y reintentos

Se puede configurar un ErrorHandler o SeekToCurrentErrorHandler para reintentos locales:
java

@Bean
public ConcurrentKafkaListenerContainerFactory<String, Pedido> kafkaListenerContainerFactory() {
    ConcurrentKafkaListenerContainerFactory<String, Pedido> factory =
            new ConcurrentKafkaListenerContainerFactory<>();
    factory.setCommonErrorHandler(new DefaultErrorHandler(
            new FixedBackOff(1000L, 3))); // 3 reintentos, 1 seg entre ellos
    return factory;
}

Para dead-letter topics, con DeadLetterPublishingRecoverer se envían los mensajes fallidos a un topic de error.
Procesamiento batch

Se pueden consumir lotes configurando factory.setBatchListener(true) y el método del listener con List<Pedido>.
Kafka Streams con Spring

Spring también soporta escribir aplicaciones de streaming mediante KafkaStreams. Configurando un StreamsBuilder bean se definen topologías. Pero eso ya forma parte de un módulo más avanzado (Spring Cloud Stream con Kafka Streams).
Spring Cloud Stream (abstracción de alto nivel)

Para quienes prefieren una capa aún más alta, Spring Cloud Stream abstrae JMS, Kafka, RabbitMQ y otros bajo un modelo de canales (Source, Sink, Processor). No se cubre aquí en profundidad, pero es importante mencionarlo.
¿Cuándo elegir JMS vs Kafka?

    JMS: transacciones distribuidas tradicionales con garantías "exactly-once" mediante protocolo XA, integración con servidores de aplicaciones, colas y tópicos clásicos. Adecuado para integraciones empresariales clásicas y entornos donde ya existe un broker JMS.

    Kafka: altísimo rendimiento, persistencia inmuttable, retroconsumo (reprocesar eventos), particionamiento, escalado horizontal nativo. Ideal para microservicios con CQRS, event sourcing y datos en tiempo real.

Spring unifica la experiencia de desarrollo con anotaciones y templates similares, lo que facilita migrar o convivir con ambos.


//////////////////////////////////////////////////////////////

///////////////////////////////////////////////
