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

03-configuración / 01-vite-config.md (a fondo)
Ciclo de resolución de la configuración

Cuando ejecutas vite o vite build, ocurre lo siguiente:

    Descubrimiento del archivo de configuración
    Vite busca en la raíz del proyecto archivos como vite.config.js, .ts, .mjs, .cjs. Si usas TypeScript, Vite lo compila al vuelo usando esbuild. También puedes forzar un archivo con --config <ruta>.

    Evaluación temprana
    Si exportas una función, Vite la invoca pasándole { command, mode } y espera que devuelva una configuración completa o una promesa.

    Resolución de plugins y fusión
    Los plugins con el hook config reciben la configuración parcial y pueden modificarla (por ejemplo, añadir define o resolve.alias). Esto sucede antes de aplicar valores por defecto.

    Aplicación de valores predeterminados
    Vite rellena campos ausentes: root: process.cwd(), base: '/', publicDir: 'public', server.port: 5173, build.outDir: 'dist', etc.

    Segundo hook: configResolved
    Una vez determinada la configuración final, se notifica a los plugins que implementen configResolved para que puedan guardar referencias o ejecutar lógica. Es el momento de leer config.command, config.mode, etc., congelados.

Configuración condicional por comando y modo

Exportar una función es clave:
js

export default defineConfig(({ command, mode }) => {
  const isDev = command === 'serve'
  return {
    define: {
      __DEV__: isDev
    },
    build: {
      sourcemap: mode === 'staging' ? 'hidden' : false,
      target: mode === 'electron' ? 'esnext' : 'es2015'
    }
  }
})

Tipos estrictos con defineConfig

Siempre usa defineConfig de 'vite'. No solo da autocompletado, sino que también ayuda a plugins que inspeccionan la configuración con TypeScript.
Incluir otras configuraciones (merge)

Puedes extender configuraciones base usando vite-merge o manualmente:
js

import baseConfig from './vite.base.config.js'

export default defineConfig({
  ...baseConfig,
  plugins: [
    ...baseConfig.plugins,
    // agregar más
  ]
})

Opciones menos conocidas pero poderosas

    appType: 'spa' (por defecto) o 'custom' (para SSR). Determina cómo se tratan los middlewares y la inyección del script de Vite en el HTML.

    logLevel: 'info', 'warn', 'error', 'silent'. Controla la verbosidad en terminal.

    clearScreen: true para limpiar consola al inicio (útil para CI).

    envDir: directorio para cargar archivos .env. Por defecto, la raíz.

    assetsInclude: un regex o función para considerar archivos como assets (ej: .glb, .hdr).

03-configuración / 02-resolve-alias.md (a fondo)
Alias con objetos y funciones

Además de { '@': '/src' }, puedes definir alias como función para mayor flexibilidad:
js

resolve: {
  alias: (id) => {
    if (id.startsWith('@components/')) {
      return path.resolve(__dirname, 'src/components', id.slice('@components/'.length))
    }
  }
}

Pero cuidado: las funciones no pueden usarse con TypeScript paths.
Resolución de paquetes: main vs module vs exports

Vite, al igual que Node, sigue el orden de resolución de paquetes basado en exports, module, main y browser. Puedes personalizarlo con resolve.mainFields:
js

resolve: {
  mainFields: ['module', 'jsnext:main', 'jsnext', 'main']
}

Para entornos de navegador, Vite por defecto busca ['browser', 'module', 'jsnext:main', 'jsnext']. Puedes priorizar 'exports' con exportsFields: ['exports'].
Extensiones y orden

El array extensions importa porque Vite probará cada una. Añadir extensiones personalizadas como .vue o .jsx evita errores:
js

resolve: {
  extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue']
}

El orden importa: si tienes Button.vue y Button.ts, al importar Button resolverá el primero que coincida.
dedupe en monorepos

Cuando usas monorepos (pnpm, yarn workspaces), a veces existen varias copias de una misma dependencia (ej: vue). dedupe fuerza que todas las importaciones de ciertos paquetes apunten a la misma instancia en node_modules raíz. Esto es vital para que React/Vue no se monten dos veces.
js

resolve: {
  dedupe: ['vue', 'react']
}

preserveSymlinks

Si tu proyecto depende de paquetes enlazados con npm link o yarn link, por defecto Vite resuelve las rutas reales (siguiendo symlinks). Esto puede romper alias o importaciones relativas dentro del paquete enlazado. Activar preserveSymlinks: true mantiene la ruta original.
03-configuración / 03-optimize-deps.md (a fondo)
Algoritmo de caché y regeneración

Vite calcula un hash de las dependencias a pre-empaquetar basándose en:

    Contenido de package-lock.json / yarn.lock / pnpm-lock.yaml (o package.json si no existe lock).

    Lista de entradas de dependencias detectadas (escaneando los archivos fuente).

    Versiones de esbuild y Vite.

    Opciones de optimizeDeps que afecten al compilado (como esbuildOptions).

Si el hash cambia, se vuelve a ejecutar el pre-bundling. Si no, se sirve desde node_modules/.vite/deps.
Escaneo de dependencias (descubrimiento)

Por defecto, Vite escanea los imports estáticos en tu código fuente (archivos .js, .ts, .jsx, .tsx, .vue, etc.) para descubrir qué dependencias precargar. Los imports dinámicos (import()) también se incluyen si son literales. Esto se controla con optimizeDeps.entries:
js

optimizeDeps: {
  entries: ['./src/main.ts', './src/worker.js']
}

Si usas index.html múltiples o entradas atípicas, debes especificarlas aquí.
Forzar inclusión/exclusión y sus trampas

    include: agrega dependencias que Vite no habría detectado automáticamente (por ejemplo, importadas con un require convertido por un plugin). También garantiza que estén disponibles en el alcance global de esbuild (útil para polyfills).

    exclude: quita del pre-bundling paquetes que ya son ESM válidos y querés mantener como peticiones separadas (ejemplo: three). Pero cuidado: excluir una dependencia que luego se importa desde otra dependencia pre-empaquetada puede causar que ambas terminen en el mismo chunk o fallen.

needsInterop

Algunos módulos CJS requieren un envoltorio de interoperabilidad para usarse con import. Vite lo detecta automáticamente, pero puedes forzarlo:
js

optimizeDeps: {
  needsInterop: ['some-cjs-lib']
}

Esto asegura que import funcione como default import.
Opciones de esbuild dentro de optimizeDeps

Puedes pasar cualquier opción válida de esbuild (excepto entryPoints, outdir, etc.):
js

optimizeDeps: {
  esbuildOptions: {
    target: 'es2020',
    supported: {
      'top-level-await': true
    },
    plugins: [miEsbuildPlugin()]  // muy raro, pero posible
  }
}

Ten en cuenta que estos ajustes solo afectan al pre-bundling de desarrollo. Para producción, configura build.target.
Pre-bundling de módulos con BINARIES o C++ nativos

Si una dependencia requiere archivos .node (nativos), el pre-bundling fallará porque esbuild solo maneja JavaScript. Solución: excluye esa dependencia y usa un plugin de Vite que cargue el archivo nativo (como vite-plugin-node-polyfills o similar).
03-configuración / 04-modos-y-env.md (a fondo)
Flujo de carga de variables de entorno

Cuando Vite arranca, ejecuta:

    Carga .env (genérico).

    Carga .env.local (sobrescribe).

    Carga .env.[mode] (sobrescribe aún más).

    Carga .env.[mode].local (sobrescribe todo).

Las variables locales (*.local) deberían estar en .gitignore.
Variables de entorno en el HTML

Además de %VITE_APP_TITLE%, puedes usar variables dentro de atributos:
html

<link rel="canonical" href="%VITE_CANONICAL_URL%" />
<meta name="version" content="%VITE_VERSION%" />

Simulación de variables en desarrollo

Puedes crear un script que genere un .env.development dinámicamente antes de ejecutar vite. O usar el hook config de un plugin para inyectar valores:
js

{
  name: 'env-injector',
  config() {
    return {
      define: {
        'import.meta.env.VITE_MY_VAR': JSON.stringify(process.env.MY_VAR)
      }
    }
  }
}

Reemplazo estático y tree-shaking profundo

En producción, import.meta.env.PROD se convierte en true o false en el código. Rollup elimina el código muerto gracias a eso. Por ejemplo:
js

if (import.meta.env.PROD) {
  // este bloque se elimina en desarrollo
}

Puedes crear constantes propias con define para lograr efectos similares.
Variables en tiempo de ejecución

Si quieres inyectar configuraciones en tiempo de ejecución (no durante el build), la práctica común es exponer un endpoint /config.js que asigne variables globales. Luego, en tu aplicación las consumes:
html

<script src="/config.js"></script>
<script>
  console.log(window.APP_CONFIG.apiUrl)
</script>

Eso es externo a Vite, pero se complementa con base y variables de entorno para entornos complejos.
loadEnv en modo programático

Cuando uses la API programática de Vite (por ejemplo, para tests con Vitest), puedes cargar variables con:
js

