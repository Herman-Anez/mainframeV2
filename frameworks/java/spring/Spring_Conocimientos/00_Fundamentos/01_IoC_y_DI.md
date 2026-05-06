# IoC y DI: el corazón del desacoplamiento

## La inversión de control (IoC) como principio

En un programa tradicional, tu código controla el flujo: instancia objetos, llama a métodos, decide cuándo finalizar. La inversión de control entrega ese control a un framework. No es un patrón exclusivo de Spring; los servlets, los event listeners o los callbacks ya lo implementan.

En Spring, IoC toma la forma de un contenedor que crea y ensambla tus objetos (beans). Tú escribes clases "inocentes" que declaran sus dependencias, y el contenedor se las suministra en tiempo de ejecución. Esto es el Hollywood Principle: "No nos llames; nosotros te llamaremos".

## Inyección de dependencias (DI) – La implementación concreta

DI es la técnica principal con la que Spring logra IoC. Consiste en que una clase no instancia sus dependencias (no hace `new Servicio()`), sino que las recibe desde el exterior.

Formas de DI en Spring:

### 1. Inyección por constructor (recomendada)

```java
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
```

- **Ventajas:** el objeto siempre está completamente inicializado, permite `final` (inmutabilidad), las dependencias son explícitas y obligatorias. Facilita el testing (no necesitas campo `@Autowired` ni `MockBean`).
- **Inconvenientes:** si hay muchas dependencias, el constructor puede tener demasiados parámetros (síntoma de que la clase necesita un refactor).

### 2. Inyección por setter

```java
@Service
public class PedidoService {
    private PedidoRepository repository;
    
    @Autowired
    public void setRepository(PedidoRepository repository) {
        this.repository = repository;
    }
}
```

- Se usa cuando la dependencia es opcional o se necesita reconfigurar después de la construcción. Menos recomendada porque el objeto puede existir en un estado temporal sin la dependencia.

### 3. Inyección por campo (`@Autowired` en atributo)

```java
@Autowired
private PedidoRepository repository;
```

- Es la más legible pero tiene graves desventajas: oculta las dependencias (no sabes qué necesita la clase sin mirar los campos), dificulta las pruebas unitarias sin Spring (necesitas usar reflexión o `@InjectMocks`), impide `final` y rompe la encapsulación.

## Cómo resuelve Spring las dependencias

El proceso de autowiring sigue estos pasos cuando encuentra `@Autowired`:

1. **Por tipo:** busca un bean que coincida con el tipo declarado (si es una interfaz, busca la implementación única).
2. Si encuentra exactamente uno, lo inyecta.
3. Si encuentra varios candidatos del mismo tipo, busca un calificador:
   - `@Primary`: el bean marcado con `@Primary` tendrá preferencia.
   - `@Qualifier("nombre")`: especifica el bean por su nombre lógico.
4. Si no hay ninguna coincidencia, por defecto lanza una excepción en tiempo de arranque (`NoSuchBeanDefinitionException`), a menos que `required = false` en `@Autowired(required = false)` o que la inyección sea dentro de un `Optional<T>` o `@Nullable`.

```java
@Autowired
@Qualifier("emailService")
private NotificacionService notificacion; // inyecta el bean con nombre "emailService"
```

> [!TIP]
> También se puede usar `@Resource` (JSR-250) que inyecta por nombre por defecto, o `@Inject` (JSR-330) que es funcionalmente equivalente a `@Autowired` sin required.

## Laziness y dependencias circulares

Spring intenta crear los beans en orden para satisfacer las dependencias. Si hay una dependencia circular irresoluble (A → B → A), el contexto no puede levantarse. Sin embargo, se puede romper con `@Lazy` en uno de los puntos de inyección, lo que hace que Spring inyecte un proxy en lugar del bean real, que se resolverá solo en el primer acceso.

```java
@Component
public class A {
    private final B b;
    public A(@Lazy B b) { this.b = b; }
}
```

También existen mecanismos como `ObjectFactory`, `Provider<T>` y `ObjectProvider` para obtener el bean bajo demanda (dependencia de tipo "lookup"):

```java
@Autowired
private ObjectProvider<ServicioCostoso> servicioProvider;
// ...
ServicioCostoso s = servicioProvider.getIfAvailable();
```

## IoC no es solo DI

Spring también ofrece Eventos y Listeners como variante de IoC: un componente publica un evento y no sabe quién lo recibe; los consumidores reaccionan sin acoplamiento directo. Igualmente con la programación orientada a aspectos (AOP): el código transversal se ejecuta sin que la clase invocada lo sepa.

---

[⬅️ Volver al Índice](../../index.md)
