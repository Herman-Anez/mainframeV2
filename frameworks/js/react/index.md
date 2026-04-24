📄 jsx.md
¿Qué es JSX?

JSX (JavaScript XML) es una extensión de sintaxis que permite escribir estructuras similares a HTML dentro de código JavaScript. No es obligatorio en React, pero es la forma recomendada por su legibilidad y potencia.
Transformación

JSX se compila (con Babel o swc) a llamadas React.createElement:
jsx

// JSX
const elemento = <h1 className="saludo">Hola, mundo</h1>;

// Compilado
const elemento = React.createElement('h1', { className: 'saludo' }, 'Hola, mundo');

Reglas y características importantes

    Una sola raíz: Todo componente debe devolver un solo elemento envolvente. Puedes usar <Fragment> o <> </>.

    Etiquetas deben cerrarse: <img />, <br />, <input />.

    Expresiones JavaScript entre {}:
    jsx

    const nombre = "Ana";
    const element = <p>Bienvenida {nombre}</p>;

    Atributos con camelCase:

        class → className

        for → htmlFor

        tabindex → tabIndex

    Estilos en línea con objeto:
    jsx

    <div style={{ backgroundColor: 'red', fontSize: '16px' }}>Texto</div>

    Comentarios: {/* comentario */}

JSX como valor

Puedes guardar JSX en variables, devolverlo desde funciones, pasarlo como props.
Seguridad contra inyección XSS

React escapa automáticamente los valores incrustados en JSX antes de renderizarlos. Nunca uses dangerouslySetInnerHTML a menos que confíes plenamente en el contenido.
Buenas prácticas

    Mantén JSX legible, extrae lógica compleja fuera del return.

    Usa paréntesis para envolver JSX multilínea.

    Prefiere fragmentos en lugar de div innecesarios.

📄 componentes.md
Definición

Un componente es una pieza de UI reutilizable e independiente. Puede ser una función o una clase. Recibe props y devuelve JSX.
Componente funcional (moderno)
jsx

function Saludo(props) {
  return <h1>Hola, {props.nombre}</h1>;
}

    Desde React 16.8 pueden usar hooks (estado, efectos, etc.).

    Son más simples y ligeros.

Componente de clase (legado)
jsx

class Saludo extends React.Component {
  render() {
    return <h1>Hola, {this.props.nombre}</h1>;
  }
}

    Necesitan render().

    Usaban this.state y ciclo de vida (componentDidMount, etc.). Hoy se recomienda funciones + hooks.

Tipos de componentes según su función

    Presentacionales (tontos): Solo reciben props y renderizan UI. Sin estado propio.

    Contenedores (inteligentes): Manejan lógica, estado, efectos secundarios.

    Componentes puros: Dado las mismas props, siempre renderizan el mismo JSX.

Reglas importantes

    Los nombres de componentes deben comenzar con mayúscula (distingue de etiquetas HTML).

    Un componente no debe modificar sus props (son de solo lectura).

    Todo componente debe ser una función pura respecto a sus props y estado (para evitar efectos colaterales).

Composición

Se recomienda composición sobre herencia. Puedes anidar componentes y usar props.children:
jsx

function Contenedor({ children }) {
  return <div className="card">{children}</div>;
}

Extracción de componentes

Cuando una parte de la UI se repite o es compleja, conviene extraerla en un componente independiente.
📄 props.md
Concepto

Las props (abreviatura de "properties") son datos de solo lectura que un componente padre pasa al hijo. Fluyen unidireccionalmente (de arriba abajo).
Uso básico
jsx

// Padre
<Saludo nombre="Carlos" edad={30} />

// Hijo
function Saludo(props) {
  return <p>{props.nombre}, edad: {props.edad}</p>;
}

Desestructuración de props (recomendado)
jsx

function Saludo({ nombre, edad }) {
  return <p>{nombre}, edad: {edad}</p>;
}

Props por defecto (defaultProps)
jsx

function Boton({ texto = "Click" }) { ... }
// o externamente:
Boton.defaultProps = { texto: "Click" };

PropTypes (validación de tipos)

Instala prop-types:
jsx

import PropTypes from 'prop-types';

Saludo.propTypes = {
  nombre: PropTypes.string.isRequired,
  edad: PropTypes.number
};

props.children

Para contenido anidado:
jsx

<Card>
  <h2>Título</h2>
  <p>Contenido</p>
</Card>

function Card({ children }) {
  return <div className="card">{children}</div>;
}

Spread de props (usar con cuidado)
jsx

<MiComponente {...objetoDeProps} />

Puede pasar props no deseadas. Prefiere listar explícitamente.
Inmutabilidad

Las props no se pueden modificar dentro del componente hijo. Si necesitas cambiarlas, el padre debe pasar una función modificadora (callback).
Patrón de render props

Pasar una función como prop que devuelve JSX (tema más avanzado, pero mencionar aquí como derivación).
📄 estado-useState.md
Estado local

El estado son datos que un componente puede modificar a lo largo del tiempo, causando un re-renderizado automático cuando cambian.
useState – Hook básico
jsx

import { useState } from 'react';

function Contador() {
  const [contador, setContador] = useState(0);
  // contador = valor actual
  // setContador = función para actualizarlo
}

Reglas de useState

    Solo se puede usar en componentes funcionales o custom hooks.

    Siempre en el mismo orden (no dentro de condicionales o bucles).

    El argumento inicial solo se usa en la primera renderización.

Actualización del estado
jsx

setContador(contador + 1);        // actualización directa
setContador(prev => prev + 1);    // forma segura cuando depende del valor anterior

Estado con objetos o arrays

Debes crear una nueva copia (inmutabilidad):
jsx

const [usuario, setUsuario] = useState({ nombre: 'Ana', edad: 30 });

// Correcto
setUsuario({ ...usuario, edad: 31 });

// Incorrecto (no provoca re-render)
usuario.edad = 31;
setUsuario(usuario);

Estado con arrays
jsx

const [items, setItems] = useState([]);
setItems([...items, nuevoItem]);               // agregar
setItems(items.filter(i => i.id !== id));      // eliminar
setItems(items.map(i => i.id === id ? {...i, done: true} : i));

Múltiples estados

Puedes usar varios useState o un useReducer si son muchas variables relacionadas.
¿Cuándo usar estado?

    Datos que cambian por interacción del usuario (inputs, toggles).

    Datos que se cargan asincrónicamente (fetch).

    Valores que afectan el renderizado.

No guardes en estado lo que se puede calcular
jsx

// Mal
const [precio, setPrecio] = useState(10);
const [conIva, setConIva] = useState(12.1);
// Bien
const conIva = precio * 1.21;

📄 eventos.md
Manejo de eventos en React

Los eventos se nombran en camelCase y se pasan una función (no un string):
jsx

<button onClick={handleClick}>Click</button>

Definir manejadores
jsx

function MiComponente() {
  function handleClick(e) {
    e.preventDefault();  // Previene comportamiento por defecto
    console.log('Clicked');
  }
  return <button onClick={handleClick}>Click</button>;
}

Diferencia con HTML nativo

    No se usa addEventListener, se declara directamente en JSX.

    El objeto e (evento sintético) es compatible con todos los navegadores.

Paso de parámetros
jsx

<button onClick={() => eliminarItem(id)}>Eliminar</button>

Cuidado: crear una nueva función en cada render puede afectar rendimiento. Para casos críticos, usa useCallback.
Eventos comunes

    onClick, onChange, onSubmit, onMouseEnter, onFocus, onBlur, onKeyDown, etc.

Eventos en formularios
jsx

const [texto, setTexto] = useState('');

function handleChange(e) {
  setTexto(e.target.value);
}

<input type="text" value={texto} onChange={handleChange} />

Esto se llama componente controlado.
e.preventDefault() y e.stopPropagation()

Funcionan igual que en DOM nativo.
Eventos personalizados

React no tiene eventos personalizados como Vue; se usan props callback.
Buenas prácticas

    No usar funciones flecha directamente en el render si afectan rendimiento (excepto componentes pequeños).

    Extraer manejadores fuera del JSX para claridad.

📄 renderizado-condicional.md
Formas de renderizar condicionalmente
1. if / else fuera del JSX
jsx

function Componente({ autenticado }) {
  if (autenticado) {
    return <Dashboard />;
  } else {
    return <Login />;
  }
}

2. Operador ternario dentro del JSX
jsx

<div>
  {autenticado ? <Dashboard /> : <Login />}
</div>

3. && lógico (para mostrar o no mostrar)
jsx

<div>
  {autenticado && <Dashboard />}
  {/* Si autenticado es true, muestra Dashboard; si false, no muestra nada */}
</div>

Cuidado: si autenticado es 0 o "" se renderizará ese valor. Mejor usar !!autenticado && ... o convertir a booleano.
4. Variables que contienen JSX
jsx

let contenido;
if (cargando) {
  contenido = <Spinner />;
} else if (error) {
  contenido = <MensajeError />;
} else {
  contenido = <Datos />;
}
return <div>{contenido}</div>;

5. Retorno anticipado (early return) en componentes
jsx

function Lista({ items }) {
  if (!items.length) {
    return <p>No hay elementos</p>;
  }
  return <ul>{items.map(...)}</ul>;
}

Comparación de patrones

    Ternario: cuando hay dos opciones claras.

    &&: para mostrar u ocultar un solo elemento.

    If/else o early return: cuando hay muchas condiciones o el JSX es extenso.

Renderizado condicional con switch
jsx

function Estado({ status }) {
  switch(status) {
    case 'loading': return <Spinner />;
    case 'error': return <Error />;
    default: return <Ok />;
  }
}

No usar && con números
jsx

{contador && <p>Valor: {contador}</p>}
// Si contador === 0, renderiza "0" (porque 0 es falsy pero React lo muestra)
// Solución: {contador !== 0 && ...}

📄 listas-keys.md
Renderizado de listas con map()
jsx

const nombres = ['Ana', 'Luis', 'Carlos'];
<ul>
  {nombres.map(nombre => <li key={nombre}>{nombre}</li>)}
</ul>

La prop key

    Ayuda a React a identificar qué elementos cambiaron, se añadieron o eliminaron.

    Debe ser única entre hermanos.

    Estable (no cambia entre renders).

    No usar índices del array como key si la lista es dinámica (reordenamiento, inserciones/eliminaciones). Los índices pueden causar bugs sutiles.

Buenas prácticas para keys
jsx

// Ideal: usar id único del objeto
{usuarios.map(usuario => <li key={usuario.id}>{usuario.nombre}</li>)}

// Aceptable solo si la lista es estática y sin filtrados/reordenamientos
{items.map((item, index) => <li key={index}>{item}</li>)}

¿Qué pasa si no pongo key?

React mostrará una advertencia y usará el índice por defecto, lo que puede causar problemas de rendimiento y estado incorrecto.
key no es accesible como prop

No puedes leer props.key en el componente hijo. React la usa internamente.
Fragmentos con key
jsx

<>
  {lista.map(item => (
    <React.Fragment key={item.id}>
      <dt>{item.term}</dt>
      <dd>{item.description}</dd>
    </React.Fragment>
  ))}
</>

Extraer componentes en listas
jsx

function Lista({ items }) {
  return (
    <ul>
      {items.map(item => <ItemComponent key={item.id} item={item} />)}
    </ul>
  );
}

Uso de filter antes de map
jsx

{tareas.filter(t => t.completada).map(t => <Tarea key={t.id} {...t} />)}

📄 estilos/css-modules.md
CSS Modules

Permite escribir CSS con ámbito local (por componente). Evita colisiones de nombres.
Configuración

Create React App y Vite lo soportan por defecto. Los archivos deben terminar en .module.css.
Uso
css

/* Boton.module.css */
.boton {
  background: blue;
  color: white;
}
.primario {
  background: green;
}

jsx

import styles from './Boton.module.css';

function Boton() {
  return <button className={styles.boton}>Click</button>;
}

Clases múltiples
jsx

<button className={`${styles.boton} ${styles.primario}`}>
  Click
</button>
// o usando arrays y join

Combinación con props
jsx

<button className={`${styles.boton} ${props.importante ? styles.importante : ''}`}>

Ventajas

    Estilos encapsulados, sin fugas.

    Nombres de clase legibles (se generan hashes).

    Funciona con CSS puro.

Desventajas

    No tiene características de CSS-in-JS (temas dinámicos complejos).

    Los nombres se vuelven verbosos en el JSX.

Alternativa: SCSS Modules

Usa Boton.module.scss y tendrás anidación, variables, etc.
📄 estilos/styled-components.md
Styled-components (CSS-in-JS)

Librería para escribir CSS dentro de JavaScript, creando componentes estilizados.
Instalación
bash

npm install styled-components

Uso básico
jsx

import styled from 'styled-components';

const Boton = styled.button`
  background: blue;
  color: white;
  padding: 10px;
  border-radius: 5px;

  &:hover {
    background: darkblue;
  }
`;

function App() {
  return <Boton>Click</Boton>;
}

Adaptación basada en props
jsx

const Boton = styled.button`
  background: ${props => props.primario ? 'green' : 'gray'};
`;

<Boton primario>Guardar</Boton>

Estilos anidados y pseudoclases

Soporta sintaxis similar a SCSS: &:hover, & > span, etc.
Extender estilos
jsx

const BotonGrande = styled(Boton)`
  font-size: 24px;
`;

Ventajas

    Estilos completamente encapsulados.

    Temas dinámicos con ThemeProvider.

    Props controlan los estilos directamente.

    Elimina clases CSS globales.

Desventajas

    Añade runtime (aunque se puede compilar con babel-plugin-styled-components).

    Mayor curva de aprendizaje.

    Puede complicar el debugging en herramientas de navegador.

Uso con attrs
jsx

const Input = styled.input.attrs(props => ({
  type: 'text',
  placeholder: props.placeholder || 'Escribe algo'
}))`
  border: 1px solid #ccc;
`;

Temas
jsx

import { ThemeProvider } from 'styled-components';

const tema = { primary: 'blue' };
<ThemeProvider theme={tema}>
  <App />
</ThemeProvider>

// En el componente
const Boton = styled.button`
  background: ${props => props.theme.primary};
`;

📄 estilos/tailwind.md
Tailwind CSS

Framework de utilidades (utility-first) que proporciona clases CSS atómicas.
Configuración rápida en React
bash

npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

Configurar tailwind.config.js con las rutas de tus componentes:
js

content: ['./src/**/*.{js,jsx,ts,tsx}'],

Importar Tailwind en index.css:
css

@tailwind base;
@tailwind components;
@tailwind utilities;

Uso básico
jsx

function Boton() {
  return (
    <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700">
      Click
    </button>
  );
}

Ventajas

    No necesitas escribir CSS personalizado.

    Muy rápido de desarrollar.

    Bundle pequeño (purga clases no usadas en producción).

    Diseño consistente gracias a la configuración de tema.

Desventajas

    JSX se vuelve verboso (puedes extraer componentes).

    Curva de aprendizaje de las clases.

    Dependencia de un framework de utilidades.

Extracción de componentes con @apply

En tu archivo CSS (si usas @layer components):
css

.btn-primary {
  @apply bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700;
}

Integración con clsx o classnames

Para combinar clases condicionalmente:
jsx

import clsx from 'clsx';
<div className={clsx('base-class', { 'bg-red': error, 'bg-green': success })} />

Plugins útiles

    @tailwindcss/forms – para resetear estilos de formularios.

    @tailwindcss/typography – para contenido HTML rico (blog, etc.).

Personalización

En tailwind.config.js puedes extender colores, fuentes, breakpoints, etc.
🧠 Resumen de buenas prácticas generales

    Organiza los estilos según la estrategia que elijas: no mezcles CSS Modules con Tailwind a menos que tengas una razón fuerte.

    Prefiere componentes pequeños y reutilizables.

    Nombres claros para props y estados.

    Mantén los archivos cerca de su componente (cada carpeta de componente puede tener su Componente.jsx, Componente.module.css, etc.).

    Documenta decisiones en tus archivos markdown para futuras consultas.

