# Scopes y Proxies en Spring

## El concepto de Scope (ámbito) en Spring

El scope define el ciclo de vida y visibilidad de un bean. Responde a cuántas instancias del bean se crean, cuándo se crean y cuándo se destruyen. Spring no solo maneja los típicos singleton y prototype, sino que ofrece una gama de ámbitos específicos para aplicaciones web.

## 1. Singleton (por defecto)

Una única instancia por contenedor Spring IoC. Ésta se crea, por defecto, en la fase de arranque (eager loading) y se sirve para todas las inyecciones. Es el scope más eficiente en memoria y el estándar para servicios sin estado.

```java
@Service // Por defecto singleton
public class UsuarioService { }
```

O de manera explícita:

```java
@Bean
@Scope(ConfigurableBeanFactory.SCOPE_SINGLETON) // "singleton"
public UsuarioService usuarioService() { return new UsuarioService(); }
```

> [!WARNING]
> El bean singleton se almacena en un mapa concurrente dentro del contenedor. Cuidado con el estado mutable: si un singleton guarda datos de petición, se mezclarán entre distintos usuarios. Para estado propio de la petición, hay que utilizar scopes web o almacenar los datos en objetos no gestionados (pass-by-value).

## 2. Prototype

Una nueva instancia por cada solicitud del bean. Si inyectas un bean prototype en un bean singleton, esa inyección ocurre una única vez; no se crea una nueva instancia cada vez que se invoca un método del singleton. Esto es la principal fuente de confusión.

```java
@Component
@Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE) // "prototype"
public class PrototipoService { }
```

Problema típico:

```java
@Component
public class Gestor {
    @Autowired
    private PrototipoService protoService; // Se inyecta una única instancia en toda la vida del Gestor
}
```

Soluciones para obtener una instancia fresca cada vez:

- Inyectar `ObjectProvider<PrototipoService>` y llamar a `getIfAvailable()`.
- Inyectar `ApplicationContext` y obtenerlo programáticamente (`context.getBean(PrototipoService.class)`), aunque eso acopla al contenedor.
- Usar `@Lookup` sobre un método abstracto que devuelva el tipo prototype: Spring generará una subclase (a través de CGLIB) que devolverá un nuevo bean cada vez.

```java
@Component
public class Gestor {
    @Lookup
    public PrototipoService obtenerPrototipoService() { return null; } // Spring sobreescribe el método
}
```

- Configurar un proxy en el scope prototype para que cada invocación a sus métodos cree una nueva instancia (ver más abajo).

> [!NOTE]
> Los beans prototype dejan de ser gestionados después de la creación: Spring no destruye sus métodos `@PreDestroy` (salvo que se registre un `DestructionAwareBeanPostProcessor` personalizado). Tú eres responsable de liberar sus recursos.

## 3. Request (ámbito web)

Una instancia por petición HTTP. Se crea al iniciar la petición y se destruye al terminarla. Permite almacenar datos del ciclo de la solicitud, como el usuario autenticado, sin necesidad de pasar `HttpServletRequest` por todos los métodos.

```java
@Component
@RequestScope // equivalente a @Scope(value = WebApplicationContext.SCOPE_REQUEST)
public class DatosRequest {
    private String usuario;
    // getters/setters
}
```

Detrás de escena: Spring no crea un bean “real” de ámbito request, sino un proxy que se inyecta en otros beans (p.ej. un controlador singleton). Cada vez que se invoca un método del proxy dentro de una petición HTTP, el proxy delega en la instancia correcta (que está almacenada en un mapa dentro del `RequestAttributes`). Este mecanismo es crucial porque no se puede inyectar un bean de vida corta directamente en un bean de vida larga (el singleton viviría eternamente).

**Necesidad de `@Scope` con proxy:**
Si inyectas `DatosRequest` en un controller singleton, Spring necesita envolverlo en un proxy. Por defecto, con `@RequestScope`, Spring Boot habilita automáticamente el proxy (lo crea mediante CGLIB o JDK). Si usas la anotación genérica `@Scope("request")` necesitas activar explícitamente el modo proxy:

```java
@Bean
@Scope(value = WebApplicationContext.SCOPE_REQUEST, proxyMode = ScopedProxyMode.TARGET_CLASS)
public DatosRequest datosRequest() { return new DatosRequest(); }
```

`proxyMode` puede ser:

- `ScopedProxyMode.TARGET_CLASS` → proxy CGLIB (necesita clase no final).
- `ScopedProxyMode.INTERFACES` → proxy JDK si la clase implementa una interfaz adecuada.
- `ScopedProxyMode.NO` → no proxy (solo válido si el bean se inyecta en otro bean del mismo ámbito o si se obtiene bajo demanda).

## 4. Session (ámbito web)

Una instancia por sesión HTTP. Mantiene estado a lo largo de todas las peticiones de un mismo usuario. Muy útil para carritos de compra, preferencias de usuario, etc.

```java
@Component
@SessionScope // @Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = TARGET_CLASS)
public class CarritoBean { ... }
```

La sesión vive mientras el `HttpSession` exista. Al destruirse la sesión, el bean también se destruye. De nuevo, el proxy hace posible la inyección en beans singleton.

> [!WARNING]
> Peligro: en aplicaciones REST sin estado, `@SessionScope` puede causar efectos no deseados si el cliente no envía cookies de sesión. En esos casos, se desactiva el soporte de sesiones o se usa un `@RequestScope` apoyado en tokens JWT para guardar estado puntual.

## 5. Application (ámbito web)

Una única instancia por `ServletContext`. Es como un singleton global a toda la aplicación web (en un clúster, cada nodo tiene su instancia). Poco usado, pero disponible para recursos compartidos por todas las sesiones y peticiones, como un catálogo en memoria que no cambia.

```java
@Component
@ApplicationScope // @Scope(value = WebApplicationContext.SCOPE_APPLICATION, proxyMode = TARGET_CLASS)
public class ConfiguracionGlobalBean { ... }
```

## 6. WebSocket (ámbito web)

Una instancia por ciclo de vida de una conexión WebSocket. Muy específico para almacenar estado durante una conversación WebSocket. Necesita también proxy.

```java
@Component
@Scope(scopeName = "websocket", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class ChatBean { ... }
```

## Cómo funcionan los proxies de ámbito

Cuando inyectas un bean de scope corto (request, session, etc.) en uno largo (singleton), Spring no puede colocar la instancia real porque ésta aún no existe en el momento del arranque del contenedor. La solución es un proxy (generado por CGLIB/JDK) que implementa la misma interfaz o extiende la clase y se registra en el lugar del bean original. Cada vez que se ejecuta un método del proxy, éste:

1. Determina el ámbito correspondiente (request, session...).
2. Busca la instancia real en el contenedor del ámbito (p.ej., la sesión HTTP).
3. Si no existe, la crea y la almacena.
4. Delega la llamada al método en la instancia real.
5. Al finalizar el ámbito, el bean real se destruye.

El proxy vive tanto como el bean donde fue inyectado (por ejemplo, toda la vida del singleton). Pero cada hilo que lo invoca recibe la instancia adecuada a su contexto. Esta magia es la que permite escribir aplicaciones web sin preocuparse explícitamente por los límites de los ámbitos.

## Cuándo usar cada scope

- **Singleton:** para lógica de negocio sin estado, repositorios, servicios utilitarios, etc.
- **Prototype:** cuando cada uso necesita su propia copia (por ejemplo, objetos que acumulan estado mutable durante un proceso, o cuando la creación tiene lógica condicional).
- **Request:** información vinculada a una sola petición HTTP, como el ID de usuario extraído de un token JWT o metadatos de la llamada.
- **Session:** estado persistente del usuario (carrito, preferencias de visualización). Solo en aplicaciones con sesiones HTTP.
- **Application:** es tan amplio que casi ningún caso práctico lo necesita; mejor usar un singleton común.

---

[⬅️ Volver al Índice](../../index.md)
