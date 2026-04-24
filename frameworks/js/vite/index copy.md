01-fundamentos/01-que-es-vite.md

Contenido sugerido para tu archivo de apuntes:
Definición y filosofía

Vite (palabra francesa que significa “rápido”) es una herramienta de frontend tooling creada por Evan You (autor de Vue.js). Está diseñada para ofrecer una experiencia de desarrollo excepcionalmente rápida y una construcción optimizada para producción. A diferencia de herramientas como Webpack, Vite no empaqueta todo el código durante el desarrollo. En su lugar, aprovecha dos capacidades modernas:

    Módulos ES nativos (ESM) soportados por los navegadores.

    esbuild (motor de empaquetado ultrarrápido en Go) para pre-empaquetar dependencias.

    Rollup para la salida de producción.

Esto se traduce en:
Fase	En desarrollo	En producción
Servidor	Arranque en frío instantáneo	–
Transformación	Bajo demanda por archivo (Koa/Connect)	Bundle completo optimizado (Rollup)
Recarga	HMR (Hot Module Replacement) casi nativo	–
Velocidad	Sin empaquetado previo, arranque en ms	Tree-shaking, hashing, code splitting
¿Por qué es diferente?

Desarrollo tradicional (Webpack):
Todo el código fuente + dependencias → empaquetado en uno o varios bundles → servido. A medida que el proyecto crece, la reconstrucción puede llevar decenas de segundos.

Enfoque de Vite:

    Dependencias pre-empaquetadas una sola vez con esbuild (en milisegundos) y cacheadas.

    Código fuente servido directamente como ESM. El navegador solicita los archivos según sus import. Vite solo transforma el archivo solicitado (ej: .vue, .ts, .scss) en el momento.

Arquitectura simplificada
text

[Navegador] ← HTTP ESM → [Servidor de desarrollo Vite]
                                |
                         [Pre-bundling: node_modules/.vite]
                                |
        Transformaciones bajo demanda (plugins oficiales/comunitarios)
                                |
                         [HMR WebSocket]

Un vistazo rápido

Crea un index.html que apunte directamente a main.js:
html

<!DOCTYPE html>
<html>
<head><title>Mi app</title></head>
<body>
  <div id="app"></div>
  <script type="module" src="/main.js"></script>
</body>
</html>

En main.js puedes importar estilos, frameworks, json:
js

import './style.css'
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')

Corre npx vite y verás todo funcionando sin ninguna configuración adicional.
Compatibilidad

Vite exige navegadores que soporten ESM dinámico. Durante el desarrollo eso está cubierto (Chrome, Firefox, Edge, Safari modernos). Para producción, el bundle es compatible con todos los navegadores objetivo que definas.
01-fundamentos/02-primeros-pasos.md

Configuración manual sin create-vite (para entender lo mínimo)
1. Crear la estructura
bash

mkdir mi-proyecto-vite && cd mi-proyecto-vite
npm init -y

Instala Vite como dependencia de desarrollo:
bash

npm install -D vite

2. Archivos fuente

Crea estos tres archivos:

index.html (en la raíz del proyecto, Vite lo toma como punto de entrada):
html

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vite desde cero</title>
</head>
<body>
  <h1>Vite funciona</h1>
  <script type="module" src="/src/main.js"></script>
</body>
</html>

src/main.js:
js

import './style.css'

document.querySelector('h1').textContent = '¡Hola Vite!'

src/style.css:
css

body {
  background: #1a1a1a;
  color: #f0f0f0;
  font-family: system-ui;
}

3. Scripts en package.json
json

{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}

4. Ejecutar

    Desarrollo: npm run dev → por defecto en http://localhost:5173
    Cambia un archivo y el navegador se actualizará al instante.

    Build: npm run build → salida optimizada en dist/

    Preview: npm run preview → sirve localmente la carpeta dist para probarla.

Directorio público

Crea una carpeta public en la raíz. Cualquier archivo ahí (como favicon.ico o imágenes) se sirve sin transformación y se copia a la raíz de dist.
Personalizar la configuración

Crea vite.config.js:
js

import { defineConfig } from 'vite'

export default defineConfig({
  base: '/mi-app/',         // si despliegas en subdirectorio
  server: {
    port: 4000,
    open: true              // abre navegador automáticamente
  },
  build: {
    outDir: 'construido'    // cambia carpeta de salida
  }
})

Resolución de ESM en el navegador

Vite no requiere que empaquetes ningún módulo. El index.html es el punto de partida. El navegador lee el script type="module", descarga /src/main.js y luego sus dependencias (CSS, etc.). Vite intercepta cada petición y la transforma al vuelo si hace falta.
01-fundamentos/03-create-vite.md
Andamio interactivo

Vite proporciona un generador oficial que ahorra la configuración manual. Ejecutar:
bash

npm create vite@latest

Te preguntará:

    Nombre del proyecto.

    Framework (vanilla, vue, react, preact, lit, svelte, solid, qwik, otros).

    Variante (JavaScript, TypeScript, con SWC, etc.).

Luego, instala dependencias y ya puedes empezar con npm run dev.
Comando abreviado

Puedes especificar todo en línea:
bash

npm create vite@latest mi-app -- --template vue-ts

Lista de plantillas oficiales
Framework	JavaScript	TypeScript
vanilla	vanilla	vanilla-ts
vue	vue	vue-ts
react	react	react-ts
react-swc	react-swc	react-swc-ts
preact	preact	preact-ts
lit	lit	lit-ts
svelte	svelte	svelte-ts
solid	solid	solid-ts
qwik	qwik	qwik-ts
¿Qué incluye una plantilla oficial?

Para vanilla (JavaScript puro):
text

mi-app/
├── index.html
├── package.json
├── public/
│   └── vite.svg
├── src/
│   ├── counter.js
│   ├── javascript.svg
│   ├── main.js
│   └── style.css
└── vite.config.js (solo con plugins si hay)

Ya viene con un contador de ejemplo, estilos y estructura lista para modificar.
Plantillas comunitarias

Además de las oficiales, existen plantillas mantenidas por la comunidad. Para usarlas se especifica el prefijo community/:
bash

npm create vite@latest mi-proyecto -- --template community/electron

Detrás de escena

create-vite básicamente:

    Copia una estructura de archivos según la plantilla.

    Inicializa package.json con las dependencias correctas (vite, plugin del framework, typescript si aplica).

    No ejecuta npm install (te lo sugiere al final).

    Genera un vite.config.js mínimo, por ejemplo:
    js

    import { defineConfig } from 'vite'
    import vue from '@vitejs/plugin-vue'

    export default defineConfig({
      plugins: [vue()]
    })

Esto lo deja listo para desarrollo.
02-desarrollo/01-servidor-de-desarrollo.md
Arranque y peticiones bajo demanda