📄 useState.md

    Nota: Aunque useState ya se introdujo en 1-basics/estado-useState.md, aquí se profundiza en aspectos más avanzados y patrones.

Concepto avanzado

useState es el hook fundamental para manejar estado local en componentes funcionales. React garantiza que el valor del estado se mantenga entre renders y que al actualizarlo se programe un nuevo render.
Formas de inicialización
Inicialización directa
jsx

const [count, setCount] = useState(0);

Inicialización diferida (lazy initialization)

Cuando el estado inicial requiere un cálculo costoso, pasa una función:
jsx

const [state, setState] = useState(() => {
  const valorInicial = calcularValorCostoso();
  return valorInicial;
});

Esta función solo se ejecutará en el primer render.
Actualizaciones basadas en el estado anterior

Siempre que la nueva dependa del valor previo, usa la forma funcional para evitar bugs por closures obsoletos:
jsx

setCount(prevCount => prevCount + 1);

Actualizaciones de objetos y arrays (inmutabilidad)

React compara el estado anterior con el nuevo por referencia (Object.is). Si mutas el objeto, la referencia no cambia y React no re-renderiza.

Forma correcta con objetos:
jsx

const [user, setUser] = useState({ name: 'Juan', age: 30 });
setUser({ ...user, age: 31 });        // spread
setUser(prev => ({ ...prev, age: 31 }));

Con arrays:
jsx

const [list, setList] = useState([]);
// Agregar
setList([...list, nuevoElemento]);
setList(prev => [...prev, nuevoElemento]);

// Eliminar por id
setList(prev => prev.filter(item => item.id !== id));

// Actualizar un elemento
setList(prev => prev.map(item => item.id === id ? { ...item, done: true } : item));

¿El setter es asíncrono?

setState es asíncrono. React agrupa múltiples actualizaciones para mejorar rendimiento. No confíes en que el estado cambie inmediatamente después de llamar al setter.
jsx

setCount(count + 1);
console.log(count); // todavía el valor anterior

Si necesitas leer el valor justo después de actualizar, usa useEffect con dependencia en ese estado.
Múltiples estados vs un solo objeto

    Varios useState: más legible para estados no relacionados.

    Un objeto con useState: útil para estados que siempre cambian juntos (ej. formulario). Pero cuidado: al actualizar debes esparcir todo el objeto.

Estado derivado (no lo guardes en el estado)
jsx

// Mal
const [precio, setPrecio] = useState(100);
const [conIva, setConIva] = useState(121); // derivado

// Bien
const conIva = precio * 1.21;

useState vs useReducer

    useState: para estado simple (boolean, número, string, objeto pequeño).

    useReducer: para estado complejo con múltiples sub-valores o transiciones interdependientes.

Buenas prácticas

    Nombra el estado y su setter con [algo, setAlgo].

    Mantén el estado lo más atómico posible.

    Extrae lógica de actualización compleja a funciones aparte o custom hooks.

📄 useEffect.md
Concepto

useEffect permite realizar efectos secundarios en componentes funcionales. Sustituye a los métodos de ciclo de vida de clases (componentDidMount, componentDidUpdate, componentWillUnmount).
Sintaxis básica
jsx

useEffect(() => {
  // efecto aquí
  return () => {
    // cleanup (opcional)
  };
}, [dependencias]);

Formas según el array de dependencias
1. Sin dependencias (ejecuta en cada render)
jsx

useEffect(() => {
  console.log('Se ejecuta después de cada render');
});

Evitar a menos que sea estrictamente necesario (problemas de rendimiento).
2. Array vacío [] (solo montaje y desmontaje)
jsx

useEffect(() => {
  console.log('Solo al montar');
  return () => console.log('Al desmontar');
}, []);

Útil para suscripciones, event listeners, fetch inicial.
3. Con dependencias (se ejecuta cuando cambian)
jsx

useEffect(() => {
  document.title = `Has clickeado ${count} veces`;
}, [count]);

Efecto con cleanup (limpieza)

Previene memory leaks. Se ejecuta antes de desmontar y antes de la próxima ejecución del efecto.
jsx

useEffect(() => {
  const id = setInterval(() => setTime(Date.now()), 1000);
  return () => clearInterval(id);
}, []);

Casos comunes
Fetch de datos
jsx

useEffect(() => {
  let ignore = false;
  async function fetchData() {
    const response = await fetch(url);
    const data = await response.json();
    if (!ignore) setData(data);
  }
  fetchData();
  return () => { ignore = true; }; // evita actualizar estado si componente desmontó
}, [url]);

Suscripción a eventos
jsx

useEffect(() => {
  const handleResize = () => setWidth(window.innerWidth);
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);

Reglas importantes

    No llames a useEffect dentro de condicionales o bucles.

    No hagas async directamente en el callback (debe devolver función de cleanup o undefined). Usa función interna.

    Si la dependencia es un objeto o función definida dentro del componente, puede causar bucles infinitos. Usa useCallback o useMemo.

Efectos que se ejecutan antes del paint: useLayoutEffect

Si necesitas medir el DOM o mutar elementos antes de que el navegador pinte, usa useLayoutEffect. Más adelante se detalla.
Advertencia de dependencias faltantes (eslint-plugin-react-hooks)
jsx

useEffect(() => {
  setCount(count + 1); // count debería estar en dependencias
}, []); // ❌ warning

Solución: incluye count o usa la forma funcional setCount(prev => prev + 1).
Ciclo de vida completo

    Montaje: se ejecuta el efecto.

    Actualización: si cambian dependencias, se ejecuta cleanup anterior y luego el nuevo efecto.

    Desmontaje: se ejecuta cleanup.

Buenas prácticas

    Cada efecto debe tener una responsabilidad única (separar varios useEffect).

    Usar dependencias correctas para evitar renders innecesarios.

    Para fetching, considera librerías como React Query que abstraen efectos.

📄 useContext.md
Concepto

useContext permite consumir un contexto creado con React.createContext sin necesidad de usar Context.Consumer o anidar componentes.
Creación del contexto
jsx

// TemaContext.js
import { createContext } from 'react';
export const TemaContext = createContext('claro'); // valor por defecto

Proveer el contexto
jsx

import { TemaContext } from './TemaContext';

function App() {
  return (
    <TemaContext.Provider value="oscuro">
      <ComponenteHijo />
    </TemaContext.Provider>
  );
}

Consumir con useContext
jsx

import { useContext } from 'react';
import { TemaContext } from './TemaContext';

function ComponenteHijo() {
  const tema = useContext(TemaContext);
  return <div className={`tema-${tema}`}>Contenido</div>;
}

Contexto con estado mutable
jsx

const AuthContext = createContext(null);

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const login = (userData) => setUser(userData);
  const logout = () => setUser(null);
  
  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

Ventajas

    Evita props drilling (pasar props por muchos niveles).

    Centraliza datos globales: tema, autenticación, idioma, etc.

Desventajas y limitaciones

    No es un sistema de gestión de estado completo: los cambios en el contexto causan re-render de todos los consumidores, sin mecanismo de memoización por defecto.

    Para rendimiento, combínalo con useMemo en el valor del provider.

jsx

const value = useMemo(() => ({ user, login, logout }), [user]);
<AuthContext.Provider value={value}>

Contexto múltiple

Puedes anidar varios providers. Cada useContext obtiene el contexto más cercano en el árbol.
Uso con useReducer (mini Redux)
jsx

const StoreContext = createContext();

function StoreProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <StoreContext.Provider value={{ state, dispatch }}>
      {children}
    </StoreContext.Provider>
  );
}

Buenas prácticas

    Crear contextos específicos (no un solo contexto gigante).

    Exportar un custom hook para consumir el contexto (más limpio):

jsx

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth debe usarse dentro de AuthProvider');
  return context;
}

📄 useRef.md
Concepto

useRef crea un objeto mutable .current que persiste durante todo el ciclo de vida del componente. Cambiar .current no causa re-render.
Usos principales
1. Acceso directo a elementos del DOM
jsx

function InputFocus() {
  const inputRef = useRef(null);
  
  const focusInput = () => {
    inputRef.current.focus();
  };
  
  return (
    <>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Enfocar</button>
    </>
  );
}

2. Guardar valores mutables que no deben causar re-render
jsx

function Timer() {
  const intervalRef = useRef();
  
  useEffect(() => {
    intervalRef.current = setInterval(() => {
      console.log('tick');
    }, 1000);
    return () => clearInterval(intervalRef.current);
  }, []);
}

3. Referencia a valores previos (como "prevProps" o "prevState")
jsx

function usePrevious(value) {
  const ref = useRef();
  useEffect(() => {
    ref.current = value;
  }, [value]);
  return ref.current;
}

Diferencias con useState
Característica	useState	useRef
Cambio provoca re-render	Sí	No
Valor persiste entre renders	Sí	Sí
Síncrono o asíncrono	Asíncrono (batch)	Síncrono (mutación directa)
ref como prop: forwardRef

Para pasar una ref a un componente hijo, usa forwardRef:
jsx

const InputConRef = forwardRef((props, ref) => {
  return <input ref={ref} {...props} />;
});

// Padre
const inputRef = useRef();
<InputConRef ref={inputRef} />

Callback ref (más control)
jsx

const [medidas, setMedidas] = useState(null);
const refCallback = (node) => {
  if (node !== null) {
    setMedidas(node.getBoundingClientRect());
  }
};
<div ref={refCallback}>...</div>

Casos avanzados

    Medir elementos DOM: combínalo con useLayoutEffect para leer dimensiones antes del paint.

    Evitar recreación de callbacks: si usas callback ref, memoízala con useCallback.

Advertencias

    No abuses de ref para "solución rápida" cuando deberías usar estado.

    Mutar .current no es reactivo; si necesitas que algo cambie en la UI, usa estado.

📄 useReducer.md
Concepto

useReducer es una alternativa a useState para manejar estados complejos con múltiples sub-valores o transiciones que dependen de acciones. Está inspirado en Redux.
Sintaxis
jsx

const [state, dispatch] = useReducer(reducer, initialState, init);

    reducer: función pura (state, action) => newState.

    initialState: valor inicial.

    init (opcional): función para inicialización diferida.

Ejemplo básico: contador
jsx

const initialState = { count: 0 };

function reducer(state, action) {
  switch (action.type) {
    case 'increment': return { count: state.count + 1 };
    case 'decrement': return { count: state.count - 1 };
    case 'reset': return initialState;
    default: throw new Error();
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <>
      Count: {state.count}
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
    </>
  );
}

Acciones con payload
jsx

function reducer(state, action) {
  switch (action.type) {
    case 'set':
      return { count: action.payload };
    default:
      return state;
  }
}
// uso
dispatch({ type: 'set', payload: 10 });

Inicialización diferida
jsx

function init(initialCount) {
  return { count: initialCount };
}
const [state, dispatch] = useReducer(reducer, initialCount, init);

¿Cuándo usar useReducer sobre useState?

    Cuando el próximo estado depende del anterior de forma compleja.

    Cuando tienes múltiples campos que se actualizan juntos (ej. formulario grande).

    Cuando la lógica de actualización es difícil de seguir con varios useState.

    Prefieres un patrón de acciones predecible.

Combinación con useContext (mini Redux)
jsx

const AppContext = createContext();

function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);
  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

Tipado con TypeScript (útil aunque no obligatorio)
tsx

type State = { count: number };
type Action = { type: 'increment' } | { type: 'decrement' };

const reducer = (state: State, action: Action): State => { ... };

Buenas prácticas

    Los reducers deben ser puros (sin efectos secundarios, sin mutar state).

    Usa constantes para los tipos de acción (ej. const INCREMENT = 'increment').

    Separa reducers en archivos diferentes para lógica compleja.

Comparación de rendimiento

useReducer evita pasar callbacks por muchos niveles (en lugar de setState puedes pasar dispatch). Es más eficiente para actualizaciones profundas.
📄 useMemo-useCallback.md
Concepto

Ambos hooks memorizan valores/funciones para evitar recrearlos en cada render, optimizando el rendimiento.
useMemo – Memoriza valores
jsx

const valorMemoizado = useMemo(() => computoCostoso(a, b), [a, b]);

    Devuelve el resultado de la función.

    Solo se recalcula cuando cambian las dependencias.

Ejemplo práctico
jsx

function Lista({ items, filtro }) {
  const itemsFiltrados = useMemo(() => {
    return items.filter(item => item.includes(filtro));
  }, [items, filtro]);
  
  return <ul>{itemsFiltrados.map(...)}</ul>;
}

useCallback – Memoriza funciones
jsx

const funcionMemoizada = useCallback(() => {
  hacerAlgo(a, b);
}, [a, b]);

    Devuelve la misma referencia de función entre renders si las dependencias no cambian.

    Evita que componentes hijos (optimizados con React.memo) se re-rendericen innecesariamente.

Ejemplo
jsx

const handleClick = useCallback(() => {
  console.log(count);
}, [count]);

<BotonMemo onClick={handleClick} />

Diferencia clave
Hook	Qué memoriza	Uso típico
useMemo	Valor calculado	Operaciones costosas, objetos/arrays derivados
useCallback	Función	Pasar callbacks a hijos memoizados
¿Cuándo NO usarlos?

    No los uses en todos lados (la optimización prematura es mala).

    Si el cálculo es barato (sumas, concatenaciones), no vale la pena.

    Si el componente no tiene problemas de rendimiento, evita complejidad.

Trampa común
jsx

// ❌ Mal: useCallback para una función que se pasa a un div nativo (no memoizado)
const handleClick = useCallback(() => {}, []);
<div onClick={handleClick} />

// ✅ Bien: solo cuando el hijo está envuelto en React.memo
const HijoMemo = React.memo(({ onClick }) => ...);

useMemo para objetos que son dependencia de otros hooks
jsx

const opciones = useMemo(() => ({ pageSize, sortBy }), [pageSize, sortBy]);
useEffect(() => {
  fetchData(opciones);
}, [opciones]); // ahora la referencia es estable

Reglas de dependencias

Al igual que useEffect, las dependencias deben incluir todos los valores reactivos usados dentro.
Diferencia con React.memo

    React.memo evita re-render del componente si sus props no cambiaron (comparación superficial).

    useCallback y useMemo evitan que las props (funciones/objetos) cambien innecesariamente.

Buenas prácticas

    Medir primero (React DevTools Profiler) antes de optimizar.

    Preferir useCallback/useMemo solo en hot paths (listas grandes, animaciones).

    Para funciones que no dependen de estado/props, definirlas fuera del componente (mejor aún).

📄 custom-hooks.md
Concepto

Un custom hook es una función JavaScript cuyo nombre comienza con use y que puede llamar a otros hooks. Permite reutilizar lógica con estado entre componentes.
Reglas

    Debe empezar con use (convención para que React pueda verificar reglas de hooks).

    Solo puede llamar hooks en el nivel superior.

    Puede recibir argumentos y devolver cualquier valor.

Ejemplo simple: useLocalStorage
jsx

function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });
  
  const setValue = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.log(error);
    }
  };
  
  return [storedValue, setValue];
}

Ejemplo: useFetch
jsx

function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    let ignore = false;
    const fetchData = async () => {
      try {
        setLoading(true);
        const res = await fetch(url);
        const json = await res.json();
        if (!ignore) {
          setData(json);
          setError(null);
        }
      } catch (err) {
        if (!ignore) setError(err);
      } finally {
        if (!ignore) setLoading(false);
      }
    };
    fetchData();
    return () => { ignore = true; };
  }, [url]);
  
  return { data, loading, error };
}

Ejemplo: useOnClickOutside (detectar clic fuera de un elemento)
jsx

function useOnClickOutside(ref, handler) {
  useEffect(() => {
    const listener = (event) => {
      if (!ref.current || ref.current.contains(event.target)) return;
      handler(event);
    };
    document.addEventListener('mousedown', listener);
    document.addEventListener('touchstart', listener);
    return () => {
      document.removeEventListener('mousedown', listener);
      document.removeEventListener('touchstart', listener);
    };
  }, [ref, handler]);
}

Composición de custom hooks

