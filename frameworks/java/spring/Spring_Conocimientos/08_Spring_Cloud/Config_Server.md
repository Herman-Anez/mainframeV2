# Spring Cloud Config Server

En una arquitectura de microservicios, las propiedades (URLs de bases de datos, secretos, parámetros de negocio, etc.) varían según el entorno y deben gestionarse sin necesidad de recompilar el código. **Spring Cloud Config Server** centraliza esta configuración en un backend versionado (Git, SVN, Vault) y la sirve a los servicios de forma dinámica.

## Config Server

Para implementar el servidor, se añade la dependencia `spring-cloud-config-server` y se anota la clase principal con `@EnableConfigServer`.

```java
@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}
```

### Configuración en application.yml

```yaml
server:
  port: 8888
spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/mi-organizacion/config-repo
          default-label: main
          clone-on-start: true
```

> [!NOTE]
> El servidor clona el repositorio Git y sirve las propiedades bajo la ruta `/{application}/{profile}` (ej. `/producto-service/dev`). El cliente consulta esta URL al arrancar y fusiona las propiedades obtenidas.

## Config Client

Los microservicios (clientes) deben añadir la dependencia `spring-cloud-starter-config` y configurar la importación en su `application.properties` o `bootstrap.properties`:

```properties
spring.application.name=producto-service
spring.config.import=optional:configserver:http://localhost:8888
```

En el repositorio Git, un archivo llamado `producto-service-dev.yml` contendrá las propiedades específicas para ese perfil. El servidor las entrega y el cliente las integra en su `Environment` antes de inicializar los beans.

## Refresco de Configuración en Caliente

Los cambios en el repositorio Git no se propagan automáticamente a los clientes que ya están en ejecución. Spring Cloud ofrece dos mecanismos:

### 1. Actuator /refresh

El cliente debe invocar un endpoint `POST /actuator/refresh` para recargar las propiedades. Solo se actualizan los beans marcados con la anotación `@RefreshScope`.

```java
@Service
@RefreshScope
public class ConfiguracionServicio {
    @Value("${mi.propiedad}")
    private String propiedad;
}
```

Al llamar a `/refresh`, el bean se reinicializa con los nuevos valores sin necesidad de reiniciar la aplicación completa.

### 2. Spring Cloud Bus

Propaga eventos de refresco a todos los clientes mediante un broker de mensajería (RabbitMQ, Kafka). Con un solo `POST /actuator/busrefresh` en cualquier cliente, todos los demás reciben la notificación y se actualizan automáticamente.

## Cifrado y Secretos

El Config Server permite cifrar valores sensibles en reposo. Los valores en los archivos de configuración pueden estar prefijados con `{cipher}`:

```yaml
spring:
  datasource:
    password: '{cipher}AQBt...'
```

El servidor descifra estos valores antes de enviarlos a los clientes. La clave se configura mediante `encrypt.key`. Para entornos de alta seguridad, se recomienda integrar **HashiCorp Vault**.

## Estrategias de Repositorio y Composición

*   **Repositorio Compuesto**: Permite usar múltiples fuentes de configuración simultáneamente (Git + Vault + Base de Datos).
*   **Patrones de Búsqueda**: Soporta marcadores de posición como `{application}`, `{profile}` y `{label}`. Permite configuración global mediante archivos `application*.yml`.
*   **Sobrescritura Local**: Las propiedades definidas localmente en el cliente pueden tener prioridad sobre las remotas según se configure.

## Config Server en Producción

*   **Alta Disponibilidad**: Se integra con Eureka para que los clientes localicen el `config-server` por su nombre lógico.
*   **Seguridad**: Se debe proteger con autenticación (ej. HTTP Basic con Spring Security).
*   **Nativo**: Es compatible con perfiles de ejecución nativos para despliegues optimizados.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Circuit Breaker](Circuit_Breaker.md) | [Índice](../../README.md) | [Service Discovery](Service_Discovery_Eureka.md) |


