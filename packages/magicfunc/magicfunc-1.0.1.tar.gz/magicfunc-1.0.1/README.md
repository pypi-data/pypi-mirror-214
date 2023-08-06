# magicfunc

magicfunc is a Python library that uses LLM to generate function bodies for function signatures and dynamically proxies them at runtime.

[中文文档](README_zh.md)

## Installation

You can install magicfunc using pip:

```bash
pip install magicfunc
```

## Usage

To use magicfunc, you need to define a function signature and pass it to the `magicfunc.magic` decorator. magicfunc will then generate a function body using LLM and dynamically proxy it at runtime.

```python
import magicfunc

@magicfunc.magic
def add(x: int, y: int) -> int:
    """
    Add two integers together.
    """
```

You can then call the function as you would any other function:

```python
result = add(2, 3)
print(result) # Output: 5
```

magicfunc will generate a function body that adds the two integers together and returns the result.

## Configuration

magicfunc can be configured using these variables:

- `DEFAULT_PROVIDER`: The default provider for generate function body.

## Contributing

If you find a bug or have a feature request, please open an issue on GitHub. If you would like to contribute code, please fork the repository and submit a pull request.

## License

magicfunc is licensed under the MIT License. See the LICENSE file for more information.