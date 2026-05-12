Waits-esperas

Las esperas son el mecanismo más crítico para evitar flaky tests. Selenium ejecuta comandos tan rápido como el código; si la UI no ha cargado el elemento, lanza NoSuchElementException.

    Esperas implícitas:
    driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
    Se configura una sola vez y aplica a todas las búsquedas de elementos. Si el driver no encuentra el elemento de inmediato, espera un tiempo máximo antes de lanzar la excepción.

        Desventaja: No es flexible; a veces se necesita esperar a que un elemento sea clickable o visible, no solo a que exista en el DOM. Combinar implícitas con explícitas puede causar comportamientos extraños.

    Esperas explícitas (la práctica recomendada por Selenium):
    Con WebDriverWait y ExpectedConditions se espera una condición concreta con un timeout dado.
    java

    WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    WebElement element = wait.until(ExpectedConditions.elementToBeClickable(By.id("submit")));
    element.click();

        Condiciones predefinidas: visibilityOf, presenceOfElementLocated, invisibilityOf, textToBe, etc.

        Permite ignorar excepciones específicas durante la espera.

        Son dinámicas: si la condición se cumple antes, la ejecución continúa.

    Esperas fluidas (FluentWait):
    Variante más configurable: se define el tiempo máximo, frecuencia de sondeo y qué excepciones ignorar. Útil cuando un elemento puede tardar debido a animaciones o peticiones AJAX.

Principio del SDET: Las esperas explícitas encapsuladas dentro de los Page Objects garantizan robustez y ocultan la complejidad.