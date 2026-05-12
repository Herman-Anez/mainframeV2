# Page Object Model (POM)

Es el patrón de diseño más adoptado para automatización de UI. Cada página web se modela como una clase; los elementos son campos y las acciones son métodos que retornan otras páginas.

## Principios

- **Encapsulamiento**: No exponer `WebDriver` ni `By` al test.
- **Funcionalidad**: Los métodos públicos representan la funcionalidad de la página (login, buscar).
- **Navegación**: Si una acción navega a otra página, el método retorna la instancia de esa nueva página.
- **Separación de responsabilidades**: No contener aserciones en los Page Objects (eso va en los tests o en capas adicionales); separar lógica de validación.

## Implementación con Page Factory

Selenium ofrece `PageFactory` que inicializa los elementos anotados con `@FindBy`.

```java
public class LoginPage {
    @FindBy(id = "username")
    WebElement username;
    @FindBy(id = "password")
    WebElement password;
    @FindBy(id = "loginBtn")
    WebElement loginButton;

    public LoginPage(WebDriver driver) {
        PageFactory.initElements(driver, this);
    }

    public HomePage loginAs(String user, String pass) {
        username.sendKeys(user);
        password.sendKeys(pass);
        loginButton.click();
        return new HomePage(driver);
    }
}
```

> [!TIP]
> **Pros**: Código declarativo y menos boilerplate.

> [!CAUTION]
> **Contras**: El *lazy initialization* puede esconder problemas; es más frágil con proxies. Muchos SDETs prefieren inicializar los `By` explícitamente y usar `driver.findElement(…)` directamente con esperas.

## Evolución del POM

- **Component Objects**: Dividir una página en componentes reutilizables (header, tabla, modal).
- **Screenplay**: Abstracción mayor que separa actores, tareas y preguntas; el Page Object se reduce a una fuente de localizadores y no contiene lógica de navegación.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Waits & Esperas](./Waits-esperas.md) | [Home](../../../index.md) | [Cypress](../Cypress/index.md) |