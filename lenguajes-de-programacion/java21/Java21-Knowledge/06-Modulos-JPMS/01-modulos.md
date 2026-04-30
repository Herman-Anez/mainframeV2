# MÓDULOS JPMS (Java Platform Module System)

El Java Platform Module System (JPMS), introducido en Java 9 y plenamente vigente en Java 21, permite organizar el código en módulos que declaran explícitamente sus dependencias y qué paquetes exportan. Proporciona encapsulación fuerte a nivel de módulo y mejora el rendimiento de carga de clases.
1. ¿Qué es un módulo?

Un módulo es un artefacto (normalmente un archivo JAR) que contiene un descriptor module-info.class en su raíz, generado a partir del archivo fuente module-info.java. Este descriptor define:

    Nombre del módulo (único, usualmente notación inversa de dominio).

    Dependencias (requires) hacia otros módulos.

    Paquetes exportados (exports) que serán accesibles para otros módulos.

    Paquetes abiertos (opens) para acceso reflexivo.

    Servicios que consume (uses) o provee (provides … with).

2. Estructura del archivo module-info.java
```java
// module-info.java
module com.mipaquete.miapp {
    // Dependencias
    requires java.logging;            // requiere el módulo java.logging
    requires transitive java.sql;     // requiere y reexporta: quien me requiere también podrá usar java.sql

    // Paquetes públicos
    exports com.mipaquete.miapp.api;  // el paquete api es accesible por otros módulos
    exports com.mipaquete.miapp.util to modulo.amigo; // exportación restringida a un módulo concreto

    // Reflexión
    opens com.mipaquete.miapp.model;  // permite reflexión sobre este paquete a todo el mundo
    opens com.mipaquete.miapp.config to modulo.framework; // reflexión restringida

    // Servicios
    uses com.mipaquete.miapp.spi.Servicio;   // consume un servicio
    provides com.mipaquete.miapp.spi.Servicio
        with com.mipaquete.miapp.internal.Implementacion; // provee una implementación
}
```

3. Directivas detalladas
3.1. requires

Declara dependencia de otro módulo.

    Sintaxis simple: requires modulo; → el módulo nombrado debe estar presente.

    requires transitive: además de requerir, cualquier módulo que requiera al nuestro verá también como accesibles los paquetes exportados por el módulo transitivo. Fomenta la reexportación de dependencias de una API.

    requires static: dependencia opcional en tiempo de compilación. Si el módulo no está presente en ejecución, se ignorará (útil para anotaciones o dependencias de herramientas que no son necesarias en tiempo de ejecución).

3.2. exports

Hace que los tipos públicos de un paquete sean accesibles desde fuera del módulo. Sin exports, un paquete es privado al módulo aunque sus clases sean public.

    exports paquete; – todos los módulos pueden acceder.

    exports paquete to modulo1, modulo2; – acceso restringido a módulos específicos (exportación cualificada). Útil para exprimir detalles internos entre módulos amigos sin abrirlos al mundo.

3.3. opens

Permite acceso reflexivo a un paquete (incluso a sus miembros privados) en tiempo de ejecución. Necesario para frameworks como Hibernate, Jackson, etc.

    opens paquete; – cualquier módulo puede usar reflexión sobre el paquete.

    opens paquete to modulo; – restringido a un módulo.

Alternativamente, en lugar de opens en módulo-info, se puede usar la opción de línea de comandos --add-opens.
3.4. Servicios (uses y provides)

    uses: declara que el módulo consume un servicio (interfaz o clase abstracta). La JVM localizará todos los módulos que provean una implementación de esa interfaz y las cargará al usar ServiceLoader.

    provides … with: declara que el módulo provee una implementación concreta para un servicio. La implementación suele ser una clase interna no exportada.

Ejemplo:
```java
module com.api {
    exports com.api.servicio;
}
module com.provider {
    requires com.api;
    provides com.api.servicio.Servicio with com.provider.ImplementacionServicio;
}
module com.consumidor {
    requires com.api;
    uses com.api.servicio.Servicio;
}
```

El consumidor puede obtener todas las implementaciones con:
```java
ServiceLoader<Servicio> loader = ServiceLoader.load(Servicio.class);
loader.forEach(s -> s.ejecutar());
```

