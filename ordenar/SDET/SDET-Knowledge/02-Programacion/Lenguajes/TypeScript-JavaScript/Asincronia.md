Asincronía

La naturaleza asíncrona de JavaScript es crítica al automatizar interacciones con el navegador y APIs. Entenderla evita pruebas erráticas.

    Callbacks a Promesas: Las APIs modernas de navegador (fetch) están basadas en promesas. Cypress y Playwright gestionan internamente las esperas automáticas, pero al escribir tests se necesita encadenar .then() o usar async/await.

    Async/await: Es el estilo preferido. Hace que el código de prueba parezca síncrono.
    typescript

    test('debe mostrar el usuario', async () => {
        const response = await request.get('/api/user/1');
        expect(response.status()).toBe(200);
    });

    Manejo en Playwright: Todos los métodos de interacción (page.click(), page.fill()) retornan promesas. Usar await garantiza que la acción se completa antes de la siguiente instrucción.

    Esperas explícitas y race conditions: Aunque las herramientas tienen auto-esperas, a veces se requiere page.waitForSelector() o page.waitForResponse(). El SDET debe saber cuándo usar Promise.all() para ejecutar acciones paralelas (ej. hacer clic y esperar navegación).

    Testing de código asíncrono con Jest: Jest requiere devolver la promesa o usar async/await con expect. Si no, la prueba puede finalizar antes de las aserciones y dar falsos positivos.