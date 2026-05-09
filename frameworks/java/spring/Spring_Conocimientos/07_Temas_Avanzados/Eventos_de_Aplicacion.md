
# El Sistema de Eventos de Spring

Spring proporciona un mecanismo de publicación/suscripción de eventos dentro del `ApplicationContext`. Permite que un componente publique un evento y que otros componentes reaccionen sin acoplamiento directo, una implementación más del principio de Inversión de Control.

## Piezas Clave

*   **ApplicationEvent**: Clase base para definir eventos. Desde Spring 4.2 ya no es obligatorio extenderla; cualquier objeto puede ser un evento.
*   **ApplicationEventPublisher**: Interfaz que posee el `ApplicationContext` (y cualquier bean que la implemente) para publicar eventos.
*   **Listener / @EventListener**: Método que recibe el evento y reacciona. Puede anotarse directamente en un bean.

## Publicación de Eventos

Inyectamos el publicador:

```java
@Component
public class PedidoService {
    private final ApplicationEventPublisher publisher;
    // ...

    public void procesarPedido(Pedido pedido) {
        // lógica de negocio
        publisher.publishEvent(new PedidoCreadoEvent(this, pedido));
    }
}
```

`PedidoCreadoEvent` es una clase simple que hereda de `ApplicationEvent` o, más moderno, simplemente un POJO (sin extender nada) y se puede publicar así desde Spring 4.2+:

```java
public class PedidoCreadoEvent {
    private final Pedido pedido;
    public PedidoCreadoEvent(Pedido pedido) { this.pedido = pedido; }
    public Pedido getPedido() { return pedido; }
}
```

Y la publicación sería `publisher.publishEvent(new PedidoCreadoEvent(pedido))`.

## Recepción de Eventos con @EventListener

Cualquier bean puede contener un método anotado con `@EventListener`. Spring lo registra automáticamente.

```java
@Component
public class NotificacionListener {

    @EventListener
    public void manejarPedidoCreado(PedidoCreadoEvent event) {
        // enviar email de confirmación
        notificar(event.getPedido());
    }
}
```

> [!TIP]
> Se pueden escuchar múltiples tipos de eventos con distintos métodos, o un mismo método puede escuchar varios usando la condición `classes` o genéricos.

## Eventos Transaccionales

Con `@TransactionalEventListener`, la escucha se vincula a las fases de una transacción:

| Fase | Descripción |
| :--- | :--- |
| `AFTER_COMMIT` (defecto) | Se ejecuta si la transacción se completa exitosamente. |
| `AFTER_ROLLBACK` | Se ejecuta si la transacción falla. |
| `AFTER_COMPLETION` | Después de commit o rollback. |
| `BEFORE_COMMIT` | Antes de que la transacción se confirme. |

```java
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void manejarPedidoCreadoCommit(PedidoCreadoEvent event) {
    // solo se ejecuta si la transacción fue exitosa
}
```

> [!IMPORTANT]
> `@TransactionalEventListener` solo funciona si el evento se publicó dentro de una transacción activa y el listener está en el mismo `ApplicationContext` (o contexto con propagación de transacciones). Es una herramienta poderosa para evitar efectos secundarios si la transacción falla (ej. no enviar email si el pedido no se persistió).

## Eventos Asíncronos

Para no bloquear al publicador, se puede ejecutar el listener de forma asíncrona. Basta con añadir `@Async` al método listener y habilitar el soporte asíncrono con `@EnableAsync`.

```java
@Component
@EnableAsync
public class AsyncNotificacionListener {

    @Async
    @EventListener
    public void manejarPedidoCreadoAsync(PedidoCreadoEvent event) {
        // este código se ejecuta en un pool de hilos separado
    }
}
```

### Precauciones con Eventos Asíncronos

> [!WARNING]
> *   La transacción del publicador no se propaga al hilo asíncrono.
> *   Los eventos asíncronos pueden perderse si la aplicación se cae antes de que se procesen; para garantías de entrega se necesita un message broker.
> *   No combinar `@Async` con `@TransactionalEventListener` en el mismo listener.

## Programación Reactiva con Eventos

También se pueden publicar eventos y escucharlos usando `@EventListener` en entornos reactivos, pero el sistema de eventos estándar es bloqueante. Para aplicaciones WebFlux, se recomienda usar `ApplicationEventMulticaster` configurable o la integración con Project Reactor mediante `Sinks.Many`.

## Orden y Herencia

Se puede controlar el orden de ejecución de varios listeners con `@Order`. Además, un listener para una superclase también recibe eventos de las subclases, gracias a la resolución de tipos.

## Eventos de Contexto (Built-in)

Spring dispara varios eventos del ciclo de vida del contexto: `ContextRefreshedEvent`, `ContextStartedEvent`, `ContextStoppedEvent`, `ContextClosedEvent`, `RequestHandledEvent`. Podemos escucharlos para inicializar recursos o cerrar de forma limpia al apagar.

```java
@Component
public class StartupListener {
    @EventListener(ContextRefreshedEvent.class)
    public void onRefresh() {
        // Cache warmup, etc.
    }
}
```

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Gestión de Caché](./Cache.md) | [Índice](../../index.md) | [Programación Reactiva (WebFlux)](./Programacion_Reactiva_WebFlux.md) |

