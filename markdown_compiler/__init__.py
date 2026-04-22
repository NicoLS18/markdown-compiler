import re
from markdown_compiler.util.line_functions import *


def compile_lines(text):
    lines = text.split('\n')
    new_lines = []
    in_paragraph = False
    in_code_block = False
    for line in lines:
        line = line.strip()
        if line=='':
            if in_paragraph:
                line='</p>'
                in_paragraph = False
        else:
            if line[0:3] == '```':
                if in_code_block:
                    line = '</pre>'
                    in_code_block = False
                else:
                    line = '<pre>'
                    in_code_block = True
            elif line[0] != '#' and not in_paragraph and not in_code_block:
                in_paragraph = True
                line = '<p>\n'+line
            elif in_code_block:
                pass
            else:
                pass
            if not in_code_block:
                line = compile_headers(line)
                line = compile_strikethrough(line)
                line = compile_bold_stars(line)
                line = compile_bold_underscore(line)
                line = compile_italic_star(line)
                line = compile_italic_underscore(line)
                line = compile_code_inline(line)
                line = compile_images(line)
                line = compile_links(line)
        new_lines.append(line)
    if in_paragraph:
        new_lines.append('</p>')
    new_text = '\n'.join(new_lines)
    return new_text


def markdown_to_html(markdown, add_css):
    html = '''
<html>
<head>
    <style>
    ins { text-decoration: line-through; }
    </style>
    '''
    if add_css:
        html += '''
<link rel="stylesheet" href="https://izbicki.me/css/code.css" />
<link rel="stylesheet" href="https://izbicki.me/css/default.css" />
        '''
    html+='''
</head>
<body>
    '''+compile_lines(markdown)+'''
</body>
</html>
    '''
    return html


def minify(html):
    html = re.sub(r'\s+', ' ', html)
    html = html.strip()
    return html


def convert_file(input_file, add_css):
    if input_file[-3:] != '.md':
        raise ValueError('input_file does not end in .md')

    with open(input_file, 'r') as f:
        markdown = f.read()

    html = markdown_to_html(markdown, add_css)
    html = minify(html)

    with open(input_file[:-2]+'html', 'w') as f:
        f.write(html)