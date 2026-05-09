# Estructura de un Proyecto Spring Boot

Spring Boot no fuerza una estructura rígida de directorios, pero existe una convención ampliamente aceptada que sigue el estándar de Maven o Gradle. Seguir estas convenciones facilita la mantenibilidad y permite que Spring Boot realice la configuración automática de manera eficiente.

---

## Estructura Recomendada de Directorios

La siguiente estructura es la base de la mayoría de los proyectos Spring Boot profesionales:

```text
mi-proyecto/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── empresa/
│   │   │           └── miapp/
│   │   │               ├── MiAppApplication.java   (Clase principal)
│   │   │               ├── controlador/
│   │   │               ├── servicio/
│   │   │               ├── repositorio/
│   │   │               ├── modelo/
│   │   │               ├── dto/
│   │   │               ├── configuracion/
│   │   │               └── excepcion/
│   │   └── resources/
│   │       ├── static/                 (Contenido estático: CSS, JS, imágenes)
│   │       ├── templates/              (Plantillas Thymeleaf, Freemarker)
│   │       ├── application.properties  (Configuración centralizada)
│   │       └── data.sql / schema.sql   (Scripts de inicialización de BD)
│   └── test/
│       ├── java/
│       │   └── com/empresa/miapp/
│       │       ├── integracion/
│       │       ├── unidad/
│       │       └── MiAppApplicationTests.java
│       └── resources/
│           └── application-test.properties
├── pom.xml (o build.gradle)
└── README.md
```

### Descripción de Directorios Clave

- **`static/`**: Servido directamente por Spring Boot. Ideal para recursos front-end que no requieren procesamiento. La ruta raíz es `/`.
- **`templates/`**: Contiene las plantillas del motor de vistas. No son accesibles directamente desde el navegador, lo que mejora la seguridad.
- **`application.properties` / `.yml`**: Archivo de configuración por defecto. Permite definir comportamientos de la aplicación y puede segmentarse por perfiles.
- **`data.sql` y `schema.sql`**: Scripts que Spring Boot ejecuta automáticamente al iniciar si detecta una base de datos embebida (comportamiento personalizable).

---

## La Clase Principal y SpringApplication

La clase principal actúa como el punto de entrada de la aplicación. Está anotada con `@SpringBootApplication`, que combina `@Configuration`, `@EnableAutoConfiguration` y `@ComponentScan`.

```java
@SpringBootApplication
public class MiAppApplication {
    public static void main(String[] args) {
        SpringApplication.run(MiAppApplication.class, args);
    }
}
```

> [!NOTE]
> `SpringApplication.run()` no solo arranca el contexto de Spring, sino que también inicializa el servidor embebido (Tomcat por defecto) y procesa los argumentos de línea de comandos.

### Personalización del Arranque

Si necesitas un control más fino sobre el inicio, puedes usar el `SpringApplicationBuilder`:

```java
new SpringApplicationBuilder(MiAppApplication.class)
    .bannerMode(Banner.Mode.OFF)
    .profiles("dev")
    .run(args);
```

---

## Empaquetado y Ejecución

Spring Boot utiliza el plugin `spring-boot-maven-plugin` (o su equivalente en Gradle) para generar un **fat jar**: un archivo JAR único que contiene todas las dependencias y el servidor embebido.

### Comandos Comunes
- **Compilar y empaquetar**:
  ```bash
  mvn clean package
  ```
- **Ejecutar el artefacto**:
  ```bash
  java -jar target/mi-app.jar
  ```
- **Ejecución en desarrollo**:
  ```bash
  mvn spring-boot:run
  ```

---

## Convenciones y Configuración del Servidor

### Package Scanning
El `@ComponentScan` implícito escanea el paquete de la clase principal y sus subpaquetes. 

> [!IMPORTANT]
> Se recomienda ubicar la aplicación en un paquete raíz (ej. `com.empresa.miapp`) para asegurar que todos los componentes sean detectados sin configuración adicional.

### Recursos Estáticos y Caché
Por defecto, Spring Boot busca en `/static`, `/public`, `/resources` y `/META-INF/resources`. Puedes personalizar estas rutas y el control de caché mediante:
- `spring.web.resources.static-locations`
- `spring.web.resources.cache.cachecontrol.max-age`

### El Servidor Embebido
Aunque Tomcat es el predeterminado, puedes cambiarlo a **Jetty** o **Undertow** excluyendo la dependencia de Tomcat en el starter web. La configuración del servidor se centraliza en las propiedades `server.*` (puerto, SSL, compresión).

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Vistas y Templates](../03_Spring_MVC/Vistas_y_Templates.md) | [Índice](../../index.md) | [Autoconfiguración y Starters](./Autoconfiguracion_y_Starters.md) |

