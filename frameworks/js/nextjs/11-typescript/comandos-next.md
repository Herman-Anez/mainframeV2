## Archivo: `12-cli-y-scripts/comandos-next.md`

CLI de Next.js y scripts personalizados

Next.js incluye una interfaz de línea de comandos (CLI) con múltiples comandos para desarrollo, construcción y análisis. También ofrece un conjunto de scripts que se integran en package.json.
Comandos principales de la CLI
Comando	Descripción
next dev	Inicia el servidor de desarrollo con Hot Module Replacement en localhost:3000.
next build	Compila la aplicación para producción (optimizada).
next start	Inicia el servidor en modo producción (requiere next build previo).
next lint	Ejecuta ESLint en los archivos del proyecto.
next telemetry	Habilita/deshabilita la telemetría (datos anónimos de uso a Vercel).
next info	Muestra información del entorno (útil para reportar bugs).
next dev
```bash
```
next dev [opciones]

Opciones comunes:

    -p, --port <puerto>: cambiar el puerto (por defecto 3000).

    -H, --hostname <host>: por defecto localhost. Usa 0.0.0.0 para exponer en red local.

    --turbo: usa Turbopack para compilaciones más rápidas (si está disponible).

Ejemplos:
```bash
```
next dev -p 4000
next dev --turbo

### next build
```bash
```
next build

Genera una carpeta .next con el bundle optimizado. Analiza las páginas y muestra si son estáticas ○, dinámicas λ, o requieren ISR. Es compatible con perfiles: next build --profile habilita el perfilador de Webpack/Turbopack.
next start
```bash
```
next start [opciones]

Similar a next dev en opciones de puerto y host. Inicia la aplicación en modo producción (después de next build). Ideal para pruebas locales de la build final.
next lint
```bash
```
next lint [opciones]

Ejecuta ESLint con la configuración base de Next.js. Opciones:

    --fix: corrige automáticamente errores.

    --dir <directorio>: limita el escaneo a un directorio.

    --file <archivo>: analiza un solo archivo.

Por defecto, el comando se configura en package.json como "lint": "next lint".
next telemetry
```bash
```
next telemetry [status/enable/disable]

Muestra el estado o modifica la telemetría. Los datos recopilados son anónimos y se limitan a características usadas, rendimiento de build, etc.
next info
```bash
```
next info

Imprime información relevante del entorno: versión de Next, Node, sistema operativo, configuraciones. Muy útil al abrir una issue en GitHub.
Scripts recomendados en package.json
```json
```
"scripts": {
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "lint": "next lint",
  "lint:fix": "next lint --fix",
  "type-check": "tsc --noEmit",
  "format": "prettier --write .",
  "test": "jest --watch",
  "test:ci": "jest --ci",
  "prepare": "husky install"
}

### create-next-app

Aunque no es parte de la CLI en sí, create-next-app es el generador oficial:
```bash
```
npx create-next-app@latest [nombre] [opciones]

Opciones interactivas: TypeScript, ESLint, Tailwind, src directory, App Router, import alias. También acepta flags:
```bash
```
npx create-next-app@latest --ts --tailwind --app mi-app

### Personalización avanzada

Puedes crear scripts personalizados que invoquen la Next.js CLI desde Node.js. Por ejemplo, un script que genere sitemaps después del build:
```js
// scripts/generate-sitemap.js
const { execSync } = require('child_process')
execSync('next build', { stdio: 'inherit' })
// luego generas el sitemap...
```

### Uso de next export (legado)

Hasta Next.js 13, next export era el comando para salida estática. Ahora se configura con output: 'export' y next build crea directamente la carpeta out.
Modo de depuración

Para depurar el servidor Next.js (con Node inspector), ejecuta:
```bash
```
NODE_OPTIONS='--inspect' next dev

Luego conecta el inspector de Chrome o VS Code.

La CLI de Next.js es concisa pero potente, y al combinarla con scripts personalizados puedes automatizar tareas de desarrollo y despliegue con facilidad.

Con estos archivos, has completado todo el temario hasta 12-cli-y-scripts. Si necesitas profundizar en algún punto o añadir algún otro módulo (por ejemplo, next-auth avanzado, etc.), estoy a tu disposición.
