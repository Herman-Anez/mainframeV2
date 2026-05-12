Appium

Es el equivalente a Selenium para móviles: permite escribir pruebas contra aplicaciones iOS, Android (nativas, web, híbridas) usando la misma API WebDriver.

Arquitectura:

    Appium Server (escrito en Node) recibe comandos HTTP y los traduce a frameworks de automatización nativos: UIAutomator2 / Espresso para Android, XCUITest para iOS.

    Cliente en cualquier lenguaje (Java, Python) usando la librería apropiada.

Conceptos fundamentales:

    Desired Capabilities: conjunto de pares clave-valor que indican el dispositivo, plataforma, app, etc. Ejemplo Android:
    java

    DesiredCapabilities caps = new DesiredCapabilities();
    caps.setCapability("platformName", "Android");
    caps.setCapability("appium:deviceName", "emulator-5554");
    caps.setCapability("appium:app", "/ruta/app.apk");
    caps.setCapability("appium:automationName", "UiAutomator2");
    AndroidDriver driver = new AndroidDriver(new URL("http://localhost:4723"), caps);

    Localización: Similar a Selenium, pero con selectores específicos como AccessibilityId, XPath nativo, UIAutomator (Android) y predicates (iOS). La AccessibilityId es el más robusto.

    Gestos: Appium provee APIs para tap, swipe, scroll, pinch, drag and drop mediante la clase TouchAction (deprecada en versiones nuevas) o mediante W3C Actions con punteros táctiles. Ejemplo swipe:
    java

    driver.executeScript("mobile: swipeGesture", ImmutableMap.of(
        "left", 100, "top", 500, "width", 200, "height", 200, "direction", "up"
    ));

    Contextos: En apps híbridas (webviews) se cambia entre contexto nativo y web con driver.getContextHandles() y driver.context().

    Ejecución en paralelo: Appium permite múltiples sesiones en un mismo servidor o usar Selenium Grid con nodos Appium. Combinado con TestNG/JUnit y dispositivos en la nube (Sauce Labs, BrowserStack) se logran pruebas masivas.

    Retos: Configuración de dispositivos/emuladores, latencia, esperas no fiables. Los SDETs aplican esperas explícitas y Page Objects móviles para mitigarlo.