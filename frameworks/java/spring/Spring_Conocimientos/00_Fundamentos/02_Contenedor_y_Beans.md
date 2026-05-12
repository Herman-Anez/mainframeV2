# Contenedor y Beans: El motor interno

## BeanFactory vs. ApplicationContext

- **BeanFactory:** Es la interfaz raíz, proporciona las capacidades básicas: crear, obtener y mantener beans. Tiene carga perezosa (*lazy load*) por defecto. No posee funcionalidades de internacionalización, eventos, etc. Rara vez se usa directamente.
- **ApplicationContext:** Hereda de `BeanFactory` y añade capacidades empresariales:
  - Carga automática de *bean post-processors* y beans de configuración (incluye `BeanFactoryPostProcessor`).
  - Publicación de eventos (`ApplicationEventPublisher`).
  - Acceso a mensajes y recursos (`MessageSource`, cargar archivos `.properties` i18n).
  - Soporte para múltiples fuentes de configuración (web, xml, anotaciones).
  - Registro automático de `BeanPostProcessor`.

> [!IMPORTANT]
> En la práctica siempre usamos `ApplicationContext`. Spring Boot crea un `AnnotationConfigApplicationContext` o un `AnnotationConfigServletWebServerApplicationContext`.

## BeanDefinition y el registro de beans

Cuando Spring arranca, no almacena directamente instancias de beans, sino sus definiciones en una estructura **`BeanDefinition`**. Una `BeanDefinition` contiene:

- **Nombre del bean** (id).
- **Nombre de la clase** (className).
- **Ámbito** (scope: singleton, prototype...).
- **Dependencias** (nombres de otros beans).
- **Modo de inicialización** (lazy o eager).
- **Métodos de callback** (init/destroy).
- **Banderas:** Si es abstracto, primario, etc.

Estas definiciones se cargan a través de un `BeanDefinitionReader` (para XML sería `XmlBeanDefinitionReader`, para anotaciones `AnnotatedBeanDefinitionReader`) y se almacenan en un `BeanDefinitionRegistry` (normalmente el mismo `ApplicationContext`).

### Ejemplo de configuración programática

```java
AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext();
ctx.register(AppConfig.class); // registra una clase @Configuration
ctx.refresh(); // aquí se procesan las definiciones y se instancian los beans
```

## Component Scanning: Cómo encuentra Spring tus beans

**`@ComponentScan`** indica los paquetes base donde buscar clases anotadas con estereotipos (`@Component`, `@Service`, `@Repository`, `@Controller`). Spring escanea el *classpath* y crea una `BeanDefinition` por cada clase encontrada que cumpla con los filtros.

Puedes afinar con:

- `basePackages` o `basePackageClasses` para evitar escanear todo.
- `includeFilters` y `excludeFilters` con expresiones como `@ComponentScan.Filter(type=FilterType.REGEX, pattern=".*Test")` o `FilterType.ASSIGNABLE_TYPE`.

> [!NOTE]
> **Estereotipos:** `@Service`, `@Repository` y `@Controller` son especializaciones de `@Component` que añaden semántica. En particular `@Repository` habilita la traducción de excepciones de persistencia a la jerarquía `DataAccessException` de Spring.

## Inicialización perezosa vs. ansiosa (Eager)

Por defecto, los beans singleton se crean en el arranque (**eager**), lo que ayuda a detectar fallos de configuración rápidamente. Se puede marcar un bean con **`@Lazy`** para que se cree solo cuando sea requerido.

> [!TIP]
> **A nivel global:** En Spring Boot, `spring.main.lazy-initialization=true` hace que todos los beans sean perezosos.

## Configuración Java: `@Configuration` y `@Bean`

Una clase `@Configuration` es una forma elegante de definir beans mediante métodos anotados con `@Bean`. El contenedor llamará a esos métodos y registrará el objeto devuelto.

### Conceptos clave:

- **`proxyBeanMethods = true` (por defecto):** Spring crea un proxy de la clase de configuración mediante **CGLIB** para interceptar las llamadas a los métodos `@Bean`. Así, si dentro de un método `@Bean` se invoca a otro método `@Bean`, se devuelve la instancia única del contenedor en lugar de crear una nueva, respetando el ámbito singleton.
- **`proxyBeanMethods = false` (Modo ligero o "Lite mode"):** No se genera proxy; las llamadas entre métodos `@Bean` invocan directamente el método Java, creando un nuevo objeto cada vez. Es más rápido y útil cuando no hay dependencia entre los beans definidos.

```java
@Configuration(proxyBeanMethods = false)
public class AppConfig {
    @Bean
    public DataSource dataSource() {
        return ...; // único
    }
    
    @Bean 
    public JdbcTemplate jdbcTemplate(DataSource ds) {
        return new JdbcTemplate(ds); // Inyección por parámetro recomendada en Lite Mode
    }
}
```

## Internacionalización, Eventos y Recursos

**`ApplicationContext`** extiende `MessageSource`. Si defines un bean `messageSource`, Spring lo utiliza para resolver mensajes multi-idioma con `getMessage(String code, Object[] args, Locale)`. Ideal para mensajes de validación o UI.

Los **eventos de aplicación** (`ApplicationEvent` y `@EventListener`) permiten comunicación desacoplada entre componentes. El publicador no conoce a los suscriptores.

La interfaz **`ResourceLoader`** del contexto permite cargar archivos con prefijos: `classpath:`, `file:`, `http:`, etc.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [IoC y DI](./01_IoC_y_DI.md) | [Índice](../../index.md) | [Configuración Java vs XML](./03_Configuracion_Java_vs_XML.md) |