### 4. Encapsulación y acceso por defecto

    Paquetes no exportados: completamente encapsulados; sus clases públicas no son accesibles fuera del módulo (ni siquiera mediante reflexión, a menos que se abra explícitamente).

    Paquetes exportados: sus tipos public son accesibles en tiempo de compilación y ejecución. Sin embargo, los miembros protected y private siguen restringidos según los modificadores de acceso clásicos.

    Un módulo no puede acceder a otro módulo si no lo requiere y ese otro no le exporta el paquete.

El sistema de módulos añade una capa de encapsulación por encima de los modificadores public/private, haciendo que las API sean mucho más claras y resistentes al mal uso.
5. Módulos de la propia plataforma Java

A partir de Java 9, el JDK está modularizado en una serie de módulos estándar como java.base, java.logging, java.sql, java.xml, etc. El módulo java.base contiene las clases fundamentales (java.lang, java.util, java.io, etc.) y siempre está implícitamente requerido por cualquier módulo.

Podemos listar los módulos del JDK con:
shell

### java --list-modules

### 6. Compilación y empaquetado con módulos
Estructura de directorios típica
```text
src/
  modulo1/
    module-info.java
    com/paquete/... (fuentes)
  modulo2/
    module-info.java
    com/otro/... (fuentes)
```

### Compilación con múltiples módulos
shell

### javac -d out --module-source-path src $(find src -name "*.java")

Luego se puede empaquetar cada módulo como un JAR:
shell

jar --create --file modulo1.jar -C out/modulo1 .

### Ejecución
shell

### java --module-path mods:libs -m modulo1/com.paquete.Main

Donde mods es la carpeta de los JARs modulares y libs para dependencias.
7. Migración y compatibilidad

    Modo compatibilidad: el código clásico (sin module-info) se ejecuta en el classpath como antes. Al no tener descriptor, se coloca en el módulo sin nombre (unnamed module), el cual puede acceder a todo lo que esté en el classpath, pero los módulos explícitos no pueden requerirlo (solo puede ser accedido mediante requires especial o mediante la API de reflexión si se abre). Para migrar gradualmente, se puede empezar por añadir module-info.java a los componentes que se deseen encapsular, manteniendo otros en el classpath.

    --add-exports y --add-opens: flags de la JVM para abrir paquetes de módulos (tanto del JDK como propios) durante la migración, permitiendo accesos que el descriptor normal no permitiría. Ejemplo:
```text
    java --add-opens java.base/java.lang=ALL-UNNAMED ...
```

    Esta práctica es común en frameworks hasta que adopten completamente módulos.

### 8. Beneficios de JPMS en Java 21

    Rendimiento: arranque más rápido y menor consumo de memoria al cargar solo los módulos necesarios.

    Escalabilidad: creación de imágenes de ejecución personalizadas con jlink, que genera una JRE mínima con solo los módulos requeridos.

    Encapsulación fuerte: previene el uso de API internas del JDK (como sun.misc.Unsafe) o de las propias aplicaciones, mejorando la mantenibilidad y seguridad.

    Servicios y acoplamiento débil: el mecanismo de servicios permite desacoplar proveedores y consumidores sin dependencias directas, facilitando arquitecturas modulares orientadas a plugins.

### 9. Ejemplo completo

### Módulo api (interfaz)
```java
// src/api/module-info.java
module api {
    exports com.api;
}

java

// src/api/com/api/Saludable.java
package com.api;
public interface Saludable {
    String saludo();
}
```

### Módulo impl (proveedor)
```java
// src/impl/module-info.java
module impl {
    requires api;
    provides com.api.Saludable with com.impl.SaludableEnglish;
}

java

// src/impl/com/impl/SaludableEnglish.java
package com.impl;
import com.api.Saludable;
public class SaludableEnglish implements Saludable {
    public String saludo() { return "Hello!"; }
}
```

### Módulo app (consumidor)
```java
// src/app/module-info.java
module app {
    requires api;
    uses com.api.Saludable;
}

java

// src/app/com/app/App.java
package com.app;
import com.api.Saludable;
import java.util.ServiceLoader;

public class App {
    public static void main(String[] args) {
        ServiceLoader<Saludable> loader = ServiceLoader.load(Saludable.class);
        loader.findFirst().ifPresent(s -> System.out.println(s.saludo()));
    }
}
```

Compilación y ejecución:
```bash
javac -d out --module-source-path src $(find src -name "*.java")
java --module-path out -m app/com.app.App
```

Salida: Hello!