Cuando ejecutas vite (o npm run dev):

    Vite inicia un servidor HTTP basado en Connect (similar a Express).

    Lee tu index.html y lo sirve.

    El navegador solicita /src/main.js.

    Vite inspecciona el archivo; si es un .js estándar lo sirve tal cual (a menos que necesite transformación, como JSX o Vue SFC).

    Si el archivo importa dependencias de node_modules (ej: import { ref } from 'vue'), Vite redirige esas peticiones a un directorio especial node_modules/.vite/deps/ donde ya se encuentran pre-empaquetadas y cacheadas.

    Si el archivo importa un recurso como CSS, Vite lo transforma añadiendo un código que inyecta el CSS en el DOM, y además envía actualizaciones HMR cuando cambie.

Configuración del servidor (server)

En vite.config.js:
js

import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    host: '0.0.0.0',    // escucha en todas las interfaces (útil en red local)
    port: 3000,
    strictPort: true,    // falla si el puerto está ocupado (no busca otro)
    open: '/docs',       // abre navegador en ruta específica
    https: {
      key: fs.readFileSync('./certs/localhost-key.pem'),
      cert: fs.readFileSync('./certs/localhost.pem'),
    },
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    },
    cors: true,           // habilita CORS
    headers: {
      'X-Custom-Header': 'vite'
    }
  }
})

Transformaciones en vivo

El servidor usa internamente los plugins de Vite. Por ejemplo, cuando pides un archivo .vue, el plugin @vitejs/plugin-vue lo compila a JavaScript, separando template, script y estilo. Para SCSS, instala sass y sass-loader no es necesario; Vite lo maneja con el preprocesador nativo.
Pipeline de peticiones

Cada petición que llega al servidor sigue este flujo:

    Resolución: Vite localiza el archivo real (teniendo en cuenta alias, extensiones, main de package.json).

    Transformación central: pasa el contenido por todos los plugins que implementan transform.

    Resultado: se envía código JavaScript válido (o CSS inyectado). Los sourcemaps se generan automáticamente.

Hot Module Replacement

El servidor maneja un WebSocket paralelo. Cuando un archivo editado llega (gracias a chokidar), Vite invalida la caché de ese módulo y notifica al frontend para que reemplace el módulo sin recargar toda la página. Veremos esto a fondo en el siguiente apartado.
Caché agresiva

Los módulos servidos incluyen cabeceras de caché fuertes (Cache-Control: max-age=31536000, immutable) ya que todos los recursos en desarrollo se sirven con un ?t=timestamp que los hace únicos si cambian.
02-desarrollo/02-hmr.md
¿Qué es HMR y por qué es importante?

Hot Module Replacement (reemplazo de módulos en caliente) permite que, al guardar un archivo, los módulos modificados se actualicen directamente en el navegador sin perder el estado local (datos en formularios, store de Vuex/Pinia, estado de React). El refresco completo de la página, por el contrario, resetea todo.

Vite logra HMR sobre el protocolo WebSocket y la API estándar import.meta.hot (heredada de Rollup/Webpack pero optimizada para ESM).
Flujo de trabajo

    El servidor de Vite vigila los archivos con chokidar.

    Al detectar un cambio, determina qué módulo del grafo debe actualizarse.

    Envía un mensaje WebSocket al cliente (el código inyectado en la página) con la información del módulo.

    El cliente recibe el nuevo código y, usando import.meta.hot.accept(), reemplaza el módulo en caliente.

    Si el módulo no puede autoaceptar (porque no tiene accept, caso típico de una hoja de estilos o de componentes de framework), el recambio se propaga hacia arriba hasta que encuentra un límite HMR o, en último caso, hace un full-reload.

La API Básica

Tu módulo puede participar en HMR agregando:
js

// main.js o cualquier módulo
import.meta.hot.accept(newModule => {
  // (opcional) callback para cuando el módulo se actualiza
  console.log('Módulo actualizado')
})

import.meta.hot.dispose(() => {
  // limpiar listeners, timers, etc.
})

Recarga de estilo sin recargar la página:
Un CSS importado no necesita nada: Vite automáticamente inyecta un código que actualiza el <style> correspondiente en el DOM sin intervención del desarrollador.
Ejemplo: Contador con estado preservado

src/counter.js:
js

export function setupCounter(element) {
  let count = 0
  const setCounter = (c) => { count = c; element.innerHTML = `cuenta es ${count}` }
  element.addEventListener('click', () => setCounter(count + 1))
  setCounter(0)
}

// permitir HMR para preservar estado
if (import.meta.hot) {
  import.meta.hot.accept(() => {
    // no hacemos nada; el contador se reemplazaría pero perderíamos el estado real.
    // Normalmente, los frameworks manejan esto internamente.
  })
}

Para preservar estado realmente, se puede usar import.meta.hot.data para almacenar el estado y rehidratarlo tras la actualización.
HMR en frameworks (cómo funciona realmente)

    Vue: @vitejs/plugin-vue genera código que permite HMR por componentes, preservando data/computed, sin necesidad de configuración extra.

    React: @vitejs/plugin-react usa React Fast Refresh (gracias a Babel o SWC), manteniendo el estado local de hooks.

    Svelte: El plugin de Svelte integra HMR para preservar el estado de los stores y componentes.

En todos los casos, el desarrollador no tiene que añadir nada; Vite y el plugin oficial se encargan.
Límites de HMR (boundaries)

Un módulo que acepta import.meta.hot.accept() (o sin argumentos) es un “límite de HMR”. La actualización no se propaga a sus padres. Los componentes de los frameworks suelen ser límites naturales. Si un archivo no es aceptado, la actualización sube hasta el módulo raíz y, si tampoco es aceptada, se fuerza una recarga completa.
02-desarrollo/03-pre-bundling.md
El problema de las dependencias

En un proyecto típico, node_modules contiene cientos o miles de archivos. Sin pre-bundling, cada import de esas librerías generaría una petición HTTP por módulo, colapsando el navegador (por ejemplo, la librería lodash tendría una petición por función). Además, muchas dependencias usan formatos CommonJS (require/module.exports) que el navegador no entiende.

Vite soluciona esto pre-empaquetando esas dependencias durante el primer arranque del servidor de desarrollo.
Cómo funciona

    Durante la primera solicitud al dev server, Vite analiza tus imports de node_modules.

    Utiliza esbuild (escrito en Go y 10-100x más rápido que alternativas en JavaScript) para convertir esas dependencias a ESM y agruparlas en pocos archivos.

    Guarda el resultado en node_modules/.vite/deps/.

    La próxima ejecución, si el package-lock.json no cambió, reutiliza la caché, haciendo el arranque prácticamente instantáneo.

