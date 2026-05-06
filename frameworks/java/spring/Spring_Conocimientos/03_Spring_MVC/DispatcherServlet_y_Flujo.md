# Spring_MVC/DispatcherServlet_y_Flujo.md
El corazón de Spring MVC: DispatcherServlet

DispatcherServlet es el Front Controller del patrón MVC. Recibe todas las peticiones HTTP, las distribuye a los controladores adecuados y gestiona todo el ciclo de vida de la respuesta. Sus responsabilidades principales:

    Recibir la petición.

    Determinar qué controlador y método manejan la solicitud (handler mapping).

    Ejecutar el handler (controlador).

    Resolver la vista lógica o generar la respuesta REST.

    Manejar excepciones.

    Aplicar interceptores.

Spring Boot registra y configura automáticamente un DispatcherServlet cuando detecta el starter spring-boot-starter-web. En un entorno tradicional, se configura en el web.xml o mediante la interfaz WebApplicationInitializer.
Roles de los beans estratégicos en Spring MVC

El DispatcherServlet utiliza una serie de beans especializados para delegar las tareas. Estos se definen en el contexto de la aplicación web (el WebApplicationContext, hijo del contexto raíz).

    HandlerMapping: Mapea una petición entrante a un handler (típicamente un método de controlador). Varias implementaciones:

        RequestMappingHandlerMapping: maneja las anotaciones @RequestMapping, @GetMapping, etc. Es la principal y está habilitada por defecto en Spring Boot.

        BeanNameUrlHandlerMapping: mapea por nombre de bean si coincide con un patrón de URL (casi en desuso).

        SimpleUrlHandlerMapping: configuraciones explícitas de URLs a beans.

    El proceso de búsqueda es secuencial: se recorre la lista de HandlerMapping en orden hasta que uno devuelve un handler no nulo.

    HandlerAdapter: Ejecuta el handler encontrado. Como los handlers pueden ser de distintos tipos (métodos anotados, controladores que implementan Controller, etc.), el HandlerAdapter sabe cómo invocarlos.

        RequestMappingHandlerAdapter: invoca métodos anotados con @RequestMapping. Se encarga de la conversión de parámetros, manejo de @ResponseBody, binding, validación, etc.

        HttpRequestHandlerAdapter, SimpleControllerHandlerAdapter para otros tipos.

    HandlerExceptionResolver: Maneja excepciones no capturadas que se propagan desde los handlers. Se verá en detalle más adelante.

    ViewResolver: Traduce el nombre lógico de una vista (String devuelto por el controlador) a un objeto View (JSP, Thymeleaf, etc.). En REST no se usa, porque el método está anotado con @ResponseBody.

    LocaleResolver, ThemeResolver, FlashMapManager: Para internacionalización, temas y atributos flash (redirecciones).

Ciclo de vida detallado de una petición

Suponiendo una petición GET /usuarios/5 con header Accept: text/html.

    Filtros previos (Filter chain) : Antes de llegar al DispatcherServlet, la petición pasa por los filtros de la cadena estándar (Spring Security, filtros personalizados, etc.). El DispatcherServlet se registra como un servlet y se invoca su service().

    Búsqueda del handler: DispatcherServlet consulta cada HandlerMapping registrado. RequestMappingHandlerMapping encuentra que el método getUsuario(Long id) en UsuarioController mapea con GET /usuarios/{id}. Retorna un HandlerExecutionChain que contiene el handler (un HandlerMethod que encapsula el controlador y método) y una lista de interceptores aplicables.

    Ejecución de interceptores (preHandle) : Si la cadena tiene interceptores, se ejecuta preHandle de cada uno en orden. Si alguno devuelve false, se corta la petición y se puede enviar una respuesta temprana.

    Determinación del HandlerAdapter: Se busca un HandlerAdapter que soporte el handler. RequestMappingHandlerAdapter es el adecuado.

    Ejecución del HandlerAdapter:

        Resolución de argumentos: mediante HandlerMethodArgumentResolvers, convierte los parámetros de la petición en los argumentos del método. Por ejemplo, @PathVariable("id") Long id, @RequestParam, @RequestBody, etc. Hay decenas de resolvers predefinidos.

        Llamada al método del controlador: se invoca usuarioController.getUsuario(5L).

        Procesamiento del retorno: mediante HandlerMethodReturnValueHandler. Si el método devuelve un String ("usuario/detalle") y la clase NO tiene @ResponseBody, se interpreta como nombre de vista. Si tiene @ResponseBody, se convierte el objeto a JSON mediante HttpMessageConverter.

    Post-ejecución de interceptores (postHandle) : Después de que el handler se ejecutó pero antes de renderizar la vista, se llama a postHandle. Permite modificar el modelo.

    Resolución de vista (si es necesario) : Si el handler devuelve un nombre de vista lógico, el ViewResolver seleccionado (ej. ThymeleafViewResolver) lo resuelve a una plantilla concreta (/templates/usuario/detalle.html). Se crea el objeto View.

    Renderizado de la vista: La vista se fusiona con el modelo (el ModelAndView o los atributos añadidos) y se escribe la respuesta en el HttpServletResponse.

    Finalización (afterCompletion) : Se llama a afterCompletion de los interceptores, incluso si hubo excepción, similar a un finally. Perfecto para limpiar recursos.

Interceptores vs Filtros

    Filtros: son parte del contenedor Servlet, no conocen detalles de Spring MVC. Útiles para logging, compresión, CORS, seguridad pre-triaje.

    Interceptores (HandlerInterceptor): tienen acceso al handler, modelo y vista, y se ejecutan dentro del contexto del DispatcherServlet. Ideal para añadir atributos comunes al modelo, verificar permisos tras el binding, medir tiempos, etc.

Configuración en Spring Boot

Boot autoconfigura DispatcherServlet, RequestMappingHandlerMapping, RequestMappingHandlerAdapter, ViewResolvers (si hay Thymeleaf, el resolver correspondiente), HandlerExceptionResolver, etc. Se puede personalizar implementando WebMvcConfigurer (sin anular @EnableWebMvc):
java

@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new MiInterceptor()).addPathPatterns("/api/**");
    }
    @Override
    public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
        converters.add(new MappingJackson2HttpMessageConverter());
    }
}
