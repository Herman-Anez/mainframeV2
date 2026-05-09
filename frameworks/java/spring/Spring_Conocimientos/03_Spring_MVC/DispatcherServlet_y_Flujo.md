# DispatcherServlet y el Flujo de Petición

El **DispatcherServlet** es el componente central de Spring MVC. Actúa como el *Front Controller*, recibiendo todas las peticiones HTTP, distribuyéndolas a los controladores adecuados y gestionando el ciclo de vida completo de la respuesta.

## Funciones Principales

Las responsabilidades principales del `DispatcherServlet` incluyen:

1. **Recibir la petición:** Actúa como único punto de entrada.
2. **Handler Mapping:** Determinar qué controlador y método deben manejar la solicitud.
3. **Ejecutar el handler:** Invocar el controlador correspondiente.
4. **Resolución de vista/respuesta:** Resolver la vista lógica o generar la respuesta REST directamente.
5. **Manejo de excepciones:** Capturar y procesar errores durante el flujo.
6. **Aplicar interceptores:** Ejecutar lógica antes y después del procesamiento del controlador.

> [!NOTE]
> Spring Boot registra y configura automáticamente un `DispatcherServlet` cuando detecta el starter `spring-boot-starter-web`. En entornos tradicionales, se configuraba en el `web.xml` o mediante `WebApplicationInitializer`.

---

## Beans Estratégicos en Spring MVC

El `DispatcherServlet` delega tareas a una serie de beans especializados definidos en el `WebApplicationContext`.

### 1. HandlerMapping
Mapea una petición entrante a un *handler* (típicamente un método de controlador).
- **RequestMappingHandlerMapping:** La implementación principal que maneja `@RequestMapping`, `@GetMapping`, etc. Está habilitada por defecto.
- **BeanNameUrlHandlerMapping:** Mapea por nombre de bean si coincide con un patrón de URL (en desuso).
- **SimpleUrlHandlerMapping:** Permite configuraciones explícitas de URLs a beans.

> [!TIP]
> El proceso de búsqueda es secuencial: se recorre la lista de `HandlerMapping` registrados en orden hasta que uno devuelve un handler no nulo.

### 2. HandlerAdapter
Es el encargado de ejecutar el handler encontrado. Como existen distintos tipos de handlers, el adapter sabe cómo invocar cada uno.
- **RequestMappingHandlerAdapter:** Invoca métodos anotados. Maneja la conversión de parámetros, `@ResponseBody`, binding y validación.
- **HttpRequestHandlerAdapter / SimpleControllerHandlerAdapter:** Para otros tipos de controladores.

### 3. HandlerExceptionResolver
Maneja excepciones no capturadas que se propagan desde los handlers.

### 4. ViewResolver
Traduce el nombre lógico de una vista (String devuelto por el controlador) a un objeto `View` real (JSP, Thymeleaf, etc.).
> [!IMPORTANT]
> En servicios REST no se utiliza `ViewResolver`, ya que los métodos están anotados con `@ResponseBody` y los datos se escriben directamente en el cuerpo de la respuesta.

### 5. Otros Beans
- **LocaleResolver:** Para internacionalización (i18n).
- **ThemeResolver:** Para gestión de temas visuales.
- **FlashMapManager:** Para manejar atributos *flash* en redirecciones.

---

## Ciclo de Vida de una Petición

Imagine una petición `GET /usuarios/5` con el encabezado `Accept: text/html`:

1. **Filtros previos (Filter chain):** La petición pasa por la cadena de filtros del contenedor (Spring Security, filtros personalizados). Finalmente llega al `service()` del `DispatcherServlet`.
2. **Búsqueda del handler:** El `DispatcherServlet` consulta los `HandlerMapping`. El `RequestMappingHandlerMapping` encuentra el método `getUsuario(Long id)` en `UsuarioController`. Retorna un `HandlerExecutionChain` con el handler y los interceptores aplicables.
3. **Ejecución de interceptores (preHandle):** Se ejecutan en orden. Si alguno devuelve `false`, se detiene el flujo.
4. **Determinación del HandlerAdapter:** Se selecciona `RequestMappingHandlerAdapter`.
5. **Ejecución del HandlerAdapter:**
    - **Resolución de argumentos:** Mediante `HandlerMethodArgumentResolvers`, se convierten los datos de la petición (e.g., `@PathVariable`).
    - **Llamada al controlador:** Se invoca el método de negocio.
    - **Procesamiento del retorno:** Mediante `HandlerMethodReturnValueHandler`. Si hay `@ResponseBody`, se usa un `HttpMessageConverter`. Si no, se interpreta como nombre de vista.
6. **Post-ejecución de interceptores (postHandle):** Se ejecuta tras el controlador pero antes del renderizado.
7. **Resolución de vista:** El `ViewResolver` (ej. `ThymeleafViewResolver`) localiza la plantilla (e.g., `/templates/usuario/detalle.html`).
8. **Renderizado:** Se fusiona el modelo con la vista y se escribe la respuesta en el `HttpServletResponse`.
9. **Finalización (afterCompletion):** Se llama a los interceptores incluso si hubo una excepción (limpieza de recursos).

---

## Interceptores vs Filtros

- **Filtros:** Pertenecen al contenedor Servlet. Ideales para tareas de bajo nivel como logging global, compresión, CORS o seguridad previa.
- **Interceptores (HandlerInterceptor):** Propios de Spring MVC. Tienen acceso al handler, modelo y vista. Ideales para lógica de negocio web como verificar permisos tras el binding o añadir atributos comunes al modelo.

---

## Configuración en Spring Boot

Boot autoconfigura DispatcherServlet, RequestMappingHandlerMapping, RequestMappingHandlerAdapter, ViewResolvers (si hay Thymeleaf, el resolver correspondiente), HandlerExceptionResolver, etc. Se puede personalizar implementando WebMvcConfigurer (sin anular @EnableWebMvc):

Boot autoconfigura la mayoría de los componentes. Para personalizar el comportamiento sin anular la configuración automática, se implementa `WebMvcConfigurer`:

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new MiInterceptor())
                .addPathPatterns("/api/**");
    }

    @Override
    public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
        converters.add(new MappingJackson2HttpMessageConverter());
    }
}
```

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Proxies JDK vs CGLIB](../02_AOP/Proxies_JDK_vs_CGLIB.md) | [Índice](../../index.md) | [Controladores REST](./Controladores_REST.md) |