Puedes combinar varios hooks dentro de uno:
jsx

function useUser(userId) {
  const { data: user, loading, error } = useFetch(`/users/${userId}`);
  const [preferences, setPrefs] = useLocalStorage(`prefs_${userId}`, {});
  return { user, loading, error, preferences, setPrefs };
}

Buenas prácticas

    Un solo propósito por custom hook.

    Devolver un objeto con valores nombrados (en lugar de array) cuando hay más de dos valores.

    Escribir pruebas para custom hooks con renderHook (React Testing Library).

    Documentar los parámetros y el retorno.

Custom hooks vs componentes

    Los custom hooks no devuelven JSX, solo lógica con estado.

    Si necesitas reutilizar UI + lógica, crea un componente. Si solo lógica, custom hook.

📄 otros-hooks.md (useId, useLayoutEffect, useImperativeHandle, useDebugValue, useTransition, useSyncExternalStore)
useId

Genera identificadores únicos estables para accesibilidad (atributos id). Evita problemas de hidratación en SSR.
jsx

function Campo() {
  const id = useId();
  return (
    <>
      <label htmlFor={id}>Nombre:</label>
      <input id={id} type="text" />
    </>
  );
}

    No usar para keys en listas.

    Cada llamada produce un ID único entre componentes.

useLayoutEffect

Similar a useEffect, pero se ejecuta síncronamente después de mutar el DOM y antes de que el navegador pinte. Útil para medir el DOM o hacer ajustes visuales inmediatos.
jsx

useLayoutEffect(() => {
  const { height } = ref.current.getBoundingClientRect();
  setAltura(height);
}, []);

Precaución: Bloquea el paint, puede degradar rendimiento. Usa useEffect por defecto.
useImperativeHandle

Personaliza el valor expuesto por una ref cuando se usa forwardRef. Permite controlar qué métodos o propiedades expones.
jsx

const FancyInput = forwardRef((props, ref) => {
  const inputRef = useRef();
  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
    customClear: () => { inputRef.current.value = ''; }
  }));
  return <input ref={inputRef} {...props} />;
});

// Padre
const ref = useRef();
<FancyInput ref={ref} />
ref.current.focus(); // válido
ref.current.customClear();

useDebugValue

Etiqueta un custom hook en React DevTools. Solo útil para depuración.
jsx

function useFriendStatus(friendID) {
  const [isOnline, setIsOnline] = useState(null);
  useDebugValue(isOnline ? 'Online' : 'Offline');
  return isOnline;
}

Para valores costosos, acepta una función de formato:
jsx

useDebugValue(date, date => date.toDateString());

useTransition (React 18+)

Marca una actualización de estado como no urgente (transición), permitiendo que el UI siga respondiendo mientras se renderiza contenido pesado.
jsx

const [isPending, startTransition] = useTransition();

const handleSearch = (input) => {
  startTransition(() => {
    setSearchQuery(input); // actualización "lenta"
  });
};

return (
  <div>
    <input onChange={e => handleSearch(e.target.value)} />
    {isPending && <Spinner />}
    <Resultados query={searchQuery} />
  </div>
);

useSyncExternalStore

Hook avanzado para suscribirse a fuentes de datos externas (store de Redux, estado global no React). Recomendado para autores de librerías.
jsx

const state = useSyncExternalStore(store.subscribe, store.getState);

useDeferredValue (mencionar breve)

Similar a useTransition pero para valores: recibe un valor y devuelve una versión "desfasada" que se actualiza en segundo plano.
Conclusión

Estos hooks cubren la mayoría de casos de uso. Para más detalles, consulta la documentación oficial de React (especialmente la sección de Hooks API Reference).

📄 props-drilling.md
Concepto

Props drilling (o "perforación de props") es la situación en la que datos deben pasar a través de múltiples niveles de componentes intermedios que no necesitan esos datos, solo para llegar a un componente profundo que sí los necesita.
Ejemplo del problema
jsx

function App() {
  const [user, setUser] = useState({ name: 'Ana' });
  return <Header user={user} />;
}

function Header({ user }) {
  return <Navbar user={user} />;
}

function Navbar({ user }) {
  return <Avatar user={user} />;
}

function Avatar({ user }) {
  return <img src={user.avatar} />;
}

Aquí Header y Navbar solo pasan user sin usarlo directamente.
¿Por qué es problemático?

    Código frágil: si cambias la estructura de componentes, tienes que modificar todos los intermediarios.

    Difícil de mantener: componentes intermedios reciben props que no les conciernen.

    Dificulta la refactorización.

    Ruido visual: el código se vuelve verboso.

Señales de que necesitas otra solución

    Una prop pasa por más de 2-3 niveles sin ser usada.

    Muchos componentes comparten el mismo dato global (tema, autenticación, idioma).

    El árbol de componentes es profundo y anidado.

Soluciones a props drilling
1. Composición (elevar el contenido)

En lugar de pasar datos a través de intermediarios, pasa el componente ya construido.
jsx

function App() {
  const [user, setUser] = useState({ name: 'Ana' });
  return <Header avatar={<Avatar user={user} />} />;
}
function Header({ avatar }) {
  return <Navbar avatar={avatar} />;
}
function Navbar({ avatar }) {
  return <div>{avatar}</div>;
}

Sigue habiendo cierto drilling, pero más controlado.
2. Context API

Provee el dato en un nivel alto y lo consume donde sea necesario. (Ver siguiente archivo)
3. Estado global con librerías (Redux, Zustand, etc.)
4. Patrón de render props o children como función (menos común hoy)
Buenas prácticas

    No optimices prematuramente: para 2 niveles, props drilling está bien.

    Agrupa datos relacionados en un objeto para pasar menos props.

    Extrae componentes: si un componente intermedio solo pasa props, quizás puede ser eliminado o fusionado.

📄 context-api.md
Concepto

Context API es una característica nativa de React que permite compartir datos globalmente sin tener que pasar props manualmente en cada nivel.
Creación y uso (repaso pero más profundo)
1. Crear contexto
jsx

import { createContext } from 'react';
const UserContext = createContext(null);

2. Proveedor
jsx

function App() {
  const [user, setUser] = useState(null);
  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Dashboard />
    </UserContext.Provider>
  );
}

3. Consumir en cualquier componente hijo
jsx

import { useContext } from 'react';
function Avatar() {
  const { user } = useContext(UserContext);
  return <img src={user?.avatar} />;
}

Contexto con estado complejo y reducción de re-renderizados

Por defecto, cualquier cambio en el value del provider provoca que todos los consumidores se re-rendericen. Para evitarlo:

    Contextos separados para datos que cambian independientemente.

    Memoizar el value con useMemo:

jsx

const value = useMemo(() => ({ user, setUser }), [user]);
<UserContext.Provider value={value}>...</UserContext.Provider>

Contexto múltiple (anidado)

Puedes tener contextos de tema, autenticación, preferencias, etc., anidados.
Contexto + useReducer (mini Redux)
jsx

const StoreContext = createContext();
function StoreProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);
  const value = useMemo(() => ({ state, dispatch }), [state]);
  return <StoreContext.Provider value={value}>{children}</StoreContext.Provider>;
}
// Uso
const { state, dispatch } = useContext(StoreContext);

Contexto vs Redux
Contexto	Redux
Nativo de React	Librería externa
Bueno para datos estáticos o poco frecuentes	Para lógica compleja y actualizaciones frecuentes
Re-renderiza todos los consumidores por defecto	Actualizaciones selectivas
Sin herramientas de debugging avanzadas	DevTools potentes
Buenas prácticas

    Crear custom hooks para consumir contexto (ej. useUser()).

    Validar que el hook se use dentro del provider:

jsx

export function useUser() {
  const context = useContext(UserContext);
  if (!context) throw new Error('useUser must be used within UserProvider');
  return context;
}

    No meter datos que cambian muy rápido (ej. posición del mouse) en un contexto grande.

    Dividir contextos por dominio (UserContext, ThemeContext, etc.).

Limitaciones

    No es adecuado para rendimiento crítico con miles de actualizaciones por segundo (usa Zustand o Jotai).

    El provider debe envolver todo el árbol que necesite acceso.

📄 redux.md
Concepto

Redux es una librería de gestión de estado global predecible basada en el patrón Flux. Se usa frecuentemente con React a través de react-redux.
Principios fundamentales

    Única fuente de verdad: el estado global vive en un solo store.

    El estado es de solo lectura: solo se modifica emitiendo acciones.

    Los cambios se hacen con funciones puras (reducers).

Flujo básico de Redux
text

Componente → dispatch(action) → Reducer → Nuevo estado → Componente se actualiza

Núcleo de Redux (sin React)
jsx

import { createStore } from 'redux';

// Reducer
const contadorReducer = (state = 0, action) => {
  switch (action.type) {
    case 'INCREMENTAR': return state + 1;
    case 'DECREMENTAR': return state - 1;
    default: return state;
  }
};

// Store
const store = createStore(contadorReducer);

// Dispatch
store.dispatch({ type: 'INCREMENTAR' });

// Suscripción
store.subscribe(() => console.log(store.getState()));

Redux con React (react-redux)
1. Proveer el store
jsx

import { Provider } from 'react-redux';
import { store } from './store';

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
);

2. Conectar un componente (hooks modernos)
jsx

import { useSelector, useDispatch } from 'react-redux';

function Contador() {
  const count = useSelector(state => state.contador);
  const dispatch = useDispatch();
  return (
    <div>
      {count}
      <button onClick={() => dispatch({ type: 'INCREMENTAR' })}>+</button>
    </div>
  );
}

Redux Toolkit (recomendado hoy)

Simplifica la configuración, reduce boilerplate.
jsx

import { configureStore, createSlice } from '@reduxjs/toolkit';

const contadorSlice = createSlice({
  name: 'contador',
  initialState: 0,
  reducers: {
    incrementar: state => state + 1,
    decrementar: state => state - 1,
    incrementarPor: (state, action) => state + action.payload,
  },
});

export const { incrementar, decrementar, incrementarPor } = contadorSlice.actions;
export const store = configureStore({ reducer: contadorSlice.reducer });

En el componente:
jsx

import { incrementar } from './store';
dispatch(incrementar());

Middleware (ej. Redux Thunk para acciones asíncronas)
jsx

const fetchUser = (id) => async (dispatch) => {
  dispatch({ type: 'FETCH_USER_REQUEST' });
  try {
    const response = await fetch(`/users/${id}`);
    const data = await response.json();
    dispatch({ type: 'FETCH_USER_SUCCESS', payload: data });
  } catch (error) {
    dispatch({ type: 'FETCH_USER_FAILURE', error });
  }
};

Buenas prácticas

    Usa Redux Toolkit siempre.

    Mantén los reducers planos y combínalos con combineReducers.

    No guardes datos derivados o no serializables (clases, funciones) en el store.

    Usa Selectors memoizados con createSelector (Reselect) para evitar cálculos innecesarios.

Cuándo usar Redux

    Estado global muy complejo y compartido por muchos componentes.

    Actualizaciones frecuentes (colaboración en tiempo real, juegos).

    Necesitas time-travel debugging o persistencia avanzada.

    Equipo grande que requiere patrones estrictos.

Alternativas modernas más ligeras

    Zustand (siguiente archivo), Jotai, Recoil.

📄 zustand.md
Concepto

Zustand es una librería de estado global minimalista para React. Su API es muy simple, sin boilerplate, basada en hooks y sin necesidad de Provider (aunque opcional).
Instalación
bash

npm install zustand

Crear un store
jsx

import { create } from 'zustand';

const useCounterStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));

Usar en un componente
jsx

function Contador() {
  const { count, increment, decrement } = useCounterStore();
  return (
    <div>
      {count}
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}

Selección parcial (evita re-renderizados innecesarios)
jsx

const count = useCounterStore((state) => state.count);
const increment = useCounterStore((state) => state.increment);

O con un selector:
jsx

const { count, increment } = useCounterStore((state) => ({
  count: state.count,
  increment: state.increment,
}), shallow); // comparación superficial

Estado asíncrono
jsx

const useUserStore = create((set) => ({
  user: null,
  loading: false,
  fetchUser: async (id) => {
    set({ loading: true });
    const res = await fetch(`/users/${id}`);
    const user = await res.json();
    set({ user, loading: false });
  },
}));

Middlewares (persistencia, devtools, logger)
jsx

import { persist } from 'zustand/middleware';

const useStore = create(
  persist(
    (set) => ({ count: 0, increment: () => set((s) => ({ count: s.count + 1 })) }),
    { name: 'counter-storage' } // localStorage key
  )
);

Store con slices (modularización)
jsx

const useBoundStore = create((...a) => ({
  ...counterSlice(...a),
  ...userSlice(...a),
}));

Ventajas sobre Redux

    Sin Provider (opcional).

    Menos código boilerplate.

    Rendimiento: solo re-renderiza componentes que usan datos específicos.

    Curva de aprendizaje baja.

Desventajas

    Menos tooling que Redux (aunque tiene DevTools).

    Menos estructura para equipos grandes (puede volverse desordenado).

Cuándo usar Zustand

    Proyectos pequeños a medianos.

    Necesitas estado global sin la complejidad de Redux.

    Prefieres una API de hooks simple.

📄 react-query.md
Concepto

React Query (ahora TanStack Query) no es una librería de estado global, sino un gestor de estado asíncrono del servidor. Maneja fetching, caching, sincronización, actualizaciones en segundo plano, etc.
Diferencia con estado global

    Estado global (Redux/Zustand): guarda datos del cliente (UI, preferencias, etc.).

    React Query: guarda datos del servidor (API, base de datos) con estrategias de caché y revalidación.

Instalación
bash

npm install @tanstack/react-query

Configuración básica
jsx

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <MiApp />
    </QueryClientProvider>
  );
}

Uso de useQuery (fetch y caché)
jsx

import { useQuery } from '@tanstack/react-query';

function ListaUsuarios() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['usuarios'],
    queryFn: () => fetch('/api/usuarios').then(res => res.json()),
  });

  if (isLoading) return <Spinner />;
  if (error) return <Error mensaje={error.message} />;
  return <ul>{data.map(user => <li key={user.id}>{user.name}</li>)}</ul>;
}

useMutation (para crear, actualizar, eliminar)
jsx

import { useMutation, useQueryClient } from '@tanstack/react-query';

function AgregarUsuario() {
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: (nuevoUsuario) => fetch('/api/usuarios', {
      method: 'POST',
      body: JSON.stringify(nuevoUsuario),
      headers: { 'Content-Type': 'application/json' },
    }).then(res => res.json()),
    onSuccess: () => {
      // Invalida la caché de usuarios para refetch
      queryClient.invalidateQueries({ queryKey: ['usuarios'] });
    },
  });

  return (
    <button onClick={() => mutation.mutate({ name: 'Nuevo' })}>
      Agregar
    </button>
  );
}

Características avanzadas

    Caché persistente (tiempo de vida configurable).

    Revalidación en segundo plano (stale-while-revalidate).

    Paginación y carga infinita (useInfiniteQuery).

    Deduplicación de peticiones (mismas query key simultáneas).

    Prefetching para mejorar UX.

Configuración global del QueryClient
jsx

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutos
      cacheTime: 1000 * 60 * 10,
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});

Comparación con useEffect + useState
Con useEffect	Con React Query
Manual handling de loading/error	Automático
Sin caché	Caché automático
Solicitudes duplicadas	Deduplicación
Dependencia manual de efectos	Declarativo con queryKey
Buenas prácticas

    Usa queryKey bien definidas (array con parámetros).

    Separa las funciones de queryFn en archivos de API.

    Usa enabled para consultas condicionales (ej. solo si hay un id).

    Combínalo con Zustand/Redux solo para estado local del cliente.

React Query vs Redux (para datos de API)

No compiten; se complementan. React Query maneja el servidor-estado; Redux maneja el cliente-estado. Puedes usar ambos.

📄 composicion.md
Concepto

