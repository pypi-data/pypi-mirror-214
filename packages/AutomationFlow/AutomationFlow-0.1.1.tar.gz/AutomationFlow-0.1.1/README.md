# AutomationFlow

A jupyter inspired automation 'language' for creating more readable (literate programming) automation (python) scripts.

I like to use jupyter for scripting nowadays, but it's not always an option especially when in the terminal.

Table of Contents
=================

- [AutomationFlow](#automationflow)
- [Table of Contents](#table-of-contents)
- [General Approach](#general-approach)
- [The Runner Class](#the-runner-class)
- [Main Rules](#main-rules)
    - [Comment block](#comment-block)
    - [Inline functions](#inline-functions)
    - [text block](#text-block)
      - [template block](#template-block)
      - [code block](#code-block)
      - [markdown block](#markdown-block)
      - [conditional block](#conditional-block)
- [Misc/Design Decisions](#miscdesign-decisions)
- [Why use it?](#why-use-it)

# General Approach

Turns something like,

````
```markdown
# Dictionary Example
```

```text

initializing dictionary, please wait..

```

```code
import time

T = initialize()
```

```text
Initialization complete! (actual initialization of the Trie is faster, this just for "pretty" reasons)


```

```code
prefixsearch(T)
```

%% print_green | "exiting... see you next time\n" %%

```code
time.sleep(1)
```
````

into 

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                  Dictionary Example                                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

initializing dictionary, please wait..
466500/466550 words [###################]
Initialization complete! (actual initialization of the Trie is faster, this just for "pretty" reasons)

Please enter a word or a prefix to search for,
or enter HELP for more options
or enter EXIT close this application

> hello

Results: 5 words in total that start with hello

hello
helloed
helloes
helloing
hellos


Please enter a word or a prefix to search for,
or enter HELP for more options
or enter EXIT close this application

> goodby

Results: 4 words in total that start with goodby

goodby
goodbye
goodbyes
goodbys


Please enter a word or a prefix to search for,
or enter HELP for more options
or enter EXIT close this application

> EXIT
exiting... see you next time
```

where the file being run looks like,

```

from Trie import DTrie
from AutomationFlow.AutomationFlow import Runner

r = Runner(script_fpath="script.md",
  _context = {
    "initialize" : initialize,
    "prefixsearch" : prefix_search,
})

r.run()

```

check out the examples directory for more..

# The Runner Class 

Arguments,

script_text str
 - The script as a text. If provided script_fpath cannot be provided.

script_fpath
 - path to the script file. If provided script_text cannot be provided.

_context
 - A dictionary with keys and values that will be reference-able within the script.

print_delay=0.01
 - Time delay between the printing of each character. 0.01 default, which is relatively fast.

# Main Rules

### Comment block

Open with **{#**, close with **#}**.

````
{# this is a comment #}

{#
  this is a comment to
#}
````

### Inline functions

Open with **%%**, and close with **%%**.

````
%% countdown | 50 | 5 %%
````

=> countdown(50, 5)

````
%% func | arg1 | arg2 | func2 | arg3 %%
````

=> func(arg1, arg2, func2(arg3))

Inline functions are for quick calling of functions, for more complicated code it's better to use a code block.

Functions have to be findable in the context dictionary of the Runner.

There are a few inbuilt functions provided in the context. 

note. inline functions have to have a default state variable, that allows the function to access things in the context.

```
def get_meaning(state, word):
    return state['Dictionary'].get_meaning(word)
```

### text block

Text blocks start with a \```text, then have a newline for the text block's content, and then finally they end with another set of \```.

````
```text
hello there this is a text block
```
````

This is a generic text block.

````
```text
you can also display variables stored in the context here. e.g.

hello my name is ${name} will display what the variable name references.
```
````

````
```text
Hi there {{ print_yellow | name }}
```
````

You can call inline functions in text blocks, however instead of starting and ending with **%%**, you start with **{{** and end with **}}**.

````
```text="block_name"
something something
```
````

This is a text with a block name, it won't be displayed straight away, instead you can reference it and display it once or many times over using a template block.

````
{? block "block_name" ?}

{? block "block_name" ?}
````

This will display the text block "block_name" two times.

#### template block

Template blocks start with **{?** and end with **?}**, and MUST have either a
block or a string indentifier prior to a string.

````
{? block "block_name" ?}

{? script "path/to/script" ?}
````

block => this is a template block that will display a block stored in the context

script => this is a script block that will open and parse a script in the given location

#### code block

Code blocks are equivilent to text blocks and start with \```code and end with \```.

````
```code
import math

n = 4
print(math.sqrt(n))
```
````

=> prints 2.0

variables defined in the code block will be stored in the context for later use.

The handling for code blocks isn't the most sophisiticated and it's intented use is meant
to be assistive for than for complex action.

````
```code="code_block_name"
# some code
```
````

Same with text blocks, code blocks can have block names and be called via a template block.o

#### markdown block

````
```markdown
# hi there
```
````

Uses the rich library to display markdown. Added more as a nice to have than anything, hence it's not majorly supported.

#### conditional block

Like most templating frameworks, it's possible to do basic conditional handling in AutomationFlow

Conditional blocks start with **{%** and end with **%}**.

````

```code
n = 10
```

{% if func | n %}

  {# do this if func(n) == True #}

{% elif func2 | n %}

  {# do this instead if func2(n) == True after func(n) turns out to be False # }

{% else %}

  {# do this if the previous two don't result in True #}

{% endif %}
````

Conditional blocks have to start with {% if something %} and have to have a {% endif %} block.

# Misc/Design Decisions

I had initially created a more writing like system, one that preserved white space so the resulting
script looked more like it was in one single block.

However, I eventually ended up choosing to go with a more jupyter inspired system, seperating
code and text oriented blocks as while it's less pretty, it's significantly easier to follow
what is going on.

Some more coding related choices

- Lexer -> Parser
- Uses a simple recursive descent technique.

# Why use it?

Literate Automation scripting.

1) Scripts can and do go wrong.
2) Scripts shouldn't be black boxes.
3) Providing help and explainations to the reader can be boring to do when
   code and user facing 'text' is seperated. Seperation causes friction.

By being able to mix the coding part of scripting, with the user facing part,
it's a lot smoother and friction-less to add more explainations.