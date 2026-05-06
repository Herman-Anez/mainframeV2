
# Service Discovery con Eureka

En una arquitectura de microservicios, los servicios se despliegan en múltiples instancias con direcciones IP y puertos dinámicos (contenedores, escalado automático, etc.). La configuración estática de endpoints se vuelve inviable. **Service Discovery** resuelve esto proporcionando un registro central donde los servicios se registran automáticamente y consultan la ubicación de sus dependencias.

## Spring Cloud Netflix Eureka

Eureka es un componente del stack Netflix OSS integrado en Spring Cloud. Consta de dos partes fundamentales:

*   **Eureka Server**: El registro central de servicios.
*   **Eureka Client**: Cada microservicio que se registra y descubre a otros servicios.

## Implementación del Eureka Server

1.  Añade la dependencia `spring-cloud-starter-netflix-eureka-server`.
2.  Anota la aplicación con `@EnableEurekaServer`.

```java
@SpringBootApplication
@EnableEurekaServer
public class EurekaServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServerApplication.class, args);
    }
}
```

3.  Configura el archivo `application.yml`:

```yaml
server:
  port: 8761
eureka:
  client:
    register-with-eureka: false   # no se registra a sí mismo
    fetch-registry: false
```

> [!TIP]
> ¡El servidor ya está listo! Puedes acceder a un dashboard visual en `http://localhost:8761`.

## Eureka Client (Microservicio)

Añade `spring-cloud-starter-netflix-eureka-client` a cada microservicio. Mediante `spring.application.name` se asigna el nombre lógico del servicio.

```yaml
spring:
  application:
    name: producto-service
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka
```

Al iniciar, el cliente se registra automáticamente. Opcionalmente, puedes usar `eureka.instance.prefer-ip-address=true` para registrar la IP en lugar del hostname (recomendado en entornos de contenedores).

## Descubrimiento en el Código: RestTemplate + @LoadBalanced

Spring Cloud integra el descubrimiento con el balanceo de carga del lado del cliente usando **Spring Cloud LoadBalancer**. Para usarlo, exponemos un `RestTemplate` con la anotación `@LoadBalanced`:

```java
@Bean
@LoadBalanced
public RestTemplate restTemplate() {
    return new RestTemplate();
}
```

Ahora, en cualquier petición HTTP, usamos el **nombre lógico** del servicio en lugar de una URL fija:

```java
restTemplate.getForObject("http://producto-service/api/productos", List.class);
```

> [!NOTE]
> La librería intercepta la petición, consulta a Eureka por las instancias disponibles de `producto-service`, elige una (round-robin por defecto) y traduce el nombre lógico a la dirección real `http://IP:puerto`.

## Alternativa Moderna: WebClient Reactivo con Balanceo

```java
@Bean
@LoadBalanced
public WebClient.Builder loadBalancedWebClientBuilder() {
    return WebClient.builder();
}

// Uso:
WebClient client = loadBalancedWebClientBuilder().build();
Mono<List<Producto>> productos = client.get()
    .uri("http://producto-service/api/productos")
    .retrieve()
    .bodyToFlux(Producto.class).collectList();
```

## Salud y Autorrenovación

El cliente de Eureka envía latidos (**heartbeats**) cada 30 segundos por defecto. Si el servidor no los recibe en un periodo determinado, la instancia es eliminada del registro. Esto se puede ajustar:

```yaml
eureka:
  instance:
    lease-renewal-interval-in-seconds: 10
    lease-expiration-duration-in-seconds: 30
```

## Zonas y Alta Disponibilidad

Para tolerancia a fallos del propio servidor Eureka, se despliegan múltiples servidores peer-to-peer que replican el registro. Cada servidor actúa como cliente de los demás.

```yaml
# server1
eureka:
  client:
    service-url:
      defaultZone: http://server2:8762/eureka,http://server3:8763/eureka
```

Los clientes pueden apuntar a todos los servidores en la lista, y Spring Cloud seleccionará uno disponible.

## Eureka vs. Otras Soluciones

*   **Eureka**: Es un sistema **AP** (Disponibilidad y Tolerancia a Particiones) en el teorema CAP, ideal para consistencia eventual y alta disponibilidad del registro.
*   **Consul**: Sistema **CP**, con chequeos de salud más avanzados y almacenamiento KV.
*   **Kubernetes Service Discovery**: En entornos de Kubernetes, se puede prescindir de Eureka y usar el `DiscoveryClient` nativo de Kubernetes.

> [!IMPORTANT]
> **Spring Cloud Commons** abstrae el descubrimiento; cambiar de Eureka a Consul o Kubernetes solo requiere cambiar las dependencias sin modificar el código de negocio.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Config Server](Config_Server.md) | [Índice](../../README.md) | [Pruebas Unitarias](../../README.md) |