Los archivos generados llevan un hash de su contenido y se sirven con cabeceras de caché fuerte.
Ejemplo de transformación

Imagina que tu código hace esto:
js

import { map } from 'lodash-es' // ESM nativo, muchas sub-imports
import axios from 'axios'        // CJS

Vite convertirá axios (CJS) a un módulo ESM, y agrupará las partes de lodash-es en uno o pocos chunks, evitando cientos de peticiones.
Configuración de optimizeDeps

En vite.config.js puedes personalizar el pre-bundling:
js

export default defineConfig({
  optimizeDeps: {
    include: ['my-legacy-cjs-lib', 'some-esm-lib'],
    exclude: ['huge-lib-i-want-as-separate-chunks'],
    esbuildOptions: {
      target: 'es2020',
      define: { global: 'globalThis' }
    },
    force: true  // fuerza re-pre-bundling en cada inicio (debug)
  }
})

include: Fuerza a que ciertas dependencias sean pre-empaquetadas, aunque Vite no las hubiera detectado (útil si se importan dinámicamente o en workers).

exclude: Excluye dependencias que ya están en ESM válido con muchas subimportaciones que deseas conservar como peticiones separadas (pero cuidado con la cascada de requests).
Pre-bundling de dependencias en construcción (vite build)

En producción, Rollup empaqueta todo. El pre-bundling es exclusivo del modo desarrollo, pero puede ser necesario para dependencias que no se pueden resolver con plugins de Rollup. Para ello, Vite ofrece build.commonjsOptions que usa @rollup/plugin-commonjs.
Interferencias y solución de problemas

A veces una dependencia tiene efectos secundarios al ser evaluada (ej: polyfills). Durante el pre-bundling esos efectos se ejecutan, pero podrían no repetirse si el archivo se carga tarde. Para eso, puedes marcar la dependencia como optimizeDeps.include y, si aún falla, ajustar esbuildOptions. Además, Vite analiza los efectos secundarios usando sideEffects del package.json.
Relación con el caché en disco

La carpeta node_modules/.vite contiene dos subdirectorios:

    deps: los chunks pre-empaquetados.

    cache: transformaciones de archivos fuente cacheadas para acelerar HMR.

Puedes borrarla seguramente con rm -rf node_modules/.vite si hay problemas de caché.
02-desarrollo/04-variables-entorno.md
Archivos .env y modos

Vite usa dotenv para cargar variables de entorno desde archivos especiales en la raíz del proyecto:

    .env — cargado en todos los modos.

    .env.local — sobreescrituras locales (no debe ir a git).

    .env.[mode] — cargado solo en ese modo (ej: .env.production, .env.staging).

    .env.[mode].local — local específico del modo.

Prioridad de carga

Las variables en archivos con .local tienen mayor prioridad que sus correspondientes sin local. El orden de menor a mayor prioridad es:
.env < .env.local < .env.[mode] < .env.[mode].local
Prefijo VITE_

Solo las variables que comienzan con VITE_ son expuestas al código del cliente (en import.meta.env). Esto evita filtraciones accidentales de secretos de servidor.

Ejemplo:
.env.development:
text

VITE_API_URL=http://localhost:3001/api
VITE_APP_TITLE=MiApp Dev
DB_PASSWORD=secreto  # NO se expone al cliente

En tu código:
js

console.log(import.meta.env.VITE_API_URL)   // 'http://localhost:3001/api'
console.log(import.meta.env.DB_PASSWORD)    // undefined

Objeto import.meta.env

Incluye además propiedades incorporadas:

    import.meta.env.MODE: string con el modo ('development', 'production', etc.)

    import.meta.env.BASE_URL: la base configurada (útil para assets)

    import.meta.env.PROD: booleano si es producción

    import.meta.env.DEV: booleano si es desarrollo

    import.meta.env.SSR: booleano si se ejecuta en servidor SSR

Uso en configuración de Vite

Para acceder a variables de entorno en vite.config.js (ejemplo: inyectar un encabezado en el proxy), usa loadEnv:
js

import { defineConfig, loadEnv } from 'vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  return {
    server: {
      proxy: {
        '/api': {
          target: env.API_SERVER_URL, // nota: no necesita VITE_ aquí
          changeOrigin: true
        }
      }
    },
    define: {
      // Puedes exponer variables fijas a cliente sin VITE_ usando define
      __BUILD_TIME__: JSON.stringify(new Date().toISOString())
    }
  }
})

Variables en el build

Durante vite build, las variables de entorno se reemplazan estáticamente en el código. Si cambias la variable de entorno entre builds, necesitas reconstruir. Esto permite tree-shaking de código condicional como:
js

if (import.meta.env.PROD) {
  // este código solo existe en producción
}

Modos personalizados

Puedes crear un modo arbitrario (por ejemplo, staging) y un archivo .env.staging. Luego ejecutas:
bash

npx vite build --mode staging

Las variables de ese archivo serán inyectadas. import.meta.env.MODE será 'staging'.
Seguridad

Nunca pongas secretos (claves API privadas) en variables con prefijo VITE_. Cualquier dato en el bundle es público. Para secretos, usa un backend o un proxy que inyecte las variables en tiempo de ejecución (mediante un endpoint /config dinámico, por ejemplo).
02-desarrollo/05-import-meta-glob.md
¿Qué es el import glob?

import.meta.glob es una función especial que Vite reconoce y transforma en tiempo de compilación. Permite importar muchos módulos con un patrón glob similar a los de shell. Es como un import múltiple y dinámico pero resuelto estáticamente, sin necesidad de un loader custom en Rollup/Webpack.
Sintaxis básica

Hay dos variantes:

    import.meta.glob(pattern, options): devuelve un objeto cuyos valores son promesas perezosas (cada módulo se carga bajo demanda).

    import.meta.glob(pattern, { eager: true }): devuelve un objeto con todos los módulos importados directamente (síncrono, útil para listados estáticos pero puede aumentar el tamaño del bundle).

Patrón de ejemplo

Supón que tienes una carpeta de componentes:
text

src/
  components/
    Button.vue
    Input.vue
    Card.vue

Puedes dinámicamente importarlos:
js

const modules = import.meta.glob('./components/*.vue')

// modules es: { './components/Button.vue': () => import('./components/Button.vue'), ... }

for (const path in modules) {
  modules[path]().then(mod => {
    console.log(path, mod.default)
  })
}

Opciones

El segundo parámetro es un objeto con:

    eager: true para importación directa.

    import: 'default' para importar solo la exportación por defecto, o una cadena con nombre específico.

    query: añade parámetros a la solicitud, por ejemplo ?raw.

Ejemplos prácticos

Importar todas las imágenes de una carpeta como URLs:
js

