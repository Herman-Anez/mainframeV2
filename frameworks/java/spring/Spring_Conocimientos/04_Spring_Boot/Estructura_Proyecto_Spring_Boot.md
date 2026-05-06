# Spring_Boot/Estructura_Proyecto_Spring_Boot.md
Estructura recomendada de directorios

Spring Boot no fuerza una estructura, pero hay una ampliamente aceptada que sigue el estándar Maven/Gradle:
text

mi-proyecto/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── empresa/
│   │   │           └── miapp/
│   │   │               ├── MiAppApplication.java   (clase principal)
│   │   │               ├── controlador/
│   │   │               ├── servicio/
│   │   │               ├── repositorio/
│   │   │               ├── modelo/
│   │   │               ├── dto/
│   │   │               ├── configuracion/
│   │   │               └── excepcion/
│   │   └── resources/
│   │       ├── static/                 (contenido estático: css, js, imágenes)
│   │       ├── templates/              (plantillas Thymeleaf, Freemarker)
│   │       ├── application.properties  (o application.yml)
│   │       └── data.sql / schema.sql   (opcional, para inicializar BD)
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

    static/: servido directamente por Spring Boot (recursos estáticos). Ruta raíz /.

    templates/: plantillas del motor de vistas (Thymeleaf, etc.). No accesibles directamente.

    application.properties o .yml: configuración por defecto. Se puede dividir por perfiles.

    data.sql y schema.sql: si existen, Spring Boot los ejecuta al iniciar la base de datos embebida, a menos que se desactive.

La clase principal y SpringApplication
java

@SpringBootApplication
public class MiAppApplication {
    public static void main(String[] args) {
        SpringApplication.run(MiAppApplication.class, args);
    }
}

SpringApplication.run() arranca el contexto de Spring, el servidor embebido (si es web) y todo lo demás. Se puede personalizar mediante SpringApplication builder:
java

new SpringApplicationBuilder(MiAppApplication.class)
    .bannerMode(Banner.Mode.OFF)
    .profiles("dev")
    .run(args);

Empaquetado y ejecución

Spring Boot ofrece el plugin spring-boot-maven-plugin que genera un fat jar (JAR autocontenido con todas las dependencias, el servidor embebido y un cargador de clases especial). Se ejecuta con:
bash

mvn clean package
java -jar target/mi-app.jar

El plugin también permite ejecutar directamente con mvn spring-boot:run para desarrollo ágil.
Convenciones en el package scanning

El @ComponentScan implícito en @SpringBootApplication escanea el paquete donde reside la clase principal y todos sus subpaquetes. Por eso se recomienda ubicar la aplicación en el paquete raíz (com.empresa.miapp). Si necesitas escanear otros paquetes, puedes usar scanBasePackages en la anotación.
Recursos estáticos y caché

Por defecto, Spring Boot sirve recursos estáticos desde classpath:/static/, classpath:/public/, classpath:/resources/, classpath:/META-INF/resources/. Puedes personalizar con spring.web.resources.static-locations. El mapeo de URL raíz es /. Para control de caché: spring.web.resources.cache.cachecontrol.max-age.
El servidor embebido

Spring Boot incluye Tomcat por defecto en spring-boot-starter-web. Pero puedes cambiarlo a Jetty o Undertow excluyendo Tomcat y añadiendo el starter correspondiente. La configuración del servidor se realiza mediante propiedades server.* (puerto, SSL, compression, etc.). El servidor se inicia desde ServletWebServerApplicationContext.
