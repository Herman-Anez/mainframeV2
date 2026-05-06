# Miscelaneos/Internacionalizacion_i18n.md
El desafío de las aplicaciones multidioma

Una aplicación global debe presentar mensajes, etiquetas, formatos de fecha/número y validaciones en el idioma y la región del usuario. Spring proporciona un soporte sólido para i18n (internacionalización) y l10n (localización) mediante la abstracción MessageSource y la resolución de Locale.
MessageSource: la fábrica de mensajes

MessageSource es una interfaz que permite obtener mensajes por código y Locale. Spring define tres implementaciones principales:

    ResourceBundleMessageSource: carga bundles .properties desde el classpath. Sin caché configurable (lee cada vez por defecto, aunque internamente usa ResourceBundle con caché de la JVM).

    ReloadableResourceBundleMessageSource: similar, pero soporta recarga en caliente sin reiniciar la aplicación. Ideal para desarrollo o cuando los bundles están externos.

    StaticMessageSource: para mensajes programáticos, útil en tests.

Spring Boot autoconfigura un MessageSource buscando archivos messages*.properties en la raíz del classpath. La configuración por defecto:
properties

spring.messages.basename=messages
spring.messages.encoding=UTF-8
spring.messages.cache-duration=3600   # segundos, para producción

Se pueden definir múltiples basenames: messages, errors.

Los archivos se nombran con el sufijo del locale: messages_es.properties, messages_en.properties, messages_fr.properties. Si no encuentra el código en el locale exacto, busca en el idioma base y luego en el archivo sin sufijo.
Resolución de mensajes en código Java

Inyectamos MessageSource y solicitamos un mensaje con un Locale:
java

@Autowired
private MessageSource messageSource;

public String saludo(Locale locale) {
    return messageSource.getMessage("saludo.bienvenida", null, locale);
}

Si el mensaje requiere parámetros:
properties

#### Miscelaneos/Internacionalizacion_i18n.md
El desafío de las aplicaciones multidioma

Una aplicación global debe presentar mensajes, etiquetas, formatos de fecha/número y validaciones en el idioma y la región del usuario. Spring proporciona un soporte sólido para i18n (internacionalización) y l10n (localización) mediante la abstracción MessageSource y la resolución de Locale.
MessageSource: la fábrica de mensajes

MessageSource es una interfaz que permite obtener mensajes por código y Locale. Spring define tres implementaciones principales:

    ResourceBundleMessageSource: carga bundles .properties desde el classpath. Sin caché configurable (lee cada vez por defecto, aunque internamente usa ResourceBundle con caché de la JVM).

    ReloadableResourceBundleMessageSource: similar, pero soporta recarga en caliente sin reiniciar la aplicación. Ideal para desarrollo o cuando los bundles están externos.

    StaticMessageSource: para mensajes programáticos, útil en tests.

Spring Boot autoconfigura un MessageSource buscando archivos messages*.properties en la raíz del classpath. La configuración por defecto:
properties

spring.messages.basename=messages
spring.messages.encoding=UTF-8
spring.messages.cache-duration=3600   # segundos, para producción

Se pueden definir múltiples basenames: messages, errors.

Los archivos se nombran con el sufijo del locale: messages_es.properties, messages_en.properties, messages_fr.properties. Si no encuentra el código en el locale exacto, busca en el idioma base y luego en el archivo sin sufijo.
Resolución de mensajes en código Java

Inyectamos MessageSource y solicitamos un mensaje con un Locale:
java

@Autowired
private MessageSource messageSource;

public String saludo(Locale locale) {
    return messageSource.getMessage("saludo.bienvenida", null, locale);
}

Si el mensaje requiere parámetros:
properties

# messages_es.properties
pedido.confirmacion=Pedido {0} confirmado con total de {1,number,currency}

java

String mensaje = messageSource.getMessage(
    "pedido.confirmacion",
    new Object[]{pedido.getId(), pedido.getTotal()},
    locale);

Podemos manejar mensajes de error con argumentos y DefaultMessageSourceResolvable.
Resolución del Locale

Spring necesita determinar el Locale del usuario. El DispatcherServlet utiliza un LocaleResolver:

    AcceptHeaderLocaleResolver (defecto): analiza el header Accept-Language de la petición HTTP. Stateless, ideal para APIs.

    SessionLocaleResolver: almacena el locale en la sesión HTTP. Útil cuando el usuario puede cambiar de idioma manualmente.

    CookieLocaleResolver: persiste el locale en una cookie, sobrevive entre sesiones.

    FixedLocaleResolver: fuerza un locale fijo (por ejemplo, para un backend interno).

Spring Boot, por defecto, usa AcceptHeaderLocaleResolver. Para permitir al usuario cambiar de idioma, se configura un SessionLocaleResolver junto con un LocaleChangeInterceptor:
java

@Bean
public LocaleResolver localeResolver() {
    SessionLocaleResolver resolver = new SessionLocaleResolver();
    resolver.setDefaultLocale(Locale.forLanguageTag("es"));
    return resolver;
}

@Bean
public LocaleChangeInterceptor localeChangeInterceptor() {
    LocaleChangeInterceptor interceptor = new LocaleChangeInterceptor();
    interceptor.setParamName("lang");
    return interceptor;
}

@Override
public void addInterceptors(InterceptorRegistry registry) {
    registry.addInterceptor(localeChangeInterceptor);
}

Ahora, una petición GET /productos?lang=en cambia el locale para esa sesión.
i18n en plantillas Thymeleaf

