import os
import sys

def main():
    tree_file = 'tree.txt'
    aux_file = 'aux-index.md'
    
    # 1. Leer la estructura del arbol
    try:
        with open(tree_file, 'r', encoding='utf-8') as f:
            tree_lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {tree_file}")
        sys.exit(1)
        
    current_dir = ""
    targets = {}
    
    for line in tree_lines:
        clean_line = line.strip()
        if not clean_line:
            continue
            
        # Es un directorio (sección)
        if clean_line.endswith('/') and not ('├── ' in clean_line or '└── ' in clean_line):
            current_dir = clean_line[:-1]
            clean_section = current_dir.replace('_', ' ')
            targets[current_dir] = f"# {clean_section}"
            
        # Es un archivo (tema)
        elif '├── ' in clean_line or '└── ' in clean_line:
            filename = clean_line.replace('├── ', '').replace('└── ', '').strip()
            
            # Ignorar subdirectorios que aparezcan en el árbol (ej. 01_hola_mundo/)
            if filename.endswith('/'):
                continue
                
            path = f"{current_dir}/{filename}" if current_dir else filename
            
            # Limpiamos el título para que se vea legible, quitando .md y guiones bajos
            clean_title = filename.replace('.md', '').replace('_', ' ')
            
            # Guardamos tanto la ruta completa como solo el nombre del archivo como posibles búsquedas
            targets[path] = f"## {clean_title}"
            targets[filename] = f"## {clean_title}"
            
    # Ordenar los targets por longitud descendente para que busque primero las rutas completas
    sorted_targets = sorted(targets.items(), key=lambda x: len(x[0]), reverse=True)
    
    # 2. Procesar aux-index.md
    try:
        with open(aux_file, 'r', encoding='utf-8') as f:
            aux_lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {aux_file}")
        sys.exit(1)
        
    new_lines = []
    modificaciones = 0
    
    for line in aux_lines:
        stripped = line.strip()
        replaced = False
        
        # Buscar si la línea actual corresponde a un tema/sección
        for path, formatted_title in sorted_targets:
            if path in stripped:
                # Para evitar reemplazar coincidencias parciales dentro de un párrafo normal,
                # nos aseguramos de que la línea consista casi exclusivamente en el path.
                # Permitimos un margen de 15 caracteres (por si hay guiones, espacios, etc).
                if len(stripped) <= len(path) + 15:
                    # Aplicamos el # o ## y borramos lo que estaba antes en la línea
                    new_lines.append(formatted_title + "\n")
                    replaced = True
                    modificaciones += 1
                    break
        
        if not replaced:
            new_lines.append(line)
            
    # 3. Guardar los cambios
    with open(aux_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
    print(f"Completado: se aplicaron {modificaciones} modificaciones de títulos en {aux_file}.")

if __name__ == '__main__':
    main()
