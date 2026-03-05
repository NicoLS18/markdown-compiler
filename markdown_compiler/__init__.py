'''
This file contains functions that work on entire documents at a time
(and not line-by-line).
'''

from markdown_compiler.util.line_functions import *  # noqa: F401,F403


def compile_lines(text):
    r'''
    Apply all markdown transformations to the input text.

    NOTE:
    This function calls all of the functions you created above to convert the full markdown file into HTML.
    This function also handles multiline markdown like <p> tags and <pre> tags;
    because these are multiline commands, they cannot work with the line-by-line style of commands above.

    NOTE:
    The doctests are divided into two sets.
    The first set of doctests below show how this function adds <p> tags and calls the functions above.
    Once you implement the functions above correctly,
    then this first set of doctests will pass.

    NOTE:
    For your assignment, the most important thing to take away from these test cases is how multiline tests can be formatted.

    >>> compile_lines('This is a **bold** _italic_ `code` test.\nAnd *another line*!\n')
    '<p>\nThis is a <b>bold</b> <i>italic</i> <code>code</code> test.\nAnd <i>another line</i>!\n</p>'

    >>> compile_lines("""
    ... This is a **bold** _italic_ `code` test.
    ... And *another line*!
    ... """)
    '\n<p>\nThis is a <b>bold</b> <i>italic</i> <code>code</code> test.\nAnd <i>another line</i>!\n</p>'

    >>> print(compile_lines("""
    ... This is a **bold** _italic_ `code` test.
    ... And *another line*!
    ... """))
    <BLANKLINE>
    <p>
    This is a <b>bold</b> <i>italic</i> <code>code</code> test.
    And <i>another line</i>!
    </p>

    >>> print(compile_lines("""
    ... *paragraph1*
    ...
    ... **paragraph2**
    ...
    ... `paragraph3`
    ... """))
    <BLANKLINE>
    <p>
    <i>paragraph1</i>
    </p>
    <p>
    <b>paragraph2</b>
    </p>
    <p>
    <code>paragraph3</code>
    </p>

    NOTE:
    This second set of test cases tests multiline code blocks.

    HINT:
    In order to get some of these test cases to pass,
    you will have to both add new code and remove some of the existing code that I provide you.

    >>> print(compile_lines("""
    ... ```
    ... x = 1*2 + 3*4
    ... ```
    ... """))
    <BLANKLINE>
    <pre>
    x = 1*2 + 3*4
    </pre>
    <BLANKLINE>

    >>> print(compile_lines("""
    ... Consider the following code block:
    ... ```
    ... x = 1*2 + 3*4
    ... ```
    ... """))
    <BLANKLINE>
    <p>
    Consider the following code block:
    <pre>
    x = 1*2 + 3*4
    </pre>
    </p>

    >>> print(compile_lines("""
    ... Consider the following code block:
    ... ```
    ... x = 1*2 + 3*4
    ... print('x=', x)
    ... ```
    ... And here's another code block:
    ... ```
    ... print(this_is_a_variable)
    ... ```
    ... """))
    <BLANKLINE>
    <p>
    Consider the following code block:
    <pre>
    x = 1*2 + 3*4
    print('x=', x)
    </pre>
    And here's another code block:
    <pre>
    print(this_is_a_variable)
    </pre>
    </p>

    >>> print(compile_lines("""
    ... ```
    ... for i in range(10):
    ...     print('i=',i)
    ... ```
    ... """))
    <BLANKLINE>
    <pre>
    for i in range(10):
        print('i=',i)
    </pre>
    <BLANKLINE>

    NOTE:
    This third set of test cases tests ordered lists.

    >>> print(compile_lines("""
    ... 1. this
    ... 2. is
    ... 3. a list
    ... """))
    <BLANKLINE>
    <ol>
    <li>this</li>
    <li>is</li>
    <li>a list</li>
    </ol>

    >>> print(compile_lines("""
    ... Some text before:
    ... 1. **bold** item
    ... 2. *italic* item
    ... """))
    <BLANKLINE>
    <p>
    Some text before:
    <ol>
    <li><b>bold</b> item</li>
    <li><i>italic</i> item</li>
    </ol>
    </p>

    >>> print(compile_lines("""
    ... 1. first
    ... 2. second
    ...
    ... Normal paragraph.
    ... """))
    <BLANKLINE>
    <ol>
    <li>first</li>
    <li>second</li>
    </ol>
    <p>
    Normal paragraph.
    </p>
    '''
    lines = text.split('\n')
    new_lines = []
    in_paragraph = False
    in_pre = False
    in_list = False
    for line in lines:
        if in_pre:
            if line.strip() == '```':
                new_lines.append('</pre>')
                in_pre = False
            else:
                new_lines.append(line)
        elif line.strip() == '```':
            in_pre = True
            new_lines.append('<pre>')
        else:
            line = line.strip()
            # detect ordered list item: starts with digits followed by '. '
            is_list_item = False
            list_text = ''
            i = 0
            while i < len(line) and line[i].isdigit():
                i += 1
            if i > 0 and i + 1 < len(line) and line[i] == '.' and line[i + 1] == ' ':
                is_list_item = True
                list_text = line[i + 2:]
            if line == '':
                closed = False
                if in_list:
                    new_lines.append('</ol>')
                    in_list = False
                    closed = True
                if in_paragraph:
                    new_lines.append('</p>')
                    in_paragraph = False
                    closed = True
                if not closed:
                    new_lines.append(line)
            elif is_list_item:
                if not in_paragraph and not in_list:
                    in_list = True
                    new_lines.append('<ol>')
                elif in_paragraph and not in_list:
                    in_list = True
                    new_lines.append('<ol>')
                list_text = compile_headers(list_text)  # noqa: F405
                list_text = compile_strikethrough(list_text)  # noqa: F405
                list_text = compile_bold_stars(list_text)  # noqa: F405
                list_text = compile_bold_underscore(list_text)  # noqa: F405
                list_text = compile_italic_star(list_text)  # noqa: F405
                list_text = compile_italic_underscore(list_text)  # noqa: F405
                list_text = compile_code_inline(list_text)  # noqa: F405
                list_text = compile_images(list_text)  # noqa: F405
                list_text = compile_links(list_text)  # noqa: F405
                new_lines.append('<li>' + list_text + '</li>')
            else:
                if in_list:
                    new_lines.append('</ol>')
                    in_list = False
                if line[0] != '#' and not in_paragraph:
                    in_paragraph = True
                    line = '<p>\n' + line
                line = compile_headers(line)  # noqa: F405
                line = compile_strikethrough(line)  # noqa: F405
                line = compile_bold_stars(line)  # noqa: F405
                line = compile_bold_underscore(line)  # noqa: F405
                line = compile_italic_star(line)  # noqa: F405
                line = compile_italic_underscore(line)  # noqa: F405
                line = compile_code_inline(line)  # noqa: F405
                line = compile_images(line)  # noqa: F405
                line = compile_links(line)  # noqa: F405
                new_lines.append(line)
    new_text = '\n'.join(new_lines)
    return new_text


