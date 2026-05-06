# Spring_MVC/Vistas_y_Templates.md
El concepto de ViewResolver y View

Cuando un método controlador retorna un String sin @ResponseBody, ese string es el nombre lógico de la vista. El DispatcherServlet consulta a los ViewResolvers registrados para convertir ese nombre en un objeto View real (JSP, HTML con Thymeleaf, Freemarker, etc.).
ViewResolvers más comunes

    InternalResourceViewResolver: para JSP. Prefijo y sufijo configurables (/WEB-INF/views/ y .jsp). Si la vista lógica es "usuarios/lista", busca /WEB-INF/views/usuarios/lista.jsp.

    ThymeleafViewResolver: si Thymeleaf está presente. Resuelve nombres de plantilla como "usuarios/lista" a templates/usuarios/lista.html. Soporta Spring Expression Language (SpEL) dentro del HTML.

    FreeMarkerViewResolver, MustacheViewResolver, etc.

En una aplicación Spring Boot, si usas spring-boot-starter-thymeleaf, no necesitas configurar nada; el ThymeleafViewResolver se registra automáticamente y espera las plantillas en src/main/resources/templates/.
Paso de datos del controlador a la vista

El controlador añade atributos al modelo. Esto se hace de varias formas:

    Model como parámetro: public String listar(Model model) { model.addAttribute("productos", lista); return "productos/lista"; }

    ModelAndView como retorno.

    @ModelAttribute a nivel de método en el controlador (se añade automáticamente a todos los métodos del controlador). Útil para datos de formularios o menús.

    model.addAttribute sin nombre (se deduce del tipo).

En la vista, con Thymeleaf accedes así: ${productos} o iteraciones th:each="p : ${productos}". Con JSP, mediante Expression Language ${productos}.
Thymeleaf como motor de plantillas estándar

Thymeleaf es el motor recomendado en Spring Boot por su sintaxis natural y su integración con Spring Security, i18n, etc. Características destacadas:

    Plantillas prototípicas: se pueden abrir en navegador sin servidor porque usan atributos en lugar de etiquetas JSP.

    Expression utilitarias: #strings, #dates, #numbers.

    Formularios: th:object, th:field, th:errors ligados al binding de Spring para mostrar errores de validación.

    Fragmentos y layouts: mediante th:fragment y th:replace se crean layouts reutilizables.

    Soporte de SpEL para seguridad: sec:authorize de Spring Security integrado.

Redirecciones y flash attributes

El patrón POST-redirect-GET es común para evitar el doble envío de formularios.

    El controlador retorna "redirect:/productos". Spring lo interpreta como una redirección y se invoca RedirectView.

    Para pasar datos a la siguiente petición, como mensajes de éxito, se usan flash attributes: RedirectAttributes.addFlashAttribute("mensaje", "Creado exitosamente"). Estos sobreviven a la redirección y se borran tras mostrarse.

java

@PostMapping
public String crear(@Valid Producto p, BindingResult result, RedirectAttributes ra) {
    if (result.hasErrors()) return "productos/formulario";
    service.save(p);
    ra.addFlashAttribute("success", "Producto creado");
    return "redirect:/productos";
}

REST y ¿vistas?

En servicios REST puros no se devuelven vistas. Sin embargo, puede haber endpoints híbridos que devuelvan HTML para documentación (Swagger UI) o que sirvan una SPA. Spring Boot maneja recursos estáticos desde static/, public/, META-INF/resources/. La configuración de vistas no interfiere.
Resolución de vistas y negociación de contenido en REST

Si un método devuelve un objeto y no tiene @ResponseBody, pero la petición tiene encabezados que indican que acepta JSON, el HttpMessageConverter puede tomar el control. En la práctica, si el controlador tiene @RestController todo es @ResponseBody. En un @Controller puro, para que el valor retornado se interprete como JSON debe estar anotado con @ResponseBody en el método.


