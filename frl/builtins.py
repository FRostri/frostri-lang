from typing import (
    cast,
    Dict,
)

from frl.object import (
    Builtin,
    Error,
    Integer,
    Object,
    String,
)

# @jdaroesti

_WRONG_NUMBER_OF_ARGS = '''on the line 1.
Too arguments for the \'get_len\' function. given {}, expected {}'''
_UNSUPPORTED_ARGUMENT_TYPE = '''on the line 1.
Unexpected type argument: expected \'STRING\' recived \'INTEGERS\''''


def get_len(*args: Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 1), '0006')
    elif type(args[0]) == String:
        argument = cast(String, args[0])
        return Integer(len(argument.value), 1)
    else:
        return Error(_UNSUPPORTED_ARGUMENT_TYPE.format("'STRING'", args[0].type().name), '0007')
    return Integer(23, 1)


BUILTINS: Dict[str, Builtin] = {
    'get_len': Builtin(fn=get_len),
}
