
📄 7-testing/testing-library.md
Concepto

React Testing Library (RTL) es una librería que promueve pruebas centradas en el comportamiento del usuario, no en los detalles de implementación. Se integra con Jest.
Principios fundamentales

    Cuanto más se parezcan tus pruebas a la forma en que se usa el software, más confianza pueden dar.

    No pruebes detalles internos (estado, métodos, props internos).

    Trabaja con elementos accesibles (roles, etiquetas, texto).

Instalación
bash

npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event

Configuración (setupTests.js)
js

import '@testing-library/jest-dom';

Prueba básica de un componente
jsx

import { render, screen } from '@testing-library/react';
import Saludo from './Saludo';

test('muestra el mensaje de saludo', () => {
  render(<Saludo nombre="Ana" />);
  const elemento = screen.getByText(/hola ana/i);
  expect(elemento).toBeInTheDocument();
});

Queries (selectores)

RTL prioriza queries accesibles:
Query	Descripción
getByRole	Busca por rol ARIA (button, heading, etc.)
getByLabelText	Busca por etiqueta de formulario
getByPlaceholderText	Por placeholder
getByText	Por texto del elemento
getByDisplayValue	Por valor actual de input
getByAltText	Por atributo alt de imagen
getByTitle	Por atributo title

Variantes: getBy, queryBy (no lanza error si no encuentra), findBy (para elementos asíncronos).
Eventos de usuario (user-event)

Recomendado sobre fireEvent porque simula interacciones más realistas.
jsx

import userEvent from '@testing-library/user-event';

test('clic en botón incrementa contador', async () => {
  const user = userEvent.setup();
  render(<Contador />);
  const boton = screen.getByRole('button', { name: /incrementar/i });
  await user.click(boton);
  expect(screen.getByText(/1/)).toBeInTheDocument();
});

Pruebas asíncronas (waitFor, findBy)
jsx

test('carga y muestra datos', async () => {
  render(<DatosAsync />);
  expect(await screen.findByText('Ana')).toBeInTheDocument();
  // o con waitFor
  await waitFor(() => {
    expect(screen.getByText('Ana')).toBeInTheDocument();
  });
});

Mock de llamadas API
jsx

import axios from 'axios';
jest.mock('axios');

test('fetch y muestra usuarios', async () => {
  axios.get.mockResolvedValue({ data: [{ name: 'Ana' }] });
  render(<ListaUsuarios />);
  const items = await screen.findAllByRole('listitem');
  expect(items).toHaveLength(1);
});

Pruebas de formularios
jsx

test('envía el formulario con los datos', async () => {
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

Pruebas de contexto y providers

Envuelve el componente en los providers necesarios:
jsx

function renderWithProviders(ui, { providerProps = {} } = {}) {
  return render(
    <AuthProvider {...providerProps}>
      <ThemeProvider>
        {ui}
      </ThemeProvider>
    </AuthProvider>
  );
}

Pruebas de React Router
jsx

import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import MiComponenteConLinks from './MiComponenteConLinks';

test('navegación funciona', () => {
  render(
    <MemoryRouter initialEntries={['/']}>
      <MiComponenteConLinks />
    </MemoryRouter>
  );
  // ...
});

Depuración
jsx

screen.debug(); // imprime el DOM actual en consola
screen.debug(screen.getByRole('main')); // solo una parte

Qué NO probar con RTL

    Detalles de implementación (estado interno, métodos de clase).

    Estilos CSS (a menos que cambien la accesibilidad).

    Versiones anteriores del DOM (snapshots completos).

Buenas prácticas

    Usa getByRole siempre que sea posible (fomenta accesibilidad).

    Evita data-testid a menos que no haya alternativa.

    Cada prueba debe probar una sola cosa (una interacción, un resultado).

    Limpia mocks después de cada prueba (jest.clearAllMocks()).

Ejemplo completo de prueba de componente
jsx

// Toggle.jsx
function Toggle() {
  const [on, setOn] = useState(false);
  return (
    <div>
      <button onClick={() => setOn(!on)}>
        {on ? 'Apagar' : 'Encender'}
      </button>
      {on && <p>Estado: Encendido</p>}
    </div>
  );
}

// Toggle.test.jsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Toggle from './Toggle';

test('muestra el mensaje al encender y lo oculta al apagar', async () => {
  const user = userEvent.setup();
  render(<Toggle />);
  
  const boton = screen.getByRole('button', { name: /encender/i });
  await user.click(boton);
  
  expect(screen.getByText(/encendido/i)).toBeInTheDocument();
  expect(boton).toHaveTextContent('Apagar');
  
  await user.click(boton);
  expect(screen.queryByText(/encendido/i)).not.toBeInTheDocument();
});

Con esto, las carpetas 6-routing/ y 7-testing/ quedan completamente desarrolladas. ¿Necesitas que continúe con las siguientes secciones (8-advanced/, 9-react-18-plus/, etc.)?