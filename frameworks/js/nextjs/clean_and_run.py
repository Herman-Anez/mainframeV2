import os

def clean_and_format():
    with open('index.md', 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    # Step 1: Revert all code blocks
    raw_lines = []
    for line in lines:
        if line.startswith('```') and len(line) > 3:
            raw_lines.append(line[3:])
        elif line.strip() == '```':
            continue
        else:
            raw_lines.append(line)

    # Write the intermediate raw file
    with open('index.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(raw_lines))

    # Step 2: Run the format script again
    os.system('python3 format_script.py')

if __name__ == '__main__':
    clean_and_format()
