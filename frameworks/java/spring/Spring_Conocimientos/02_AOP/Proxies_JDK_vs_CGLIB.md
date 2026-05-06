# Proxies en Spring AOP: JDK vs CGLIB

## Spring AOP es proxy-based AOP

Spring AOP no modifica bytecode como AspectJ (weaving en compilación o carga). En su lugar, en tiempo de ejecución, el contenedor crea un objeto **proxy** que envuelve al bean objetivo. Las llamadas externas al bean pasan por el proxy, que aplica los interceptores (aspectos). Toda la magia de `@Transactional`, `@Cacheable`, `@Secured`, etc., ocurre a través de estos proxies.

## JDK Dynamic Proxy

Si el bean objetivo implementa al menos una interfaz, Spring utilizará por defecto un proxy dinámico de JDK.

### Cómo funciona internamente

1.  Se llama a `java.lang.reflect.Proxy.newProxyInstance(ClassLoader, interfaces, InvocationHandler)`.
2.  Se crea una clase proxy en tiempo de ejecución que implementa las mismas interfaces que el target.
3.  Cualquier invocación de un método de esas interfaces es redirigida al `InvocationHandler`, que puede ejecutar los advisors, consejos y delegar al target mediante reflexión (`Method.invoke(target, args)`).

**Ejemplo simplificado:**

```java
MiServicio target = new MiServicioImpl();
MiServicio proxy = (MiServicio) Proxy.newProxyInstance(
    MiServicio.class.getClassLoader(),
    new Class[]{MiServicio.class},
    (proxyObj, method, args) -> {
        System.out.println("Antes del método " + method.getName());
        Object result = method.invoke(target, args);
        System.out.println("Después");
        return result;
    }
);
proxy.hacerAlgo(); // pasa por el handler
```

### Ventajas e Inconvenientes

*   **Ventajas:**
    *   Más liviano que CGLIB, forma parte del JDK.
    *   Permite que el proxy solo prometa la interfaz, más desacoplado.
*   **Limitaciones:**
    *   Solo puede interceptar métodos definidos en la interfaz.
    *   El target debe implementar interfaces; no funciona con clases concretas sin interfaz.
    *   `this.invocacionInterna()` dentro del target no es interceptada porque `this` es el target, no el proxy.

## CGLIB Proxy

Si el bean no implementa interfaces, Spring crea un proxy generando una subclase con la librería CGLIB (Code Generation Library).

### Mecanismo

1.  CGLIB utiliza `Enhancer` para generar una subclase del bean target en tiempo de ejecución.
2.  Sobrescribe los métodos públicos no finales para delegar en un `MethodInterceptor`.
3.  Cuando se llama a un método, se invoca al interceptor, que ejecuta los consejos y luego llama al método de la superclase (`super.metodo()`) o directamente al target si está configurado como callback.

**Ejemplo conceptual:**

```java
Enhancer enhancer = new Enhancer();
enhancer.setSuperclass(MiServicioConcreto.class);
enhancer.setCallback((MethodInterceptor) (obj, method, args, proxy) -> {
    System.out.println("Antes");
    Object result = proxy.invokeSuper(obj, args); // llama al método real
    System.out.println("Después");
    return result;
});
MiServicioConcreto proxy = (MiServicioConcreto) enhancer.create();
proxy.hacerAlgo(); // interceptado
```

### Ventajas e Inconvenientes

*   **Ventajas:**
    *   No requiere que el bean implemente interfaces.
    *   Puede interceptar todos los métodos públicos de la clase (si no son `final`).
*   **Limitaciones:**
    *   No puede interceptar métodos `final` ni clases `final` (CGLIB no puede subclasear).
    *   Los constructores se ejecutan dos veces: una para el target (CGLIB suele crear una instancia del target usando Objenesis que no llama al constructor completo, solo asigna memoria) y otra para la subclase proxy.
    *   Aumenta ligeramente el tiempo de creación y el uso de memoria.
    *   `this` dentro del target sigue siendo el target, no el proxy, por lo que las llamadas internas no pasan por el proxy.

## ¿Cuándo usa Spring cada uno?

La decisión se toma en el `DefaultAopProxyFactory`. La lógica es:

1.  Si `proxyTargetClass` es `true` (configurado con `@EnableAspectJAutoProxy(proxyTargetClass = true)` o en Boot `spring.aop.proxy-target-class=true`), fuerza CGLIB incluso si hay interfaces.
2.  Si `proxyTargetClass` es `false` (por defecto), se evalúa:
    *   Si el bean implementa al menos una interfaz, usa JDK dynamic proxy.
    *   Si no, usa CGLIB.

> [!NOTE]
> En Spring Boot, por defecto `spring.aop.proxy-target-class=true`, por lo que se usa CGLIB a menos que se cambie explícitamente.

> [!WARNING]
> **Ojo con el casteo:** si tu código espera un objeto de tipo concreto y Spring te entrega un proxy JDK que solo implementa la interfaz, obtendrás `ClassCastException`. Por eso se prefiere programar contra interfaz o forzar CGLIB.

### Configuración explícita

```java
@Configuration
@EnableAspectJAutoProxy(proxyTargetClass = true) // fuerza CGLIB
public class AppConfig { }
```

## El problema de la auto-invocación (self-invocation)

Este es el punto más importante y malinterpretado. Como el proxy envuelve al target, cuando desde fuera se llama a `bean.metodoA()`, la llamada va al proxy, que aplica los aspectos. Pero si `metodoA()` internamente llama a `this.metodoB()`, `this` es el target, no el proxy, por lo que `metodoB()` no pasa por los aspectos.

> [!IMPORTANT]
> Anotaciones como `@Transactional` en `metodoB` no tienen efecto si se llama desde `metodoA` dentro del mismo bean.

**Demostración:**

```java
@Service
public class TransaccionalService {
    @Transactional
    public void metodoBatch() {
        for (Item i : items) {
            this.procesarItem(i); // ¡problema! this es el target
        }
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void procesarItem(Item i) {
        // ... debería ejecutarse en transacción separada, pero no lo hará
    }
}
```

### Soluciones

1.  **Reestructurar:** mover `procesarItem` a otro bean e inyectarlo.
    ```java
    @Service
    public class ProcesadorItemService {
        @Transactional(propagation = Propagation.REQUIRES_NEW)
        public void procesarItem(Item i) { ... }
    }
    // en el batch:
    @Autowired private ProcesadorItemService procesador;
    public void metodoBatch() {
        for (Item i : items) procesador.procesarItem(i); // ahora sí es proxy
    }
    ```
2.  **Obtener el proxy mediante AopContext.currentProxy():**
    *   Habilitar `exposeProxy = true`: `@EnableAspectJAutoProxy(exposeProxy = true)`.
    *   Luego en el código: `((TransaccionalService) AopContext.currentProxy()).procesarItem(i);`
3.  **Inyectarse a sí mismo (con @Autowired o @Resource):**
    ```java
    @Autowired
    private TransaccionalService self;
    public void metodoBatch() {
        self.procesarItem(i); // self es el proxy
    }
    ```
    > [!NOTE]
    > Esto crea una dependencia circular que Spring maneja, pero puede confundir.

## Diferencias internas y de rendimiento

*   **Arranque:** JDK proxy es más rápido de crear porque es una función del JDK. CGLIB genera una nueva clase en memoria, lo que implica más trabajo.
*   **Invocación:** En JDK proxy, cada llamada usa reflexión (`Method.invoke`). CGLIB puede generar bytecode que evita reflexión después de la primera invocación, siendo marginalmente más rápido. En la práctica, la diferencia es ínfima.
*   **Compatibilidad:** Si usas Java moderno (17+) y necesitas características como records o sealed classes, CGLIB puede tener problemas (aunque Spring ya se ha adaptado).

## Tip de depuración: identificación del proxy

Si en tiempo de ejecución necesitas saber si un bean es un proxy, puedes inspeccionar su clase:

```java
if (bean instanceof SpringProxy) {
    System.out.println("Es un proxy de Spring");
}
```

`SpringProxy` es una interfaz marcadora implementada por todos los proxies de Spring AOP.

---

[⬅️ Anterior: Aspectos Personalizados](./Aspectos_personalizados.md) | [Volver al índice](../README.md)
