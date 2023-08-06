#!/usr/bin/env python3

import re
from collections import defaultdict


def parse(molecule_str: "str") -> "dict[str, int]":
    """
    Parse the molecule input and return the Atoms object.

    digit_exclude_zero ::= '1', '2', '3', '4', '5', '6', '7', '8', '9'
    digit ::= '0' | digit_exclude_zero
    natural_number ::= digit_exclude_zero, {digit}
    atom ::= 'H' | 'He' | 'Li' | 'Be' | 'B' | 'C' | 'N' | 'O' | 'F' | 'Ne' | ... | 'Rg'
    atom_number ::= { atom, natural_number }
    bra ::= '(' | '[' | '{'
    ket ::= ')' | ']' | '}'
    nests ::= bra, { nests | atom_number }, ket, [natural_number]
    molecule ::= [natural_number], nests | atom_number
    """

    def digit_exclude_zero(string: str) -> str:
        global parser_idx
        if parser_idx < len(string) and string[parser_idx].isdigit() and string[parser_idx] != "0":
            parser_idx += 1
            return string[parser_idx - 1]
        return ""

    def digit(string: str) -> str:
        global parser_idx
        if parser_idx < len(string) and string[parser_idx].isdigit():
            parser_idx += 1
            return string[parser_idx - 1]
        return ""

    def natural_number(string: str) -> int:
        """
        This function is a numerical element dedicated to the rational formula.
        If the number is not given, return 1 (e.g) H2O => H2O1
        """
        res = digit_exclude_zero(string)
        while True:
            tmp = digit(string)
            if tmp == "":
                break
            res += tmp
        if res == "":
            return 1
        return int(res)

    def atom(string: str) -> str:
        global parser_idx
        if parser_idx + 2 <= len(string) and string[parser_idx : parser_idx + 2] in elements:
            parser_idx += 2
            return string[parser_idx - 2 : parser_idx]
        elif parser_idx + 1 <= len(string) and string[parser_idx] in elements:
            parser_idx += 1
            return string[parser_idx - 1]
        return ""

    def atom_number(string: str) -> "defaultdict[str, int]":
        # atom_number: { atom, natural_number }
        res: defaultdict[str, int] = defaultdict(int)
        while True:
            atom_str = atom(string)
            atom_num = natural_number(string)
            if atom_str == "":
                break
            res[atom_str] += atom_num
        return res

    def is_bra(string: str) -> bool:
        global parser_idx
        return string[parser_idx] in bra_list

    def is_ket(string: str) -> bool:
        global parser_idx
        return string[parser_idx] in ket_list

    def nests(string: str) -> "defaultdict[str, int]":
        global parser_idx
        # Get the index of the last bra
        parser_idx = max([string.rfind(bra) for bra in bra_list])
        while parser_idx != -1 and parser_idx < len(string):
            start_idx = parser_idx
            # Check bra
            if not is_bra(string):
                raise ValueError(f"Error: Parse error. The character is not in {bra_list}. your input: {string}. Please check your input.")
            parser_idx += 1
            # Check atom_number
            elem_num = atom_number(string)
            # Check ket
            if not is_ket(string):
                raise ValueError(f"Error: Parse error. The character is not in {ket_list}. your input: {string}. Please check your input.")
            parser_idx += 1
            # Check natural_number
            num = natural_number(string)
            # All elem_num values are multiplied by num
            for key in elem_num:
                elem_num[key] *= num
            replace_str = "".join([key + str(elem_num[key]) for key in elem_num])
            end_idx = parser_idx
            string = string[:start_idx] + replace_str + string[end_idx:]  # string is updated
            parser_idx = max([string.rfind(bra) for bra in bra_list])  # Next bra
        # All bra and ket are removed, so the remaining string is only atom_number
        parser_idx = 0  # Reset parser_idx
        return atom_number(string)

    def check_brackets(string: str) -> None:
        re_brackets = re.compile(r"[\(\)\[\]\{\}]")
        brackets_dict = {bra_list[idx]: ket_list[idx] for idx in range(len(bra_list))}
        check_brackets = list()
        brackets = re_brackets.findall(string)
        for c in brackets:
            if c in bra_list:
                check_brackets.append(c)
            else:
                if len(check_brackets) == 0:
                    raise ValueError(f"Error: Parse error. The number of bra is less than the number of ket. your input: {string}. Please check your -m or --mol option.")
                if c != brackets_dict[check_brackets.pop()]:
                    raise ValueError(f"Error: Parse error. Correspondence between brackets is not taken. your input: {string}. Please check your -m or --mol option.")

    def check_invalid_characters(string: str) -> None:
        re_invalid = re.compile(r"[^a-zA-Z\(\)\[\]\{\}0-9]")  # Only alphanumeric characters and brackets are allowed
        str_invalid = re_invalid.findall(string)
        if str_invalid != []:
            raise ValueError(f"Error: Parse error. The character is invalid. your input: {string}, invalid characters: {str_invalid}. Please check your input.")

    def parse_head_number(string: str) -> str:
        """
        (e.g.) H2O => (H2O)1
               3H2O => (H2O)3
        """
        global parser_idx
        parser_idx = 0
        num = natural_number(string)
        start_idx = parser_idx
        if num == 1:
            return string[start_idx:]
        return "(" + string[start_idx:] + ")" + str(num)

    def molecule(string: str):
        global parser_idx
        check_brackets(string)
        check_invalid_characters(string)
        string = parse_head_number(string)
        elem_num = nests(string)
        retval: dict[str, int] = dict()
        for key in elem_num:
            retval[key] = elem_num[key]
        return retval

    molecule_str = molecule_str.replace(" ", "")  # remove all spaces
    # special characters [-=≡] are removed
    molecule_str = re.sub(r"[-=≡]", "", molecule_str)
    global parser_idx
    parser_idx = 0
    bra_list = ["(", "[", "{"]
    ket_list = [")", "]", "}"]
    elements: "list[str]" = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg"]
    return molecule(molecule_str)