import { loadEnv } from 'vite'

const env = loadEnv('development', process.cwd(), 'VITE_')
console.log(env.VITE_API_URL)

Útil para setear la URL de API en configuraciones de pruebas.
04-plugins / 01-introduccion-plugins.md (a fondo)
Ciclo de vida de hooks en detalle

Un plugin puede implementar muchos hooks. Orden de ejecución durante el desarrollo:

    config: modificar configuración inicial.

    configResolved: leer configuración final.

    configureServer: recibir instancia del servidor (solo en serve).

    resolveId: resolución de importaciones (puede ser asíncrono).

    load: carga de módulos virtuales.

    transform: transformación del código fuente (con orden pre, normal y post).

    handleHotUpdate: personalizar HMR.

En producción (build) se omiten configureServer y handleHotUpdate, y se usan hooks de Rollup puros (Vite pasa la configuración de Rollup a los plugins).
Hook transformIndexHtml

Permite alterar el HTML final servido durante el desarrollo. Múltiples plugins pueden usarlo; se ejecutan en serie. Puede devolver una cadena o un objeto { html, tags }.
js

transformIndexHtml(html, ctx) {
  return html.replace(/__REPLACE_ME__/, 'valor dinámico')
}

Hook configureServer y el servidor WebSocket

El parámetro server proporciona:

    server.config: la configuración completa.

    server.ws: el servidor WebSocket para enviar eventos personalizados.

    server.middlewares: la pila de middlewares Connect.

    server.httpServer: el servidor HTTP nativo.

    server.printUrls(): imprime las URLs en consola.

Puedes añadir middlewares antes o después de Vite:
js

configureServer(server) {
  server.middlewares.use('/api-custom', (req, res) => {
    // ...
  })
}

Hook handleHotUpdate y propagación inteligente

Recibe { file, timestamp, modules, server }. Devuelve un array de módulos a recargar o un [] vacío para suprimir la actualización. Si devuelves void, Vite decide mediante propagación hacia arriba.

Útil para recargas personalizadas:
js

handleHotUpdate({ file, server, modules }) {
  if (file.endsWith('.config.js')) {
    server.ws.send({ type: 'full-reload' })
    return [] // evita HMR parcial
  }
}

Orden de aplicación (enforce)

    enforce: 'pre' se ejecuta antes que los plugins normales.

    Normal (sin enforce) es el estándar.

    enforce: 'post' después de todos los plugins normales.

La diferencia importa si un plugin debe transformar antes que otro. Por ejemplo, un plugin que procesa lenguaje A debe ejecutarse antes de uno que procesa lenguaje B si A compila a B.
Plugins asíncronos

Casi todos los hooks pueden devolver Promises. resolveId, load, transform se encadenan asíncronamente.
Plugins condicionales (apply)

Puedes condicionar un plugin con apply:
js

{
  name: 'only-dev',
  apply: 'serve', // solo en desarrollo
  // ...hooks
}

Valores: 'serve', 'build', o una función (config, { command }) => boolean.
04-plugins / 02-plugin-vue.md (a fondo)
Internamente: cómo funciona @vitejs/plugin-vue

    Se engancha en load para devolver una versión compilada de los SFC.

    Utiliza el compilador de Vue (@vue/compiler-sfc) para separar template, script y estilos.

    Cada bloque de <script> se procesa según lang (TypeScript, CoffeeScript, etc.) usando sus propias dependencias.

    <template> se compila a render functions.

    <style> con scoped genera atributos únicos.

HMR en componentes Vue

El plugin inyecta código que usa la API de HMR de Vite. Cada componente SFC exporta un __hmrId que Vue Runtime usa para reemplazar el componente en caliente y preservar el estado. Soporta cambios en script, template y estilo por separado.

Si cambias solo <style>, se actualiza sin tocar el componente (el CSS se reemplaza). Si cambias <script>, se actualiza el componente pero se mantiene el estado si usas defineProps, ref, etc.
Componentes functional y opciones avanzadas

El plugin admite opciones de compilador como isCustomElement para Web Components:
js

vue({
  template: {
    compilerOptions: {
      isCustomElement: (tag) => tag.startsWith('my-wc-')
    }
  }
})

Para usar Vue como Web Component:
js

vue({
  customElement: true // o /\.ce\.vue$/
})

Integración con JSX

Si usas JSX con Vue necesitas @vitejs/plugin-vue-jsx. El plugin Vue no compila JSX. Debes añadir ambos:
js

plugins: [vue(), vueJsx()]

Compilación en modo “suspense” o experimental

Puedes activar características experimentales del compilador de Vue pasando compilerOptions.mode: 'module' o similar.
04-plugins / 03-plugin-react.md (a fondo)
React Fast Refresh en detalle

Es una implementación de “React Refresh” que Vite habilita mediante Babel o SWC. Requiere inyectar código en cada componente que registre una firma y permita el reemplazo sin perder estado de hooks.

El plugin:

    Añade el preset react-refresh/babel (o su equivalente en SWC).

    Inyecta import RefreshRuntime from '/@react-refresh' en los módulos.

    En desarrollo, sirve el runtime de Refresh.

Limitaciones: no conserva el estado de componentes de clase (solo hooks). Para componentes basados en clases, el HMR se degrada a recarga completa.
Configuración de Babel personalizada

Puedes pasar opciones a Babel directamente:
js

react({
  babel: {
    plugins: [
      ['@babel/plugin-proposal-decorators', { legacy: true }]
    ]
  }
})

Esto es útil si usas decorators o propios plugins de Babel. Cuidado: si defines babel, sobrescribes la configuración por defecto de Babel; no es un merge profundo.
SWC vs Babel

@vitejs/plugin-react-swc es significativamente más rápido. Soporta la mayoría de casos, excepto algunos plugins de Babel muy específicos. Si tu proyecto usa decoradores legacy, verifica el soporte de SWC.
JSX automático y jsxImportSource

El plugin respeta la configuración del tsconfig.json. Para Preact, por ejemplo:
tsconfig

"jsx": "react-jsx",
"jsxImportSource": "preact"

Luego en vite.config:
js

import preact from '@preact/preset-vite'
// o el plugin react con jsxImportSource

Variables de entorno en JSX

Puedes usar import.meta.env directamente en JSX, se reemplaza estáticamente. No hay restricciones.
Producción y eliminación de propTypes

En producción, @vitejs/plugin-react elimina automáticamente propTypes si detecta que están definidas, reduciendo el tamaño del bundle.
04-plugins / 04-plugin-personalizado.md (a fondo)
Estructura avanzada de un plugin real

Vamos a construir un plugin que:

    Sirva archivos .glsl (shaders) como strings o módulos ES.

    Inyecte una variable global __SHADER_VERSION__ con la versión del proyecto.

    Genere automáticamente una galería de colores en el servidor de desarrollo.

Paso 1: Estructura básica
js

// plugins/vite-plugin-shaders.js

import { readFileSync } from 'node:fs'
import path from 'node:path'

export default function shaderPlugin(opciones = {}) {
  let version = '0.0.0'
  let outDir = 'dist'

  return {
    name: 'vite-plugin-shaders',

    // Tomamos la versión del package.json para inyectarla
    configResolved(config) {
      outDir = config.build.outDir
      try {
        const pkg = JSON.parse(readFileSync('package.json', 'utf8'))
        version = pkg.version || '0.0.0'
      } catch {}
    },

    // Módulo virtual con información de shaders
    resolveId(id) {
      if (id === 'virtual:shaders-info') return '\0virtual:shaders-info'
    },

    load(id) {
      if (id === '\0virtual:shaders-info') {
        return `export default { version: '${version}', count: ${opciones.count || 0} }`
      }
    },

    // Transformar archivos .glsl a módulo ES (export default string)
    transform(code, id) {
      if (id.endsWith('.glsl')) {
        // Podemos aplicar transformaciones al código GLSL aquí (p.ej, inclusión de archivos)
        return {
          code: `export default ${JSON.stringify(code)}`,
          map: null
        }
      }
      // Para fragment shader y vertex shader juntos podríamos soportar múltiples exportaciones
    },

    // Agregar un endpoint visual de prueba en desarrollo
    configureServer(server) {
      server.middlewares.use('/shader-gallery', (req, res) => {
        const shaderFiles = opciones.shaderPaths || []
        const list = shaderFiles
          .map(file => `<li>${file}</li>`)
          .join('')
        res.end(`
          <html>
            <body>
              <h1>Shader Gallery (v${version})</h1>
              <ul>${list}</ul>
            </body>
          </html>
        `)
      })
    },

    // En producción, podemos emitir los shaders como assets si es necesario
    generateBundle(options, bundle) {
      // Acceso a los archivos generados, por si queremos añadir un manifiesto
    }
  }
}

Uso en vite.config.js:
js

import shaderPlugin from './plugins/vite-plugin-shaders'

const shaderFiles = ['./src/shaders/basic.vert', './src/shaders/basic.frag']

