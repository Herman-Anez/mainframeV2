# Dockerizar una aplicación Next.js

Dockerizar permite empaquetar la aplicación con todas sus dependencias y desplegarla en cualquier entorno compatible con contenedores. La opción **standalone** de Next.js optimiza la imagen eliminando la necesidad de `node_modules` completos en la etapa final.

## Configurar `next.config.js` para Standalone

Para habilitar la optimización de salida, añade la siguiente configuración:

```javascript
// next.config.js
module.exports = {
  output: 'standalone',
}
```

> [!NOTE]
> Esta opción genera una carpeta `.next/standalone` que contiene solo el código necesario (servidor compilado y una copia mínima de dependencias), reduciendo drásticamente el tamaño de la imagen final.

---

## Dockerfile Multi-stage (Recomendado)

Utilizar múltiples etapas asegura que la imagen final sea lo más pequeña y segura posible.

```dockerfile
# Etapa 1: Instalación de dependencias
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

# Etapa 2: Construcción (Build)
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Etapa 3: Ejecución (Runner)
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
# Descomentar si usas telemetría: ENV NEXT_TELEMETRY_DISABLED=1

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
ENV PORT=3000

CMD ["node", "server.js"]
```

---

## Construcción y Ejecución

Para construir la imagen y lanzarla localmente:

```bash
# Construir la imagen
docker build -t mi-next-app .

# Ejecutar el contenedor
docker run -p 3000:3000 -e DATABASE_URL=... mi-next-app
```

> [!TIP]
> Usa un archivo `.dockerignore` para evitar copiar `node_modules`, `.git` y otros archivos innecesarios al contexto de Docker, lo que acelerará el proceso de construcción.

---

## Uso con Docker Compose

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
    volumes:
      - next-cache:/app/.next/cache

volumes:
  next-cache:
```

---

## Consideraciones con ISR y Persistencia

En entornos con múltiples contenedores (Kubernetes, Swarm), el **ISR** puede presentar inconsistencias ya que la caché reside localmente en cada instancia.

**Soluciones posibles:**
*   **Volúmenes Compartidos:** Montar un almacenamiento compartido (NFS/EFS) en `.next/cache`.
*   **Revalidación bajo demanda:** Notificar a todas las instancias mediante webhooks tras una mutación.
*   **Adaptadores de Caché:** Implementar un proveedor de caché externo (Redis) si la plataforma lo permite.

> [!IMPORTANT]
> Al usar el modo `standalone`, los archivos estáticos (`public` y `.next/static`) deben ser copiados manualmente en el Dockerfile, ya que el servidor compilado en `server.js` espera encontrarlos en su ubicación relativa pero no los incluye por defecto en el bundle comprimido.

---

Dockerizar con el modo standalone genera imágenes ligeras y eficientes, listas para ser desplegadas en cualquier orquestador de contenedores moderno.
