# Postman & Newman

Aunque el SDET tiende a usar código, Postman/Newman sigue siendo necesario para equipos donde la colaboración con QA menos técnicos es vital.

## Postman

- **Colecciones**: Agrupan peticiones. Soporta variables en diferentes ámbitos (global, colección, entorno).
- **Scripts**: Permite scripts *pre-request* y *tests* en JavaScript para programar lógica de prueba y encadenamiento.
- **Ecosistema**: Integración con monitores, versionamiento y documentación.

## Newman

Es el CLI (Command Line Interface) que ejecuta colecciones de Postman sin interfaz gráfica.

### Uso
```bash
newman run mi-coleccion.json -e entorno.json --reporters cli,junit
```

### Aplicación
Permite integrar colecciones como prueba de humo (*smoke tests*) en pipelines CI/CD, aunque con limitaciones en mantenibilidad cuando crece la complejidad.

> [!TIP]
> **Rol del SDET**: Puede generar colecciones desde definiciones OpenAPI; usarlas como punto de partida para migrar a REST Assured o código más robusto. También definir estándares para que los QA escriban colecciones que Newman ejecute en CI.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [REST Assured](./REST-Assured.md) | [Home](../../index.md) | [GraphQL Testing](./GraphQL-testing.md) |