export default defineConfig({
  plugins: [
    shaderPlugin({ shaderPaths: shaderFiles })
  ]
})

Trucos para plugins profesionales

    Manejo de configuraciones config: si tu plugin necesita opciones que pueden ser sobrescritas, usa config() para mergear con las opciones del usuario.

    Módulos virtuales: usa el prefijo \0 para indicar que es virtual (Rollup lo ignora en tiempo de bundle). Puedes hacerlo interactivo con TypeScript declarando tipos.

    HMR personalizado: emite eventos al cliente para forzar recargas completas o actualizaciones parciales.

js

server.ws.send({ type: 'custom:shader-update', data: { ... } })

El cliente puede escuchar:
js

import.meta.hot.on('custom:shader-update', (data) => {
  // recargar shader específico
})

    Construcción (build): cuando tu plugin genera archivos extra, usa generateBundle o writeBundle de Rollup.

Debug de plugins

Activar DEBUG=vite:plugin* para ver logs de ejecución. También puedes usar console.log dentro de los hooks, pero con cuidado en transform que se llama muchas veces.
Distribución de plugins

Publica como vite-plugin-*. Debe exportar la función del plugin. Recomiendo soportar opciones con tipos y documentar hooks internos.

05-assets-y-estilos / 01-assets-estaticos.md
Carpeta public

Todo lo que coloques en public/ se sirve en la raíz del sitio web sin ser procesado por Vite. En desarrollo, el servidor lo entrega tal cual; en producción, se copia directamente a dist/.

    Contenido típico: favicon.ico, robots.txt, manifest.json, imágenes que no necesitan hashing.

    Referencia en HTML: <link rel="icon" href="/favicon.ico" />. La ruta es absoluta desde la raíz.

    Personalización: cambia el directorio público con publicDir: 'static' o desactívalo con publicDir: false.

Los archivos en public no se benefician de:

    Hashing en el nombre de archivo (lo que impide cacheo agresivo y control de versiones).

    Optimización de imágenes.

    Inlining para reducir peticiones.

Importación de assets como URL

Cuando importas un recurso (imagen, fuente, archivo) desde JavaScript o CSS, Vite te devuelve la URL final:
js

import logoUrl from './logo.png'
// logoUrl será '/assets/logo.123abc.png' en producción (con hash)

Internamente, al construir, el archivo se copia a dist/assets/ con un hash de contenido y la referencia se actualiza. En desarrollo, la URL apunta al servidor de Vite con un parámetro ?t=timestamp para invalidar caché en cada cambio.
Tipos de archivo que se consideran assets

Por defecto, extensiones comunes de imágenes, fuentes, audio, video, etc., se tratan como assets. Puedes ampliar con assetsInclude en vite.config.js:
js

assetsInclude: ['**/*.glb', '**/*.hdr']

Ahora import modelo from './modelo.glb' devolverá la URL del archivo.
Límite de inlining

Los assets con tamaño menor a build.assetsInlineLimit (por defecto 4096 bytes) se incrustan como base64 en el bundle, evitando una petición HTTP adicional. Puedes cambiar el límite:
js

build: {
  assetsInlineLimit: 0  // nunca inlinear
}

O configurarlo por tipo mediante un plugin, aunque no es directo.
Reescritura de URLs en CSS

En CSS, las rutas url(./imagen.png) se reescriben automáticamente para reflejar la ubicación real del asset tras el build. Vite interpreta rutas absolutas (que comienzan con /) o relativas. Las rutas absolutas respetan la base configurada.
Assets dinámicos con new URL()

Cuando la ruta del asset se construye en tiempo de ejecución, debes usar la API new URL():
js

function getImageUrl(name) {
  return new URL(`./img/${name}.png`, import.meta.url).href
}

Vite analiza estos patrones durante el build y reemplaza new URL() con la URL del asset real, emitiendo el archivo correspondiente. Para que funcione, la parte relativa (./img/${name}.png) debe ser una string template con al menos un segmento estático (Vite necesita poder escanear el directorio). Si toda la ruta es dinámica, no puede resolverse.
Soporte en Workers y Web Workers

Dentro de Workers la API import.meta.url está disponible, y Vite puede manejar new URL() en trabajadores empaquetados.
Construcción del new URL en el código

Vite transforma:
js

const url = new URL(`./assets/${dynamic}.png`, import.meta.url).href
// en producción se convierte en algo como:
const url = "/assets/pic.abc123.png"
// si no es alcanzable analíticamente, lo deja como está y el asset se maneja por separado.

Hash y caché en producción

    Los assets importados obtienen nombres con hash (mi-imagen.1a2b3c4d.png). Esto permite servirlos con encabezados de caché fuerte (inmutable).

    Los archivos en public mantienen su nombre original, por lo que si cambias el contenido sin cambiar el nombre, los clientes en caché verán la versión antigua.

base y assets

La opción base en vite.config.js define la ruta pública base. Todos los enlaces generados por Vite (tanto en HTML, JS como CSS) la incluirán automáticamente:
js

base: '/miapp/'

Entonces import.meta.env.BASE_URL será '/miapp/' y las URLs de assets serán /miapp/assets/logo.png. En desarrollo, el servidor sirve todo en la raíz, pero puedes simular la base con server.origin y server.base.
05-assets-y-estilos / 02-css-modules.md
Activación y funcionamiento básico

Cualquier archivo con extensión .module.css (o .module.scss, .module.less… si tienes preprocesadores) se trata como Módulo CSS. Vite genera automáticamente nombres de clase únicos, evitando colisiones globales.
css

/* Button.module.css */
.red {
  color: red;
}

js

import styles from './Button.module.css'
button.className = styles.red  // resultado: <button class="_red_1a2b3">

Características avanzadas y sintaxis
Composición (composes)

Puedes heredar estilos de otras clases dentro del mismo módulo o incluso de módulos distintos:
css

.base {
  padding: 8px;
}
.primary {
  composes: base;
  background: blue;
}
.imported {
  composes: heading from './typography.module.css';
}

Selectores globales y locales

Con :global() y :local() puedes escapar del ámbito del módulo o forzar el ámbito local:
css

.button {
  color: blue;
}
:global(.global-class) {
  font-size: 20px;
}
.button :global(.icon) {
  margin-right: 5px; /* .icon no se renombra */
}

En el JS, .global-class queda como está, no se le aplica hash.
Configuración detallada

En vite.config.js, bajo css.modules:
js

css: {
  modules: {
    localsConvention: 'camelCaseOnly', // dash-case en CSS -> camelCase en JS
    scopeBehaviour: 'local',           // 'global' para desactivar ámbito local por defecto
    generateScopedName: '[name]__[local]___[hash:base64:5]', // patrón de nombres
    hashPrefix: 'my-app',              // prefijo para el hash (evita colisiones)
    globalModulePaths: [/path\/global\.css/] // archivos tratados como globales siempre
  }
}

    localsConvention: 'camelCase', 'camelCaseOnly', 'dashes', 'dashesOnly'.
    Ejemplo: clase .color-red → styles.colorRed.

    generateScopedName: puedes usar una función (name, filename, css) => string para generar nombres dinámicos, por ejemplo añadiendo la carpeta.

    globalModulePaths: array de expresiones regulares contra los cuales se comparan las rutas de los archivos .module.css. Si coincide, no se realiza scope (útil si tienes un módulo con clases que realmente quieres globales).

Integración con TypeScript

Para que TS reconozca las importaciones de módulos CSS, crea un archivo src/global.d.ts:
ts

declare module '*.module.css' {
  const classes: { readonly [key: string]: string }
  export default classes
}
declare module '*.module.scss' { ... } // etc.

El paquete vite/client ya incluye estas declaraciones, así que si tienes "types": ["vite/client"] en tu tsconfig.json, no necesitas las líneas adicionales.
Módulos CSS con preprocesadores

Los módulos funcionan con .scss, .less, .styl sin configuración extra, siempre que tengas el compilador instalado (sass, less, stylus). La regla de extensión .module.scss activa CSS Modules tras la compilación del preprocesador.
HMR para Módulos CSS

Cuando editas un archivo .module.css, Vite reemplaza el módulo en caliente, actualizando automáticamente los componentes que lo importan. Si el componente de framework usa HMR, verás el cambio reflejado sin perder estado.
05-assets-y-estilos / 03-postcss-preprocesadores.md
PostCSS

Vite tiene soporte nativo para PostCSS. Busca automáticamente un archivo de configuración en la raíz:

    postcss.config.js (o .cjs, .mjs)

    .postcssrc (JSON o YAML)

    postcss.config.ts (si configuras vite.config.ts con cargador .ts)

    postcss en package.json

Si no existe ninguna configuración, Vite por defecto intenta autoprefijar con autoprefixer basándose en el build.target (ej: es2015).
Orden de evaluación

Al encontrar varios archivos de configuración, Vite usa el que tenga mayor prioridad (el primero en la lista anterior). Para evitar ambigüedades, recomiendo postcss.config.js.
Plugins de PostCSS

Instala cualquier plugin de PostCSS y agrégalo a la configuración:
js

