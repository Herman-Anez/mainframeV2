# 🔍 Fiddler y Charles Proxy (Depuración de tráfico)

Como SDET, a menudo necesitas ver exactamente qué está pasando entre el cliente (navegador, móvil, script de automatización) y el servidor. Los proxies de depuración como Fiddler y Charles son herramientas imprescindibles.

---

## 🏗️ Funcionalidades comunes y uso en automatización

*   **Intercepción de tráfico HTTP/HTTPS:** Ambos se sitúan como intermediarios y registran todas las peticiones y respuestas, incluyendo cabeceras, cuerpos, códigos de estado y tiempos. Esto es vital cuando una prueba falla y necesitas saber si el frontend envió los datos incorrectos o el backend respondió con un error inesperado.
*   **Inspección de tráfico cifrado (MITM):** Para HTTPS, instalan un certificado raíz en el dispositivo/emulador/navegador y descifran el tráfico. Crucial para probar APIs con SSL/TLS.
*   **Modificación de peticiones/respuestas (Breakpoints y AutoResponder):**
    *   **Breakpoints:** Se puede pausar una petición antes de que salga y modificarla (cambiar un parámetro) o pausar la respuesta antes de que llegue al cliente y alterarla. Esto permite simular condiciones de error del servidor, inyección de datos o tiempos de respuesta lentos, sin cambiar el código del backend.
    *   **AutoResponder (Fiddler) / Map Local / Map Remote (Charles):** Redirige una petición a un archivo local o a otra URL. Así se puede reemplazar un script, una imagen o incluso una respuesta de API completa. El SDET usa esto para aislar el frontend y probar cómo responde la UI ante distintos mensajes del backend, o para saltar fases de autenticación.
*   **Simulación de latencia y ancho de banda:** Ambos permiten *throttling* de red (lentitud, pérdida de paquetes) para probar cómo se comporta la aplicación en condiciones de red adversas. Esto es especialmente útil en pruebas móviles.
*   **Composición de solicitudes (Fiddler Composer):** Permite construir manualmente peticiones HTTP y enviarlas, probando rápidamente sin necesidad de escribir un script completo.

---

## ⚖️ Fiddler vs Charles: diferencias relevantes

### Fiddler (Classic y Everywhere)
*   Originalmente para Windows (.NET); Fiddler Everywhere es multiplataforma.
*   Muy potente en entornos Windows, con un gran ecosistema de extensiones.
*   Puede actuar como proxy inverso y capturar tráfico de prácticamente cualquier aplicación que soporte proxy.
*   FiddlerScript (en Classic) permite automatizar reglas de modificación mediante JavaScript/C#.

### Charles Proxy
*   Nativo multiplataforma, muy popular en macOS.
*   Excelente soporte para depurar tráfico de dispositivos móviles (iOS y Android) mediante proxy WiFi.
*   Funciones como Map Remote y Rewrite son muy intuitivas.
*   Grabación de sesiones y exportación en varios formatos (HAR, etc.).

---

## 🚀 Integración en automatización

Aunque la automatización diaria no usa Fiddler/Charles directamente, el SDET los emplea durante el desarrollo y depuración de scripts. En pruebas de seguridad, se pueden configurar como proxy upstream de OWASP ZAP para análisis adicional. Las sesiones grabadas se pueden exportar como archivos `.har` y luego transformarlas en scripts de prueba con herramientas de generación, o simplemente documentar el comportamiento esperado.

### Ejemplo de uso para depurar un fallo en Selenium:
1.  Configurar el navegador de Selenium para usar el proxy (por ejemplo, `--proxy-server=127.0.0.1:8888`).
2.  Ejecutar la prueba que falla.
3.  En Charles, buscar la petición que retornó un código inesperado, inspeccionar su carga y comparar con la especificación.
4.  Usar **Rewrite** para modificar un parámetro y volver a ejecutar, confirmando la hipótesis.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [⬅️ Swagger / OpenAPI](swagger-OpenAPI.md) | [🏠 Inicio](../../index.md) | [Jira y TestRail ➡️](Jira-TestRail.md) |