def markdown_to_html(markdown, add_css):
    '''
    Convert the input markdown into valid HTML,
    optionally adding CSS formatting.

    NOTE:
    This function is separated out from the `compile_lines` function so that the doctests are much simpler.
    In particular, by splitting these functions in two,
    there's no need to add all of the HTML boilerplate code to the doctests in `compile_lines`.

    NOTE:
    The code for this function is simple enough that we don't even have a "real" doctest.
    The only purpose of this doctest is to run the function and ensure that there are no errors.
    The `assert` function prints no output whenever the input is "truthy".

    >>> assert(markdown_to_html('this *is* a _test_', False))
    >>> assert(markdown_to_html('this *is* a _test_', True))
    '''

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
    html += '''
</head>
<body>
    ''' + compile_lines(markdown) + '''
</body>
</html>
    '''
    return html


def minify(html):
    r'''
    Remove redundant whitespace (spaces and newlines) from the input HTML,
    and convert all whitespace characters into spaces.

    NOTE:
    When we transfer HTML files over the internet,
    we'd like them to be as small as possible in order to save bandwidth and make the webpage load faster.
    Minifying html documents is an important step for webservers.
    It may not seem like much, but at the scale of Google/Facebook,
    it can reduce costs by millions of dollars annually.

    >>> minify('       ')
    ''
    >>> minify('   a    ')
    'a'
    >>> minify('   a    b        c    ')
    'a b c'
    >>> minify('a b c')
    'a b c'
    >>> minify('a\nb\nc')
    'a b c'
    >>> minify('a \nb\n c')
    'a b c'
    >>> minify('a\n\n\n\n\n\n\n\n\n\n\n\n\n\nb\n\n\n\n\n\n\n\n\n\n')
    'a b'
    '''
    return ' '.join(html.split())


def convert_file(input_file, add_css):
    '''
    Convert the input markdown file into an HTML file.
    If the input filename is `README.md`,
    then the output filename will be `README.html`.

    NOTE:
    It is difficult to write meaningful doctests for functions that deal with files.
    This is because we would have to create a bunch of different files to do so.
    Therefore, there are no tests for this function.
    But we can still be confident that this function will work because of the extensive tests on the "helper functions" that this function depends on.
    '''

    # validate that the input file is a markdown file
    if input_file[-3:] != '.md':
        raise ValueError('input_file does not end in .md')

    # load the input file
    with open(input_file, 'r') as f:
        markdown = f.read()

    # generate the HTML from the Markdown
    html = markdown_to_html(markdown, add_css)
    html = minify(html)

    # write the output file
    with open(input_file[:-2] + 'html', 'w') as f:
        f.write(html)
