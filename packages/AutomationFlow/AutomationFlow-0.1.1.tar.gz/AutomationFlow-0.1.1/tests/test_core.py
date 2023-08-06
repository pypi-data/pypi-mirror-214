import pytest
import subprocess

@pytest.mark.parametrize(
    "script, expected_output",
    [
#### text block
("""
```text
hi there
```
""", "hi there"),
# text block + text code block
("""
```text
hi {{ 'bob' }}
```
""", "hi bob"),
# text block + text code block with arguments
("""
```text
hi {{ return_s | 'tom' }}
```
""", "hi tom"),
#### code block
("""
```code
x = 1 + 1
print(x)
```
""", "2"),
# markdown
("""
```markdown
hi there
```
""", "hi there"),
#### inline block
 ("""
%% print_twice | 'hi' %%
""", "hi\nhi"),
#### conditional
 ("""
{% if False %}
%% print_twice | 'a' %%
{% else %}
%% print_twice | 'b' %%
{% endif %}
""", "b\nb"),
 ("""
{% if False %}
%% print_twice | 'a' %%
{% elif True %}
%% print_twice | 'b' %%
{% else %}
%% print_twice | 'c' %%
{% endif %}
""", "b\nb"),
 ("""
```text='blah'
hi
```
#### Template
{? block 'blah' ?}
""", "hi"),
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
