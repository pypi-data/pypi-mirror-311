from collections import defaultdict
from inspect import signature


def check_attr(attr: str, total_attrs: list, strict=True):
    for curr_attr in total_attrs:
        if strict and attr == curr_attr:
            return True
        elif not strict and attr in curr_attr:
            return True
    return False


def no_magic_attrs(attrs: list):
    attrs = [
        attr for attr in attrs if not (attr.startswith("__") and attr.endswith("__"))
    ]
    return attrs


def no_private_attrs(attrs: list):
    attrs = [attr for attr in attrs if attr.startswith("_")]
    return attrs


def clear_attrs(attrs: list):
    attrs = no_magic_attrs(attrs)
    attrs = no_private_attrs(attrs)
    return attrs


def parse_arg_types(f):
    """
    Returns a dictionary with argument's types (positional,keywords,etc.) of the function as keys
    and the arguments that belongs to each category.
    """
    args_types = defaultdict(list)
    for arg in signature(f).parameters.values():
        args_types[arg.kind.name].append(arg.name)
    return args_types
