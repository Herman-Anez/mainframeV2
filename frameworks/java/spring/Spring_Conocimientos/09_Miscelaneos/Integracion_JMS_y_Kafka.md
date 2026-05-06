
# Mensajería Asíncrona: JMS y Apache Kafka

Spring ofrece abstracciones para los dos estándares de mensajería más extendidos: **JMS (Java Message Service)** para brokers tradicionales como ActiveMQ o Artemis, y **Apache Kafka** para streaming de eventos de alto rendimiento.

Aunque los detalles difieren, el patrón es similar: un **Template** para enviar mensajes y un **Listener** anotado para recibirlos.

---

## Integración JMS

### Configuración con Spring Boot

Starter: `spring-boot-starter-artemis` (o `-activemq`). Boot autoconfigura una `ConnectionFactory` y un `JmsTemplate` a partir de las propiedades:

```properties
spring.artemis.mode=native
spring.artemis.broker-url=tcp://localhost:61616
spring.artemis.user=admin
spring.artemis.password=admin
```

O con **ActiveMQ**:

```properties
spring.activemq.broker-url=tcp://localhost:61616
spring.activemq.user=admin
spring.activemq.password=admin
```

### Envío de mensajes con JmsTemplate

```java
@Autowired
private JmsTemplate jmsTemplate;

public void enviarPedido(Pedido pedido) {
    jmsTemplate.convertAndSend("cola.pedidos", pedido);
}
```

> [!NOTE]
> `convertAndSend` utiliza un `MessageConverter` (por defecto `MappingJackson2MessageConverter` si Jackson está presente) para serializar a JSON.

> [!TIP]
> Si necesitas control fino (headers, propiedades JMS), puedes crear un `Message` con `JmsTemplate.send()`.

### Recepción con @JmsListener

```java
@Component
public class PedidoListener {

    @JmsListener(destination = "cola.pedidos")
    public void recibirPedido(Pedido pedido) {
        // procesar pedido
    }
}
```

> [!IMPORTANT]
> Para lecturas transaccionales, añade `@Transactional` al método (si hay un `JmsTransactionManager` o `JtaTransactionManager`).

También se puede configurar `concurrency` para paralelismo:

```java
@JmsListener(destination = "cola.pedidos", concurrency = "3-10")
```

### Configuración avanzada de JMS

*   **Destinos dinámicos:** usar `dynamicQueues/...` en Artemis.
*   **Mensajes de texto plano:** cambiar `MessageConverter` por `SimpleMessageConverter`.
*   **Dead Letter Queue:** configurar en el broker.
*   **Pub/Sub con tópicos:** `jmsTemplate.setPubSubDomain(true)` y destino `tema.nombre`.

---

## Integración Apache Kafka

### Dependencias y configuración

Starter: `spring-kafka`. Spring Boot autoconfigura `KafkaTemplate` y *consumer factories*.

Propiedades base:

```properties
spring.kafka.bootstrap-servers=localhost:9092
spring.kafka.consumer.group-id=pedidos-group
spring.kafka.consumer.key-deserializer=org.apache.kafka.common.serialization.StringDeserializer
spring.kafka.consumer.value-deserializer=org.springframework.kafka.support.serializer.JsonDeserializer
spring.kafka.producer.key-serializer=org.apache.kafka.common.serialization.StringSerializer
spring.kafka.producer.value-serializer=org.springframework.kafka.support.serializer.JsonSerializer
```

### Productor con KafkaTemplate

```java
@Autowired
private KafkaTemplate<String, Pedido> kafkaTemplate;

public void enviarPedido(Pedido pedido) {
    kafkaTemplate.send("topic-pedidos", pedido.getId().toString(), pedido)
        .addCallback(
            result -> log.info("Enviado: {}", result.getProducerRecord().value()),
            ex -> log.error("Error", ex)
        );
}
```

> [!NOTE]
> Se envía con una clave para particionamiento. El serializador JSON maneja el objeto.

### Consumidor con @KafkaListener

```java
@Component
public class PedidoConsumer {

    @KafkaListener(topics = "topic-pedidos", groupId = "pedidos-group")
    public void escuchar(Pedido pedido) {
        // procesar pedido
    }
}
```

> [!IMPORTANT]
> Spring gestiona el *offset commit* automáticamente (por defecto `enable.auto.commit=true`, se confirma tras el procesamiento). Para control manual, usar `Acknowledgment` en el parámetro y `spring.kafka.consumer.enable-auto-commit=false`.

### Manejo de errores y reintentos

Se puede configurar un `ErrorHandler` o `SeekToCurrentErrorHandler` para reintentos locales:

```java
@Bean
public ConcurrentKafkaListenerContainerFactory<String, Pedido> kafkaListenerContainerFactory() {
    ConcurrentKafkaListenerContainerFactory<String, Pedido> factory =
            new ConcurrentKafkaListenerContainerFactory<>();
    factory.setCommonErrorHandler(new DefaultErrorHandler(
            new FixedBackOff(1000L, 3))); // 3 reintentos, 1 seg entre ellos
    return factory;
}
```

> [!TIP]
> Para *dead-letter topics*, con `DeadLetterPublishingRecoverer` se envían los mensajes fallidos a un topic de error.

### Procesamiento batch

Se pueden consumir lotes configurando `factory.setBatchListener(true)` y el método del listener con `List<Pedido>`.

---

## Kafka Streams con Spring

Spring también soporta escribir aplicaciones de streaming mediante **Kafka Streams**. Configurando un `StreamsBuilder` bean se definen topologías.

> [!NOTE]
> Este tema suele formar parte de un módulo más avanzado como **Spring Cloud Stream** con Kafka Streams.

---

## Spring Cloud Stream (Abstracción de alto nivel)

Para quienes prefieren una capa aún más alta, **Spring Cloud Stream** abstrae JMS, Kafka, RabbitMQ y otros bajo un modelo de canales (`Source`, `Sink`, `Processor`). No se cubre aquí en profundidad, pero es importante mencionarlo.

---

## ¿Cuándo elegir JMS vs Kafka?

*   **JMS:** Transacciones distribuidas tradicionales con garantías "exactly-once" mediante protocolo XA, integración con servidores de aplicaciones, colas y tópicos clásicos. Adecuado para integraciones empresariales clásicas y entornos donde ya existe un broker JMS.
*   **Kafka:** Altísimo rendimiento, persistencia inmutable, retroconsumo (reprocesar eventos), particionamiento, escalado horizontal nativo. Ideal para microservicios con CQRS, event sourcing y datos en tiempo real.

Spring unifica la experiencia de desarrollo con anotaciones y templates similares, lo que facilita migrar o convivir con ambos.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Manejo de Errores y Excepciones](../03_Spring_MVC/Manejo_de_Excepciones.md) | [Índice](../../README.md) | [Internacionalización i18n](./Internacionalizacion_i18n.md) |

