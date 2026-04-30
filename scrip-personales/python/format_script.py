import re

def main():
    with open('aux-index.md', 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f]

    out_lines = []
    i = 0
    in_code_block = False
    lines_in_block = 0
    
    code_start_keywords = {
        'import', 'export', 'const', 'let', 'var', 'function', 'return', 
        'if', 'else', 'for', 'while', 'switch', 'case', 'default', 
        '}', ']', ')', 'type', 'interface', '{', '/*', '*', '//', '<', 
        '...', 'await', 'async', 'class', 'console.log', "'use", '"use',
        'npm', 'npx', 'yarn', 'pnpm', 'node', 'git', 'yaml', 'bash', 'javascript',
        'cd', 'ls', 'cat', 'echo', 'mkdir', 'rm', 'cp', 'mv', 'sudo', 'docker', 'apt', 'apt-get', 'export','java', 'curl', 'wget',
        'public', 'private', 'protected', 'static', 'void', 'final', 'package', 'System.out.println', 'String', 'int', 'boolean', 'double', 'long', 'byte', 'short', 'float', 'char'
    }

    def is_text_line(line, prev_line_empty):
        stripped = line.strip()
        if not stripped:
            return False
            
        first_word = stripped.split()[0] if stripped.split() else ''
        
        # If it starts with common JS/bash/Java keywords or brackets, it's code
        if first_word in code_start_keywords or stripped.startswith(('}', ')', ']', '</', '/>', '{', '[', '"', "'", '`', '-', '$', '#', '@')):
            return False
            
        # Exception for Next.js folder structures (text blocks)
        if first_word in ['├──', '│', '└──', 'app/']:
            return False
            
        # If it's indented...
        if line.startswith(' ') or line.startswith('\t'):
            # If it's heavily indented text that starts with a capital letter and previous line was empty, it might be a list item/text.
            # Especially if it doesn't contain typical code symbols like =, {, }, (, )
            if prev_line_empty and first_word[0].isupper() and not any(c in stripped for c in '={}()'):
                return True
            return False

        # Otherwise it's likely text
        return True

    while i < len(lines):
        line = lines[i]

        # 1. File boundaries
        if re.match(r'^\d{2}-.*\.md$', line.strip()):
            out_lines.append(f"---\n\n## Archivo: `{line.strip()}`\n")
            i += 1
            continue

        # 2. Start of code block
        if not in_code_block and line.strip() in ['jsx', 'js', 'tsx', 'ts', 'text', 'html', 'css', 'json', 'bash', 'sh', 'java']:
            lang = line.strip()
            in_code_block = True
            lines_in_block = 0
            out_lines.append(f"```{lang}")
            i += 1
            # Skip immediate empty line after language identifier if there is one
            if i < len(lines) and lines[i].strip() == '':
                i += 1
            continue

        # 3. Inside code block
        if in_code_block:
            prev_empty = (i > 0 and lines[i-1].strip() == '')
            if lines_in_block > 0 and is_text_line(line, prev_empty) and prev_empty:
                in_code_block = False
                
                if out_lines and out_lines[-1].strip() == '':
                    out_lines.insert(-1, "```")
                else:
                    out_lines.append("```")
            else:
                out_lines.append(line)
                lines_in_block += 1
                i += 1
                continue
                
        # Headers heuristic
        if not in_code_block and line.strip():
            stripped = line.strip()
            if len(stripped) > 2 and len(stripped) < 80:
                if not stripped.endswith(('.', ':', '?', '!')) and not stripped.startswith(('-', '*', '1.', '2.', '3.')):
                    if i > 0 and lines[i-1].strip() == '':
                        if out_lines and out_lines[-1].strip() == '':
                            out_lines.append(f"### {stripped}")
                            i += 1
                            continue

        if not in_code_block:
            out_lines.append(line)
            
        i += 1

    if in_code_block:
        out_lines.append("```")

    with open('index.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines) + '\n')

if __name__ == '__main__':
    main()
