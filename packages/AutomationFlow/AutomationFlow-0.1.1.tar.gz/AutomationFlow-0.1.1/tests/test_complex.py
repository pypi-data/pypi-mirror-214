import pytest
import subprocess

from AutomationFlow import Runner, Lexer, Parser

@pytest.mark.parametrize(
    "script, expected_output",
    [
#### text block
("""
{# comment #}

```text
hi there

```

```text='if_true'
I am true
```

```text='if_false'
I am false
```

```code
n = 6 > 5
```

{% if n %}
{? block 'if_true' ?}
{% else %}
{? block 'if_false' ?}
{% endif %}

""", "hi there\nI am true"),
    ],
)
def test_runner(script, expected_output):

    command = [
        "python",
        "tests/helper.py",
        f"{script}"
    ]

    # Execute the command and capture the output
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    actual_output = output.decode().strip()

    # Compare the actual output with the expected output
    assert actual_output == expected_output
