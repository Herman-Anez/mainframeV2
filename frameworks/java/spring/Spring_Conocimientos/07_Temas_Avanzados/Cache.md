# Temas_Avanzados/Cache.md
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