La composición en React es el principio de construir componentes complejos a partir de componentes más pequeños y reutilizables, combinándolos como piezas de Lego. React favorece la composición sobre la herencia.
Composición vs Herencia

    Herencia: extender clases (ej. class Boton extends ComponenteBase). React no la recomienda para reutilizar lógica.

    Composición: incluir un componente dentro de otro mediante props o children.

Formas de composición
1. props.children (contenido anidado)
jsx

function Card({ children }) {
  return <div className="card">{children}</div>;
}

function App() {
  return (
    <Card>
      <h2>Título</h2>
      <p>Contenido</p>
    </Card>
  );
}

2. Props con componentes (especialización)
jsx

function Dialog({ title, message, buttons }) {
  return (
    <div className="dialog">
      <h2>{title}</h2>
      <p>{message}</p>
      <div className="buttons">{buttons}</div>
    </div>
  );
}

// Uso
<Dialog 
  title="Confirmar"
  message="¿Estás seguro?"
  buttons={
    <>
      <button>Cancelar</button>
      <button>Confirmar</button>
    </>
  }
/>

3. Props que reciben componentes (render props simplificadas)
jsx

function ListaDeItems({ items, renderItem }) {
  return <ul>{items.map(item => <li key={item.id}>{renderItem(item)}</li>)}</ul>;
}

<ListaDeItems 
  items={usuarios} 
  renderItem={user => <span>{user.nombre} ({user.email})</span>}
/>

4. HOCs (aunque son una forma de composición, se tratan aparte)

Un HOC es una función que recibe un componente y devuelve otro componente.
Patrón de contenedor vs presentacional (composición)
jsx

// Presentacional: solo UI
function UserProfile({ user }) {
  return <div>{user.name}</div>;
}

// Contenedor: lógica y datos
function UserProfileContainer({ userId }) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);
  return <UserProfile user={user} />;
}

Composición vs Configuración

En lugar de tener un componente enorme con muchas props booleanas para variantes, compón variantes como componentes separados.
jsx

// ❌ Mal: muchas props de configuración
<Button primary large disabled icon="save" />

// ✅ Bien: composición
<PrimaryButton large>Guardar</PrimaryButton>
// o
<Button variant="primary" size="large">Guardar</Button> // pero sigue siendo configuración

Ventajas de la composición

    Reutilización de lógica y UI.

    Flexibilidad: puedes cambiar el orden o tipo de componentes hijos.

    Mantenibilidad: componentes pequeños con una sola responsabilidad.

    Sin acoplamiento entre padre e hijo más allá de la interfaz (children o props).

Composición con contexto

El contexto se combina perfectamente con la composición: un Provider envuelve componentes hijos.
Buenas prácticas

    Prefiere children para contenido desconocido o dinámico.

    Para slots múltiples, usa props con nombres (ej. header, footer, sidebar).

    No pases componentes por props a menos que sea necesario (render props).

    Extrae lógica repetida en custom hooks, no en componentes heredados.

📄 render-props.md
Concepto

Render Props es un patrón donde un componente recibe una función como prop (generalmente llamada render o children) que retorna JSX. El componente llama a esa función con sus propios datos internos, permitiendo al padre definir cómo renderizar.
Origen

Popularizado antes de los hooks. Sigue siendo útil, aunque muchos casos se resuelven con custom hooks.
Ejemplo básico
jsx

// Componente que maneja el ratón
function MouseTracker({ children }) {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const handleMouseMove = (e) => setPosition({ x: e.clientX, y: e.clientY });
  
  return (
    <div onMouseMove={handleMouseMove}>
      {children(position)}
    </div>
  );
}

// Uso
<MouseTracker>
  {({ x, y }) => (
    <p>La posición del ratón es ({x}, {y})</p>
  )}
</MouseTracker>

Patrón con prop render (alternativa a children)
jsx

function MouseTracker({ render }) {
  // ... mismo estado
  return <div onMouseMove={handleMouseMove}>{render(position)}</div>;
}

<MouseTracker render={({ x, y }) => <p>{x},{y}</p>} />

Ejemplo real: componente de solicitud de datos
jsx

function Fetch({ url, children }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(data => { setData(data); setLoading(false); });
  }, [url]);
  
  return children({ data, loading });
}

// Uso
<Fetch url="/api/user">
  {({ data, loading }) => (
    loading ? <Spinner /> : <UserInfo user={data} />
  )}
</Fetch>

Ventajas

    Máxima flexibilidad: el componente padre decide completamente el renderizado.

    Reutilización de lógica sin necesidad de herencia.

    Composición dinámica.

Desventajas

    Callback hell si se anidan muchos render props.

    Legibilidad reducida en comparación con hooks.

    Rendimiento porque se crea una nueva función en cada render (aunque es manejable).

Render props vs Hooks

Con la llegada de los custom hooks, los render props han perdido popularidad:
jsx

