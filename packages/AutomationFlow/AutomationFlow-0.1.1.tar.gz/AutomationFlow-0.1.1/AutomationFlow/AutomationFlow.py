
import re
import sys
from string import Template
from time import sleep

# for markdown
from rich.markdown import Markdown
from rich.console import Console

from loguru import logger

from .defaults import (
    _DEFAULT_CONTEXT_FUNCTIONS,
    _DEFAULT_CONTEXT_VARIABLES
)

CODE_START_STRING = '```code'
CODE_END_STRING = '```'
TEXT_START_STRING = '```text'
TEXT_END_STRING = '```'
MARKDOWN_START_STRING = '```markdown'
MARKDOWN_END_STRING = '```'
INLINE_BLOCK_START_STRING = r'\%\%'
INLINE_BLOCK_END_STRING = r'\%\%'
CONDITIONAL_START_STRING = r'\{\%'
CONDITIONAL_END_STRING = r'\%\}'
COMMENT_START_STRING = r'\{#'
COMMENT_END_STRING = r'#\}'
TEMPLATE_START_STRING = r'\{\?'
TEMPLATE_END_STRING = r'\?\}'
PIPE_STRING = "|"
IF_STRING = 'if'
ELIF_STRING = 'elif'
ELSE_STRING = 'else'
END_STRING = 'endif'

TOKEN_TEXT = 'TEXT'
TOKEN_TEXT2 = 'TEXT2'
TOKEN_CODE = 'CODE'
TOKEN_MARKDOWN = 'MARKDOWN'
TOKEN_INLINEBLOCK = 'INLINEBLOCK'
TOKEN_CONDITIONAL = 'CONDITIONAL'
TOKEN_TEMPLATE = 'TEMPLATE'
TOKEN_COMMENT = 'COMMENT'

class Runner:

    def __init__(self, script_text=None, script_fpath=None, _context=None, print_delay=0.01):

        logger.add("logs/app_{time}.log")

        #logger.add("errors.log", level="ERROR") # Add a file sink to log only ERROR level messages to a file
        #logger.add(sys.stderr, level="ERROR") # Print error level messages to console

        if script_text and script_fpath:
            emsg = f'''
            Error:

            Only one of target_script or target_fpath can be inputted.

            e.g.

            Runner(target_script="""
            ```text
            hi there
            """)

            vs

            Runner(target_fpath="/path/to/script.md")

            Inputs:

            script_text: {script_text}
            script_fpath: {script_fpath}
            '''

            logger.error(emsg)
            sys.exit()

        try:
            if script_text:
                script = script_text
            else:
                with open(script_fpath, "r") as f:
                    script = f.read()
        except (FileNotFoundError, IOError) as e:
            emsg = f'''
            Error:

            target_script must be valid script as a string, OR a filepath
            to a script file.

            {e}
            '''

            logger.error(emsg)
            sys.exit()


        self.script = Parser(script,
               _context = _context,
               print_delay = print_delay
        )

    def run(self):
        self.script.execute()

class Lexer:
    def __init__(self):

        self.rules = [
            #(TOKEN_ASSIGNMENT, r'\{\{\s*(?P<variable>[^\s=]+)\s*=\s*(?P<value>[^}]+)\s*\}\}'),
            (TOKEN_CODE, rf'{CODE_START_STRING}(.*?){CODE_END_STRING}', re.DOTALL),
            (TOKEN_TEXT, rf'{TEXT_START_STRING}(.*?){TEXT_END_STRING}', re.DOTALL),
            (TOKEN_MARKDOWN, rf'{MARKDOWN_START_STRING}(.*?){MARKDOWN_END_STRING}', re.DOTALL),
            (TOKEN_INLINEBLOCK, rf'{INLINE_BLOCK_START_STRING}(.*?){INLINE_BLOCK_END_STRING}', re.DOTALL),
            (TOKEN_CONDITIONAL, rf'{CONDITIONAL_START_STRING}(.*?){CONDITIONAL_END_STRING}', re.DOTALL),
            (TOKEN_TEMPLATE, rf'{TEMPLATE_START_STRING}(.*?){TEMPLATE_END_STRING}', re.DOTALL),
            (TOKEN_COMMENT, rf'{COMMENT_START_STRING}(.*?){COMMENT_END_STRING}', re.DOTALL),
            (TOKEN_TEXT2, r'[^{}$]', re.DOTALL)
        ]

        self.patterns = [(token_type, re.compile(pattern, flags)) for token_type, pattern, flags in self.rules]

    def tokenize(self, script):
        pos = 0

        while pos < len(script):
            for token_type, pattern in self.patterns:
                match = pattern.match(script, pos)
                if match:
                    token_value = match.group().strip()
                    yield (token_type, token_value)
                    pos = match.end()
                    break
            else:

                emsg = f'''
                Failed while tokenizing
                
                Location: Lexer.tokenize

                Expected:

                Valid token.

                Got:

                Invalid token at position {pos}: {script[pos]}
                
                {list(script[pos-10:pos+10])}
                '''

                logger.error(emsg)
                sys.exit()

        #logger.debug("Tokenization complete")
    