const imageModules = import.meta.glob('../assets/images/*.{png,jpg,svg}', {
  eager: true,
  import: 'default',
  query: '?url'
})
// imageModules es un objeto { ruta: url }

Cargar archivos markdown y extraer metadata (ej: para un blog):
js

const posts = import.meta.glob('./posts/*.md', { eager: true, import: 'default' })
// posts = { './posts/intro.md': contenido, ... }

Combinar con frontmatter: necesitarías un plugin de Vite que soporte .md. Por ejemplo, con vite-plugin-markdown:
js

const postsMetadata = import.meta.glob('./posts/*.md', {
  eager: true,
  import: 'metadata' // si el plugin exporta metadata
})

¿Cómo funciona internamente?

Durante el desarrollo, Vite intercepta el patrón y genera un código similar a:
js

const modules = {
  './Button.vue': () => import('/src/components/Button.vue?t=1234'),
  ...
}

En producción, Rollup transforma esto en un código que realiza code-splitting automático y genera chunks por cada archivo, permitiendo carga perezosa real.
Casos de uso típicos

    Catálogos de componentes (como Storybook sin necesidad de más configuración).

    Internacionalización (i18n): cargar todos los archivos JSON de traducciones de un directorio.

    Documentación: importar todos los .vue de una carpeta para generar una galería.

    Iconos: importar todos los SVG de una carpeta.

Cuidado con el tamaño del bundle

eager: true incluirá todos los módulos en el bundle principal, lo que puede ser contraproducente. Usa la versión perezosa (import.meta.glob sin eager) si los módulos se consumen bajo demanda (ej: rutas dinámicas). Así cada uno se convierte en un chunk separado.
import.meta.globEager (obsoleto)

En versiones anteriores de Vite existía import.meta.globEager. Está deprecado en favor de import.meta.glob(..., { eager: true }). Si encuentras código antiguo, actualízalo.

Con estos apuntes tienes una base sólida de los fundamentos y el entorno de desarrollo de Vite. Si quieres que profundice en los siguientes bloques (03-configuracion, 04-plugins, etc.), solo tienes que pedírmelo.

03-configuración / 01-vite-config.md
El archivo vite.config.js (o .ts)

Vite busca automáticamente vite.config.js, vite.config.ts, etc. en la raíz. Se recomienda usar defineConfig para tener autocompletado y validación:
js

import { defineConfig } from 'vite'

export default defineConfig({
  // opciones globales
})

Puede exportar una función si necesitas acceso al modo o variables de entorno:
js

export default defineConfig(({ command, mode }) => {
  // command: 'serve' | 'build'
  // mode: 'development' | 'production' | custom
  return {
    // configuración
  }
})

Principales secciones de configuración

    root: directorio raíz del proyecto (por defecto process.cwd()). El index.html se busca aquí o en public.

    base: ruta pública base (útil para desplegar en subdirectorios). Por ejemplo '/miapp/'. Afecta a los enlaces de assets.

    publicDir: carpeta de activos estáticos (por defecto 'public'). Si quieres desactivarla, pon false.

    server: configuración del servidor de desarrollo.

    build: configuración de producción (Rollup).

    plugins: array de plugins.

    resolve: alias y extensiones.

    css: opciones de CSS (módulos, preprocesadores, PostCSS).

    optimizeDeps: pre-bundling.

    envPrefix: prefijo de variables de entorno expuestas (por defecto VITE_).

Referencia completa rápida
js

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  root: '.',               // directorio raíz
  base: '/',
  publicDir: 'public',
  plugins: [vue()],
  server: {
    host: true,
    port: 5173
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'esbuild',
    target: 'es2015'
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  },
  css: {
    modules: { /* ... */ },
    preprocessorOptions: { /* ... */ }
  },
  optimizeDeps: {
    include: [],
    exclude: []
  },
  envPrefix: 'VITE_'
})

03-configuración / 02-resolve-alias.md
Alias de rutas

En resolve.alias puedes mapear prefijos a directorios, simplificando los imports:
js

export default defineConfig({
  resolve: {
    alias: {
      '@': '/src',
      '@components': '/src/components',
      '@utils': '/src/utils',
      '@data': '/src/data'
    }
  }
})

Así, en lugar de '../../components/Button.vue' puedes usar '@components/Button.vue'.

Con TypeScript: debes reflejar los alias en tsconfig.json para que el editor no marque errores:
json

{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"]
    }
  }
}

Extensiones que se resuelven automáticamente

Por defecto Vite resuelve extensiones: .js, .ts, .vue, .jsx, .tsx, .json, .mjs, .cjs. Puedes personalizar:
js

resolve: {
  extensions: ['.web.ts', '.web.tsx', '.ts', '.tsx', '.vue', '.js']
}

Otras opciones de resolve

    dedupe: lista de dependencias para que siempre resuelvan a la misma copia (útil en monorepos). Ej: dedupe: ['vue'].

    preserveSymlinks: por defecto resuelve paths reales (false). Si usas symlinks y quieres mantenerlos, pon true.

03-configuración / 03-optimize-deps.md

(Profundización adicional a lo visto en 02-desarrollo/03-pre-bundling.md)
Estrategia de caché y reconstrucción

Los resultados del pre-bundling se almacenan en node_modules/.vite/deps/ con un hash que depende de la lista de dependencias y sus versiones. Si package.lock o package.json no cambian, se reutiliza. Puedes forzar la reconstrucción con:
bash

npx vite --force

O en la config:
js

optimizeDeps: {
  force: true
}

Optimización de dependencias con efectos secundarios

Algunas librerías (polyfills, @firebase/app) necesitan ejecutar código al iniciar. El pre-bundling las agrupa, pero podría romper el orden de efectos. Para asegurar que se incluyan correctamente, añádelas a include y, si es necesario, márcalas como no “side effects” en el package.json del proyecto o usa esbuildOptions:
js

optimizeDeps: {
  include: ['@firebase/app', 'global-polyfill'],
  esbuildOptions: {
    target: 'es2020',
    define: { global: 'globalThis' }
  }
}

Excluir dependencias del pre-bundling

Puedes excluir grandes librerías que ya son ESM válidas y cuyos miles de subimports no quieras convertir en un solo chunk. Por ejemplo, three:
js

optimizeDeps: {
  exclude: ['three']
}

Así cada subimport de Three será una petición separada en desarrollo. En producción Rollup manejará el tree-shaking.
Opciones de optimizeDeps
Propiedad	Descripción
include	Array de strings (dependencias a forzar en el pre-bundling)
exclude	Array de dependencias a omitir
needsInterop	Dependencias que requieren interoperabilidad CJS/ESM
esbuildOptions	Pasar opciones directamente a esbuild
extensions	Extensiones de archivo a considerar como dependencias (por defecto .js, .cjs, .mjs)
Depuración