// postcss.config.js
module.exports = {
  plugins: {
    'postcss-nesting': {},   // permite CSS nesting nativo
    tailwindcss: {},
    autoprefixer: {},
  }
}

Si usas Tailwind CSS, asegúrate de que tailwindcss y postcss estén instalados como dependencias.
CSS Nesting (anidamiento) – diferencias

    La especificación CSS Nesting ya está soportada por navegadores modernos. Puedes activarla directamente con postcss-nesting o esperar que el build transpile con postcss-preset-env.

    Vite no transpila CSS nesting por sí mismo; necesitas un plugin PostCSS para convertir nested CSS a CSS plano si tu target no lo soporta.

Preprocesadores (SCSS, Less, Stylus)

Para usar un preprocesador, instala el compilador correspondiente:
bash

npm add -D sass        # para SCSS/SASS
npm add -D less
npm add -D stylus

Luego importa archivos con la extensión adecuada (styles.scss, styles.less). Vite los compilará sobre la marcha.
Variables globales / mixins automáticos

Para inyectar variables, funciones o mixins a todos los archivos sin necesidad de importarlos manualmente, usa additionalData en css.preprocessorOptions:
js

css: {
  preprocessorOptions: {
    scss: {
      additionalData: `@use "@/styles/variables" as *;\n`
    },
    less: {
      additionalData: `@import "@/styles/variables.less";\n`,
    }
  }
}

Ten cuidado: additionalData se antepone literalmente a cada hoja de estilo, por lo que si usas @use con namespaces, asegúrate de no causar conflictos de definición múltiple. A veces es mejor un archivo de mixins cargado mediante additionalData solo con variables.
Opciones específicas de preprocesador

    sourceMap: por defecto Vite activa los sourcemaps para estilos en desarrollo. Puedes sobrescribir con sourceMap: true/false.

    api: en Less, 'modern' es la API más rápida. Vite la usa por defecto si está disponible.

    rewriteUrls: en Less, controla la reescritura de url().

    includePaths: en SCSS, puedes añadir rutas de inclusión para que @import resuelva sin rutas relativas.

js

css: {
  preprocessorOptions: {
    scss: {
      includePaths: ['./node_modules'],
    }
  }
}

Combinación de preprocesador y PostCSS

Primero se ejecuta el preprocesador (ej: SCSS → CSS) y luego PostCSS sobre el resultado. Esto permite, por ejemplo, escribir SCSS y después aplicar autoprefijado y nesting con PostCSS.
HMR para preprocesadores

Funciona exactamente igual que con CSS plano. Si editas un archivo .scss, Vite recompila y actualiza el módulo CSS, inyectando los nuevos estilos sin recargar la página. Para estilos globales importados en main.js, se actualiza la hoja de estilos completa.
Producción: code splitting de CSS

Configurado con build.cssCodeSplit: true (por defecto), Vite genera un archivo CSS separado por cada chunk asíncrono que importa CSS. Si lo pones false, todo el CSS se extrae en un único archivo style.css.

Los estilos en módulos CSS también se extraen y se deduplican cuando varios módulos comparten las mismas reglas (gracias al orden de inclusión de Rollup).
05-assets-y-estilos / 04-imports-especiales-raw-urls.md
Import ?raw

Importa el contenido de cualquier archivo como una cadena de texto. Útil para archivos GLSL, SVG como texto, Markdown crudo, etc.
js

import shader from './shader.glsl?raw'
console.log(shader) // "#version 300 es\n..."

La transformación la realiza Vite internamente (sin plugin extra). En el build, el archivo se incluye como una constante en el bundle, no como un asset separado.
Import ?url

Devuelve la URL pública del recurso, igual que la importación estándar de assets, pero sin meta datos de la imagen.
js

import soundUrl from './sound.mp3?url'
const audio = new Audio(soundUrl)

Funciona para cualquier archivo que de otra forma se importaría como asset (imágenes, fuentes, etc.). En el build, el archivo se copia a dist/assets/ con hash. En desarrollo, se sirve desde el servidor.
Import ?worker y ?sharedworker

Permite importar directamente un Web Worker como Constructor:
js

import MyWorker from './worker.js?worker'
const worker = new MyWorker()

Internamente, Vite empaqueta el worker en un archivo separado y el import se convierte en la URL de ese chunk. El worker se ejecuta como módulo ES por defecto ({ type: 'module' }). Para Shared Workers:
js

import MySharedWorker from './shared-worker.js?sharedworker'
const shared = new MySharedWorker()

Los workers se tratan como entradas separadas en Rollup, por lo que heredan el mismo target y plugins. En desarrollo se usa new Worker() con la URL directa del servidor de Vite.
Workers con new URL

Una alternativa sin sufijo es:
js

const worker = new Worker(new URL('./worker.js', import.meta.url), { type: 'module' })

Vite analiza esto y empaqueta el worker como chunk separado. La sintaxis ?worker es más breve y se ha convertido en la recomendada.
Import ?init para WebAssembly

Cuando trabajas con .wasm que requieres inicializar con imports, Vite soporta ?init:
js

import init from './math.wasm?init'
const wasm = await init({
  env: {
    memory: new WebAssembly.Memory({ initial: 256 })
  }
})

En producción, el archivo .wasm se inlinea si es pequeño o se copia como asset. El sufijo ?init genera una función que recibe el objeto de imports y devuelve una promesa con las exportaciones.
Importación de JSON y exports nombrados

Un JSON se importa directamente como objeto:
js

import pkg from '../package.json'
console.log(pkg.version)

Además, si el JSON tiene campos de primer nivel, Vite permite named exports:
js

import { version, author } from '../package.json'

Esto es posible porque Vite transforma el JSON y emite export const version = .... Funciona tanto en desarrollo como en producción.
Import ?inline (Deprecado)

En versiones tempranas de Vite, ?inline forzaba el inlining como cadena base64. Ahora es mejor usar ?raw para contenido textual o importación normal que inlinea automáticamente si es pequeño.
Tipado para estas importaciones especiales

Para TypeScript, necesitas declarar módulos para los patrones de query. vite/client incluye:
ts

declare module '*?raw' { const content: string; export default content }
declare module '*?url' { const url: string; export default url }
declare module '*?worker' { const WorkerFactory: new () => Worker; export default WorkerFactory }
declare module '*?sharedworker' { ... }

Asegúrate de incluir "types": ["vite/client"] en tsconfig.json o agregar un /// <reference types="vite/client" /> en un archivo .d.ts.
Casos de uso y combinaciones

    SVG como componente React/Vue: no hay import especial, sino un plugin (como vite-plugin-svg). Podrías importar ?raw y luego manipular el string.

    Markdown compilado a HTML: plugin que intercepta .md y devuelve HTML. Importar ?raw es un enfoque más directo si no necesitas compilación.

    Archivos de configuración dinámicos: ?raw para cargar un JSON comentado o YAML crudo y luego parse manual.

06-typescript-jsx / 01-typescript-en-vite.md
Transpilación con esbuild

Vite utiliza esbuild para transformar TypeScript (y TSX) a JavaScript. Esto implica:

    Elimina anotaciones de tipo.

    Convierte JSX según el tsconfig.json (sin comprobar tipos).

    No realiza chequeo de tipos. Para ello debes ejecutar tsc --noEmit externamente.

Razón: esbuild es entre 20 y 100 veces más rápido que el compilador de TypeScript, garantizando arranque instantáneo.
Configuración del tsconfig.json

Un tsconfig.json mínimo y efectivo para Vite:
json

{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "jsx": "preserve",
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "lib": ["ESNext", "DOM"],
    "skipLibCheck": true,
    "noEmit": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },
    "types": ["vite/client"]
  },
  "include": ["src"]
}

    moduleResolution: "bundler" (TS 4.7+): ideal para Vite, entiende imports sin extensión y condiciones de exportación modernas.

    noEmit: true: porque Vite se encarga de generar los archivos; solo queremos chequeo de tipos.

    jsx: "preserve": para que esbuild maneje la transformación según framework. O usa "react-jsx" si quieres que el servidor de lenguaje TypeScript también entienda JSX automático.

    paths deben coincidir exactamente con resolve.alias en vite.config.js.

Chequeo de tipos

En tu package.json:
json

"scripts": {
  "build": "tsc --noEmit && vite build",
  "check": "tsc --noEmit"
}

Para proyectos Vue, usa vue-tsc:
bash

npm add -D vue-tsc
"build": "vue-tsc --noEmit && vite build"

Durante el desarrollo puedes correr tsc --noEmit --watch en una terminal aparte para tener feedback continuo de tipos.
Aliases y TypeScript

Define alias en vite.config.js:
js

resolve: {
  alias: { '@': '/src' }
}

Y en tsconfig.json:
json

"paths": {
  "@/*": ["./src/*"]
}

La coincidencia es crucial porque el editor usa tsconfig.json y Vite usa resolve.alias. Si no concuerdan, los imports se marcarán como error.
Tipos del cliente Vite (vite/client)

