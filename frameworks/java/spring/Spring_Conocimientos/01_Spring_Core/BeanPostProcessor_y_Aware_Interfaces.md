# El secreto para extender el contenedor: BeanPostProcessor

Un `BeanPostProcessor` permite ejecutar lógica antes y después de la inicialización de cada bean. No solo es un mecanismo para observar, sino para modificar o envolver beans. Todos los comportamientos transversales (inyección de dependencias, proxies transaccionales, seguridad, programación de tareas) se implementan a través de ellos.

La interfaz tiene dos métodos:

```java
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
```

- `postProcessBeforeInitialization`: se ejecuta después de la inyección de dependencias pero antes de los callbacks de inicialización (`@PostConstruct`, `afterPropertiesSet`, etc.).
- `postProcessAfterInitialization`: se ejecuta después de los callbacks de inicialización. Aquí es donde típicamente se crean los proxies (transacciones, seguridad, aspectos).

> [!NOTE]
> Ambos pueden devolver el mismo bean o uno diferente (un wrapper). Si devuelves `null`, el bean no se registrará.

Ejemplo básico: logging de beans

```java
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
```

## BeanFactoryPostProcessor vs BeanPostProcessor

No confundir estas dos interfaces:

- **BeanFactoryPostProcessor:** opera sobre las definiciones de los beans (antes de que se creen). Puede modificar propiedades de `BeanDefinition`, añadir nuevos beans, etc. El ejemplo más famoso es `ConfigurationClassPostProcessor`, que procesa las anotaciones `@Configuration`, `@ComponentScan`, etc.
- **BeanPostProcessor:** opera sobre instancias de beans ya creadas.

> [!WARNING]
> Ambos son extensiones muy potentes y se aplican a todos los beans, por lo que hay que filtrar cuidadosamente para no dañar infraestructura interna.

## Ejemplos reales de BeanPostProcessor en Spring

- `AutowiredAnnotationBeanPostProcessor`: procesa `@Autowired` y `@Value`.
- `CommonAnnotationBeanPostProcessor`: maneja `@PostConstruct`, `@PreDestroy`, `@Resource`.
- `AbstractAutoProxyCreator` (como `InfrastructureAdvisorAutoProxyCreator`): crea los proxies AOP para `@Transactional`, `@Cacheable`, etc., en `postProcessAfterInitialization`.
- `ServletContextAwareProcessor` y similares: invocan las interfaces Aware.

## Crear un BeanPostProcessor personalizado

Imagina que quieres medir el tiempo de ejecución de todos los métodos de los beans de un paquete sin usar AOP. Puedes crear un proxy en `postProcessAfterInitialization`:

```java
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
```

## Interfaces Aware: darle al bean acceso al contenedor

Un bean puede querer conocer su nombre, el `ApplicationContext` o el `BeanFactory`. Spring lo consigue mediante interfaces “Aware”. Cuando el contenedor detecta que un bean implementa alguna de estas interfaces, inyecta la dependencia correspondiente en el momento adecuado.

Principales interfaces Aware:

| Interfaz | Descripción | Método |
|---|---|---|
| `BeanNameAware` | Recibe su nombre dentro del contenedor | `setBeanName(String name)` |
| `BeanFactoryAware` | Accede al BeanFactory que lo contiene | `setBeanFactory(BeanFactory factory)` |
| `ApplicationContextAware` | El contexto completo | `setApplicationContext(ApplicationContext ctx)` |
| `MessageSourceAware` | Para resolución de mensajes i18n | `setMessageSource(MessageSource ms)` |
| `ApplicationEventPublisherAware` | Para publicar eventos | `setApplicationEventPublisher(ApplicationEventPublisher pub)` |
| `EnvironmentAware` | Acceso al Environment (propiedades, perfiles) | `setEnvironment(Environment env)` |
| `ResourceLoaderAware` | Para cargar recursos del classpath, etc. | `setResourceLoader(ResourceLoader loader)` |
| `ServletContextAware` (web) | El ServletContext de la aplicación web | `setServletContext(ServletContext context)` |

Ejemplo: un bean que necesita publicar eventos sin inyectar el publicador (aunque siempre es preferible la inyección):

```java
@Component
public class MiComponente implements ApplicationEventPublisherAware {
    private ApplicationEventPublisher publisher;

    @Override
    public void setApplicationEventPublisher(ApplicationEventPublisher publisher) {
        this.publisher = publisher;
    }
    // ...
}
```

> [!TIP]
> ¿Son buenas prácticas? En general, preferimos la inyección de dependencias explícita (`@Autowired` o constructor). Las interfaces Aware acoplan tu código al framework más de lo necesario, pero son útiles en casos de infraestructura o cuando se está desarrollando una librería que necesita interactuar con Spring sin recibir inyecciones tradicionales.

## Orden de ejecución combinado

El contenedor sigue un orden preciso cuando crea un bean:

1. Instanciación (constructor o factory method).
2. Inyección de dependencias (campo/setter) – manejada por `AutowiredAnnotationBeanPostProcessor`.
3. Llamada a Aware interfaces en orden: `BeanNameAware` → `BeanClassLoaderAware` → `BeanFactoryAware` → `ApplicationContextAware` → otros.
4. `BeanPostProcessor.postProcessBeforeInitialization(...)` (puede modificar el bean).
5. Inicialización: `@PostConstruct` → `afterPropertiesSet()` → `init-method` personalizado.
6. `BeanPostProcessor.postProcessAfterInitialization(...)` (creación de proxies, aspectos).
7. El bean ya está listo para su uso.

Conocer este orden te permite depurar problemas de inyección, proxies o valores `null` en métodos init.

---

[⬅️ Volver al Índice](../../index.md)
