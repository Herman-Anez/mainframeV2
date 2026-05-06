# Spring_Boot/Perfiles_y_Propiedades.md
Externalización de la configuración

Spring Boot permite casi todas las propiedades de la aplicación (URL de base de datos, puerto, claves API, etc.) fuera del código, en archivos de propiedades, variables de entorno, argumentos de línea de comandos, o servidores de configuración. Esto sigue las reglas de The Twelve-Factor App.
Fuentes de propiedades y orden de prioridad

Spring Boot lee las propiedades desde 17 fuentes diferentes (ordenadas de mayor a menor prioridad):

    Argumentos de línea de comandos (--server.port=9090)

    Propiedades de Java System (System.getProperties())

    Variables de entorno (export SERVER_PORT=9090)

    Archivos application.properties / .yml

        application-{profile}.properties dentro del classpath (o spring.config.additional-location).

    @PropertySource en clases @Configuration
    ... etc. La lista exacta está en la documentación.

La sobreescritura sigue ese orden: un argumento de línea de comandos vence a una variable de entorno, que vence a un archivo de perfil.
Archivos application.properties y application.yml

Spring Boot soporta ambos formatos. YAML es más legible para estructuras jerárquicas, pero ambos son equivalentes.

properties:
properties

server.port=8080
spring.datasource.url=jdbc:mysql://localhost/midb

yml:
yaml

server:
  port: 8080
spring:
  datasource:
    url: jdbc:mysql://localhost/midb

Perfiles (profiles)

Los perfiles permiten tener múltiples conjuntos de configuración para distintos entornos (dev, test, prod). Se activan con spring.profiles.active=dev (en variable de entorno, línea de comandos, o en el application.properties principal). Los archivos específicos de perfil se nombran application-{profile}.properties o .yml. Si un perfil está activo, sus propiedades se superponen a las del archivo base.

Ejemplo:
application.properties define puerto 8080.
application-prod.properties define puerto 80 y datasource de producción.
Al activar prod, el puerto se sobrescribe a 80.

Los documentos multi-perfil en YAML permiten agrupar configuraciones:
yaml

## application.yml
server:
  port: 8080
---
spring:
  config:
    activate:
      on-profile: dev
server:
  port: 9090
---
spring:
  config:
    activate:
      on-profile: prod
server:
  port: 80

@Value y @ConfigurationProperties

    @Value("${clave}"): inyecta un valor simple, con posibilidad de valor por defecto (${clave:defecto}). Útil para una o pocas propiedades. Pero no ofrece chequeo de tipos ni auto-completado en IDE.

    @ConfigurationProperties: mapea un prefijo de propiedades a un bean Java, con binding relajado (camelCase, kebab-case, snake_case). Más seguro y escalable.

java

@ConfigurationProperties(prefix = "app.pedidos")
@Component
public class PedidosProperties {
    private int maxItems = 10;    // valor por defecto
    private Duration timeout;
    private List<String> estadosValidos;
    // getters y setters
}

properties

app.pedidos.max-items=20
app.pedidos.timeout=5s
app.pedidos.estados-validos=CREADO,ENVIADO

Para activar el autocompletado en el IDE, añade la dependencia spring-boot-configuration-processor (optional). Además, se pueden anidar clases POJO para mapear estructuras complejas.
Relajación del binding

@ConfigurationProperties soporta nombres de propiedades en distintos formatos:

    app.pedidos.max-items

    app.pedidos.maxItems

    app.pedidos.max_items

    APP_PEDIDOS_MAXITEMS (variable de entorno)

Todos se mapean a la misma propiedad maxItems.
Placeholders y SpEL en propiedades

Se pueden referenciar otras propiedades o usar expresiones SpEL limitadas en los valores:
properties

app.url-base=http://localhost:${server.port}
app.descripcion=La aplicación ${info.app.name} escuchando en ${app.url-base}

Configuración externa en producción: variables de entorno y Config Server

En entornos como Kubernetes o plataformas de nube, las propiedades se inyectan mediante variables de entorno (p.ej. SPRING_DATASOURCE_URL). Spring Boot convierte automáticamente variables mayúsculas con guiones bajos al formato de propiedad.

Para aplicaciones distribuidas, Spring Cloud Config Server centraliza la configuración y permite actualizarla en caliente (con @RefreshScope). El listado de fuentes se amplía para incluir la configuración remota con prioridad adecuada.
Validación de propiedades

Se puede utilizar Bean Validation en el POJO de @ConfigurationProperties para validar en el arranque. Si se añade @Validated a la clase y @NotNull, @Min, etc. en los campos, si la validación falla la aplicación no arranca, lo cual es deseable para evitar errores tardíos.
java

@Validated
@ConfigurationProperties(prefix = "app.pedidos")
public class PedidosProperties {
    @Min(1)
    private int maxItems;
    ...
}

//////////////////////////////////////////////////////////////