class Parser:

    def __init__(self, script, _context=None, print_delay=0.015):

        self.script = script
        self.index = 0  # Initialize the index variable to 0
        self.context = _DEFAULT_CONTEXT_FUNCTIONS.copy()
        self.layers = []
        self.console = Console()
        self.print_delay = print_delay

        if _context is not None:
            self.context.update(_context)

        if "blocks" not in self.context:
            self.context["blocks"] = {}

        self.lexer = Lexer()

        try:
            self.token_generator = self.lexer.tokenize(self.script)
        except Exception as e:

            emsg = f'''
            Lexer exception
            
            {e}

            Expected:

            Lexer to produce a valid Generator via self.lexer.tokenize

            Got:

            It didn't.
            '''

            logger.error(emsg)

            sys.exit()


    def execute(self):
        self.run()

    def advance(self):
        self.index += 1

    def run(self):
        for token in self.token_generator:
            token_type = token[0]
            token_value = token[1:]

            if token_type == TOKEN_TEXT2:
                self.advance()
                continue

            if token_type == TOKEN_CONDITIONAL:
                self.parse_conditional_block(token_value[0])
                self.advance()
                continue

            if self.layers and self.layers[-1]["cond"] != "triggered":
                self.advance()
                continue

            if token_type == TOKEN_COMMENT:
                pass
            elif token_type == TOKEN_INLINEBLOCK:
                self.parse_inline_block(token_value[0])
            elif token_type == TOKEN_CODE:
                self.parse_code_section(token_value[0])
            elif token_type == TOKEN_TEXT:
                self.parse_text_section(token_value[0])
            elif token_type == TOKEN_MARKDOWN:
                self.parse_markdown_section(token_value[0])
            elif token_type == TOKEN_TEMPLATE:
                self.parse_template_block(token_value[0])

            self.advance()


    def parse_template_block(self, template_block):

        _type, value = template_block.strip("\{\}? ").split(" ", 1)
        value = value.strip("'").strip('"')

        if _type == "script":
            self.execute_template(value)
        elif _type == "block":
            self.run_block(value)
        else:
            emsg = f'''

            Failed to parse template block
                            
            Expected:
            
            Valid block type i.e. scripts/block
            
                e.g.
                
                {{? script 'path/to/script' ?}}
                {{? block 'introduction' ?}}

            Got:
            
            Invalid block type {value}
                            
            '''

            logger.error(emsg)
            sys.exit()

    def execute_template(self, fpath):

        new_script = Runner(
            fpath,
            _context=self.context,
        )

        new_script.run()

    def run_block(self, value):

        if value in self.context["blocks"]:

            _type = self.context["blocks"][value]["type"]
            content = self.context["blocks"][value]["content"]

            if _type == "text":
                self.display_text_section(content)
            elif _type == "code":
                self.exec_code(content)
            elif _type == "markdown":
                self.console.print(content)
            else:
                emsg = f'''

                    Invalid block type

                    Expected:

                    block of type: text, code, markdown blocks

                    e.g.

                    ```text="bob"
                    ```

                    ```markdown="header"
                    ```

                    Got:

                    block of type {_type} which isn't currently supported.
                    
                    
                '''

                logger.error(emsg)
                sys.exit()

        else:
            emsg = '''

                Block template not found

                Expected:

                A valid block name in self.context

                e.g. initialize the block previously to be able to
                call it

                e.g.

                ```text="hello"
                hello, bonjour, hola
                ```

                {{? block 'hello' ?}}

                Got:

                No block {0}

                These are the current stored blocks:

                {1}

            '''.format(
                value,
                self.context["blocks"].keys()
            )

            logger.error(emsg)
            sys.exit()


    def replace_template(self, s):
        template = Template(s)
        try:
            result = template.substitute(self.context)
            return result
        except KeyError as e:

            key = str(e)
            emsg = f'''
            Key not found in self.context - key: {key}

            Given content: {s[:50] if len(s) < 50 else s[:50] + "..."}
            '''
            logger.error(emsg)

        except Exception as e:
            emsg = f'''
            Error: {e}

            Given content: {s[:50] if len(s) < 50 else s[:50] + "..."}
            '''
            logger.error(emsg)


    def print_slowly(self, text, _delay=None):

        if _delay is None:
            _delay = self.print_delay

        for c in text:
          print(c, end="", flush=True)
          sleep(_delay)

    def display_text_section(self, text):

        if "{{" not in text:
            self.print_slowly(text)
            return

        index = 0

        while index < len(text):

            if text.startswith("{{", index):

                start = index + 2
                end = text.find("}}", start)

                if end == -1:
                    return self.print_slowly(text[start:])

                script_block = text[start:end].strip()

                optional = self.execute_script_block(script_block)
                
                if optional:
                    self.print_slowly(optional)

                index = end + len("}}")

                continue

            self.print_slowly(text[index])
            index += 1

    def parse_text_section(self, text_section):

        if text_section == "":
            return

        title, content = text_section.split("\n", 1)
        if "=" in title:
            title = title.split("=")[1]
            title = title.strip('"').strip("'").strip(" ")
        else:
            title = ""

        content = content[:-4]
        content = self.replace_template(content)

        if title == "":

            self.display_text_section(content)

        else:

            self.context["blocks"][title] = {
                "type" : "text",
                "content" : content
            }

    def parse_markdown_section(self, text_section):

        if text_section == "":
            return

        title, content = text_section.split("\n", 1)
        if "=" in title:
            title = title.split("=")[1]
            title = title.strip('"').strip("'").strip(" ")
        else:
            title = ""

        content = content[:-4]
        content = self.replace_template(content)
        content = Markdown(content)

        if title == "":

            self.console.print(content)

        else:

            self.context["blocks"][title] = {
                "type" : "markdown",
                "content" : content
            }

    def exec_code(self, code):

        try:
            exec(code, self.context)

            del self.context["__builtins__"]
        except Exception as e:
            emsg = f'''
            Attempted to execute code block, but failed.

            Expected: success

            Got:

            {e}

            given code

            {code if len(code) < 50 else code[:50] + "..."}
            '''

            logger.error(emsg)
            sys.exit()

    def parse_code_section(self, text_section):
        title, content = text_section.split("\n", 1)
        if "=" in title:
            title = title.split("=")[1]
            title = title.strip('"').strip("'").strip(" ")
        else:
            title = ""

        content = content[:-4]

        if title == "":

            self.exec_code(content)

        else:

            self.context["blocks"][title] = {
                "type" : "code",
                "content" : content
            }

    def check_condition(self, condition):
        return self.execute_script_block(condition)

    def parse_conditional_block(self, conditional_block):

        if END_STRING in conditional_block:
            self.layers.pop()
            return

        if self.layers and self.layers[-1]["cond"] == "triggered":

            if (ELIF_STRING in conditional_block or
                ELSE_STRING in conditional_block):

                self.layers[-1]["cond"] = "passed"

                return

        if f" {IF_STRING}" in conditional_block:

            if self.layers and self.layers[-1]["cond"] == "passed":
                self.layers.append({
                    "cond" : "passed"
                })
                return

            self.layers.append({
                "cond" : "new"
            })


        if self.layers and self.layers[-1]["cond"] == "passed":
            return

        if ELSE_STRING in conditional_block:

            self.layers[-1]["cond"] = "triggered"
            flag = True

        else:

            end = conditional_block.find(IF_STRING)

            if end == -1:
                raise ValueError("No yada yada")

            condition = conditional_block[end + len(IF_STRING):-(len(CONDITIONAL_END_STRING) - 1)].strip()
            core_condition = condition.strip()

            flag = self.check_condition(core_condition)

        if flag:
            self.layers[-1] = {
                "cond" : "triggered"
            }

    def parse_inline_block(self, script_block):

        script_block = script_block.strip('% ')

        self.execute_script_block(script_block)


    def execute_script_block(self, script_block):
        parts = [part.strip() for part in script_block.split("|")]
        stack = []

        while parts:
            arg = parts.pop()

            # case: default variable e.g. True, False
            if arg in _DEFAULT_CONTEXT_VARIABLES:
                arg = _DEFAULT_CONTEXT_VARIABLES[arg]
                stack.append(arg)

            else:

                # case: new argument
                if arg not in self.context:

                    if arg[0] in ('"', "'"):
                        arg = arg.strip('"')
                        arg = arg.strip("'")
                    else:
                        try:
                            arg = eval(arg)
                        except Exception as e:
                            print(e)
                            raise

                    stack.append(arg)

                # argument in context
                else:

                    v = self.context[arg]

                    # case: variable
                    if not callable(v):

                        stack.append(v)

                    # case: function/callable
                    else:

                        f = v

                        if stack:
                            r = f(self.context, *stack)
                        else:
                            r = f(self.context, None)

                        stack = []
                        if r != None:
                            stack.append(r)

        if stack:
            return stack[0]
