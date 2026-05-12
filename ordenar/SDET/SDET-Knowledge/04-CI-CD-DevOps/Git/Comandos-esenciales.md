Comandos esenciales

Más allá de add, commit, push, el arsenal avanzado de un SDET cubre:

    Gestión de ramas y estado:

        git fetch --prune: limpia referencias locales a ramas remotas eliminadas.

        git branch -a: lista todas las ramas locales y remotas.

        git checkout -b feature/test-123: crea y cambia a una rama nueva para una historia.

        git stash / git stash pop: guarda cambios rápidamente para cambiar de contexto sin hacer commit (útil cuando estás depurando una prueba y necesitas probar otra rama).

        git stash list / git stash drop: gestionar el stack de cambios temporales.

    Historial y depuración:

        git log --oneline --graph --decorate --all: visualiza el grafo de ramas y merges.

        git diff main...feature/rama o git diff --name-only: ver diferencias de archivos entre ramas.

        git blame <archivo>: identifica quién modificó cada línea; útil para rastrear cuándo un localizador o configuración cambió y empezó a fallar.

        git bisect start / git bisect bad / git bisect good: herramienta de búsqueda binaria para encontrar el commit exacto que introdujo una regresión en las pruebas. Flujo típico: marcas un commit malo (tests fallan) y uno bueno (tests pasan), y Git te va llevando a puntos intermedios para que ejecutes la suite y marques good o bad. Como SDET, puedes automatizar git bisect run con un script que lance el test fallido.

        git revert <commit> vs git reset: el primero crea un nuevo commit que deshace cambios; el segundo mueve el puntero. Para revertir un merge incorrecto, git revert -m 1 <commit>.

    Rebase y sincronización:

        git rebase main: reaplica tus commits de la rama actual sobre la punta de main, manteniendo un historial lineal. Preferible a merge en ramas de características para mantener limpio el historial de la suite de pruebas.

        git rebase --continue / --skip / --abort: control del proceso interactivo.

        git cherry-pick <commit>: trae un commit específico de otra rama sin fusionar toda la rama. Muy usado en automatización para portar una corrección de un flaky test entre ramas de release.

    Submódulos (submodules):

        Muchos equipos centralizan utilidades comunes (drivers, factories, reportes) en un repositorio aparte que se incluye como submódulo en el proyecto de pruebas.

        git submodule add <url> <path> y git submodule update --init --recursive.

        El SDET define la estrategia de versionado para que las pruebas no se rompan por una actualización no deseada del submódulo (apuntar a un tag específico).

    Tags y releases:

        git tag -a v1.2.3 -m "Suite de regresión release 1.2.3" y git push origin --tags: permite vincular exactamente la versión de las pruebas con la versión del producto bajo test. Las pipelines pueden ejecutar la suite etiquetada para una release concreta.