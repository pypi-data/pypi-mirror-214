from src.pymolecule_parser import parse


def test_parser():
    testcases = {
        "H2O": {"H": 2, "O": 1},
        "C6H12O6": {"C": 6, "H": 12, "O": 6},
        "3H2O": {"H": 6, "O": 3},
        "[Co(NH3)6]Cl3": {"Co": 1, "N": 6, "H": 18, "Cl": 3},
    }
    for key, value in testcases.items():
        assert parse(key) == value