Este módulo de declaraciones añade tipos para:

    import.meta.env (con MODE, BASE_URL, PROD, DEV, SSR y variables con prefijo VITE_).

    Importaciones de CSS modules (*.module.css).

    Importaciones de assets (.png, .svg como string).

    Importaciones especiales (?raw, ?url, ?worker).

    import.meta.glob y import.meta.globEager.

Para activarlo, puedes poner en tu tsconfig.json:
json

"types": ["vite/client"]

O en un archivo env.d.ts:
ts

/// <reference types="vite/client" />

Soporte de decoradores experimentales

Habilita "experimentalDecorators": true en tsconfig.json. Vite transpila decoradores sin problema. Para metadatos de design (como en Angular), necesitas "emitDecoratorMetadata": true y puede requerir tslib y @types/reflect-metadata.
Const enums y isolatedModules

esbuild trata const enum de forma similar a enum. Pero es recomendable evitar export const enum y usar enums normales o union types, ya que TypeScript con isolatedModules: true (implícito en Vite) prohíbe export const enum porque no puede saber si el valor se usará en otros módulos sin contexto global. En su lugar, define enum simple.
Errores comunes y soluciones

    "Cannot find module './App' or its corresponding type declarations"
    Ocurre si importas un archivo .vue sin tener tipados. Agrega declare module '*.vue' { import type { DefineComponent } from 'vue'; const component: DefineComponent<{}, {}, any>; export default component } en un .d.ts.

    "Cannot find module './logo.png' or its corresponding type declarations"
    Agrega "types": ["vite/client"].

    Fallo en import con extensión omitida
    Vite resuelve extensiones automáticamente, pero TypeScript no. Asegúrate de que moduleResolution: 'bundler' esté configurado.

06-typescript-jsx / 02-jsx-react-vue-svelte.md
JSX en React
Configuración del compilador

En tsconfig.json:
json

"jsx": "react-jsx"

Esto habilita el runtime automático de React (sin necesidad de import React from 'react'). Si quieres el modo clásico importando React, usa "jsx": "react".

Vite con @vitejs/plugin-react detecta la configuración JSX y la aplica. Si usas SWC, el plugin @vitejs/plugin-react-swc respeta también.
React Fast Refresh

El plugin inyecta código para habilitar Hot Module Replacement con preservación del estado de hooks. Funciona automáticamente; cualquier componente exportado que use hooks se actualizará sin perder estado al editar JSX o lógica.
JSX sin React (Preact, otros)

Cambia jsxImportSource:
json

"jsx": "react-jsx",
"jsxImportSource": "preact"

Y en vite.config.js:
js

import preact from '@preact/preset-vite'
plugins: [preact()]

O manualmente sin plugin, basta con que el módulo 'preact/jsx-runtime' exista.
JSX en Vue

Vue 3 soporta JSX a través de @vitejs/plugin-vue-jsx. No es parte del plugin principal @vitejs/plugin-vue.
Instalación y configuración
bash

npm add -D @vitejs/plugin-vue-jsx

js

import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

export default defineConfig({
  plugins: [vue(), vueJsx()]
})

En tsconfig.json:
json

"jsx": "preserve",
"jsxImportSource": "vue"

Si omites jsxImportSource, el editor no reconocerá los elementos de Vue.
Uso en SFC o archivos .tsx

Puedes escribir componentes en .tsx:
tsx

import { defineComponent } from 'vue'
export default defineComponent({
  setup() {
    return () => <div>Hola</div>
  }
})

Los SFC .vue pueden mezclar <template> con <script lang="tsx"> usando la opción setup. Sin embargo, JSX en SFC es menos común.
Svelte (sin JSX)

Svelte utiliza su propio compilador, no JSX. Vite se integra con @sveltejs/vite-plugin-svelte:
bash

npm create vite@latest my-svelte-app -- --template svelte

O manualmente:
bash

npm add -D @sveltejs/vite-plugin-svelte

js

import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
  plugins: [svelte()]
})

TypeScript en Svelte se maneja con <script lang="ts"> dentro de los archivos .svelte. El plugin procesa el TypeScript internamente usando svelte-preprocess.
SolidJS

Solid usa JSX con una gramática extremadamente similar a React pero sin VDOM. Vite tiene soporte oficial:
bash

npm create vite@latest my-solid-app -- --template solid

O plugin: vite-plugin-solid.

Configuración de TS:
json

"jsx": "preserve",
"jsxImportSource": "solid-js"

Y el plugin se encarga de la transformación.
Resumen de configuraciones JSX comunes
Framework	Plugin Vite	tsconfig.json
React	@vitejs/plugin-react o -swc	"jsx": "react-jsx"
Vue JSX	@vitejs/plugin-vue + -vue-jsx	"jsx": "preserve", "jsxImportSource": "vue"
Preact	@preact/preset-vite	"jsx": "react-jsx", "jsxImportSource": "preact"
Solid	vite-plugin-solid	"jsx": "preserve", "jsxImportSource": "solid-js"
Svelte	@sveltejs/vite-plugin-svelte	No JSX

07-build-produccion / 01-build-rollup.md
Delegación en Rollup

Para el empaquetado de producción, Vite confía en Rollup, una herramienta madura de bundling que produce árboles de dependencias más pequeños y eficientes que esbuild (diseñado para velocidad, no para compresión final). Vite preconfigura Rollup para que trabaje con el mismo código fuente que ya manejas en desarrollo, aplicando los plugins que hayas añadido a vite.config.js.

El comando vite build ejecuta internamente:

    Resolución de todas las dependencias a partir de las entradas HTML/JS.

    Aplicación del hook transform de cada plugin en el orden adecuado.

    Bundle mediante Rollup con tree‑shaking, división de código y optimizaciones.

    Generación de los archivos finales en dist/.

Opciones principales de build

En vite.config.js, la propiedad build controla toda la salida:
js

export default defineConfig({
  build: {
    target: 'es2015',           // nivel de sintaxis JS de salida
    outDir: 'dist',             // directorio de salida
    assetsDir: 'assets',        // subdirectorio para assets (imágenes, fuentes...)
    cssCodeSplit: true,         // extraer CSS en chunks separados
    cssMinify: 'esbuild',       // 'esbuild' o 'lightningcss' (rápido), `true` para usar cssnano
    sourcemap: false,           // generar sourcemaps para producción
    minify: 'esbuild',          // 'esbuild', 'terser', o false
    terserOptions: { compress: { drop_console: true } }, // si usas terser
    brotliSize: true,           // mostrar tamaño comprimido en el reporte
    chunkSizeWarningLimit: 500, // umbral de advertencia en KB
    manifest: false,            // generar un manifest.json con mapeo de archivos
    ssr: false,                 // construir para entornos SSR
    rollupOptions: { /* ... */ }, // personalización directa de Rollup
    commonjsOptions: { /* ... */ }, // opciones para @rollup/plugin-commonjs
    dynamicImportVarsOptions: { /* ... */ }, // opciones para @rollup/plugin-dynamic-import-vars
  }
})

target

Define el nivel de características de JavaScript/ES que se mantienen sin transformar. Por ejemplo 'es2015' produce código compatible con navegadores que soportan ES6. Vite pasará este valor a esbuild (para minificación) y a Rollup (para transpilación). Si defines 'esnext', no se transpilan características modernas, ideal para Electron o entornos controlados.
minify

Por defecto 'esbuild' es rapidísimo y muy eficaz. Si necesitas compresión extrema (por ejemplo eliminar console.log), puedes configurar terser y añadir terserOptions. Para desactivar la minificación (debug), asigna false.
sourcemap

En producción se puede generar true (archivos .map separados), 'hidden' (sin referencia en el bundle), o 'inline'. Recomendado true o 'hidden' para rastrear errores sin exponer el código fuente al público.
manifest

Si activas manifest: true, Vite genera un manifest.json que mapea los nombres de archivo originales a los hasheados. Muy útil para backends que necesitan inyectar las URLs correctas de los assets.
rollupOptions

Permite pasar cualquier opción soportada por Rollup (excepto aquellas que Vite ya gestiona). La estructura típica:
js

build: {
  rollupOptions: {
    input: {
      main: 'index.html',
      admin: 'admin/index.html'
    },
    output: {
      entryFileNames: 'js/[name].[hash].js',
      chunkFileNames: 'js/[name].[hash].js',
      assetFileNames: 'assets/[name].[hash][extname]'
    },
    plugins: [ /* plugins de Rollup adicionales */ ],
    external: ['external-dep']
  }
}

Importante: la entrada por defecto es el index.html raíz. Para aplicaciones multi‑página, debes especificar manualmente las entradas HTML adicionales.
commonjsOptions

Afecta a @rollup/plugin-commonjs que convierte dependencias CJS a ESM. Puedes pasar opciones como:
js

commonjsOptions: {
  include: [/node_modules/],
  transformMixedEsModules: true
}