Thymeleaf integra el MessageSource mediante la expresión #{…}:
html

<h1 th:text="#{titulo.productos}">Productos</h1>
<p th:text="#{pedido.confirmado(${pedido.id}, ${pedido.total})}">Pedido confirmado</p>

Para fechas y números, Thymeleaf usa #dates.format y #numbers.formatDecimal con el Locale del contexto automáticamente.
i18n en REST y validación

Las anotaciones de Bean Validation también se pueden internacionalizar. En los archivos de validación (messages_es.properties) definimos:
properties

producto.nombre.obligatorio=El nombre del producto es obligatorio
precio.positivo=El precio debe ser positivo

Las anotaciones usan {producto.nombre.obligatorio} como valor de message. Spring MVC, al fallar la validación, resuelve esos mensajes usando el MessageSource y el Locale de la petición.

En un @ControllerAdvice personalizado, también podemos inyectar MessageSource para construir mensajes de error localizados:
java

@ExceptionHandler(RecursoNoEncontradoException.class)
public ResponseEntity<ErrorDTO> manejarNoEncontrado(RecursoNoEncontradoException ex, Locale locale) {
    String mensaje = messageSource.getMessage("error.recurso_no_encontrado", new Object[]{ex.getId()}, locale);
    return ResponseEntity.status(404).body(new ErrorDTO(mensaje));
}

Internacionalización de valores en @ConfigurationProperties

No directamente. Las propiedades de configuración no están pensadas para i18n. Usa mensajes en las vistas o respuestas API.
Buenas prácticas

    Centraliza los mensajes en archivos .properties con nombres descriptivos.

    Usa ReloadableResourceBundleMessageSource en desarrollo.

    Evita mensajes largos con lógica de negocio en las plantillas; mantenlos simples.

    Para aplicaciones con muchos idiomas, considera servicios externos de traducción o un CMS.

 messages_es.properties
pedido.confirmacion=Pedido {0} confirmado con total de {1,number,currency}

java

String mensaje = messageSource.getMessage(
    "pedido.confirmacion",
    new Object[]{pedido.getId(), pedido.getTotal()},
    locale);

Podemos manejar mensajes de error con argumentos y DefaultMessageSourceResolvable.
Resolución del Locale

Spring necesita determinar el Locale del usuario. El DispatcherServlet utiliza un LocaleResolver:

    AcceptHeaderLocaleResolver (defecto): analiza el header Accept-Language de la petición HTTP. Stateless, ideal para APIs.

    SessionLocaleResolver: almacena el locale en la sesión HTTP. Útil cuando el usuario puede cambiar de idioma manualmente.

    CookieLocaleResolver: persiste el locale en una cookie, sobrevive entre sesiones.

    FixedLocaleResolver: fuerza un locale fijo (por ejemplo, para un backend interno).

Spring Boot, por defecto, usa AcceptHeaderLocaleResolver. Para permitir al usuario cambiar de idioma, se configura un SessionLocaleResolver junto con un LocaleChangeInterceptor:
java

@Bean
public LocaleResolver localeResolver() {
    SessionLocaleResolver resolver = new SessionLocaleResolver();
    resolver.setDefaultLocale(Locale.forLanguageTag("es"));
    return resolver;
}

@Bean
public LocaleChangeInterceptor localeChangeInterceptor() {
    LocaleChangeInterceptor interceptor = new LocaleChangeInterceptor();
    interceptor.setParamName("lang");
    return interceptor;
}

@Override
public void addInterceptors(InterceptorRegistry registry) {
    registry.addInterceptor(localeChangeInterceptor);
}

Ahora, una petición GET /productos?lang=en cambia el locale para esa sesión.
i18n en plantillas Thymeleaf

Thymeleaf integra el MessageSource mediante la expresión #{…}:
html

<h1 th:text="#{titulo.productos}">Productos</h1>
<p th:text="#{pedido.confirmado(${pedido.id}, ${pedido.total})}">Pedido confirmado</p>

Para fechas y números, Thymeleaf usa #dates.format y #numbers.formatDecimal con el Locale del contexto automáticamente.
i18n en REST y validación

Las anotaciones de Bean Validation también se pueden internacionalizar. En los archivos de validación (messages_es.properties) definimos:
properties

producto.nombre.obligatorio=El nombre del producto es obligatorio
precio.positivo=El precio debe ser positivo

Las anotaciones usan {producto.nombre.obligatorio} como valor de message. Spring MVC, al fallar la validación, resuelve esos mensajes usando el MessageSource y el Locale de la petición.

En un @ControllerAdvice personalizado, también podemos inyectar MessageSource para construir mensajes de error localizados:
java

@ExceptionHandler(RecursoNoEncontradoException.class)
public ResponseEntity<ErrorDTO> manejarNoEncontrado(RecursoNoEncontradoException ex, Locale locale) {
    String mensaje = messageSource.getMessage("error.recurso_no_encontrado", new Object[]{ex.getId()}, locale);
    return ResponseEntity.status(404).body(new ErrorDTO(mensaje));
}

Internacionalización de valores en @ConfigurationProperties

No directamente. Las propiedades de configuración no están pensadas para i18n. Usa mensajes en las vistas o respuestas API.
Buenas prácticas

    Centraliza los mensajes en archivos .properties con nombres descriptivos.

    Usa ReloadableResourceBundleMessageSource en desarrollo.

    Evita mensajes largos con lógica de negocio en las plantillas; mantenlos simples.

    Para aplicaciones con muchos idiomas, considera servicios externos de traducción o un CMS.

