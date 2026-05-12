# WebDriver Basics

## ¿Qué es WebDriver?

Es una interfaz de control de navegadores. No es una herramienta, sino una especificación W3C que los navegadores implementan mediante drivers (`chromedriver`, `geckodriver`, etc.). El script envía comandos HTTP al driver, que los traduce en acciones sobre el navegador real.

### Arquitectura

```text
Código de prueba (Java, Python...) → Cliente WebDriver → Driver (ejecutable) → Navegador
```

### Configuración básica

En Java con Selenium 4:

```java
WebDriver driver = new ChromeDriver();
driver.get("https://example.com");
String title = driver.getTitle();
driver.quit();
```

> [!TIP]
> `WebDriverManager` de Boni García elimina la descarga manual de drivers.

> [!NOTE]
> En Selenium 4 se añaden capacidades relativas de Actions, DevTools (Chrome DevTools Protocol) y localizadores mejorados.

## Localizadores (Selectores)

`By.id`, `By.name`, `By.className`, `By.tagName`, `By.linkText`/`partialLinkText`, `By.cssSelector`, `By.xpath`.

- **Prioridad**: IDs únicos > selectores CSS robustos > XPaths fiables (evitar XPaths absolutos).
- **XPath**: Posee funciones como `contains()`, `starts-with()`, ejes (`following-sibling`) útiles en estructuras complejas, pero más lentos que CSS.

## Gestión del Navegador

```java
driver.manage().window().maximize();
driver.navigate().back()/forward()/refresh();
driver.switchTo().frame() / alert() / window(handle);
```

## Cierre y Ciclo de Vida

`driver.close()` cierra la pestaña actual y `driver.quit()` cierra todas y finaliza el driver. En pruebas siempre usar `quit()` al finalizar.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Selenium Index](./index.md) | [Home](../../../index.md) | [Waits & Esperas](./Waits-esperas.md) |