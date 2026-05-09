# Conceptos de AOP: JoinPoint, Pointcut y Advice

## ¿Qué es AOP? El problema que resuelve

En una aplicación OOP, hay preocupaciones que atraviesan múltiples capas: registro de auditoría, manejo de transacciones, seguridad, control de caché, medición de rendimiento. Si no se tratan con cuidado, el mismo código se repite por todas partes (**código cross-cutting**). AOP permite encapsular ese comportamiento en módulos llamados **aspectos** y aplicarlo de forma declarativa, sin modificar la lógica de negocio.

Spring AOP se basa en **proxies** para interceptar ejecuciones de métodos y añadir comportamiento antes, después o alrededor de dichas invocaciones.

## Terminología fundamental

*   **Join point:** Un punto durante la ejecución del programa donde se puede insertar un aspecto. En Spring AOP, un join point siempre es la ejecución de un método (nunca acceso a campos o inicialización de clases, como en AspectJ completo).
*   **Pointcut (punto de corte):** Un predicado o expresión que selecciona uno o varios join points. Define en qué métodos debe aplicarse el consejo. Ej: `execution(* com.empresa..servicio.*.*(..))`.
*   **Advice (consejo):** El código que se ejecuta en un join point. Define qué hacer y cuándo (antes, después, alrededor, etc.). Es la implementación real de la preocupación transversal.
*   **Aspect (aspecto):** La combinación de un pointcut y un advice. En Spring se modela con una clase anotada con `@Aspect` que contiene métodos de pointcut y métodos de advice.
*   **Weaving (tejido):** Proceso de aplicar los aspectos a los objetos objetivo para crear objetos proxy. En Spring AOP ocurre en tiempo de ejecución mediante proxies dinámicos.
*   **Target object:** El objeto original que será interceptado por el consejo.
*   **Proxy:** El objeto creado por Spring AOP que envuelve al target e implementa las interceptaciones.
*   **Introduction:** Posibilidad de añadir nuevos métodos o interfaces a un objeto existente. En Spring AOP se logra mediante `@DeclareParents`.

## Tipos de Advice en detalle

Un advice puede aplicarse en distintos momentos del ciclo de ejecución del método:

| Tipo | Anotación | Momento de ejecución |
| :--- | :--- | :--- |
| **Before** | `@Before` | Antes de la ejecución del método. |
| **AfterReturning** | `@AfterReturning` | Después de que el método retorne exitosamente (sin excepción). |
| **AfterThrowing** | `@AfterThrowing` | Después de que el método lance una excepción. |
| **After (finally)** | `@After` | Siempre, sin importar si hubo éxito o excepción. |
| **Around** | `@Around` | Rodea completamente el método, tiene control sobre cuándo y si se ejecuta, y puede modificar argumentos y valor de retorno. |

### @Before

El consejo se invoca antes de la ejecución del método objetivo. No puede evitar que el método se ejecute, salvo que lance una excepción.

```java
@Aspect
@Component
public class LoggingAspect {
    @Before("execution(* com.empresa..*Service.*(..))")
    public void logBefore(JoinPoint joinPoint) {
        System.out.println("Llamando a: " + joinPoint.getSignature().toShortString());
    }
}
```

Se puede acceder a los parámetros del join point a través del objeto `JoinPoint`.

### @AfterReturning

Se ejecuta después de un retorno normal. Puede obtener el valor retornado mediante el atributo `returning`.

```java
@AfterReturning(
    pointcut = "execution(* com.empresa..*Repository.save(..))",
    returning = "result"
)
public void logAfterReturning(JoinPoint joinPoint, Object result) {
    System.out.println(joinPoint.getSignature().getName() + " retornó " + result);
}
```

El nombre de la variable en el argumento del método debe coincidir con el atributo `returning`.

### @AfterThrowing

Interviene cuando el método lanza una excepción. Puede capturar la excepción lanzada con `throwing`.

```java
@AfterThrowing(
    pointcut = "execution(* com.empresa..*Service.*(..))",
    throwing = "ex"
)
public void logAfterThrowing(JoinPoint joinPoint, Exception ex) {
    System.err.println("Error en " + joinPoint.getSignature() + ": " + ex.getMessage());
}
```

### @After (finally)

Se ejecuta en cualquier terminación, como un bloque `finally`. Ideal para liberar recursos o registrar el fin de la operación.