Si ves errores como Failed to resolve entry for package..., revisa que el package.json de la librería tenga un campo "module" o "exports" válido. Puedes usar optimizeDeps.include para forzarla y también configurar resolve.mainFields.
03-configuración / 04-modos-y-env.md

(Ampliación más allá de lo básico cubierto en 02-desarrollo/04-variables-entorno.md)
Modos personalizados y archivos .env

El modo se determina con --mode. Por defecto, vite => development, vite build => production. Puedes crear, por ejemplo, .env.staging y ejecutar:
bash

npx vite build --mode staging

Dentro de la configuración, el modo está disponible en la función:
js

export default defineConfig(({ mode }) => {
  console.log(`Construyendo para modo: ${mode}`)
})

Prefijo de variables de entorno (envPrefix)

Por defecto solo las variables que comienzan con VITE_ se exponen a import.meta.env. Puedes cambiarlo:
js

export default defineConfig({
  envPrefix: 'APP_'
})

Ahora APP_API_URL será expuesta, pero VITE_SECRET ya no (a menos que también incluyas VITE_). Se puede pasar un array: envPrefix: ['VITE_', 'APP_'].
Variables en HTML

Dentro del index.html puedes usar variables de entorno con el mismo prefijo:
html

<title>%VITE_APP_TITLE%</title>

Se reemplazan durante el build.
Uso seguro de variables

    Nunca expongas secretos (claves privadas de API, tokens de servicio). Todo lo que se inyecta en el bundle es público.

    Para secretos dinámicos, crea un endpoint en tu backend que devuelva configuraciones bajo autenticación.

    Usa define para constantes de compilación (no variables de entorno) si no necesitan cambiar por modo:

js

define: {
  __VERSION__: JSON.stringify(package.version)
}

.env.production y variables en el build

En producción, las variables se reemplazan estáticamente. Puedes comprobar si la app corre en producción con import.meta.env.PROD. Esto ayuda a tree-shaking:
js

if (import.meta.env.PROD) {
  // código solo para producción
} else {
  // código solo para desarrollo
}

04-plugins / 01-introduccion-plugins.md
La API de Plugins de Vite

Vite utiliza los hooks de Rollup ampliados con propiedades específicas para el servidor. Un plugin es un objeto con:

    name: nombre del plugin.

    config: modifica la configuración de Vite.

    configResolved: configuración ya resuelta.

    configureServer(server): acceso al servidor de desarrollo para añadir middlewares.

    transformIndexHtml(html): transformación del HTML.

    transform(code, id): transforma módulos fuente (similar a Rollup, pero con soporte adicional).

    resolveId, load: hooks para módulos virtuales.

    handleHotUpdate(ctx): control personalizado del HMR.

    Etc.

Flujo típico de un plugin
js

// mi-plugin.js
export default function miPlugin(opciones) {
  return {
    name: 'mi-plugin',
    // inyectar datos globales
    config(config, { command }) {
      if (command === 'serve') {
        config.define = { __DEV__: true }
      }
    },
    // módulo virtual
    resolveId(id) {
      if (id === 'virtual:mensaje') return '\0virtual:mensaje'
    },
    load(id) {
      if (id === '\0virtual:mensaje') return `export default "¡Hola desde virtual!"`
    },
    // transformar código
    transform(code, id) {
      if (id.endsWith('.txt')) {
        return `export default ${JSON.stringify(code)}`
      }
    },
    // personalizar HMR
    handleHotUpdate({ file, server }) {
      if (file.endsWith('.custom')) {
        // enviamos evento personalizado
        server.ws.send({ type: 'custom', path: file })
        return [] // para prevenir recarga completa
      }
    }
  }
}

Se usa en vite.config.js:
js

import miPlugin from './mi-plugin.js'

export default defineConfig({
  plugins: [miPlugin({ debug: true })]
})

Orden y preprocesamiento

Los plugins se ejecutan en orden. Vite ejecuta enforce: 'pre' antes de los plugins normales y enforce: 'post' después:
js

{
  name: 'mi-pre',
  enforce: 'pre',
  transform(code, id) { /* ... */ }
}

04-plugins / 02-plugin-vue.md
@vitejs/plugin-vue

Plugin oficial para Vue 3. Soporta Single File Components (SFC), HMR y configuración del compilador.

Instalación:
bash

npm install -D @vitejs/plugin-vue

Uso mínimo:
js

import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()]
})

Opciones destacadas

    include / exclude: filtros para archivos que se tratarán como Vue SFC (por defecto .vue).

    reactivityTransform (obsoleto en Vue 3.4): transformación $ref y $computed, ahora se recomienda 'script setup' con ref normal.

    template.compilerOptions: opciones del compilador de plantillas. Por ejemplo:

js

vue({
  template: {
    compilerOptions: {
      isCustomElement: (tag) => tag.startsWith('ion-') // soporte para componentes personalizados
    }
  }
})

    customElement: habilitar compilación para Web Components con Vue (true o patrón).

    ssr: configuración para SSR (build).

HMR con Vue

El plugin inyecta código para que los componentes acepten HMR. Conserva el estado usando __VUE_HMR_RUNTIME__. No requiere configuración adicional; si editas <script> o <style>, el componente se actualiza sin perder los datos.
Preprocesadores en SFC

Dentro de <style lang="scss">, Vite usa el compilador de Sass instalado. No necesitas configurar nada extra si tienes sass en devDependencies.
04-plugins / 03-plugin-react.md
@vitejs/plugin-react

Plugin oficial para React. Aprovecha React Fast Refresh para HMR con preservación del estado de hooks.

Instalación:
bash

npm install -D @vitejs/plugin-react

Uso:
js

import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()]
})

Opciones

    include / exclude: archivos que se transformarán.

    jsxImportSource: por defecto 'react', puedes cambiarlo a 'preact' si usas Preact.

    babel: opciones para Babel (si quieres plugins específicos). Normalmente Vite usa esbuild para transpilar JSX, pero el plugin React usa Babel (o SWC) para el Fast Refresh.

Desde Vite 5, puedes usar el plugin con SWC (@vitejs/plugin-react-swc), más rápido que Babel. Se instala y se usa igual:
bash

npm install -D @vitejs/plugin-react-swc

js

import react from '@vitejs/plugin-react-swc'

React Fast Refresh

Mantiene el estado de los componentes durante ediciones en el código. El plugin lo configura automáticamente. Si tienes un componente con useState y editas su JSX, verás el cambio sin perder el estado.
Configuración de jsx-runtime

Vite permite usar la nueva transformación JSX automática. No necesitas import React from 'react'. Asegúrate de que tu tsconfig.json tenga "jsx": "react-jsx". El plugin respeta esa configuración.
04-plugins / 04-plugin-personalizado.md
Creación de un plugin completo