// Con hook
function useMousePosition() {
  const [pos, setPos] = useState({ x: 0, y: 0 });
  useEffect(() => {
    const handler = (e) => setPos({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handler);
    return () => window.removeEventListener('mousemove', handler);
  }, []);
  return pos;
}

// Uso
function MiComponente() {
  const { x, y } = useMousePosition();
  return <p>{x},{y}</p>;
}

¿Cuándo usar render props hoy?

    En librerías que aún lo soportan (ej. react-router v5).

    Cuando necesitas que un componente controle el ciclo de vida y múltiples puntos de renderizado.

    Para mantener compatibilidad con código antiguo.

Buenas prácticas

    Nombra la prop children o render según el caso.

    Si usas children, asegúrate de documentar que espera una función.

    Combínalo con React.memo para evitar renders innecesarios.

📄 higher-order-components.md
Concepto

Un Higher-Order Component (HOC) es una función que recibe un componente y devuelve un nuevo componente mejorado. Es un patrón para reutilizar lógica entre componentes, común antes de los hooks.
Firma
jsx

const EnhancedComponent = higherOrderComponent(WrappedComponent);

Ejemplo básico: HOC de logging
jsx

function withLogger(WrappedComponent) {
  return function(props) {
    useEffect(() => {
      console.log(`Componente ${WrappedComponent.name} montado`);
      return () => console.log(`Componente ${WrappedComponent.name} desmontado`);
    }, []);
    return <WrappedComponent {...props} />;
  };
}

const UserPageWithLogger = withLogger(UserPage);

HOC que añade props
jsx

function withUser(WrappedComponent) {
  return function(props) {
    const [user, setUser] = useState(null);
    useEffect(() => {
      fetchUser(props.userId).then(setUser);
    }, [props.userId]);
    return <WrappedComponent {...props} user={user} />;
  };
}

const UserProfileWithData = withUser(UserProfile);

Composición de HOCs
jsx

const EnhancedComponent = withLogger(withUser(withTheme(BaseComponent)));
// o con una función compose (Redux)
import compose from 'lodash/fp/compose';
const EnhancedComponent = compose(withLogger, withUser, withTheme)(BaseComponent);

HOCs con configuración (fábrica de HOCs)
jsx

function withFetch(url) {
  return function(WrappedComponent) {
    return function(props) {
      const [data, setData] = useState(null);
      useEffect(() => {
        fetch(url).then(res => res.json()).then(setData);
      }, []);
      return <WrappedComponent {...props} data={data} />;
    };
  };
}

const UserListWithFetch = withFetch('/api/users')(UserList);

Convenciones importantes

    Pasar props no relacionadas al componente envuelto (usar spread).

    Display name para debugging: WrappedComponent.displayName || 'Component'.

    No usar HOCs dentro de render (causa desmontado/montado constante).

    Ref forwarding con forwardRef.

jsx

function withLogger(WrappedComponent) {
  const WithLogger = React.forwardRef((props, ref) => {
    // ... lógica
    return <WrappedComponent {...props} ref={ref} />;
  });
  WithLogger.displayName = `withLogger(${getDisplayName(WrappedComponent)})`;
  return WithLogger;
}

function getDisplayName(WrappedComponent) {
  return WrappedComponent.displayName || WrappedComponent.name || 'Component';
}

Ventajas

    Reutilización de lógica (antes de hooks).

    Composición de múltiples comportamientos.

    Aislamiento de lógica compleja.

Desventajas

    Wrapper hell (muchos niveles de componentes en React DevTools).

    Colisiones de props (dos HOCs pueden añadir la misma prop).

    Dificultad para tipar (TypeScript mejora, pero no es trivial).

    Menos legible que los hooks.

HOCs vs Hooks
HOC	Hook
Envuelve el componente	Se llama dentro del componente
Puede causar wrapper hell	No añade componentes extra
Más difícil de componer	Fácil de componer funciones
Ideal para librerías (react-redux connect)	Ideal para lógica de aplicación
¿Cuándo usar HOCs hoy?

    Librerías consolidadas (react-redux, react-router v5).

    Necesitas interceptar el ciclo de vida de un componente de manera no intrusiva.

    Código legacy que ya usa HOCs.

En proyectos nuevos, los custom hooks son la opción preferida.
📄 controlled-vs-uncontrolled.md
Concepto

Diferencia entre cómo un componente maneja sus datos internamente (no controlado) vs. cómo React controla sus datos a través del estado (controlado).
Componentes no controlados

    El DOM mantiene el estado (input, select, textarea).

    React solo lee el valor cuando es necesario (ej. onSubmit con ref).

    Se usa defaultValue en lugar de value.

jsx

function FormularioNoControlado() {
  const inputRef = useRef();
  
  const handleSubmit = (e) => {
    e.preventDefault();
    alert(inputRef.current.value);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input ref={inputRef} defaultValue="Texto inicial" />
      <button type="submit">Enviar</button>
    </form>
  );
}

Componentes controlados

    React maneja el estado con useState.

    El valor del input se lee de state y se actualiza con onChange.

    El DOM es solo una representación del estado de React.

jsx

function FormularioControlado() {
  const [valor, setValor] = useState('');
  
  return (
    <input 
      value={valor} 
      onChange={(e) => setValor(e.target.value)} 
    />
  );
}

Comparativa
Característica	Controlado	No controlado
Fuente de la verdad	Estado de React	DOM
Validación en tiempo real	Fácil	Complejo
Formato dinámico (máscaras)	Fácil	Difícil
Rendimiento	Ligeramente peor (re-render)	Mejor
Simplicidad inicial	Más código	Menos código
Acceso a valores	Inmediato (estado)	Requiere ref
Casos de uso
Controlado es mejor cuando:

    Necesitas validar o transformar la entrada en cada tecla.

    El campo depende de otros campos.

    Quieres habilitar/deshabilitar botones según el valor.

    Usas librerías de formularios (Formik, React Hook Form en modo controlado).

No controlado es mejor cuando:

    Formularios muy simples.

    Necesitas el mínimo re-renderizado posible.

    Integras con librerías no React (ej. jQuery datepicker).

    Usas React Hook Form en modo no controlado (por defecto).

Inputs especiales

    Checkbox/radio controlado: checked={estado} onChange={handler}

    Select controlado: value={estado} onChange={handler}

jsx

const [acepta, setAcepta] = useState(false);
<input type="checkbox" checked={acepta} onChange={(e) => setAcepta(e.target.checked)} />

React Hook Form (híbrido)

React Hook Form es mayormente no controlado por defecto (usa refs), pero puede ser controlado si se desea. Ofrece buen rendimiento.
jsx

const { register, handleSubmit } = useForm();
<input {...register('nombre')} /> // no controlado

Buenas prácticas

    Prefiere controlado para formularios con validación o dependencias.

    Usa no controlado solo si el rendimiento es crítico o el formulario es trivial.

    No mezcles ambos en el mismo campo (o será de solo lectura).

📄 atomic-design.md
Concepto

Atomic Design es una metodología para diseñar sistemas de componentes, propuesta por Brad Frost. No es exclusiva de React, pero se lleva muy bien con componentes funcionales.
Los 5 niveles atómicos
1. Átomos

Componentes básicos e indivisibles: botones, inputs, etiquetas, íconos.
jsx

// Átomo: Button
function Button({ children, onClick, variant = 'primary' }) {
  return <button className={`btn btn-${variant}`} onClick={onClick}>{children}</button>;
}

// Átomo: Input
function Input({ type = 'text', placeholder }) {
  return <input type={type} placeholder={placeholder} className="input" />;
}

2. Moléculas

Combinación de dos o más átomos que funcionan juntos como una unidad.
jsx

// Molécula: SearchField (Input + Button)
function SearchField({ onSearch }) {
  const [query, setQuery] = useState('');
  return (
    <div className="search-field">
      <Input value={query} onChange={(e) => setQuery(e.target.value)} />
      <Button onClick={() => onSearch(query)}>Buscar</Button>
    </div>
  );
}

3. Organismos

Componentes más complejos formados por moléculas, átomos y/o otros organismos. Representan secciones de la interfaz.
jsx

// Organismo: Header (Logo + SearchField + NavMenu)
function Header() {
  return (
    <header className="header">
      <Logo />
      <SearchField onSearch={handleGlobalSearch} />
      <NavMenu items={['Inicio', 'Productos', 'Contacto']} />
    </header>
  );
}

4. Plantillas (Templates)

Combinan organismos en una estructura de página sin contenido final (esqueletos). No tienen lógica de datos, solo layout.
jsx

// Template: ProductPageTemplate
function ProductPageTemplate({ header, sidebar, content, footer }) {
  return (
    <div className="page">
      {header}
      <div className="layout">
        <aside>{sidebar}</aside>
        <main>{content}</main>
      </div>
      {footer}
    </div>
  );
}

5. Páginas

Instancias concretas de plantillas con datos reales. Son los componentes que se enrutan.
jsx

function ProductPage({ productId }) {
  const { product, related } = useProductData(productId);
  return (
    <ProductPageTemplate
      header={<Header />}
      sidebar={<ProductSidebar product={product} />}
      content={<ProductContent product={product} related={related} />}
      footer={<Footer />}
    />
  );
}

Estructura de carpetas sugerida para Atomic Design
text

src/
├── components/
│   ├── atoms/
│   │   ├── Button/
│   │   ├── Input/
│   │   └── Icon/
│   ├── molecules/
│   │   ├── SearchField/
│   │   └── ProductCard/
│   ├── organisms/
│   │   ├── Header/
│   │   └── ProductList/
│   ├── templates/
│   │   └── ProductPageTemplate/
│   └── pages/
│       └── ProductPage/

Ventajas

    Reutilización máxima.

    Consistencia en toda la aplicación.

    Escalabilidad para equipos grandes.

    Fácil testing de componentes pequeños.

Desventajas

    Sobreesfuerzo para apps pequeñas.

    Dificultad para clasificar algunos componentes (¿molécula u organismo?).

    Verboso en carpetas.

Consejos prácticos

    No es necesario seguir al pie de la letra; adapta el concepto.

    Usa Atomic Design principalmente para sistemas de diseño (bibliotecas de componentes).

    Combínalo con Storybook para documentar cada nivel.

Alternativas similares

    Componentes compuestos (sin jerarquía estricta).

    Domain-driven design (componentes por dominio funcional).

📄 react-memo.md
Concepto

React.memo es una función de orden superior (HOC) que evita que un componente funcional se re-renderice si sus props no han cambiado (comparación superficial por defecto).
Sintaxis
jsx

const ComponenteMemoizado = React.memo(ComponenteOriginal);

¿Cuándo usar React.memo?

    Componentes que reciben las mismas props frecuentemente.

    Componentes que se renderizan muchas veces (listas grandes, tablas).

    Componentes pesados (con cálculos costosos o muchos elementos DOM).

Ejemplo básico
jsx

const Hijo = React.memo(({ valor }) => {
  console.log('Hijo renderizado');
  return <div>{valor}</div>;
});

function Padre() {
  const [contador, setContador] = useState(0);
  const [texto, setTexto] = useState('Hola');
  
  return (
    <div>
      <button onClick={() => setContador(c => c + 1)}>Contador: {contador}</button>
      <input value={texto} onChange={(e) => setTexto(e.target.value)} />
      <Hijo valor="Este texto no cambia" />
    </div>
  );
}

El componente Hijo solo se renderizará una vez, aunque el padre se re-renderice al cambiar contador o texto.
Personalización de la comparación

Por defecto, React.memo hace una comparación superficial (shallow compare) de las props. Si necesitas control personalizado, pasa una función como segundo argumento:
jsx

const MemoComponent = React.memo(
  Componente,
  (prevProps, nextProps) => {
    // Devuelve true si son iguales (NO debe re-renderizar)
    return prevProps.usuario.id === nextProps.usuario.id;
  }
);

Cuidado: la función debe ser pura y rápida.
Limitaciones importantes
1. Las funciones como props siempre cambian (a menos que uses useCallback)
jsx

// ❌ Mal: handleClick se recrea en cada render
<HijoMemo onClick={() => console.log('click')} />

// ✅ Bien: con useCallback
const handleClick = useCallback(() => console.log('click'), []);
<HijoMemo onClick={handleClick} />

2. Los objetos/arrays literales también cambian cada vez
jsx

// ❌ Mal: objeto nuevo cada vez
<HijoMemo config={{ tema: 'oscuro' }} />

// ✅ Bien: usar useMemo o definir fuera
const config = useMemo(() => ({ tema: 'oscuro' }), []);
<HijoMemo config={config} />

3. React.memo solo mira las props, no el estado interno ni el contexto

Si el componente usa useContext y el contexto cambia, se re-renderizará igualmente.
¿Cuándo NO usar React.memo?

    Componentes que casi siempre reciben props diferentes (ej. inputs controlados).

    Componentes muy ligeros (el costo de la comparación supera el beneficio).

    En toda la aplicación sin medir (optimización prematura).

Medir antes de optimizar

Usa React DevTools → Profiler para identificar componentes que se re-renderizan innecesariamente. Solo entonces aplica React.memo.
React.memo vs PureComponent

    React.memo para componentes funcionales.

    PureComponent para componentes de clase (implementa shouldComponentUpdate con shallow compare).

Buenas prácticas

    Envuelve solo los componentes que realmente lo necesitan.

    Combínalo con useCallback y useMemo para props estables.

    Prefiere la composición para evitar pasar props innecesarias.

📄 virtual-dom.md
Concepto

El Virtual DOM es una representación liviana del DOM real en memoria, como un árbol de objetos JavaScript. React lo usa para optimizar las actualizaciones de la interfaz.
¿Por qué existe?

Manipular el DOM real es lento porque cada cambio puede provocar reflows y repaints. El Virtual DOM permite agrupar cambios y aplicar la mínima cantidad de mutaciones al DOM real.
Algoritmo básico de React

    Render inicial: React crea un árbol Virtual DOM a partir del JSX.

    Actualización: Cuando cambia el estado o las props, React crea un nuevo árbol Virtual DOM.

    Diffing: React compara el nuevo árbol con el anterior (algoritmo de diferenciación).

    Reconciliación: React calcula el conjunto mínimo de operaciones necesarias para actualizar el DOM real.

    Commit: React aplica esos cambios al DOM real.

Ejemplo conceptual
jsx

// Virtual DOM simplificado (no es exactamente así)
const vDOM = {
  type: 'div',
  props: { className: 'container' },
  children: [
    { type: 'h1', props: {}, children: ['Hola'] },
    { type: 'button', props: { onClick: fn }, children: ['Click'] }
  ]
};

Ventajas del Virtual DOM

    Rendimiento: evita operaciones costosas del DOM real.

    Abstracción: React puede generar DOM para web, Native para móviles, etc.

    Declarativo: no necesitas manipular el DOM manualmente.

Desventajas

    No es el más rápido posible: para apps con actualizaciones ultra frecuentes (animaciones 60fps), puede haber soluciones más óptimas (manipulación directa del DOM, WebGL, etc.).

    Costo de memoria: mantener dos árboles virtuales consume RAM.

¿Es realmente más rápido?

Depende. Para la mayoría de aplicaciones, el Virtual DOM es suficientemente rápido. El verdadero beneficio es la simplicidad conceptual y la consistencia.
Comparativa con otros enfoques

    Manipulación manual del DOM: más rápido en manos expertas, pero propenso a errores y código verboso.

    Svelte: compila en tiempo de build, no usa Virtual DOM, actualiza el DOM directamente. Para muchos casos es más rápido.

    Solid: similar a Svelte, pero con sintaxis similar a React.

Conceptos erróneos comunes

    "El Virtual DOM es más rápido que el DOM real" → Falso. El Virtual DOM es una capa de abstracción; el DOM real sigue siendo la base. La optimización está en minimizar las operaciones.

    "React usa Virtual DOM para todo" → React también puede usar dangerouslySetInnerHTML o findDOMNode (legado).

Buenas prácticas

    No pienses demasiado en el Virtual DOM; confía en React, pero evita patrones que causen re-renderizados masivos (ej. modificar el estado raíz frecuentemente).

    Usa key correctamente para ayudar al algoritmo de diffing.

📄 reconciliation.md
Concepto

La reconciliación es el algoritmo que React utiliza para comparar dos árboles del Virtual DOM y determinar qué cambios aplicar al DOM real.
Algoritmo de diffing (diferenciación)

React hace dos suposiciones principales para lograr un algoritmo O(n) (lineal) en lugar de O(n³):

    Dos elementos de diferente tipo producirán árboles diferentes. React destruye el primero y crea el nuevo desde cero.

    El atributo key permite identificar elementos que se mueven entre renders.

Reglas del algoritmo
1. Comparación de nodos raíz

    Tipos diferentes (ej. <div> → <span>): React desmonta el árbol antiguo y monta el nuevo. Todos los componentes hijos se destruyen (se ejecutan efectos de limpieza) y se crean nuevos.

jsx

// Antes
<div><Counter /></div>
// Después
<span><Counter /></span>
// Resultado: Counter se desmonta y remonta (pierde su estado interno)

    Mismo tipo (ej. <div> → <div>): React actualiza los atributos del elemento y luego recorre los hijos recursivamente.

2. Comparación de elementos del mismo tipo

Cuando el tipo es el mismo, React actualiza las props del elemento existente para que coincidan con el nuevo. Luego recorre los hijos.
3. Comparación de listas (importancia de key)

Sin key, React usa un algoritmo ingenuo que puede ser ineficiente. Con key, React puede reordenar, insertar y eliminar elementos de manera óptima.
jsx

// Sin key (ineficiente)
<ul>
  <li>Ana</li>
  <li>Luis</li>
</ul>
// Después de invertir
<ul>
  <li>Luis</li>
  <li>Ana</li>
</ul>
// React destruye los dos li y crea otros nuevos (costoso)

// Con key
<ul>
  <li key="ana">Ana</li>
  <li key="luis">Luis</li>
</ul>
// React solo reordena los nodos existentes (eficiente)

¿Qué pasa con el estado durante la reconciliación?

    Si un componente se mantiene (mismo tipo, misma posición), React conserva su estado.

    Si un componente se elimina, se destruye su estado.

    Para forzar la reinicialización del estado, usa la key diferente.

jsx

// Reiniciar estado de un formulario cambiando la key
const [resetKey, setResetKey] = useState(0);
<Form key={resetKey} /> // Cambiar resetKey para reiniciar el formulario

Ciclo de vida de la reconciliación (versión simplificada)

    Render (crea Virtual DOM)

    Diff (compara con versión anterior)

    Commit (aplica cambios al DOM real)

    Efectos (ejecuta useEffect, useLayoutEffect)

Algoritmo de reconciliación y Fibers (React 16+)

React 16 introdujo Fibers (re-arquitectura) que permite:

    Pausar, reanudar y priorizar el trabajo.

    Dividir la reconciliación en unidades de trabajo (frames).

    Hacer que el renderizado no bloquee el hilo principal.

Buenas prácticas para ayudar a la reconciliación

    Usa key únicas y estables (no índices de array si la lista es dinámica).

    No cambies innecesariamente el tipo de un componente raíz.

    Prefiere if condicional a display: none si el componente es costoso (así React lo desmonta).

Depuración de reconciliación

    React DevTools → Highlight updates cuando se renderizan componentes.

    why-did-you-render librería para detectar re-renderizados innecesarios.

📄 code-splitting-lazy.md
Concepto

Code splitting (división de código) y lazy loading (carga diferida) son técnicas para reducir el tamaño del bundle inicial, cargando solo el código necesario para la vista actual.
División de código en React
1. React.lazy + Suspense
jsx

import { lazy, Suspense } from 'react';

const ComponentePesado = lazy(() => import('./ComponentePesado'));

function App() {
  return (
    <div>
      <h1>Mi app</h1>
      <Suspense fallback={<div>Cargando...</div>}>
        <ComponentePesado />
      </Suspense>
    </div>
  );
}

2. Lazy con rutas (React Router)
jsx

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { lazy, Suspense } from 'react';

const Home = lazy(() => import('./pages/Home'));
const Productos = lazy(() => import('./pages/Productos'));
const Contacto = lazy(() => import('./pages/Contacto'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<div>Cargando página...</div>}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/productos" element={<Productos />} />
          <Route path="/contacto" element={<Contacto />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

Estrategias de división

    Por rutas: cada página es un chunk separado.

    Por componentes pesados: gráficos, editores de texto, calendarios, mapas.

    Por librerías: si una librería es grande y no se usa siempre (ej. moment.js, lodash), se puede cargar bajo demanda.

Límites de errores con lazy

Si falla la carga de un componente lazy, puedes usar un Error Boundary:
jsx

class ErrorBoundary extends React.Component {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  render() {
    if (this.state.hasError) return <div>Error al cargar</div>;
    return this.props.children;
  }
}

// Uso
<ErrorBoundary>
  <Suspense fallback="Cargando...">
    <ComponenteLazy />
  </Suspense>
</ErrorBoundary>

Prefetching (carga anticipada)

Puedes cargar un componente antes de que se necesite (ej. cuando el usuario pasa el mouse sobre un enlace):
jsx

const prefetchComponente = () => import('./ComponentePesado');

<Link 
  to="/ruta"
  onMouseEnter={prefetchComponente}
>
  Ir
</Link>

Configuración de Webpack/Vite

Ambos soportan import() dinámico nativamente. Puedes personalizar los nombres de los chunks:
jsx

const Componente = lazy(() => import(/* webpackChunkName: "mi-componente" */ './Componente'));

División de código con React 18+ y Server Components

En Next.js App Router, los Server Components permiten división automática. En React 18 con frameworks como Vite, sigue funcionando React.lazy.
Buenas prácticas

    No dividas componentes demasiado pequeños (cada chunk tiene overhead).

    Coloca Suspense en un nivel adecuado (no uno por cada componente lazy).

    Prueba que la experiencia de carga sea buena (no mostrar fallbacks parpadeantes).

    Monitorea el tamaño de los bundles con herramientas como webpack-bundle-analyzer.

Limitaciones

    React.lazy no funciona con Server Side Rendering (SSR) nativo. Necesitas librerías como loadable-components.

    Solo funciona con exports por defecto (export default).

📄 optimization-tips.md

Este archivo compila técnicas prácticas de optimización de rendimiento en React.
1. Evitar renderizados innecesarios
Usar React.memo, useMemo, useCallback

Ya vistos en detalle.
Mover el estado hacia abajo (State colocation)
jsx

// ❌ Mal: estado en el padre, causa re-render de toda la lista
function App() {
  const [texto, setTexto] = useState('');
  return (
    <div>
      <input value={texto} onChange={e => setTexto(e.target.value)} />
      <ListaGrande /> {/* se re-renderiza cada vez que cambia texto */}
    </div>
  );
}

// ✅ Bien: estado en el componente que lo necesita
function App() {
  return (
    <div>
      <InputControlado />
      <ListaGrande />
    </div>
  );
}

Extraer componentes que cambian frecuentemente

Mantén los componentes estables separados de los que cambian.
2. Optimizar listas grandes
Virtualización (react-window, react-virtualized)

Renderiza solo los elementos visibles en la ventana.
jsx

import { FixedSizeList as List } from 'react-window';

function ListaVirtualizada({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>{items[index]}</div>
  );
  return (
    <List
      height={400}
      itemCount={items.length}
      itemSize={35}
      width={300}
    >
      {Row}
    </List>
  );
}

Paginación o carga infinita

No cargues 10,000 elementos de una vez.
3. Evitar funciones anónimas en props (cuando sea posible)
jsx

// ❌ Mal (crea nueva función en cada render)
<button onClick={() => handleClick(id)}>Eliminar</button>

// ✅ Bien (usar useCallback o definir función fuera)
const handleClickMemo = useCallback(() => handleClick(id), [id]);
<button onClick={handleClickMemo}>Eliminar</button>

Si el componente hijo no está memoizado, la diferencia es mínima. Solo es crítica con React.memo.
4. Memoizar valores costosos
jsx

// ❌ Mal: recalcula en cada render
const total = items.reduce((sum, i) => sum + i.price, 0);

// ✅ Bien: solo cuando items cambia
const total = useMemo(() => items.reduce((sum, i) => sum + i.price, 0), [items]);

5. Usar useTransition para actualizaciones no urgentes (React 18)
jsx

const [isPending, startTransition] = useTransition();
const [query, setQuery] = useState('');

const handleChange = (e) => {
  const value = e.target.value;
  startTransition(() => {
    setQuery(value); // no urgente
  });
};

6. Evitar la propagación de contextos grandes

Si usas Context API, divide contextos por dominio y memoiza el value.
jsx

// ❌ Mal: contexto gigante que cambia todo el tiempo
<AppContext.Provider value={{ user, theme, notifications, ... }}>

// ✅ Bien: contextos separados
<UserProvider>
  <ThemeProvider>
    <NotificationsProvider>
      ...
    </NotificationsProvider>
  </ThemeProvider>
</UserProvider>

7. Evitar objetos literales en dependencias de efectos
jsx

// ❌ Mal: objeto nuevo en cada render
useEffect(() => {
  fetchData({ page, limit });
}, [{ page, limit }]); // siempre diferente

// ✅ Bien: desestructurar dependencias
useEffect(() => {
  fetchData({ page, limit });
}, [page, limit]);

8. Imágenes optimizadas

    Usar loading="lazy" en <img> (nativo del navegador).

    Usar formatos modernos (WebP, AVIF).

    Pre-dimensionar imágenes (evitar reflow).

9. Web Workers para tareas pesadas

Si tienes procesamiento intensivo (ordenar 1M de registros, cálculos criptográficos), muévelo a un Web Worker.
10. Medir y monitorear

    React DevTools Profiler: graba interacciones y muestra qué componentes se renderizan.

    Lighthouse: mide rendimiento general.

    Web Vitals: Core Web Vitals de Google.

Herramientas de análisis de bundles
bash

npm install --save-dev webpack-bundle-analyzer
# o para Vite
npm install --save-dev rollup-plugin-visualizer

Checklist de optimización (antes de optimizar)

    ¿Hay re-renderizados innecesarios visibles? (Profiler)

    ¿El bundle inicial es demasiado grande? (Bundle analyzer)

    ¿Hay operaciones costosas en el hilo principal? (Performance tab de Chrome)

    ¿Las imágenes están optimizadas?

    ¿Se puede dividir el código por rutas?

    ¿Se puede virtualizar una lista larga?

Principio fundamental

    "Las optimizaciones tempranas son la raíz de todos los males" – Donald Knuth.

Optimiza solo cuando tengas un problema medible. La legibilidad y mantenibilidad del código son más importantes que micro-optimizaciones sin impacto real.

📄 react-router.md
Concepto

React Router es la librería estándar para manejar enrutamiento (navegación entre páginas) en aplicaciones React. Permite sincronizar la interfaz con la URL del navegador, creando una experiencia de Single Page Application (SPA) con múltiples vistas.
Instalación
bash

npm install react-router-dom

Componentes principales (v6)
1. BrowserRouter

Envuelve la aplicación para habilitar el enrutamiento. Usa la API History de HTML5.
jsx

import { BrowserRouter } from 'react-router-dom';
ReactDOM.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>,
  document.getElementById('root')
);

2. Routes y Route

Definen las rutas y qué componente renderizar en cada una.
jsx

import { Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
    </Routes>
  );
}

3. Link y NavLink

Para navegación sin recargar la página.
jsx

import { Link, NavLink } from 'react-router-dom';

// Link básico
<Link to="/about">Acerca de</Link>

// NavLink (añade clase 'active' cuando la ruta coincide)
<NavLink to="/about" className={({ isActive }) => isActive ? 'active' : ''}>
  Acerca
</NavLink>

Parámetros de ruta
Parámetros dinámicos (:id)
jsx

// Definición
<Route path="/users/:userId" element={<UserProfile />} />

// En el componente
import { useParams } from 'react-router-dom';

function UserProfile() {
  const { userId } = useParams();
  return <div>Usuario ID: {userId}</div>;
}

Parámetros opcionales (con ? - no soportado directamente, usa dos rutas o patrón)
jsx

<Route path="/products/:category?/:id?" element={<Products />} />

Query strings (parámetros en URL después de ?)
jsx

// URL: /search?q=react&page=2
import { useSearchParams } from 'react-router-dom';

function Search() {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get('q');       // 'react'
  const page = searchParams.get('page');     // '2'
  
  const updateQuery = (newQuery) => {
    setSearchParams({ q: newQuery, page: 1 });
  };
  
  return <div>Buscando: {query}</div>;
}

Navegación programática
useNavigate
jsx

import { useNavigate } from 'react-router-dom';

function LoginButton() {
  const navigate = useNavigate();
  
  const handleLogin = async () => {
    await login();
    navigate('/dashboard');        // redirige
    // navigate(-1)               // atrás
    // navigate(1)                // adelante
    // navigate('/about', { replace: true })  // reemplazar historial
  };
  
  return <button onClick={handleLogin}>Login</button>;
}

Rutas anidadas (Nested Routes)
Layouts compartidos
jsx

import { Outlet } from 'react-router-dom';

function Layout() {
  return (
    <div>
      <header>Mi Sitio</header>
      <nav>
        <Link to="/">Inicio</Link>
        <Link to="/blog">Blog</Link>
      </nav>
      <main>
        <Outlet />  {/* Aquí se renderiza la ruta hija */}
      </main>
      <footer>Footer</footer>
    </div>
  );
}

// Definición de rutas anidadas
<Routes>
  <Route path="/" element={<Layout />}>
    <Route index element={<Home />} />           // index = ruta por defecto
    <Route path="blog" element={<Blog />} />
    <Route path="blog/:slug" element={<Post />} />
  </Route>
</Routes>

Outlet con contexto (opcional)
jsx

<Outlet context={{ user: currentUser }} />

// En componente hijo
import { useOutletContext } from 'react-router-dom';
const { user } = useOutletContext();

Rutas protegidas (Authentication)
jsx

function PrivateRoute({ children }) {
  const { user } = useAuth();
  const navigate = useNavigate();
  
  useEffect(() => {
    if (!user) navigate('/login');
  }, [user, navigate]);
  
  return user ? children : null;
}

// Enrutamiento
<Routes>
  <Route path="/login" element={<Login />} />
  <Route path="/dashboard" element={
    <PrivateRoute>
      <Dashboard />
    </PrivateRoute>
  } />
</Routes>

O usando un wrapper layout:
jsx

<Route element={<ProtectedLayout />}>
  <Route path="/dashboard" element={<Dashboard />} />
  <Route path="/profile" element={<Profile />} />
</Route>

Rutas con lazy loading (code splitting)
jsx

import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));

