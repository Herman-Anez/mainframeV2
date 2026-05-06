# Ciclo de vida del Bean: paso a paso con internals

Comprender el ciclo de vida es indispensable para personalizar el comportamiento del contenedor y para entender cómo funcionan las transacciones, aspectos y la seguridad.

## Fases completas del ciclo de vida (arranque de un bean singleton)

Imagina que Spring está arrancando y decide instanciar un bean `MiServicio`. El proceso detallado es:

1. **Instanciación del objeto**
   - Se llama al constructor (o al método estático de fábrica) usando la información de `BeanDefinition`. El objeto es "crudo", sin dependencias.

2. **Inyección de propiedades (dependencias)**
   - Spring inyecta las dependencias vía setters o directamente en campos anotados con `@Autowired`, `@Value`, `@Inject`, etc. Esto lo hacen `BeanPostProcessors` específicos como `AutowiredAnnotationBeanPostProcessor` y `CommonAnnotationBeanPostProcessor`.

3. **Ejecución de interfaces Aware**
   - Si el bean implementa ciertas interfaces Aware, se invocan sus métodos en este orden típico:
     - `BeanNameAware.setBeanName(String name)`
     - `BeanClassLoaderAware.setBeanClassLoader(ClassLoader)`
     - `BeanFactoryAware.setBeanFactory(BeanFactory)` (si es un BeanFactory)
     - `ApplicationContextAware.setApplicationContext(ApplicationContext)` (solo en contexto ApplicationContext)
   - De esta forma, el bean puede obtener referencias al entorno de Spring sin buscar el contexto por fuera.

4. **BeanPostProcessor – Antes de inicialización**
   - Para cada `BeanPostProcessor` registrado, se ejecuta `postProcessBeforeInitialization(bean, beanName)`. Aquí se puede modificar el bean, envolverlo en un proxy temprano, o hacer cualquier lógica transversal (p.ej., en Spring AOP se marcan los beans candidatos a ser proxy, aunque el proxy real se crea después).
   - Ejemplo común: `InitDestroyAnnotationBeanPostProcessor` busca métodos `@PostConstruct` pero su ejecución real ocurrirá en el siguiente paso, no aquí; esta fase es más de preparación.

5. **Inicialización del bean**
   Se ejecutan los métodos de inicialización en el siguiente orden de prioridad:
   - a. Método anotado con `@PostConstruct` (detectado por el `CommonAnnotationBeanPostProcessor` que se ejecutó antes).
   - b. `afterPropertiesSet()` de la interfaz `InitializingBean`.
   - c. Método `init-method` personalizado definido en `@Bean(initMethod = "nombre")` o en XML.
   - Durante esta fase el bean puede configurarse a sí mismo, validar dependencias o iniciar recursos.

6. **BeanPostProcessor – Después de inicialización**
   - Se ejecuta `postProcessAfterInitialization(bean, beanName)`. Esta es la etapa donde normalmente se generan los proxies (AOP, transacciones, seguridad). Si el bean necesita ser envuelto en un proxy, el `AbstractAutoProxyCreator` (un `BeanPostProcessor`) reemplaza la instancia original por un proxy CGLIB o JDK. Por eso si llamas a un método interno dentro del mismo bean, la anotación `@Transactional` no se aplica: porque la llamada no pasa por el proxy.

7. **El bean está listo para ser usado**
   - El bean se almacena en el contenedor singleton (en un `ConcurrentHashMap`). Cualquier otra dependencia que lo necesite recibirá el bean ya completamente vestido.

8. **Destrucción del bean (al cerrar el contexto)**
   - Métodos anotados con `@PreDestroy`.
   - `destroy()` de `DisposableBean` interface.
   - Método `destroy-method` personalizado de `@Bean` o XML.
   - Los `DestructionAwareBeanPostProcessor` pueden ejecutar lógica previa.

## Diagrama resumido (texto)

```text
[Constructor o Fábrica] --> [Inyección de Deps] --> [Aware: BenaName, ApplicationContext, etc.]
--> [BeanPostProcessor::before] --> [@PostConstruct / afterPropertiesSet / init-method]
--> [BeanPostProcessor::after] (proxies creados aquí) --> [Bean listo]
--> [Al cerrar: @PreDestroy / destroy()]
```

## Extensiones poderosas: BeanFactoryPostProcessor y BeanDefinitionRegistryPostProcessor

Antes de que ningún bean sea instanciado, el contenedor permite modificar las propias definiciones de los beans. Los `BeanFactoryPostProcessor` trabajan con el `BeanFactory` (en realidad `ConfigurableListableBeanFactory`). Los `BeanDefinitionRegistryPostProcessor` pueden incluso registrar nuevas definiciones de beans.

El caso más famoso es `ConfigurationClassPostProcessor`, que procesa todas las clases `@Configuration`, `@ComponentScan` y `@Import` para registrar las definiciones correspondientes.

Ejemplo: modificar una propiedad tras la lectura del Classpath

```java
@Component
public class CustomBeanFactoryPostProcessor implements BeanFactoryPostProcessor {
    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) {
        BeanDefinition bd = beanFactory.getBeanDefinition("dataSource");
        bd.getPropertyValues().add("maxPoolSize", 20);
    }
}
```

## Ejemplo práctico de un BeanPostProcessor personalizado

Supón que quieres medir el tiempo de ejecución de todos los métodos de los beans de un paquete.

```java
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
```

Este processor envuelve el bean en un proxy JDK justo después de la inicialización, añadiendo el comportamiento de medición.

## ¿Por qué es vital este entendimiento?

- Te permite implementar cross-cutting concerns sin necesidad de AOP declarativa para casos específicos.
- Explica por qué funciona `@Transactional`: un `BeanPostProcessor` crea el proxy que maneja la transacción alrededor del método real.
- Depuración de problemas de beans: si una dependencia se resuelve mal, sabrás en qué fase mirar.

---

[⬅️ Volver al Índice](../../index.md)
