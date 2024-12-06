import sys


DIRECT_OPERATORS = {
    'PATH': 'ctx.beginPath()',
    'FILL': 'ctx.fill()',
    'STROKE': 'ctx.stroke()',
}

SET_OPERATORS = {
    'FILL': 'fillStyle',
    'STROKE': 'strokeStyle',
    'WIDTH': 'lineWidth',
}

CURSOR_OPERATORS = {
    'M': 'moveTo',
    'L': 'lineTo',
    'C': 'arc',
    'A': 'arc',
    'R': 'rect',
}


def parse_command(command:str) -> str:
    if command.startswith('//'):
        return ''
    js = ''
    if command in DIRECT_OPERATORS:
        js = DIRECT_OPERATORS[command]
    if command.startswith('SET:'):
        operator = command.split(' ')[0].split(':')[1]
        operand = command.split(' ')[1]
        js = 'ctx.' + SET_OPERATORS[operator] + '="' + operand + '"'
    if command.split(' ')[0] in CURSOR_OPERATORS:
        operator = command.split(' ')[0]
        operand = command.split(' ')[1]
        js = 'ctx.' + CURSOR_OPERATORS[operator] + '(' + operand
        if operator == 'C':
            js += ',0,Math.PI*2'
        js += ')'
    return js + ';'
    


def parse(lines:list) -> list:
    js = []

    for line in lines:
        js.append(parse_command(line))

    return js


if __name__ == '__main__':
    if len(sys.argv) > 1:
        FILENAME = sys.argv[1]
    else:
        raise Exception('No file provided')
    if len(sys.argv) > 2:
        OUTPUT_FILE = sys.argv[2]
    else:
        raise Exception('No output provided')
    
    with open(FILENAME) as file:
        lines = file.read().split(';')
        lines = [line.strip() for line in lines]
        
    js = parse(lines)

    with open(OUTPUT_FILE, 'w') as output:
        output.writelines(js)