# Spring_Cloud/Config_Server.md
La necesidad de configuración externa centralizada

Los microservicios tienen propiedades (URLs de bases de datos, secretos, parámetros de negocio) que varían por entorno y deben gestionarse sin recompilar. Spring Cloud Config Server centraliza esta configuración en un backend versionado (Git, SVN, Vault) y la sirve a los servicios.
Config Server

Añade spring-cloud-config-server y anota con @EnableConfigServer.
java

@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}

Configuración application.yml:
yaml

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

El servidor clona el repositorio Git y sirve las propiedades bajo /{application}/{profile} (ej. /producto-service/dev). El cliente consulta esta URL al arrancar y fusiona las propiedades.
Config Client

Los microservicios añaden spring-cloud-starter-config y un archivo bootstrap.properties (o application.properties) con la ubicación:
properties

spring.application.name=producto-service
spring.config.import=optional:configserver:http://localhost:8888

En el repositorio Git, un archivo producto-service-dev.yml contendrá las propiedades para ese perfil. El servidor las entrega, y el cliente las integra en su Environment antes de la inicialización de beans.
Refresco de configuración en caliente

Los cambios en Git no se propagan automáticamente a los clientes en ejecución. Spring Cloud ofrece:

    Actuator /refresh: el cliente debe invocar POST /actuator/refresh para recargar propiedades anotadas con @RefreshScope. Solo se actualizan beans marcados con @RefreshScope (normalmente servicios que leen propiedades).

java

@Service
@RefreshScope
public class ConfiguracionServicio {
    @Value("${mi.propiedad}")
    private String propiedad;
}

Al llamar a /refresh, el bean se reinicializa con los nuevos valores sin reiniciar la aplicación.

    Spring Cloud Bus: propaga eventos de refresco a todos los clientes mediante un broker de mensajería (RabbitMQ, Kafka). Con un solo POST /actuator/busrefresh en cualquier cliente, todos los demás reciben la notificación.

Cifrado y secretos

El Config Server puede cifrar valores en reposo usando claves simétricas o asimétricas. Los valores en los archivos de configuración pueden estar prefijados con {cipher}:
yaml

spring:
  datasource:
    password: '{cipher}AQBt...'

El servidor descifra antes de enviar a los clientes. La clave se configura con encrypt.key (simétrica). Para mayor seguridad, se puede integrar Vault como backend.
Estrategias de repositorio y composición

    Repositorio compuesto: múltiples fuentes de configuración (Git + Vault + base de datos).

    Patrones de búsqueda: soporta {application}, {profile}, {label}. Permite configuración global con archivos application*.yml.

    Sobrescritura local: las propiedades locales del cliente (application.yml) pueden anular las remotas según la prioridad.

Config Server en producción

    Se integra con Eureka para alta disponibilidad (los clientes usan el nombre lógico config-server en lugar de la URL fija).

    Autenticación HTTP básica con Spring Security.

    Aplicaciones nativas de Spring Cloud: spring-cloud-config-server + spring-cloud-starter-netflix-eureka-client.

