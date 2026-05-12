# OWASP ZAP Automation

ZAP (Zed Attack Proxy) es un proxy de seguridad que permite realizar pruebas dinámicas (DAST) a aplicaciones web. Es gratuito y altamente automatizable.

## Modos de Funcionamiento

- **Proxy Pasivo**: Intercepta el tráfico mientras un navegador o script interactúa con la app; analiza las peticiones y respuestas buscando patrones de vulnerabilidades (ej. cabeceras de seguridad faltantes, cookies sin flag HttpOnly).
- **Active Scan**: Envía activamente payloads maliciosos (inyecciones SQL, XSS, etc.) a los endpoints descubiertos. 
- **Spider Tradicional / AJAX Spider**: Recorre la aplicación para descubrir URLs.

> [!CAUTION]
> El **Active Scan** requiere autorización porque modifica datos y puede ser agresivo con el servidor.

## Automatización con ZAP API

ZAP expone una API REST que puede ser controlada desde código (Python, Java) o desde scripts curl. Para CI/CD se usan imágenes Docker y comandos o wrappers.

### Opción 1: Docker y ZAP Baseline Scan

```bash
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://myapp.example.com -r report.html
```

- Baseline scan ejecuta spider y escaneo pasivo (sin modificar datos).
- Se obtiene un reporte HTML con alertas de riesgo.
- Si el numero de alertas excede un límite, el contenedor sale con error -> puerta de calidad.

### Opción 2: Full Scan (Activo) con Docker

```bash
docker run -t owasp/zap2docker-stable zap-full-scan.py -t https://myapp -r report.html
```

### Opción 3: Integración Programática con Java (Cliente ZAP)

Usando `zap-client` desde Maven, se puede iniciar ZAP, abrir la URL, lanzar spider, active scan y recuperar alertas, todo orquestado por un test JUnit que falla si aparecen alertas de nivel alto.

## Ejemplo con Python y la API

```python
import time
from zapv2 import ZAPv2

zap = ZAPv2(apikey='mykey', proxies={'http': 'http://localhost:8080'})
zap.urlopen('https://myapp.example.com')
spider_id = zap.spider.scan('https://myapp.example.com')
time.sleep(10) # esperar, sondeo
while int(zap.spider.status(spider_id)) < 100:
    pass
scan_id = zap.ascan.scan('https://myapp.example.com')
while int(zap.ascan.status(scan_id)) < 100:
    pass
alerts = zap.core.alerts()
high_risk = [a for a in alerts if a['risk'] == 'High']
assert len(high_risk) == 0, f'Se encontraron {len(high_risk)} alertas de alto riesgo'
```

## Buenas Prácticas SDET

- Incluir el **Baseline Scan** como paso obligatorio en cada PR que afecte a un servicio web.
- Generar reportes en formato HTML/XML y archivarlos como artefactos del build.
- Configurar el contexto de ZAP (autenticación, sesión) para escanear áreas protegidas, utilizando `zap-context.py` o definiendo el contexto vía API.
- Hacer que el escaneo pasivo sea muy rápido (pocos minutos) para no bloquear el pipeline; el activo se ejecuta en horarios nocturnos.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Pruebas SAST y DAST](./Pruebas-SAST-DAST.md) | [Home](../../../index.md) | [Módulo 06](../../06-Bases-Datos/index.md) |