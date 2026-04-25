
Detecta bloques de codigo vacios en markdowns
^```(\S*)\s*\n\s*```$

USO
```someText
```

Detecta # solitarios en markdowns
^\s*#\s*$


(?<=^\s*)#.*  //toda la linea
(?<=^\s*)#  // solo el #
(?<=^\s*)#(?!\!) // excluye los que tengan un !