# Singleton y Factory en Testing

## Singleton

Asegura que una clase tenga una única instancia y provee un punto de acceso global. En testing se usa controvertidamente para los drivers `WebDriver`, porque compartir el mismo driver entre pruebas en paralelo causa interferencias. El patrón correcto es Singleton por thread o inyección de dependencia con container.

> [!IMPORTANT]
> El patrón correcto para pruebas en paralelo es Singleton por thread o inyección de dependencia con container para evitar interferencias.

### Ejemplo clásico
`WebDriverManager` que devuelve el mismo driver para toda la clase de prueba (no para ejecución paralela).

```java
public class DriverManager {
    private static ThreadLocal<WebDriver> driver = new ThreadLocal<>();
    public static WebDriver getDriver() {
        if (driver.get() == null) {
            driver.set(new ChromeDriver());
        }
        return driver.get();
    }
}
```

En Python, se puede implementar con módulos (el módulo es singleton) o con `@singleton` decorator. En la práctica, los frameworks modernos como Selenide o Playwright manejan esto internamente; el SDET rara vez necesita un singleton manual.

## Factory (Método de fábrica / Abstract Factory)

Crea objetos sin especificar la clase concreta. Magnífico para:

*   Crear drivers según parámetros (Chrome, Firefox, Remote) sin que el test conozca la implementación.
*   Generar datos de prueba con fábricas que devuelven objetos `User`, `Product` con valores válidos, aleatorios o concretos. Se combina con el patrón Builder para legibilidad.

```java
public class UserFactory {
    public static User createDefaultUser() {
        return User.builder().name("Test").email("test@test.com").build();
    }
    public static User createAdminUser() { ... }
}
```

En testing de APIs, una `ResponseFactory` convierte respuestas crudas en objetos de dominio para aserciones tipadas.

---

| Anterior | Inicio | Siguiente |
| :------- | :----: | :-------- |
| ⏪ [Patrones de diseño](index.md) | [Índice](index.md) | [Screenplay y Fluent](Screenplay-fluent.md) ⏩ |