<Routes>
  <Route path="/dashboard" element={
    <Suspense fallback={<div>Cargando...</div>}>
      <Dashboard />
    </Suspense>
  } />
</Routes>

Manejo de rutas no encontradas (404)
jsx

<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/about" element={<About />} />
  <Route path="*" element={<NotFound />} />  // * captura todas las demás
</Routes>

Redirecciones
Con Navigate componente
jsx

import { Navigate } from 'react-router-dom';

<Route path="/old-route" element={<Navigate to="/new-route" replace />} />

Redirección condicional en componente
jsx

if (!user) return <Navigate to="/login" />;

Hooks útiles adicionales

    useLocation(): obtiene el objeto de ubicación actual (pathname, search, state).

    useNavigation() (React Router 6.4+): estado de navegación (cargando, enviando, etc.).

    useRouteError() (v6.4+): captura errores en rutas.

Ejemplo completo
jsx

// App.jsx
import { BrowserRouter, Routes, Route, Link, Outlet } from 'react-router-dom';

function Layout() {
  return (
    <div>
      <nav>
        <Link to="/">Inicio</Link>
        <Link to="/products">Productos</Link>
      </nav>
      <Outlet />
    </div>
  );
}

function Home() { return <h1>Inicio</h1>; }
function Products() { return <h1>Productos</h1>; }
function ProductDetail() {
  const { id } = useParams();
  return <h1>Producto {id}</h1>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="products" element={<Products />} />
          <Route path="products/:id" element={<ProductDetail />} />
        </Route>
        <Route path="*" element={<h1>404</h1>} />
      </Routes>
    </BrowserRouter>
  );
}

Buenas prácticas

    Organiza las rutas en un archivo separado (ej. routes.jsx) para mantenibilidad.

    Usa rutas anidadas para layouts compartidos (headers, footers).

    Protege rutas usando layouts o componentes wrapper.

    Prefiere parámetros en la URL (:id) sobre query strings para recursos principales.

    Usa NavLink para menús activos con estilos.

    Lazy loading por ruta para reducir el bundle inicial.

Errores comunes

    Olvidar el BrowserRouter alrededor de la app.

    Usar href en lugar de to (recarga la página).

    No poner element en Route (antes era component o render).

    Confundir index con path="".

    No manejar rutas 404 – siempre poner path="*" al final.

Comparativa con otras librerías

    React Router v6 – Estándar, potente, API declarativa.

    Reach Router – Integrado en v6 (ahora es lo mismo).

    Wouter – Más ligero (<2KB), para proyectos pequeños.

    TanStack Router – Tipado fuerte, rutas anidadas automáticas, más nuevo.

Conclusión

React Router es esencial para cualquier SPA mediana o grande. Su API en v6 es más limpia y predecible que versiones anteriores.

📄 jest.md
Concepto

Jest es un framework de pruebas unitarias desarrollado por Meta. Es rápido, tiene断言 (expectations), mocking, y cobertura de código. Se integra perfectamente con React y es el corredor de pruebas por defecto en Create React App y Vite.
Instalación en un proyecto React manual
bash

npm install --save-dev jest @testing-library/react @testing-library/jest-dom

Configuración básica (opcional, Create React App ya la trae)
js

// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
};

js

// src/setupTests.js
import '@testing-library/jest-dom';

Estructura de una prueba con Jest
jsx

// suma.js
export const suma = (a, b) => a + b;

// suma.test.js
import { suma } from './suma';

test('suma 1 + 2 es igual a 3', () => {
  expect(suma(1, 2)).toBe(3);
});

Expects y matchers comunes
js

expect(valor).toBe(3);                 // igualdad estricta (Object.is)
expect(valor).toEqual({ a: 1 });       // igualdad profunda para objetos
expect(valor).toBeTruthy();            // truthy
expect(valor).toBeFalsy();             // falsy
expect(valor).toBeNull();
expect(valor).toBeUndefined();
expect(valor).not.toBe(4);             // negación
expect(array).toContain('item');       // contiene elemento
expect(array).toHaveLength(3);
expect(fn).toThrow();                  // lanza error
expect(mock).toHaveBeenCalled();       // fue llamado
expect(mock).toHaveBeenCalledTimes(2);
expect(mock).toHaveBeenCalledWith(arg);

Pruebas asíncronas
jsx

// callback con done (no recomendado, mejor async/await)
test('async con async/await', async () => {
  const data = await fetchData();
  expect(data).toBe('ok');
});

// con resolves/rejects
test('usando resolves', () => {
  return expect(Promise.resolve('leche')).resolves.toBe('leche');
});

Mocking de funciones y módulos
Mock de función
jsx

const mockFn = jest.fn();
mockFn('arg1');
expect(mockFn).toHaveBeenCalledWith('arg1');
mockFn.mockReturnValue('valor fijo');
mockFn.mockResolvedValue('promesa resuelta');

Mock de módulo completo (ej. axios)
jsx

jest.mock('axios');
import axios from 'axios';
axios.get.mockResolvedValue({ data: { id: 1 } });

Mock parcial (solo una función)
jsx

jest.spyOn(api, 'fetchUser').mockImplementation(() => Promise.resolve({ name: 'Ana' }));

Mocks manuales (carpeta __mocks__)

Crea __mocks__/axios.js y Jest lo usará automáticamente.
Cobertura de código
bash

npm test -- --coverage

Genera reporte de líneas, funciones, ramas y statements cubiertos.
Pruebas de componentes React con Jest + Testing Library
jsx

import { render, screen } from '@testing-library/react';
import Saludo from './Saludo';

test('muestra el nombre prop', () => {
  render(<Saludo nombre="Ana" />);
  expect(screen.getByText(/Hola, Ana/)).toBeInTheDocument();
});

Correr pruebas
bash

npm test                 # modo watch
npm test -- --coverage   # con cobertura
npm test -- -u           # actualizar snapshots

Snapshots (uso moderado)
jsx

test('componente coincide con snapshot', () => {
  const { asFragment } = render(<MiComponente />);
  expect(asFragment()).toMatchSnapshot();
});

Los snapshots son útiles para estructuras estables, pero pueden llevar a pruebas frágiles.
Buenas prácticas en Jest

    Nombrar archivos como Componente.test.js o Componente.spec.js.

    Un test o it por comportamiento (mantener pruebas pequeñas y enfocadas).

    No usar lógica compleja dentro de las pruebas (if, loops).

    Limpiar mocks con jest.clearAllMocks() o jest.resetAllMocks().

    Evitar snapshots grandes (mejor aserciones explícitas).

    No probar implementación, probar comportamiento.

Debugging

    Usa console.log dentro de la prueba (se muestra en consola).

    Usa screen.debug() de Testing Library.

    Usa node --inspect-brk y depurador de Chrome.

📄 testing-library.md
Concepto

React Testing Library (RTL) es la extensión oficial de Testing Library para React. Su filosofía es probar componentes desde la perspectiva del usuario, no los detalles de implementación.
Principios clave

    "Cuanto más se parezcan tus pruebas a la forma en que se usa tu software, más confianza te darán."

    No probar detalles internos (estado, props internos, métodos de ciclo de vida).

    Interactuar con el DOM como un usuario: encontrar elementos por texto, rol, etiqueta, etc.

    Usar fireEvent o userEvent para simular interacciones reales.

Instalación
bash

npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event

Renderizado y consultas básicas
jsx

import { render, screen } from '@testing-library/react';
import MiComponente from './MiComponente';

test('renderiza el título', () => {
  render(<MiComponente />);
  const titulo = screen.getByText('Bienvenido');
  expect(titulo).toBeInTheDocument();
});

Tipos de consultas (queries)
Query	Encuentra por	Devuelve
getByRole	Rol ARIA (button, heading, link)	Elemento o error
getByLabelText	<label> asociado o atributo aria-label	Elemento o error
getByPlaceholderText	Atributo placeholder	Elemento o error
getByText	Contenido textual	Elemento o error
getByDisplayValue	Valor actual de input/textarea/select	Elemento o error
getByAltText	Atributo alt de imagen	Elemento o error
getByTitle	Atributo title	Elemento o error
getByTestId	Atributo data-testid (último recurso)	Elemento o error

Además de getBy*, existen:

    queryBy*: devuelve null si no encuentra (no lanza error).

    findBy*: retorna Promise, útil para elementos asíncronos.

    getAllBy*, queryAllBy*, findAllBy*: para múltiples elementos.

Orden de preferencia de consultas (recomendado)

    getByRole (más accesible)

    getByLabelText

    getByPlaceholderText

    getByText

    getByDisplayValue

    getByAltText

    getByTitle

    getByTestId (solo si no hay otra opción)

Simular eventos: fireEvent vs userEvent
fireEvent (síncrono, más bajo nivel)
jsx

import { fireEvent } from '@testing-library/react';

fireEvent.click(button);
fireEvent.change(input, { target: { value: 'nuevo texto' } });

userEvent (recomendado, simula interacciones completas)
jsx

import userEvent from '@testing-library/user-event';

test('click en botón llama a función', async () => {
  const user = userEvent.setup();
  await user.click(button);    // incluye focus, hover, etc.
});

Prueba de componentes asíncronos (datos de API)
jsx

import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('carga datos al hacer click', async () => {
  render(<FetchButton />);
  const button = screen.getByRole('button', { name: /cargar/i });
  await userEvent.click(button);
  
  // Esperar a que aparezca el texto "Usuario: Ana"
  const usuario = await screen.findByText(/Usuario: Ana/i);
  expect(usuario).toBeInTheDocument();
});

Prueba de formularios
jsx

test('envía formulario con datos', async () => {
  const user = userEvent.setup();
  const onSubmit = jest.fn();
  render(<Formulario onSubmit={onSubmit} />);
  
  await user.type(screen.getByLabelText(/nombre/i), 'Carlos');
  await user.type(screen.getByLabelText(/email/i), 'carlos@mail.com');
  await user.click(screen.getByRole('button', { name: /enviar/i }));
  
  expect(onSubmit).toHaveBeenCalledWith({
    nombre: 'Carlos',
    email: 'carlos@mail.com'
  });
});

Prueba de componentes con contexto personalizado
jsx

function renderWithContext(component, providerProps) {
  return render(
    <AuthProvider value={providerProps}>
      {component}
    </AuthProvider>
  );
}

Prueba de routing (React Router)
jsx

import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import MiRuta from './MiRuta';

test('ruta /productos muestra Productos', () => {
  render(
    <MemoryRouter initialEntries={['/productos']}>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText(/lista de productos/i)).toBeInTheDocument();
});

Mock de fetch o axios
jsx

global.fetch = jest.fn(() =>
  Promise.resolve({ json: () => Promise.resolve({ name: 'Ana' }) })
);

// después de la prueba
global.fetch.mockRestore();

Depuración visual con screen.debug()
jsx

test('debug', () => {
  render(<Componente />);
  screen.debug();                 // imprime todo el DOM
  screen.debug(screen.getByRole('button')); // imprime solo el botón
});

Prueba de errores (Error Boundaries)
jsx

test('muestra fallback cuando hay error', () => {
  const ThrowError = () => { throw new Error('boom'); };
  render(
    <ErrorBoundary fallback={<div>Error!</div>}>
      <ThrowError />
    </ErrorBoundary>
  );
  expect(screen.getByText('Error!')).toBeInTheDocument();
});

Buenas prácticas con Testing Library

    No uses waitFor a menos que sea estrictamente necesario (prefiere findBy).

    Prueba interacciones completas (escribe, click, espera, verifica).

    No expongas data-testid como primera opción, pero úsalo para elementos difíciles (selectores complejos).

    Mantén las pruebas independientes (cada prueba limpia el DOM).

    Usa jest.spyOn en lugar de mocks manuales cuando sea posible.

Ejemplo completo de un componente con eventos asíncronos
jsx

// ListaUsuarios.jsx
function ListaUsuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const cargar = async () => {
    const res = await fetch('/api/usuarios');
    const data = await res.json();
    setUsuarios(data);
  };
  return (
    <div>
      <button onClick={cargar}>Cargar</button>
      <ul>
        {usuarios.map(u => <li key={u.id}>{u.name}</li>)}
      </ul>
    </div>
  );
}

// ListaUsuarios.test.jsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ListaUsuarios from './ListaUsuarios';

global.fetch = jest.fn();

test('carga y muestra usuarios al hacer click', async () => {
  const mockUsers = [{ id: 1, name: 'Ana' }, { id: 2, name: 'Luis' }];
  fetch.mockResolvedValue({ json: async () => mockUsers });
  
  const user = userEvent.setup();
  render(<ListaUsuarios />);
  
  await user.click(screen.getByRole('button', { name: /cargar/i }));
  
  expect(await screen.findByText('Ana')).toBeInTheDocument();
  expect(screen.getByText('Luis')).toBeInTheDocument();
  expect(fetch).toHaveBeenCalledTimes(1);
  
  fetch.mockRestore();
});