Vamos a construir un plugin que:

    Crea un módulo virtual virtual:build-info que exporte la fecha de construcción.

    Transforma archivos .md a componentes Vue/React sencillos (sólo como ejemplo).

    Añade un endpoint al servidor de desarrollo.

js

// plugins/mi-plugin.js
import { createHash } from 'node:crypto'

export default function miPlugin(opciones = {}) {
  let base = '/'
  let mode = ''

  return {
    name: 'mi-plugin',

    config(config, env) {
      base = config.base || '/'
      mode = env.mode
    },

    resolveId(id) {
      if (id === 'virtual:build-info') return '\0virtual:build-info'
    },

    load(id) {
      if (id === '\0virtual:build-info') {
        const info = {
          time: new Date().toISOString(),
          mode
        }
        return `export default ${JSON.stringify(info)}`
      }
    },

    transform(code, id) {
      if (id.endsWith('.md')) {
        // transformación simplificada: convertir markdown a string
        const content = JSON.stringify(code.trim())
        return `export default ${content}`
      }
    },

    configureServer(server) {
      // endpoint: /__build-info
      server.middlewares.use('/__build-info', (req, res) => {
        res.writeHead(200, { 'Content-Type': 'application/json' })
        res.end(JSON.stringify({ base, mode, uptime: process.uptime() }))
      })
    }
  }
}

Uso en vite.config.js:
js

import miPlugin from './plugins/mi-plugin.js'

export default defineConfig({
  plugins: [miPlugin({ debug: true })]
})

Luego puedes importar:
js

import buildInfo from 'virtual:build-info'
console.log(buildInfo.time)

05-assets-y-estilos / 01-assets-estaticos.md
La carpeta public

Todo lo que pongas en public/ (o la carpeta definida en publicDir) será servido en la raíz del sitio sin transformación. Por ejemplo, public/favicon.ico -> http://localhost:5173/favicon.ico.

En el index.html puedes referenciarlos directamente:
html

<link rel="icon" href="/favicon.ico" />

En producción se copian a dist/ tal cual. Si necesitas que pasen por un pipeline de optimización, no los pongas en public.
Importar assets desde JavaScript

Puedes importar imágenes, fuentes, etc., y obtendrás una URL con hash para cacheo óptimo:
js

import logoUrl from './logo.png'

const img = document.createElement('img')
img.src = logoUrl

Durante el build, los archivos menores a 4KB se inlinean como base64 automáticamente. Puedes cambiar este límite con build.assetsInlineLimit (0 = desactiva el inlining).
Usar new URL() para assets dinámicos
js

function getImageUrl(name) {
  return new URL(`./dir/${name}.png`, import.meta.url).href
}

Vite lo transforma para que sea válido en producción (mueve el asset a la carpeta de salida correctamente). Si la ruta no contiene variables dinámicas en el fragmento relativo, no funcionará.
Ajustar la base de los assets

Si despliegas en un subdirectorio, establece base: '/mi-app/' y todos los enlaces generados la incluirán. En desarrollo, el servidor hace el proxy correspondiente.
05-assets-y-estilos / 02-css-modules.md
Uso básico

Cualquier archivo con extensión .module.css se procesa como módulo CSS, generando nombres de clase únicos:
css

/* styles.module.css */
.box {
  background: #eee;
  border: 1px solid #ccc;
}

js

import styles from './styles.module.css'
document.getElementById('app').classList.add(styles.box)

En el DOM verás algo como ._box_1a2b3.
Composición

CSS Modules permite composición con composes:
css

.base {
  color: blue;
}
.main {
  composes: base;
  font-weight: bold;
}

Integración con TypeScript

Para tipado, crea un archivo *.d.ts:
ts

declare module '*.module.css' {
  const classes: { readonly [key: string]: string }
  export default classes
}

También puedes usar vite/client que ya incluye estas declaraciones.
Configuración de CSS Modules

En vite.config.js:
js

css: {
  modules: {
    localsConvention: 'camelCaseOnly',  // permite acceder a .my-class como styles.myClass
    scopeBehaviour: 'local',            // o 'global'
    generateScopedName: '[name]__[local]___[hash:base64:5]'
  }
}

05-assets-y-estilos / 03-postcss-preprocesadores.md
PostCSS

Vite detecta automáticamente un archivo de configuración de PostCSS (postcss.config.js, .postcssrc, etc.) y lo aplica a todos los CSS. Puedes usar plugins como autoprefixer, postcss-nesting, tailwindcss, etc.

Ejemplo postcss.config.js:
js

module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  }
}

Si no hay configuración externa, Vite aplica autoprefixer por defecto (a partir de build.target).
Preprocesadores: SCSS, Less, Stylus

Solo necesitas instalar el compilador:

    sass para SCSS/SASS

    less para Less

    stylus para Stylus

Luego puedes importar directamente archivos .scss, .less, etc.:
js

import './estilo.scss'

Opciones globales de preprocesadores

Puedes inyectar variables o mixins globales sin necesidad de importarlos en cada archivo:
js

css: {
  preprocessorOptions: {
    scss: {
      additionalData: `@import "@/styles/variables.scss";`
    },
    less: {
      math: 'always',
      globalVars: {
        mainColor: 'red'
      }
    }
  }
}

Nota: additionalData se agrega al principio de cada hoja de estilo procesada, útil para variables, pero con cuidado de no duplicar código.
05-assets-y-estilos / 04-imports-especiales-raw-urls.md
Importar archivos como string (?raw)

Cualquier archivo puede importarse como texto plano añadiendo ?raw:
js

import script from './script.py?raw'
console.log(script) // contenido del archivo Python como string

Importar como URL (?url)

Devuelve la URL final del asset (útil para Workers, sonidos, videos):
js

import audioUrl from './sound.mp3?url'
const audio = new Audio(audioUrl)

Importar Workers (?worker)

Importa un Web Worker como constructor:
js

import MyWorker from './worker.js?worker'
const worker = new MyWorker()

Esto evita tener que gestionar rutas manualmente y aplica empaquetado en producción.
JSON y otros

Los archivos JSON se importan directamente como objetos, y si el JSON tiene campos en la raíz, puedes desestructurarlos:
js

import { version } from './package.json'
console.log(version)

06-typescript-jsx / 01-typescript-en-vite.md
Transpilación vs chequeo

Vite usa esbuild para transpilar TypeScript a JavaScript, lo que es extremadamente rápido pero no verifica tipos. Solo elimina las anotaciones de tipo.

Para chequeo de tipos, debes ejecutar tsc --noEmit en paralelo (o usar vue-tsc para proyectos Vue). Puedes agregar un script:
json

