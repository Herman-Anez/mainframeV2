# Gestión de Perfiles y Propiedades

Spring Boot facilita la externalización de la configuración, permitiendo que la misma aplicación funcione en diferentes entornos (desarrollo, pruebas, producción) sin necesidad de recompilar el código. Este enfoque sigue los principios de **The Twelve-Factor App**.

---

## Fuentes de Propiedades y Prioridad

Spring Boot puede leer propiedades de múltiples fuentes. Existe una jerarquía de prioridad estricta; si una propiedad se define en varias fuentes, la de mayor prioridad prevalece.

### Orden de Prioridad (Simplificado)
1.  **Argumentos de línea de comandos** (Ej: `--server.port=9090`).
2.  **Propiedades de sistema de Java** (`System.getProperties()`).
3.  **Variables de entorno del SO** (Ej: `export SERVER_PORT=9090`).
4.  **Archivos de configuración específicos de perfil** (`application-{profile}.properties`).
5.  **Archivo de configuración principal** (`application.properties` o `.yml`).

> [!IMPORTANT]
> Las variables de entorno son ideales para entornos de contenedores (Docker/Kubernetes), mientras que los argumentos de línea de comandos son útiles para pruebas rápidas.

---

## Formatos de Configuración: Properties vs YAML

Spring Boot soporta tanto el formato tradicional de propiedades como YAML. YAML es generalmente preferido por su legibilidad y estructura jerárquica.

### Comparativa de Sintaxis

```properties
# application.properties
server.port=8080
spring.datasource.url=jdbc:mysql://localhost/midb
```

```yaml
# application.yml
server:
  port: 8080
spring:
  datasource:
    url: jdbc:mysql://localhost/midb
```

---

## Perfiles (Profiles)

Los perfiles permiten segregar partes de la configuración de la aplicación y hacer que solo estén disponibles en ciertos entornos.

### Activación de Perfiles
Se activan mediante la propiedad `spring.profiles.active`. 
- Ejemplo: `java -jar app.jar --spring.profiles.active=prod`

### Archivos Específicos
- `application-dev.yml`: Configuración para desarrollo local (H2, logging debug).
- `application-prod.yml`: Configuración para producción (MySQL, seguridad estricta).

> [!TIP]
> En YAML, puedes usar documentos multi-perfil separados por `---` para mantener toda la configuración en un solo archivo, aunque para proyectos grandes se recomienda separar por archivos.

---

## Inyección de Propiedades en Java

Existen dos formas principales de acceder a las propiedades configuradas desde el código Java:

### 1. `@Value`
Ideal para inyectar valores simples o individuales. Permite definir valores por defecto.

```java
@Value("${app.timeout:5000}")
private int timeout;
```

### 2. `@ConfigurationProperties`
Mapea un prefijo de propiedades a un objeto POJO. Es la opción recomendada para configuraciones complejas o agrupadas por funcionalidad.

```java
@ConfigurationProperties(prefix = "app.pedidos")
@Component
@Validated
public class PedidosProperties {
    @Min(1)
    private int maxItems = 10;
    private Duration timeout;
    private List<String> estadosValidos;
    // Getters y Setters
}
```

> [!NOTE]
> `@ConfigurationProperties` soporta **binding relajado**, lo que significa que `max-items`, `maxItems` y `MAX_ITEMS` se mapearán correctamente al campo `maxItems`.

---

## Funcionalidades Avanzadas

### Placeholders y SpEL
Puedes referenciar propiedades dentro de otras propiedades:
```properties
app.url-base=http://localhost:${server.port}
app.descripcion=Servicio escuchando en ${app.url-base}
```

### Validación de Configuración
Al añadir `@Validated` y anotaciones de Bean Validation (`@NotNull`, `@Min`, etc.) a una clase `@ConfigurationProperties`, Spring Boot validará los valores al arrancar. Si no son válidos, la aplicación fallará inmediatamente, evitando errores en tiempo de ejecución.

### Centralización con Config Server
Para arquitecturas de microservicios, se utiliza **Spring Cloud Config Server** para centralizar la configuración en un repositorio Git o base de datos, permitiendo actualizaciones dinámicas sin reiniciar los servicios mediante `@RefreshScope`.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Autoconfiguración y Starters](./Autoconfiguracion_y_Starters.md) | [Índice](../../index.md) | [Actuator y Métricas](./Actuator_y_Metricas.md) |