Conclusión

La combinación de Jest + Testing Library es la recomendada oficialmente para probar React. Testing Library promueve pruebas robustas que se rompen solo cuando la funcionalidad real para el usuario se rompe, no cuando cambian los detalles internos.

📄 server-components.md
Concepto

React Server Components (RSC) es una arquitectura que permite ejecutar componentes en el servidor, generando un formato especial que se envía al cliente sin incluir su código JavaScript. Se introdujo oficialmente en React 18 con frameworks como Next.js App Router.
Diferencia entre Client Components y Server Components
Característica	Client Component	Server Component
Ejecución	Navegador (cliente)	Servidor
Bundle JS	Sí (se envía al cliente)	No (solo resultado)
Acceso a backend	Indirecto (API)	Directo (DB, filesystem)
Interactividad	Sí (useState, useEffect, eventos)	No (solo renderizado)
Hidratación	Necesaria	No aplica
¿Por qué Server Components?

    Reducción del bundle del cliente: componentes que no requieren interactividad no envían código JS.

    Acceso directo a datos: pueden leer bases de datos o sistemas de archivos sin API intermedia.

    Mejor rendimiento inicial: el servidor envía HTML/JSON especial listo para renderizar.

    Mejor SEO: contenido generado en servidor.

Sintaxis y uso (con Next.js App Router)

Por defecto, en Next.js 13+ los componentes dentro de app/ son Server Components a menos que declares 'use client'.
jsx

// app/page.js - Server Component por defecto
import { db } from '@/lib/db';

async function HomePage() {
  const users = await db.user.findMany(); // consulta directa a DB
  
  return (
    <div>
      <h1>Usuarios</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
      {/* Cliente Component para interactividad */}
      <LikeButton userId={user.id} />
    </div>
  );
}

// Cliente Component (necesita interactividad)
'use client';
function LikeButton({ userId }) {
  const [liked, setLiked] = useState(false);
  return <button onClick={() => setLiked(!liked)}>{liked ? '❤️' : '🤍'}</button>;
}

Limitaciones de Server Components

    No pueden usar hooks de estado o efectos (useState, useEffect, etc.).

    No pueden usar contexto del cliente (solo contexto en servidor, diferente API).

    No pueden escuchar eventos del DOM (onClick, onChange).

    No pueden usar APIs del navegador (window, localStorage).

    No se pueden anidar Client Components dentro de Server Components? Sí se puede, pero al revés no.

Patrón de composición: Server → Client
jsx

// Server Component
import { ClientCounter } from './ClientCounter';

export default function Page() {
  const data = fetchData(); // en servidor
  return (
    <div>
      <ClientCounter initialCount={data.initialCount} />
    </div>
  );
}

// Client Component
'use client';
export function ClientCounter({ initialCount }) {
  const [count, setCount] = useState(initialCount);
  return <button onClick={() => setCount(c => c+1)}>{count}</button>;
}

Server Components puros (sin framework)

Teóricamente, se puede usar con React 18 + un bundler que soporte el protocolo RSC, pero en la práctica la mayoría usa Next.js o Remix.
Ventajas profundas

    Zero bundle para lógica de datos: las consultas y transformaciones ocurren en el servidor.

    Suspense integrado: los Server Components pueden ser async y usar await, mostrando fallbacks automáticos.

    Mejor seguridad: código sensible (credenciales de DB) nunca llega al cliente.

Desventajas y retos

    Curva de aprendizaje: entender cuándo usar 'use client'.

    Herramientas limitadas: muchas librerías de UI aún asumen cliente.

    No todas las apps necesitan RSC: una SPA tradicional puede seguir con solo client components.

Buenas prácticas

    Usa Server Components para todo lo que no requiera interacción (layouts, páginas, listas estáticas).

    Aísla la interactividad en componentes cliente pequeños.

    Pasa props serializables de servidor a cliente (no funciones, no símbolos).

    No abuses de 'use client' (cada vez que lo usas, todo el subárbol se envía al cliente).

📄 concurrent-mode.md
Concepto

Concurrent Mode (Modo Concurrente) es un conjunto de características en React 18+ que permite que React prepare múltiples versiones de la UI al mismo tiempo, pausando, priorizando o retomando el trabajo según la urgencia. El objetivo es mantener la aplicación respondiendo incluso durante renders pesados.
¿Qué resuelve?

    Renders largos bloquean el hilo principal: el usuario siente la UI congelada.

    Actualizaciones urgentes vs no urgentes: typing en input vs renderizado de gráficos.

    Mejor experiencia en dispositivos lentos.

Principios del modo concurrente

    Interrumpibilidad: React puede pausar un render costoso para atender una actualización urgente (ej. el usuario escribe).

    Priorización: las actualizaciones tienen diferentes prioridades (urgente = evento de usuario; normal = fetching; baja = análisis).

    Transiciones: marcar actualizaciones como "no urgentes" con useTransition.

Cómo habilitar el modo concurrente

En React 18, ya no existe un "modo" separado. En su lugar, usas nuevas APIs como createRoot:
jsx

// Antes (React 17)
ReactDOM.render(<App />, document.getElementById('root'));

// React 18 (concurrent features habilitadas)
import { createRoot } from 'react-dom/client';
const root = createRoot(document.getElementById('root'));
root.render(<App />);

Características clave
1. useTransition

Permite marcar una actualización como no urgente.
jsx

function SearchResults() {
  const [query, setQuery] = useState('');
  const [isPending, startTransition] = useTransition();
  
  const handleChange = (e) => {
    const value = e.target.value;
    // Actualización urgente (input del usuario)
    setQuery(value);
    
    // Actualización no urgente (búsqueda pesada)
    startTransition(() => {
      setSearchQuery(value);
    });
  };
  
  return (
    <div>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <ResultList query={searchQuery} />
    </div>
  );
}

2. useDeferredValue

Similar a useTransition pero para valores, no para actualizaciones de estado.
jsx

function App() {
  const [text, setText] = useState('');
  const deferredText = useDeferredValue(text);
  
  return (
    <>
      <input value={text} onChange={e => setText(e.target.value)} />
      <SlowList text={deferredText} /> {/* recibe versión "atrasada" */}
    </>
  );
}

3. Suspense mejorado

Puede esperar datos asíncronos y mostrar fallbacks sin necesidad de useEffect.
Cómo React prioriza las actualizaciones

    Eventos de usuario (click, input) → alta prioridad.

    Transiciones (cambio de ruta, búsqueda) → baja prioridad.

    Suspense y fetching → puede pausar hasta que los datos lleguen.

Ejemplo visual de concurrencia

Sin concurrencia:
text

Usuario escribe "hola" → React bloquea por 200ms renderizando lista → input se actualiza después → sensación de lag.

Con concurrencia:
text

Usuario escribe "h" → React actualiza input inmediatamente.
React empieza a renderizar lista con "h" → el usuario escribe "o" → React pausa render de lista, actualiza input, luego retoma render de lista.

Beneficios reales

    Aplicaciones más fluidas (especialmente en dispositivos de gama baja).

    Carga progresiva: puedes mostrar partes de la UI a medida que llegan datos.

    Mejor manejo de errores con Suspense.

Limitaciones

    No todas las librerías soportan concurrencia (aquellas que usan refs o mutaciones sincrónicas pueden fallar).

    Depuración más compleja porque los renders pueden ser interrumpidos.

    Solo funciona con createRoot (no con ReactDOM.render legacy).

Buenas prácticas

    Envuelve actualizaciones costosas en startTransition (cambios de ruta, filtros de listas grandes).

    Usa useDeferredValue para props que llegan a componentes pesados.

    No uses startTransition para actualizaciones de input de usuario (deben ser urgentes).

    Combina con Suspense para experiencias de carga fluidas.

React 18 sin concurrencia explícita

Si no usas useTransition ni useDeferredValue, tu app seguirá funcionando como antes, pero ganarás automatic batching y otras mejoras.
📄 suspense.md
Concepto

Suspense es un componente de React que permite "esperar" a que algo (datos, código, imágenes) esté listo antes de renderizar el contenido, mostrando un fallback (spinner, skeleton) mientras tanto.
Historia

    React 16.6: Suspense para lazy loading de componentes.

    React 18: Suspense para data fetching (con librerías compatibles como Relay, Next.js, o implementación manual con fetch y Suspense aún no estable).

Suspense para lazy loading (código)
jsx

const LazyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Cargando componente...</div>}>
      <LazyComponent />
    </Suspense>
  );
}

Suspense para data fetching (concepto)

La idea es que un componente puede "suspender" (lanzar una promesa) mientras carga datos. React captura esa promesa y muestra el fallback hasta que se resuelva.
jsx

// Ejemplo con una librería que soporta Suspense (Relay, SWR con suspense: true)
function UserProfile({ userId }) {
  const user = useSuspenseQuery(fetchUser, userId); // lanza promesa si no hay datos
  return <div>{user.name}</div>;
}

function Page({ userId }) {
  return (
    <Suspense fallback={<UserSkeleton />}>
      <UserProfile userId={userId} />
    </Suspense>
  );
}

Implementación manual de Suspense (solo entendimiento)
jsx

let resource = null;

function fetchResource(id) {
  let status = 'pending';
  let result;
  const promise = fetch(`/api/user/${id}`).then(r => r.json()).then(
    data => { status = 'success'; result = data; },
    error => { status = 'error'; result = error; }
  );
  return {
    read() {
      if (status === 'pending') throw promise;
      if (status === 'error') throw result;
      return result;
    }
  };
}

function User({ id }) {
  if (!resource) resource = fetchResource(id);
  const user = resource.read();
  return <p>{user.name}</p>;
}

Suspense con múltiples componentes
jsx

<Suspense fallback={<Spinner />}>
  <ComponenteA />
  <ComponenteB />
</Suspense>
// Espera a que todos los componentes hijos que suspenden estén listos

Si quieres fallbacks independientes, anida Suspense:
jsx

<Suspense fallback={<SpinnerA />}>
  <ComponenteA />
</Suspense>
<Suspense fallback={<SpinnerB />}>
  <ComponenteB />
</Suspense>

Suspense vs useEffect + loading
Con useEffect	Con Suspense
Estado de loading manual	Declarativo (fallback)
Riesgo de waterfall (carga secuencial)	Permite carga paralela
Más boilerplate	Menos código
No integrado con transiciones	Integración con useTransition
Suspense + Transiciones (evita fallbacks parpadeantes)
jsx

const [isPending, startTransition] = useTransition();

const handleRefresh = () => {
  startTransition(() => {
    setResource(fetchNewData()); // nueva petición que suspende
  });
};

return (
  <div>
    <button onClick={handleRefresh}>Refrescar</button>
    {isPending && <div>Actualizando...</div>}
    <Suspense fallback={<Spinner />}>
      <DataView resource={resource} />
    </Suspense>
  </div>
);

Suspense para imágenes (react-experimental)
jsx

function Image({ src, alt }) {
  const [isLoaded, setIsLoaded] = useState(false);
  // Sin suspender, solo ejemplo conceptual
  return (
    <>
      {!isLoaded && <div className="placeholder" />}
      <img src={src} alt={alt} onLoad={() => setIsLoaded(true)} style={{ display: isLoaded ? 'block' : 'none' }} />
    </>
  );
}

Buenas prácticas

    Usa Suspense en el nivel más alto posible para evitar múltiples fallbacks anidados.

    Combínalo con lazy para code splitting.

    Para data fetching, espera a que la API estable de Suspense madure o usa librerías como Relay, Next.js App Router.

    No abuses de Suspense para todo (en aplicaciones simples, useEffect sigue siendo válido).

Limitaciones actuales (React 18)

    Suspense para data fetching no es estable para uso general (solo con frameworks o implementaciones muy específicas). En Next.js App Router sí es estable.

    No evita waterfalls automáticamente (necesitas prefetch o cargar datos en paralelo).

📄 portals.md
Concepto

Portals permiten renderizar un componente en un nodo DOM diferente al del componente padre, manteniendo el contexto de React (eventos, contextos) intacto.
¿Por qué usar Portals?

    Modales, tooltips, popovers que deben romper el flujo z-index de CSS.

    Notificaciones globales que no deben estar limitadas por el overflow del contenedor.

    Widgets flotantes (chat, ayuda) que se montan al final del body.

Sintaxis básica
jsx

import { createPortal } from 'react-dom';

function Modal({ children, isOpen }) {
  if (!isOpen) return null;
  return createPortal(
    <div className="modal-overlay">
      <div className="modal-content">{children}</div>
    </div>,
    document.getElementById('modal-root') // nodo destino
  );
}

Configuración del nodo destino

En index.html:
html

<body>
  <div id="root"></div>
  <div id="modal-root"></div>
</body>

Mantenimiento del contexto

Aunque el modal se renderiza fuera del árbol DOM, el contexto de React (ej. ThemeContext) sigue funcionando porque el portal sigue siendo hijo lógico.
jsx

<ThemeProvider value="dark">
  <Modal isOpen={true}>
    <p>Este modal tendrá tema oscuro aunque esté en el body</p>
  </Modal>
</ThemeProvider>

Eventos con Portals

Los eventos de React (burbujeo) siguen el árbol de React, no el DOM. Si haces clic dentro del portal, el evento burbujeará hacia arriba en el árbol de componentes de React, no en el DOM real.
Portal con refs (acceder al nodo interno)
jsx

function Modal({ children }) {
  const modalRef = useRef();
  
  useEffect(() => {
    // modalRef.current es el div .modal-content que está en el portal
  }, []);
  
  return createPortal(
    <div className="modal-overlay">
      <div ref={modalRef} className="modal-content">{children}</div>
    </div>,
    document.getElementById('modal-root')
  );
}

Portal condicional (mount/desmount)

Puedes crear y destruir el portal dinámicamente. El nodo destino puede ser creado a demanda.
jsx

function DynamicPortal({ children }) {
  const [portalRoot, setPortalRoot] = useState(null);
  
  useEffect(() => {
    const div = document.createElement('div');
    document.body.appendChild(div);
    setPortalRoot(div);
    return () => document.body.removeChild(div);
  }, []);
  
  if (!portalRoot) return null;
  return createPortal(children, portalRoot);
}

Portal para eventos globales (escuchar fuera)
jsx

function ClickOutside({ onOutsideClick, children }) {
  const ref = useRef();
  
  useEffect(() => {
    const handleClick = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        onOutsideClick();
      }
    };
    document.addEventListener('click', handleClick);
    return () => document.removeEventListener('click', handleClick);
  }, [onOutsideClick]);
  
  return createPortal(
    <div ref={ref}>{children}</div>,
    document.body
  );
}

Buenas prácticas

    Úsalos solo cuando sea necesario (no abuses).

    Mantén la accesibilidad: asegura que el foco se maneje correctamente (trap focus en modales).

    Limpia el portal al desmontar si creaste nodos dinámicamente.

    No hagas estilos globales excesivos que asuman que el portal está dentro de un contenedor específico.

Alternativas a Portals

    CSS z-index y position: fixed dentro de un contenedor (a veces funciona, pero puede romperse por overflow: hidden).

    Librerías como react-modal (usan portals internamente).

Depuración

En React DevTools, los portales aparecen con un ícono especial, pero su ubicación en el árbol de componentes sigue la lógica de React, no el DOM.
📄 forwardRef.md
Concepto

forwardRef es una función de React que permite pasar una ref desde un componente padre a un elemento DOM específico dentro de un componente hijo. Es necesario porque por defecto las refs no se pasan a través de los componentes (a menos que se use forwardRef).
¿Por qué existe?

En React, los componentes funcionales no reciben ref como prop (es una prop especial como key). Si intentas pasar ref a un componente funcional, React la ignora.
jsx

// ❌ No funciona
function MiInput(props) {
  return <input {...props} />;
}
const ref = useRef();
<MiInput ref={ref} /> // ref no se asigna a nada

