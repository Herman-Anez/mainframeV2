Postman & Newman

Aunque el SDET tiende a usar código, Postman/Newman sigue siendo necesario para equipos donde la colaboración con QA menos técnicos es vital.

Postman:

    Colecciones: agrupan peticiones. Variables en diferentes ámbitos (global, colección, entorno).

    Scripts pre-request y tests en JavaScript: se puede programar lógica de prueba y encadenamiento.

    Integración con monitores y versionamiento.

Newman:

    CLI que ejecuta colecciones de Postman sin interfaz gráfica.

    Uso: newman run mi-coleccion.json -e entorno.json --reporters cli,junit

    Permite integrar colecciones como prueba de humo en pipelines CI/CD, aunque con limitaciones en mantenibilidad cuando crece la complejidad.

    Rol del SDET: Puede generar colecciones desde definiciones OpenAPI; usarlas como punto de partida para migrar a REST Assured o código más robusto. También definir estándares para que los QA escriban colecciones que Newman ejecute en CI.