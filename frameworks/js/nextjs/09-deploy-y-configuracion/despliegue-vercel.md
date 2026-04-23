# Despliegue en Vercel

**Vercel** es la plataforma creada por los desarrolladores de Next.js y ofrece la integración más profunda y optimizada. Permite desplegar con un solo comando desde Git y habilita automáticamente características avanzadas como **ISR**, **Edge Functions** y análisis de rendimiento.

## Conexión con Repositorio Git (Recomendado)

La forma más sencilla de desplegar es conectando tu proveedor de Git (GitHub, GitLab, Bitbucket):

1.  **Importar Proyecto:** Crea un proyecto en vercel.com e importa tu repositorio.
2.  **Detección Automática:** Vercel identifica que es Next.js y configura los comandos de `build` y `output` por ti.
3.  **Variables de Entorno:** Configura tus secretos en el panel de control antes del primer despliegue.
4.  **Flujo Continuo:** Cada `push` a la rama principal dispara un despliegue de producción. Los PRs generan entornos de **Preview** automáticos.

---

## Despliegue con Vercel CLI

Si prefieres el control desde la terminal o necesitas despliegues desde un CI externo:

```bash
# Instalación
npm i -g vercel

# Despliegue inicial (Entorno de desarrollo/preview)
vercel

# Despliegue a producción
vercel --prod
```

---

## Configuración y Personalización

Aunque Next.js funciona "out of the box", puedes usar un archivo `vercel.json` para ajustes finos:

```json
{
  "functions": {
    "api/**/*.js": {
      "memory": 512,
      "maxDuration": 30
    }
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Custom-Header", "value": "my-value" }
      ]
    }
  ]
}
```

### Características Integradas:

*   **Edge Functions:** Al usar `export const runtime = 'edge'`, Vercel despliega tu código en su red global de baja latencia.
*   **ISR & Cache:** Las regeneraciones de página se almacenan en la capa de caché de borde de Vercel, garantizando actualizaciones atómicas y ultra rápidas.
*   **SSL Automático:** Vercel provee certificados SSL gestionados mediante Let's Encrypt de forma gratuita.
*   **Web Vitals:** Análisis integrado de métricas de rendimiento real directamente en el dashboard.

---

## Consideraciones Técnicas

*   **Serverless Limits:** El tamaño máximo de una función serverless es de **50 MB** (comprimido). Evita dependencias excesivamente pesadas.
*   **Server Actions:** Funcionan de forma nativa sin configuración adicional.
*   **Next Export:** Si usas `output: 'export'`, Vercel servirá el proyecto como un sitio estático puro, desactivando las funciones del lado del servidor.

> [!TIP]
> Utiliza los entornos de **Preview** de Vercel para compartir versiones funcionales de tus ramas con otros desarrolladores o clientes antes de fusionar a la rama principal.

---
### Edge Functions

Next.js en Vercel puede ejecutar middleware y Route Handlers en el borde global. Solo necesitas exportar export const runtime = 'edge'. Vercel despliega automáticamente en su red Edge.
ISR y Cache

El ISR se almacena en la capa de Edge Cache de Vercel, lo que asegura regeneraciones atómicas y baja latencia. No requiere configuración extra. Las revalidaciones por revalidateTag y revalidatePath funcionan instantáneamente.
Dominios personalizados y SSL

Desde el dashboard puedes añadir cualquier dominio; Vercel provee SSL automático con Let's Encrypt. También puedes proteger con autenticación o IP whitelist.
Análisis y logs

Vercel Analytics (Web Vitals) y Runtime Logs están integrados. Puedes ver errores, tiempo de respuesta, y métricas de experiencia de usuario.
Escalado automático

El plan Pro escala automáticamente según la demanda. No necesitas administrar servidores.
Consideraciones

    Si usas next export en Vercel, la exportación estática se sirve como sitio estático, sin serverless.

    Las Server Actions funcionan de forma nativa.

    El límite de tamaño de función serverless es 50 MB (comprimido), ten cuidado con dependencias muy pesadas.

    Puedes configurar funciones de fondo con maxDuration hasta 800 segundos (plan Enterprise).
    
Vercel es la opción definitiva para quienes buscan la mejor experiencia de desarrollo y el máximo rendimiento con Next.js sin complicaciones de infraestructura.