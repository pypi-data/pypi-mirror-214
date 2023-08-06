
from .default_functions import (
    pause,
    lt, red, green, yellow, blue, magenta, cyan, white,
    print_red, print_green, print_yellow,
    print_blue, print_magenta, print_cyan, print_white
)

BLOCK_START_STRING = '{{'
BLOCK_END_STRING = '}}'
CONDITIONAL_START_STRING = '{%'
CONDITIONAL_END_STRING = '%}'
COMMENT_START_STRING = '{#'
COMMENT_END_STRING = '#}'
TEMPLATE_START_STRING = '{?'
TEMPLATE_END_STRING = '?}'
IF_STRING = 'if'
ELIF_STRING = 'elif'
ELSE_STRING = 'else'
END_STRING = 'endif'

#BLOCK_START_STRING = r'\{\{'
#BLOCK_END_STRING = r'\}\}'
#CONDITIONAL_START_STRING = r'\{%'
#CONDITIONAL_END_STRING = r'%\}'
#COMMENT_START_STRING = r'\{#'
#COMMENT_END_STRING = r'#\}'
#TEMPLATE_START_STRING = r'\{\?'
#TEMPLATE_END_STRING = r'\?\}'
#IF_STRING = 'if'
#ELIF_STRING = 'elif'
#ELSE_STRING = 'else'
#END_STRING = 'endif'

_DEFAULT_CONTEXT_FUNCTIONS = {
    "pause": pause,
    "red": red,
    "green": green,
    "yellow": yellow,
    "blue": blue,
    "magenta": magenta,
    "cyan": cyan,
    "white" : white,
    "print_red": print_red,
    "print_green": print_green,
    "print_yellow": print_yellow,
    "print_blue": print_blue,
    "print_magenta": print_magenta,
    "print_cyan": print_cyan,
    "print_white" : print_white,
}



_DEFAULT_CONTEXT_VARIABLES = {
    "True" : True,
    "False" : False
}