```java
@After("execution(* com.empresa..*Service.procesar(..))")
public void logAfter(JoinPoint joinPoint) {
    System.out.println("Finalizó: " + joinPoint.getSignature());
}
```

### @Around (el más poderoso y complejo)

Tiene el control total: puede modificar argumentos, decidir si invoca o no `proceed()`, alterar el valor de retorno, medir el tiempo y manejar excepciones.

```java
@Around("execution(* com.empresa..*Service.calcular*(..))")
public Object medirTiempo(ProceedingJoinPoint pjp) throws Throwable {
    long inicio = System.nanoTime();
    Object resultado = pjp.proceed(); // ejecuta el método original
    long tiempo = System.nanoTime() - inicio;
    System.out.println(pjp.getSignature() + " tardó " + tiempo + " ns");
    return resultado;
}
```

> [!CAUTION]
> Si no se llama a `proceed()` se omite la ejecución original, y si no se retorna su resultado, se silencia el valor de retorno real. Además, `ProceedingJoinPoint` es una subinterfaz de `JoinPoint` que añade `proceed()`.

## Pointcut: el arte de seleccionar join points

Las expresiones de pointcut se basan en un lenguaje propio. Los designadores más importantes son:

*   **execution:** el más común. Define la firma del método a interceptar.
    *   Patrón: `execution(modificadores? tipo-retorno nombre-clase.nombre-metodo(parametros) throws-excepcion?)`
    *   Ejemplos:
        *   `execution(* com.empresa.servicio.*.*(..))`: cualquier método de cualquier clase en ese paquete.
        *   `execution(public String com.empresa..*.*(Long,..))`: métodos públicos que retornan String, comienzan con un Long y luego cualquier número de parámetros.
        *   `execution(* *..*Service.*(..))`: métodos de cualquier clase cuyo nombre termina en "Service".
*   **within:** limita a métodos dentro de ciertos tipos o paquetes.
    *   `within(com.empresa.servicio.*)`: todos los métodos de las clases en ese paquete.
    *   `within(com.empresa..*)`: paquete y subpaquetes.
*   **this y target:** `this(com.empresa.Interface)` hace referencia al objeto proxy; `target` al objeto objetivo. Útiles cuando se necesita que el objeto sea de un tipo específico.
*   **args:** selecciona según los tipos de parámetros en tiempo de ejecución.
    *   `args(java.io.Serializable)`: métodos con un parámetro serializable.
*   **@annotation:** intercepta métodos anotados con una anotación determinada.
    *   `@annotation(com.empresa.Auditable)`: excelente para preocupaciones transversales basadas en anotaciones.
*   **@within:** clase anotada con una anotación específica.
*   **@args:** la anotación está en los argumentos en tiempo de ejecución.
*   **bean (Spring AOP):** permite referenciar beans por nombre con comodines: `bean(*Service)`.

Se pueden combinar con `&&`, `||` y `!`:

```java
@Pointcut("execution(public * *(..)) && within(com.empresa..*)")
public void metodosPublicos() {}
```

## Escribiendo un aspecto completo

```java
@Aspect
@Component
public class AuditoriaAspect {

    // Pointcut reusable
    @Pointcut("execution(* com.empresa..*Service.*(..))")
    public void capaServicio() {}

    @Pointcut("@annotation(com.empresa.anotaciones.Auditable)")
    public void metodosAuditables() {}

    @Before("capaServicio() && metodosAuditables()")
    public void auditar(JoinPoint jp) {
        // Acceso a parámetros
        Object[] args = jp.getArgs();
        String usuario = SecurityContextHolder.getContext().getAuthentication().getName();
        System.out.println(usuario + " ejecuta " + jp.getSignature() + " con " + Arrays.toString(args));
    }
}
```

## Ordenación de aspectos

Cuando varios aspectos aplican al mismo join point, se puede controlar el orden con `@Order` (número más bajo = mayor prioridad) o implementando `Ordered`.

> [!NOTE]
> En el caso de `@Before`, el de menor orden se ejecuta primero; en `@After` y `@Around`, el último en ejecutarse es el de menor orden (como capas de cebolla).

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [SpEL](../01_Spring_Core/SpEL.md) | [Índice](../../index.md) | [Aspectos Personalizados](./Aspectos_personalizados.md) |
