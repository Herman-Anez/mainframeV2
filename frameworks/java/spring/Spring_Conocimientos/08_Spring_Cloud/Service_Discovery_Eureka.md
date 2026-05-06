
# Spring_Cloud/Service_Discovery_Eureka.md

 El problema del descubrimiento de servicios

En una arquitectura de microservicios, los servicios se despliegan en múltiples instancias, con direcciones IP y puertos dinámicos (contenedores, escalado automático). La configuración estática de endpoints se vuelve inviable. **Service Discovery** resuelve esto proporcionando un registro central donde los servicios se registran y consultan la ubicación de sus dependencias.

 Spring Cloud Netflix Eureka

Eureka es un componente del stack Netflix OSS integrado en Spring Cloud. Consta de:

- **Eureka Server**: el registro central.
- **Eureka Client**: cada microservicio que se registra y descubre otros.

 Implementación del Eureka Server

1. Añade `spring-cloud-starter-netflix-eureka-server`.
2. Anota la aplicación con `@EnableEurekaServer`.

```java
@SpringBootApplication
@EnableEurekaServer
public class EurekaServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServerApplication.class, args);
    }
}

    Configura application.yml:
```
yaml

server:
  port: 8761
eureka:
  client:
    register-with-eureka: false   # no se registra a sí mismo
    fetch-registry: false

¡El servidor ya está listo! Se accede a un dashboard en http://localhost:8761.
Eureka Client (microservicio)

Añade spring-cloud-starter-netflix-eureka-client a cada microservicio. Con spring.application.name se asigna el nombre lógico del servicio.
yaml

spring:
  application:
    name: producto-service
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka

Al iniciar, el cliente se registra. Opcional: eureka.instance.prefer-ip-address=true para registrar la IP en lugar del hostname (mejor en contenedores).
Descubrimiento en el código: RestTemplate + @LoadBalanced

Spring Cloud integra el descubrimiento con balanceo de carga del lado cliente usando Spring Cloud LoadBalancer (sucesor de Ribbon). Exponemos un RestTemplate con @LoadBalanced:
java

@Bean
@LoadBalanced
public RestTemplate restTemplate() {
    return new RestTemplate();
}

Ahora, en cualquier petición HTTP, usamos el nombre lógico del servicio:
java

restTemplate.getForObject("http://producto-service/api/productos", List.class);

La librería intercepta la petición, consulta a Eureka por las instancias de producto-service, elige una (round-robin por defecto) y traduce el nombre lógico a http://IP:puerto.
Alternativa moderna: WebClient reactivo con balanceo
java

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

Salud y autorenovación

El Eureka client envía latidos (heartbeats) cada 30 segundos por defecto. Si el server no los recibe, la instancia se saca del registro. Se puede afinar con:
yaml

eureka:
  instance:
    lease-renewal-interval-in-seconds: 10
    lease-expiration-duration-in-seconds: 30

Zonas y alta disponibilidad

Para tolerancia a fallos del servidor Eureka, se despliegan múltiples servidores peer-to-peer que replican el registro. Cada servidor es cliente de los demás.
yaml

# server1
eureka:
  client:
    service-url:
      defaultZone: http://server2:8762/eureka,http://server3:8763/eureka

Los clientes pueden apuntar a todos los servidores en la lista, y Spring Cloud selecciona uno disponible.
Eureka vs. otras soluciones

    Eureka: AP (disponibilidad y tolerancia a particiones) en el teorema CAP, ideal para consistencia eventual y alta disponibilidad del registro.

    Consul: CP, con chequeos de salud más ricos y KV store.

    Kubernetes Service Discovery: en Kubernetes, se puede prescindir de Eureka y usar DiscoveryClient para Kubernetes.

Spring Cloud Commons abstrae el descubrimiento; cambiar de Eureka a Consul o Kubernetes solo requiere cambiar dependencias sin tocar el código de negocio.
