from termcolor import colored

__COLOR_ENABLED = True

text_settings = {
    'process':      ('cyan', []),
    'result_head':  ('magenta', []),
    'result':       ('white', []),
    'key':          ('yellow', []),
    'link':         ('green', ['underline']),
    'error':        ('red', ['bold']),
    'warning':      ('red', ['bold', 'dark']),
}

all_colors = [
    'grey',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white'
]

"""
avalable attributes
    'bold'
    'dark'
    'underline'
    'blink'
    'reverse'
    'concealed'
"""

def config_colorization (enabled):
    global __COLOR_ENABLED
    __COLOR_ENABLED = False if enabled == 'FALSE' else True
    
def __convert_to_color (value, color, attrs):
    if __COLOR_ENABLED:
        return colored(str(value), color, attrs=attrs)
    else:
        return str(value)

# color-based converter functions
for color in all_colors:
    exec('def t_{0} (value, attrs=[]): return __convert_to_color(value, "{0}", attrs)'.format(color))

for purpose, args in text_settings.items():
    exec('def t_{0} (value): return t_{1}(value, attrs={2})'.format(purpose, *args))

'''
# purpose-based converter functions
def t_process (value):
    return t_cyan(value)

def t_result_head (value):
    return t_magenta(value)

def t_result (value):
    return t_white(value)

def t_key (value):
    return t_yellow(value)

def t_link (value):
    return t_green(value, attrs=['underline'])

def t_error (value):
    return t_red(value, attrs=['bold'])

def t_warning (value):
    return t_red(value, attrs=['bold','dark'])

# print wrapping for convenience
def print_process (value, *a):
    print(t_process(value), *a)

def print_result_head (value, *a):
    print(t_result_head(value), *a)
    
def print_result (value, *a):
    print(t_result(value), *a)

def print_key (value, *a):
    print(t_key(value), *a)

def print_link (value, *a):
    print(t_link(value), *a)
    
def print_error (value, *a):
    print(t_error(value), *a)

def print_warning (value, *a):
    print(t_warning(value) *a)

def _expand_print (func, *a):
    print(*map(func,a))
'''