El proceso de build paso a paso

    Resolución de entradas: Vite recorre el/los HTML raíz y extrae todos los <script type="module"> y los imports asociados.

    Carga y transformación: Rollup carga los módulos, aplica los plugins Vite habilitados para build (muchos hooks de Vite son compatibles con Rollup).

    Tree shaking: Rollup marca el código no utilizado y lo elimina.

    Code splitting: Los import() dinámicos se convierten en chunks separados. Los CSS también se dividen si cssCodeSplit: true.

    Reemplazo de variables de entorno: Todas las import.meta.env.VITE_* y las constantes de define se sustituyen por sus valores finales.

    Minificación: con esbuild/terser y CSS con esbuild/lightningcss/cssnano.

    Generación de archivos: se escriben en outDir con la estructura definida en rollupOptions.output.

Múltiples páginas (MPA)

Para una web con varias entradas HTML, sin un framework SPA:
js

build: {
  rollupOptions: {
    input: {
      home: 'index.html',
      about: 'about.html',
      contact: 'contact.html'
    }
  }
}

Cada HTML generado incluirá solo los chunks necesarios para sus scripts y estilos.
CSS en producción

    cssCodeSplit: true (por defecto): cada chunk asíncrono de JS que importa CSS genera su propio archivo .css.

    cssCodeSplit: false: todo el CSS se concentra en un solo archivo style.css, eliminando múltiples peticiones pero aumentando el peso de la hoja principal.

    cssMinify permite elegir entre 'esbuild' (rápido, compresión aceptable) o 'lightningcss' (más rápido y con soporte para CSS moderno). Si usas true, se aplica cssnano (más lento pero más configurable con postcss.config).

Watch mode del build

Puedes usar vite build --watch para reconstruir automáticamente al cambiar archivos. Ideal para flujos de integración donde necesitas copiar la salida a otro directorio. Internamente Rollup observa los archivos fuente y reempaqueta solo lo necesario.
Solución de problemas comunes

    Chunk demasiado grande → usa manualChunks o revisa imports de librerías pesadas.

    Error "Could not resolve..." → verifica que todas las dependencias estén instaladas; si usas external, asegura que se carguen globalmente.

    Variables de entorno no reemplazadas en build → comprueba que el prefijo sea VITE_ y que el archivo .env.production exista o pases el modo correcto con --mode.

07-build-produccion / 02-library-mode.md
Propósito

El modo librería de Vite permite empaquetar código para ser distribuido y consumido por otros proyectos, en lugar de generar una aplicación completa. Perfecto para publicar componentes, utilidades o SDKs.
Configuración mínima
js

export default defineConfig({
  build: {
    lib: {
      entry: 'src/index.ts',          // archivo de entrada
      name: 'MiLibreria',             // nombre global para UMD
      formats: ['es', 'cjs', 'umd'],  // formatos de salida
      fileName: (format) => `mi-libreria.${format}.js`
    },
    rollupOptions: {
      external: ['vue', 'react'],     // no empaquetar estas dependencias
      output: {
        globals: {                    // para UMD, mapea a variables globales
          vue: 'Vue',
          react: 'React'
        }
      }
    }
  }
})

    entry: ruta al punto de entrada principal. Puede ser un array para múltiples entradas.

    name: obligatorio para el formato UMD, se expone en window.MiLibreria.

    formats: array que puede incluir 'es', 'cjs', 'umd' y 'iife'.

    fileName: puede ser una función o un string (p.ej. 'index'). Si es función recibe el formato como argumento y debe devolver el nombre de archivo.

Dependencias externas

Todas las dependencias que serán instaladas por el consumidor final (peerDependencies) deben marcarse como external en rollupOptions. Así Rollup no las incluirá en el bundle, reduciendo el tamaño drásticamente y evitando conflictos de versión.

Ejemplo para una librería de componentes React:
js

export default defineConfig({
  build: {
    lib: { ... },
    rollupOptions: {
      external: ['react', 'react-dom', 'react/jsx-runtime'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
          'react/jsx-runtime': 'jsxRuntime'
        }
      }
    }
  }
})

Para la salida UMD, globals indica cómo se accede a la dependencia externa en el contexto global del navegador.
Manejo de CSS

Si tu librería incluye estilos (componente con hoja de estilos importada), Vite extraerá el CSS en un archivo separado llamado style.css (a menos que configures cssCodeSplit). Para que el consumidor pueda importar ese CSS, debes indicárselo en la documentación o empaquetar los estilos dentro de JS.

Una técnica común es importar el CSS dentro del archivo JS de entrada, y en el package.json apuntar a ambos:
json

"main": "./dist/mi-libreria.cjs.js",
"module": "./dist/mi-libreria.es.js",
"style": "./dist/style.css"

Si prefieres que el CSS se inyecte automáticamente, necesitas un plugin que lo inyecte en el head al cargar el módulo (no es el comportamiento por defecto).
Generación de tipos (.d.ts)

Vite no genera archivos de declaración TypeScript por sí solo. Las opciones más comunes son:

    tsc --emitDeclarationOnly usando un tsconfig.build.json que apunte a la entrada y tenga "outDir": "dist".

    vite-plugin-dts que se integra en el proceso de build y emite las declaraciones automáticamente.

Ejemplo con vite-plugin-dts:
bash

npm add -D vite-plugin-dts

js

import dts from 'vite-plugin-dts'

export default defineConfig({
  plugins: [dts({ insertTypesEntry: true })]
})

Consideraciones de compatibilidad

    Al construir en formato CJS, Vite establece module.exports para la exportación por defecto. Asegúrate de que tu código exporte un default o compatibiliza con __esModule.

    Los módulos ESM ('es') deben tener extensión .mjs o el campo "type": "module" en el package.json del proyecto consumidor. Vite por defecto genera .js, pero puedes forzar .mjs en fileName.

    Para UMD, el nombre debe ser único para evitar colisiones globales.

Ejemplo completo: librería de componentes Vue
js

import vue from '@vitejs/plugin-vue'
import dts from 'vite-plugin-dts'

export default defineConfig({
  plugins: [vue(), dts()],
  build: {
    lib: {
      entry: 'src/index.ts',
      name: 'MiUILib',
      formats: ['es', 'cjs'],
    },
    rollupOptions: {
      external: ['vue'],
      output: {
        globals: { vue: 'Vue' }
      }
    }
  }
})

07-build-produccion / 03-code-splitting.md
División automática con import()

Cualquier import() dinámico que Rollup detecte se convierte en un chunk separado. Esto permite cargar código bajo demanda, ideal para rutas, funcionalidades secundarias o widgets pesados.
js

const module = await import('./heavyModule.js')

En producción, heavyModule.js se empaqueta en un archivo con hash, y el código principal solo lo carga cuando se ejecuta la línea. Rollup gestiona el grafo de dependencias para no duplicar código compartido entre chunks.
Manual chunks

A veces quieres agrupar ciertos módulos en chunks específicos, incluso sin import() dinámico. Puedes hacerlo con output.manualChunks:
js

rollupOptions: {
  output: {
    manualChunks: {
      vendor: ['react', 'react-dom'],
      utils: ['lodash', 'axios']
    }
  }
}

O mediante una función que recibe el id del módulo:
js

manualChunks(id) {
  if (id.includes('node_modules/react')) return 'vendor-react'
  if (id.includes('node_modules')) return 'vendor'
}

Esta técnica sirve para aislar dependencias que cambian poco (mejor cacheo) y para controlar el peso de cada chunk.
splitVendorChunkPlugin

Vite proporciona un plugin oficial que separa automáticamente todas las dependencias de node_modules en un chunk vendor:
js

import { splitVendorChunkPlugin } from 'vite'

export default defineConfig({
  plugins: [splitVendorChunkPlugin()]
})

Es la manera más rápida de evitar un chunk principal gigante.
Preload de módulos (modulepreload)

Por defecto, Vite inyecta etiquetas <link rel="modulepreload"> en el HTML para todos los chunks que son dependencias directas de las entradas. Esto indica al navegador que descargue esos chunks en segundo plano mientras se ejecuta la aplicación, mejorando el rendimiento de carga.

Puedes desactivarlo con:
js

build: {
  modulePreload: false
}

O ajustar la resolución de qué precargar con una función:
js

build: {
  modulePreload: {
    resolveDependencies: (filename, deps, { hostId, hostType }) => deps
  }
}

Convenciones de nomenclatura

Los archivos generados siguen el patrón [name].[hash].js. Puedes personalizarlo con entryFileNames, chunkFileNames y assetFileNames en output.
js

output: {
  entryFileNames: 'entries/[name]-[hash].js',
  chunkFileNames: 'chunks/[name]-[hash].js',
  assetFileNames: 'assets/[name]-[hash][extname]'
}

Análisis del bundle

Instala rollup-plugin-visualizer y añádelo a plugins de rollupOptions:
bash

npm add -D rollup-plugin-visualizer

js

import { visualizer } from 'rollup-plugin-visualizer'

build: {
  rollupOptions: {
    plugins: [visualizer({ open: true })]
  }
}

