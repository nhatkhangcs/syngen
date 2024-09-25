import pytest
import syngen as syngen
from nguyenpanda.swan import color, yellow

import types
from typing import Set, Tuple, Type


def submodule_classes_info(module: types.ModuleType) -> Tuple[Set[str], Set[Type]]:
    """
    List all class names and class objects defined in the given module.

    Args:
        module (types.ModuleType): The module from which to extract class names and class objects.

    Returns:
        tuple: A tuple containing:
            - A set of class names (as strings) defined in the module.
            - A set of class objects (types) defined in the module.
    """
    name = module.__name__
    classes, objects = syngen.utils.get_classes(module)
    color.print(f'Module {name}', color='m', end=' - ')
    color.print(f'Contains {len(classes)} classes', color='c')
    for cls, obj in zip(classes, objects):
        print('\t-> {: <30} : id = {}'.format(yellow(cls), hex(id(obj))))
    return classes, objects


if __name__ == '__main__':
    print(color['g'] + f'`main` block at file' + color.reset, f'"{__file__}"')

    submodule_classes_info(syngen.attribute)
    submodule_classes_info(syngen.condition)
    submodule_classes_info(syngen.dtype)
