# -*- coding: utf-8 -*-
# Copyright (c) 2017 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""A pocket full of useful reflection functions!"""

from __future__ import absolute_import
import inspect
import functools

import six
from pockets.collections import listify
from six import string_types


__all__ = [
    'collect_subclasses', 'collect_superclasses',
    'collect_superclass_attr_names', 'is_data', 'resolve']


def collect_subclasses(cls):
    """
    Recursively collects all descendant subclasses that inherit from the
    given class, not including the class itself.

    Note:
        Does not include `cls` itself.

    Args:
        cls (class): The class object from which the collection should begin.

    Returns:
        list: A list of `class` objects that inherit from `cls`. This list
            will not include `cls` itself.
    """
    subclasses = set()
    for subclass in cls.__subclasses__():
        subclasses.add(subclass)
        subclasses.update(collect_subclasses(subclass))
    return list(subclasses)


def collect_superclasses(cls, terminal_class=None, modules=None):
    """
    Recursively collects all ancestor superclasses in the inheritance
    hierarchy of the given class, including the class itself.

    Note:
        Inlcudes `cls` itself. Will not include `terminal_class`.

    Args:
        cls (class): The class object from which the collection should begin.
        terminal_class (class or list): If `terminal_class` is encountered in
            the hierarchy, we stop ascending the tree. `terminal_class` will
            not be included in the returned list.
        modules (string, module, or list): If `modules` is passed, we only
            return classes that are in the given module/modules. This can be
            used to exclude base classes that come from external libraries.

    Returns:
        list: A list of `class` objects from which `cls` inherits. This list
            will include `cls` itself.
    """
    terminal_class = listify(terminal_class)
    if modules is not None:
        modules = listify(modules)
        module_strings = []
        for m in modules:
            if isinstance(m, six.string_types):
                module_strings.append(m)
            else:
                module_strings.append(m.__name__)
        modules = module_strings

    superclasses = set()
    is_in_module = modules is None or cls.__module__ in modules
    if is_in_module and cls not in terminal_class:
        superclasses.add(cls)
        for base in cls.__bases__:
            superclasses.update(
                collect_superclasses(base, terminal_class, modules))

    return list(superclasses)


def collect_superclass_attr_names(cls, terminal_class=None, modules=None):
    """
    Recursively collects all attribute names of ancestor superclasses in the
    inheritance hierarchy of the given class, including the class itself.

    Note:
        Inlcudes `cls` itself. Will not include `terminal_class`.

    Args:
        cls (class): The class object from which the collection should begin.
        terminal_class (class or list): If `terminal_class` is encountered in
            the hierarchy, we stop ascending the tree. Attributes from
            `terminal_class` will not be included in the returned list.
        modules (string, module, or list): If `modules` is passed, we only
            return classes that are in the given module/modules. This can be
            used to exclude base classes that come from external libraries.

    Returns:
        list: A list of `str` attribute names for every `class` in the
            inheritance hierarchy.
    """
    superclasses = collect_superclasses(cls, terminal_class, modules)
    attr_names = set()
    for superclass in superclasses:
        attr_names.update(superclass.__dict__.keys())
    return list(attr_names)


def is_data(obj):
    """
    Returns True if `obj` is a "data like" object.

    Strongly inspired by `inspect.classify_class_attrs`. This function is
    useful when trying to determine if an attribute has a meaningful docstring
    or not. In general, a routine can have meaningful docstrings, whereas
    non-routines cannot.

    See Also:
        * `inspect.classify_class_attrs`
        * `inspect.isroutine`

    Args:
        obj (object): The object in question.

    Returns:
        bool: True if `obj` is "data like", False otherwise.
    """
    if isinstance(obj, (staticmethod, classmethod, property)) or \
            inspect.isroutine(obj):
        return False
    else:
        return True


def resolve(name, modules=None):
    """
    Resolve a dotted name to an object (usually class, module, or function).

    If `name` is a string, attempt to resolve it according to Python
    dot notation, e.g. "path.to.MyClass". If `name` is anything other than a
    string, return it immediately:

    >>> resolve("calendar.TextCalendar")
    <class 'calendar.TextCalendar'>
    >>> resolve(object()) #doctest: +ELLIPSIS
    <object object at 0x...>

    If `modules` is specified, then resolution of `name` is restricted
    to the given modules. Leading dots are allowed in `name`, but they are
    ignored. Resolution **will not** traverse up the module path if `modules`
    is specified.

    If `modules` is not specified and `name` has leading dots, then resolution
    is first attempted relative to the calling function's module, and then
    absolutely. Resolution **will** traverse up the module path. If `name` has
    no leading dots, resolution is first attempted absolutely and then
    relative to the calling module.

    Warning:
        Do not resolve strings supplied by an end user without specifying
        `modules`. Instantiating an arbitrary object specified by an end user
        can introduce a potential security risk.

        To avoid this, restrict the search path by explicitly specifying
        `modules`.

    Restricting `name` resolution to a set of `modules`:

    >>> resolve("pockets.camel") #doctest: +ELLIPSIS
    <function camel at 0x...>
    >>> resolve("pockets.camel", modules=["re", "six"]) #doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    ValueError: Unable to resolve 'pockets.camel' in modules: ['re', 'six']

    Args:
        name (str or object): A dotted name.

        modules (str or list, optional): A module or list of modules, under
            which to search for `name`.

    Returns:
        object: The object specified by `name`.

    Raises:
        ValueError: If `name` can't be resolved.

    """
    if not isinstance(name, string_types):
        return name

    obj_path = name.split('.')
    search_paths = []
    if modules:
        while not obj_path[0]:
            obj_path.pop(0)
        for module_path in listify(modules):
            search_paths.append(module_path.split('.') + obj_path)
    else:
        caller = inspect.getouterframes(inspect.currentframe())[1][0].f_globals
        module_path = caller['__name__'].split('.')
        if not obj_path[0]:
            obj_path.pop(0)
            while not obj_path[0]:
                obj_path.pop(0)
                if module_path:
                    module_path.pop()

            search_paths.append(module_path + obj_path)
            search_paths.append(obj_path)
        else:
            search_paths.append(obj_path)
            search_paths.append(module_path + obj_path)

    for path in search_paths:
        try:
            obj = functools.reduce(getattr, path[1:], __import__(path[0]))
        except (AttributeError, ImportError):
            pass
        else:
            return obj

    raise ValueError(
        "Unable to resolve '{0}' in modules: {1}".format(name, modules))
