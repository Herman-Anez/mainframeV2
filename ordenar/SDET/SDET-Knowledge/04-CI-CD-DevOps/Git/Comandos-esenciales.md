# Comandos esenciales de Git

Más allá de `add`, `commit`, `push`, el arsenal avanzado de un SDET cubre herramientas críticas para la depuración y gestión de suites de automatización.

## Gestión de ramas y estado

*   `git fetch --prune`: Limpia referencias locales a ramas remotas eliminadas.
*   `git branch -a`: Lista todas las ramas locales y remotas.
*   `git checkout -b feature/test-123`: Crea y cambia a una rama nueva para una historia.
*   `git stash` / `git stash pop`: Guarda cambios rápidamente para cambiar de contexto sin hacer commit.
    > [!TIP]
    > Muy útil cuando estás depurando una prueba y necesitas saltar a otra rama para verificar algo rápidamente.
*   `git stash list` / `git stash drop`: Gestionar el stack de cambios temporales.

## Historial y depuración

*   `git log --oneline --graph --decorate --all`: Visualiza el grafo de ramas y merges de forma compacta.
*   `git diff main...feature/rama` o `git diff --name-only`: Ver diferencias de archivos entre ramas.
*   `git blame <archivo>`: Identifica quién modificó cada línea.
    > [!NOTE]
    > Esencial para rastrear cuándo un localizador (selector) o configuración cambió y empezó a causar fallos en las pruebas.
*   `git bisect start` / `git bisect bad` / `git bisect good`: Herramienta de búsqueda binaria para encontrar el commit exacto que introdujo una regresión.
    *   **Flujo típico:** Marcas un commit malo (tests fallan) y uno bueno (tests pasan), y Git te lleva a puntos intermedios.
    *   **Automatización:** Como SDET, puedes automatizar `git bisect run` con un script que lance el test fallido.
*   `git revert <commit>` vs `git reset`: El primero crea un nuevo commit que deshace cambios; el segundo mueve el puntero. Para revertir un merge incorrecto: `git revert -m 1 <commit>`.

## Rebase y sincronización

*   `git rebase main`: Reaplica tus commits sobre la punta de `main`, manteniendo un historial lineal.
    > [!IMPORTANT]
    > Preferible a `merge` en ramas de características para mantener limpio el historial de la suite de pruebas.
*   `git rebase --continue` / `--skip` / `--abort`: Control del proceso interactivo.
*   `git cherry-pick <commit>`: Trae un commit específico de otra rama sin fusionar toda la rama.
    > [!TIP]
    > Muy usado en automatización para portar una corrección de un *flaky test* entre ramas de release.

## Submódulos (Submodules)

Muchos equipos centralizan utilidades comunes (drivers, factories, reportes) en un repositorio aparte que se incluye como submódulo en el proyecto de pruebas.

*   `git submodule add <url> <path>`
*   `git submodule update --init --recursive`

El SDET define la estrategia de versionado para que las pruebas no se rompan por una actualización no deseada del submódulo (apuntar a un tag específico).

## Tags y Releases

*   `git tag -a v1.2.3 -m "Suite de regresión release 1.2.3"`
*   `git push origin --tags`

Permite vincular exactamente la versión de las pruebas con la versión del producto bajo test. Las pipelines pueden ejecutar la suite etiquetada para una release concreta.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Git para SDET](./index.md) | [Home](../../../index.md) | [Estrategias de ramas](./Estrategias-ramas.md) |