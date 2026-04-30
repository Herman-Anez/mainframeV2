# Maven y Gradle: Gestión Avanzada de Proyectos

## 1. El Papel de las Herramientas de Construcción

Antes de Maven/Gradle se usaba Ant (scripts XML) o simplemente `javac`. Hoy es impensable un proyecto sin gestión automática de dependencias, ciclo de vida estandarizado y plugins.

## 2. Maven

Maven se basa en la **convención sobre configuración**. Utiliza un archivo `pom.xml` que describe el proyecto, sus dependencias y los plugins que ejecutan tareas.

### 2.1. Estructura de un Proyecto Maven

```text
miapp/
├── pom.xml
└── src/
    ├── main/java/         # Código fuente
    ├── main/resources/    # Recursos (application.properties, etc.)
    ├── test/java/         # Pruebas
    └── test/resources/
```

### 2.2. pom.xml mínimo para Java 21

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.empresa</groupId>
    <artifactId>miapp</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.10.1</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <release>21</release>
                    <!-- Para características preview: <compilerArgs>--enable-preview</compilerArgs> -->
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### 2.3. Ciclo de Vida de Maven

Fases principales:
*   `validate`, `compile`, `test`, `package`, `verify`, `install`, `deploy`.
*   Ejecutar `mvn package` compila, ejecuta tests y empaqueta un JAR.

### 2.4. Plugins Importantes

*   **maven-compiler-plugin**: Configura la versión de Java.
*   **maven-surefire-plugin**: Ejecución de tests unitarios.
*   **maven-failsafe-plugin**: Tests de integración.
*   **maven-jar-plugin**: Empaquetado base.
*   **maven-shade-plugin / maven-assembly-plugin**: Crear *fat JAR* con dependencias.
*   **maven-jlink-plugin**: Construir imágenes JRE personalizadas.
*   **maven-jpackage-plugin**: Invocar `jpackage`.

### 2.5. Gestión de Dependencias

Las dependencias se declaran con `groupId`, `artifactId`, `version` y `scope` (`compile`, `test`, `provided`, `runtime`). Maven resuelve las dependencias transitivas y las almacena en el repositorio local (`~/.m2`).

Para evitar conflictos se puede usar `<dependencyManagement>` y la sección `<exclusions>`.

---

## 3. Gradle

Gradle usa un DSL basado en Groovy o Kotlin. Es más flexible y se adapta mejor a proyectos grandes o multimódulo.

### 3.1. Estructura Típica

```text
miapp/
├── build.gradle (o build.gradle.kts)
├── settings.gradle
└── src/
    ├── main/java/
    ├── main/resources/
    ├── test/java/
    └── test/resources/
```

### 3.2. build.gradle.kts mínimo (Kotlin DSL) para Java 21

```kotlin
plugins {
    application
}

group = "com.empresa"
version = "1.0.0"

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
    // Para preview: options.compilerArgs.add("--enable-preview")
}

application {
    mainClass.set("com.empresa.Main")
}

repositories {
    mavenCentral()
}

dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.1")
}

tasks.test {
    useJUnitPlatform()
}
```

### 3.3. Ciclo de Vida y Tareas

*   `gradle build`: Compila, ejecuta tests y empaqueta.
*   `gradle run`: Ejecuta la aplicación.
*   Las tareas pueden encadenarse y crearse automáticamente por los plugins.

### 3.4. Plugins Principales

*   **java**, **application**
*   **org.gradlex.java.enable-preview**: Para preview fácil.
*   **org.beryx.jlink**: Para `jlink`.
*   **com.github.johnrengelman.shadow**: *fat JAR*.
*   **org.panteleyev.jpackage** o **com.github.ben-manes.gradle-versions-plugin**.

### 3.5. Gestión de Dependencias

*   **implementation**: Dependencia necesaria en compilación y ejecución, no expuesta a consumidores del módulo.
*   **api**: Expuesta a consumidores.
*   **testImplementation**, **testRuntimeOnly**, etc.

> [!TIP]
> Se pueden usar BOMs (*Bill of Materials*) para alinear versiones, por ejemplo Spring Boot, Jackson, etc.

---

## 4. Comparativa Rápida: Maven vs Gradle

| Característica | Maven | Gradle |
| :--- | :--- | :--- |
| **Lenguaje** | XML | Groovy / Kotlin DSL |
| **Extensibilidad** | Plugins XML | Scripts / Plugins programáticos |
| **Rendimiento** | Más lento en builds grandes | Mayor velocidad, incremental y build cache |
| **Convención** | Muy estricta y homogénea | Flexible, adaptable |
| **Curva aprendizaje** | Menor | Moderada |

---

> [!NOTE]
> Ambos son perfectamente capaces y se integran con IDEs y CI/CD. Gradle suele preferirse en nuevos desarrollos de Android, grandes multimódulos o cuando se necesita mucha personalización; Maven sigue siendo el estándar en muchos entornos enterprise.

---

| Anterior | Inicio | Siguiente |
| :---: | :---: | :---: |
| [JVM Rendimiento](../10-JVM-Rendimiento/03-tuning-avanzado.md) | [Índice](../../README.md) | [Pruebas JUnit 5](02-pruebas-junit5.md) |