Solución con forwardRef
jsx

import { forwardRef } from 'react';

const MiInput = forwardRef((props, ref) => {
  return <input {...props} ref={ref} />;
});

// Uso en padre
const inputRef = useRef();
<MiInput ref={inputRef} />;
inputRef.current.focus();

forwardRef con componentes de clase (legado)
jsx

class MiInputClase extends React.Component {
  render() { return <input ref={this.props.forwardedRef} />; }
}
const MiInput = forwardRef((props, ref) => (
  <MiInputClase {...props} forwardedRef={ref} />
));

forwardRef con múltiples refs (uso de useImperativeHandle)

A veces quieres exponer solo ciertos métodos, no todo el nodo DOM.
jsx

const InputConImperative = forwardRef((props, ref) => {
  const inputRef = useRef();
  
  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
    clear: () => { inputRef.current.value = ''; },
    getValue: () => inputRef.current.value
  }));
  
  return <input ref={inputRef} {...props} />;
});

// Padre
const inputRef = useRef();
<InputConImperative ref={inputRef} />;
inputRef.current.focus(); // OK
inputRef.current.clear(); // OK

forwardRef en componentes de orden superior (HOC)
jsx

function withLogging(WrappedComponent) {
  const WithLogging = forwardRef((props, ref) => {
    useEffect(() => console.log('montado'), []);
    return <WrappedComponent {...props} ref={ref} />;
  });
  return WithLogging;
}

const EnhancedInput = withLogging(MiInput);
const ref = useRef();
<EnhancedInput ref={ref} />; // la ref llega al input interno

forwardRef con TypeScript
tsx

interface InputProps {
  placeholder: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => {
  return <input ref={ref} {...props} />;
});

forwardRef con elementos HTML personalizados (sin librería)

Si necesitas pasar una ref a un componente que no es un elemento nativo, forwardRef es la única manera.
Buenas prácticas

    No abuses de forwardRef: la mayoría de componentes no necesitan exponer refs. Prefiere composición y callbacks.

    Documenta qué ref hace (si es a un nodo DOM o a una API imperativa).

    Usa useImperativeHandle para limitar lo que se expone (mejor encapsulamiento).

    Nombra la prop interna (ej. innerRef) si el componente ya usa ref para otra cosa (poco común).

Alternativas a forwardRef

    Callback refs: puedes pasar una función que recibe el nodo.

jsx

function MiComponente({ innerRef }) {
  return <input ref={innerRef} />;
}
// Uso
const inputRef = useRef();
<MiComponente innerRef={(node) => (inputRef.current = node)} />

Pero es menos estándar.
forwardRef vs useRef en el mismo componente

    En el mismo componente: usas useRef.

    Para pasar ref a un hijo: usas forwardRef en el hijo.

Depuración

En React DevTools, los componentes envueltos con forwardRef aparecen con una etiqueta ForwardRef.

📄 transitions.md
Concepto

Las transiciones en React 18 permiten marcar actualizaciones de estado como no urgentes, manteniendo la interfaz responsiva mientras se renderizan componentes pesados. Son parte del modo concurrente.
Problema que resuelven

Sin transiciones, cualquier actualización de estado bloquea el hilo principal hasta que termina de renderizar. Si el render es costoso (filtrar una lista enorme, cambiar una ruta pesada), la interfaz se congela y el usuario siente "lag".
API principal: useTransition
jsx

import { useTransition, useState } from 'react';

function SearchPage() {
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    const value = e.target.value;
    // Actualización urgente: lo que el usuario ve inmediatamente
    setQuery(value);
    
    // Actualización no urgente: la búsqueda pesada
    startTransition(() => {
      const results = performExpensiveSearch(value);
      setSearchResults(results);
    });
  };

  return (
    <div>
      <input value={query} onChange={handleChange} />
      {isPending && <div className="spinner">Buscando...</div>}
      <ResultList results={searchResults} />
    </div>
  );
}

isPending

Indica si la transición está activa (aún no ha terminado). Útil para mostrar indicadores de carga sin bloquear la UI.
Diferencia entre useTransition y useDeferredValue
useTransition	useDeferredValue
Envuelve una actualización de estado	Envuelve un valor
Controlas cuándo y qué actualizar	React decide automáticamente cuándo diferir
Devuelve isPending para feedback	Solo devuelve el valor diferido
Ideal para manejadores de eventos	Ideal para props que vienen de un padre

Ejemplo con useDeferredValue:
jsx

function App() {
  const [text, setText] = useState('');
  const deferredText = useDeferredValue(text); // versión "lenta"
  
  return (
    <>
      <input value={text} onChange={e => setText(e.target.value)} />
      <SlowList text={deferredText} />
    </>
  );
}

Transiciones con Suspense

Puedes combinar startTransition con código que suspende (data fetching) para evitar que los fallbacks parpadeen:
jsx

const [isPending, startTransition] = useTransition();

const handleRefresh = () => {
  startTransition(() => {
    setResource(fetchData()); // esta petición puede suspender
  });
};

return (
  <div>
    <button onClick={handleRefresh}>Refrescar</button>
    {isPending && <div>Actualizando...</div>}
    <Suspense fallback={<Spinner />}>
      <Profile resource={resource} />
    </Suspense>
  </div>
);

¿Cuándo usar transiciones?

    Cambios de ruta (navegación entre páginas pesadas).

    Filtros / ordenamientos en listas grandes.

    Auto-completado con búsquedas costosas.

    Cualquier actualización que no necesite respuesta inmediata del usuario.

¿Cuándo NO usar transiciones?

    Input de texto, checkbox, toggles (deben ser urgentes).

    Animaciones dependientes de estado rápido.

    Validaciones en tiempo real que deben aparecer al instante.

Limitaciones

    startTransition solo puede usarse dentro de componentes o hooks.

    Si la actualización dentro de startTransition es muy rápida, isPending puede no llegar a mostrarse (bueno para UX).

    Solo funciona si el render se puede interrumpir; si tu componente tiene efectos secundarios no preparados para concurrencia, pueden ejecutarse múltiples veces.

Buenas prácticas

    Envuelve solo la actualización no urgente dentro de startTransition, no todo el manejador.

    No uses startTransition para cada setState; úsalo estratégicamente.

    Combínalo con Suspense para transiciones de rutas o datos.

    Si usas librerías de estado (Redux, Zustand), asegúrate de que soporten transiciones (la mayoría sí, pero la actualización debe estar envuelta).

📄 automatic-batching.md
Concepto

Automatic batching (agrupación automática) es una optimización que React realiza para combinar múltiples actualizaciones de estado en un solo re-render, mejorando el rendimiento.
En React 17 y anteriores

El batching solo ocurría dentro de manejadores de eventos de React (como onClick, onChange). Fuera de ellos (promesas, setTimeout, fetch, eventos nativos), no había batching y cada setState causaba un re-render independiente.
jsx

// React 17: sin batching fuera de eventos
function App() {
  const [count, setCount] = useState(0);
  const [flag, setFlag] = useState(false);

  const handleClick = () => {
    setCount(c => c+1);  // provoca re-render
    setFlag(f => !f);    // otro re-render → 2 renders
  };

  const handleAsync = () => {
    fetch('/api').then(() => {
      setCount(c => c+1); // re-render 1
      setFlag(f => !f);   // re-render 2
    });
  };
}

En React 18 (con createRoot)

El batching automático funciona en cualquier lugar, incluso dentro de promesas, setTimeout, eventos nativos, etc.
jsx

// React 18: batching automático siempre
const root = createRoot(document.getElementById('root'));
root.render(<App />);

function App() {
  const [count, setCount] = useState(0);
  const [flag, setFlag] = useState(false);

  const handleAsync = () => {
    fetch('/api').then(() => {
      setCount(c => c+1); // marca actualización
      setFlag(f => !f);   // marca actualización
      // React agrupa y re-renderiza solo una vez
    });
  };
}

¿Qué pasa si necesitas forzar un re-render intermedio?

Puedes usar flushSync (importado de react-dom) para salir del batching:
jsx

import { flushSync } from 'react-dom';

const handleClick = () => {
  flushSync(() => {
    setCount(c => c+1);  // re-render inmediato
  });
  // Ya puedes leer el DOM actualizado
  flushSync(() => {
    setFlag(f => !f);    // otro re-render
  });
};

Usar flushSync raramente es necesario y puede dañar el rendimiento.
Beneficios del automatic batching

    Menos renders → mejor rendimiento.

    Código más simple (no necesitas pensar en optimizar manualmente).

    Comportamiento consistente dentro y fuera de eventos.

Detalles técnicos

React agrupa actualizaciones que ocurren en la misma "tarea" (microtask o macrotask) usando el scheduler interno. Las actualizaciones dentro de startTransition también se agrupan, pero con prioridad más baja.
Ejemplo complejo con múltiples fuentes
jsx

function Componente() {
  const [a, setA] = useState(0);
  const [b, setB] = useState(0);
  const [c, setC] = useState(0);

  useEffect(() => {
    setA(1);
    setB(2);
    Promise.resolve().then(() => setC(3));
    // a y b se agrupan en 1 render, c puede ser en otro microtask
  }, []);
}

Compatibilidad con librerías

Librerías como Redux, Zustand, React Query se benefician automáticamente porque sus actualizaciones también se agrupan si usan setState o hooks internos de React.
Buenas prácticas

    Confía en el batching automático; no necesitas unstable_batchedUpdates (API antigua).

    Evita flushSync a menos que tengas una razón muy específica (ej. medir DOM justo después de un cambio).

    Actualiza múltiples estados independientes en secuencia; React los agrupará.

📄 new-hooks.md

React 18 introdujo varios hooks nuevos. Aquí se detallan los más importantes: useId, useSyncExternalStore, useInsertionEffect, y también useDeferredValue (ya mencionado en transiciones) y useTransition (visto arriba).
1. useId

Genera identificadores únicos y estables para accesibilidad (atributos id). Es especialmente útil en SSR (Server Side Rendering) para evitar inconsistencias entre servidor y cliente.
jsx

import { useId } from 'react';

function CampoNombre() {
  const id = useId();
  return (
    <>
      <label htmlFor={id}>Nombre:</label>
      <input id={id} type="text" />
    </>
  );
}

Características:

    Los IDs son únicos globalmente dentro de la aplicación.

    Son estables entre renders (no cambian).

    Funcionan con hidratación (servidor y cliente generan el mismo ID).

    No usar para key en listas.

Ejemplo con múltiples elementos relacionados:
jsx

function Formulario() {
  const id = useId();
  return (
    <div>
      <label htmlFor={`${id}-nombre`}>Nombre</label>
      <input id={`${id}-nombre`} type="text" />
      <label htmlFor={`${id}-email`}>Email</label>
      <input id={`${id}-email`} type="email" />
    </div>
  );
}

¿Por qué no usar Math.random() o useState(0)+1?

    En SSR, el servidor y el cliente generarían números distintos, causando advertencias de hidratación.

    useId garantiza consistencia.

2. useSyncExternalStore

Hook avanzado para suscribirse a fuentes de datos externas (stores fuera de React) y mantener la UI sincronizada. Fue diseñado para autores de librerías (Redux, Zustand, etc.) pero puede usarse directamente.
jsx

import { useSyncExternalStore } from 'react';

// Store externa simple (ejemplo)
let nextId = 0;
let todos = [{ id: nextId++, text: 'Aprender React 18' }];
let listeners = [];

function subscribe(listener) {
  listeners.push(listener);
  return () => {
    listeners = listeners.filter(l => l !== listener);
  };
}

function getSnapshot() {
  return todos;
}

function addTodo(text) {
  todos = [...todos, { id: nextId++, text }];
  listeners.forEach(l => l());
}

function TodoList() {
  const todos = useSyncExternalStore(subscribe, getSnapshot);
  return (
    <ul>
      {todos.map(todo => <li key={todo.id}>{todo.text}</li>)}
    </ul>
  );
}

Parámetros:

    subscribe: recibe un callback y retorna una función de limpieza.

    getSnapshot: devuelve el estado actual (debe ser inmutable o al menos estable).

    getServerSnapshot (opcional): para SSR, devuelve el estado inicial en el servidor.

Uso típico con Redux:
jsx

import { useSyncExternalStore } from 'react';
import store from './reduxStore';

function useReduxStore() {
  return useSyncExternalStore(store.subscribe, store.getState);
}

¿Por qué no useState + useEffect?

    Con useEffect, la suscripción puede ocurrir después del render inicial, causando un desfase.

    useSyncExternalStore es síncrono y evita "tearing" (mostrar estados inconsistentes durante renders concurrentes).

3. useInsertionEffect

Hook para inyectar estilos dinámicos en el DOM antes de que se apliquen los efectos de layout. Es útil para librerías de CSS-in-JS que necesitan insertar <style> etiquetas y evitar conflictos de medición.
jsx

import { useInsertionEffect } from 'react';

function useDynamicStyles(className, styles) {
  useInsertionEffect(() => {
    const styleSheet = document.createElement('style');
    styleSheet.textContent = `
      .${className} {
        color: ${styles.color};
        background: ${styles.background};
      }
    `;
    document.head.appendChild(styleSheet);
    return () => styleSheet.remove();
  }, [className, styles.color, styles.background]);
}

function Button({ color, background }) {
  const className = useMemo(() => `btn-${Math.random()}`, []);
  useDynamicStyles(className, { color, background });
  return <button className={className}>Click</button>;
}

Diferencia con useEffect y useLayoutEffect:

    useInsertionEffect se ejecuta antes de cualquier useLayoutEffect y useEffect.

    No puede acceder a refs del DOM (porque el DOM aún se está mutando).

    Está pensado solo para inserción de estilos dinámicos, no para lógica general.

Cuándo usarlo:

    Librerías CSS-in-JS como styled-components (implementación interna).

    Inyección de reglas CSS críticas antes de que el navegador pinte.

    No lo necesitas en aplicaciones típicas que usan CSS modules o Tailwind.

4. useDeferredValue (repaso)

Permite diferir una actualización de valor. Ya se mencionó en transiciones, pero aquí se detalla como hook independiente.
jsx

const deferredValue = useDeferredValue(value, { timeoutMs: 5000 });

    Devuelve una versión "atrasada" de value.

    React retrasa la actualización si hay trabajo urgente.

    Opcionalmente, puedes establecer un timeoutMs para forzar la actualización después de un tiempo.

Ejemplo con lista grande:
jsx

function Search() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  
  const results = useMemo(() => 
    searchInBigList(deferredQuery),
    [deferredQuery]
  );
  
  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <div style={{ opacity: query !== deferredQuery ? 0.5 : 1 }}>
        <List results={results} />
      </div>
    </>
  );
}

5. useEvent (experimental, no estable)

En futuras versiones (React 18+ experimental), useEvent permite crear funciones con referencias estables pero que siempre acceden a las props/estado más recientes. No incluido en estable aún.
Resumen de hooks nuevos (React 18+)
Hook	Propósito principal	Uso típico
useId	Generar IDs únicos para atributos de accesibilidad	Formularios, etiquetas ARIA
useSyncExternalStore	Suscribirse a stores externos (Redux, Zustand, etc.)	Autores de librerías o integraciones manuales
useInsertionEffect	Insertar estilos dinámicos antes del layout	CSS-in-JS
useTransition	Marcar actualizaciones no urgentes	Búsquedas, cambios de ruta
useDeferredValue	Diferir una prop o valor pesado	Listas filtradas, gráficos
useLayoutEffect	(existía, pero mejorado para concurrencia)	Mediciones DOM síncronas
Buenas prácticas con nuevos hooks

    useId: Úsalo siempre que necesites id para accesibilidad en componentes reutilizables.

    useSyncExternalStore: No lo uses directamente a menos que escribas una librería; prefiere el store ya adaptado (ej. Redux con useSelector).

    useInsertionEffect: Ignóralo en aplicaciones de negocio; está pensado para librerías.

    useDeferredValue y useTransition: Úsalos cuando notes lag en la UI por renders pesados.

