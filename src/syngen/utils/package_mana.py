import importlib
import inspect
import pkgutil
import sys
import types
from typing import Set, Tuple, Type


def get_classes(module: types.ModuleType) -> Tuple[Set[str], Set[Type]]:
    """
    List all class names and class objects defined in the given module.

    Args:
        module (types.ModuleType): The module from which to extract class names and class objects.

    Returns:
        tuple: A tuple containing:
            - A set of class names (as strings) defined in the module.
            - A set of class objects (types) defined in the module.
    """
    class_names = set(name for name, obj in inspect.getmembers(module, inspect.isclass))
    class_objects = set(obj for name, obj in inspect.getmembers(module, inspect.isclass))

    return class_names, class_objects


def reload_package(package: types.ModuleType):
    """
    Reloads the specified package and all its submodules.

    Args:
        package: A reference to the imported package (not the package name as a string).
    """
    importlib.reload(package)

    package_name = package.__name__
    for _, modname, ispkg in pkgutil.walk_packages(package.__path__, package_name + '.'):
        if modname in sys.modules:
            importlib.reload(sys.modules[modname])