Tras el build, abrirá una página interactiva donde verás el tamaño de cada módulo y podrás identificar dependencias que inflan el bundle.
Estrategias para un splitting óptimo

    Rutas perezosas: en Vue/React, usa () => import('./Page.vue') para que cada página sea su propio chunk.

    Librerías grandes: si una librería como moment o three solo se usa en una sección, asegúrate de importarla dinámicamente en esa sección.

    Caché de larga duración: los chunks de vendor con hash no cambian si no actualizas dependencias, lo que permite al navegador reutilizar la caché.

    No abuses de manualChunks: fragmentar en exceso puede aumentar el overhead de peticiones HTTP. Encuentra un equilibrio.

07-build-produccion / 04-despliegue.md
Estructura de salida lista para producción

Tras vite build, la carpeta dist/ contiene:
text

dist/
├── index.html              (o varias si es MPA)
├── assets/
│   ├── index.abc123.js
│   ├── index.abc123.css
│   ├── vendor.def456.js
│   └── logo.ghi789.png
└── ... (otros archivos de public/)

Los archivos HTML ya referencian a los recursos con las rutas correctas (incluyendo la base configurada). Los assets poseen hash para cacheo inmutable.
Configuración de la ruta base

Si tu aplicación no se sirve desde la raíz del dominio, debes ajustar base:
js

export default defineConfig({
  base: '/miapp/'
})

Esto afecta a todas las URLs generadas dentro del código y a las etiquetas <link> y <script> del HTML. En el despliegue, el servidor debe servir los archivos exactamente bajo ese prefijo.
Base condicional según entorno
js

export default defineConfig(({ mode }) => {
  return {
    base: mode === 'production' ? '/produccion/' : '/'
  }
})

Despliegue como SPA (Single Page Application)

La mayoría de las aplicaciones modernas usan enrutamiento del lado del cliente. Para que las rutas profundas funcionen al refrescar la página, el servidor debe redirigir todas las peticiones no coincidentes con archivos físicos al index.html (fallback).

Ejemplos de configuración:

Nginx:
nginx

location / {
  try_files $uri $uri/ /index.html;
}

Apache (.htaccess):
apache

RewriteEngine On
RewriteBase /
RewriteRule ^index\.html$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]

Netlify: agrega un archivo _redirects en la raíz o en public:
text

