# Aspectos Personalizados en Spring AOP

Aquí mostramos cómo crear aspectos desde cero, incluyendo técnicas avanzadas para resolver problemas concretos.

## Estructura básica de un aspecto personalizado

Todo aspecto requiere:

*   **@Aspect** en la clase.
*   **@Component** (u otra forma de registro) para que Spring lo detecte.
*   Uno o varios métodos anotados con **@Pointcut** (opcional, pero buena práctica).
*   Métodos de advice anotados con **@Before**, **@Around**, etc.

## Ejemplo: Sistema de caché declarativa con @Around y anotación personalizada

Creemos una anotación `@CacheableResult` que almacene el resultado de un método en un `ConcurrentHashMap` durante un tiempo.

**Anotación:**

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface CacheableResult {
    long ttlMillis() default 30000;
    String key() default "";
}
```

**Aspecto:**

```java
@Aspect
@Component
public class CacheAspect {
    private final ConcurrentHashMap<String, CacheEntry> cache = new ConcurrentHashMap<>();

    @Around("@annotation(cacheable)")
    public Object cacheMethod(ProceedingJoinPoint pjp, CacheableResult cacheable) throws Throwable {
        String key = buildKey(pjp, cacheable);
        CacheEntry entry = cache.get(key);
        if (entry != null && (System.currentTimeMillis() - entry.timestamp) < cacheable.ttlMillis()) {
            return entry.value;
        }
        Object result = pjp.proceed();
        cache.put(key, new CacheEntry(result, System.currentTimeMillis()));
        return result;
    }

    private String buildKey(ProceedingJoinPoint pjp, CacheableResult cacheable) {
        String customKey = cacheable.key();
        if (!customKey.isEmpty()) return customKey;
        // Genera clave por clase + método + argumentos
        return pjp.getTarget().getClass().getSimpleName() + "." 
               + pjp.getSignature().getName() + ":" 
               + Arrays.toString(pjp.getArgs());
    }

    private static class CacheEntry {
        final Object value;
        final long timestamp;
        CacheEntry(Object value, long timestamp) { this.value = value; this.timestamp = timestamp; }
    }
}
```

**Uso en un servicio:**

```java
@Service
public class DatosExternosService {
    @CacheableResult(ttlMillis = 60000, key = "ultimo-precio")
    public BigDecimal obtenerPrecioActual() {
        // Operación costosa (API externa)
        return new BigDecimal("100.5");
    }
}
```

## Pasando parámetros del método al advice

Se puede ligar un parámetro del pointcut al advice mediante `args` y nombre de parámetro. Ejemplo para validar una restricción de acceso:

```java
@Before("execution(* com.empresa..*Service.*(Long,..)) && args(id)")
public void validarId(Long id) {
    if (id == null || id <= 0) {
        throw new IllegalArgumentException("ID inválido: " + id);
    }
}
```

O usando `JoinPoint` para obtener argumentos dinámicamente.

## Aspectos con lógica condicional (combinando con contexto)

Puedes exponer el proxy actual con `AopContext.currentProxy()` (requiere `@EnableAspectJAutoProxy(exposeProxy = true)`) para solucionar el problema de auto-invocación, o combinar chequeos de perfiles:

```java
@Around("execution(* com.empresa..*Controller.*(..))")
public Object medirSoloEnDev(ProceedingJoinPoint pjp) throws Throwable {
    if (EnvironmentUtils.esDev()) {
        long t0 = System.currentTimeMillis();
        Object result = pjp.proceed();
        System.out.println("DEV: " + (System.currentTimeMillis() - t0) + "ms");
        return result;
    }
    return pjp.proceed(); // en otros entornos no mide
}
```

## Registro de eventos de negocio con @AfterReturning y publicación de eventos Spring

Podemos acoplar AOP con el modelo de eventos de Spring para desacoplar aún más.

```java
@Aspect
@Component
public class EventPublisherAspect {
    private final ApplicationEventPublisher publisher;

    public EventPublisherAspect(ApplicationEventPublisher publisher) {
        this.publisher = publisher;
    }

    @AfterReturning(
        pointcut = "@annotation(com.empresa.evento.PublicarEvento)",
        returning = "result"
    )
    public void publicar(JoinPoint jp, Object result) {
        PublicarEvento anotacion = obtenerAnotacion(jp); // helper con reflexión
        publisher.publishEvent(new NegocioEvento(anotacion.tipo(), result));
    }
}
```

## Buenas prácticas en aspectos personalizados

*   **Un aspecto, una responsabilidad:** no mezcles medición de tiempos con seguridad. Mantenlos pequeños y enfocados.
*   **Usa @Pointcut para centralizar expresiones:** facilita el mantenimiento.
*   **Prefiere @Around solo cuando realmente necesitas el control total;** los otros consejos son más semánticos y seguros.
*   **Evita lógica pesada o transaccional dentro del advice;** no invoques servicios que a su vez puedan ser interceptados (cuidado con dependencias circulares indirectas).
*   **Considera la trazabilidad:** un advice no debe causar pérdida de información de excepciones ni alterar la semántica del método a menos que así lo hayas diseñado.

---

[⬅️ Anterior: Conceptos JoinPoint, Pointcut, Advice](./Conceptos_JoinPoint_Pointcut_Advice.md) | [Siguiente: Proxies JDK vs CGLIB ➡️](./Proxies_JDK_vs_CGLIB.md)
