from collections.abc import Mapping
from uuid import uuid4


class _Register:
    ids = {}

    def register(self, instance, overide=False):
        if hasattr(
            instance,
            "name",
        ) and isinstance(instance, ArgEnv):
            name = instance.name
            if not overide and name in self.ids:
                raise TypeError(f"Instance with name {name} is already registered")
            if name == "default" and name in self.ids:
                if not overide:
                    raise TypeError("Can exist only one default Environment")
            self.ids[name] = instance
        else:
            raise ValueError(
                "Instance doesnt have 'name' attribute or is not a ArgEnv instance"
            )

    def _getenv(self, name):
        try:
            env = self.ids[name]
            return env
        except KeyError as exc:
            raise (f"Environment with {name} name does not exist ") from exc


_register = _Register()


class EnvMeta(type):
    instances = _register

    def __call__(self, *args, **kwargs):
        __instance = super().__call__(*args, **kwargs)
        self.instances.register(__instance, getattr(__instance, "overide"))
        return __instance


class ArgEnv(metaclass=EnvMeta):
    def __init__(self, args: dict, name=None, *, overide=False):
        self._check_args(args)
        self.args = args
        self.name = name if name else "".join(str(uuid4()).split("-")[:2])
        self.overide = overide

    def _check_args(self, args):
        if not isinstance(args, Mapping):
            raise TypeError("Expect a dict-like object for arguments")
        return True


class DefaultEnv(ArgEnv):
    def __init__(self, args=None, *, overide=False):
        super().__init__(args, name="default", overide=overide)


def getenv(name):
    inst = _register._getenv(name)
    return inst


def getdefault():
    try:
        return getenv(name="default")
    except:
        raise AttributeError("Could not find a default environment")