/*    /index.html   200

Vercel: automáticamente maneja SPAs; si no, un vercel.json con:
json

{ "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }] }

GitHub Pages: puedes usar un 404.html que redirija (con un script) o habilitar el truco del hash en la URL (no recomendado). La mejor opción es configurar el repositorio con el dominio personalizado y enable "Enforce HTTPS".
Caché y encabezados HTTP

Los archivos con hash (prácticamente todos los que están dentro de assets/) pueden servirse con cabeceras de caché agresiva:
text

Cache-Control: public, max-age=31536000, immutable

El index.html debe tener una política de no caché o validación (ETag) para que el navegador siempre pida la última versión.

En plataformas como Vercel o Netlify, esto se configura automáticamente. Si despliegas en un servidor propio, ajusta el servidor web para que a los archivos con patrón assets/*.[hash].* se les aplique la caché inmutable.
Variables de entorno en producción

Durante vite build, todas las variables con prefijo VITE_ se reemplazan estáticamente en el código. No se necesita un servidor que inyecte las variables en tiempo de ejecución. Por tanto, debes construir la aplicación una vez para cada entorno o usar una variable inyectada externamente (como window.__CONFIG__ inyectada desde un script servidor) si necesitas cambiar configuraciones sin reempaquetar.
Probando el build localmente

Usa vite preview para levantar un servidor local que sirva la carpeta dist. Es ideal para verificar que la aplicación funciona exactamente igual que en producción, incluyendo rutas base y fallbacks SPA.

Puedes también servir con cualquier servidor estático, por ejemplo:
bash

npx serve dist

Despliegues comunes paso a paso

    Vercel: conecta tu repositorio, Vercel detecta Vite automáticamente, ejecuta vite build y despliega la carpeta dist.

    Netlify: arrastra la carpeta dist o conecta el repo, define el comando npm run build y el directorio de publicación dist.

    GitHub Pages: configura un workflow que ejecute vite build y publique la rama gh-pages con el contenido de dist. Recuerda ajustar base según el nombre del repositorio si no usas dominio personalizado.

    AWS S3 + CloudFront: sube dist a un bucket S3, habilita el hosting estático y configura CloudFront para distribución HTTPS. Usa una política de caché personalizada para los archivos hasheados.

    Firebase Hosting: ejecuta firebase init hosting, indica dist como carpeta pública y configura el firebase.json con las reescrituras SPA.

08-avanzado / 01-ssr.md
SSR con Vite

Vite proporciona herramientas de bajo nivel para implementar Server‑Side Rendering sin imponer una estructura fija. La idea es usar el mismo código de la aplicación tanto en el servidor (Node) como en el cliente, pero empaquetados de forma distinta.
Desarrollo con SSR

Durante el desarrollo, puedes levantar un servidor Node personalizado que use el middleware de Vite. Vite transformará el código fuente al vuelo y permitirá HMR incluso del lado del servidor.
Configuración del servidor de desarrollo SSR
js

// server.js (archivo del backend)
import fs from 'node:fs/promises'
import express from 'express'
import { createServer } from 'vite'

const app = express()

const vite = await createServer({
  server: { middlewareMode: true },
  appType: 'custom'
})

app.use(vite.middlewares)

app.get('*', async (req, res) => {
  try {
    const url = req.originalUrl

    // 1. Leer el HTML base
    let template = await fs.readFile('index.html', 'utf-8')
    template = await vite.transformIndexHtml(url, template)

    // 2. Cargar el módulo de entrada del servidor (con HMR)
    const { render } = await vite.ssrLoadModule('/src/entry-server.js')

    // 3. Renderizar la aplicación
    const appHtml = await render(url)

    // 4. Insertar el HTML renderizado en el template
    const html = template.replace(`<!--ssr-outlet-->`, appHtml)

    res.status(200).set({ 'Content-Type': 'text/html' }).end(html)
  } catch (e) {
    vite.ssrFixStacktrace(e)
    res.status(500).end(e.stack)
  }
})

app.listen(3000)

En este esquema, entry-server.js exporta una función render(url) que devuelve el HTML. Cada vez que cambia ese archivo (o sus dependencias), vite.ssrLoadModule devuelve la nueva versión sin reiniciar el proceso Node. El cliente se actualiza vía HMR gracias a vite.middlewares.
Cliente para SSR

El archivo entry-client.js típico:
js

import { createApp } from './main.js'

createApp().mount('#app')

El index.html debe contener un marcador como <!--ssr-outlet--> donde se inyectará el HTML del servidor.
Producción con SSR

Para producción hay que construir dos bundles:

    Bundle del cliente (igual que siempre) con vite build.

    Bundle del servidor que se ejecutará en Node.

Vite permite construir para servidor especificando build.ssr y una entrada distinta:
js

// vite.config.ssr.js
export default defineConfig({
  build: {
    ssr: 'src/entry-server.js', // entrada para el build de servidor
    outDir: 'dist/server'
  }
})

Y se ejecuta con:
bash

vite build --config vite.config.ssr.js

El output será un módulo que puedes importar en tu servidor de producción:
js

import { render } from './dist/server/entry-server.js'

El servidor Express en producción no necesita el middleware Vite; sirve los assets estáticos del build del cliente y renderiza con la función importada.
Externos automáticos

En el build para servidor, Vite externaliza automáticamente todas las dependencias de node_modules. Esto evita empaquetar Express, Vue, etc., y acelera el build. Puedes controlar los externos con ssr.external y ssr.noExternal.
Manejo de CSS durante SSR

Si los componentes importan CSS, durante la renderización en el servidor esos estilos no se inyectan automáticamente. Existen estrategias como recolectar todos los estilos usados durante la renderización (con @vue/server-renderer en Vue, o streaming en React) e insertarlos en el <head> del HTML. Para react, puedes usar renderToString y recolectar las hojas de estilo con librerías como styled-components o emotion.
Plugins específicos para SSR

    Vite-plugin-ssr / Vike: abstrae toda la complejidad del SSR y SSG, permitiendo definir páginas con prerrenderizado, data fetching y layouts. Muy recomendado para proyectos grandes.

    @vitejs/plugin-vue y @vitejs/plugin-react soportan SSR sin configuración adicional; solo debes construir el bundle del servidor con la opción ssr.

08-avanzado / 02-web-workers.md
Inclusión de Workers en Vite

Vite soporta Web Workers de forma nativa mediante dos sintaxis complementarias.
1. Sintaxis new URL (recomendada para ESM)
js

const worker = new Worker(new URL('./worker.js', import.meta.url), { type: 'module' })

Durante el build, Rollup detecta este new URL y empaqueta worker.js como un chunk separado. En desarrollo, la URL apunta directamente al archivo servido por Vite, que lo transforma sobre la marcha.
2. Import con sufijo ?worker

Proporciona una experiencia más declarativa:
js

import MyWorker from './worker.js?worker'
const worker = new MyWorker()

MyWorker es una función constructora que al instanciarse devuelve un Worker real. Internamente, Vite genera la URL correcta y la pasa al constructor Worker. Esta sintaxis también es compatible con tipado TypeScript gracias a vite/client.
Workers compartidos

De forma similar, para Shared Workers:
js

import MySharedWorker from './shared-worker.js?sharedworker'
const shared = new MySharedWorker()

Empaquetado de Workers

Cada Worker se trata como una entrada independiente en Rollup. Esto significa que:

    Se pueden importar módulos dentro del Worker normalmente.

    Las dependencias de node_modules se comparten (deduplican) entre el hilo principal y los Workers, a menos que se dividan manualmente.

    Se aplican las mismas reglas de target, minificación y hashing que al bundle principal.

El nombre del chunk del Worker sigue el patrón [name].[hash].js. Puedes personalizarlo con rollupOptions.output.chunkFileNames o mediante la función fileName en worker (no disponible directamente; se hereda de la configuración general).
Servicio Workers (Service Workers)

Vite no tiene soporte específico para Service Workers porque estos no se construyen desde el mismo grafo de módulos de la aplicación (se registran como un script separado que vive en el scope raíz). Lo habitual es:

    Colocar un sw.js en la carpeta public (no pasará por Vite, se sirve tal cual en la raíz).

    O usar un plugin como vite-plugin-pwa que genera el Service Worker a partir de Workbox, aprovechando el build de Vite.

Variables de entorno en Workers

Las variables con prefijo VITE_ se reemplazan estáticamente también en los Workers. No necesitas ninguna configuración adicional. Puedes usar import.meta.env.VITE_API_URL dentro del Worker como en el hilo principal.
Workers y WebAssembly

Dentro de un Worker, puedes usar la misma sintaxis ?init para cargar módulos .wasm. Vite empaquetará el .wasm como un asset y lo resolverá correctamente en el Worker.
Restricciones / buenas prácticas

    El código del Worker debe estar en un archivo separado (no se puede embeber mediante ?worker inline directamente; se crea un chunk).

    Los Workers se descargan con CORS; si despliegas en un CDN, asegúrate de que los encabezados CORS permitan la carga.

    Para librerías que esperan un Worker desde un string, puedes importar el script con ?raw y luego crear un Blob, pero el import() dinámico no estará disponible allí.

08-avanzado / 03-webassembly.md
Soporte nativo de WebAssembly (WASM) en Vite

Vite maneja archivos .wasm de forma eficiente. Dependiendo del caso de uso, puedes importarlos directamente o mediante el sufijo ?init para módulos que requieren un objeto de imports.
Importación directa (módulos WASM ESM)

Si el archivo .wasm fue compilado con soporte para ESM (por ejemplo, con la opción --target bundler en wasm-pack, o usando wasm-bindgen con la salida web), puedes importarlo directamente:
js

import init, { add } from './math.wasm'
await init()
console.log(add(1, 2))

Vite reconocerá la extensión y emitirá el archivo .wasm como un asset separado. En el build, el código de inicialización se incluye para cargar el wasm correctamente. (Para que esto funcione, el .wasm debe exportar una función init y las funciones prometidas; típico de wasm-pack).
Importación con ?init (control manual)

Si tu módulo Wasm necesita que tú proporciones imports (por ejemplo, un objeto env con funciones), debes usar el sufijo ?init:
js

import init from './math.wasm?init'

const wasmInstance = await init({
  env: {
    memory: new WebAssembly.Memory({ initial: 256 }),
    log: (val) => console.log(val)
  }
})

const { add } = wasmInstance.exports
console.log(add(5, 3))

init es una función que recibe el objeto de imports y devuelve una promesa con la instancia de WebAssembly. Esto te da control total sobre la memoria, los imports y la inicialización.
Inlining de archivos .wasm pequeños

Por defecto, Vite aplica el mismo límite de inlining que para otros assets (assetsInlineLimit, 4 KB). Si un .wasm es menor, se inlineará como una cadena base64 y se cargará mediante WebAssembly.instantiate con un buffer. Esto evita peticiones extra. Puedes ajustar el límite o desactivarlo.
Uso combinado con Workers

Cargar Wasm dentro de un Worker sigue el mismo patrón. El chunk del Worker incluirá el código de carga y el .wasm se copiará como asset compartido.
Configuración adicional

Para opciones más avanzadas (como habilitar top-level await en el Wasm o en el código que lo importa), es posible que necesites ajustar build.target a esnext o configurar el soporte en esbuild con optimizeDeps.esbuildOptions. Vite se encarga automáticamente de las dependencias asíncronas.
Plugins de la comunidad para WASM

Si por algún motivo el soporte nativo no cubre tu caso (por ejemplo, necesitas empaquetar Wasm de manera diferente), existen plugins como vite-plugin-wasm que ofrecen mayor compatibilidad con librerías más antiguas.
08-avanzado / 04-integracion-backend.md
Vite como middleware en un servidor personalizado

Una de las capacidades más poderosas de Vite es que puedes incrustar su servidor de desarrollo dentro de tu propio backend, compartiendo puerto y lógica. Esto permite, por ejemplo, tener una aplicación Express que sirva una API REST y a la vez el frontend en desarrollo con HMR.
Habilitar modo middleware

Configura Vite con middlewareMode: true y appType: 'custom':
js

import express from 'express'
import { createServer } from 'vite'

async function startServer() {
  const app = express()

  // Crea el servidor Vite en modo middleware
  const vite = await createServer({
    server: { middlewareMode: true },
    appType: 'custom'
  })

  // Monta los middlewares de Vite
  app.use(vite.middlewares)

  // Tus rutas de API
  app.get('/api/data', (req, res) => {
    res.json({ msg: 'desde el backend' })
  })

  // ... otras rutas

  app.listen(3000, () => {
    console.log('Servidor en http://localhost:3000')
  })
}

startServer()

El parámetro appType: 'custom' le dice a Vite que no asuma que es una SPA (evita que sirva automáticamente index.html para cada ruta desconocida). Tú te encargas del enrutamiento final.
Fallback SPA en modo middleware

Si deseas que el propio backend maneje el fallback SPA, después de tus rutas API puedes añadir un middleware que sirva el index.html transformado por Vite:
js

app.get('*', async (req, res) => {
  let template = await fs.readFile('index.html', 'utf-8')
  template = await vite.transformIndexHtml(req.url, template)
  res.status(200).set({ 'Content-Type': 'text/html' }).end(template)
})

Así, mientras Vite está en desarrollo, cualquier ruta no capturada por la API devolverá el HTML de la aplicación con HMR activo.
WebSocket y HMR en backend personalizado

El HMR de Vite funciona sobre WebSocket. Al montar vite.middlewares, Vite también adjunta el manejador del WebSocket al servidor HTTP subyacente (si middlewareMode es true, Vite no crea su propio servidor HTTP, sino que usa el que le proporcione Express/Connect). Por ello, el WebSocket de HMR convive sin problemas con tus propias rutas y WebSockets, siempre y cuando no haya conflictos de ruta (Vite usa __vite_hmr).

Si tu servidor Express ya tiene un WebSocket en otra ruta, puedes combinarlos sin interferencias.
Integración con HTTPS y certificados

Para desarrollo con HTTPS, puedes pasar las opciones server.https al crear el servidor Vite. Si estás en modo middleware, debes crear el servidor HTTPS nativo y luego adjuntar la app Express a él, pasando ese servidor a Vite:
js

import https from 'node:https'
import fs from 'node:fs'

const httpsOptions = {
  key: fs.readFileSync('localhost-key.pem'),
  cert: fs.readFileSync('localhost.pem')
}

const httpsServer = https.createServer(httpsOptions, app)

const vite = await createServer({
  server: {
    middlewareMode: true,
    https: true  // Para que Vite configure el HMR con WSS
  },
  appType: 'custom'
})

app.use(vite.middlewares)

httpsServer.listen(3443)

Fíjate que server.https: true habilita que el cliente reciba las URLs con wss://.
Uso programático del build y preview

Puedes invocar build() desde un script de Node para empaquetar la aplicación como parte de un flujo mayor:
js

import { build } from 'vite'

await build({
  base: '/production/',
  mode: 'production',
  // ... más config
})

También puedes iniciar un servidor de preview programáticamente con preview():
js

import { preview } from 'vite'

const server = await preview({
  preview: { port: 8080, open: true }
})
server.printUrls()

Testing con Vitest

Vitest está construido sobre Vite y reutiliza su configuración y plugins. No necesitas una integración adicional; solo crea vite.config.js y los tests lo heredarán. Para más detalles consulta la documentación de Vitest.
Integración en monorepos

En entornos como Nx o Turborepo, puedes separar el frontend (Vite) del backend. En desarrollo, el backend puede levantar Vite programáticamente para que ambos compartan puerto y cookies. En producción, el backend simplemente sirve los archivos estáticos de la carpeta dist generada por Vite.

