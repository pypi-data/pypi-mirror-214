# pymolecule-parser: A parser for a molecule formula that supports nested brackets

## Installation

```bash
pip install pymolecule-parser
```

## Usage

```python
from pymolecule_parser import parse

parse("H2O") # {'H': 2, 'O': 1}
parse("3H2O") # {'H': 6, 'O': 3}
parse("H2O2(OH)2") # {'H': 4, 'O': 4}
parse("[Co(NH3)6]Cl3") # {'Co': 1, 'N': 6, 'H': 18, 'Cl': 3}
```


## Limitations
The following notations are not supported.
- Ion notations
  - For example, `[Cu(NH3)4]2+` is not supported. Use `Cu(NH3)4` instead.
- middle dot `·`
  - For example, `CuSO4·5H2O` is not supported. Use `CuSO4(H2O)5` instead.

## License

Apache License 2.0

## Author

Kohei Noda
