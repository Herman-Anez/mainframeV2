# Autoconfiguración y Starters

Spring Boot revolucionó el ecosistema Java al resolver la complejidad de la configuración manual. Mientras que Spring tradicional requería extensos archivos XML o clases de configuración Java para beans de infraestructura (DataSource, EntityManagerFactory, etc.), Spring Boot introdujo un enfoque basado en la opinión y la convención.

---

## Conceptos Fundamentales

Spring Boot se apoya en dos pilares para simplificar el desarrollo:

1.  **Starters**: Dependencias agrupadoras que proporcionan todo el classpath necesario y autoconfiguración preconfigurada para una funcionalidad específica.
2.  **Autoconfiguración (`@EnableAutoConfiguration`)**: Un mecanismo inteligente que, basándose en las librerías presentes en el classpath, decide qué beans crear y cómo configurarlos.

### La Anotación `@SpringBootApplication`

Esta anotación es el punto de entrada más común y actúa como un atajo para tres funcionalidades críticas:

```java
@SpringBootConfiguration  // Variante de @Configuration para el contexto Boot
@EnableAutoConfiguration  // Activa el mecanismo de autoconfiguración
@ComponentScan            // Escanea el paquete raíz y subpaquetes
public @interface SpringBootApplication { ... }
```

---

## Funcionamiento Interno de la Autoconfiguración

El proceso de autoconfiguración sigue un flujo lógico riguroso:

1.  **Activación**: `@EnableAutoConfiguration` importa el `AutoConfigurationImportSelector`.
2.  **Descubrimiento**: El selector carga las clases listadas en:
    - `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (Spring Boot 3.x).
    - `spring.factories` (Versiones anteriores).
3.  **Filtrado Condicional**: Cada clase de autoconfiguración utiliza anotaciones condicionales para determinar si debe ejecutarse.
4.  **Ejecución**: Si las condiciones se cumplen, los beans de infraestructura se registran en el contexto.

### Ejemplo: `DataSourceAutoConfiguration`
- **Condición de Clase**: Se activa solo si `DataSource.class` está presente.
- **Condición de Bean**: Se ejecuta solo si el usuario **no** ha definido su propio bean de `DataSource` (`@ConditionalOnMissingBean`).
- **Resultado**: Crea un pool de conexiones (HikariCP por defecto) usando las propiedades `spring.datasource.*`.

---

## Catálogo de Anotaciones Condicionales

| Anotación | Condición de Activación |
| :--- | :--- |
| `@ConditionalOnClass` | Si una clase específica está presente en el classpath. |
| `@ConditionalOnMissingBean` | Si NO existe un bean de ese tipo ya definido. |
| `@ConditionalOnProperty` | Si una propiedad tiene un valor específico en el entorno. |
| `@ConditionalOnWebApplication` | Si la aplicación es de tipo web (Servlet o Reactive). |
| `@ConditionalOnResource` | Si existe un recurso específico (ej. un archivo config). |
| `@ConditionalOnExpression` | Basada en una expresión SpEL compleja. |

---

## Starters: La Navaja Suiza del Classpath

Los starters garantizan la compatibilidad de versiones y reducen la verbosidad del `pom.xml` o `build.gradle`. Siguen el patrón de nombres `spring-boot-starter-*`.

| Starter | Propósito Principal |
| :--- | :--- |
| `spring-boot-starter-web` | Spring MVC, Tomcat, Jackson y Validación. |
| `spring-boot-starter-data-jpa` | Hibernate, Spring Data JPA y pool de conexiones Hikari. |
| `spring-boot-starter-security` | Seguridad, autenticación y autorización. |
| `spring-boot-starter-test` | JUnit 5, Mockito, AssertJ y herramientas de testeo. |
| `spring-boot-starter-actuator` | Endpoints de monitoreo y métricas en producción. |

---

## Creación de Starters Personalizados

Para encapsular lógica reutilizable entre proyectos, se pueden crear starters propios siguiendo estos pasos:

1.  **Módulo de Autoconfiguración**: Contiene las clases `@AutoConfiguration` con sus respectivas condiciones.
2.  **Registro**: Registrar las clases en el archivo de importaciones de Spring Boot.
3.  **Módulo Starter**: Un POM vacío que depende del módulo de autoconfiguración y de las librerías necesarias.

> [!TIP]
> Utiliza `spring-boot-configuration-processor` en tus starters personalizados para generar metadatos que permitan al IDE ofrecer autocompletado en los archivos de propiedades.

### Orden de Ejecución
Las autoconfiguraciones pueden ordenarse para evitar conflictos de dependencia:
- `@AutoConfigureOrder`
- `@AutoConfigureBefore`
- `@AutoConfigureAfter` (Ej. Configurar Hibernate después de DataSource).

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Estructura del Proyecto](./Estructura_Proyecto_Spring_Boot.md) | [Índice](../../README.md) | [Perfiles y Propiedades](./Perfiles_y_Propiedades.md) |

