# Despliegue en Vercel

**Vercel** es la plataforma creada por los desarrolladores de Next.js y ofrece la integración más profunda y optimizada. Permite desplegar con un solo comando desde Git y habilita automáticamente características avanzadas como **ISR**, **Edge Functions** y análisis de rendimiento.

## Conexión con Repositorio Git (Recomendado)

La forma más sencilla de desplegar es conectando tu proveedor de Git (GitHub, GitLab, Bitbucket):

1.  **Importar Proyecto**: Crea un proyecto en `vercel.com` e importa tu repositorio.
2.  **Detección Automática**: Vercel identifica que es Next.js y configura los comandos de `build` y `output` por ti.
3.  **Variables de Entorno**: Configura tus secretos en el panel de control antes del primer despliegue.
4.  **Flujo Continuo**: Cada `push` a la rama principal dispara un despliegue de producción. Los PRs generan entornos de **Preview** automáticos.

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

## Características y Funcionalidades Integradas

### 1. Edge Functions y Middleware
Next.js en Vercel puede ejecutar middleware y Route Handlers en el borde global. Solo necesitas exportar `export const runtime = 'edge'`. Vercel despliega automáticamente en su red global de baja latencia.

### 2. ISR y Edge Cache
Las regeneraciones de página (ISR) se almacenan en la capa de caché de borde de Vercel, lo que asegura actualizaciones atómicas y baja latencia. Las revalidaciones por `revalidateTag` y `revalidatePath` funcionan instantáneamente sin configuración extra.

### 3. Dominios y Seguridad
*   **SSL Automático**: Vercel provee certificados SSL gestionados mediante Let's Encrypt de forma gratuita.
*   **Dominios Personalizados**: Añade cualquier dominio desde el dashboard; la configuración es sencilla y automática.
*   **Protección**: Puedes proteger entornos con autenticación o IP whitelist (en planes superiores).

### 4. Análisis y Monitoreo
*   **Web Vitals**: Análisis integrado de métricas de rendimiento real directamente en el dashboard.
*   **Runtime Logs**: Visualiza errores, tiempos de respuesta y eventos de revalidación en tiempo real.

---

## Configuración con `vercel.json`

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

---

## Consideraciones Técnicas y Límites

*   **Serverless Limits**: El tamaño máximo de una función serverless es de **50 MB** (comprimido). Evita dependencias excesivamente pesadas.
*   **Server Actions**: Funcionan de forma nativa sin configuración adicional.
*   **Next Export**: Si usas `output: 'export'`, Vercel servirá el proyecto como un sitio estático puro, desactivando las funciones del lado del servidor.
*   **Escalado Automático**: El plan Pro escala automáticamente según la demanda, eliminando la necesidad de administrar servidores.
*   **Duración de Funciones**: Puedes configurar `maxDuration` hasta 800 segundos en el plan Enterprise para procesos de fondo.

> [!TIP]
> Utiliza los entornos de **Preview** de Vercel para compartir versiones funcionales de tus ramas con otros desarrolladores o clientes antes de fusionar a la rama principal.

---

Vercel es la opción definitiva para quienes buscan la mejor experiencia de desarrollo y el máximo rendimiento con Next.js sin complicaciones de infraestructura.

---
[<- Anterior: next.config.js](next-config-js.md) | [Siguiente: Despliegue en Node.js ->](despliegue-node.md)