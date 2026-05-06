# Vistas y Templates

En Spring MVC, una "Vista" es el componente encargado de renderizar la respuesta final al usuario (generalmente HTML).

## Concepto de ViewResolver y View

Cuando un método controlador retorna un `String` (y no tiene `@ResponseBody`), ese string es el **nombre lógico** de la vista. El `DispatcherServlet` consulta a los `ViewResolvers` para convertir ese nombre en un objeto `View` real.

### ViewResolvers Comunes

- **InternalResourceViewResolver:** Utilizado para JSPs. Permite configurar prefijos y sufijos (e.g., `/WEB-INF/views/` y `.jsp`).
- **ThymeleafViewResolver:** Utilizado cuando Thymeleaf está presente. Resuelve nombres a plantillas `.html` dentro de `templates/`. Soporta *Spring Expression Language* (SpEL).
- **FreeMarkerViewResolver / MustacheViewResolver:** Para otros motores de plantillas.

> [!NOTE]
> En aplicaciones Spring Boot con `spring-boot-starter-thymeleaf`, no es necesaria la configuración manual; el motor se registra automáticamente y busca las plantillas en `src/main/resources/templates/`.

---

## Paso de Datos a la Vista

El controlador comunica datos a la vista mediante el **Modelo**. Existen varias formas de hacerlo:

1. **`Model` como parámetro:**
   ```java
   public String listar(Model model) { 
       model.addAttribute("productos", lista); 
       return "productos/lista"; 
   }
   ```
2. **`ModelAndView` como retorno:** Combina el nombre de la vista y el modelo en un solo objeto.
3. **`@ModelAttribute`:** A nivel de método, permite añadir datos que estarán disponibles en todos los métodos del controlador (e.g., para menús o listas de selección).

> [!TIP]
> En la vista (Thymeleaf), accedes a los datos usando `${nombreAtributo}`. Ejemplo: `${productos}`.

---

## Thymeleaf: El Estándar Moderno

Thymeleaf es el motor recomendado por su sintaxis natural y su profunda integración con Spring.

### Características Principales

- **Plantillas Prototípicas:** Los archivos `.html` se pueden abrir directamente en un navegador sin servidor, ya que usan atributos (`th:`) que el navegador ignora.
- **Expresiones Utilitarias:** Soporte para `#strings`, `#dates`, `#numbers`, etc.
- **Formularios:** Integración con `th:object`, `th:field` y `th:errors` para binding y validación.
- **Layouts y Fragmentos:** Reutilización de código mediante `th:fragment` y `th:replace`.
- **Seguridad:** Integración con Spring Security mediante el dialecto `sec:authorize`.

---

## Redirecciones y Flash Attributes

Para evitar el reenvío de formularios al refrescar la página (patrón **POST-redirect-GET**):

1. **Redirección:** El controlador retorna `"redirect:/ruta"`.
2. **Flash Attributes:** Se usa `RedirectAttributes` para pasar datos que sobrevivan a la redirección (e.g., mensajes de éxito) y se borren inmediatamente después.

```java
@PostMapping
public String crear(@Valid Producto p, BindingResult result, RedirectAttributes ra) {
    if (result.hasErrors()) return "productos/formulario";
    service.save(p);
    ra.addFlashAttribute("success", "Producto creado exitosamente");
    return "redirect:/productos";
}
```

---

## REST y Vistas Híbridas

En servicios REST puros no se devuelven vistas, pero puede haber **endpoints híbridos**. 

- Si un controlador tiene `@RestController`, todo es `@ResponseBody`.
- En un `@Controller` estándar, si un método no tiene `@ResponseBody`, Spring intentará resolverlo como una vista.
- Spring Boot sirve automáticamente recursos estáticos desde `/static`, `/public` o `/META-INF/resources`.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Validación y Binding](./Validacion_y_BindingResult.md) | [Índice](../../README.md) | [Spring Boot: Autoconfiguración](../04_Spring_Boot/Autoconfiguracion_y_Starters.md) |