"scripts": {
  "build": "tsc --noEmit && vite build",
  "dev": "vite"
}

Configuración de tsconfig.json

Vite respeta los alias (paths) definidos en el compilador si están correctamente configurados. Es importante asegurar que baseUrl y paths coincidan con los alias de Vite.

tsconfig.json mínimo:
json

{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler", // o "node"
    "strict": true,
    "jsx": "preserve",
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "lib": ["ESNext", "DOM"],
    "skipLibCheck": true,
    "noEmit": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"]
}

JSX con TypeScript

Para React, usa "jsx": "react-jsx". Para Vue, no aplica porque usa SFC; para JSX en Vue, "jsx": "preserve" y "jsxImportSource": "vue".
Mixins, decoradores, etc.

Si usas decoradores (experimental), habilita "experimentalDecorators": true. Vite lo transpila correctamente.
Tipos de cliente Vite

Include "vite/client" en compilerOptions.types o agrega una referencia en un .d.ts para que TypeScript reconozca tipos como import.meta.env, *.module.css, etc.:
ts

/// <reference types="vite/client" />

06-typescript-jsx / 02-jsx-react-vue-svelte.md
React JSX

La transformación automática (React 17+) está soportada. Asegura "jsx": "react-jsx" en tsconfig.json. Vite usará el plugin @vitejs/plugin-react o plugin-react-swc para manejar JSX y Fast Refresh.

Si usas JSX sin React (por ejemplo, con Preact), configura jsxImportSource en el plugin o en el tsconfig:
json

"jsx": "react-jsx",
"jsxImportSource": "preact"

Vue JSX

Es posible escribir JSX con Vue, pero el plugin Vue no lo compila por defecto. Necesitas agregar @vitejs/plugin-vue-jsx:
bash

npm install -D @vitejs/plugin-vue-jsx

js

import vueJsx from '@vitejs/plugin-vue-jsx'

export default defineConfig({
  plugins: [vue(), vueJsx()]
})

Luego en tsconfig.json:
json

"jsx": "preserve",
"jsxImportSource": "vue"

Svelte

Svelte tiene su propio compilador, no JSX. Se integra con @sveltejs/vite-plugin-svelte. No requiere configuración JSX especial.
07-build-produccion / 01-build-rollup.md
Empaquetado de producción

vite build utiliza Rollup internamente. La configuración se personaliza mediante build.rollupOptions. Vite preconfigura aspectos de entrada, salida, plugins de Rollup necesarios (como @rollup/plugin-commonjs, @rollup/plugin-node-resolve).
Opciones de build
js

export default defineConfig({
  build: {
    target: 'es2015',       // nivel de sintaxis de salida
    outDir: 'dist',
    assetsDir: 'assets',
    cssCodeSplit: true,     // dividir CSS en chunks
    sourcemap: true,        // generar sourcemaps de producción
    minify: 'esbuild',      // o 'terser' (lento pero más compresión)
    chunkSizeWarningLimit: 500, // umbral de alerta (KB)
    rollupOptions: {
      input: {
        main: 'index.html'  // entradas adicionales aquí
      },
      output: {
        manualChunks: {
          vendor: ['vue', 'lodash']  // agrupación manual
        }
      }
    }
  }
})

Plugins de Rollup adicionales

Puedes añadir cualquier plugin de Rollup dentro de build.rollupOptions.plugins, pero ten cuidado de no duplicar los que Vite ya incluye. Normalmente se añaden plugins como rollup-plugin-visualizer o @rollup/plugin-image.
CSS en producción

Si cssCodeSplit es true, cada chunk de JS que importe CSS generará un archivo CSS asociado. Con false todo el CSS irá en un único archivo.
07-build-produccion / 02-library-mode.md
Empaquetar una librería

Configura build.lib para generar una entrada específica y formatos (ES, CJS, UMD). Ideal para compartir código reutilizable.
js

export default defineConfig({
  build: {
    lib: {
      entry: 'src/index.ts',
      name: 'MiLibreria',
      formats: ['es', 'cjs', 'umd'],
      fileName: (format) => `mi-libreria.${format}.js`
    },
    rollupOptions: {
      external: ['vue'],  // excluir peer dependencies
      output: {
        globals: {
          vue: 'Vue'
        }
      }
    }
  }
})

    entry: archivo de entrada.

    name: nombre global para UMD.

    formats o formats: los formatos deseados.

    fileName: patrón del archivo de salida.

Generar tipos (.d.ts)

Vite no genera declaraciones automáticamente. Debés ejecutar tsc --emitDeclarationOnly y configurar tsconfig.json adecuadamente. O usar vite-plugin-dts.
07-build-produccion / 03-code-splitting.md
División de código

Vite/Rollup aprovechan los import() dinámicos para crear chunks asíncronos automáticamente:
js

const module = await import('./heavy.js')

En producción, se generará un archivo separado que se cargará bajo demanda.
Chunks manuales

Agrupa módulos en chunks con output.manualChunks. Puede ser un objeto o una función:
js

rollupOptions: {
  output: {
    manualChunks: {
      vendor: ['react', 'react-dom'],
      utils: ['lodash', 'axios']
    }
  }
}

O con función:
js

manualChunks(id) {
  if (id.includes('node_modules/lodash')) return 'lodash'
  if (id.includes('node_modules')) return 'vendor'
}

Plugin splitVendorChunkPlugin

Vite expone un plugin oficial para separar automáticamente dependencias de node_modules en un chunk vendor:
js

import { splitVendorChunkPlugin } from 'vite'

export default defineConfig({
  plugins: [splitVendorChunkPlugin()]
})

Es una forma simple sin configuración manual.
Carga diferida de rutas (frameworks)

En Vue, React, etc., las rutas perezosas (() => import(...)) generan chunks por ruta, logrando una división de código óptima.
07-build-produccion / 04-despliegue.md
Despliegue estático

La carpeta dist contiene HTML, JS, CSS y assets listos para subir a cualquier servidor de archivos (Nginx, Apache, AWS S3, Vercel, Netlify, GitHub Pages).
Configuración de la ruta base

Si tu app no se sirve desde raíz, ajusta base:
js

base: '/miapp/'

También puedes usar base condicional con variables de entorno:
js

base: process.env.NODE_ENV === 'production' ? '/miapp/' : '/'

SPA fallback

La mayoría de las SPAs necesitan servir index.html para cualquier ruta que no sea un archivo. En servidores como Nginx:
nginx

location / {
  try_files $uri $uri/ /index.html;
}

En plataformas como Netlify, activa el redireccionamiento a index.html. Netlify soporta archivos _redirects o configuración de SPAs.
Headers y caché

