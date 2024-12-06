from functools import wraps
from fillargs.utils import check_attr, clear_attrs
from fillargs.arg_handler import ArgsHandler
from fillargs.env import ArgEnv, getdefault


def fill_function(f=None, reserved_args: dict = None, arg_env: ArgEnv = None):
    def wrapper(f):
        nonlocal reserved_args, arg_env
        if not arg_env:
            arg_env = ArgEnv(reserved_args) if reserved_args else getdefault()
        args_handler = ArgsHandler(f, arg_env.args)

        @wraps(f)
        def wrapped(*args, **kwds):
            args, kwds = args_handler.parse_args(args, kwds)
            return f(*args, **kwds)

        return wrapped

    if f:
        return wrapper(f)
    return wrapper


def fill_method(instance, f, reserved_args: dict = None, arg_env: ArgEnv = None):
    try:
        method = getattr(instance, f)
        wrapped_method = fill_function(method, reserved_args, arg_env)
        setattr(instance, method.__name__, wrapped_method)
    except AttributeError as exc:
        raise exc


def handle_instance(
    instance,
    reserved_args: dict = None,
    arg_env: ArgEnv = None,
    on_names: list = None,
    strict: bool = True,
):
    attrs = dir(instance)

    if on_names:
        for method in on_names:
            if check_attr(method, attrs, strict):
                fill_method(instance, method, reserved_args, arg_env)
        return instance

    good_attrs = clear_attrs(attrs)
    for method in good_attrs:
        fill_method(instance, method, reserved_args, arg_env)
    return instance
