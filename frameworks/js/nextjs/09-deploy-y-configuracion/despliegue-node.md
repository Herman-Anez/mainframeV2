# Despliegue en Servidor Node.js

Cuando no utilizas un proveedor especializado como Vercel, puedes ejecutar Next.js en tu propio servidor Node.js. Esto te otorga control total sobre la infraestructura, pero requiere configuración adicional para entornos de producción.

## Construcción y Arranque

Para preparar la aplicación, ejecuta los siguientes comandos:

```bash
npm run build
npm start
```

> [!NOTE]
> `next start` inicia el servidor en modo producción en el puerto 3000 por defecto. Para cambiarlo, usa la variable de entorno `PORT`:
> `PORT=8000 npm start`

---

## Gestión de Procesos con PM2

Para garantizar que la aplicación se mantenga activa y se reinicie ante fallos, se recomienda el uso de **PM2**.

```bash
# Instalación global
npm install -g pm2

# Inicio de la aplicación
pm2 start npm --name "mi-app" -- start

# Guardar configuración para reinicios del sistema
pm2 save
pm2 startup
```

### Configuración con `ecosystem.config.js`

Permite una gestión más fina, incluyendo el modo cluster para aprovechar múltiples núcleos:

```javascript
module.exports = {
  apps: [{
    name: 'next-app',
    script: 'node_modules/.bin/next',
    args: 'start',
    instances: 'max', // Escala a todos los núcleos disponibles
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3000,
    },
  }],
}
```

---

## Configuración de Proxy Inverso (Nginx)

Es una mejor práctica colocar **Nginx** delante de Next.js para manejar SSL, compresión y servir archivos estáticos eficientemente.

```nginx
server {
    listen 443 ssl http2;
    server_name misitio.com;

    ssl_certificate /etc/letsencrypt/live/misitio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/misitio.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Caché de activos estáticos de Next.js
    location /_next/static {
        alias /ruta/a/tu/app/.next/static;
        expires 1y;
        access_log off;
    }
}
```

---

## Servicio del Sistema (Systemd)

En servidores Linux, puedes crear un servicio para gestionar el ciclo de vida de la aplicación.

**Archivo `/etc/systemd/system/nextjs.service`:**

```ini
[Unit]
Description=Next.js Production Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/next-app
ExecStart=/usr/bin/npm start
Restart=on-failure
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

**Comandos de activación:**
```bash
systemctl enable nextjs
systemctl start nextjs
```

---

## Servidor Personalizado (Custom Server)

Si necesitas lógica adicional (manejo de sesiones, websockets, subprocesos), puedes crear un servidor Express que importe el request handler de Next.js. 

> [!WARNING]
> Usar un servidor personalizado desactiva algunas optimizaciones automáticas de Next.js como la gestión de rutas de borde y ciertas capacidades de caché.

```typescript
// server.ts
import express from 'express'
import next from 'next'

const dev = process.env.NODE_ENV !== 'production'
const app = next({ dev })
const handle = app.getRequestHandler()

app.prepare().then(() => {
  const server = express()
  server.all('*', (req, res) => handle(req, res))
  server.listen(3000, () => {
    console.log('> Ready on http://localhost:3000')
  })
})
```

---

## Consideraciones de Rendimiento y Monitoreo

1.  **Modo Cluster**: Siempre usa el modo cluster (ya sea vía PM2 o el módulo `cluster` de Node) para aprovechar todos los núcleos del procesador.
2.  **Compresión**: Habilita `gzip` o `brotli` en Nginx (o mediante middleware como `compression` si usas un servidor custom) para reducir el tamaño de transferencia.
3.  **Caché de Estáticos**: Asegúrate de que Nginx sirva directamente la carpeta `.next/static` para liberar carga del servidor Node.js.
4.  **Monitoreo**: Utiliza herramientas como `pm2 monit`, Prometheus o Grafana para supervisar el consumo de recursos y la latencia.

> [!IMPORTANT]
> Al desplegar en tu propio servidor, eres responsable de la seguridad del sistema operativo, las actualizaciones de Node.js y la gestión de certificados SSL.

---

Desplegar en un servidor Node.js propio es la opción ideal para entornos corporativos o cuando se requiere una integración profunda con otros servicios del sistema.

---
[<- Anterior: Despliegue en Vercel](despliegue-vercel.md) | [Siguiente: Dockerizar Next.js ->](dockerizar.md)
