from typing import (
    cast,
    Dict,
)

from frl.object import (
    Boolean,
    Builtin,
    Error,
    Float,
    Integer,
    Object,
    String,
)

# @jdaroesti

_WRONG_NUMBER_OF_ARGS = '''on the line 1.
Too many arguments for \'get_len\' function. given {}, expected {}'''
_UNSUPPORTED_ARGUMENT_TYPE = '''on the line 1.
Unexpected type argument: expected \'{}\' recived \'{}\''''


def get_len(*args: Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 1), '0006')
    elif type(args[0]) == String:
        argument = cast(String, args[0])
        return Integer(len(argument.value), 1)
    else:
        return Error(_UNSUPPORTED_ARGUMENT_TYPE.format("STRING", args[0].type().name), '0007')
    return Integer(23, 1)


def println(*args: Object) -> Object:
    if len(args) != 1:
        args_list = list(args)
        string_list = []
        for i in args_list:
            i = cast(String, i)
            string_list.append(str(i.value))

        string_joined = ' '.join(string_list)
        return String(string_joined)
    elif type(args[0]) == String:
        argument = cast(String, args[0])
        return String(argument.value)
    elif type(args[0]) == Float:
        argument = cast(String, args[0])
        return Float(argument.value, 1)
    elif type(args[0]) == Integer:
        argument = cast(String, args[0])
        return Integer(argument.value, 1)
    elif type(args[0]) == Boolean:
        argument = cast(String, args[0])
        return Boolean(argument.value)
    else:
        return Error(_UNSUPPORTED_ARGUMENT_TYPE.format("STRING | FLOAT | INTEGER | BOOLEAN", args[0].type().name), '0007')


BUILTINS: Dict[str, Builtin] = {
    'get_len': Builtin(fn=get_len),
    'print': Builtin(fn=println),
}
