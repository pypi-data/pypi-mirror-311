from .utils import parse_arg_types

INSPECT_CODES = {
    "POSITIONAL_ONLY": "PO",
    "POSITIONAL_OR_KEYWORD": "PK",
    "VAR_POSITIONAL": "VP",
    "KEYWORD_ONLY": "KO",
    "VAR_KEYWORD": "VK",
}


class ArgsHandler:
    def __init__(self, f, arguments: dict):
        self.default_args = arguments
        self._types_arg = parse_arg_types(f)
        for key, value in self._types_arg.items():
            setattr(self, INSPECT_CODES[key], value)

    def parse_args(self, args: list, kwds: dict):
        new_args = list(args)
        new_kwds = dict()

        # handle POSITIONAL_ONLY arguments
        if len(self.PO) - len(args) > 0:
            for pos in self.PO[len(args) :]:
                if pos in self.default_args:
                    new_args.append(self.default_args[pos])

        # handle POSITIONAL_OR_KEYWORD arguments
        remain_args = args[len(self.PO) : len(self.PO) + len(self.PK)]
        # Positional_Keyword arguments that have passed as positional
        # will be pass to the underlying function as keyword argument
        for ind, p_arg in enumerate(remain_args):
            new_kwds[self.PK[ind]] = p_arg
            # remove positional argument's value that corresponds to keyword now
            new_args.pop(len(self.PO))
        for pk_key in self.PK:
            if (pk_key not in new_kwds) and (pk_key in self.default_args):
                new_kwds[pk_key] = self.default_args[pk_key]

        # handle KEYWORD_ONLYarguments
        for kw_only in self.KO:
            if (kw_only in self.default_args) and (kw_only not in kwds):
                new_kwds[kw_only] = self.default_args[kw_only]

        # will pass all the remaining parameters in the argument environment
        # that are not define in function. Only if its accept Keyword_Var argument

        if self.VK:
            f_parameters = {v for value in self._types_arg.values() for v in value}
            for default_param in self.default_args:
                if default_param not in f_parameters:
                    new_kwds[default_param] = self.default_args[default_param]
        new_kwds.update(kwds)

        # In case function has *args argument and there are enough passed args
        # keyword_positional arguments will be passed as positional
        if len(args) > len(self.PO + self.PK) and self.VP:
            for ind, pk_key in enumerate(self.PK):
                if pk_key in new_kwds:
                    new_args.insert(len(self.PO) + ind, new_kwds.pop(pk_key))
        return new_args, new_kwds

    def __getattr__(self, name):
        if name in INSPECT_CODES.values():
            return []
        return super().__getattr__(name)
