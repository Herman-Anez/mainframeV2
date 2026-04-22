# tar

El comando tar es una herramienta clásica de sistemas Unix/Linux que sirve para agrupar varios archivos y directorios en un solo archivo (llamado “tarball”) y, opcionalmente, comprimirlo.

tar [opciones] archivo.tar [archivos o directorios]

Funciones principales

## Crear un archivo .tar

tar -cvf archivo.tar carpeta/

-c → crear archivo

-v → modo verbose (muestra lo que hace)

-f → especifica el nombre del archivo

👉 Esto NO comprime, solo agrupa.

## Extraer un archivo .tar

tar -xvf archivo.tar

-x → extraer

## Ver contenido sin extraer

tar -tvf archivo.tar

-t → listar contenido

🗜️ Compresión con tar
tar suele combinarse con algoritmos de compresión:

🔹 Con gzip (.tar.gz o .tgz)
tar -czvf archivo.tar.gz carpeta/

-z → usa gzip

Extraer:
tar -xzvf archivo.tar.gz

🔹 Con bzip2 (.tar.bz2)
tar -cjvf archivo.tar.bz2 carpeta/

-j → usa bzip2

🔹 Con xz (.tar.xz)
tar -cJvf archivo.tar.xz carpeta/

-J → usa xz (mejor compresión, más lento)

📁 Ejemplos útiles
Comprimir varios archivos
tar -czvf backup.tar.gz archivo1.txt archivo2.txt carpeta/

Extraer en una carpeta específica
tar -xzvf archivo.tar.gz -C /ruta/destino/

Excluir archivos
tar -czvf backup.tar.gz carpeta/ --exclude="*.log"

⚡ Resumen rápido
AcciónComando básicoCreartar -cvf archivo.tarExtraertar -xvf archivo.tarListartar -tvf archivo.targzip-zbzip2-jxz-J

🧩 Concepto clave

.tar = empaquetado

.gz, .bz2, .xz = compresión

👉 Es decir:

tar junta → el compresor reduce tamaño

Si quieres, puedo darte ejercicios prácticos o explicarte errores comunes (como rutas, permisos o sobrescritura), que es donde la mayoría se confunde.

 ejemplo

tar -czvf docs.tar.gz docs/xxxDxxxD
