# Appium

Es el equivalente a Selenium para móviles: permite escribir pruebas contra aplicaciones iOS, Android (nativas, web, híbridas) usando la misma API WebDriver.

## Arquitectura

- **Appium Server**: Escrito en Node.js, recibe comandos HTTP y los traduce a frameworks de automatización nativos (`UIAutomator2` / `Espresso` para Android, `XCUITest` para iOS).
- **Cliente**: Disponible en múltiples lenguajes (Java, Python, JS, etc.) usando la librería cliente apropiada.

## Conceptos Fundamentales

### Desired Capabilities
Conjunto de pares clave-valor que indican el dispositivo, plataforma, app y otras configuraciones.

```java
DesiredCapabilities caps = new DesiredCapabilities();
caps.setCapability("platformName", "Android");
caps.setCapability("appium:deviceName", "emulator-5554");
caps.setCapability("appium:app", "/ruta/app.apk");
caps.setCapability("appium:automationName", "UiAutomator2");
AndroidDriver driver = new AndroidDriver(new URL("http://localhost:4723"), caps);
```

### Localización
Similar a Selenium, pero con selectores específicos:
- **AccessibilityId**: El más robusto y recomendado.
- **XPath Nativo**.
- **UIAutomator** (Android).
- **Predicates** (iOS).

### Gestos
Appium provee APIs para *tap*, *swipe*, *scroll*, *pinch*, *drag and drop*. Se utilizan mediante `W3C Actions` con punteros táctiles.

```java
driver.executeScript("mobile: swipeGesture", ImmutableMap.of(
    "left", 100, "top", 500, "width", 200, "height", 200, "direction", "up"
));
```

### Contextos
En apps híbridas (*webviews*) se cambia entre contexto nativo y web con `driver.getContextHandles()` y `driver.context()`.

## Ejecución en Paralelo
Appium permite múltiples sesiones en un mismo servidor o usar Selenium Grid con nodos Appium. Combinado con TestNG/JUnit y granjas de dispositivos en la nube (Sauce Labs, BrowserStack), se logran pruebas masivas.

> [!IMPORTANT]
> **Retos**: Configuración de dispositivos/emuladores, latencia y esperas no fiables. Los SDETs aplican esperas explícitas y Page Objects móviles para mitigar estos problemas.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Mobile Index](./index.md) | [Home](../../index.md) | [Detox](./Detox.md) |