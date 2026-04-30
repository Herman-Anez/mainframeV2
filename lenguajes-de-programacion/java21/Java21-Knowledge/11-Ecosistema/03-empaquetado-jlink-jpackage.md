# EMPAQUETADO CON JLINK Y JPACKAGE
1. El declive del JRE monolítico

Con la modularización (JPMS), podemos crear imágenes de ejecución ligeras que contengan solo los módulos necesarios para nuestra aplicación. Para distribuir aplicaciones a usuarios finales de forma nativa, jpackage genera instaladores como .exe, .dmg o .deb.
2. jlink: imagen JRE personalizada

jlink crea una imagen de tiempo de ejecución a partir de un conjunto de módulos. Requiere que la aplicación esté modularizada (tener module-info.java) o al menos que conozcamos los módulos que necesita (se puede hacer con jdeps).
2.1. Comando básico
```bash
jlink --module-path módulos:libs --add-modules com.miapp.mimodulo \
      --output mi-jre --launcher mi-app=com.miapp.mimodulo/com.miapp.Main

    --add-modules: lista los módulos a incluir (el raíz y sus dependencias transitivas).

    --output: directorio de la imagen generada (contiene binarios, libs, etc.).

    --launcher: crea un script ejecutable en mi-jre/bin.
```

2.2. Plugins de Maven/Gradle

    Maven: maven-jlink-plugin se configura dentro del pom.xml.

    Gradle: plugin org.beryx.jlink (badass-jlink-plugin).
    Ambos simplifican la invocación y se integran en el ciclo de package.

2.3. Ejemplo con Gradle (Kotlin DSL)
kotlin

### plugins {
    id("org.beryx.jlink") version "2.25.0"
}

### jlink {
    imageDir.set(file("$buildDir/image"))
    options.set(listOf("--strip-debug", "--compress", "2", "--no-header-files", "--no-man-pages"))
    launcher {
        name = "miapp"
        jvmArgs = listOf("-Xmx256m")
    }
}

3. jpackage: empaquetado nativo

jpackage toma la imagen generada por jlink y crea un paquete nativo para el sistema operativo. Genera un instalador autocontenido que no requiere que el usuario instale Java.
3.1. Modos de operación

    Aplicación nativa (--type app-image): genera una carpeta ejecutable ligada a una JRE ya incluida.

    Instalador (--type msi, --type deb, --type rpm, --type dmg, --type pkg): crea un instalador para distribución.

3.2. Requisitos

    La aplicación debe estar empaquetada como JAR modular o no modular (puede usar classpath, pero mejor si está en una imagen jlink previa).

    Se necesita tener herramientas nativas (En Windows: Wix para MSI; en macOS: herramientas de línea de comandos; en Linux: dpkg, rpm).

3.3. Comando típico desde jlink a jpackage

Primero creamos la imagen con jlink, luego ejecutamos jpackage:
```bash
# 1) jlink crea la JRE personalizada y launcher
jlink --module-path libs --add-modules com.mi.modulo \
      --output build/app-jre --launcher mi-app=com.mi.modulo/com.mi.Main

# 2) jpackage empaqueta esa imagen como instalador
jpackage --type deb \
         --name "MiAplicacion" \
         --input build/app-jre/bin \
         --main-jar miapp.jar \
         --main-class com.mi.Main \
         --java-options "-Xmx256m" \
         --dest build/dist
```

Alternativamente, se puede saltar jlink y que jpackage genere la JRE automáticamente con --runtime-image (señalando a un JDK).
3.4. Personalización

    --icon icono.ico (Windows) o --icon icono.icns (macOS).

    --file-associations para asociar extensiones de archivo.

    --install-dir, --vendor, --description.

    --win-console para habilitar consola en Windows.

3.5. Integración con herramientas de construcción

    Maven: org.panteleyev.jpackageplugin o se.vidstige.jpackage-maven-plugin.

    Gradle: org.panteleyev.jpackageplugin.

Ejemplo básico con Gradle:
kotlin

### plugins {
    id("org.panteleev.jpackageplugin") version "1.5.0"
}

### tasks.jpackage {
    dependsOn("build")
    appName = "MiApp"
    appVersion = project.version.toString()
    inputDir = file("${buildDir}/libs")
    mainJar = bootJar.archiveFileName.get()
    mainClass = "com.mi.Main"
    type = "deb" // o "msi", "dmg", etc.
    destinationDir = file("${buildDir}/dist")
    javaOptions = listOf("-Xmx256m")
}

3.6. Ventajas de jpackage en Java 21

    Distribuciones más seguras y pequeñas.

    Experiencia de instalación nativa.

    Compatibilidad con actualizaciones futuras (firma de código).

    Integración fluida con pipelines CI/CD.

