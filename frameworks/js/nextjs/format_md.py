import re

with open('/home/hermandev/Documents/proyectos/1Profecional/mainframeV2/frameworks/js/nextjs/index.md', 'r') as f:
    lines = f.readlines()

output = []
in_code_block = False
code_lang = ""

i = 0
while i < len(lines):
    line = lines[i].rstrip()
    
    # Check if line is just a language identifier for a code block
    if not in_code_block and line in ['jsx', 'js', 'ts', 'tsx', 'text', 'html', 'css'] and (i+1 < len(lines) and lines[i+1].strip() == ''):
        # start code block
        in_code_block = True
        code_lang = line
        output.append(f"```{code_lang}")
        i += 1
        if i < len(lines) and lines[i].strip() == '':
            i += 1 # skip empty line after lang
        continue
    
    # End of code block is trickier because there are no closing tags. 
    # Usually code blocks end when there is a new paragraph of normal text that is not indented, or another header.
    # Actually wait, there are no closing tags at all? 
    # Let's see the original text...