Puedes configurar el Cache-Control para assets con hash (fuertes) y para index.html (no almacenable en caché). Vite genera hashes en los nombres de archivos para permitir caché agresiva.
08-avanzado / 01-ssr.md
Server-Side Rendering con Vite

Vite ofrece APIs para construir aplicaciones con SSR usando el servidor de desarrollo en modo middleware o construyendo bundles separados para servidor y cliente.

Arquitectura típica:

    Entrada del cliente: src/entry-client.js con createApp().

    Entrada del servidor: src/entry-server.js (exporta una función que recibe la URL y devuelve la app renderizada).

En desarrollo

Se crea un servidor Node (Express, Koa) que usa el middleware de Vite:
js

import { createServer } from 'vite'

const vite = await createServer({
  server: { middlewareMode: true },
  appType: 'custom'
})
app.use(vite.middlewares)

app.get('*', async (req, res) => {
  // 1. Leer index.html y aplicar transformaciones
  let template = await fs.readFile('index.html', 'utf-8')
  template = await vite.transformIndexHtml(req.url, template)
  // 2. Cargar el módulo del servidor (con HMR)
  const { render } = await vite.ssrLoadModule('/src/entry-server.js')
  // 3. Renderizar y devolver
  const { html } = await render(req.url)
  const finalHtml = template.replace('<!--app-html-->', html)
  res.status(200).send(finalHtml)
})

En este esquema, los cambios en código del servidor se reflejan sin reiniciar el proceso (gracias a ssrLoadModule).
En producción

vite build se ejecuta dos veces (con configuración SSR distinta) o con un plugin como vite-plugin-ssr. Vite puede generar bundles de servidor con formato ESM o CJS.
08-avanzado / 02-web-workers.md
Workers con ESM

Vite soporta Workers con sintaxis de módulo:
js

const worker = new Worker(new URL('./worker.js', import.meta.url), { type: 'module' })

Esto funciona en desarrollo y se empaqueta correctamente en producción. Para importar un Worker y usarlo como constructor, usa el sufijo ?worker:
js

import MyWorker from './worker.js?worker'
const worker = new MyWorker()

El worker se convierte en un chunk separado.
Shared Workers

Para Shared Workers, se utiliza ?sharedworker:
js

import MySharedWorker from './shared-worker.js?sharedworker'
const worker = new MySharedWorker()

Plugin Comlink (opcional)

Puedes integrar comlink para una comunicación más limpia con Workers. Vite no lo incluye directamente, pero puedes usarlo normalmente.
08-avanzado / 03-webassembly.md
Importar WebAssembly

Vite puede importar módulos .wasm directamente si son compilados con ESM. La mayoría de herramientas (Rust, Go, C++) generan .wasm con import/export.
js

import init, { add } from './math.wasm'
init().then(() => console.log(add(1, 2)))

Si tu .wasm no es ESM, puedes inicializarlo manualmente:
js

import wasmUrl from './math.wasm?url'
const response = await fetch(wasmUrl)
const buffer = await response.arrayBuffer()
const module = await WebAssembly.instantiate(buffer)

Prefijo ?init

Vite ofrece ?init para obtener una función que inicializa el módulo pasando importaciones:
js

import init from './math.wasm?init'

const instance = await init({
  env: { memory: new WebAssembly.Memory({ initial: 256 }) }
})

En producción, Rollup inlinea el archivo .wasm como un Uint8Array si es pequeño, o lo emite como archivo separado.
08-avanzado / 04-integracion-backend.md
Modo Middleware

Vite puede funcionar como middleware en un servidor Node personalizado (Express, Fastify, Koa). Esto permite usar el servidor de desarrollo de Vite dentro de tu propia aplicación backend.

Ejemplo con Express:
js

import express from 'express'
import { createServer as createViteServer } from 'vite'

const app = express()

const vite = await createViteServer({
  server: { middlewareMode: true },
  appType: 'custom'
})

app.use(vite.middlewares)

app.listen(3000)

Con esto, puedes manejar APIs propias y delegar las peticiones de frontend a Vite.
Integración avanzada

Puedes acceder al servidor HTTP de Vite y adjuntarlo a un https.createServer existente, o usarlo junto con ws para WebSockets propios.
Uso programático del Dev Server

Si no usas Connect/Express, puedes crear el servidor con createServer() y luego montarlo manualmente:
js

const server = await createViteServer({ ... })
// server.httpServer es un http.Server (o https)
// server.middlewares es la app Connect

09-recursos / 01-comandos-utiles.md
CLI de Vite

    vite – inicia servidor de desarrollo.

    vite build – construye para producción.

    vite preview – sirve la carpeta de producción localmente (para probar).

    vite optimize – fuerza el pre-bundling y sale (útil para CI).

    vite --debug – muestra logs detallados.

    vite --port 4000 – cambia el puerto.

    vite --open – abre el navegador.

    vite --force – fuerça el re-pre-bundling ignorando caché.

    vite build --mode staging – build con modo personalizado.

Depuración

Puedes inspeccionar el rendimiento con DEBUG=vite:*:
bash

DEBUG=vite:* vite

09-recursos / 02-comparativa-otras-herramientas.md
Vite vs Webpack
Aspecto	Vite	Webpack
Desarrollo	ESM nativo, arranque instantáneo, HMR rápido	Empaca todo, arranque lento en proyectos grandes
Empaquetado	Rollup (más simple, tree-shaking eficiente)	Webpack (configuración compleja, muchos loaders)
Plugins	API compatible Rollup + hooks específicos; plugin oficiales para frameworks	Ecosistema enorme, pero configuración verbosa
Rendimiento	esbuild en dev (pre-bundling y transpilación)	Babel/Terser más lentos
Curva aprendizaje	Moderada, configuración mínima	Alta, entender loaders, plugins, optimización

Vite es ideal para nuevos proyectos; Webpack aún es necesario en proyectos empresariales con configuraciones muy personalizadas antiguas.
Vite vs Parcel

Parcel también ofrece cero configuración y es rápido, pero Vite tiene un ecosistema más amplio de plugins y mejor soporte SSR.
Vite vs Turbopack

Turbopack (Next.js 13+) es extremadamente rápido (escrito en Rust) pero está muy ligado a Next.js. Vite es más flexible y funciona con cualquier framework.
09-recursos / 03-fuentes-oficiales.md
Documentación

    Sitio oficial: vitejs.dev

    Guía de inicio: Getting Started

    Configuración: Config Reference

    API de plugins: Plugin API

Repositorio y comunidad

    GitHub: vitejs/vite

    Discord: Chat Vite Land

    Twitter: @vite_js

    Ejemplos: Awesome Vite

Cursos y tutoriales

    “Vite: The Complete Guide” en Vite’s docs

    “Fast & Modern Frontend Tooling with Vite” en YouTube (Evan You)